# Interview Protocol

Use this reference to make the `make-harness` interview reproducible across agents.

The high-level style rules still live in [interview-guide.md](interview-guide.md). This document fixes the operational details that were previously too loose: question order, branching thresholds, normalization rules, resume behavior, and contradiction handling.

## Goals

- keep the interview short when the repository already answers most questions
- allow a denser first interview when the harness is doing a one-time setup and durable project rules still need to be discovered
- ask one question at a time
- inspect the repository before asking for information
- prefer confirmation over open-ended prompts when the repo already gives a strong signal
- normalize durable defaults into stable canonical values
- resume cleanly when the interview was interrupted
- split interview behavior between existing repositories and blank projects so the agent asks only what the situation actually requires
- for one-time setup, precision is more important than minimizing question count

## Existing repository mode

Use this mode when the repository already contains meaningful code, config, or runtime/tooling signals.

Rules:

- analyze the codebase first
- do not ask for stack or package-manager choices that the repository already answers
- infer commands from executable metadata before asking
- default to confirmation questions because most durable defaults should already be visible
- treat the interview as gap-filling, not initial discovery

Typical existing-repo topics that may still require confirmation:

- collaboration language when signals are mixed
- definition of done when the repo has code but weak quality rituals
- approval/change posture preferences that code alone cannot reveal
- project constraints that are social or organizational rather than technical

## Blank project mode

Use this mode when the project is empty or almost empty and there is no meaningful codebase to inspect.

Rules:

- ask more upfront because there is no code to inspect
- gather the minimum setup-defining answers needed to avoid bad defaults
- ask in plain product-builder language rather than schema language
- prefer compact choice-oriented questions over abstract policy questions

For blank projects, the first interview usually needs to confirm at least:

- collaboration language
- project type
- primary stack
- runtime
- package manager
- test/build/dev command expectations when they are not implied yet
- whether `typecheck` should be part of the default verification set when the stack implies typed code (for example TypeScript or typed Python tooling)
- whether the default command set should include `dev / build / test / lint / typecheck` rather than stopping at a thinner subset

## Question order

Use this order unless an earlier answer makes a later question unnecessary:

1. `communication_language`
2. `project_type`
3. `definition_of_done`
4. `change_posture`
5. `change_guardrails`
6. `verification_policy`
7. `approval_policy`
8. `project_commands`
9. `project_constraints`
10. `communication_tone`
11. `stack_summary`
12. `environment`

Why this order:

- language changes the wording of every later question
- project type, commands, and stack shape the rest of the interview
- verification and approval rules should be confirmed before finalizing the contract
- constraints and tone are cheaper to ask once core execution rules are already known

## Branching and confidence rules

### Confidence thresholds

Treat repo signals using these thresholds:

- `high` confidence: about 70% or higher and multiple signals agree
- `medium` confidence: one strong signal or several weak signals that mostly agree
- `low` confidence: weak, mixed, or contradictory signals

### What to do at each confidence level

- `high`: ask a confirmation question, not an open-ended question
- `medium`: ask a short either/or or short-answer confirmation question
- `low`: ask an open-ended question in plain language

### Signal priority

Use deterministic source priority when inferring likely values:

- language: root README, root docs, issue templates, file naming, then comments
- commands: package/tool config first, then README examples, then fallback guesses
- stack: package manifests and lockfiles first, then source tree, then README text

For commands specifically:

- README.md before package.json is acceptable only as an exploratory hint
- package.json scripts override README command guesses once scripts are present
- pyproject.toml / Makefile / justfile / cargo metadata should outrank prose descriptions when they exist

### Confirmation wording rule

If a likely answer exists, phrase the next question as a confirmation:

- good: "README와 package.json을 보면 테스트는 `npm test`로 보이는데, 이걸 기본 검증 명령으로 둘까?"
- bad: "테스트 명령은 무엇인가요?"

### Language-first framing rule

Do not prepend English mode/status framing before the first Korean confirmation question when Korean confidence is high.

- good: "README가 한국어라 기본 협업 언어도 한국어로 보면 될까?"
- bad: "Bootstrap mode — existing repo detected. README가 한국어라 기본 협업 언어도 한국어로 보면 될까?"
- if run classification or repo summary needs to be explained before the first question, explain it in Korean as well
- If the current user message is already in Korean, keep the preface and the first question in Korean even when the repository itself is blank.
- Use the current conversation language as a first-pass signal before falling back to plain-English blank-repo openers.

