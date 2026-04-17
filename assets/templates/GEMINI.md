# Gemini Entry For make-harness

This file is part of the `make-harness` bootstrap template, not a completed project harness.
It is a thin synchronized projection of the shared project contract for Gemini-compatible tools.

Primary contract:
- Read `PROJECT_HARNESS.md` first.
- Read `harness-state.json` before making assumptions.

Bootstrap rules:
- Classify the run as `bootstrap`, `refresh`, or `repair` before changing harness files.
- If `harness-state.json` says `bootstrap_status` is `pending_interview`, do not treat the harness as configured.
- If `bootstrap_status` is `interview_in_progress`, continue the interview from the saved step.
- If `bootstrap_status` is `configured` but `pending_fields` is not empty, treat the harness state as inconsistent and repair it.
- Before changing project rules, inspect the repository and start a short setup interview.
- Ask the first setup question in English unless `harness-state.json` already confirms another communication language.
- Once `communication_language` is confirmed, switch the next question and all following interview questions into that language.
- Ask one durable setup question at a time, then reflect the answer into `harness-state.json` before asking the next one.
- Confirm or correct the project type (`greenfield` or `legacy`) with the user.
- Confirm durable defaults only: communication language, project type, definition of done, change posture, change guardrails, verification policy, approval boundary, project commands, project constraints, communication tone, stack summary, and environment.
- Prefer inferring app name, package structure, and entrypoints from the repository instead of asking by default.
- Do not store framework-level tactics such as parallel work, subagent loops, or review-loop strategies in the project harness.
- If harness files disagree, repair the managed harness state before treating the harness as healthy.
- If `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` diverge on shared contract points, repair them back to the same canonical contract.

Working rules:
- Keep this file thin. Shared operating rules belong in `PROJECT_HARNESS.md`.
- Treat this file as a pointer and summary, not the canonical location for the full project contract.
- Treat `bugfix`, `feature`, `maintenance`, and `refactor` as per-request interpretation, not permanent harness state.
- If the user already has custom `GEMINI.md` content in another project, preserve it and update only a harness-managed block.
- Keep `AGENTS.md` and `CLAUDE.md` aligned as thin entry files that point back to the same project harness.
