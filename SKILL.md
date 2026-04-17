---
name: make-harness
description: Use when the user wants to set up, install, audit, refresh, repair, or sync a project-local AI harness for the current repository. Inspect the repo, run a short interview for durable defaults and execution guardrails, then create or update synchronized AGENTS.md, CLAUDE.md, GEMINI.md, PROJECT_HARNESS.md, and harness-state.json files.
---

# make-harness

Use this skill when the user wants to set up, audit, refresh, or repair a project-local harness in the current repository.

This skill is the bootstrapper and maintenance entrypoint. The actual project contract must live in the target project's local files, not in the skill itself.

## What this skill manages

Create, refresh, or repair these project-local files:

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `PROJECT_HARNESS.md`
- `harness-state.json`

Template sources live in [assets/templates](assets/templates).

## Core behavior

1. Inspect the current repository and any existing harness files first.
2. Classify the run as `bootstrap`, `refresh`, or `repair` before editing files.
3. If the harness is incomplete or missing durable defaults, start a short interview before treating any defaults as final.
4. Run the interview interactively, one question at a time.
5. After each answer, reflect it into the local harness state before asking the next question.
6. Confirm only durable project defaults and execution guardrails:
   - communication language
   - project type (`greenfield` or `legacy`)
   - change posture
   - definition of done
   - change guardrails
   - verification policy
   - approval boundary
   - default project commands
   - project constraints not obvious from the repo
   - communication tone
   - inferred stack summary
   - environment constraints not visible in the repo
   - treat those fields as the fixed shared contract schema for synchronization and repair
7. Keep `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` thin. Put the durable contract in `PROJECT_HARNESS.md`, then keep the entry files as pointers and summary rules.
8. Validate that the managed harness files agree on the confirmed contract. If drift is detected, repair it before finishing.
9. Record a concise change history entry whenever the durable project contract changes.
10. Do not store per-request work types such as `bugfix`, `feature`, `maintenance`, or `refactor` as permanent harness state.
11. Do not store framework-level orchestration preferences such as parallel work, subagent loops, or review-loop tactics as permanent harness state.
12. Treat `PROJECT_HARNESS.md` and `harness-state.json` as canonical sources, and treat `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` as synchronized thin projections of the same contract.

## File policy

- If `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md` does not exist, create it from the template.
- If any of those files already exists, treat it as user-owned.
- Prefer inserting or updating a harness-managed block instead of rewriting the whole file.

## Run classification

Read `harness-state.json` if it exists.

- If all harness files are missing, treat the run as `bootstrap`.
- If the harness exists and the durable contract is still valid, treat the run as `refresh`.
- If one or more harness files are missing, stale, or inconsistent with the current contract, treat the run as `repair`.
- If the entry files diverge from each other on core contract points, treat the run as `repair` even when all files exist.
- If `bootstrap_status` is `pending_interview`, the harness is not configured yet.
- If `bootstrap_status` is `interview_in_progress`, resume from the recorded interview state.
- In either state, inspect first and interview before normalizing files or assuming defaults.

## Interactive interview flow

- Ask exactly one question at a time.
- Ask the first question in English unless the saved harness state already confirms a different communication language.
- After the user confirms the collaboration language, use that language for every subsequent question and response without exception. Use English only for technical terms that have no natural equivalent in the confirmed language.
- Do not send the full question list in one message.
- Use plain, easy language in user-facing questions.
- Avoid jargon when a simpler phrase can get the same answer.
- Prefer confirmation questions over open-ended questions whenever the repository already provides a likely answer.
- Prefer inspecting the repository over asking for metadata that is usually inferable, such as app name, package layout, or entrypoints.
- Ask about app name, package structure, or similar identifiers only when that ambiguity blocks a reliable project contract.
- Normalize simple user answers into canonical stored values before writing state.
- After each answer:
  - update `bootstrap_status` to `interview_in_progress` if it is still pending
  - update `interview_step`
  - remove the answered field from `pending_fields`
  - add it to `confirmed_fields`
  - persist any confirmed value into the appropriate field
  - if the answered field is `communication_language`, use that language for all following interview questions
- Keep `pending_fields` and `confirmed_fields` normalized as non-overlapping sets.
- Only set `bootstrap_status` to `configured` when all required durable defaults are confirmed.

## Required interview

Ask only the smallest useful set of questions after inspection, in sequence:

- Which language should we use? Example answer: `Korean`.
- Is this a new project or an existing project? Example answer: `existing project`.
- How short should replies be? Example answer: `short`.
- What does done look like for this project? Example answer: `code works and passes checks` or `code works, no checks required`.
- Should changes be careful, balanced, or bold by default? Example answer: `careful`.
- What should the agent avoid changing unless you say yes? Example answer: `dependencies, database schema, production config`.
- Should we run tests and linting by default? Example answer: `always run them`, `run them when possible`, or `skip unless asked`.
- Which commands should count as this project's default commands? Example answer: `test is pnpm test, lint is pnpm lint`.
- Are there important project rules not obvious from the repo? Example answer: `keep API responses backward compatible`.
- Is this stack summary right? Example answer: `yes` or a short correction.
- Are there environment limits or setup rules not obvious from the repo? Example answer: `local only, no Docker`.

## Output files

After bootstrap, refresh, or repair, the target project should have:

- a thin `AGENTS.md`
- a thin `CLAUDE.md`
- a thin `GEMINI.md`
- a human-readable `PROJECT_HARNESS.md`
- a machine-readable `harness-state.json`
- synchronized durable defaults and execution guardrails across all managed harness files

## Resources

- Templates: [assets/templates](assets/templates)
- Coexistence: [docs/coexistence.md](docs/coexistence.md)
- Interview guide: [references/interview-guide.md](references/interview-guide.md)
- Repair and validation guide: [references/repair-validation-guide.md](references/repair-validation-guide.md)
- Validation fixtures: [assets/fixtures](assets/fixtures)
- Repair playbook: [assets/repair-playbook.md](assets/repair-playbook.md)
- Healthy checklist: [assets/healthy-checklist.md](assets/healthy-checklist.md)
- Sample output: [assets/examples](assets/examples)
- Positioning: [docs/positioning.md](docs/positioning.md)
- Optional UI metadata: [agents/openai.yaml](agents/openai.yaml), [agents/gemini.yaml](agents/gemini.yaml)
