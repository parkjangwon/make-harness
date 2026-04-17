# Coexistence

`make-harness` is designed to work with stronger agent frameworks, plugins, and specialist skills.

It is a contract layer, not an execution layer.

## What it does

- fixes project-local rules
- records durable defaults
- keeps root entry files aligned
- makes drift visible and repairable

## What it does not do

- force a coding methodology
- force a plugin, MCP, or sub-agent strategy
- replace orchestration frameworks
- define team architecture by default
- try to be the strongest coding assistant in the stack

## How it should be used

- let strong frameworks handle execution
- let specialist skills handle domain work
- let `make-harness` hold the local project contract

## Practical rule

If a rule is about **how this project should be handled over time**, it belongs in the harness.

If a rule is about **how an agent should execute a task right now**, it probably belongs in a framework, plugin, or specialist skill.
