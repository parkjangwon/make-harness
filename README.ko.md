# make-harness

<img width="1000" height="550" alt="make-harness" src="https://github.com/user-attachments/assets/e68f3bdd-d549-4158-9f17-5a3111f3c850" />

`make-harness`는 저장소 안에서 오래 유지할 AI 작업 규칙을 정리해주는 로컬 하네스 스킬입니다.

이 스킬은 강한 에이전트 프레임워크를 대체하려는 도구가 아닙니다. 대신 프로젝트마다 달라지는 운영 계약과 실행 가드레일을 로컬 파일에 차분하게 고정해서, 매번 같은 설명을 반복하지 않도록 돕습니다.

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

설치 전에 이 저장소가 노출하는 스킬을 먼저 확인하려면:

```bash
npx skills add parkjangwon/make-harness --list
```

이 스킬이 관리하는 파일은 아래 다섯 개입니다.

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `PROJECT_HARNESS.md`
- `harness-state.json`

## 구조

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

`PROJECT_HARNESS.md`와 `harness-state.json`이 실제 계약의 기준이 되고, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`는 그 계약을 얇게 반영하는 엔트리 파일입니다.

## 무엇을 고정하나

하네스는 아래 같은 항목을 프로젝트 기본 계약으로 다룹니다.

- `communication_language` (소통 언어)
- `project_type` (프로젝트 형태)
- `definition_of_done` (완료 기준)
- `change_posture` (변경 성향)
- `change_guardrails` (변경 가드레일)
- `verification_policy` (검증 정책)
- `approval_policy` (승인 경계)
- `project_commands` (기본 프로젝트 명령)
- `project_constraints` (프로젝트 제약사항)
- `communication_tone` (응답 톤)
- `stack_summary` (기술 스택 요약)
- `environment` (개발 및 실행 환경)

반대로 앱 이름이나 패키지 구조처럼 저장소를 보면 알 수 있는 정보는 기본 계약 필드로 고정하지 않습니다. 정말 필요할 때만 보강합니다.

이 스킬은 강한 플러그인이나 전문 스킬과 경쟁하려는 도구가 아니라, 그런 도구들과 함께 쓸 수 있는 프로젝트 로컬 계약 계층으로 남는 것을 목표로 합니다.

## 어떻게 동작하나

하네스 작업은 세 가지 모드로 나뉩니다.

- `bootstrap`: 하네스가 아직 없을 때 처음 세팅합니다.
- `refresh`: 하네스가 건강한 상태인지 확인하고 가볍게 갱신합니다.
- `repair`: 파일이 빠졌거나 계약이 어긋났을 때 다시 맞춥니다.

인터뷰는 저장소를 먼저 탐색한 뒤, 한 번에 하나씩 질문합니다. 저장소에서 추론 가능한 항목은 확인 형태로 묻습니다. 전체 질문 항목은 아래와 같습니다.

- 소통 언어
- 신규 프로젝트인지 기존 프로젝트인지
- 응답 길이 선호도
- 완료 정의
- 변경 성향 (보수적 / 균형 / 적극적)
- 변경 가드레일
- 검증 정책
- 기본 프로젝트 명령
- 저장소만 보고 알기 어려운 프로젝트 제약사항
- 기술 스택 요약 확인
- 환경 제약사항

## harness-state.json

상태 파일은 durable 설정과 volatile 런타임 상태를 함께 담고 있습니다.

- `_config_fields`: 커밋해도 안전한 영구 프로젝트 계약 필드
- `_volatile_fields`: 인터뷰 진행 상태, sync 메타데이터 등 런타임 상태 — 공유 레포에서 merge conflict 유발 가능

팀이 함께 쓰는 저장소라면 `harness-state.json`을 `.gitignore`에 추가하는 것을 권장합니다. 기본 템플릿은 [assets/templates/.gitignore-harness](assets/templates/.gitignore-harness)에 있습니다.

## healthy는 무엇인가

하네스는 아래 조건이 모두 맞을 때 healthy라고 봅니다.

- 관리 파일이 모두 존재한다
- `PROJECT_HARNESS.md`와 `harness-state.json`이 같은 계약을 가리킨다
- 엔트리 파일 세 개가 얇고 같은 계약 요약을 반영한다
- 상태 불변식이 깨지지 않았다
- sync metadata가 healthy 상태를 명시한다

자세한 기준은 [assets/healthy-checklist.md](assets/healthy-checklist.md)에 정리되어 있습니다.

## fixture 검증

모든 fixture 시나리오의 구조적 유효성을 확인하려면 아래 명령을 실행합니다.

```text
python tools/validate-fixtures.py
```

상태 불변식, 템플릿 스키마 일치 여부, run-mode 일관성을 자동으로 검사합니다.

## 더 보고 싶다면

조금 더 자세한 자료는 아래 문서에 나뉘어 있습니다.

- 포지셔닝: [docs/positioning.md](docs/positioning.md)
- 공존 원칙: [docs/coexistence.md](docs/coexistence.md)
- fixture: [assets/fixtures](assets/fixtures)
- fixture 검증기: [tools/validate-fixtures.py](tools/validate-fixtures.py)
- sample output: [assets/examples](assets/examples)
- repair playbook: [assets/repair-playbook.md](assets/repair-playbook.md)
- healthy checklist: [assets/healthy-checklist.md](assets/healthy-checklist.md)
- gitignore 템플릿: [assets/templates/.gitignore-harness](assets/templates/.gitignore-harness)

처음 감을 잡을 때는 아래 예시 두 개를 먼저 보는 걸 추천합니다.

- healthy 예시: [assets/examples/legacy-webapp-healthy.md](assets/examples/legacy-webapp-healthy.md)
- before/after 예시: [assets/examples/legacy-webapp-before-after.md](assets/examples/legacy-webapp-before-after.md)

## 사용 예시

```text
/make-harness
```

```text
Use the make-harness skill to set up a harness for this repository.
```
