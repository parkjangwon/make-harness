#!/usr/bin/env python3
"""Lightweight harness auditor for make-harness."""

from __future__ import annotations

import json
import sys
from pathlib import Path

MANAGED = [
    'AGENTS.md',
    'CLAUDE.md',
    'GEMINI.md',
    'PROJECT_HARNESS.md',
    'harness-contract.json',
    'harness-runtime.json',
]
ENTRY_FILES = ['AGENTS.md', 'CLAUDE.md', 'GEMINI.md']
ENTRY_REQUIRED_LINES = [
    'Read `PROJECT_HARNESS.md` first.',
    'Read `harness-contract.json` for durable defaults.',
    'Read `harness-runtime.json` only for current interview/runtime state.',
]
SHARED_CONTRACT_FIELDS = [
    'communication_language',
    'project_type',
    'definition_of_done',
    'change_posture',
    'change_guardrails',
    'verification_policy',
    'approval_policy',
    'project_commands',
    'project_constraints',
    'rule_strengths',
    'communication_tone',
    'stack_summary',
    'environment',
]
RULE_STRENGTH_FIELDS = [
    'change_guardrails',
    'verification_policy',
    'approval_policy',
    'project_constraints',
    'communication_tone',
]
VALID_RULE_STRENGTHS = {'advisory', 'guided', 'enforced'}
CONTRACT_ALLOWED_META_FIELDS = {
    'harness_version',
    '_file_role',
    '_commit_policy',
    'shared_contract_fields',
    'change_history',
    'notes',
}
RUNTIME_REQUIRED_FIELDS = {
    'harness_version',
    '_file_role',
    '_gitignore_note',
    '_volatile_fields',
    'run_mode',
    'bootstrap_status',
    'interview_step',
    'pending_fields',
    'confirmed_fields',
    'validated_shared_fields',
    'drift_reasons',
    'sync_status',
    'entry_files_sync',
    'language_detection',
    'managed_files',
    'last_audit_at',
    'last_validated_at',
}
VALID_RUN_MODES = {'bootstrap', 'update', 'repair'}
VALID_BOOTSTRAP_STATUSES = {'pending_interview', 'interview_in_progress', 'configured'}
VALID_SYNC_STATUSES = {'healthy', 'drifted', 'unvalidated', 'unknown'}
VALID_LANGUAGE_CONFIDENCE = {'low', 'medium', 'high'}
MAX_ENTRY_NON_EMPTY_LINES = 18
PROJECT_HARNESS_REQUIRED_SECTION_ALIASES = {
    "status": ["## Status", "## 상태"],
    "canonical_model": ["## Canonical model", "## 기준 모델"],
    "agent_defaults": ["## Agent defaults", "## 에이전트 기본 원칙"],
    "durable_contract_fields": ["## Durable contract fields", "## 지속 계약 필드"],
    "runtime_state_fields": ["## Runtime state fields", "## 런타임 상태 필드"],
    "state_invariants": ["## State invariants", "## 상태 불변식"],
    "entry_file_principles": ["## Entry file principles", "## 진입 파일 원칙"],
    "repair_order": ["## Repair order", "## 복구 순서"],
    "pre_completion_checklist": ["## Pre-completion checklist", "## 완료 전 체크리스트"],
    "change_history": ["## Change history", "## 변경 이력"],
}


def _load_json(path: Path, errors: list[str]) -> dict | None:
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f'{path.name}: invalid JSON ({exc.msg} at line {exc.lineno}, column {exc.colno})')
    return None


def _check_entry_files(root: Path, errors: list[str]) -> None:
    for entry in ENTRY_FILES:
        text = (root / entry).read_text()
        lines = [line for line in text.splitlines() if line.strip()]
        if len(lines) > MAX_ENTRY_NON_EMPTY_LINES:
            errors.append(f'{entry}: too thick ({len(lines)} non-empty lines)')
        for required_line in ENTRY_REQUIRED_LINES:
            if required_line not in text:
                errors.append(f'{entry}: missing canonical pointer line: {required_line}')


