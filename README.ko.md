# make-harness

`make-harness`는 각 저장소에 프로젝트 로컬 하네스를 설치하고 유지하는 도구다.

하나의 canonical durable contract에 저장소별 규칙, 명령, 제약, guardrail을 모으고, 그 계약에서 `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` 같은 thin projection을 다시 만들고, 하네스가 healthy한지 점검한다.

`make-harness`는 개발론 프레임워크가 아니고, 실행 프레임워크도 아니며, orchestration 레이어도 아니다. 더 강한 workflow/methodology 레이어와 조합되는 framework-agnostic local rule layer로 남는 것이 목적이다.

영문 버전: [README.md](README.md)

## 왜 설치하나

`make-harness`를 쓰기 전 흔한 고통:

### Before

- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`가 조금씩 달라진다
- 새 AI 세션마다 같은 프로젝트 규칙을 다시 설명한다
- 어느 파일이 진짜 기준인지 애매해진다
- 위험한 변경 기준이 문서보다 사람 기억에 의존한다

### After

- durable contract 하나가 기준이 된다
- thin entry 파일은 손으로 맞추는 대신 다시 생성한다
- audit / completion check가 하네스가 실제로 healthy한지 말해준다
- 더 큰 에이전트 런타임을 들이지 않고도 repo-local 기본값이 세션을 넘어 유지된다

처음 체감되는 효용은 단순하다. 같은 설명을 덜 반복하고, drift 난 루트 파일이 줄어든다.

## 이런 사람에게 맞다

`make-harness`는 이런 개발자와 팀에 맞습니다.

- 한 리포에서 둘 이상의 AI 코딩 도구를 같이 쓴다
- 새 AI 세션이 열릴 때마다 프로젝트 규칙, 명령, 가드레일을 다시 설명하게 된다
- 여러 루트 instruction 파일을 손으로 맞추기보다 repo-local source of truth 하나를 두고 싶다

예를 들면 Claude Code, Codex, Gemini CLI, Cursor 같은 도구를 함께 쓰는 팀이 대표적인 사용자입니다.

## 특히 잘 맞는 환경

`make-harness`는 프로젝트마다 저장소 로컬 규칙이 다른 환경에서 특히 유용합니다.

대표적으로 잘 맞는 환경:

- 고객사/프로덕트별로 리포를 많이 운영하는 솔루션/서비스 개발 회사
- 레거시 리포, 신규 리포, 보안 민감 리포가 함께 섞여 있는 팀
- 여러 개발자나 여러 AI 도구가 같은 리포를 시간차를 두고 계속 건드리는 조직
- 승인 규칙, 기본 검증 명령, 민감 경로가 프로젝트마다 다른 경우
- 반복 설명과 루트 파일 drift가 장기적으로 계속 쌓이는 리포

상대적으로 덜 맞는 환경:

- 금방 버릴 일회성 리포
- 아주 짧게 쓰고 버릴 실험용 PoC
- 아직 durable한 로컬 규칙을 유지할 필요가 거의 없는 리포

## 더 강한 워크플로와의 조합

`make-harness`는 더 강한 workflow 시스템을 대체하려는 도구가 아니라, 그 아래에서 함께 조합되도록 설계되어 있습니다.

좋은 조합은 보통 이렇게 나뉩니다.

- `make-harness`는 저장소 로컬 계약을 맡는다: 기본값, 명령, 제약, 승인 규칙, thin projection sync
- ecc, superpowers 같은 상위 워크플로 도구는 planning, TDD, code review loop, sub-agent coordination 같은 실행 레이어를 맡는다
- 결과적으로 위 레이어는 어떻게 일할지를 담당하고, `make-harness`는 각 저장소의 로컬 규칙을 안정적으로 유지한다

이 방식이 모든 리포에 하나의 전역 workflow를 억지로 강제하는 것보다 보통 더 현실적입니다.

## `/make-harness`를 실행하면 무슨 일이 일어나나

전형적인 흐름은 이렇습니다.

```text
You: /make-harness

Agent:
1. 저장소와 기존 harness 파일을 먼저 본다
2. repo signal에서 알 수 있는 건 먼저 추론한다
3. durable하게 남아야 할 빈칸만 짧게 묻는다
4. harness 파일을 생성하거나 repair한다
5. 지금 harness가 healthy한지 알려준다
```

결과:

- `PROJECT_HARNESS.md`가 사람이 읽는 계약 기준이 된다
- `harness-contract.json`이 기계가 읽는 durable contract를 담는다
- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`는 얇은 projection으로 정렬된다
- audit / completion check로 지금 harness가 healthy한지 검증할 수 있다

## `skills.sh`로 설치

```bash
npx skills add parkjangwon/make-harness
```

특정 에이전트에만 설치하려면:

```bash
npx skills add parkjangwon/make-harness -a claude-code
npx skills add parkjangwon/make-harness -a codex
npx skills add parkjangwon/make-harness -a gemini-cli
```

설치 전에 노출되는 스킬을 먼저 확인하려면:

```bash
npx skills add parkjangwon/make-harness --list
```

