from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "assets" / "templates"


def load_audit_module():
    path = ROOT / "tools" / "audit-harness.py"
    spec = importlib.util.spec_from_file_location("audit_harness", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def make_sample_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "sample"
    repo.mkdir()
    for name in ["AGENTS.md", "CLAUDE.md", "GEMINI.md", "PROJECT_HARNESS.md", "harness-contract.json", "harness-runtime.json"]:
        (repo / name).write_text((TEMPLATES / name).read_text())
    return repo


def test_audit_repository_passes_for_template_sample(tmp_path):
    module = load_audit_module()
    repo = make_sample_repo(tmp_path)

    errors = module.audit_repository(repo)

    assert errors == []


def test_audit_repository_flags_missing_shared_contract_fields(tmp_path):
    module = load_audit_module()
    repo = make_sample_repo(tmp_path)
    contract_path = repo / "harness-contract.json"
    contract = json.loads(contract_path.read_text())
    contract.pop("shared_contract_fields")
    contract_path.write_text(json.dumps(contract, indent=2) + "\n")

    errors = module.audit_repository(repo)

    assert any("shared_contract_fields" in error for error in errors)


def test_audit_repository_flags_missing_project_harness_sections(tmp_path):
    module = load_audit_module()
    repo = make_sample_repo(tmp_path)
    (repo / "PROJECT_HARNESS.md").write_text("# make-harness Project Harness\n\n## Status\n\nToo short.\n")

    errors = module.audit_repository(repo)

    assert any("PROJECT_HARNESS.md missing required section" in error for error in errors)


def test_audit_repository_flags_invalid_rule_strengths(tmp_path):
    module = load_audit_module()
    repo = make_sample_repo(tmp_path)
    contract_path = repo / "harness-contract.json"
    contract = json.loads(contract_path.read_text())
    contract["rule_strengths"] = {
        "approval_policy": "strictest",
        "verification_policy": "guided",
    }
    contract_path.write_text(json.dumps(contract, indent=2) + "\n")

    errors = module.audit_repository(repo)

    assert any("rule_strengths" in error for error in errors)


def test_audit_repository_flags_thick_entry_file(tmp_path):
    module = load_audit_module()
    repo = make_sample_repo(tmp_path)
    thick = "\n".join([f"line {i}" for i in range(25)]) + "\n"
    (repo / "AGENTS.md").write_text(thick)

    errors = module.audit_repository(repo)

    assert any("too thick" in error for error in errors)


def test_audit_repository_flags_missing_entry_pointer_line(tmp_path):
    module = load_audit_module()
    repo = make_sample_repo(tmp_path)
    (repo / "AGENTS.md").write_text("# Agent Entry\n\nShort but wrong.\n")

    errors = module.audit_repository(repo)

    assert any("missing canonical pointer line" in error for error in errors)


def test_audit_repository_flags_malformed_runtime_json(tmp_path):
    module = load_audit_module()
    repo = make_sample_repo(tmp_path)
    (repo / "harness-runtime.json").write_text('{"broken": true\n')

    errors = module.audit_repository(repo)

    assert any("invalid JSON" in error for error in errors)


def test_audit_repository_flags_runtime_contract_field_leakage(tmp_path):
    module = load_audit_module()
    repo = make_sample_repo(tmp_path)
    runtime_path = repo / "harness-runtime.json"
    runtime = json.loads(runtime_path.read_text())
    runtime["communication_language"] = "ko"
    runtime_path.write_text(json.dumps(runtime, indent=2) + "\n")

    errors = module.audit_repository(repo)

    assert any("contains durable contract field" in error for error in errors)


def test_audit_repository_flags_configured_runtime_with_incomplete_interview(tmp_path):
    module = load_audit_module()
    repo = make_sample_repo(tmp_path)
    runtime_path = repo / "harness-runtime.json"
    runtime = json.loads(runtime_path.read_text())
    runtime["bootstrap_status"] = "configured"
    runtime["interview_step"] = "project_type"
    runtime["pending_fields"] = []
    runtime_path.write_text(json.dumps(runtime, indent=2) + "\n")

    errors = module.audit_repository(repo)

    assert any("incomplete interview_step" in error for error in errors)
