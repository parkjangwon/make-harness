# Interview Guide

Use this guide when running the `make-harness` interview.

For the full executable rules, question order, normalization tables, resume behavior, contradiction handling, question budget, and user-facing question templates, read the [interview protocol](interview-protocol.md) first.

The protocol now includes:

- existing-repo and blank-project question sets
- a three-level template matrix for high / medium / low confidence wording
- English companion templates for multilingual collaboration contexts
- adaptive response modes such as precision mode, clarify mode, and safe-default mode
- deterministic planner inputs that can be pinned in fixtures via `tools/interview_planner.py`
- minimal security interview items for project-local security guardrails such as sensitive areas, secret-handling prohibitions, configuration-based TLS exception rules, and security verification commands

## Interview style

- ask one question at a time
- use plain, everyday language
- avoid jargon when a simpler phrase works
- prefer short answer shapes that are easy to normalize
- inspect the repository first, then ask only what is still unclear
- use a repo-first strategy for an existing repository: infer first, then confirm
- use a blank project strategy when there is no code yet: ask only the setup-defining questions needed to choose stack, runtime, and package manager
- support both senior and junior developers: do not assume the user already knows every architectural choice
- when a choice may feel hard, offer a safe default first instead of forcing an immediate decision
- prefer two-step questioning for harder topics: start with an easy default-offer question, then ask a more specific follow-up only if needed
- detect likely collaboration language from repo signals first
- if signals are weak or mixed, ask the language question in plain English
- switch immediately to the confirmed language after the language answer is stored
- prefer confirmation questions over open-ended questions when repo confidence is high
- treat repo-derived guesses as temporary inference until confirmed
- if the interview must resume, continue from the recorded `interview_step`
- if a new answer creates a contradiction with durable state, explain the conflict briefly and confirm before overwriting
- ask only for repository-local defaults, guardrails, commands, and constraints
- do not ask the user to choose a general development philosophy, methodology, branch strategy, code review loop, brainstorming process, or sub-agent workflow as durable harness state