관리 파일은 아래 여섯 개입니다.

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `PROJECT_HARNESS.md`
- `harness-contract.json`
- `harness-runtime.json`

## 핵심 원칙

- `PROJECT_HARNESS.md` + `harness-contract.json`이 영속 계약의 기준이다
- `harness-runtime.json`은 인터뷰 진행, 감지 결과, sync 메타데이터 같은 휘발성 상태만 담는다
- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`는 얇은 projection이다
- durable 계약에는 오래 유지할 기본값과 가드레일만 넣는다
- drift는 보여야 하고 repair 가능해야 한다
- 더 강한 프레임워크와 전문 스킬 옆에서 조용히 공존해야 한다
- 프로젝트 로컬 보안 가드레일은 계약에 넣고, 리포에는 lightweight path-based guardrail smoke check만 둔다

## 공유 계약 필드

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

`rule_strengths`는 계약의 최소 enforcement layer야. 각 durable rule이 advisory / guided / enforced 중 어느 강도로 다뤄져야 하는지 표현하되, 하네스를 무거운 실행 프레임워크로 키우지는 않는다.

## 경계선 필드: 방법론이 아니라 저장소 로컬 규칙으로 다뤄야 한다

몇몇 필드는 이름만 보면 범위가 넓어 보일 수 있지만, `make-harness` 안에서는 반드시 저장소 로컬 의미로만 다뤄야 한다.

- `definition_of_done` = 이 저장소의 기본 완료 기준 또는 local completion gate
- `verification_policy` = 이 저장소의 기본 검증 규칙
- `approval_policy` = 위험하거나 민감한 변경에 대한 이 저장소의 확인 규칙
- `change_posture` = 이 저장소에서 변경 범위를 어느 정도 보수적으로 볼지에 대한 좁은 기본값

반대로 planning, TDD, branch strategy, code review loop, brainstorming, sub-agent coordination 같은 것은 더 강한 상위 workflow 레이어에서 다룰 일이지, durable harness contract에 강하게 저장할 일이 아니다.

## 동작 모드


- `bootstrap`: 하네스가 아직 없음
- `update`: healthy 하네스면 같은 `/make-harness` 명령에서 보강/수정 모드로 들어감
- `repair`: 파일 누락, 계약 drift, invariant 파손이 있음

## 인터뷰

하네스는 저장소를 먼저 보고, 남는 불확실성만 짧게 묻습니다. 언어는 영어 고정 시작이 아니라 detect-first 원칙을 따릅니다. README, 디렉터리, 기존 문맥 등으로 협업 언어 힌트를 먼저 잡고, 확신이 부족할 때만 확인 질문을 합니다.

인터뷰는 다음 원칙으로 더 구체적으로 고정되어 있습니다.

- 이건 one-time setup이므로, 질문 수를 무작정 줄이는 것보다 정확한 규칙 확정이 더 중요
- 기존 저장소는 repo-first gap-filling 방식으로, 코드 분석 후 정말 필요한 것만 확인
- 빈 프로젝트는 코드가 없으므로 stack/runtime/package manager를 정하는 소규모 setup-discovery 질문을 먼저 진행
- durable default용 고정 질문 순서 사용
- 저장소 confidence에 따른 분기 규칙 사용
- 일반적인 저장소에서는 명시 질문 5개 이하를 목표로 하되, 빈 프로젝트는 필요한 경우 더 촘촘히 물을 수 있음
- change posture, approval policy, verification policy 같은 자유 응답을 canonical 값으로 정규화
- `harness-runtime.json`이 중간 상태를 가리키면 resume 규칙과 contradiction 규칙 적용
- 보안 민감 영역, 금지 secret/debug 패턴, 설정 기반 TLS 예외 규칙, 추가 보안 검증 명령처럼 꼭 필요한 최소 보안 인터뷰 항목 포함

자세한 규칙은 [references/interview-guide.md](references/interview-guide.md), [references/interview-protocol.md](references/interview-protocol.md)를 참고하세요.

## durable / volatile 분리

### `harness-contract.json`

커밋 대상입니다. 기계가 읽을 수 있는 영속 프로젝트 계약을 담습니다.

### `harness-runtime.json`

영속 계약의 기준 파일이 아닙니다. 인터뷰 진행 상태, 언어 감지 힌트, sync 메타데이터, audit 타임스탬프 같은 휘발성 상태만 담습니다.

공유 저장소에서는 `harness-runtime.json`을 `.gitignore`에 넣는 것을 권장합니다. 기본 템플릿은 [assets/templates/.gitignore-harness](assets/templates/.gitignore-harness)에 있습니다.

## healthy의 의미

- 관리 파일이 모두 존재한다
- 영속 canonical source가 같은 계약을 가리킨다
- 엔트리 파일이 얇고 같은 계약 요약을 반영한다
- runtime invariant가 유지된다
- sync metadata가 healthy하다

자세한 기준은 [assets/healthy-checklist.md](assets/healthy-checklist.md)에 정리되어 있습니다.

## fixture 검증

```text
python tools/validate-fixtures.py
```

이 검증기는 이제 `tools/interview_planner.py`의 deterministic interview planner와도 교차 검증합니다. 즉 blank project에서 runtime/package manager discovery를 물어야 하는지, detect-first language confirmation이 맞는지, resume 시 다음 질문이 무엇인지가 문서 설명에만 머물지 않고 fixture 레벨에서 고정됩니다.

## 가벼운 audit

```text
python tools/audit-harness.py /path/to/project
```

이 명령은 LLM 없이도 파일 구성, contract/runtime 분리, 엔트리 파일 두께, 핵심 runtime invariant를 검사합니다.

## 결정적 projection 생성기

`harness-contract.json`과 `harness-runtime.json`에서 바로 `PROJECT_HARNESS.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`를 기계적으로 생성하려면 다음을 실행하세요:

```text
python tools/apply-harness.py /path/to/project
```

이 도구는 리포 안에서 가장 작은 실행 계층이다. LLM이 durable contract를 결정하더라도 projection file은 손으로 다시 쓰지 않게 해준다.

## 완료 게이트

하네스가 단순히 존재하는 수준이 아니라 실제로 완료 가능한 상태인지 확인하려면 다음을 실행하세요:

```text
python tools/check-harness-done.py /path/to/project
```

이 게이트는 audit 성공, `configured` + `healthy` 상태, 전체 `validated_shared_fields`, 그리고 현재 projection이 deterministic generator 출력과 완전히 일치하는지를 요구한다.

## 구조

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

## 가벼운 경로 기반 guardrail smoke check

다음 명령으로 auth / 권한 / secret / 결제 / 암호화 / public API 영역을 건드리는 변경을 감지할 수 있다:

```text
python tools/check-sensitive-change.py /path/to/project --paths src/auth/login.py config/tls-dev.yaml
```

git ref 기준으로 검사하려면 다음처럼 실행한다:

```text
python tools/check-sensitive-change.py /path/to/project --base HEAD~1 --head HEAD
```

관련 `rule_strengths`가 `enforced`면 민감한 변경은 완료/CI/hook 단계에서 차단된다. `guided`면 카테고리를 보고만 하고 막지는 않는다.

이 checker는 의도적으로 가볍다. 현재는 깊은 코드 분석기가 아니라 path-based smoke check다.

## hooks와 CI

- CI는 이제 `audit-harness`, `check-harness-done`, diff-sensitive smoke check를 함께 실행한다.
- 샘플 git hook은 `assets/templates/pre-commit-harness.sh`에 있다.
- hook은 `HEAD~1..HEAD` 가정 대신 `git diff --cached --name-only --diff-filter=ACMR` 기준으로 staged file만 검사한다.
- `MAKE_HARNESS_HOOK_MODE`는 `strict`(기본), `warn`, `off`를 지원한다.
- hook은 `audit: pass`, `done-gate: pass`, `sensitive-change: pass` 같은 짧은 요약을 출력해서 실패 이유를 더 읽기 쉽게 만든다.

성공 예시:

```text
PASS: managed files present, contract/runtime split detected, entry files thin
```

실패 예시:

```text
missing managed files: ['harness-contract.json', 'harness-runtime.json']
```

## 빠른 판단 가이드

다음 상황이면 `make-harness`가 잘 맞습니다.

- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`가 계속 어긋난다
- 무거운 프레임워크 없이 프로젝트 로컬 기본 계약만 안정화하고 싶다
- 레거시 저장소의 숨은 제약을 한 번 정리해 재사용하고 싶다

