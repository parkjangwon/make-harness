# make-harness

<img width="1000" height="550" alt="make-harness" src="https://github.com/user-attachments/assets/e68f3bdd-d549-4158-9f17-5a3111f3c850" />

`make-harness` installs and maintains a project-local harness for each repository.

It is a durable contract bootstrap + maintenance tool: it captures repository-local rules, commands, constraints, and guardrails in one canonical contract, regenerates thin `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` projections from that contract, and checks whether the harness is still healthy.

`make-harness` is not a development methodology, not an execution framework, and not an orchestration layer. It is a framework-agnostic local rule layer that stays small enough to compose with stronger workflow systems.

Korean version: [README.ko.md](README.ko.md)

## Why teams install this

Typical pain before `make-harness`:

### Before

- `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` slowly diverge
- the same project rules get re-explained in every new AI session
- nobody is sure which file is authoritative anymore
- risky changes depend on tribal knowledge instead of an explicit local contract

### After

- one durable contract becomes the source of truth
- thin entry files are regenerated instead of hand-maintained
- audit and completion checks tell you whether the harness is actually healthy
- repo-specific defaults survive across sessions without adopting a bigger agent runtime

In practice, the first win is simple: less repeated setup chatter and fewer drifted root files.

## Who this is for

`make-harness` is for developers and teams who:

- use more than one AI coding tool on the same repository
- keep re-explaining repo rules, commands, and guardrails to new AI sessions
- want one local source of truth instead of hand-maintaining multiple root instruction files

Common examples include teams mixing Claude Code, Codex, Gemini CLI, Cursor, or other agentic coding workflows.

## What happens when you run `/make-harness`

Typical flow:

```text
You: /make-harness

Agent:
1. inspect the repository and any existing harness files
2. infer what it can from repo signals first
3. ask only the missing durable questions
4. generate or repair the harness files
5. report whether the harness is healthy
```

Result:

- `PROJECT_HARNESS.md` becomes the human-readable contract
- `harness-contract.json` stores the machine-readable durable contract
- `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` stay aligned as thin projections
- audit and completion checks can verify whether the harness is still in a healthy state

## Install with skills.sh

```bash
npx skills add parkjangwon/make-harness
```

Install to a specific agent:

```bash
npx skills add parkjangwon/make-harness -a claude-code
npx skills add parkjangwon/make-harness -a codex
npx skills add parkjangwon/make-harness -a gemini-cli
```

List what the repository exposes before installing:

```bash
npx skills add parkjangwon/make-harness --list
```

Managed files:

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `PROJECT_HARNESS.md`
- `harness-contract.json`
- `harness-runtime.json`

## Core

- `PROJECT_HARNESS.md` + `harness-contract.json` are the canonical durable contract
- `harness-runtime.json` is volatile runtime state only
- `AGENTS.md` + `CLAUDE.md` + `GEMINI.md` are thin projections
- only durable defaults and guardrails belong in the durable contract
- drift should be visible and repairable
- this skill should stay easy to compose with stronger frameworks and specialist skills
- project-local security guardrails belong in the contract, and the repo ships only a lightweight path-based guardrail smoke check

## Shared contract fields

- `communication_language`
- `project_type`
- `definition_of_done`
- `change_posture`
- `change_guardrails`
- `verification_policy`
- `approval_policy`
- `project_commands`
- `project_constraints`
- `rule_strengths`
- `communication_tone`
- `stack_summary`
- `environment`

`rule_strengths` is the minimal enforcement layer for the contract. Use it to say whether a durable rule is advisory, guided, or enforced without turning the harness into a heavy execution framework.

## Boundary fields: keep them local, not methodological

Some fields can look broader than they really are. In `make-harness`, they must stay narrowly project-local:

- `definition_of_done` = the repository's default completion expectation or local completion gate, not a universal development philosophy
- `verification_policy` = the repository's default verification rule, not a statement about how all development should be done
- `approval_policy` = the repository's confirmation rule for risky or sensitive changes, not a full team workflow policy
- `change_posture` = a narrow local default for change scope and risk tolerance in this repository, not a general engineering philosophy

If a rule is really about planning, TDD, branch strategy, code review loops, brainstorming, or sub-agent coordination, it belongs in a stronger workflow layer above `make-harness`, not in the durable harness contract.

## Modes


- `bootstrap`: no harness yet
- `update`: healthy harness -> update from the same `/make-harness` command
- `repair`: missing files, contract drift, or invariant failure

## Interview

The skill inspects the repository first, then runs a short interview — one question at a time. It should detect likely collaboration language from repo signals first, then confirm when unclear. Where the repository already gives a clear answer, it asks for confirmation instead of asking open-ended.

The interview is intentionally bounded:

- this is a one-time setup, so precision matters more than blindly minimizing question count
- existing repositories use repo-first gap-filling rather than broad setup questions
- blank projects use a small upfront setup-discovery interview because there is no code to inspect
- fixed question order for durable defaults
- detect-first branching based on repo confidence
- question budget targeting 5 or fewer explicit questions for common repos, while allowing denser blank-project discovery when needed
- canonical normalization for free-form answers like change posture, approval policy, and verification policy
- explicit resume and contradiction rules when `harness-runtime.json` shows an interrupted setup
- minimal security interview items for security-sensitive areas, forbidden secret/debug patterns, configuration-based TLS exception rules, and security verification commands

Details: [references/interview-guide.md](references/interview-guide.md), [references/interview-protocol.md](references/interview-protocol.md)

