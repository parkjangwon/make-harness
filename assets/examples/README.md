# Harness Examples

These examples show what a healthy harness can look like after bootstrap, update, or repair.

They are not templates to copy verbatim.
They are reference outputs that make the contract shape easier to understand.
They should be read as examples of local project rules, not workflow prescriptions.

## How to use them

- Compare the example against the shared contract schema.
- Check that entry files stay thin.
- Check that canonical sources carry the real contract.
- Use examples to judge whether a generated harness feels simple, stable, and consistent as a local project rule layer.
- Treat evaluator and reviewer references as contract examples for repository-local quality criteria, not workflow prescriptions or a fixed agent topology.

## Example set

- `legacy-webapp-healthy.md`: a representative healthy harness for a legacy web application
- `legacy-webapp-before-after.md`: a before/after showing why the contract/runtime split matters
- `legacy-webapp-rollout.md`: an end-to-end adoption example for an existing repository, including planner / generator / evaluator handoff without turning the harness into an orchestration engine
- `mock-interview-junior-developer.md`: a safe-default setup transcript showing low-pressure guidance without turning the harness into a personality classifier
- `mock-interview-senior-developer.md`: a precision-mode setup transcript showing explicit overrides without changing the core harness model
- `social-preview.png`: a ready-to-upload GitHub social preview image for this repository
