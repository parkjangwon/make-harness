# Before / After Example: Legacy Web App

This example shows the difference between a weak pre-harness state and a stable post-harness state.

## Before

```md
# AGENTS.md

- be careful
- run tests if possible
- don't break things
```

```md
# CLAUDE.md

- use Korean
- ask before major changes
```

```md
# GEMINI.md

- keep responses short
- try not to change too much
```

### What is wrong here

- each entry file carries a different partial contract
- no canonical source exists
- approval, verification, and completion standards are vague
- switching CLI can easily change behavior
- drift is hard to detect

## After

```md
# AGENTS.md

Read `PROJECT_HARNESS.md` first.
Read `harness-state.json` before making assumptions.

- Treat canonical sources as authoritative.
- Keep this file thin.
```

```md
# CLAUDE.md

Read `PROJECT_HARNESS.md` first.
Read `harness-state.json` before making assumptions.

- Treat canonical sources as authoritative.
- Keep this file thin.
```

```md
# GEMINI.md

Read `PROJECT_HARNESS.md` first.
Read `harness-state.json` before making assumptions.

- Treat canonical sources as authoritative.
- Keep this file thin.
```

```md
# PROJECT_HARNESS.md

## Shared Contract
- Project type: `legacy`
- Definition of done: working code plus verification
- Change posture: conservative
- Verification policy: required
- Approval policy: dependencies, schema changes, and production config changes require approval
- Project constraints:
  - preserve existing routes and API responses
  - avoid broad refactors without approval
```

```json
{
  "bootstrap_status": "configured",
  "interview_step": "complete",
  "sync_status": "healthy",
  "entry_files_sync": {
    "status": "healthy"
  },
  "drift_reasons": []
}
```

### What improved

- one canonical contract replaced three drifting mini-contracts
- completion, approval, and verification expectations became explicit
- default commands for checking and running work became explicit
- entry files became projections instead of competing sources of truth
- drift became easier to detect and repair
- switching tools is less likely to change the project contract
