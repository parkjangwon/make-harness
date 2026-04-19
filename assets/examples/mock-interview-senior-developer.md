# Mock Interview: senior developer

This example shows how the same `make-harness` one-time setup can stay precise for a senior developer without changing the underlying philosophy.

Goal:
- confirm durable rules quickly
- allow explicit overrides instead of forcing defaults
- keep the interview compact while preserving precision

Context:
- existing repository
- package scripts and code structure already exist
- the developer wants precise control over approval and definition of done
- this follows the repo-first path, where the agent confirms only what code cannot settle

## Transcript

Agent: 이건 one-time setup이야. 먼저 repo를 살펴봤고, 코드만으로 안 정해지는 durable rule만 짧게 확인할게.

Agent: 지금 구조를 보면 이 프로젝트는 웹앱으로 보면 될까?
User: 네. 다만 관리자 대시보드와 공개 사이트가 같이 있어요.

Agent: 좋아. 그럼 `webapp`을 기본 타입으로 두고, 굳이 새 카테고리를 만들지 말고 메모로만 남길게.

Agent: README와 설정을 보면 기본 검증은 `pnpm test`로 잡는 게 맞아 보여. lint는 `pnpm lint`, typecheck는 `pnpm typecheck`로 같이 둘까?
User: 네. 그리고 build 기본값은 `pnpm build:prod`로 override 해주세요.

Agent: 좋아. 그 exact command들을 그대로 저장할게.

Agent: 기본 완료 기준은 `pnpm test`, `pnpm lint`, `pnpm typecheck` 통과로 둘까? 콘텐츠만 바뀌는 수정은 예외 메모를 남기는 식으로 처리할 수도 있어.
User: 맞아요. 콘텐츠만 바뀌면 수동 확인만으로도 충분하고, 코드 변경이면 저 세 개는 필요해요.

Agent: 이해했어. 기본 완료 기준은 보수적으로 저장하고, 콘텐츠 변경 예외는 note로 남길게.

Agent: 큰 변경은 먼저 확인하고, 안전한 수정은 바로 진행해도 될까? 애매하면 위험한 변경만 먼저 확인받는 기본값으로 둘 수 있어.
User: 위험한 변경만 먼저 확인받게 해주세요. 안전한 수정은 바로 진행해도 돼요.

Agent: 좋아. 그 승인 기본값과 override 메모를 함께 유지할게.

## Why this is good for seniors

- it respects repo-first inference
- it keeps defaults visible but easy to override
- it allows precise approval and definition of done rules
- it preserves exact commands like `pnpm test`
- it does not force a simplistic wizard when the developer already knows what they want

## Important note

This is the same one-time setup skill as the junior example.
The difference is that the senior path uses more precise overrides, not a different harness philosophy.