## Question budget

Keep the bootstrap interview tight:

- hard target: 5 or fewer explicit questions for common repos
- soft ceiling: 8 questions before the agent should explain why more clarification is needed
- never ask a question when the answer is already strongly implied and only needs confirmation

If a repo is already well-described, the interview should feel like selective confirmation, not a blank survey.

## Canonical normalization

Normalize free-form user answers into stable stored values.

### `communication_language`

- "한국어", "한글", "한국어 위주" -> `ko`
- "영어", "English" -> `en`
- "한국어 위주인데 필요하면 영어도 괜찮아" -> `ko` plus note in `change_guardrails` or `notes`, not a hybrid enum

### `project_type`

Prefer a small stable set:

- app, web app, website -> `webapp`
- backend service, API server -> `service`
- library, SDK, package -> `library`
- legacy app, existing old project -> `legacy`
- monorepo -> `monorepo`
- unclear mixed repo -> keep the nearest durable type and add notes instead of inventing a new enum casually

### `change_posture`

`change_posture` is only a narrow local default for change scope in this repository.
It is not a general engineering philosophy.

- "웬만하면 보수적으로", "작게 가자", "큰 변경은 부담" -> `conservative`
- "필요하면 과감하게 정리" -> `balanced`
- "대대적으로 뜯어고쳐도 된다" -> `aggressive`

### `approval_policy`

`approval_policy` is stored as the repository's confirmation rule for risky or sensitive changes.
It is not a full team workflow policy.

- "큰 변경은 먼저 물어봐", "위험한 건 승인 받고" -> `explicit_for_risky_changes`
- "왠만한 건 그냥 진행해도 돼" -> `implicit_for_safe_changes`
- "모든 변경 전에 확인" -> `explicit_for_all_changes`

### `definition_of_done`

`definition_of_done` is stored as a repo-local completion expectation or local completion gate.
It is not a universal development philosophy.

- "보통은 테스트/린트까지 통과하면 완료" -> repo-local completion expectation focused on the repository's default completion checks
- "코드 변경이면 테스트/린트/타입체크, 문서 변경이면 수동 확인" -> keep the local completion gate narrow and store exceptions in notes if needed
- avoid turning this field into a broad statement about how all work must be done across every situation

### `verification_policy`

`verification_policy` is stored as the repository's default verification rule.
It is not a statement about how all development should be done.

- "테스트는 있으면 돌리고, 없으면 빌드라도" -> `required` with command notes describing fallback behavior
- "항상 테스트/린트 확인" -> `required`
- "급하면 검증 없이도 가능" -> `best_effort`

### `communication_tone`

- "짧고 실무적으로" -> `concise`
- "친절하게 설명해줘" -> `supportive`
- "딱딱하게 사실만" -> `direct`

### `project_commands`

When the repo exposes real commands, store them exactly.

- keep actual executable strings such as `npm test`, `pnpm lint`, `pytest -q`
- do not normalize commands into abstract labels
- if both README and tool metadata disagree, ask a confirmation question before storing

## Resume rules

When `bootstrap_status` is `interview_in_progress`, resume instead of restarting.

Resume checklist:

1. read `harness-runtime.json`
2. read the latest durable answers in `harness-contract.json`
3. use `interview_step` as the next default question
4. preserve `confirmed_fields`
5. treat unconfirmed repo-derived guesses as temporary inference, not durable truth
6. only move a field from temporary inference into durable contract after explicit confirmation or a very strong existing canonical source

If the repository changed since the last interview run, re-check any field whose inference source is now stale.

## Contradiction handling

Contradiction means the user answer conflicts with an existing durable value or with a strong repo signal.

When contradiction happens:

1. do not silently overwrite the durable contract
2. explain the conflict briefly
3. ask a focused confirmation question
4. if the user confirms the new answer, update the durable contract and append change history
5. if the user rejects the new answer, keep the current durable value and record the reason in notes or drift metadata

Example:

- repo says Korean README, previous contract says `ko`, user now says "영어로 하자"
- response: confirm whether collaboration language should change permanently or only for this conversation

## Adaptive response modes

do not classify the user as junior or senior.
Instead, adapt per answer, not per person label.

