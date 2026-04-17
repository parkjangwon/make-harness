# Interview Guide

Use this guide when running the `make-harness` interview.

## Interview style

- ask one question at a time
- use plain, everyday language
- avoid jargon when a simpler phrase works
- prefer short answer shapes that are easy to normalize
- inspect the repository first, then ask only what is still unclear
- ask the first language question in English only when no language is confirmed yet
- switch immediately to the confirmed language after the language answer is stored

## Answer normalization

Store user answers in canonical values even if the question is phrased simply.

| User-facing question | Good answer shape | Canonical field | Canonical values |
|---|---|---|---|
| Which language should we use? | `Korean`, `English` | `communication_language` | free text or language code |
| Is this a new project or an existing project? | `new project`, `existing project` | `project_type` | `greenfield`, `legacy` |
| How short should replies be? | `short`, `normal`, `detailed` | `communication_tone` | team-defined tone value |
| When is work done by default? | `small patch only`, `working change plus checks`, `change plus checks and docs` | `definition_of_done` | normalized internal value |
| Should changes be careful, balanced, or bold? | `careful`, `balanced`, `bold` | `change_posture` | `conservative`, `balanced`, `aggressive` |
| What should the agent avoid changing unless you say yes? | short rule list | `change_guardrails` | string array |
| How much checking should we do by default? | `always`, `when practical`, `light only` | `verification_policy` | `required`, `preferred`, `minimal` |
| Which changes always need approval? | short rule or short list | `approval_policy` | free text or normalized rule |
| Which commands should count as this project's default commands? | `test`, `lint`, `build`, `dev` values | `project_commands` | object with command strings |
| Are there important project rules not obvious from the repo? | short rule list | `project_constraints` | string array |
| Is this stack summary right? | `yes`, `no`, short correction | `stack_summary` | string array |
| Are there environment limits or setup rules not obvious from the repo? | short rule list | `environment` | object and notes |

## Question wording

Use wording like this:

- Which language should we use?
- Is this a new project or an existing project?
- How short should replies be?
- When should we count work as done by default?
- Should changes be careful, balanced, or bold by default?
- What should the agent avoid changing unless you say yes?
- How much checking should we do by default?
- Which commands should count as this project's default commands? For example: test, lint, build, or dev.
- Are there important project rules not obvious from the repo?
- Is this stack summary right?
- Are there environment limits or setup rules not obvious from the repo?

## Good follow-up behavior

- if the repository strongly suggests an answer, ask for confirmation instead of asking broadly
- if the answer is vague, restate it in simple terms and confirm the normalized meaning
- if a command does not exist, store it as `unknown` instead of guessing
- if the user gives multiple rules, store them as separate list items when possible
- if the user picks a language, do not keep asking in English out of habit
