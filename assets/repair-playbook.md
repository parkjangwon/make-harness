# Repair Playbook

This playbook defines the minimum deterministic repair flow for `make-harness`.

Use it when a harness run is classified as `repair`.

## Repair goal

Return the harness to a simple healthy state where:

- all managed files exist
- canonical sources agree on the shared contract schema
- entry files are thin synchronized projections
- state invariants hold
- sync metadata is explicit and internally consistent

## Canonical order

Always repair in this order:

1. `harness-state.json`
2. `PROJECT_HARNESS.md`
3. `AGENTS.md`
4. `CLAUDE.md`
5. `GEMINI.md`

The first two files are canonical sources.
The last three files are projections.

Do not repair projections first and then guess the canonical contract from them.

## Minimum repair steps

### 1. Identify drift reasons

Collect only concrete reasons:

- `missing_managed_file`
- `canonical_contract_mismatch`
- `entry_file_contract_mismatch`
- `entry_file_not_thin`
- `state_invariant_broken`

Record the detected reasons before synchronization.

### 2. Normalize machine state

Repair `harness-state.json` first.

Minimum checks:

- `pending_fields` and `confirmed_fields` do not overlap
- `configured` implies `pending_fields` is empty
- `configured` implies `interview_step` is `complete`
- `validated_shared_fields` only contains shared contract fields
- `sync_status` is not left as `unknown` or `unvalidated` after successful validation

### 3. Repair canonical human contract

Repair `PROJECT_HARNESS.md` so it matches the normalized shared contract fields from `harness-state.json`.

Do not add new shared fields during repair unless the contract itself intentionally changed.

### 4. Re-project entry files

Rebuild `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` as thin projections of the repaired canonical contract.

Minimum checks:

- each file points back to `PROJECT_HARNESS.md`
- each file stays thin
- each file reflects the same shared contract summary
- tool-specific wording may differ slightly, but contract meaning must not differ

### 5. Validate final state

A repaired harness should end with:

- `sync_status: healthy`
- `entry_files_sync.status: healthy`
- `pending_fields: []` when configured
- `interview_step: complete` when configured
- `validated_shared_fields` filled with the shared contract fields that were checked

## Fail-closed rule

If the shared contract is still ambiguous after inspection, do not silently finalize as healthy.

Either:

- keep the harness in an interview-required state
- or report the unresolved drift clearly

## Repair output expectations

When repair succeeds, summarize:

- what drift was found
- which file was treated as canonical
- what was synchronized
- whether the harness is now healthy
