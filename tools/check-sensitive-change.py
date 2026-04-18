#!/usr/bin/env python3
"""Diff-sensitive guardrail checker for make-harness."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SENSITIVE_TOKENS = {
    "auth": ["auth", "login", "oauth", "session", "token"],
    "permissions": ["permission", "permissions", "role", "roles", "acl"],
    "secrets": ["secret", "secrets", "api_key", "apikey", "token", "credential"],
    "payments": ["payment", "payments", "billing", "invoice", "checkout", "stripe"],
    "encryption": ["tls", "ssl", "cert", "crypto", "encrypt", "decrypt", "verify"],
    "public_api": ["api", "route", "routes", "controller", "openapi", "public"],
}
ENFORCEMENT_FIELDS = ["change_guardrails", "verification_policy", "approval_policy"]


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def _normalize_paths(paths: list[str]) -> list[str]:
    return [p.replace("\\", "/").lower() for p in paths]


def detect_sensitive_categories(paths: list[str]) -> dict[str, list[str]]:
    normalized = _normalize_paths(paths)
    hits: dict[str, list[str]] = {}
    for category, tokens in SENSITIVE_TOKENS.items():
        matched = [path for path in normalized if any(token in path for token in tokens)]
        if matched:
            hits[category] = matched
    return hits


def describe_sensitive_change(repo_root: Path | str, paths: list[str]) -> str:
    repo_root = Path(repo_root).resolve()
    contract = _load_json(repo_root / "harness-contract.json")
    categories = detect_sensitive_categories(paths)
    if not categories:
        return "PASS: no sensitive changes detected"

    strengths = contract.get("rule_strengths", {})
    active_strengths = ", ".join(f"{field}={strengths.get(field, 'unknown')}" for field in ENFORCEMENT_FIELDS)
    categories_text = ", ".join(sorted(categories))
    matched_paths = sorted({path for values in categories.values() for path in values})
    return f"Sensitive categories: {categories_text}; paths: {matched_paths}; enforcement: {active_strengths}"


def check_sensitive_change(repo_root: Path | str, paths: list[str]) -> list[str]:
    repo_root = Path(repo_root).resolve()
    contract = _load_json(repo_root / "harness-contract.json")
    categories = detect_sensitive_categories(paths)
    if not categories:
        return []

    strengths = contract.get("rule_strengths", {})
    enforced_fields = [field for field in ENFORCEMENT_FIELDS if strengths.get(field) == "enforced"]
    if not enforced_fields:
        return []

    categories_text = ", ".join(sorted(categories))
    path_text = sorted({path for paths_for_category in categories.values() for path in paths_for_category})
    return [
        f"sensitive change detected in categories [{categories_text}] for paths {path_text}",
        f"blocked by enforced guardrails: {', '.join(f'{field}=enforced' for field in enforced_fields)}",
    ]


def changed_paths_from_git(repo_root: Path, base: str, head: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base}..{head}"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python tools/check-sensitive-change.py /path/to/project [--paths file1 file2 ... | --base <git-ref> --head <git-ref>]")
        return 2

    repo_root = Path(argv[1]).resolve()
    paths: list[str] = []
    if "--paths" in argv:
        idx = argv.index("--paths")
        paths = argv[idx + 1 :]
    elif "--base" in argv and "--head" in argv:
        base = argv[argv.index("--base") + 1]
        head = argv[argv.index("--head") + 1]
        paths = changed_paths_from_git(repo_root, base, head)
    else:
        print("Usage: python tools/check-sensitive-change.py /path/to/project [--paths file1 file2 ... | --base <git-ref> --head <git-ref>]")
        return 2

    errors = check_sensitive_change(repo_root, paths)
    if errors:
        for error in errors:
            print(error)
        return 1

    print(describe_sensitive_change(repo_root, paths))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
