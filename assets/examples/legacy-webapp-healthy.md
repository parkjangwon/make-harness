# Healthy Harness Example: Legacy Web App

This example shows a compact healthy harness for a legacy web application.

## AGENTS.md

```md
# Agent Entry

Read `PROJECT_HARNESS.md` first.
Read `harness-state.json` before making assumptions.

- Treat `PROJECT_HARNESS.md` and `harness-state.json` as canonical.
- Keep changes conservative unless the contract says otherwise.
- Use this file only as a thin summary and pointer.
```

## CLAUDE.md

```md
# Claude Entry

Read `PROJECT_HARNESS.md` first.
Read `harness-state.json` before making assumptions.

- Treat `PROJECT_HARNESS.md` and `harness-state.json` as canonical.
- Keep changes conservative unless the contract says otherwise.
- Use this file only as a thin summary and pointer.
```

## GEMINI.md

```md
# Gemini Entry

Read `PROJECT_HARNESS.md` first.
Read `harness-state.json` before making assumptions.

- Treat `PROJECT_HARNESS.md` and `harness-state.json` as canonical.
- Keep changes conservative unless the contract says otherwise.
- Use this file only as a thin summary and pointer.
```

## PROJECT_HARNESS.md

```md
# Project Harness

## Summary
- Project type: `legacy`
- Communication language: Korean
- Communication tone: concise

## Shared Contract
- Definition of done: working code plus verification
- Change posture: conservative
- Verification policy: required
- Approval policy: dependencies, schema changes, and production config changes require approval
- Project commands:
  - test: `pnpm test`
  - lint: `pnpm lint`
  - build: `pnpm build`
  - dev: `pnpm dev`
- Project constraints:
  - keep existing routes and API responses stable
  - avoid broad refactors without approval
  - preserve user-authored docs and custom config blocks

## Environment
- Stack summary:
  - React
  - Vite
  - Node.js
- Environment:
  - development: local workstation
  - runtime: node
  - primary_os: macOS
```

## harness-state.json

```json
{
  "run_mode": "refresh",
  "bootstrap_status": "configured",
  "interview_step": "complete",
  "shared_contract_fields": [
    "communication_language",
    "project_type",
    "definition_of_done",
    "change_posture",
    "change_guardrails",
    "verification_policy",
    "approval_policy",
    "project_commands",
    "project_constraints",
    "communication_tone",
    "stack_summary",
    "environment"
  ],
  "pending_fields": [],
  "validated_shared_fields": [
    "communication_language",
    "project_type",
    "definition_of_done",
    "change_posture",
    "change_guardrails",
    "verification_policy",
    "approval_policy",
    "project_commands",
    "project_constraints",
    "communication_tone",
    "stack_summary",
    "environment"
  ],
  "drift_reasons": [],
  "sync_status": "healthy",
  "entry_files_sync": {
    "status": "healthy"
  },
  "communication_language": "ko",
  "project_type": "legacy",
  "change_posture": "conservative",
  "definition_of_done": "working_code_verified",
  "change_guardrails": [
    "preserve existing behavior unless explicitly changing it",
    "prefer small patches over broad rewrites"
  ],
  "verification_policy": "required",
  "approval_policy": "dependencies, schema changes, and production config changes require approval",
  "project_commands": {
    "test": "pnpm test",
    "lint": "pnpm lint",
    "build": "pnpm build",
    "dev": "pnpm dev"
  },
  "project_constraints": [
    "preserve existing routes and API responses",
    "avoid broad refactors without approval"
  ],
  "communication_tone": "concise",
  "stack_summary": [
    "react",
    "vite",
    "node"
  ],
  "environment": {
    "development": "local workstation",
    "runtime": "node",
    "primary_os": "macOS"
  }
}
```

## Why this example is healthy

- canonical sources carry the real contract
- entry files are short and aligned
- shared contract fields are explicit
- sync metadata is healthy
- no drift reasons remain
