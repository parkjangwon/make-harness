# make-harness Positioning

`make-harness` is a lightweight project-local harness starter for AI-assisted development.

Its job is simple:

- bootstrap a durable local project contract
- keep that contract synchronized
- keep volatile runtime state separate
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

## Core value

The value of `make-harness` is not that it creates markdown files.

The value is:

- the project contract becomes explicit
- the contract survives across repeated sessions
- volatile runtime state stops polluting the durable contract
- drift becomes visible
- repair has a small deterministic flow
- different root entry files stop acting like separate sources of truth

## What makes it credible

This skill is intentionally narrow.
It now has:

- a fixed shared contract schema
- a durable/volatile file split
- thin-entry-file rules
- fixture cases for `bootstrap`, `update`, and `repair`
- a deterministic repair playbook
- a healthy checklist
- a lightweight local audit script

## Short positioning line

`make-harness` is a calm, project-local contract layer for AI-assisted development.`
