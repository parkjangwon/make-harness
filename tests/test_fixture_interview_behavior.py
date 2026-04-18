from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "assets" / "fixtures"


def load_validator_module():
    path = ROOT / "tools" / "validate-fixtures.py"
    spec = importlib.util.spec_from_file_location("validate_fixtures", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name / "fixture.json").read_text())


def test_interview_heavy_fixtures_record_expected_planner_behavior():
    blank = load_fixture("bootstrap-empty-project-stack-discovery")
    detect = load_fixture("bootstrap-detect-korean")
    resume = load_fixture("resume-interview-after-partial-confirmation")

    assert blank["expected"]["interview_mode"] == "setup_discovery"
    assert blank["expected"]["next_question_field"] == "communication_language"
    assert blank["expected"]["next_question_style"] == "open"
    assert "runtime" in blank["expected"]["discovery_fields"]
    assert "package_manager" in blank["expected"]["discovery_fields"]

    assert detect["expected"]["interview_mode"] == "repo_first_gap_fill"
    assert detect["expected"]["next_question_style"] == "confirmation"

    assert resume["expected"]["run_mode"] == "update"
    assert resume["expected"]["next_question_field"] == "approval_policy"
    assert resume["expected"]["next_question_style"] == "open"


def test_validator_flags_fixture_when_expected_planner_behavior_disagrees_with_deterministic_plan():
    module = load_validator_module()
    fixture = {
        "name": "bad-planner-fixture",
        "purpose": "Existing repo should not ask blank-project discovery questions when package manager is already inferable.",
        "initial_conditions": {
            "managed_files_present": ["AGENTS.md"],
            "repo_language_signal": "korean_readme",
            "repo_language_confidence": "high",
            "pending_fields": ["communication_language"],
        },
        "expected": {
            "run_mode": "repair",
            "interview_mode": "setup_discovery",
            "next_question_field": "project_type",
            "next_question_style": "open",
            "discovery_fields": ["runtime", "package_manager"],
        },
    }

    errors = module.check_fixture_schema(fixture, fixture["name"])
    assert errors == []

    errors = module.cross_check_interview_plan(fixture, fixture["name"])

    assert any("expected.interview_mode" in error for error in errors)
    assert any("expected.next_question_field" in error for error in errors)
    assert any("expected.discovery_fields" in error for error in errors)
