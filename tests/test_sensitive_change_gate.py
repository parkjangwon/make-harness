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


def make_repo(tmp_path: Path, *, enforced: bool) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    contract = deep_merge(
        load_json(ROOT / "assets" / "templates" / "harness-contract.json"),
        load_json(FIXTURES / "refresh-configured-healthy" / "expected-contract.json"),
    )
    strength = "enforced" if enforced else "guided"
    contract["rule_strengths"]["change_guardrails"] = strength
    contract["rule_strengths"]["verification_policy"] = strength
    contract["rule_strengths"]["approval_policy"] = strength
    (repo / "harness-contract.json").write_text(json.dumps(contract, indent=2, ensure_ascii=False) + "\n")
    return repo


def test_sensitive_change_gate_blocks_enforced_sensitive_changes(tmp_path):
    gate = load_module("check_sensitive_change", ROOT / "tools" / "check-sensitive-change.py")
    repo = make_repo(tmp_path, enforced=True)

    errors = gate.check_sensitive_change(repo, ["src/auth/login.py", "src/http/routes.py"])

    assert any("sensitive change detected" in error for error in errors)
    assert any("approval_policy=enforced" in error or "verification_policy=enforced" in error or "change_guardrails=enforced" in error for error in errors)


def test_sensitive_change_gate_allows_non_sensitive_changes(tmp_path):
    gate = load_module("check_sensitive_change", ROOT / "tools" / "check-sensitive-change.py")
    repo = make_repo(tmp_path, enforced=True)

    errors = gate.check_sensitive_change(repo, ["docs/notes.md", "README.md"])

    assert errors == []


def test_sensitive_change_gate_reports_guided_changes_without_blocking(tmp_path):
    gate = load_module("check_sensitive_change", ROOT / "tools" / "check-sensitive-change.py")
    repo = make_repo(tmp_path, enforced=False)

    errors = gate.check_sensitive_change(repo, ["config/tls-dev.yaml"])

    assert errors == []
    report = gate.describe_sensitive_change(repo, ["config/tls-dev.yaml"])
    assert "guided" in report
    assert "tls" in report.lower()
