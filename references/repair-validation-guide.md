# Repair and Validation Guide

Use this guide when the harness is classified as `repair`, or when final validation is needed.

## Repair triggers

Treat the run as `repair` when:

- a managed file is missing
- a shared contract field disagrees across canonical durable sources
- an entry file disagrees with the shared contract
- an entry file is no longer thin
- a runtime invariant is broken

## State invariants

- `configured` implies `pending_fields` is empty
- `configured` implies `interview_step` is `complete`
- `pending_fields` and `confirmed_fields` do not overlap
- `validated_shared_fields` only contains shared contract fields
- `last_validated_at` must not coexist with `sync_status: unknown` or `unvalidated`

## Deterministic repair order

1. Normalize `harness-contract.json`
2. Normalize `harness-runtime.json`
3. Repair `PROJECT_HARNESS.md`
4. Re-project `AGENTS.md`
5. Re-project `CLAUDE.md`
6. Re-project `GEMINI.md`
7. Validate shared contract fields, sync metadata, and deterministic interview-plan expectations for interview-heavy fixtures
