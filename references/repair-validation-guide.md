# Repair and Validation Guide

Use this guide when the harness is classified as `repair`, or when final validation is needed.

## Repair triggers

Treat the run as `repair` when:

- a managed file is missing
- a shared contract field disagrees across canonical sources
- an entry file disagrees with the shared contract
- an entry file is no longer thin
- a state invariant is broken

## State invariants

- `configured` implies `pending_fields` is empty
- `configured` implies `interview_step` is `complete`
- `pending_fields` and `confirmed_fields` do not overlap
- `validated_shared_fields` only contains shared contract fields
- `last_validated_at` must not coexist with `sync_status: unknown` or `unvalidated`

## Deterministic repair order

1. Normalize `harness-state.json`
2. Repair `PROJECT_HARNESS.md`
3. Re-project `AGENTS.md`
4. Re-project `CLAUDE.md`
5. Re-project `GEMINI.md`
6. Validate shared contract fields and sync metadata

Canonical sources stay authoritative during repair.
Do not infer the contract from a drifted entry file.

## Final validation

Before claiming the harness is healthy:

- confirm that all managed files exist
- confirm that canonical sources agree on the shared contract schema
- confirm that entry files are thin and aligned
- update `validated_shared_fields`
- update `drift_reasons`
- update sync metadata

Use [assets/healthy-checklist.md](../assets/healthy-checklist.md) as the final healthy gate.
