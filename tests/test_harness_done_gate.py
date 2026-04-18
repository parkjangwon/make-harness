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


def make_done_repo(tmp_path: Path) -> Path:
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
    apply_module = load_module("apply_harness", ROOT / "tools" / "apply-harness.py")
    apply_module.apply_harness(repo)
    return repo


def test_done_gate_passes_for_healthy_generated_harness(tmp_path):
    done_gate = load_module("check_harness_done", ROOT / "tools" / "check-harness-done.py")
    repo = make_done_repo(tmp_path)

    errors = done_gate.check_harness_done(repo)

    assert errors == []


def test_done_gate_rejects_unhealthy_sync_and_partial_validation(tmp_path):
    done_gate = load_module("check_harness_done", ROOT / "tools" / "check-harness-done.py")
    repo = make_done_repo(tmp_path)
    runtime_path = repo / "harness-runtime.json"
    runtime = json.loads(runtime_path.read_text())
    runtime["sync_status"] = "drifted"
    runtime["entry_files_sync"]["status"] = "drifted"
    runtime["validated_shared_fields"] = ["communication_language"]
    runtime_path.write_text(json.dumps(runtime, indent=2, ensure_ascii=False) + "\n")

    errors = done_gate.check_harness_done(repo)

    assert any("sync_status must be 'healthy'" in error for error in errors)
    assert any("entry_files_sync.status must be 'healthy'" in error for error in errors)
    assert any("validated_shared_fields must exactly match" in error for error in errors)


def test_done_gate_rejects_projection_drift_even_when_audit_files_exist(tmp_path):
    done_gate = load_module("check_harness_done", ROOT / "tools" / "check-harness-done.py")
    repo = make_done_repo(tmp_path)
    agents = (repo / "AGENTS.md").read_text().rstrip() + "\n- Manual note that still keeps the file thin.\n"
    (repo / "AGENTS.md").write_text(agents)

    errors = done_gate.check_harness_done(repo)

    assert any("projection drift detected" in error for error in errors)
