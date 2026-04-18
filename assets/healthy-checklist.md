# Healthy Checklist

Use this checklist before treating a harness as healthy.

| Check | Healthy when |
|------|--------------|
| Managed files | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `PROJECT_HARNESS.md`, `harness-contract.json`, and `harness-runtime.json` all exist |
| Canonical contract | `PROJECT_HARNESS.md` and `harness-contract.json` agree on the shared contract schema, and `PROJECT_HARNESS.md` still includes the required structural sections |
| Runtime state | `harness-runtime.json` contains only volatile fields and passes invariants |
| Entry files | `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` are thin and reflect the same contract summary |
| Sync metadata | `sync_status: healthy`, `entry_files_sync.status: healthy`, and `validated_shared_fields` matches the checked shared contract fields |
| security-sensitive rules | project-local security guardrails are captured through existing durable fields such as `change_guardrails`, `approval_policy`, `verification_policy`, and `project_constraints`, without turning the harness into a full AppSec framework |

If any row fails, the harness is not healthy yet.
