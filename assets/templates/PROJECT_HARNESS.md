# make-harness Project Harness

## Status

- This document is the bootstrap template, not a completed project contract.
- The current state assumes `pending_interview`.
- Inspect the repository and run a short interview before treating this as a real contract.
- A harness run is always classified as `bootstrap`, `refresh`, or `repair` before editing files.
- The interview goal is to confirm durable project defaults and guardrails — not to lock in framework-level tactics.

## Agent defaults

- Do not treat this document or `harness-state.json` alone as proof the project contract is final.
- Inspect the codebase, manifests, test presence, and environment signals first.
- Only ask the user about things that inspection cannot answer.
- Do not confirm `greenfield`/`legacy`, definition of done, change posture, verification intensity, or approval scope before the interview.
- Ask one question at a time during the interview. Reflect each answer into the state file before asking the next.
- Once `communication_language` is confirmed, use that language for all subsequent interview questions.
- When an existing harness is present, check for missing files and contract drift first.
- Do not hardcode framework tactics (parallel work, subagent loops, review loops) as permanent harness defaults.
- Infer app name, package structure, and entrypoints from the repository instead of asking.

## Interview questions

Always ask:
- What language should we use to collaborate?
- Should changes be careful, balanced, or bold by default?
- What should the agent avoid changing without explicit approval?
- Are there important project rules not visible from the repository?

Inspect first, then confirm as a single block:
- `project_type`: infer from git depth, package maturity, migration files
- `definition_of_done`: infer from CI presence
- `verification_policy`: infer from test suite presence
- `project_commands`: infer from `package.json`, `Makefile`, `pyproject.toml`, etc.
- `communication_tone`: default to `concise`
- `stack_summary`: infer from manifest files and directory layout
- `environment`: infer from `.nvmrc`, `Dockerfile`, `.python-version`, `go.mod`, etc.
- `approval_policy`: default based on `project_type`

## Interview state tracking

- `harness-state.json` records interview progress alongside the durable contract.
- `run_mode`: `bootstrap`, `refresh`, or `repair`
- `bootstrap_status`: `pending_interview`, `interview_in_progress`, or `configured`
- `interview_step`: current question field
- `pending_fields`: fields not yet confirmed
- `confirmed_fields`: fields already confirmed
- `sync_status`: synchronization health across harness files

## State invariants

- `configured` implies `pending_fields` is empty.
- `configured` implies `interview_step` is `complete`.
- `pending_fields` and `confirmed_fields` must not overlap.
- If `last_validated_at` is set, `sync_status` must be `healthy` or `drifted` — not `unknown` or `unvalidated`.
- A fully synchronized harness targets `sync_status: healthy`.

## Fields to populate after interview

- Project summary
- Communication language
- Project type
- Stack summary
- Development and runtime environment
- Definition of done
- Change posture
- Change guardrails
- Verification policy
- Default project commands
- Project constraints
- Approval boundary
- Communication tone

## Shared contract schema

These fields must stay synchronized across all harness files:

- `communication_language`
- `project_type`
- `definition_of_done`
- `change_posture`
- `change_guardrails`
- `verification_policy`
- `approval_policy`
- `project_commands`
- `project_constraints`
- `communication_tone`
- `stack_summary`
- `environment`

`PROJECT_HARNESS.md` and `harness-state.json` are the canonical sources. Entry files reflect only a summary of these fields.

## Entry file principles

- Keep `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` thin.
- Detailed operating rules live in this document and `harness-state.json`.
- Entry files contain pointers and summary rules only — no duplicated policy detail.
- All three entry files reflect the same contract as synchronized projections.

## Audit and synchronization

- Before and after each harness run, check that all five managed files exist and agree on core contract fields.
- If canonical fields disagree across files, classify as `repair` and synchronize.
- When confirmed durable defaults change, update this document and `harness-state.json` together.
- If any entry file diverges on a core contract point, treat it as entry-file sync drift and repair.

Minimum conditions for `repair`:
- A managed file is missing
- Shared contract schema fields disagree across canonical sources
- Entry files diverge on core contract summary
- An entry file has grown too thick
- A state invariant is broken

## Coexistence principles

- Separate the role of this harness from global plugins, skills, and MCP configuration.
- This harness manages only the project-local operating contract. It does not replace global execution frameworks.
- Do not overwrite existing user content or global plugin pointers in `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`.
- Do not force a specific global skill, MCP server, model, or orchestration style as a permanent project default.
- Framework tactics (parallel work, ralph loops, review loops, subagent strategies) are not harness interview items.
- If a global rule and a local contract conflict, surface the conflict — do not silently delete or ignore either side.

## Pre-completion checklist

- All five harness files exist?
- `harness-state.json` durable defaults match this document?
- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` are thin entry files?
- All three entry files reflect the same core contract?
- Default build/run/test commands are confirmed or explicitly marked as unknown?
- Changes recorded in the change history?
- If `configured`: `pending_fields` is empty and `sync_status` is `healthy`?

## Task interpretation

- Interpret each user request dynamically as `bugfix`, `feature`, `maintenance`, or `refactor`.
- Do not store those work types as harness defaults.
- Keep project operating principles separate from per-request task type.
- Do not treat app name, package structure, or deployment target as required interview fields — infer from the repository when needed.

## Update principles

- This template starts small.
- The harness does not need to be complete in one pass.
- When the user requests a policy change during operation, update this document and `harness-state.json` together.

## Change history

| Date | Change | Target | Reason |
|------|--------|--------|--------|
| YYYY-MM-DD | Initial harness setup or most recent update | Relevant files or policy | One-line explanation |
