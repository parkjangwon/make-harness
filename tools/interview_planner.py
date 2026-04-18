#!/usr/bin/env python3
"""Deterministic interview planning helpers for make-harness."""

from __future__ import annotations

import re
from typing import Any

QUESTION_ORDER = [
    "communication_language",
    "project_type",
    "definition_of_done",
    "change_posture",
    "change_guardrails",
    "verification_policy",
    "approval_policy",
    "project_commands",
    "project_constraints",
    "rule_strengths",
    "communication_tone",
    "stack_summary",
    "environment",
]
BLANK_PROJECT_DISCOVERY_FIELDS = [
    "communication_language",
    "project_type",
    "stack_summary",
    "runtime",
    "package_manager",
    "project_commands",
]


def _has_meaningful_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() not in {"", "unknown", "none"}
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    return True


def infer_project_state(initial_conditions: dict) -> str:
    if any(_has_meaningful_value(initial_conditions.get(key)) for key in ("package_manager", "runtime")):
        return "blank_project"

    managed_files = initial_conditions.get("managed_files_present") or []
    entry_files = initial_conditions.get("entry_files_present") or []
    if managed_files or entry_files or initial_conditions.get("canonical_sources_present"):
        return "existing_repository"

    if initial_conditions.get("repo_language_signal"):
        return "existing_repository"

    notes = " ".join(initial_conditions.get("notes") or []).lower()
    if any(token in notes for token in ("readme", "comments", "codebase", "repository signals", "code to inspect")):
        return "existing_repository"

    return "blank_project"


def infer_interview_mode(initial_conditions: dict) -> str:
    return "setup_discovery" if infer_project_state(initial_conditions) == "blank_project" else "repo_first_gap_fill"


def remaining_fields(initial_conditions: dict) -> list[str]:
    pending = initial_conditions.get("pending_fields")
    confirmed = set(initial_conditions.get("confirmed_fields") or [])
    if isinstance(pending, list) and pending:
        ordered_pending = [field for field in QUESTION_ORDER if field in pending and field not in confirmed]
        extras = [field for field in pending if field not in QUESTION_ORDER and field not in confirmed]
        return ordered_pending + extras
    return [field for field in QUESTION_ORDER if field not in confirmed]


def classify_question_style(field: str, initial_conditions: dict) -> str:
    confidence = initial_conditions.get("repo_language_confidence")
    project_state = infer_project_state(initial_conditions)

    if field == "communication_language":
        if confidence == "high":
            return "confirmation"
        if confidence == "medium":
            return "either_or"
        return "open"

    if project_state == "blank_project":
        return "open"

    if field in {"project_commands", "stack_summary", "environment", "project_type"}:
        if confidence == "high":
            return "confirmation"
        if confidence == "medium":
            return "either_or"

    return "open"


def classify_answer_mode(answer: str) -> str:
    text = (answer or "").strip().lower()

    safe_default_patterns = [
        "잘 모르겠",
        "아직 안 정",
        "모르겠어요",
        "not sure",
        "don't know",
        "do not know",
        "undecided",
    ]
    if any(pattern in text for pattern in safe_default_patterns):
        return "safe_default"

    precision_patterns = [
        r"\b(npm|pnpm|yarn|pytest|py_compile|bun|cargo|make)\b",
        r"\bbuild[: -]",
        r"\btest[: -]",
        r"\blint[: -]",
        r"\boverride\b",
        r"\bexplicit\b",
        r"\bverify\b",
        r"`[^`]+`",
    ]
    if any(re.search(pattern, text) for pattern in precision_patterns):
        return "precision"

    clarify_patterns = [
        "대충",
        "느낌",
        "아마",
        "같긴 한데",
        "애매",
        "sort of",
        "kind of",
        "roughly",
    ]
    if any(pattern in text for pattern in clarify_patterns):
        return "clarify"

    return "precision" if len(text.split()) >= 8 else "clarify"


def plan_interview(initial_conditions: dict) -> dict:
    project_state = infer_project_state(initial_conditions)
    interview_mode = infer_interview_mode(initial_conditions)
    remaining = remaining_fields(initial_conditions)
    next_field = remaining[0] if remaining else "complete"

    discovery_fields = list(BLANK_PROJECT_DISCOVERY_FIELDS if project_state == "blank_project" else [])
    skip_fields = []
    if project_state == "existing_repository":
        skip_fields.extend(["runtime", "package_manager"])

    return {
        "project_state": project_state,
        "interview_mode": interview_mode,
        "remaining_fields": remaining,
        "next_question_field": next_field,
        "next_question_style": classify_question_style(next_field, initial_conditions) if next_field != "complete" else "none",
        "discovery_fields": discovery_fields,
        "skip_fields": skip_fields,
    }


if __name__ == "__main__":
    import json
    import sys

    payload = json.loads(sys.stdin.read() or "{}")
    print(json.dumps(plan_interview(payload), indent=2, ensure_ascii=False))