### precision mode

Use this when the user answers with concrete commands, explicit trade-offs, or exact override rules.

Signals:
- specific commands like `pnpm test` or `python3 -m pytest -q`
- explicit exception rules
- confident corrections such as "아니, 그건 이렇게 저장해줘"

Behavior:
- ask tighter follow-up questions
- allow precise overrides
- avoid repeating explanatory defaults the user no longer needs

### clarify mode

Use this when the user gives partial intent but not enough detail to store a durable rule yet.

Signals:
- "대충 이런 느낌"
- mixed or half-complete answers
- answers that identify direction but not the exact stored value

Behavior:
- ask a short either/or follow-up
- narrow ambiguity before writing durable state
- prefer one clarifying question over a long explanation

### safe-default mode

Use this when the user is unsure, hesitant, or explicitly says they do not know.

Signals:
- "잘 모르겠어요"
- "아직 안 정했어요"
- long hesitation without concrete preference

Behavior:
- offer a safe default first
- explain that it can be changed later
- keep the choice low-pressure
- avoid making the user invent architecture on the spot

## Existing repository question templates

These should feel like confirmation, not configuration.

- language: "README가 한국어라 기본 협업 언어도 한국어로 보면 될까?"
- project type: "지금 구조를 보면 이 프로젝트는 웹앱으로 보면 될까?"
- definition of done: "이 저장소에서 기본 완료 기준은 어떤 로컬 체크로 둘까? 잘 모르겠으면 테스트/린트 같은 저장소 기본 검증을 completion gate로 먼저 둘게."
- approval policy: "이 저장소에서 위험하거나 민감한 변경은 먼저 확인받을까, 아니면 안전한 수정은 바로 진행해도 될까? 애매하면 위험한 변경만 먼저 확인받는 로컬 기본값으로 둘 수 있어."
- verification policy: "이 저장소의 기본 검증 규칙은 `npm test`와 `npm run lint` 기준으로 잡을까?"
- constraints: "코드만 보고는 안 보이는 저장소 로컬 제약이 있으면 한두 가지만 알려줘. 잘 모르겠으면 지금은 비워두고 나중에 보강해도 돼."

## Minimal security interview items

Keep this light. The harness should capture project-local security guardrails, not become a full AppSec framework.

Ask only the minimum durable security questions that actually affect how an agent should change code in this repository:

1. sensitive areas
- ask whether changes touching auth, permissions, secrets, payments, encryption, or public API exposure need stricter confirmation
- store durable answers mainly in `change_guardrails` and, when approval strictness changes, in `approval_policy`

2. secrets and unsafe debug patterns
- ask whether any files or values must never be committed, and whether patterns like hardcoded secrets or debug backdoors are explicitly forbidden
- for TLS verification, do not impose a blanket prohibition on all exceptions: ask whether configuration-based exception paths are allowed for specific environments or compatibility cases, and require that any configuration-based TLS exception be explicit, reviewable, and never silently enabled by default
- store these in `project_constraints` and `change_guardrails`

3. security verification commands
- ask whether security verification commands are required when touching sensitive code, such as `bandit`, `semgrep`, `npm audit`, or repo-specific checks
- store the requirement in `verification_policy` and the exact commands in `project_commands` notes or command entries

Recommended wording for existing repositories:
- "인증, 권한, secret, 결제, 외부 공개 API 같은 민감 영역은 수정 전에 더 엄격하게 확인받아야 할까?"
- "절대 커밋하면 안 되는 값이나 금지 패턴이 있을까? 예를 들면 실제 secret, 하드코딩 키, 디버그 백도어 같은 것들. TLS 검증 예외가 필요하다면 설정 기반으로만 허용하고 기본값은 안전하게 둘지 같이 정할 수 있어."
- "보안 민감 코드를 건드릴 때 추가로 꼭 돌려야 하는 검증 명령이 있을까? 없으면 지금 검증 규칙 그대로 둘게."

Recommended wording for blank projects:
- "이 프로젝트에서 특히 민감한 영역이 예상되면 미리 알려줘. 예를 들면 auth, 권한, 결제, secret 처리 같은 것들."
- "절대 허용하면 안 되는 보안 패턴이 있으면 지금 한두 가지만 정할까? 잘 모르겠으면 기본적으로 secret 하드코딩과 디버그 백도어 금지로 둘 수 있어. TLS 검증 예외가 필요하면 설정 기반으로만 켜고 끄도록 두는 식으로 정리할 수 있어."
- "보안 관련 검증을 기본 검증에 같이 묶을까, 아니면 민감한 코드 변경 때만 추가로 돌릴까?"

