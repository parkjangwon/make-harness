# Coexistence

`make-harness` is designed to work with stronger agent frameworks, plugins, and specialist skills.

It is a contract layer, not an execution layer.
It does not replace stronger workflow or methodology frameworks. Tools like superpowers can own planning, TDD, code review loops, or sub-agent coordination above this layer while `make-harness` continues to own only the repository-local contract.

## A practical multi-agent split

In a multi-agent setup, a healthy boundary usually looks like this:

- planner: decomposes the task, decides the order of work, and chooses when review is needed
- generator / executor: produces code, UI, docs, migrations, or other repository artifacts
- evaluator / reviewer: checks the generated result against explicit criteria instead of relying only on the generator's self-evaluation
- `make-harness`: preserves the shared local contract all of those agents should read before acting

That contract can include:

- definition of done
- verification defaults
- project commands for test / lint / typecheck / e2e / visual review
- approval boundaries
- project constraints
- short repository-local rubric hints for what counts as acceptable quality

## Why this boundary matters

The main value of `make-harness` in a stronger workflow stack is not that it creates the agent loop.
The value is that it gives every agent in the loop the same repository-local expectations.

This is especially useful when:

- the planner and executor are different tools
- a reviewer should evaluate the work independently
- the repository has UI, security, or rollout-specific quality criteria that should survive across sessions

In other words, `make-harness` can preserve the evaluation criteria without trying to become the evaluator runtime.

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

It also does not:

- decide how many planner / generator / evaluator passes a workflow should run
- permanently encode agent topology as harness state
- turn Playwright, MCP, or screenshot review into mandatory built-in runtime behavior
