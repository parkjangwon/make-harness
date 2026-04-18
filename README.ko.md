# make-harness

<img width="1000" height="550" alt="make-harness" src="https://github.com/user-attachments/assets/e68f3bdd-d549-4158-9f17-5a3111f3c850" />

`make-harness`는 저장소 안에서 오래 유지할 AI 작업 계약을 정리해주는 로컬 하네스 스킬입니다.

강한 에이전트 프레임워크를 대체하려는 도구는 아닙니다. 대신 프로젝트마다 달라지는 영속 계약과 실행 가드레일을 로컬 파일에 고정하고, 인터뷰/동기화 같은 런타임 상태는 별도 파일로 분리해 둡니다.

영문 안내는 [README.md](README.md)에서 볼 수 있습니다.

## skills.sh로 설치하기

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
│   ├── interview_planner.py
│   └── validate-fixtures.py
└── assets/
    ├── templates/
    ├── fixtures/
    ├── examples/
    ├── healthy-checklist.md
    └── repair-playbook.md
```

## 핵심 원칙

- `PROJECT_HARNESS.md` + `harness-contract.json`이 영속 계약의 기준이다
- `harness-runtime.json`은 인터뷰 진행, 감지 결과, sync 메타데이터 같은 휘발성 상태만 담는다
- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`는 얇은 projection이다
- durable 계약에는 오래 유지할 기본값과 가드레일만 넣는다
- drift는 보여야 하고 repair 가능해야 한다
- 더 강한 프레임워크와 전문 스킬 옆에서 조용히 공존해야 한다
- 프로젝트 로컬 보안 가드레일은 계약에 넣되, 전체 AppSec 프레임워크까지 떠안지는 않는다

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

## Deterministic projection generator

`harness-contract.json`과 `harness-runtime.json`에서 바로 `PROJECT_HARNESS.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`를 기계적으로 생성하려면 다음을 실행하세요:

```text
python tools/apply-harness.py /path/to/project
```

이 도구는 리포 안에서 가장 작은 실행 계층이다. LLM이 durable contract를 결정하더라도 projection file은 손으로 다시 쓰지 않게 해준다.

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
