# Mock Interview: junior developer

This example shows how the same `make-harness` one-time setup can stay friendly for a junior developer.

Goal:
- keep the questions practical
- avoid forcing immediate architectural certainty
- offer safe defaults when the user is unsure
- keep the interaction 부담 없이 진행되도록 한다

Context:
- blank project
- no existing code to inspect
- the developer knows the rough product idea, but not every stack decision yet
- this follows the setup-discovery path rather than a repo-first confirmation path

## Transcript

Agent: 이건 one-time setup이라서 처음 규칙만 잘 잡아두면 돼. 잘 모르겠으면 내가 무난한 기본값을 먼저 제안할게.

Agent: 기본 협업 언어는 한국어로 갈까, 영어로 갈까? 잘 모르겠으면 내가 한국어를 기본값으로 둘 수도 있어.
User: 한국어로 해줘.

Agent: 이번 프로젝트는 웹앱, 백엔드 서비스, 라이브러리 중 어디에 가까워? 잘 모르겠으면 내가 가장 가까운 기본값을 먼저 제안할게.
User: 웹앱이요.

Agent: 런타임은 Node, Bun, Python 중 어떤 쪽으로 갈까? 잘 모르겠으면 가장 무난한 기본값부터 잡아도 돼.
User: 잘 모르겠어요.

Agent: 그럼 우선은 Node를 기본값으로 둘게. 나중에 바꾸고 싶으면 다시 수정할 수 있어.
User: 좋아요.

Agent: 패키지 매니저는 npm, pnpm, yarn 중 뭐로 갈까? 아직 취향이 없으면 내가 무난한 기본값을 먼저 제안할게.
User: 이것도 잘 모르겠어요.

Agent: 그럼 npm으로 먼저 둘게. 가장 익숙한 기본값이라 시작하기 편해.
User: 네.

Agent: 초기 기준으로는 테스트/린트까지 통과하면 완료로 볼까? 잘 모르겠으면 이걸 기본값으로 둘게.
User: 일단 그렇게 해주세요.

Agent: 좋아. 지금은 무난한 기본값으로 잡고, 나중에 프로젝트가 커지면 더 촘촘하게 바꿔도 돼.

## Why this is good for juniors

- 어려운 결정을 바로 강요하지 않는다
- 잘 모르겠다는 답이 허용된다
- 기본값 제안이 포함되어 있다
- 질문이 스킬의 내부 schema를 직접 드러내지 않는다
- one-time setup이라는 맥락을 먼저 알려줘 부담을 줄인다

## Important note

This is still the same harness philosophy as the senior path.
Only the depth and pressure of the questions change, not the contract model itself.
