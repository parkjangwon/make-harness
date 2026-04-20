#!/usr/bin/env python3
"""Deterministically materialize harness projection files from contract/runtime state."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "assets" / "templates"
ENTRY_TITLES = {
    "AGENTS.md": "# Agent Entry",
    "CLAUDE.md": "# Claude Entry",
    "GEMINI.md": "# Gemini Entry",
}
DURABLE_FIELD_ORDER = [
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
RUNTIME_FIELD_ORDER = [
    "run_mode",
    "bootstrap_status",
    "interview_step",
    "pending_fields",
    "confirmed_fields",
    "validated_shared_fields",
    "drift_reasons",
    "sync_status",
    "entry_files_sync",
    "language_detection",
    "last_audit_at",
    "last_validated_at",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def render_scalar(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return str(value)


def render_list(items: list, indent: str = "  ") -> list[str]:
    if not items:
        return [f"{indent}- (none)"]
    lines: list[str] = []
    for item in items:
        if isinstance(item, dict):
            lines.append(f"{indent}-")
            lines.extend(render_dict(item, indent + "  "))
        else:
            lines.append(f"{indent}- {render_scalar(item)}")
    return lines


def render_dict(mapping: dict, indent: str = "  ") -> list[str]:
    if not mapping:
        return [f"{indent}- (none)"]
    lines: list[str] = []
    for key, value in mapping.items():
        if isinstance(value, dict):
            lines.append(f"{indent}- {key}:")
            lines.extend(render_dict(value, indent + "  "))
        elif isinstance(value, list):
            lines.append(f"{indent}- {key}:")
            lines.extend(render_list(value, indent + "  "))
        else:
            lines.append(f"{indent}- {key}: {render_scalar(value)}")
    return lines


def is_korean_contract(contract: dict) -> bool:
    return str(contract.get("communication_language", "")).strip().lower() == "ko"


def _verification_summary(contract: dict) -> str:
    commands = contract.get("project_commands") or {}
    ordered_keys = [key for key in ("test", "lint", "typecheck", "build") if commands.get(key)]
    if not ordered_keys:
        return "not set"
    return ", ".join(str(commands[key]) for key in ordered_keys)


def _approval_summary(contract: dict) -> str:
    approval_policy = contract.get("approval_policy")
    if approval_policy == "explicit_for_risky_changes":
        return "위험한 변경은 먼저 확인, 안전한 수정은 바로 진행"
    if approval_policy == "implicit_for_safe_changes":
        return "안전한 수정은 바로 진행, 위험한 변경은 별도 확인"
    if approval_policy == "explicit_for_all_changes":
        return "모든 변경 전에 먼저 확인"
    return render_scalar(approval_policy)


def render_entry_file(title: str, contract: dict) -> str:
    korean = is_korean_contract(contract)
    if korean:
        summary_heading = "현재 기본값 요약:"
        summary_lines = [
            f"- 언어: {render_scalar(contract.get('communication_language'))}",
            f"- 기본 검증: {_verification_summary(contract)}",
            f"- 승인 규칙: {_approval_summary(contract)}",
        ]
    else:
        summary_heading = "Current defaults:"
        summary_lines = [
            f"- language: {render_scalar(contract.get('communication_language'))}",
            f"- verification: {_verification_summary(contract)}",
            f"- approval: {render_scalar(contract.get('approval_policy'))}",
        ]
    return "\n".join(
        [
            title,
            "",
            "Read `PROJECT_HARNESS.md` first.",
            "Read `harness-contract.json` for durable defaults.",
            "Read `harness-runtime.json` only for current interview/runtime state.",
            "",
            summary_heading,
            *summary_lines,
            "",
            "- Treat `PROJECT_HARNESS.md` and `harness-contract.json` as canonical.",
            "- If `bootstrap_status` is not `configured`, inspect first and continue the setup interview.",
            "- Detect likely collaboration language from repo signals first; confirm it if unclear.",
            "- Prefer independent reviewer/evaluator checks for artifact quality; keep only the criteria and commands in the canonical contract.",
            "- Keep this file thin and preserve any user-authored content outside the harness-managed block.",
            "",
        ]
    )


def render_project_harness(contract: dict, runtime: dict) -> str:
    korean = is_korean_contract(contract)
    title = "# 프로젝트 하네스" if korean else "# make-harness Project Harness"
    section_status = "## 상태" if korean else "## Status"
    section_canonical = "## 기준 모델" if korean else "## Canonical model"
    section_defaults = "## 에이전트 기본 원칙" if korean else "## Agent defaults"
    section_fields = "## 지속 계약 필드" if korean else "## Durable contract fields"
    section_values = "## 지속 계약 값" if korean else "## Durable contract values"
    section_runtime = "## 런타임 상태 필드" if korean else "## Runtime state fields"
    section_invariants = "## 상태 불변식" if korean else "## State invariants"
    section_entry = "## 진입 파일 원칙" if korean else "## Entry file principles"
    section_repair = "## 복구 순서" if korean else "## Repair order"
    section_checklist = "## 완료 전 체크리스트" if korean else "## Pre-completion checklist"
    section_history = "## 변경 이력" if korean else "## Change history"

    lines = [
        title,
        "",
        section_status,
        "",
        f"- run_mode: {render_scalar(runtime.get('run_mode'))}",
        f"- bootstrap_status: {render_scalar(runtime.get('bootstrap_status'))}",
        f"- sync_status: {render_scalar(runtime.get('sync_status'))}",
        "- Durable contract lives in `PROJECT_HARNESS.md` and `harness-contract.json`.",
        "- Runtime interview/audit state lives in `harness-runtime.json`.",
        "- Treat `/make-harness` as a single entry command: bootstrap when no harness exists, update when a healthy harness exists, and repair when drift or breakage is detected first.",
        "",
        section_canonical,
        "",
        "- `PROJECT_HARNESS.md`: human-readable durable contract",
        "- `harness-contract.json`: machine-readable durable contract",
        "- `harness-runtime.json`: volatile interview, audit, and sync state",
        "- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`: thin projections only",
        "",
        section_defaults,
        "",
        "- Inspect the repository before asking for metadata that can be inferred.",
        "- Confirm durable project defaults, project-local security guardrails, and execution guardrails only.",
        "- Do not store framework-level tactics as permanent harness state.",
        "- Use detect-first language selection: infer likely collaboration language from repo signals, then confirm if needed.",
        "- Ask one interview question at a time and reflect runtime progress into `harness-runtime.json`.",
        "- Prefer independent review for artifact quality; keep the review criteria and verification commands in the contract, not the workflow topology.",
        "",
        section_fields,
        "",
        "These fields must stay synchronized across `PROJECT_HARNESS.md` and `harness-contract.json`:",
        "",
    ]
    lines.extend(f"- `{field}`" for field in DURABLE_FIELD_ORDER)
    lines.extend(
        [
            "",
            section_values,
            "",
        ]
    )
    for field in DURABLE_FIELD_ORDER:
        value = contract.get(field)
        if isinstance(value, dict):
            lines.append(f"- {field}:")
            lines.extend(render_dict(value))
        elif isinstance(value, list):
            lines.append(f"- {field}:")
            lines.extend(render_list(value))
        else:
            lines.append(f"- {field}: {render_scalar(value)}")
    lines.extend(
        [
            "",
            section_runtime,
            "",
            "`harness-runtime.json` tracks only volatile state such as:",
            "",
        ]
    )
    for field in RUNTIME_FIELD_ORDER:
        value = runtime.get(field)
        lines.append(f"- {field}:")
        if isinstance(value, dict):
            lines.extend(render_dict(value))
        elif isinstance(value, list):
            lines.extend(render_list(value))
        else:
            lines.append(f"  - {render_scalar(value)}")
    lines.extend(
        [
            "",
            section_invariants,
            "",
            "- `configured` implies `pending_fields` is empty.",
            "- `configured` implies `interview_step` is `complete`.",
            "- `pending_fields` and `confirmed_fields` must not overlap.",
            "- `validated_shared_fields` may contain only shared contract fields.",
            "- `last_validated_at` requires an explicit `sync_status` of `healthy` or `drifted`.",
            "",
            section_entry,
            "",
            "- Keep entry files short enough to stay obviously non-canonical.",
            "- Entry files point back to the canonical durable contract.",
            "- Entry files may mention runtime-state recovery, but must not duplicate the full policy block.",
            "",
            section_repair,
            "",
            "1. `harness-contract.json`",
            "2. `harness-runtime.json`",
            "3. `PROJECT_HARNESS.md`",
            "4. `AGENTS.md`",
            "5. `CLAUDE.md`",
            "6. `GEMINI.md`",
            "",
            "Repair durable contract first, then volatile runtime state, then projections.",
            "",
            section_checklist,
            "",
            "- All managed files exist.",
            "- `PROJECT_HARNESS.md` and `harness-contract.json` agree on shared contract fields.",
            "- `harness-runtime.json` invariants hold.",
            "- Entry files are thin and aligned.",
            "- `validated_shared_fields` matches what was actually checked.",
            "- Change history is updated when durable defaults change.",
            "",
            section_history,
            "",
            "| Date | Change | Target | Reason |",
            "|------|--------|--------|--------|",
        ]
    )
    change_history = contract.get("change_history") or []
    if change_history:
        for item in change_history:
            if isinstance(item, dict):
                lines.append(
                    f"| {render_scalar(item.get('date', 'unknown'))} | {render_scalar(item.get('change', 'unknown'))} | {render_scalar(item.get('target', 'unknown'))} | {render_scalar(item.get('reason', 'unknown'))} |"
                )
            else:
                lines.append(f"| unknown | {render_scalar(item)} | unknown | imported from contract |")
    else:
        lines.append("| YYYY-MM-DD | Initial harness setup or most recent update | Relevant files or policy | One-line explanation |")
    lines.append("")
    return "\n".join(lines)


def build_projection_files(contract: dict, runtime: dict) -> dict[str, str]:
    projections = {name: render_entry_file(title, contract) for name, title in ENTRY_TITLES.items()}
    projections["PROJECT_HARNESS.md"] = render_project_harness(contract, runtime)
    return projections


def apply_harness(repo_root: Path | str) -> None:
    repo_root = Path(repo_root).resolve()
    contract = load_json(repo_root / "harness-contract.json")
    runtime = load_json(repo_root / "harness-runtime.json")

    for name, content in build_projection_files(contract, runtime).items():
        (repo_root / name).write_text(content)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python tools/apply-harness.py /path/to/project")
        return 2
    apply_harness(argv[1])
    print("PASS: harness projections generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