반대로 아래라면 맞지 않을 수 있습니다.

- 저장소가 일회성이다
- 문제의 본질이 contract가 아니라 execution orchestration이다
- 플러그인, 런타임 툴, 에이전트 팀 관리까지 기대한다

## 더 보고 싶다면

- 포지셔닝: [docs/positioning.md](docs/positioning.md)
- 공존 원칙: [docs/coexistence.md](docs/coexistence.md)
- fixture: [assets/fixtures](assets/fixtures)
- fixture 검증기: [tools/validate-fixtures.py](tools/validate-fixtures.py)
- interview planner: [tools/interview_planner.py](tools/interview_planner.py)
- lightweight audit: [tools/audit-harness.py](tools/audit-harness.py)
- sample output: [assets/examples](assets/examples)
- 도입 예시: [assets/examples/legacy-webapp-rollout.md](assets/examples/legacy-webapp-rollout.md)
- 인터뷰 가이드: [references/interview-guide.md](references/interview-guide.md)
- 인터뷰 프로토콜: [references/interview-protocol.md](references/interview-protocol.md)
- repair playbook: [assets/repair-playbook.md](assets/repair-playbook.md)
- healthy checklist: [assets/healthy-checklist.md](assets/healthy-checklist.md)
- gitignore 템플릿: [assets/templates/.gitignore-harness](assets/templates/.gitignore-harness)

## 사용 예시

```text
/make-harness
```

```text
하네스가 없으면 bootstrap, 이미 healthy하면 update, 깨져 있으면 repair 후 이어서 진행하는 단일 엔트리 `/make-harness` 명령입니다.
```
