---
name: make-harness
description: Use when the user wants to set up, install, audit, update, repair, or sync a project-local AI harness for the current repository. Inspect the repo, run a short interview for durable defaults and execution guardrails, then create or update synchronized AGENTS.md, CLAUDE.md, GEMINI.md, PROJECT_HARNESS.md, harness-contract.json, and harness-runtime.json files.
---

# make-harness

Use this skill when the user wants to set up, audit, update, or repair a project-local harness in the current repository.

This skill is the bootstrapper and maintenance entrypoint. The actual project contract must live in the target project's local files, not in the skill itself.

## What this skill manages

Create, update, or repair these project-local files:

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `PROJECT_HARNESS.md`
- `harness-contract.json`
- `harness-runtime.json`

Template sources live in [assets/templates](assets/templates).

## Core behavior

1. Inspect the current repository and any existing harness files first.
2. Treat `/make-harness` as a single entry command: `bootstrap` when no harness exists, `update` when a healthy harness already exists, and `repair` when drift or breakage is detected.
3. Keep the durable project contract in `PROJECT_HARNESS.md` and `harness-contract.json`.
4. Keep interview progress, sync metadata, and language-detection hints in `harness-runtime.json` only.
5. If the harness is incomplete or missing durable defaults, start a short interview before treating any defaults as final.
6. Run the interview interactively, one question at a time.
7. Detect likely collaboration language from repo signals first; confirm it when unclear instead of forcing an English-first opener.
8. After each answer, reflect runtime progress into `harness-runtime.json` and durable answers into `harness-contract.json`.
9. Confirm only durable project defaults and execution guardrails.
10. Keep `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` thin. Put the durable contract in `PROJECT_HARNESS.md`, then keep the entry files as pointers and summary rules.
11. Validate that the managed harness files agree on the confirmed contract. If drift is detected, repair it before finishing.
12. Record a concise change history entry whenever the durable project contract changes.
13. Do not store per-request work types such as `bugfix`, `feature`, `maintenance`, or `refactor` as permanent harness state.
14. Do not store framework-level orchestration preferences as permanent harness state.

## Run classification

Read `harness-contract.json` and `harness-runtime.json` if they exist.

- If no harness exists, bootstrap it.
- If the harness exists and is healthy, enter update mode.
- If the harness exists but is drifted or broken, repair first and only continue with update if needed.
- If `bootstrap_status` is `pending_interview`, the harness is not configured yet.
- If `bootstrap_status` is `interview_in_progress`, resume from recorded runtime state.

## Interactive interview flow

- Ask exactly one question at a time.
- This is a one-time setup flow, so precision is more important than minimizing question count.
- For an existing repository, use repo-first interview behavior: inspect and infer first, then confirm only what remains unclear.
- For a blank project, switch to setup-discovery interview behavior: ask only the small set of upfront questions needed to choose stack, runtime, package manager, and core commands.
- Follow the fixed question order from [references/interview-protocol.md](references/interview-protocol.md).
- Prefer confirmation questions over open-ended questions whenever the repository already provides a likely answer.
- Prefer inspecting the repository over asking for metadata that is usually inferable.
- Use detect-first language selection:
  - look for README language, existing root docs, comments, and file naming patterns
  - if one language is strongly implied, start there with a confirmation tone
  - if signals are weak or mixed, ask the language question in plain English
- Respect the interview question budget from the protocol:
  - target 5 or fewer explicit questions for common repos
  - treat 8 as a soft ceiling that requires justification
- Normalize simple user answers into canonical stored values before writing state.
- Use the canonical normalization tables in `references/interview-protocol.md` for `project_type`, `change_posture`, `approval_policy`, `verification_policy`, and `communication_tone`.
- Use the user-facing question templates from `references/interview-protocol.md` instead of exposing internal schema names directly.
- Choose wording from the protocol's three-level template matrix based on confidence (`high`, `medium`, `low`).
- When the interview runs in English, use the protocol's English companion templates rather than ad-hoc translations.
- Adapt per answer, not per person label: switch between precision mode, clarify mode, and safe-default mode based on the user's actual response pattern.
- Keep `pending_fields` and `confirmed_fields` normalized as non-overlapping sets.
- Treat repo-derived guesses as temporary inference until they are confirmed.
- If `bootstrap_status` is `interview_in_progress`, resume from the recorded `interview_step` instead of restarting.
- If a new user answer creates a contradiction with durable state or strong repo signals, confirm before overwriting the contract.
- Only set `bootstrap_status` to `configured` when all required durable defaults are confirmed.

## Output files

After bootstrap, update, or repair, the target project should have:

- a thin `AGENTS.md`
- a thin `CLAUDE.md`
- a thin `GEMINI.md`
- a human-readable `PROJECT_HARNESS.md`
- a machine-readable durable `harness-contract.json`
- a machine-readable volatile `harness-runtime.json`

## Resources

- Templates: [assets/templates](assets/templates)
- Coexistence: [docs/coexistence.md](docs/coexistence.md)
- Interview guide: [references/interview-guide.md](references/interview-guide.md)
- Interview protocol: [references/interview-protocol.md](references/interview-protocol.md)
- Repair and validation guide: [references/repair-validation-guide.md](references/repair-validation-guide.md)
- Validation fixtures: [assets/fixtures](assets/fixtures)
- Interview planner: [tools/interview_planner.py](tools/interview_planner.py) — deterministic helper that pins blank-project discovery, repo-first confirmation, resume order, and answer-mode adaptation in tests and fixtures
- Repair playbook: [assets/repair-playbook.md](assets/repair-playbook.md)
- Healthy checklist: [assets/healthy-checklist.md](assets/healthy-checklist.md)
- Sample output: [assets/examples](assets/examples)
- Local audit tool: [tools/audit-harness.py](tools/audit-harness.py) — checks managed files, `PROJECT_HARNESS.md` structure, entry thinness, and runtime invariants
- Positioning: [docs/positioning.md](docs/positioning.md)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Optional UI metadata: [agents/openai.yaml](agents/openai.yaml), [agents/gemini.yaml](agents/gemini.yaml)