Do not create a separate heavyweight security framework section in the harness. Keep security as project-local security guardrails mapped into existing durable fields.

## Blank project question templates

These should feel like setup decisions for a new project, not abstract policy forms.

- language: "기본 협업 언어는 한국어로 갈까, 영어로 갈까? 잘 모르겠으면 내가 한국어를 기본값으로 둘 수도 있어."
- project type: "이번 프로젝트는 웹앱, 백엔드 서비스, 라이브러리 중 어디에 가까워? 잘 모르겠으면 내가 가장 가까운 기본값을 먼저 제안할게."
- stack: "프론트/백엔드 기준으로 어떤 기술스택으로 시작할까? 아직 정해진 게 없으면 내가 무난한 시작 스택을 제안할게."
- runtime: "런타임은 Node, Bun, Python 중 어떤 쪽으로 갈까? 잘 모르겠으면 가장 무난한 기본값부터 잡아도 돼."
- package manager: "패키지 매니저는 npm, pnpm, yarn 중 뭐로 갈까? 아직 취향이 없으면 내가 무난한 기본값을 먼저 제안할게."
- definition of done: "초기 기준으로는 이 저장소의 기본 완료 체크를 테스트/린트까지로 둘까? 타입이 있는 스택이면 `typecheck`도 로컬 completion gate에 넣을게. 잘 모르겠으면 이걸 기본값으로 둘게."
- approval policy: "이 저장소에서 큰 구조 변경이나 민감 변경은 먼저 물어보고 갈까, 아니면 안전한 수정은 바로 진행해도 될까? 잘 모르겠으면 위험한 변경만 먼저 확인받는 로컬 기본값으로 둘 수 있어."
- commands: "이 저장소의 기본 명령은 dev / build / test / lint / typecheck 정도로 잡을 텐데, 원하는 형태가 있으면 말해줘. 아직 없으면 내가 일반적인 로컬 기본값으로 먼저 잡을게."

## Three-level template matrix

Use this matrix when choosing the actual wording for each field.

- high confidence -> confirmation wording
- medium confidence -> short either/or confirmation wording
- low confidence -> open-ended plain wording
- for both senior and junior users, prefer two-step questioning: start with an easy default-offer question, then ask a more specific follow-up only if needed
- if the user seems unsure, say: "잘 모르겠으면 내가 무난한 기본값을 먼저 제안할게"
- if the interview is in English, say: "If you're not sure, I can suggest a safe default first"

### communication_language

- KO high: "README가 한국어라 기본 협업 언어도 한국어로 보면 될까?"
- KO medium: "기본 협업 언어는 한국어 쪽이 맞아, 아니면 영어로 보는 게 더 맞아?"
- KO low: "기본 협업 언어를 어떻게 잡는 게 좋을까?"
- EN high: "Would it be okay to treat the default collaboration language as Korean?"
- EN medium: "Should the default collaboration language be Korean or English?"
- EN low: "What should the default collaboration language be for this project?"

### project_type

- KO high: "지금 구조를 보면 이 프로젝트는 웹앱으로 보면 될까?"
- KO medium: "웹앱에 더 가까워 보여. 아니면 백엔드 서비스나 라이브러리 쪽이 더 맞아?"
- KO low: "이 프로젝트는 웹앱, 백엔드 서비스, 라이브러리 중 어디에 가까워?"
- EN high: "From the current structure, would it make sense to treat this project as a web app?"
- EN medium: "It looks closer to a web app. Is that right, or is it more of a backend service or library?"
- EN low: "Which project type fits best here: web app, backend service, or library?"

### definition_of_done

