# Healthy Harness Example: Legacy Web App

## AGENTS.md

```md
# Agent Entry

Read `PROJECT_HARNESS.md` first.
Read `harness-contract.json` for durable defaults.
Read `harness-runtime.json` only for current interview/runtime state.

- Treat `PROJECT_HARNESS.md` and `harness-contract.json` as canonical.
- If `bootstrap_status` is not `configured`, inspect first and continue the setup interview.
```

## PROJECT_HARNESS.md

```md
# Project Harness

## Summary
- Project type: `legacy`
- Communication language: Korean
- Communication tone: concise
```

## harness-contract.json

```json
{
  "communication_language": "ko",
  "project_type": "legacy",
  "change_posture": "conservative"
}
```

## harness-runtime.json

```json
{
  "run_mode": "refresh",
  "bootstrap_status": "configured",
  "interview_step": "complete",
  "sync_status": "healthy",
  "entry_files_sync": {
    "status": "healthy"
  }
}
```
