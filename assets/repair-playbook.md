# Repair Playbook

This playbook defines the minimum deterministic repair flow for `make-harness`.

## Repair goal

Return the harness to a simple healthy state where:

- all managed files exist
- canonical durable sources agree on the shared contract schema
- entry files are thin synchronized projections
- runtime invariants hold
- sync metadata is explicit and internally consistent

## Canonical order

Always repair in this order:

1. `harness-contract.json`
2. `harness-runtime.json`
3. `PROJECT_HARNESS.md`
4. `AGENTS.md`
5. `CLAUDE.md`
6. `GEMINI.md`

The first three files define authority.
The last three files are projections.

## Minimum repair steps

### 1. Identify drift reasons

Collect only concrete reasons:

- `missing_managed_file`
- `canonical_contract_mismatch`
- `entry_file_contract_mismatch`
- `entry_file_not_thin`
- `runtime_invariant_broken`

### 2. Normalize durable machine contract

Repair `harness-contract.json` first.

### 3. Normalize volatile runtime state

Repair `harness-runtime.json` so runtime invariants hold and sync metadata is explicit.

### 4. Repair canonical human contract

Repair `PROJECT_HARNESS.md` so it matches the normalized shared contract fields from `harness-contract.json`.

### 5. Re-project entry files

Rebuild `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` as thin projections of the repaired canonical contract.