- KO high: "보통은 테스트/린트까지 통과하면 완료로 볼까? 잘 모르겠으면 내가 이걸 기본값으로 둘게."
- KO medium: "완료 기준을 테스트/린트 통과까지로 볼까, 아니면 동작 확인까지만 볼까? 애매하면 내가 먼저 기본값을 제안할게."
- KO low: "이 프로젝트에서 작업이 끝났다고 볼 기준은 뭐가 좋을까? 잘 모르겠으면 테스트/린트 통과를 기본값으로 잡아도 돼."
- EN high: "Would it be okay to treat passing tests and lint as the default definition of done? If you're not sure, I can use that as a safe default."
- EN medium: "Should the default definition of done be passing tests/lint, or is a working manual check enough? If you want, I can suggest a safe default first."
- EN low: "What should count as done for this project by default? If you're not sure, I can suggest a safe default."

### approval_policy

- KO high: "큰 변경은 먼저 확인받는 쪽이 좋아, 아니면 안전한 수정은 바로 진행해도 될까? 애매하면 위험한 변경만 먼저 확인받는 기본값으로 둘게."
- KO medium: "위험한 변경만 먼저 확인받을까, 아니면 모든 변경 전에 확인받는 게 좋을까? 잘 모르겠으면 내가 무난한 기본값을 먼저 제안할게."
- KO low: "변경 전에 어느 정도까지 확인을 받고 진행하면 좋을까? 잘 모르겠으면 위험한 변경만 먼저 확인받는 쪽으로 시작할 수 있어."
- EN high: "For larger changes, should I check with you first, while safe edits can go through directly? If you're unsure, I can default to confirming only risky changes first."
- EN medium: "Should only risky changes require approval first, or should every change be confirmed? If you want, I can suggest a safe default first."
- EN low: "How strict should the approval rule be before making changes? If you're not sure, I can start with a safe default."

### project_commands

- KO high: "README와 설정을 보면 기본 검증은 `npm test`로 보이는데, 이걸 기준으로 둘까?"
- KO medium: "지금 보이는 명령은 `npm test` 쪽인데, 다른 기본 테스트 명령이 있으면 그걸로 잡을까? 잘 모르겠으면 현재 보이는 명령을 기본값으로 둘게."
- KO low: "기본 dev/build/test 명령은 어떤 형태로 잡는 게 좋을까? 아직 없으면 내가 일반적인 기본값을 먼저 제안할게."
- EN high: "From the README and config, `npm test` looks like the default verification command. Should I use that?"
- EN medium: "The repo suggests `npm test`, but if you prefer a different default test command I can use that instead. If you're unsure, I can keep the current visible command as the default."
- EN low: "What should the default dev/build/test commands be for this project? If you're not sure, I can suggest a safe default first."

## English companion templates

Use these when the collaboration language is English or when the protocol explicitly needs an English opener.

- Existing repo language confirmation: "Would it be okay to treat the default collaboration language as Korean?"
- Existing repo project type confirmation: "From the current structure, would it make sense to treat this project as a web app?"
- Existing repo done criteria: "Would it be okay to treat passing tests and lint as the default definition of done?"
- Blank project package manager: "Which package manager do you want to use: npm, pnpm, or yarn?"
- Blank project runtime: "Which runtime do you want to start with: Node, Bun, or Python?"
- Blank project stack: "What stack do you want to start with for this project?"

## Minimal question templates

Use short, plain prompts.

- language high confidence: "README가 한국어라 기본 협업 언어도 한국어로 보면 될까?"
- project type high confidence: "지금 구조를 보면 웹앱으로 보이는데, 이 프로젝트 타입을 `webapp`으로 잡을까?"
- approval policy open question: "큰 변경이나 위험한 수정은 먼저 확인받아야 해, 아니면 안전한 건 바로 진행해도 돼?"
- verification policy confirmation: "기본 검증은 `npm test`와 `npm run lint` 기준으로 잡을까?"

## What not to store durably

Do not store these as permanent contract state:

- current task type like bugfix or refactor
- temporary urgency
- one-off branch names
- framework-specific orchestration preferences
- guesses that were never confirmed
- TDD preferences or broader development methodology choices
- branch strategy defaults that are not repo-local guardrails
- code review loop structure
- brainstorming or planning procedures
- sub-agent usage rules

Do not ask about TDD, branch strategy, code review loops, or sub-agent usage as durable contract state unless a repository-local rule directly depends on them and can be expressed as a concrete local guardrail.

## Fixture expectations for interview-heavy scenarios

Interview-oriented fixture coverage should include at least:

- detect-first language confirmation
- interrupted interview resume
- conflicting repo signals
- contradiction between user answer and durable contract
- partial command discovery where only some scripts exist
