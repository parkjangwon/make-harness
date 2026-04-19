from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "assets" / "templates"
FIXTURES = ROOT / "assets" / "fixtures"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def deep_merge(base: dict, overlay: dict) -> dict:
    merged = json.loads(json.dumps(base))
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def materialize_repo(tmp_path: Path, *, contract_overlay: dict | None = None, runtime_overlay: dict | None = None) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()

    for name in ["AGENTS.md", "CLAUDE.md", "GEMINI.md", "PROJECT_HARNESS.md"]:
        shutil.copy2(TEMPLATES / name, repo / name)

    contract = load_json(TEMPLATES / "harness-contract.json")
    runtime = load_json(TEMPLATES / "harness-runtime.json")

    if contract_overlay:
        contract = deep_merge(contract, contract_overlay)
    if runtime_overlay:
        runtime = deep_merge(runtime, runtime_overlay)

    (repo / "harness-contract.json").write_text(json.dumps(contract, indent=2, ensure_ascii=False) + "\n")
    (repo / "harness-runtime.json").write_text(json.dumps(runtime, indent=2, ensure_ascii=False) + "\n")
    return repo


def test_blank_project_e2e_starts_with_setup_discovery_questions():
    planner = load_module("interview_planner", ROOT / "tools" / "interview_planner.py")
    fixture = load_json(FIXTURES / "bootstrap-empty-project-stack-discovery" / "fixture.json")

    plan = planner.plan_interview(fixture["initial_conditions"])

    assert plan["project_state"] == "blank_project"
    assert plan["interview_mode"] == "setup_discovery"
    assert plan["next_question_field"] == "communication_language"
    assert "runtime" in plan["discovery_fields"]
    assert "package_manager" in plan["discovery_fields"]


def test_existing_repo_e2e_starts_with_detect_first_confirmation():
    planner = load_module("interview_planner", ROOT / "tools" / "interview_planner.py")
    fixture = load_json(FIXTURES / "bootstrap-detect-korean" / "fixture.json")

    plan = planner.plan_interview(fixture["initial_conditions"])

    assert plan["project_state"] == "existing_repository"
    assert plan["interview_mode"] == "repo_first_gap_fill"
    assert plan["next_question_field"] == "communication_language"
    assert plan["next_question_style"] == "confirmation"
    assert "runtime" in plan["skip_fields"]
    assert "package_manager" in plan["skip_fields"]


def test_materialized_healthy_repo_passes_real_audit_and_uses_update_mode(tmp_path):
    audit = load_module("audit_harness", ROOT / "tools" / "audit-harness.py")
    contract_overlay = load_json(FIXTURES / "refresh-configured-healthy" / "expected-contract.json")
    runtime_overlay = load_json(FIXTURES / "refresh-configured-healthy" / "expected-runtime.json")
    runtime_overlay.pop("phase", None)

    repo = materialize_repo(tmp_path, contract_overlay=contract_overlay, runtime_overlay=runtime_overlay)

    errors = audit.audit_repository(repo)

    assert runtime_overlay["run_mode"] == "update"
    assert errors == []


def test_materialized_repo_with_missing_runtime_file_is_detected_as_repair_need(tmp_path):
    audit = load_module("audit_harness", ROOT / "tools" / "audit-harness.py")
    contract_overlay = load_json(FIXTURES / "refresh-configured-healthy" / "expected-contract.json")
    runtime_overlay = load_json(FIXTURES / "refresh-configured-healthy" / "expected-runtime.json")
    runtime_overlay.pop("phase", None)

    repo = materialize_repo(tmp_path, contract_overlay=contract_overlay, runtime_overlay=runtime_overlay)
    (repo / "harness-runtime.json").unlink()

    errors = audit.audit_repository(repo)

    assert any("missing managed files" in error for error in errors)


def test_materialized_repo_with_entry_drift_is_detected_by_real_audit(tmp_path):
    audit = load_module("audit_harness", ROOT / "tools" / "audit-harness.py")
    contract_overlay = load_json(FIXTURES / "refresh-configured-healthy" / "expected-contract.json")
    runtime_overlay = load_json(FIXTURES / "refresh-configured-healthy" / "expected-runtime.json")
    runtime_overlay.pop("phase", None)

    repo = materialize_repo(tmp_path, contract_overlay=contract_overlay, runtime_overlay=runtime_overlay)
    (repo / "AGENTS.md").write_text("# Agent Entry\n\nWrong summary.\n")

    errors = audit.audit_repository(repo)

    assert any("missing canonical pointer line" in error for error in errors)


def test_generated_entry_files_include_concise_project_specific_summary(tmp_path):
    apply = load_module("apply_harness", ROOT / "tools" / "apply-harness.py")
    contract_overlay = load_json(FIXTURES / "refresh-configured-healthy" / "expected-contract.json")
    runtime_overlay = load_json(FIXTURES / "refresh-configured-healthy" / "expected-runtime.json")
    runtime_overlay.pop("phase", None)

    repo = materialize_repo(tmp_path, contract_overlay=contract_overlay, runtime_overlay=runtime_overlay)
    apply.apply_harness(repo)

    agents_text = (repo / "AGENTS.md").read_text()

    assert "Current defaults:" in agents_text or "현재 기본값 요약:" in agents_text
    assert "communication_language" not in agents_text
    assert "pnpm test" in agents_text
    assert "risky changes" in agents_text or "위험한 변경" in agents_text


def test_generated_project_harness_uses_korean_headings_when_contract_language_is_korean(tmp_path):
    apply = load_module("apply_harness", ROOT / "tools" / "apply-harness.py")
    contract_overlay = load_json(FIXTURES / "refresh-configured-healthy" / "expected-contract.json")
    runtime_overlay = load_json(FIXTURES / "refresh-configured-healthy" / "expected-runtime.json")
    runtime_overlay.pop("phase", None)

    repo = materialize_repo(tmp_path, contract_overlay=contract_overlay, runtime_overlay=runtime_overlay)
    apply.apply_harness(repo)

    harness_text = (repo / "PROJECT_HARNESS.md").read_text()

    assert "# 프로젝트 하네스" in harness_text
    assert "## 상태" in harness_text
    assert "## 지속 계약 값" in harness_text
    assert "## 변경 이력" in harness_text
