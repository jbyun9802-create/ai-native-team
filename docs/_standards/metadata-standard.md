---
date: 2026-03-15
type: guide
role: all
topic: 문서 메타데이터 표준
project: ai-native-team
---

# 문서 메타데이터 표준

모든 .md 문서 최상단에 아래 형식의 메타데이터를 붙입니다.
이 메타데이터가 있어야 나중에 AI가 "3월에 PM이 한 결정만 찾아줘" 같은 검색을 할 수 있습니다.

## 형식

```yaml
---
date: 2026-03-15
type: meeting | trace | decision | product | raw-transcript | raw-chat | research | spec | role-overview | guide
role: pm | engineering | design | uxr | gtm | all
participants: [Robin, 건희, 우석, 아롬]
topic: 문제 선정
project: ai-native-team
tags: [mvp, 투표, 문제정의]
---
```

## 각 필드 설명

| 필드 | 필수 | 설명 |
|------|------|------|
| date | ✅ | 작성일 (YYYY-MM-DD) |
| type | ✅ | 문서 종류 (아래 목록 참고) |
| role | ✅ | 작성자 역할 또는 `all` |
| participants | 미팅만 | 참여자 이름 |
| topic | ✅ | 한 줄 요약 (검색 키워드 역할) |
| project | ✅ | 프로젝트 이름 |
| tags | 선택 | 자유 태그 (나중에 연관 문서 찾기용) |
| category | product만 | `prd` / `spec` / `storybook` / `research` / `validation` |
| status | spec만 | `draft` / `review` / `approved` / `deprecated` |
| method | research만 | `interview` / `survey` / `usability-test` / `competitive-analysis` |
| participant-count | research만 | 리서치 대상 인원 수 |
| supersedes | 선택 | 이 문서가 대체하는 이전 문서 경로 |

## type 종류

| type | 언제 쓰나 | 예시 |
|------|-----------|------|
| `meeting` | 미팅 정리본 | 문제 선정 회의록 |
| `trace` | 개인 사고 기록 | /save로 저장한 작업 기록 |
| `decision` | 중요 의사결정 | 기술 스택 선정, 방향 전환 |
| `product` | 프로덕트 문서 | 문제 분석, PRD, 스펙 |
| `raw-transcript` | 미팅 트랜스크립트 원문 | Fireflies에서 자동 저장된 파일 |
| `raw-chat` | 채팅 원문 | 슬랙/카톡 내보내기 |
| `research` | UX 리서치 산출물 | 인터뷰 노트, 설문 결과, 사용성 테스트 |
| `spec` | 구현 명세 (살아있는 문서) | API 스펙, 인터랙션 스펙, 데이터 모델 |
| `role-overview` | 역할 정의 | 각 역할별 README |
| `guide` | 가이드/템플릿 | 미팅 기록 가이드, trace 템플릿 |

## 예시: 미팅 기록

```markdown
---
date: 2026-03-14
type: meeting
role: all
participants: [Robin, 건희, 우석, 아롬]
topic: 문제 선정 및 MVP 스코프 정의
project: ai-native-team
tags: [mvp, 투표, 문제정의, 핸드오프]
---

# 문제 선정 및 분석
...
```

## 예시: 개인 trace

```markdown
---
date: 2026-03-15
type: trace
role: pm
topic: /save 슬래시 커맨드 설계
project: ai-native-team
tags: [자동화, 슬래시커맨드, 작업기록]
---

# 팀 작업 기록 시스템 설계
...
```

## 예시: Fireflies 자동 저장 (raw-transcript)

```markdown
---
date: 2026-03-15
type: raw-transcript
role: all
participants: [Robin, 건희]
topic: 스프린트 리뷰
project: ai-native-team
source: fireflies
tags: [스프린트, 리뷰]
---

(트랜스크립트 원문 전체)
```

## 예시: UX 리서치

```markdown
---
date: 2026-03-20
type: research
role: uxr
topic: 팀원 인터뷰 - 핸드오프 고통점 검증
project: ai-native-team
method: interview
participant-count: 4
tags: [인터뷰, 핸드오프, 검증]
---

# 팀원 인터뷰 결과
...
```

## 예시: 구현 명세 (spec)

```markdown
---
date: 2026-04-01
type: spec
role: engineering
topic: /save API 엔드포인트 명세
project: ai-native-team
status: draft
tags: [api, save, 핸드오프]
---

# /save API 명세
...
```

## 예시: 문서 업데이트 (supersedes)

```markdown
---
date: 2026-04-15
type: product
role: pm
topic: 문제 분석 v2 - 인터뷰 결과 반영
project: ai-native-team
supersedes: docs/product/problem-analysis.md
tags: [문제분석, v2, 인터뷰반영]
---
```

→ AI가 "최신 문제 분석 문서 찾아줘" 할 때 supersedes를 보고 최신 버전을 찾음

## 왜 이게 중요한가

메타데이터 없이 문서만 쌓으면 → AI가 **모든 문서를 다 읽어야** 답을 찾음 (느리고 비쌈)
메타데이터가 있으면 → AI가 **필요한 문서만 골라서** 읽음 (빠르고 정확함)

이것이 RAG의 성능을 결정하는 가장 기본적인 요소입니다.
