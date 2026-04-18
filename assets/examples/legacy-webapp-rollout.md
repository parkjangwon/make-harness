# Legacy Web App Rollout Example

This example is intentionally concrete: a team had drift across `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`, kept repeating the same setup rules in chat, and wanted one local source of truth without adopting a bigger agent runtime.

## Before

Repository symptoms:

- `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` drifted apart
- project rules were being restated manually in chat
- legacy constraints existed but were scattered across old docs and tribal knowledge
- reviewers were not sure which root file actually represented the current default

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

### After

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
