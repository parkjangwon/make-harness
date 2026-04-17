# make-harness Positioning

`make-harness` is a lightweight project-local harness starter for AI-assisted development.

Its job is simple:

- bootstrap a durable local project contract
- keep that contract synchronized
- make drift visible and repairable

It does not try to replace strong agent frameworks.
It is meant to stay small enough to compose with them.

## Who this is for

This skill is most useful for people who:

- work on the same repository over time with AI agents
- do not want to restate project rules on every request
- want stable project-local defaults for approval, verification, and change scope
- want `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` to stop drifting apart
- work on legacy repositories where hidden constraints matter

## When to use it

Use `make-harness` when:

- a repository has no local harness yet
- the current harness feels vague, stale, or inconsistent
- root entry files have drifted apart
- a project now has stable operating expectations worth recording
- an AI workflow needs stronger local guardrails without adding a heavy framework

## When not to use it

Do not use `make-harness` when:

- the work is a one-off toy or disposable prototype
- the repository will not be used with AI agents in any durable way
- the user wants orchestration automation more than project-local contracts
- the team expects this skill to install runtime tools, create agent teams, or run a planning framework

## Core value

The value of `make-harness` is not "it creates markdown files."

The value is:

- the project contract becomes explicit
- the contract survives across repeated sessions
- drift becomes visible
- repair has a deterministic flow
- different root entry files stop acting like separate sources of truth

## What it is not

`make-harness` is not:

- a coding super-plugin
- an orchestration framework
- a sub-agent team generator by default
- a replacement for strong specialist skills
- a rule system for forcing one preferred development style

## What makes it credible

This skill is intentionally narrow.

It now has:

- a fixed shared contract schema
- thin-entry-file rules
- fixture cases for `bootstrap`, `refresh`, and `repair`
- a deterministic repair playbook
- a healthy checklist
- sample healthy outputs and before/after examples

That combination makes it more trustworthy than a generic template generator.

## Practical promise

The practical promise of `make-harness` is modest but useful:

- it helps a repository stay locally consistent
- it gives AI agents clearer boundaries
- it reduces repeated setup chatter
- it makes project-specific constraints easier to preserve

It should feel calm, predictable, and easy to maintain.

## Coexistence

It works best next to stronger tools:

- frameworks handle execution
- specialist skills handle domain work
- `make-harness` holds the local project contract

## Short positioning line

`make-harness` is a calm, project-local contract layer for AI-assisted development.
