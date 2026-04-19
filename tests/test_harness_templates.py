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


def test_skill_requires_runtime_state_to_move_to_update_on_healthy_rerun():
    skill = (ROOT / "SKILL.md").read_text()

    assert "rewrite `harness-runtime.json` with `run_mode: update`" in skill
    assert "healthy harness already exists" in skill


def test_interview_protocol_forbids_english_preface_when_korean_confidence_is_high():
    protocol = (ROOT / "references" / "interview-protocol.md").read_text()

    assert "Do not prepend English mode/status framing before the first Korean confirmation question" in protocol
    assert "If the current user message is already in Korean, keep the preface and the first question in Korean even when the repository itself is blank" in protocol
    assert "README가 한국어라 기본 협업 언어도 한국어로 보면 될까?" in protocol


def test_blank_project_protocol_explicitly_captures_typecheck_and_build_defaults():
    protocol = (ROOT / "references" / "interview-protocol.md").read_text()

    assert "typecheck" in protocol
    assert "build" in protocol
    assert "dev / build / test / lint / typecheck" in protocol


def test_readme_and_positioning_describe_make_harness_as_local_contract_layer_not_methodology():
    readme = (ROOT / "README.md").read_text()
    positioning = (ROOT / "docs" / "positioning.md").read_text()
    coexistence = (ROOT / "docs" / "coexistence.md").read_text()

    assert "project-local harness" in readme
    assert "durable contract bootstrap + maintenance" in readme
    assert "not a development methodology" in readme
    assert "not an execution framework" in readme
    assert "not an orchestration layer" in readme
    assert "framework-agnostic local rule layer" in positioning
    assert "does not replace stronger workflow or methodology frameworks" in coexistence
    assert "superpowers" in coexistence


def test_protocol_redefines_boundary_fields_as_repo_local_rules_not_general_methodology():
    protocol = (ROOT / "references" / "interview-protocol.md").read_text()

    assert "`definition_of_done` is stored as a repo-local completion expectation" in protocol
    assert "`verification_policy` is stored as the repository's default verification rule" in protocol
    assert "`approval_policy` is stored as the repository's confirmation rule for risky or sensitive changes" in protocol
    assert "`change_posture` is only a narrow local default for change scope" in protocol
    assert "Do not ask about TDD, branch strategy, code review loops, or sub-agent usage as durable contract state" in protocol


def test_examples_and_fixtures_describe_local_contract_collection_not_methodology_capture():
    fixtures = (ROOT / "assets" / "fixtures" / "README.md").read_text()
    examples = (ROOT / "assets" / "examples" / "README.md").read_text()

    assert "local contract" in fixtures
    assert "not to encode a development methodology" in fixtures
    assert "local project rules" in examples
    assert "not workflow prescriptions" in examples


def test_readme_documents_audit_success_and_failure_examples():
    readme = (ROOT / "README.md").read_text()

    assert "PASS: managed files present, contract/runtime split detected, entry files thin" in readme
    assert "missing managed files" in readme


def test_docs_reference_deterministic_projection_generator():
    readme = (ROOT / "README.md").read_text()
    skill = (ROOT / "SKILL.md").read_text()

    assert "python tools/apply-harness.py /path/to/project" in readme
    assert "Deterministic projection generator" in readme
    assert "tools/apply-harness.py" in skill


def test_docs_reference_harness_done_gate():
    readme = (ROOT / "README.md").read_text()
    skill = (ROOT / "SKILL.md").read_text()

    assert "python tools/check-harness-done.py /path/to/project" in readme
    assert "completion gate" in readme
    assert "tools/check-harness-done.py" in skill


def test_docs_reference_hook_template_and_sensitive_change_gate():
    readme = (ROOT / "README.md").read_text()
    skill = (ROOT / "SKILL.md").read_text()
    hook = ROOT / "assets" / "templates" / "pre-commit-harness.sh"
    hook_text = hook.read_text()

    assert "python tools/check-sensitive-change.py /path/to/project" in readme
    assert "pre-commit-harness.sh" in readme
    assert "check-sensitive-change.py" in skill
    assert hook.exists()
    assert "git diff --cached --name-only" in hook_text
    assert "MAKE_HARNESS_HOOK_MODE" in hook_text
    assert "HERMES_HOOK_MODE" not in hook_text
    assert "strict" in hook_text
    assert "warn" in hook_text
    assert "off" in hook_text
    assert "audit: pass" in hook_text
    assert "done-gate: pass" in hook_text
    assert "sensitive-change: pass" in hook_text


def test_readme_leads_with_painkiller_before_architecture():
    readme = (ROOT / "README.md").read_text()

    assert "## Why teams install this" in readme
    assert "AGENTS.md" in readme
    assert "CLAUDE.md" in readme
    assert "GEMINI.md" in readme
    assert "Before" in readme
    assert "After" in readme
    assert readme.index("## Why teams install this") < readme.index("## Structure")


def test_ci_workflow_exists_and_runs_core_checks():
    workflow = ROOT / ".github" / "workflows" / "validate.yml"
    assert workflow.exists()

    text = workflow.read_text()

    assert "python -m pip install pytest" in text
    assert "python3 -m pytest -q" in text
    assert "python3 tools/validate-fixtures.py" in text
    assert "python3 tools/audit-harness.py" in text
    assert "python3 tools/check-harness-done.py" in text
    assert "python3 tools/check-sensitive-change.py" in text
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


def test_rollout_example_has_concrete_before_after_painkiller_story():
    rollout = (ROOT / "assets" / "examples" / "legacy-webapp-rollout.md").read_text()

    assert "Before" in rollout
    assert "After" in rollout
    assert "AGENTS.md" in rollout
    assert "CLAUDE.md" in rollout
    assert "GEMINI.md" in rollout
    assert "repeated setup chatter" in rollout


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
