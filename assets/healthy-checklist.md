# Healthy Checklist

Use this checklist before treating a harness as healthy.

| Check | Healthy when |
|------|--------------|
| Managed files | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `PROJECT_HARNESS.md`, `harness-state.json` all exist |
| Canonical contract | `PROJECT_HARNESS.md` and `harness-state.json` agree on the shared contract schema |
| Entry files | `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` are thin and reflect the same contract summary |
| State invariants | `configured` implies `pending_fields: []` and `interview_step: complete` |
| Sync metadata | `sync_status: healthy`, `entry_files_sync.status: healthy`, and `validated_shared_fields` matches the checked shared contract fields |

If any row fails, the harness is not healthy yet.