def _check_project_harness(root: Path, errors: list[str]) -> None:
    text = (root / 'PROJECT_HARNESS.md').read_text()
    for section_name, aliases in PROJECT_HARNESS_REQUIRED_SECTION_ALIASES.items():
        if not any(alias in text for alias in aliases):
            errors.append(f'PROJECT_HARNESS.md missing required section: {aliases[0]}')
    if 'harness-contract.json' not in text or 'harness-runtime.json' not in text:
        errors.append('PROJECT_HARNESS.md must describe the contract/runtime split explicitly')
    if '| Date | Change | Target | Reason |' not in text:
        errors.append('PROJECT_HARNESS.md must include the durable change-history table header')


def _check_contract(contract: dict, errors: list[str]) -> None:
    if contract.get('_file_role') != 'durable_project_contract':
        errors.append('harness-contract.json has invalid _file_role')

    if contract.get('harness_version') != 2:
        errors.append('harness-contract.json has invalid harness_version')

    shared_fields = contract.get('shared_contract_fields')
    if shared_fields != SHARED_CONTRACT_FIELDS:
        errors.append('harness-contract.json shared_contract_fields must exactly match the canonical ordered field list')

    missing_contract_fields = sorted(set(SHARED_CONTRACT_FIELDS) - set(contract))
    if missing_contract_fields:
        errors.append(f'harness-contract.json missing required contract field(s): {missing_contract_fields}')

    rule_strengths = contract.get('rule_strengths')
    if not isinstance(rule_strengths, dict):
        errors.append('harness-contract.json rule_strengths must be an object')
    else:
        if sorted(rule_strengths) != sorted(RULE_STRENGTH_FIELDS):
            errors.append(f'harness-contract.json rule_strengths must define exactly {RULE_STRENGTH_FIELDS}')
        invalid_strengths = {
            field: value for field, value in rule_strengths.items() if value not in VALID_RULE_STRENGTHS
        }
        if invalid_strengths:
            errors.append(f'harness-contract.json rule_strengths contains invalid rule strength values: {invalid_strengths}')

    leaked_runtime_fields = sorted((set(contract) - set(SHARED_CONTRACT_FIELDS) - CONTRACT_ALLOWED_META_FIELDS) & RUNTIME_REQUIRED_FIELDS)
    if leaked_runtime_fields:
        errors.append(f'harness-contract.json contains runtime-only field(s): {leaked_runtime_fields}')


