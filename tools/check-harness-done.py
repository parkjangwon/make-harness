#!/usr/bin/env python3
"""Completion gate for a project-local harness."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRY_AND_PROJECT_FILES = ["AGENTS.md", "CLAUDE.md", "GEMINI.md", "PROJECT_HARNESS.md"]


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def check_harness_done(repo_root: Path | str) -> list[str]:
    repo_root = Path(repo_root).resolve()
    errors: list[str] = []

    audit_module = _load_module("audit_harness", ROOT / "tools" / "audit-harness.py")
    apply_module = _load_module("apply_harness", ROOT / "tools" / "apply-harness.py")

    errors.extend(audit_module.audit_repository(repo_root))
    if errors:
        return errors

    contract = _load_json(repo_root / "harness-contract.json")
    runtime = _load_json(repo_root / "harness-runtime.json")

    if runtime.get("bootstrap_status") != "configured":
        errors.append("bootstrap_status must be 'configured' before the harness is done")
    if runtime.get("sync_status") != "healthy":
        errors.append("sync_status must be 'healthy' before the harness is done")

    entry_sync = runtime.get("entry_files_sync") or {}
    if entry_sync.get("status") != "healthy":
        errors.append("entry_files_sync.status must be 'healthy' before the harness is done")

    if runtime.get("validated_shared_fields") != contract.get("shared_contract_fields"):
        errors.append("validated_shared_fields must exactly match shared_contract_fields before the harness is done")

    projections = apply_module.build_projection_files(contract, runtime)
    for name in ENTRY_AND_PROJECT_FILES:
        current = (repo_root / name).read_text()
        expected = projections[name]
        if current != expected:
            errors.append(f"projection drift detected: {name} does not match deterministic generator output")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python tools/check-harness-done.py /path/to/project")
        return 2
    errors = check_harness_done(argv[1])
    if errors:
        for error in errors:
            print(error)
        return 1
    print("PASS: harness completion gate satisfied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
