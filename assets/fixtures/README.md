# Fixtures

Fixtures model three things separately:

- repository conditions in `fixture.json`
- expected durable contract effects (when needed) in `expected-contract.json`
- expected volatile runtime state in `expected-runtime.json`

Current fixture coverage includes:

- empty bootstrap
- blank-project stack discovery bootstrap
- detect-first language bootstrap
- conflicting-signals bootstrap
- interrupted interview resume
- healthy refresh
- entry-file drift repair
- missing managed file repair
- broken runtime invariant repair

For interview-heavy scenarios, `fixture.json` can now pin deterministic planner expectations such as:

- `interview_mode`
- `next_question_field`
- `next_question_style`
- `discovery_fields`
- `skip_fields`

`python tools/validate-fixtures.py` cross-checks those expectations against `tools/interview_planner.py`, so repo-first vs setup-discovery behavior is mechanically enforced instead of remaining prose-only.

The goal is not to simulate every repository, but to keep the contract model, interview branching, and repair rules concrete enough to audit.
