"""Mechanics checks, not semantic acceptance or external-value validation."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import unittest


DIRECTORY = Path(__file__).resolve().parents[1] / "drafts/cutoff-ledger-2026-11-06"
SPEC = importlib.util.spec_from_file_location("cutoff_replay", DIRECTORY / "replay.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CutoffLedgerTests(unittest.TestCase):
    def setUp(self):
        self.ledger = json.loads((DIRECTORY / "ledger.json").read_text())

    def at(self, cutoff=100):
        return MODULE.replay(self.ledger, cutoff)

    def keep(self, cutoff):
        self.ledger["events"] = [e for e in self.ledger["events"] if e["seq"] <= cutoff]

    def append(self, template, **changes):
        event = deepcopy(template)
        event.update(changes)
        event["seq"] = self.ledger["events"][-1]["seq"] + 1
        self.ledger["events"].append(event)
        return event

    def assert_a(self, state, cutoff=100):
        result = self.at(cutoff)
        self.assertEqual(result["tasks"]["A"]["state"], state)
        self.assertEqual(result["current_input_acceptance"]["denominator"], 2)
        self.assertEqual(sum(result["counts"].values()), 2)
        return result

    def test_recorded_results_match_replay_without_mutation(self):
        before = deepcopy(self.ledger)
        actual = {name: self.at(cutoff) for name, cutoff in self.ledger["checkpoints"].items()}
        self.assertEqual(actual, json.loads((DIRECTORY / "results.json").read_text()))
        self.assertEqual(self.ledger, before)

    def test_paper_example_historical_two_current_one(self):
        self.assertEqual(self.at(4)["current_input_acceptance"]["numerator"], 2)
        result = self.assert_a("stale", 5)
        self.assertEqual(result["current_input_acceptance"]["numerator"], 1)
        self.assertEqual(result["ever_passed_at_checkpoint"]["numerator"], 2)

    def test_same_output_can_pass_revised_input(self):
        old = self.assert_a("stale", 5)["tasks"]["A"]["key"]
        new = self.assert_a("passed", 6)["tasks"]["A"]["key"]
        self.assertEqual(old, new)
        self.assertEqual(new["output_revision"], "report-r1")
        self.assertEqual(self.at(6)["tasks"]["A"]["active_evidence_ids"], ["E-A-v2-pass"])

    def test_disagreement_and_explicit_resolution_checkpoints(self):
        for cutoff, expected in ((7, "disputed"), (9, "disputed"), (10, "rejected"),
                                 (11, "disputed"), (12, "passed")):
            with self.subTest(cutoff=cutoff):
                self.assert_a(expected, cutoff)
        self.assertEqual(self.at(11)["tasks"]["A"]["active_evidence_ids"], ["R-reject", "R-pass"])
        self.assertEqual(self.at(12)["tasks"]["A"]["active_evidence_ids"], ["R-both"])

    def test_later_appends_do_not_rewrite_any_earlier_prefix(self):
        for cutoff in range(13):
            with self.subTest(cutoff=cutoff):
                truncated = deepcopy(self.ledger)
                truncated["events"] = [e for e in truncated["events"] if e["seq"] <= cutoff]
                self.assertEqual(self.at(cutoff), MODULE.replay(truncated, cutoff))
        before = self.at(7)
        self.ledger["events"][7] = {"seq": 8, "anything": "malformed future payload"}
        self.assertEqual(self.at(7), before)

    def test_timestamps_do_not_order_or_authorize(self):
        before = self.at()
        for event in self.ledger["events"]:
            event["evaluated_at"] = "2099-01-01" if event["seq"] % 2 else "1900-01-01"
        self.assertEqual(self.at(), before)

    def test_history_is_ever_passed_state_not_current_validity(self):
        result = self.assert_a("disputed", 7)
        self.assertEqual(result["ever_passed_at_checkpoint"]["numerator"], 2)
        self.assertEqual(result["current_input_acceptance"]["numerator"], 1)
        # Rejection first, then a pass creates only a dispute, never a passed state.
        self.keep(7)
        self.ledger["events"][1]["outcome"] = "rejected"
        self.ledger["events"][5]["outcome"] = "rejected"
        self.ledger["events"][6]["outcome"] = "passed"
        self.assertEqual(self.at()["ever_passed_at_checkpoint"]["numerator"], 1)

    def test_invalid_resolutions_are_visible_and_atomic(self):
        result = self.assert_a("disputed", 9)
        self.assertEqual([e["code"] for e in result["invalid_events"]],
                         ["unauthorized_resolver", "cross_key_reference"])
        self.assertEqual(result["tasks"]["A"]["active_evidence_ids"],
                         ["E-A-v2-pass", "E-A-v2-reject"])
        self.assertIn("R-unauthorized", result["visible_event_ids"])
        self.assertEqual(result["tasks"]["B"]["state"], "passed")

    def test_partial_resolution_cannot_hide_conflicting_active_resolutions(self):
        joint = deepcopy(self.ledger["events"][-1])
        self.keep(11)
        self.append(joint, id="R-partial", outcome="rejected", supersedes=["R-pass"])
        result = self.assert_a("disputed")
        self.assertEqual(result["invalid_events"][-1]["code"], "unaddressed_active_resolutions")
        self.assertEqual(result["tasks"]["A"]["active_evidence_ids"], ["R-reject", "R-pass"])

    def test_new_opposite_evaluation_reopens_resolved_dispute(self):
        self.append(self.ledger["events"][6], id="E-later")
        self.assert_a("disputed")
        self.assertEqual(self.at()["tasks"]["A"]["active_evidence_ids"], ["R-both", "E-later"])

    def test_forward_missing_self_and_two_event_cycles_do_not_retire_evidence(self):
        template = deepcopy(self.ledger["events"][9])
        for target, code in (("R-future", "reference_not_prior"),
                             ("missing", "reference_not_prior"), ("R-test", "cyclic_reference")):
            with self.subTest(target=target):
                self.keep(7)
                self.append(template, id="R-test", supersedes=["E-A-v2-pass", "E-A-v2-reject", target])
                result = self.assert_a("disputed")
                self.assertEqual(result["invalid_events"][-1]["code"], code)
        self.keep(7)
        self.append(template, id="R-cycle-a", supersedes=["R-cycle-b"])
        before = self.at(8)
        self.append(template, id="R-cycle-b", supersedes=["R-cycle-a"])
        result = self.assert_a("disputed")
        self.assertEqual([e["code"] for e in result["invalid_events"]],
                         ["reference_not_prior", "invalid_reference"])
        self.assertEqual(self.at(8), before)

    def test_invalid_target_cannot_be_resurrected(self):
        template = deepcopy(self.ledger["events"][9])
        self.keep(8)
        self.append(template, id="R-invalid-target", supersedes=["R-unauthorized"])
        self.assertEqual(self.assert_a("disputed")["invalid_events"][-1]["code"], "invalid_reference")

    def test_all_four_key_components_are_enforced(self):
        template = deepcopy(self.ledger["events"][9])
        for field, value in (("task_id", "B"), ("output_revision", "other-report"),
                             ("required_input_revision", "outline-v1"), ("rubric_revision", "other-rubric")):
            with self.subTest(field=field):
                self.keep(7)
                self.ledger["rubrics"]["other-rubric"] = "Another synthetic rubric."
                if field == "output_revision":
                    self.append(self.ledger["events"][0], id="O-other", output_revision=value,
                                attempt_id="A-attempt-2")
                key = dict(template["key"], **{field: value})
                self.append(self.ledger["events"][5], id="E-other", key=key)
                self.append(template, id="R-cross", supersedes=["E-A-v2-pass", "E-A-v2-reject", "E-other"])
                self.assertEqual(self.at()["invalid_events"][-1]["code"], "cross_key_reference")

    def test_new_output_does_not_inherit_old_acceptance_or_later_old_conflicts(self):
        self.keep(6)
        self.append(self.ledger["events"][0], id="O-A-r2", output_revision="report-r2",
                    attempt_id="A-attempt-2", produced_input_revision="outline-v2")
        self.assert_a("unevaluated")
        key = dict(self.ledger["events"][5]["key"], output_revision="report-r2")
        self.append(self.ledger["events"][5], id="E-A-r2", key=key)
        self.assert_a("passed")
        self.append(self.ledger["events"][5], id="E-old-output-reject", outcome="rejected")
        result = self.assert_a("passed")
        self.assertEqual(result["tasks"]["A"]["active_evidence_ids"], ["E-A-r2"])

    def test_rubric_change_is_stale_until_exact_revision_evaluation(self):
        self.keep(6)
        self.ledger["rubrics"]["rubric-v2"] = "A revised synthetic rubric."
        self.append(self.ledger["events"][4], id="I-new-rubric", rubric_revision="rubric-v2")
        self.assert_a("stale")
        key = dict(self.ledger["events"][5]["key"], rubric_revision="rubric-v2")
        self.append(self.ledger["events"][5], id="E-new-rubric", key=key, outcome="rejected")
        self.assert_a("rejected")

    def test_unattempted_failed_and_retried_tasks_keep_assigned_denominator(self):
        self.keep(1)
        self.ledger["events"][0]["text"] = None
        result = self.assert_a("unevaluated")
        self.assertEqual(result["counts"]["unevaluated"], 2)  # B is abandoned before an attempt.
        failed_evaluation = {"id": "E-failed", "kind": "evaluation", "key": {
            "task_id": "A", "output_revision": "report-r1",
            "required_input_revision": "outline-v1", "rubric_revision": "rubric-v1"},
            "author": "synthetic-evaluator", "reason": "Cannot evaluate null output.", "outcome": "passed"}
        self.append(failed_evaluation)
        self.assertEqual(self.at()["invalid_events"][-1]["code"], "unknown_output")
        self.append(self.ledger["events"][0], id="O-retry", attempt_id="A-attempt-2",
                    output_revision="report-r2", text="Summary: A retry.")
        self.assert_a("unevaluated")
        self.append(failed_evaluation, id="E-retry", key=dict(failed_evaluation["key"], output_revision="report-r2"))
        self.assertEqual(self.assert_a("passed")["current_input_acceptance"]["rate"], 0.5)

    def test_empty_cohort_has_null_rates(self):
        self.ledger["assigned_tasks"] = []
        self.ledger["events"] = []
        self.assertIsNone(self.at()["current_input_acceptance"]["rate"])
        self.assertIsNone(self.at()["ever_passed_at_checkpoint"]["rate"])

    def test_all_unmeasured_fields_remain_null(self):
        self.assertTrue(self.at()["measurements"])
        self.assertTrue(all(value is None for value in self.at()["measurements"].values()))

    def test_duplicate_event_ids_and_output_revisions_do_not_replace_valid_records(self):
        self.keep(6)
        self.append(self.ledger["events"][5], outcome="rejected")
        self.assertEqual(self.assert_a("passed")["invalid_events"][-1]["code"], "duplicate_id")
        self.append(self.ledger["events"][0], id="O-redefinition", text="Different content")
        self.assertEqual(self.assert_a("passed")["invalid_events"][-1]["code"], "invalid_output_revision")

    def test_evaluations_cannot_supersede(self):
        self.keep(7)
        self.append(self.ledger["events"][5], id="E-override", supersedes=["E-A-v2-reject"])
        self.assertEqual(self.assert_a("disputed")["invalid_events"][-1]["code"], "evaluation_cannot_supersede")

    def test_wrong_rule_blank_reason_missing_conflict_and_incomplete_targets_are_invalid(self):
        template = deepcopy(self.ledger["events"][9])
        for changes, code in (({"rule_revision": "other"}, "wrong_rule_revision"),
                              ({"reason": " "}, "invalid_judgment"),
                              ({"conflicting_evaluation_ids": ["E-A-v2-pass"]}, "no_conflict"),
                              ({"supersedes": ["E-A-v2-pass"]}, "unaddressed_conflict")):
            with self.subTest(code=code):
                self.keep(7)
                self.append(template, id="R-bad", **changes)
                self.assertEqual(self.assert_a("disputed")["invalid_events"][-1]["code"], code)

    def test_malformed_revision_values_are_reported_without_state_changes(self):
        for index, field, code in ((0, "produced_input_revision", "invalid_output"),
                                   (4, "required_input_revision", "unknown_requirement"),
                                   (4, "rubric_revision", "unknown_requirement")):
            for value in ([], {}, None, 3, True):
                with self.subTest(field=field, value=value):
                    ledger = deepcopy(self.ledger)
                    event = deepcopy(ledger["events"][index])
                    event.update(seq=13, id="malformed", **{field: value})
                    if index == 0:
                        event.update(output_revision="new-report", attempt_id="new-attempt")
                    ledger["events"].append(event)
                    result = MODULE.replay(ledger, 13)
                    self.assertEqual(result["invalid_events"][-1]["code"], code)
                    self.assertEqual(result["tasks"], self.at(12)["tasks"])

    def test_rule_revision_resolver_and_sequence_declarations_fail_closed(self):
        for field, value in (("revision", "new-rule"), ("authorized_resolvers", ["synthetic-outsider"])):
            ledger = deepcopy(self.ledger)
            ledger["rule"][field] = value
            with self.assertRaises(ValueError):
                MODULE.replay(ledger, 12)
        for value in (0, 1, True, "2"):
            ledger = deepcopy(self.ledger)
            ledger["events"][1]["seq"] = value
            with self.assertRaises(ValueError):
                MODULE.replay(ledger, 12)
        for cutoff in (-1, True, 1.5):
            with self.assertRaises(ValueError):
                self.at(cutoff)


if __name__ == "__main__":
    unittest.main()
