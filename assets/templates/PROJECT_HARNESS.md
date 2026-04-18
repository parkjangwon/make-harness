# make-harness Project Harness

## Status

- This document is the bootstrap template, not a completed project contract.
- Durable contract lives in `PROJECT_HARNESS.md` and `harness-contract.json`.
- Runtime interview/audit state lives in `harness-runtime.json`.
- Treat `/make-harness` as a single entry command: bootstrap when no harness exists, update when a healthy harness exists, and repair when drift or breakage is detected first.

## Canonical model

- `PROJECT_HARNESS.md`: human-readable durable contract
- `harness-contract.json`: machine-readable durable contract
- `harness-runtime.json`: volatile interview, audit, and sync state
- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`: thin projections only

## Agent defaults

- Inspect the repository before asking for metadata that can be inferred.
- Confirm durable project defaults and execution guardrails only.
- Do not store framework-level tactics as permanent harness state.
- Use detect-first language selection: infer likely collaboration language from repo signals, then confirm if needed.
- Ask one interview question at a time and reflect runtime progress into `harness-runtime.json`.

## Durable contract fields

These fields must stay synchronized across `PROJECT_HARNESS.md` and `harness-contract.json`:

- `communication_language`
- `project_type`
- `definition_of_done`
- `change_posture`
- `change_guardrails`
- `verification_policy`
- `approval_policy`
- `project_commands`
- `project_constraints`
- `rule_strengths`
- `communication_tone`
- `stack_summary`
- `environment`

`rule_strengths` is the minimal enforcement map for the durable contract:

- `advisory`: remember and prefer this rule, but do not treat it as a hard gate
- `guided`: use this as the default path and call out exceptions explicitly
- `enforced`: do not treat the work as complete unless the rule is satisfied or explicitly overridden

## Runtime state fields

`harness-runtime.json` tracks only volatile state such as:

- `run_mode`
- `bootstrap_status`
- `interview_step`
- `pending_fields`
- `confirmed_fields`
- `validated_shared_fields`
- `drift_reasons`
- `sync_status`
- `entry_files_sync`
- `language_detection`
- audit timestamps

## State invariants

- `configured` implies `pending_fields` is empty.
- `configured` implies `interview_step` is `complete`.
- `pending_fields` and `confirmed_fields` must not overlap.
- `validated_shared_fields` may contain only shared contract fields.
- `last_validated_at` requires an explicit `sync_status` of `healthy` or `drifted`.

## Entry file principles

- Keep entry files short enough to stay obviously non-canonical.
- Entry files point back to the canonical durable contract.
- Entry files may mention runtime-state recovery, but must not duplicate the full policy block.

## Repair order

1. `harness-contract.json`
2. `harness-runtime.json`
3. `PROJECT_HARNESS.md`
4. `AGENTS.md`
5. `CLAUDE.md`
6. `GEMINI.md`

Repair durable contract first, then volatile runtime state, then projections.

## Pre-completion checklist

- All managed files exist.
- `PROJECT_HARNESS.md` and `harness-contract.json` agree on shared contract fields.
- `harness-runtime.json` invariants hold.
- Entry files are thin and aligned.
- `validated_shared_fields` matches what was actually checked.
- Change history is updated when durable defaults change.

## Change history

| Date | Change | Target | Reason |
|------|--------|--------|--------|
| YYYY-MM-DD | Initial harness setup or most recent update | Relevant files or policy | One-line explanation |
