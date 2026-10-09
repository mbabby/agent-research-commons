"""Deterministic scoring of constructed outputs; no model or human-work run."""
import argparse
import json
from pathlib import Path


def check(output, expected):
    if not isinstance(output, dict):
        return False, ["missing structured output"]
    errors = []
    if set(output) != set(expected):
        errors.append("field set mismatch")
    for field, value in expected.items():
        if type(output.get(field)) is not type(value) or output.get(field) != value:
            errors.append("incorrect field: " + field)
    return not errors, errors


def ratio(numerator, denominator):
    return {"numerator": numerator, "denominator": denominator,
            "rate": numerator / denominator if denominator else None}


def score(fixture):
    ledger = []
    for task in fixture["tasks"]:
        attempts = []
        for index, attempt in enumerate(task["attempts"], 1):
            accepted, errors = check(attempt["output"], task["expected"])
            attempts.append({"attempt": index, "claimed_complete": attempt["claimed_complete"],
                             "accepted": accepted, "errors": errors})
        final = attempts[-1] if attempts else None
        ledger.append({"task_id": task["id"], "disposition": task["disposition"],
                       "attempts": attempts, "retry_count": max(0, len(attempts) - 1),
                       "final_claimed_complete": bool(final and final["claimed_complete"]),
                       "final_accepted": bool(final and final["accepted"]),
                       "human_correction_minutes": None, "human_intervention_count": None,
                       "waiting_minutes": None, "task_latency_seconds": None, "total_cost": None})
    assigned = len(ledger)
    attempted = sum(bool(row["attempts"]) for row in ledger)
    accepted = sum(row["final_accepted"] for row in ledger)
    claims = sum(row["final_claimed_complete"] for row in ledger)
    false_claims = sum(row["final_claimed_complete"] and not row["final_accepted"] for row in ledger)
    all_attempts = [a for row in ledger for a in row["attempts"]]
    attempt_claims = sum(a["claimed_complete"] for a in all_attempts)
    return {"provenance": "Synthetic authored inputs and outputs; actual deterministic scorer execution only",
            "assigned_task_count": assigned, "attempt_count": len(all_attempts),
            "retry_count": sum(row["retry_count"] for row in ledger),
            "claimed_completion_all_assigned": ratio(claims, assigned),
            "accepted_all_assigned": ratio(accepted, assigned),
            "false_final_completion_claims": ratio(false_claims, claims),
            "false_final_completion_claims_all_assigned": ratio(false_claims, assigned),
            "attempt_acceptance": ratio(sum(a["accepted"] for a in all_attempts), len(all_attempts)),
            "false_attempt_completion_claims": ratio(sum(a["claimed_complete"] and not a["accepted"] for a in all_attempts), attempt_claims),
            "denominator_sensitivity": {
                "exclude_unattempted_abandonment": ratio(accepted, attempted),
                "condition_on_final_completion_claim": ratio(sum(row["final_accepted"] and row["final_claimed_complete"] for row in ledger), claims),
                "retain_only_accepted_tasks_circular": ratio(accepted, accepted)},
            "human_correction_minutes": None, "human_intervention_count": None,
            "waiting_minutes": None, "task_latency_seconds": None,
            "total_measured_cost_per_accepted_outcome": None, "manual_work_baseline": None,
            "ledger": ledger}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=Path(__file__).with_name("fixture.json"))
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("results.json"))
    args = parser.parse_args()
    result = score(json.loads(args.fixture.read_text()))
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("assigned_task_count", "attempt_count", "retry_count", "claimed_completion_all_assigned", "accepted_all_assigned", "false_final_completion_claims")}, indent=2))
