# Before/After: Durable Contract Split

This example shows the exact structural change `make-harness` now encourages.

## Before

A single file tried to carry two responsibilities at once:

- durable project defaults that should survive across clones and commits
- volatile runtime state such as interview progress and sync metadata

```json
{
  "bootstrap_status": "interview_in_progress",
  "interview_step": "verification_policy",
  "sync_status": "drifted",
  "communication_language": "ko",
  "project_type": "legacy",
  "definition_of_done": "working_code_verified",
  "project_commands": {
    "test": "pnpm test",
    "lint": "pnpm lint"
  }
}
```

Why this is weak:

- runtime-only fields create noisy diffs and merge conflicts
- teams get pushed toward gitignoring the whole file
- once that happens, the durable machine-readable contract is no longer a reliable canonical source

## After

The durable contract and volatile runtime state are split.

### `harness-contract.json`

Commit this file.

```json
{
  "harness_version": 2,
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
  "communication_language": "ko",
  "project_type": "legacy",
  "definition_of_done": "working_code_verified",
  "change_posture": "conservative",
  "change_guardrails": [
    "avoid broad rewrites without approval"
  ],
  "verification_policy": "required"
}
```

### `harness-runtime.json`

Treat this as volatile and gitignore it in shared repos when appropriate.

```json
{
  "harness_version": 2,
  "run_mode": "refresh",
  "bootstrap_status": "configured",
  "interview_step": "complete",
  "pending_fields": [],
  "confirmed_fields": [
    "communication_language",
    "project_type",
    "definition_of_done"
  ],
  "validated_shared_fields": [
    "communication_language",
    "project_type",
    "definition_of_done"
  ],
  "sync_status": "healthy",
  "entry_files_sync": {
    "status": "healthy"
  },
  "language_detection": {
    "strategy": "detect_first_then_confirm",
    "repo_signal": "korean_readme",
    "confidence": "high"
  }
}
```

## What improved

- canonical durable state stays committable
- runtime churn no longer pollutes the durable contract
- repair can normalize durable and volatile state separately
- entry files can stay thin because they point to a cleaner source model

## Practical takeaway

If a field should survive as a stable project rule, put it in the durable contract.
If a field only exists to help the current setup, audit, or sync run, put it in runtime state.
