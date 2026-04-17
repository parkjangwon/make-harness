# make-harness

<img width="1000" height="550" alt="make-harness" src="https://github.com/user-attachments/assets/e68f3bdd-d549-4158-9f17-5a3111f3c850" />

`make-harness` bootstraps and maintains a repository-local AI harness.

It does not replace a strong agent framework. It fixes project-local operating rules and guardrails into local files.

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
- `harness-state.json`

## Structure

```text
make-harness/
├── SKILL.md
├── README.md
├── README.ko.md
├── docs/
│   └── positioning.md
├── agents/
│   ├── openai.yaml
│   └── gemini.yaml
├── tools/
│   └── validate-fixtures.py
└── assets/
    ├── templates/
    │   ├── .gitignore-harness
    │   └── ...
    ├── fixtures/
    ├── examples/
    ├── healthy-checklist.md
    └── repair-playbook.md
```

## Core

- `PROJECT_HARNESS.md` + `harness-state.json` are the canonical source
- `AGENTS.md` + `CLAUDE.md` + `GEMINI.md` are thin projections
- only durable defaults and guardrails belong here
- drift should be visible and repairable
- this skill should stay easy to compose with stronger frameworks and specialist skills

## Shared contract fields

- `communication_language` (collaboration language)
- `project_type` (project type)
- `definition_of_done` (definition of done)
- `change_posture` (change posture)
- `change_guardrails` (change guardrails)
- `verification_policy` (verification policy)
- `approval_policy` (approval boundary)
- `project_commands` (default project commands)
- `project_constraints` (project constraints)
- `communication_tone` (response tone)
- `stack_summary` (stack summary)
- `environment` (development and runtime environment)

## Modes

- `bootstrap`: no harness yet
- `refresh`: harness is healthy
- `repair`: missing files, contract drift, or invariant failure

## Interview

The skill inspects the repository first, then runs a short interview — one question at a time. Where the repository already gives a clear answer, it asks for confirmation instead of asking open-ended. The full question set covers:

- Collaboration language
- New or existing project
- Reply length preference
- Definition of done
- Change posture (careful / balanced / bold)
- Change guardrails
- Verification policy
- Default project commands
- Project constraints not visible from the repo
- Stack summary confirmation
- Environment constraints

## harness-state.json

The state file tracks both durable config and volatile runtime state.

- `_config_fields`: safe to commit — the durable project contract
- `_volatile_fields`: runtime state (interview progress, sync metadata) — causes merge conflicts on shared repos

For shared repositories, consider adding `harness-state.json` to `.gitignore`. A starter template is at [assets/templates/.gitignore-harness](assets/templates/.gitignore-harness).

## Healthy means

- all managed files exist
- canonical sources agree on the shared contract schema
- entry files are thin and reflect the same contract summary
- state invariants hold
- sync metadata is healthy

Details: [assets/healthy-checklist.md](assets/healthy-checklist.md)

## Fixture validation

Run to verify all fixture scenarios are structurally valid:

```text
python tools/validate-fixtures.py
```

Checks state invariants, template schema alignment, and run-mode consistency across all fixture cases.

## Resources

- positioning: [docs/positioning.md](docs/positioning.md)
- coexistence: [docs/coexistence.md](docs/coexistence.md)
- fixtures: [assets/fixtures](assets/fixtures)
- fixture validator: [tools/validate-fixtures.py](tools/validate-fixtures.py)
- sample output: [assets/examples](assets/examples)
- repair playbook: [assets/repair-playbook.md](assets/repair-playbook.md)
- healthy checklist: [assets/healthy-checklist.md](assets/healthy-checklist.md)
- gitignore template: [assets/templates/.gitignore-harness](assets/templates/.gitignore-harness)

Recommended examples:

- healthy harness: [assets/examples/legacy-webapp-healthy.md](assets/examples/legacy-webapp-healthy.md)
- before/after: [assets/examples/legacy-webapp-before-after.md](assets/examples/legacy-webapp-before-after.md)

## Usage

```text
/make-harness
```

```text
Use the make-harness skill to set up a harness for this repository.
```
