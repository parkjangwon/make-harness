from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "assets" / "fixtures"


def load_planner_module():
    path = ROOT / "tools" / "interview_planner.py"
    spec = importlib.util.spec_from_file_location("interview_planner", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def load_fixture(name: str) -> dict:
    import json

    return json.loads((FIXTURES / name / "fixture.json").read_text())


def test_blank_project_plan_uses_setup_discovery_and_explicit_runtime_choices():
    planner = load_planner_module()
    fixture = load_fixture("bootstrap-empty-project-stack-discovery")

    plan = planner.plan_interview(fixture["initial_conditions"])

    assert plan["project_state"] == "blank_project"
    assert plan["interview_mode"] == "setup_discovery"
    assert plan["next_question_field"] == "communication_language"
    assert plan["next_question_style"] == "open"
    assert "runtime" in plan["discovery_fields"]
    assert "package_manager" in plan["discovery_fields"]
    assert "stack_summary" in plan["discovery_fields"]


def test_detect_first_repo_plan_uses_confirmation_when_language_confidence_is_high():
    planner = load_planner_module()
    fixture = load_fixture("bootstrap-detect-korean")

    plan = planner.plan_interview(fixture["initial_conditions"])

    assert plan["project_state"] == "existing_repository"
    assert plan["interview_mode"] == "repo_first_gap_fill"
    assert plan["next_question_field"] == "communication_language"
    assert plan["next_question_style"] == "confirmation"
    assert "runtime" not in plan["discovery_fields"]
    assert "package_manager" not in plan["discovery_fields"]


def test_conflicting_repo_signals_fall_back_to_open_question_not_overconfident_confirmation():
    planner = load_planner_module()
    fixture = load_fixture("bootstrap-conflicting-signals")

    plan = planner.plan_interview(fixture["initial_conditions"])

    assert plan["project_state"] == "existing_repository"
    assert plan["next_question_field"] == "communication_language"
    assert plan["next_question_style"] == "open"


def test_resume_plan_starts_from_first_pending_field_without_reasking_confirmed_fields():
    planner = load_planner_module()
    fixture = load_fixture("resume-interview-after-partial-confirmation")

    plan = planner.plan_interview(fixture["initial_conditions"])

    assert plan["project_state"] == "existing_repository"
    assert plan["interview_mode"] == "repo_first_gap_fill"
    assert plan["next_question_field"] == "approval_policy"
    assert plan["next_question_style"] == "open"
    assert "communication_language" not in plan["remaining_fields"]
    assert "project_type" not in plan["remaining_fields"]
    assert plan["remaining_fields"][0] == "approval_policy"


def test_answer_patterns_switch_between_precision_clarify_and_safe_default_modes():
    planner = load_planner_module()

    assert planner.classify_answer_mode("기본 verify는 pytest -q로 하고 코드 변경 시 py_compile도 추가해줘") == "precision"
    assert planner.classify_answer_mode("대충 웹앱 느낌이긴 한데 아직 확실하진 않아요") == "clarify"
    assert planner.classify_answer_mode("잘 모르겠어요. 아직 안 정했어요.") == "safe_default"
