# make-harness

<img width="1000" height="550" alt="make-harness" src="https://github.com/user-attachments/assets/e68f3bdd-d549-4158-9f17-5a3111f3c850" />

`make-harness` bootstraps and maintains a repository-local AI harness.

It does not replace a strong agent framework. It fixes durable project-local rules and guardrails into local files, while keeping volatile interview and sync state separate.

Korean version: [README.ko.md](README.ko.md)

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
│   ├── audit-harness.py
│   ├── interview_planner.py
│   └── validate-fixtures.py
└── assets/
    ├── templates/
    ├── fixtures/
    ├── examples/
    ├── healthy-checklist.md
    └── repair-playbook.md
```

## Core

- `PROJECT_HARNESS.md` + `harness-contract.json` are the canonical durable contract
- `harness-runtime.json` is volatile runtime state only
- `AGENTS.md` + `CLAUDE.md` + `GEMINI.md` are thin projections
- only durable defaults and guardrails belong in the durable contract
- drift should be visible and repairable
- this skill should stay easy to compose with stronger frameworks and specialist skills

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
- `communication_tone`
- `stack_summary`
- `environment`

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
