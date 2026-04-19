# Coexistence

`make-harness` is designed to work with stronger agent frameworks, plugins, and specialist skills.

It is a contract layer, not an execution layer.
It does not replace stronger workflow or methodology frameworks. Tools like superpowers can own planning, TDD, code review loops, or sub-agent coordination above this layer while `make-harness` continues to own only the repository-local contract.

## What it does

- fixes project-local durable rules
- records durable defaults
- keeps root entry files aligned
- keeps volatile runtime state separate from durable contract
- makes drift visible and repairable

## What it does not do

- force a coding methodology
- force a plugin, MCP, or sub-agent strategy
- replace orchestration frameworks
- define team architecture by default
- try to be the strongest coding assistant in the stack
