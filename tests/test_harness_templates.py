from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "assets" / "templates"


def load_validator_module():
    path = ROOT / "tools" / "validate-fixtures.py"
    spec = importlib.util.spec_from_file_location("validate_fixtures", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_templates_split_durable_and_runtime_state():
    assert (TEMPLATES / "harness-contract.json").exists()
    assert (TEMPLATES / "harness-runtime.json").exists()
    assert not (TEMPLATES / "harness-state.json").exists()


def test_entry_files_stay_thin_and_point_to_new_sources():
    for name in ["AGENTS.md", "CLAUDE.md", "GEMINI.md"]:
        text = (TEMPLATES / name).read_text()
        assert "Read `PROJECT_HARNESS.md` first." in text
        assert "Read `harness-contract.json` for durable defaults." in text
        assert "Read `harness-runtime.json` only for current interview/runtime state." in text
        assert "Bootstrap rules:" not in text
        non_empty_lines = [line for line in text.splitlines() if line.strip()]
        assert len(non_empty_lines) <= 18, f"{name} is too thick: {len(non_empty_lines)} lines"


def test_validator_rejects_missing_required_keys_and_bad_sync_status():
    module = load_validator_module()
    contract = {
        "communication_language": "ko",
        "project_type": "legacy",
        "definition_of_done": "working_code_verified",
        "change_posture": "conservative",
        "change_guardrails": [],
        "verification_policy": "required",
        "approval_policy": "explicit_for_risky_changes",
        "project_commands": {"test": "pytest"},
        "project_constraints": [],
        "communication_tone": "concise",
        "stack_summary": ["python"],
        # environment intentionally missing
    }
    runtime = {
        "run_mode": "update",
        "bootstrap_status": "configured",
        "interview_step": "complete",
        "pending_fields": [],
        "confirmed_fields": list(module.SHARED_CONTRACT_FIELDS),
        "validated_shared_fields": list(module.SHARED_CONTRACT_FIELDS),
        "drift_reasons": [],
        "sync_status": "broken",
        "entry_files_sync": {"status": "healthy"},
        "last_audit_at": None,
        "last_validated_at": None,
    }

    errors = module.check_contract_runtime_alignment(contract, runtime, "unit-test")

    assert any("missing required contract field" in error for error in errors)
    assert any("invalid sync_status" in error for error in errors)


def test_validator_rejects_unknown_validated_shared_fields():
    module = load_validator_module()
    runtime = {
        "run_mode": "update",
        "bootstrap_status": "configured",
        "interview_step": "complete",
        "pending_fields": [],
        "confirmed_fields": [],
        "validated_shared_fields": ["communication_language", "imaginary_field"],
        "drift_reasons": [],
        "sync_status": "healthy",
        "entry_files_sync": {
            "status": "healthy",
            "entry_files": ["AGENTS.md", "CLAUDE.md", "GEMINI.md"],
            "required_shared_fields": list(module.SHARED_CONTRACT_FIELDS),
            "notes": [],
        },
        "language_detection": {
            "strategy": "detect_first_then_confirm",
            "repo_signal": "unknown",
            "confidence": "low",
        },
        "managed_files": ["AGENTS.md", "CLAUDE.md", "GEMINI.md", "PROJECT_HARNESS.md", "harness-contract.json", "harness-runtime.json"],
        "_volatile_fields": list(module.EXPECTED_VOLATILE_FIELDS),
        "last_audit_at": None,
        "last_validated_at": None,
    }

    errors = module.check_runtime_invariants(runtime, "unit-test")

    assert any("validated_shared_fields contains unknown fields" in error for error in errors)


def test_validator_rejects_wrong_contract_and_runtime_file_roles():
    module = load_validator_module()
    contract = json.loads((TEMPLATES / "harness-contract.json").read_text())
    runtime = json.loads((TEMPLATES / "harness-runtime.json").read_text())

    contract["_file_role"] = "volatile_runtime_state"
    runtime["_file_role"] = "durable_project_contract"

    errors = module.check_contract_runtime_alignment(contract, runtime, "unit-test")

    assert any("contract _file_role" in error for error in errors)
    assert any("runtime _file_role" in error for error in errors)


def test_validator_rejects_invalid_rule_strengths_shape_and_values():
    module = load_validator_module()
    contract = json.loads((TEMPLATES / "harness-contract.json").read_text())

    contract["rule_strengths"] = {
        "approval_policy": "strictest",
        "verification_policy": "guided",
    }

    errors = module.check_contract_runtime_alignment(contract, {}, "unit-test")

    assert any("rule_strengths must define exactly" in error for error in errors)
    assert any("invalid rule strength" in error for error in errors)


def test_refresh_fixture_includes_expected_contract_example():
    expected_contract = ROOT / "assets" / "fixtures" / "refresh-configured-healthy" / "expected-contract.json"
    assert expected_contract.exists()

    contract = json.loads(expected_contract.read_text())

    assert contract["communication_language"] == "ko"
    assert contract["project_type"] == "legacy"
    assert contract["project_commands"]["test"] == "pnpm test"
    assert contract["rule_strengths"]["verification_policy"] == "enforced"
    assert "shared_contract_fields" in contract


def test_single_entry_docs_prefer_update_when_harness_already_exists():
    skill = (ROOT / "SKILL.md").read_text()
    readme = (ROOT / "README.md").read_text()

    assert "single entry" in skill
    assert "If no harness exists, bootstrap it." in skill
    assert "If the harness exists and is healthy, enter update mode." in skill
    assert "If the harness exists but is drifted or broken, repair first" in skill
    assert "healthy harness -> update" in readme


def test_readme_documents_audit_success_and_failure_examples():
    readme = (ROOT / "README.md").read_text()

    assert "PASS: managed files present, contract/runtime split detected, entry files thin" in readme
    assert "missing managed files" in readme


def test_ci_workflow_exists_and_runs_core_checks():
    workflow = ROOT / ".github" / "workflows" / "validate.yml"
    assert workflow.exists()

    text = workflow.read_text()

    assert "python -m pip install pytest" in text
    assert "python3 -m pytest -q" in text
    assert "python3 tools/validate-fixtures.py" in text
    assert "python3 tools/audit-harness.py" in text
    assert "python3 -m py_compile tools/*.py tests/*.py" in text


def test_fixture_set_covers_missing_file_and_detect_first_language_cases():
    missing_runtime = ROOT / "assets" / "fixtures" / "repair-missing-runtime-file" / "fixture.json"
    detect_first = ROOT / "assets" / "fixtures" / "bootstrap-detect-korean" / "fixture.json"

    assert missing_runtime.exists()
    assert detect_first.exists()

    missing_runtime_text = missing_runtime.read_text()
    detect_first_text = detect_first.read_text()

    assert '"harness-runtime.json"' not in missing_runtime_text
    assert '"repo_language_signal": "korean_readme"' in detect_first_text


def test_examples_readme_mentions_rollout_and_mock_interview_examples():
    examples_readme = (ROOT / "assets" / "examples" / "README.md").read_text()

    assert "legacy-webapp-rollout.md" in examples_readme
    assert "mock-interview-junior-developer.md" in examples_readme
    assert "mock-interview-senior-developer.md" in examples_readme


def test_shared_contract_schema_stays_in_sync_across_validator_and_templates():
    module = load_validator_module()
    contract_template = json.loads((TEMPLATES / "harness-contract.json").read_text())
    runtime_template = json.loads((TEMPLATES / "harness-runtime.json").read_text())

    assert contract_template["shared_contract_fields"] == module.SHARED_CONTRACT_FIELDS
    assert runtime_template["pending_fields"] == module.SHARED_CONTRACT_FIELDS
    assert runtime_template["entry_files_sync"]["required_shared_fields"] == module.SHARED_CONTRACT_FIELDS
    assert runtime_template["managed_files"] == module.MANAGED_FILES
    assert runtime_template["_volatile_fields"] == module.EXPECTED_VOLATILE_FIELDS


def test_entry_templates_share_the_same_managed_rules():
    texts = [
        (TEMPLATES / "AGENTS.md").read_text().splitlines()[1:],
        (TEMPLATES / "CLAUDE.md").read_text().splitlines()[1:],
        (TEMPLATES / "GEMINI.md").read_text().splitlines()[1:],
    ]

    assert texts[0] == texts[1] == texts[2]


def test_validator_rejects_fixture_with_semantic_mismatch():
    module = load_validator_module()
    fixture = {
        "name": "broken-bootstrap",
        "purpose": "Empty repository without harness files should stay in bootstrap mode.",
        "initial_conditions": {
            "managed_files_present": ["harness-contract.json"],
        },
        "expected": {
            "run_mode": "bootstrap",
        },
    }

    errors = module.check_fixture_schema(fixture, "broken-bootstrap")

    assert any("purpose says no harness files exist" in error for error in errors)