## Durable vs volatile files

### `harness-contract.json`

Commit this file. It stores the durable machine-readable project contract.

### `harness-runtime.json`

Do not treat this as canonical durable state. It stores interview progress, sync metadata, language detection hints, and audit timestamps.

For shared repositories, consider adding `harness-runtime.json` to `.gitignore`. A starter template is at [assets/templates/.gitignore-harness](assets/templates/.gitignore-harness).

## Healthy means

- all managed files exist
- canonical durable sources agree on the shared contract schema
- entry files are thin and reflect the same contract summary
- runtime invariants hold
- sync metadata is healthy

Details: [assets/healthy-checklist.md](assets/healthy-checklist.md)

## Fixture validation

Run to verify all fixture scenarios are structurally valid:

```text
python tools/validate-fixtures.py
```

This validator now also cross-checks interview-heavy fixtures against a deterministic planner in `tools/interview_planner.py`, so blank-project discovery, detect-first confirmation, and resume behavior stay behaviorally pinned rather than living only in prose.

## Lightweight audit

Run to check a repository-local harness layout without invoking an LLM:

```text
python tools/audit-harness.py /path/to/project
```

This verifies the file set, contract/runtime split, required `PROJECT_HARNESS.md` sections, entry-file thinness, and a few critical runtime invariants.

## Deterministic projection generator

Run to materialize `PROJECT_HARNESS.md`, `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` directly from `harness-contract.json` and `harness-runtime.json`:

```text
python tools/apply-harness.py /path/to/project
```

This is the smallest execution layer in the repo: the LLM can decide the durable contract, but projection files no longer need to be handwritten.

## completion gate

Run to decide whether a harness is actually done, not just structurally present:

```text
python tools/check-harness-done.py /path/to/project
```

This gate requires audit success, `configured` + `healthy` runtime state, full `validated_shared_fields`, and zero drift between the checked-in projections and deterministic generator output.

## Structure

```text
make-harness/
├── SKILL.md
├── README.md
├── README.ko.md
├── docs/
│   ├── coexistence.md
│   └── positioning.md
├── agents/
│   ├── openai.yaml
│   └── gemini.yaml
├── tools/
│   ├── apply-harness.py
│   ├── audit-harness.py
│   ├── check-harness-done.py
│   ├── check-sensitive-change.py
│   ├── interview_planner.py
│   └── validate-fixtures.py
└── assets/
    ├── templates/
    ├── fixtures/
    ├── examples/
    ├── healthy-checklist.md
    └── repair-playbook.md
```

## lightweight path-based guardrail smoke check

Run to detect whether a diff touches auth / permissions / secrets / payments / encryption / public API areas:

```text
python tools/check-sensitive-change.py /path/to/project --paths src/auth/login.py config/tls-dev.yaml
```

For git-based checks, use refs instead of explicit paths:

```text
python tools/check-sensitive-change.py /path/to/project --base HEAD~1 --head HEAD
```

If the relevant `rule_strengths` are `enforced`, sensitive changes block completion and hooks/CI can fail. If they are only `guided`, the checker reports the category but does not block.

This checker is intentionally lightweight. Today it is a path-based smoke check, not a deep code-aware security engine.

## hooks and CI

- CI now runs `audit-harness`, `check-harness-done`, and a diff-sensitive smoke check.
- A sample git hook is provided at `assets/templates/pre-commit-harness.sh`.
- The hook now checks staged files with `git diff --cached --name-only --diff-filter=ACMR` instead of assuming `HEAD~1..HEAD`.
- `MAKE_HARNESS_HOOK_MODE` supports `strict` (default), `warn`, and `off`.
- The hook prints short summaries like `audit: pass`, `done-gate: pass`, and `sensitive-change: pass` so failures are easier to understand.

Example success output:

```text
PASS: managed files present, contract/runtime split detected, entry files thin
```

Example failure output:

```text
missing managed files: ['harness-contract.json', 'harness-runtime.json']
```

## Quick decision guide

Use `make-harness` when:

- a repository keeps drifting across `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`
- the team wants durable local defaults without adopting a heavier framework
- hidden legacy constraints should be captured once and reused across sessions

Do not use it when:

- the repo is disposable
- the real problem is execution orchestration rather than local contract clarity
- you want the skill to manage runtime tools, plugins, or agent teams

## Resources

- positioning: [docs/positioning.md](docs/positioning.md)
- coexistence: [docs/coexistence.md](docs/coexistence.md)
- fixtures: [assets/fixtures](assets/fixtures)
- fixture validator: [tools/validate-fixtures.py](tools/validate-fixtures.py)
- interview planner: [tools/interview_planner.py](tools/interview_planner.py)
- lightweight audit: [tools/audit-harness.py](tools/audit-harness.py)
- sample output: [assets/examples](assets/examples)
- rollout example: [assets/examples/legacy-webapp-rollout.md](assets/examples/legacy-webapp-rollout.md)
- interview guide: [references/interview-guide.md](references/interview-guide.md)
- interview protocol: [references/interview-protocol.md](references/interview-protocol.md)
- repair playbook: [assets/repair-playbook.md](assets/repair-playbook.md)
- healthy checklist: [assets/healthy-checklist.md](assets/healthy-checklist.md)
- gitignore template: [assets/templates/.gitignore-harness](assets/templates/.gitignore-harness)

## Usage

```text
/make-harness
```

```text
Use the single-entry `/make-harness` skill to bootstrap when no harness exists, update when a healthy harness already exists, or repair drift before continuing.
```
