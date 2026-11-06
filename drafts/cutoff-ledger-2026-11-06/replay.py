"""A deliberately small, synthetic cutoff ledger. Python standard library only."""
import argparse
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path


RULE = {
    "revision": "synthetic-explicit-resolution-v1",
    "authorized_resolvers": ["synthetic-resolver-a", "synthetic-resolver-b"],
}
KEY_FIELDS = ("task_id", "output_revision", "required_input_revision", "rubric_revision")
STATES = ("stale", "unevaluated", "passed", "rejected", "disputed")
MEASUREMENTS = dict.fromkeys((
    "human_correction_minutes", "evaluation_minutes", "waiting_minutes",
    "latency_seconds", "intervention_count", "total_cost",
    "cost_per_accepted_outcome", "manual_baseline_minutes",
))


class InvalidEvent(ValueError):
    """An event is retained for inspection but has no effect on the replay."""

    def __init__(self, code, detail):
        super().__init__(detail)
        self.code = code


def require(condition, code, detail):
    if not condition:
        raise InvalidEvent(code, detail)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def exact_key(event):
    key = event.get("key")
    require(isinstance(key, dict) and set(key) == set(KEY_FIELDS),
            "invalid_key", "key must contain exactly the four declared fields")
    require(all(nonempty(key[field]) for field in KEY_FIELDS),
            "invalid_key", "key fields must be nonempty strings")
    return tuple(key[field] for field in KEY_FIELDS)