def _check_runtime(runtime: dict, errors: list[str]) -> None:
    if runtime.get('_file_role') != 'volatile_runtime_state':
        errors.append('harness-runtime.json has invalid _file_role')

    if runtime.get('harness_version') != 2:
        errors.append('harness-runtime.json has invalid harness_version')

    missing_runtime = sorted(RUNTIME_REQUIRED_FIELDS - set(runtime))
    if missing_runtime:
        errors.append(f'harness-runtime.json missing required runtime field(s): {missing_runtime}')

    volatile_fields = runtime.get('_volatile_fields')
    expected_volatile_fields = [
        'run_mode',
        'bootstrap_status',
        'interview_step',
        'pending_fields',
        'confirmed_fields',
        'validated_shared_fields',
        'drift_reasons',
        'sync_status',
        'entry_files_sync',
        'last_audit_at',
        'last_validated_at',
        'language_detection',
    ]
    if volatile_fields != expected_volatile_fields:
        errors.append('harness-runtime.json _volatile_fields must exactly match the canonical ordered runtime field list')

    if runtime.get('run_mode') not in VALID_RUN_MODES:
        errors.append('harness-runtime.json has invalid run_mode')

    if runtime.get('bootstrap_status') not in VALID_BOOTSTRAP_STATUSES:
        errors.append('harness-runtime.json has invalid bootstrap_status')

    if runtime.get('sync_status') not in VALID_SYNC_STATUSES:
        errors.append('harness-runtime.json has invalid sync_status')

    pending_fields = runtime.get('pending_fields')
    confirmed_fields = runtime.get('confirmed_fields')
    validated_fields = runtime.get('validated_shared_fields')
    if not isinstance(pending_fields, list):
        errors.append('harness-runtime.json pending_fields must be a list')
    if not isinstance(confirmed_fields, list):
        errors.append('harness-runtime.json confirmed_fields must be a list')
    if not isinstance(validated_fields, list):
        errors.append('harness-runtime.json validated_shared_fields must be a list')

    if isinstance(pending_fields, list) and isinstance(confirmed_fields, list):
        overlap = sorted(set(pending_fields) & set(confirmed_fields))
        if overlap:
            errors.append(f'harness-runtime.json pending_fields and confirmed_fields overlap: {overlap}')

    if isinstance(validated_fields, list):
        unknown_validated = sorted(set(validated_fields) - set(SHARED_CONTRACT_FIELDS))
        if unknown_validated:
            errors.append(f'harness-runtime.json validated_shared_fields contains unknown fields: {unknown_validated}')

    if runtime.get('bootstrap_status') == 'configured' and runtime.get('pending_fields'):
        errors.append('harness-runtime.json has configured state with non-empty pending_fields')

    if runtime.get('bootstrap_status') == 'configured' and runtime.get('interview_step') != 'complete':
        errors.append('harness-runtime.json has configured state with incomplete interview_step')

    managed_files = runtime.get('managed_files')
    if managed_files != MANAGED:
        errors.append('harness-runtime.json managed_files must exactly match the canonical managed file list')

    entry_sync = runtime.get('entry_files_sync')
    if not isinstance(entry_sync, dict):
        errors.append('harness-runtime.json entry_files_sync must be an object')
    else:
        if entry_sync.get('status') not in VALID_SYNC_STATUSES:
            errors.append('harness-runtime.json entry_files_sync.status has invalid value')
        if entry_sync.get('entry_files') != ENTRY_FILES:
            errors.append('harness-runtime.json entry_files_sync.entry_files must exactly match the canonical entry file list')
        if entry_sync.get('required_shared_fields') != SHARED_CONTRACT_FIELDS:
            errors.append('harness-runtime.json entry_files_sync.required_shared_fields must exactly match the canonical ordered field list')
        if not isinstance(entry_sync.get('notes'), list):
            errors.append('harness-runtime.json entry_files_sync.notes must be a list')

    language_detection = runtime.get('language_detection')
    if not isinstance(language_detection, dict):
        errors.append('harness-runtime.json language_detection must be an object')
    else:
        if language_detection.get('strategy') != 'detect_first_then_confirm':
            errors.append('harness-runtime.json language_detection.strategy must be detect_first_then_confirm')
        if language_detection.get('confidence') not in VALID_LANGUAGE_CONFIDENCE:
            errors.append('harness-runtime.json language_detection.confidence has invalid value')

    leaked_contract_fields = sorted(set(SHARED_CONTRACT_FIELDS) & set(runtime))
    if leaked_contract_fields:
        errors.append(f'harness-runtime.json contains durable contract field(s): {leaked_contract_fields}')


def audit_repository(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    missing = [name for name in MANAGED if not (root / name).exists()]
    if missing:
        errors.append(f'missing managed files: {missing}')
        return errors

    _check_entry_files(root, errors)
    _check_project_harness(root, errors)

    contract = _load_json(root / 'harness-contract.json', errors)
    runtime = _load_json(root / 'harness-runtime.json', errors)
    if contract is None or runtime is None:
        return errors

    _check_contract(contract, errors)
    _check_runtime(runtime, errors)

    if contract.get('harness_version') != runtime.get('harness_version'):
        errors.append('harness-contract.json and harness-runtime.json must use the same harness_version')

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print('Usage: python tools/audit-harness.py /path/to/project', file=sys.stderr)
        return 2

    errors = audit_repository(Path(sys.argv[1]))
    if errors:
        for error in errors:
            print(error)
        return 1

    print('PASS: managed files present, contract/runtime split detected, entry files thin')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
