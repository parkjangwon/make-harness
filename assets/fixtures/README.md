# Harness Fixtures

These fixtures are small contract-level validation cases for `make-harness`.

They are intentionally simple. The goal is not to simulate a full runtime, but to pin down the minimum cases that should stay stable as the skill evolves.

## What these fixtures validate

- run classification: `bootstrap`, `refresh`, `repair`
- fixed shared contract schema
- entry-file synchronization expectations
- invariant handling
- deterministic drift reasons

## Fixture files

- `fixture.json`: scenario description, expected classification, and behavioral checks
- `expected-state.json`: minimum machine-readable state snapshot the harness should converge to for that scenario

## How to use them

- Read a fixture's `fixture.json`.
- Compare the resulting harness state against `expected-state.json`.
- Compare the current skill behavior against the fixture's expected classification and checks.
- If the skill changes, update fixtures only when the contract intentionally changes.
- If the contract did not intentionally change, the fixture should still hold.

## Fixture philosophy

- Keep fixtures small and readable.
- Prefer explicit expected outcomes over long prose.
- Cover the core trust cases before edge cases.
- Treat these fixtures as a stability harness for the harness itself.
