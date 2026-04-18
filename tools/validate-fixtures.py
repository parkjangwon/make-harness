#!/usr/bin/env python3
"""Fixture validator for make-harness."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
FIXTURES_DIR = ROOT / "assets" / "fixtures"
CONTRACT_TEMPLATE_PATH = ROOT / "assets" / "templates" / "harness-contract.json"
RUNTIME_TEMPLATE_PATH = ROOT / "assets" / "templates" / "harness-runtime.json"

SHARED_CONTRACT_FIELDS = [
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
]
ENTRY_FILES = ["AGENTS.md", "CLAUDE.md", "GEMINI.md"]
MANAGED_FILES = ENTRY_FILES + ["PROJECT_HARNESS.md", "harness-contract.json", "harness-runtime.json"]
EXPECTED_VOLATILE_FIELDS = [
    "run_mode",
    "bootstrap_status",
    "interview_step",
    "pending_fields",
    "confirmed_fields",
    "validated_shared_fields",
    "drift_reasons",
    "sync_status",
    "entry_files_sync",
    "last_audit_at",
    "last_validated_at",
    "language_detection",
]
VALID_RUN_MODES = {"bootstrap", "refresh", "repair"}
VALID_BOOTSTRAP_STATUSES = {"pending_interview", "interview_in_progress", "configured"}
VALID_SYNC_STATUSES = {"healthy", "drifted", "unvalidated", "unknown"}
VALID_LANGUAGE_CONFIDENCE = {"low", "medium", "high"}
EXPECTED_CONTRACT_FILE_ROLE = "durable_project_contract"
EXPECTED_RUNTIME_FILE_ROLE = "volatile_runtime_state"
EXPECTED_HARNESS_VERSION = 2
FIXTURE_REQUIRED_KEYS = {"name", "purpose", "initial_conditions", "expected"}
INITIAL_CONDITIONS_ALLOWED_KEYS = {
    "managed_files_present",
    "canonical_sources_present",
    "entry_files_present",
    "notes",
    "bootstrap_status",
    "pending_fields",
    "confirmed_fields",
    "repo_language_signal",
    "repo_language_confidence",
    "canonical_sources_aligned",
    "entry_files_aligned",
    "entry_files_thin",
    "example_drift",
    "package_manager",
    "runtime",
}
EXPECTED_ALLOWED_KEYS = {
    "run_mode",
    "bootstrap_status",
    "interview_step",
    "sync_status",
    "entry_files_sync_status",
    "drift_reasons",
    "checks",
    "interview_mode",
    "next_question_field",
    "next_question_style",
    "discovery_fields",
    "skip_fields",
}


def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def load_interview_planner_module():
    import importlib.util

    path = ROOT / "tools" / "interview_planner.py"
    spec = importlib.util.spec_from_file_location("interview_planner", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _type_error(fixture_name: str, field: str, expected: str) -> str:
    return f"[{fixture_name}] {field} must be {expected}"


def check_runtime_invariants(state: dict, fixture_name: str) -> list[str]:
    errors = []
    status = state.get("bootstrap_status")
    pending = state.get("pending_fields", [])
    confirmed = state.get("confirmed_fields", [])
    interview_step = state.get("interview_step")
    last_validated = state.get("last_validated_at")
    sync_status = state.get("sync_status")
    validated = state.get("validated_shared_fields", [])

    if not isinstance(pending, list):
        errors.append(_type_error(fixture_name, "pending_fields", "a list"))
        pending = []
    if not isinstance(confirmed, list):
        errors.append(_type_error(fixture_name, "confirmed_fields", "a list"))
        confirmed = []
    if not isinstance(validated, list):
        errors.append(_type_error(fixture_name, "validated_shared_fields", "a list"))
        validated = []

    if status == "configured" and pending:
        errors.append(f"[{fixture_name}] bootstrap_status=configured but pending_fields is not empty: {pending}")
    if status == "configured" and interview_step != "complete":
        errors.append(f"[{fixture_name}] bootstrap_status=configured but interview_step={interview_step!r} (expected 'complete')")
    overlap = set(pending) & set(confirmed)
    if overlap:
        errors.append(f"[{fixture_name}] pending_fields and confirmed_fields overlap: {sorted(overlap)}")
    if last_validated and sync_status in ("unknown", "unvalidated", None):
        errors.append(f"[{fixture_name}] last_validated_at is set but sync_status={sync_status!r} is not explicit")
    if state.get("run_mode") not in VALID_RUN_MODES:
        errors.append(f"[{fixture_name}] invalid run_mode: {state.get('run_mode')!r}")
    if status not in VALID_BOOTSTRAP_STATUSES:
        errors.append(f"[{fixture_name}] invalid bootstrap_status: {status!r}")
    if sync_status not in VALID_SYNC_STATUSES:
        errors.append(f"[{fixture_name}] invalid sync_status: {sync_status!r}")
    unknown_validated = sorted(set(validated) - set(SHARED_CONTRACT_FIELDS))
    if unknown_validated:
        errors.append(f"[{fixture_name}] validated_shared_fields contains unknown fields: {unknown_validated}")

    entry_sync = state.get("entry_files_sync")
    if not isinstance(entry_sync, dict):
        errors.append(_type_error(fixture_name, "entry_files_sync", "an object"))
    else:
        if entry_sync.get("status") not in VALID_SYNC_STATUSES:
            errors.append(f"[{fixture_name}] invalid entry_files_sync.status: {entry_sync.get('status')!r}")
        if "entry_files" in entry_sync and entry_sync.get("entry_files") != ENTRY_FILES:
            errors.append(f"[{fixture_name}] entry_files_sync.entry_files must exactly match {ENTRY_FILES}")
        if "required_shared_fields" in entry_sync and entry_sync.get("required_shared_fields") != SHARED_CONTRACT_FIELDS:
            errors.append(f"[{fixture_name}] entry_files_sync.required_shared_fields must exactly match the canonical ordered field list")
        if "notes" in entry_sync and not isinstance(entry_sync.get("notes"), list):
            errors.append(_type_error(fixture_name, "entry_files_sync.notes", "a list"))

    language_detection = state.get("language_detection")
    if language_detection is not None:
        if not isinstance(language_detection, dict):
            errors.append(_type_error(fixture_name, "language_detection", "an object"))
        else:
            if language_detection.get("strategy") != "detect_first_then_confirm":
                errors.append(f"[{fixture_name}] language_detection.strategy must be 'detect_first_then_confirm'")
            if language_detection.get("confidence") not in VALID_LANGUAGE_CONFIDENCE:
                errors.append(f"[{fixture_name}] invalid language_detection.confidence: {language_detection.get('confidence')!r}")

    if "managed_files" in state and state.get("managed_files") != MANAGED_FILES:
        errors.append(f"[{fixture_name}] managed_files must exactly match {MANAGED_FILES}")

    if "_volatile_fields" in state and state.get("_volatile_fields") != EXPECTED_VOLATILE_FIELDS:
        errors.append(f"[{fixture_name}] _volatile_fields must exactly match the canonical ordered runtime field list")

    leaked_contract_fields = sorted(set(SHARED_CONTRACT_FIELDS) & set(state))
    if leaked_contract_fields:
        errors.append(f"[{fixture_name}] runtime state contains durable contract field(s): {leaked_contract_fields}")

    return errors


def check_contract_runtime_alignment(contract: dict, runtime: dict, fixture_name: str) -> list[str]:
    errors = []
    missing_contract = sorted(set(SHARED_CONTRACT_FIELDS) - set(contract))
    if missing_contract:
        errors.append(f"[{fixture_name}] missing required contract field(s): {missing_contract}")
    runtime_required = {"run_mode", "bootstrap_status", "interview_step", "pending_fields", "confirmed_fields", "validated_shared_fields", "drift_reasons", "sync_status", "entry_files_sync", "last_audit_at", "last_validated_at"}
    missing_runtime = sorted(runtime_required - set(runtime))
    if missing_runtime:
        errors.append(f"[{fixture_name}] missing required runtime field(s): {missing_runtime}")
    if '_file_role' in contract and contract.get('_file_role') != EXPECTED_CONTRACT_FILE_ROLE:
        errors.append(f"[{fixture_name}] contract _file_role must be {EXPECTED_CONTRACT_FILE_ROLE!r}")
    if '_file_role' in runtime and runtime.get('_file_role') != EXPECTED_RUNTIME_FILE_ROLE:
        errors.append(f"[{fixture_name}] runtime _file_role must be {EXPECTED_RUNTIME_FILE_ROLE!r}")
    if 'harness_version' in contract and contract.get('harness_version') != EXPECTED_HARNESS_VERSION:
        errors.append(f"[{fixture_name}] contract harness_version must be {EXPECTED_HARNESS_VERSION}")
    if 'harness_version' in runtime and runtime.get('harness_version') != EXPECTED_HARNESS_VERSION:
        errors.append(f"[{fixture_name}] runtime harness_version must be {EXPECTED_HARNESS_VERSION}")
    if 'harness_version' in contract and 'harness_version' in runtime and contract.get('harness_version') != runtime.get('harness_version'):
        errors.append(f"[{fixture_name}] contract and runtime harness_version must match")
    if runtime.get('sync_status') not in VALID_SYNC_STATUSES:
        errors.append(f"[{fixture_name}] invalid sync_status: {runtime.get('sync_status')!r}")
    if contract.get('shared_contract_fields') != SHARED_CONTRACT_FIELDS:
        errors.append(f"[{fixture_name}] contract shared_contract_fields must exactly match the canonical ordered field list")
    if '_volatile_fields' in runtime and runtime.get('_volatile_fields') != EXPECTED_VOLATILE_FIELDS:
        errors.append(f"[{fixture_name}] runtime _volatile_fields must exactly match the canonical ordered runtime field list")
    return errors


def check_template_schema(template: dict, state: dict, fixture_name: str) -> list[str]:
    errors = []
    fixture_only_keys = {"phase"}
    template_keys = set(template.keys()) | fixture_only_keys
    for key in state:
        if key not in template_keys:
            errors.append(f"[{fixture_name}] expected file has unknown key: {key!r} (not in template schema)")
    return errors


def check_fixture_schema(fixture: dict, fixture_name: str) -> list[str]:
    errors = []
    missing = sorted(FIXTURE_REQUIRED_KEYS - set(fixture))
    if missing:
        errors.append(f"[{fixture_name}] fixture.json missing required field(s): {missing}")
        return errors

    if not isinstance(fixture.get("purpose"), str):
        errors.append(_type_error(fixture_name, "purpose", "a string"))

    initial_conditions = fixture.get("initial_conditions")
    expected = fixture.get("expected")
    if not isinstance(initial_conditions, dict):
        errors.append(_type_error(fixture_name, "initial_conditions", "an object"))
        initial_conditions = {}
    if not isinstance(expected, dict):
        errors.append(_type_error(fixture_name, "expected", "an object"))
        expected = {}

    unknown_initial = sorted(set(initial_conditions) - INITIAL_CONDITIONS_ALLOWED_KEYS)
    if unknown_initial:
        errors.append(f"[{fixture_name}] initial_conditions has unknown key(s): {unknown_initial}")
    unknown_expected = sorted(set(expected) - EXPECTED_ALLOWED_KEYS)
    if unknown_expected:
        errors.append(f"[{fixture_name}] expected has unknown key(s): {unknown_expected}")

    managed_files_present = initial_conditions.get("managed_files_present", [])
    if managed_files_present is not None and not isinstance(managed_files_present, list):
        errors.append(_type_error(fixture_name, "initial_conditions.managed_files_present", "a list"))
        managed_files_present = []
    if isinstance(managed_files_present, list):
        unknown_managed = sorted(set(managed_files_present) - set(MANAGED_FILES))
        if unknown_managed:
            errors.append(f"[{fixture_name}] initial_conditions.managed_files_present contains unknown managed file(s): {unknown_managed}")

    entry_files_present = initial_conditions.get("entry_files_present", [])
    if entry_files_present is not None and not isinstance(entry_files_present, list):
        errors.append(_type_error(fixture_name, "initial_conditions.entry_files_present", "a list"))
    elif isinstance(entry_files_present, list):
        unknown_entry = sorted(set(entry_files_present) - set(ENTRY_FILES))
        if unknown_entry:
            errors.append(f"[{fixture_name}] initial_conditions.entry_files_present contains unknown entry file(s): {unknown_entry}")

    notes = initial_conditions.get("notes", [])
    if notes is not None and not isinstance(notes, list):
        errors.append(_type_error(fixture_name, "initial_conditions.notes", "a list"))

    checks = expected.get("checks", [])
    if checks is not None and not isinstance(checks, list):
        errors.append(_type_error(fixture_name, "expected.checks", "a list"))

    if expected.get("run_mode") and expected["run_mode"] not in VALID_RUN_MODES:
        errors.append(f"[{fixture_name}] expected.run_mode has invalid value: {expected['run_mode']!r}")
    if expected.get("bootstrap_status") and expected["bootstrap_status"] not in VALID_BOOTSTRAP_STATUSES:
        errors.append(f"[{fixture_name}] expected.bootstrap_status has invalid value: {expected['bootstrap_status']!r}")
    if expected.get("sync_status") and expected["sync_status"] not in VALID_SYNC_STATUSES:
        errors.append(f"[{fixture_name}] expected.sync_status has invalid value: {expected['sync_status']!r}")
    if expected.get("entry_files_sync_status") and expected["entry_files_sync_status"] not in VALID_SYNC_STATUSES:
        errors.append(f"[{fixture_name}] expected.entry_files_sync_status has invalid value: {expected['entry_files_sync_status']!r}")
    if expected.get("drift_reasons") is not None and not isinstance(expected.get("drift_reasons"), list):
        errors.append(_type_error(fixture_name, "expected.drift_reasons", "a list"))
    if expected.get("interview_mode") is not None and not isinstance(expected.get("interview_mode"), str):
        errors.append(_type_error(fixture_name, "expected.interview_mode", "a string"))
    if expected.get("next_question_field") is not None and not isinstance(expected.get("next_question_field"), str):
        errors.append(_type_error(fixture_name, "expected.next_question_field", "a string"))
    if expected.get("next_question_style") is not None and not isinstance(expected.get("next_question_style"), str):
        errors.append(_type_error(fixture_name, "expected.next_question_style", "a string"))
    if expected.get("discovery_fields") is not None and not isinstance(expected.get("discovery_fields"), list):
        errors.append(_type_error(fixture_name, "expected.discovery_fields", "a list"))
    if expected.get("skip_fields") is not None and not isinstance(expected.get("skip_fields"), list):
        errors.append(_type_error(fixture_name, "expected.skip_fields", "a list"))

    purpose = fixture.get("purpose", "")
    if "without harness files" in purpose and managed_files_present:
        errors.append(f"[{fixture_name}] fixture purpose says no harness files exist, but managed_files_present is not empty")

    return errors


def cross_check_fixture_expectations(fixture: dict, runtime: dict, fixture_name: str) -> list[str]:
    errors = []
    expected = fixture.get("expected", {})

    runtime_checks = {
        "run_mode": runtime.get("run_mode"),
        "bootstrap_status": runtime.get("bootstrap_status"),
        "interview_step": runtime.get("interview_step"),
        "sync_status": runtime.get("sync_status"),
        "entry_files_sync_status": runtime.get("entry_files_sync", {}).get("status") if isinstance(runtime.get("entry_files_sync"), dict) else None,
        "drift_reasons": runtime.get("drift_reasons"),
    }
    for key, actual in runtime_checks.items():
        if key in expected and expected.get(key) != actual:
            errors.append(f"[{fixture_name}] fixture.expected.{key}={expected.get(key)!r} does not match expected-runtime.{key}={actual!r}")
    return errors


def cross_check_interview_plan(fixture: dict, fixture_name: str) -> list[str]:
    expected = fixture.get("expected", {})
    if not any(key in expected for key in ("interview_mode", "next_question_field", "next_question_style", "discovery_fields", "skip_fields")):
        return []

    planner = load_interview_planner_module()
    plan = planner.plan_interview(fixture.get("initial_conditions", {}))
    errors = []

    for key in ("interview_mode", "next_question_field", "next_question_style"):
        if key in expected and expected.get(key) != plan.get(key):
            errors.append(
                f"[{fixture_name}] expected.{key}={expected.get(key)!r} does not match deterministic interview plan {plan.get(key)!r}"
            )

    for key in ("discovery_fields", "skip_fields"):
        if key in expected and expected.get(key) != plan.get(key):
            errors.append(
                f"[{fixture_name}] expected.{key}={expected.get(key)!r} does not match deterministic interview plan {plan.get(key)!r}"
            )

    return errors


def validate_fixture(fixture_dir: Path, contract_template: dict, runtime_template: dict) -> list[str]:
    fixture_path = fixture_dir / "fixture.json"
    expected_runtime_path = fixture_dir / "expected-runtime.json"
    expected_contract_path = fixture_dir / "expected-contract.json"
    if not fixture_path.exists():
        return [f"[{fixture_dir.name}] missing fixture.json"]
    if not expected_runtime_path.exists() and not expected_contract_path.exists():
        return [f"[{fixture_dir.name}] missing expected-runtime.json or expected-contract.json"]
    fixture = load_json(fixture_path)
    name = fixture.get('name', fixture_dir.name)
    errors = check_fixture_schema(fixture, name)
    errors += cross_check_interview_plan(fixture, name)
    if expected_runtime_path.exists():
        runtime = load_json(expected_runtime_path)
        errors += check_template_schema(runtime_template, runtime, name)
        errors += check_runtime_invariants(runtime, name)
        errors += check_contract_runtime_alignment(contract_template, runtime, name)
        errors += cross_check_fixture_expectations(fixture, runtime, name)
    if expected_contract_path.exists():
        contract = load_json(expected_contract_path)
        errors += check_template_schema(contract_template, contract, name)
        missing_contract = sorted(set(SHARED_CONTRACT_FIELDS) - set(contract))
        if missing_contract:
            errors.append(f"[{name}] missing required contract field(s): {missing_contract}")
        if contract.get("shared_contract_fields") != SHARED_CONTRACT_FIELDS:
            errors.append(f"[{name}] contract shared_contract_fields must exactly match the canonical ordered field list")
    return errors


def main() -> int:
    if not CONTRACT_TEMPLATE_PATH.exists() or not RUNTIME_TEMPLATE_PATH.exists():
        print('ERROR: split templates not found', file=sys.stderr)
        return 1
    contract_template = load_json(CONTRACT_TEMPLATE_PATH)
    runtime_template = load_json(RUNTIME_TEMPLATE_PATH)
    fixture_dirs = sorted(d for d in FIXTURES_DIR.iterdir() if d.is_dir() and not d.name.startswith('.'))
    if not fixture_dirs:
        print('No fixture directories found.', file=sys.stderr)
        return 1
    all_errors = []
    results = []
    for fixture_dir in fixture_dirs:
        errors = validate_fixture(fixture_dir, contract_template, runtime_template)
        passed = len(errors) == 0
        results.append((fixture_dir.name, passed))
        all_errors.extend(errors)
    for name, passed in results:
        print(f"  {'PASS' if passed else 'FAIL'}  {name}")
    if all_errors:
        print()
        for err in all_errors:
            print(f"       {err}")
        print(f"\n{len(all_errors)} error(s) found across {len(fixture_dirs)} fixture(s).")
        return 1
    print(f"\nAll {len(fixture_dirs)} fixture(s) passed.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
