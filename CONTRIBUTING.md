# Contributing to make-harness

Thanks for contributing.

`make-harness` is intentionally narrow. Please keep changes aligned with the core philosophy:

- it is a project-local contract layer
- it is not an execution framework
- entry files should stay thin
- durable defaults and volatile runtime state should stay separate
- framework-specific orchestration tactics should not become permanent harness defaults

## Good contributions

Examples of strong contributions:

- clearer durable/volatile contract boundaries
- stronger fixture coverage for bootstrap / refresh / repair
- better local audit or validation logic
- smaller, clearer templates
- improved examples that show contract-layer behavior
- documentation that reduces ambiguity without expanding scope

## Changes to avoid by default

Please avoid turning `make-harness` into:

- a plugin installer
- an MCP manager
- a subagent orchestration system
- a full coding framework
- a repo-specific execution workflow engine

Those may be useful tools, but they belong next to this project, not inside its core contract model.

## Development workflow

1. Make the smallest change that improves correctness or clarity.
2. If behavior changes, add or update tests first when practical.
3. Run the verification commands before opening a PR.

```bash
python3 -m pytest -q
python3 tools/validate-fixtures.py
python3 tools/audit-harness.py /path/to/sample-project
```

## Scope rule

When in doubt, prefer:

- better contract structure over more features
- better validation over more prompts
- clearer examples over broader automation

That bias keeps the project calm and composable.
