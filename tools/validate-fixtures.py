#!/usr/bin/env python3
"""
Fixture validator for make-harness.

Checks that each fixture scenario's expected-state.json is structurally
consistent with the harness-state.json template and that state invariants hold.

Usage:
    python tools/validate-fixtures.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
FIXTURES_DIR = ROOT / "assets" / "fixtures"
TEMPLATE_PATH = ROOT / "assets" / "templates" / "harness-state.json"

SHARED_CONTRACT_FIELDS = {
    "communication_language",
    "project_type",
    "definition_of_done",
    "change_posture",
    "change_guardrails",
    "verification_policy",
    "approval_policy",
    "project_commands",
    "project_constraints",
    "communication_tone",
    "stack_summary",
    "environment",
}

VALID_RUN_MODES = {"bootstrap", "refresh", "repair"}
VALID_BOOTSTRAP_STATUSES = {"pending_interview", "interview_in_progress", "configured"}
VALID_SYNC_STATUSES = {"healthy", "drifted", "unvalidated", "unknown"}


def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def check_invariants(state: dict, fixture_name: str) -> list[str]:
    errors = []

    status = state.get("bootstrap_status")
    pending = state.get("pending_fields", [])
    confirmed = state.get("confirmed_fields", [])
    interview_step = state.get("interview_step")
    last_validated = state.get("last_validated_at")
    sync_status = state.get("sync_status")

    # configured implies pending_fields is empty
    if status == "configured" and pending:
        errors.append(
            f"[{fixture_name}] bootstrap_status=configured but pending_fields is not empty: {pending}"
        )

    # configured implies interview_step=complete
    if status == "configured" and interview_step != "complete":
        errors.append(
            f"[{fixture_name}] bootstrap_status=configured but interview_step={interview_step!r} (expected 'complete')"
        )

    # pending_fields and confirmed_fields must not overlap
    overlap = set(pending) & set(confirmed)
    if overlap:
        errors.append(
            f"[{fixture_name}] pending_fields and confirmed_fields overlap: {overlap}"
        )

    # last_validated_at set => sync_status must be explicit
    if last_validated and sync_status in ("unknown", "unvalidated", None):
        errors.append(
            f"[{fixture_name}] last_validated_at is set but sync_status={sync_status!r} is not explicit"
        )

    # run_mode must be valid
    run_mode = state.get("run_mode")
    if run_mode and run_mode not in VALID_RUN_MODES:
        errors.append(f"[{fixture_name}] invalid run_mode: {run_mode!r}")

    # bootstrap_status must be valid
    if status and status not in VALID_BOOTSTRAP_STATUSES:
        errors.append(f"[{fixture_name}] invalid bootstrap_status: {status!r}")

    return errors


def check_template_schema(template: dict, state: dict, fixture_name: str) -> list[str]:
    """All keys in expected-state must exist in the template (or be allowed fixture-only keys)."""
    errors = []
    # _meta keys added to template, plus fixture-only annotation keys
    fixture_only_keys = {"phase"}
    meta_keys = {"_gitignore_note", "_volatile_fields", "_config_fields"}
    template_keys = set(template.keys()) | meta_keys | fixture_only_keys

    for key in state:
        if key not in template_keys:
            errors.append(
                f"[{fixture_name}] expected-state has unknown key: {key!r} (not in template schema)"
            )

    return errors


def validate_fixture(fixture_dir: Path, template: dict) -> list[str]:
    fixture_path = fixture_dir / "fixture.json"
    expected_path = fixture_dir / "expected-state.json"

    if not fixture_path.exists():
        return [f"[{fixture_dir.name}] missing fixture.json"]
    if not expected_path.exists():
        return [f"[{fixture_dir.name}] missing expected-state.json"]

    fixture = load_json(fixture_path)
    expected = load_json(expected_path)
    name = fixture.get("name", fixture_dir.name)

    errors = []
    errors += check_template_schema(template, expected, name)
    errors += check_invariants(expected, name)

    # fixture.json expected.run_mode must match expected-state run_mode
    fixture_expected_mode = fixture.get("expected", {}).get("run_mode")
    state_mode = expected.get("run_mode")
    if fixture_expected_mode and state_mode and fixture_expected_mode != state_mode:
        errors.append(
            f"[{name}] fixture.expected.run_mode={fixture_expected_mode!r} "
            f"does not match expected-state.run_mode={state_mode!r}"
        )

    return errors


def main() -> int:
    if not TEMPLATE_PATH.exists():
        print(f"ERROR: template not found at {TEMPLATE_PATH}", file=sys.stderr)
        return 1

    template = load_json(TEMPLATE_PATH)

    fixture_dirs = sorted(
        d for d in FIXTURES_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")
    )

    if not fixture_dirs:
        print("No fixture directories found.", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    results: list[tuple[str, bool]] = []

    for fixture_dir in fixture_dirs:
        errors = validate_fixture(fixture_dir, template)
        passed = len(errors) == 0
        results.append((fixture_dir.name, passed))
        all_errors.extend(errors)

    # Report
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {status}  {name}")

    if all_errors:
        print()
        for err in all_errors:
            print(f"       {err}")
        print(f"\n{len(all_errors)} error(s) found across {len(fixture_dirs)} fixture(s).")
        return 1

    print(f"\nAll {len(fixture_dirs)} fixture(s) passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