def replay(ledger, cutoff):
    """Return one prefix-only view; never mutate the ledger or inspect future content."""
    if type(cutoff) is not int or cutoff < 0:
        raise ValueError("cutoff must be a nonnegative integer")
    if ledger.get("schema_version") != 1 or ledger.get("rule") != RULE:
        raise ValueError("unsupported schema or changed frozen rule/resolver declaration")
    for catalog in ("inputs", "rubrics"):
        if not isinstance(ledger.get(catalog), dict) or not all(
            nonempty(k) and nonempty(v) for k, v in ledger[catalog].items()
        ):
            raise ValueError("inputs and rubrics must map revisions to nonempty text")
    tasks = {}
    for task in ledger["assigned_tasks"]:
        task_id = task.get("task_id")
        if (not nonempty(task_id) or task_id in tasks
                or not nonempty(task.get("required_input_revision"))
                or not nonempty(task.get("rubric_revision"))
                or task["required_input_revision"] not in ledger["inputs"]
                or task["rubric_revision"] not in ledger["rubrics"]):
            raise ValueError("invalid or duplicate assigned task")
        tasks[task_id] = dict(task, output_revision=None)
    outputs, evidence, seen = {}, {}, set()
    inactive, historical = set(), set()
    errors, visible_ids = [], []

    def view(task_id):
        task = tasks[task_id]
        output = outputs.get((task_id, task["output_revision"]))
        key = (task_id, task["output_revision"],
               task["required_input_revision"], task["rubric_revision"])
        active = [event for event_id, event in evidence.items()
                  if event_id not in inactive and exact_key(event) == key]
        outcomes = {event["outcome"] for event in active}
        if outcomes:
            state = "disputed" if len(outcomes) > 1 else next(iter(outcomes))
        elif output is None or output["text"] is None:
            state = "unevaluated"
        elif (output["produced_input_revision"] != task["required_input_revision"]
              or any(exact_key(event)[:2] == key[:2] for event in evidence.values())):
            state = "stale"
        else:
            state = "unevaluated"
        return {"key": dict(zip(KEY_FIELDS, key)), "state": state,
                "active_evidence_ids": [event["id"] for event in active]}

    def reference(ref, event_id, key, evaluation_only=False):
        require(ref != event_id, "cyclic_reference", "an event cannot reference itself")
        require(ref in seen, "reference_not_prior", "missing or forward reference: " + ref)
        require(ref in evidence, "invalid_reference", "not earlier valid evidence: " + ref)
        target = evidence[ref]
        require(exact_key(target) == key, "cross_key_reference", "different evaluation key: " + ref)
        require(not evaluation_only or target["kind"] == "evaluation",
                "invalid_reference", "conflicting_evaluation_ids must name evaluations")
        return target

    last_seq = 0
    for event in ledger["events"]:
        # A future event ends the prefix. Its payload, IDs and references are not read.
        seq = event.get("seq")
        if type(seq) is not int or seq <= last_seq:
            raise ValueError("event sequences must be strictly increasing positive integers")
        if seq > cutoff:
            break
        last_seq = seq
        event_id = event.get("id")
        visible_ids.append(event_id)
        try:
            require(nonempty(event_id), "invalid_id", "event id must be a nonempty string")
            require(event_id not in seen, "duplicate_id", "earlier event ID is immutable")
            # Reserve even invalid IDs so later records cannot silently replace them.
            seen.add(event_id)
            kind = event.get("kind")
            if kind in ("output", "requirement"):
                task_id = event.get("task_id")
                require(isinstance(task_id, str) and task_id in tasks,
                        "unknown_task", "task must belong to the fixed assigned cohort")
                if kind == "output":
                    revision = event.get("output_revision")
                    require(nonempty(revision) and (task_id, revision) not in outputs,
                            "invalid_output_revision", "output revision is missing or already defined")
                    require(nonempty(event.get("attempt_id")) and "text" in event
                            and (event["text"] is None or nonempty(event["text"]))
                            and nonempty(event.get("produced_input_revision"))
                            and event["produced_input_revision"] in ledger["inputs"],
                            "invalid_output", "output needs attempt, input revision and text (or null failure)")
                    require(not any(old["attempt_id"] == event["attempt_id"]
                                    for (owner, _), old in outputs.items() if owner == task_id),
                            "duplicate_attempt", "a retry needs a new attempt ID")
                    outputs[(task_id, revision)] = deepcopy(event)
                    tasks[task_id]["output_revision"] = revision
                else:
                    require(nonempty(event.get("required_input_revision"))
                            and nonempty(event.get("rubric_revision"))
                            and event["required_input_revision"] in ledger["inputs"]
                            and event["rubric_revision"] in ledger["rubrics"],
                            "unknown_requirement", "input and rubric revisions must be declared")
                    tasks[task_id].update({field: event[field] for field in
                                          ("required_input_revision", "rubric_revision")})
            elif kind in ("evaluation", "resolution"):
                key = exact_key(event)
                output = outputs.get(key[:2])
                require(output is not None and output["text"] is not None,
                        "unknown_output", "evaluation needs an earlier non-null output for this task")
                require(key[2] in ledger["inputs"] and key[3] in ledger["rubrics"],
                        "unknown_requirement", "input and rubric revisions must be declared")
                require(nonempty(event.get("author")) and nonempty(event.get("reason"))
                        and event.get("outcome") in ("passed", "rejected"),
                        "invalid_judgment", "judgment needs author, reason and passed/rejected outcome")
                targets = []
                if kind == "evaluation":
                    require("supersedes" not in event, "evaluation_cannot_supersede",
                            "only an authorized explicit resolution may supersede evidence")
                else:
                    require(event["author"] in RULE["authorized_resolvers"],
                            "unauthorized_resolver", "author is not in the frozen resolver list")
                    require(event.get("rule_revision") == RULE["revision"],
                            "wrong_rule_revision", "resolution must name the frozen rule revision")
                    for field in ("supersedes", "conflicting_evaluation_ids"):
                        refs = event.get(field)
                        require(isinstance(refs, list) and bool(refs)
                                and all(nonempty(ref) for ref in refs) and len(refs) == len(set(refs)),
                                "invalid_references", field + " must be a nonempty list of unique IDs")
                    conflicts = [reference(ref, event_id, key, True)
                                 for ref in event["conflicting_evaluation_ids"]]
                    require({item["outcome"] for item in conflicts} == {"passed", "rejected"},
                            "no_conflict", "named evaluations must contain both outcomes")
                    targets = event["supersedes"]
                    active_resolutions = {old_id: old for old_id, old in evidence.items()
                                          if old_id not in inactive and old["kind"] == "resolution"
                                          and exact_key(old) == key}
                    if len({old["outcome"] for old in active_resolutions.values()}) > 1:
                        require(not set(targets).intersection(active_resolutions)
                                or set(active_resolutions) <= set(targets),
                                "unaddressed_active_resolutions",
                                "resolving an active resolution conflict must explicitly address all sides")
                    covered, pending = set(), list(targets)
                    while pending:
                        ref = pending.pop()
                        target = reference(ref, event_id, key)
                        if ref not in covered:
                            covered.add(ref)
                            pending.extend(target.get("supersedes", []))
                    require(set(event["conflicting_evaluation_ids"]) <= covered,
                            "unaddressed_conflict", "targets do not cover all named conflicting evaluations")
                # Atomic: no reference can retire evidence before all checks succeed.
                evidence[event_id] = deepcopy(event)
                inactive.update(targets)
            else:
                raise InvalidEvent("unknown_event_kind", "unsupported event kind")
        except InvalidEvent as exc:
            errors.append({"seq": seq, "id": event_id, "code": exc.code, "detail": str(exc)})
        historical.update(task_id for task_id in tasks if view(task_id)["state"] == "passed")

    per_task = {task_id: view(task_id) for task_id in tasks}
    counts = Counter(item["state"] for item in per_task.values())
    denominator = len(tasks)

    def metric(numerator):
        return {"numerator": numerator, "denominator": denominator,
                "rate": numerator / denominator if denominator else None}

    return {"cutoff": cutoff, "rule": deepcopy(RULE),
            "current_input_acceptance": metric(counts["passed"]),
            "ever_passed_at_checkpoint": metric(len(historical)),
            "counts": {state: counts[state] for state in STATES},
            "tasks": per_task, "visible_event_ids": visible_ids,
            "invalid_events": errors, "measurements": dict(MEASUREMENTS)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=Path(__file__).with_name("ledger.json"))
    parser.add_argument("--cutoff", type=int)
    args = parser.parse_args()
    ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    result = replay(ledger, args.cutoff) if args.cutoff is not None else {
        name: replay(ledger, cutoff) for name, cutoff in ledger["checkpoints"].items()
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
