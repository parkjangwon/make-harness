from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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


def make_repo_with_contract_runtime(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    contract = deep_merge(
        load_json(ROOT / "assets" / "templates" / "harness-contract.json"),
        load_json(FIXTURES / "refresh-configured-healthy" / "expected-contract.json"),
    )
    runtime = deep_merge(
        load_json(ROOT / "assets" / "templates" / "harness-runtime.json"),
        load_json(FIXTURES / "refresh-configured-healthy" / "expected-runtime.json"),
    )
    runtime.pop("phase", None)
    (repo / "harness-contract.json").write_text(json.dumps(contract, indent=2, ensure_ascii=False) + "\n")
    (repo / "harness-runtime.json").write_text(json.dumps(runtime, indent=2, ensure_ascii=False) + "\n")
    return repo


def test_generator_materializes_projection_files_from_contract_and_runtime(tmp_path):
    generator = load_module("apply_harness", ROOT / "tools" / "apply-harness.py")
    audit = load_module("audit_harness", ROOT / "tools" / "audit-harness.py")
    repo = make_repo_with_contract_runtime(tmp_path)

    generator.apply_harness(repo)

    assert (repo / "AGENTS.md").exists()
    assert (repo / "CLAUDE.md").exists()
    assert (repo / "GEMINI.md").exists()
    assert (repo / "PROJECT_HARNESS.md").exists()
    assert "# Agent Entry" in (repo / "AGENTS.md").read_text()
    assert "# Claude Entry" in (repo / "CLAUDE.md").read_text()
    assert "# Gemini Entry" in (repo / "GEMINI.md").read_text()

    project_harness = (repo / "PROJECT_HARNESS.md").read_text()
    assert "communication_language: ko" in project_harness
    assert "project_type: legacy" in project_harness
    assert "verification_policy: required" in project_harness
    assert "verification_policy: enforced" in project_harness
    assert "pnpm test" in project_harness
    assert "keep API responses backward compatible" in project_harness
    assert audit.audit_repository(repo) == []


def test_generator_repairs_drifted_projection_files_back_to_contract(tmp_path):
    generator = load_module("apply_harness", ROOT / "tools" / "apply-harness.py")
    audit = load_module("audit_harness", ROOT / "tools" / "audit-harness.py")
    repo = make_repo_with_contract_runtime(tmp_path)

    (repo / "AGENTS.md").write_text("# Agent Entry\n\nWrong summary.\n")
    (repo / "PROJECT_HARNESS.md").write_text("# broken\n")

    generator.apply_harness(repo)

    assert "Read `PROJECT_HARNESS.md` first." in (repo / "AGENTS.md").read_text()
    assert "## Durable contract values" in (repo / "PROJECT_HARNESS.md").read_text()
    assert audit.audit_repository(repo) == []
