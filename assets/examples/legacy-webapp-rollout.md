# Legacy Web App Rollout Example

This example shows how `make-harness` should feel when applied to an existing repository without pretending to be a heavy execution framework.

## Starting point

Repository symptoms:

- `AGENTS.md` and `CLAUDE.md` drifted apart
- project rules were being restated manually in chat
- legacy constraints existed but were scattered across old docs and tribal knowledge
- the team did not want to adopt a bigger agent framework just to record those defaults

## What make-harness adds

1. Inspect the repository and existing root files.
2. Infer likely context from manifests, docs, and directory layout.
3. Confirm only durable project defaults that inspection cannot settle alone.
4. Write:
   - thin entry files
   - one human-readable durable contract
   - one machine-readable durable contract
   - one volatile runtime state file

## Example outcome

Durable defaults captured once:

- collaboration language: Korean
- project type: legacy
- change posture: conservative
- verification policy: required
- approval boundary: dependencies, schema changes, production config

Runtime state kept separate:

- current run mode
- interview progress
- detected language signal
- sync status

## What did not change

`make-harness` did not:

- install plugins
- pick an orchestration framework
- create agent teams
- force a repo-specific execution engine

That boundary is the point. The repo gained a durable contract layer, not a heavier runtime stack.

## Why this example matters

A good rollout should make the repository feel calmer, not more magical.

Success looks like:

- less repeated setup chatter
- fewer drifted root files
- stable local defaults across repeated sessions
- no confusion about which file is durable vs runtime-only
