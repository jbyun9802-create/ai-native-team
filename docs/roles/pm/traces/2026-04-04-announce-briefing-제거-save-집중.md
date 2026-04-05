---
date: 2026-04-04
type: trace
role: pm
topic: announce/briefing 제거 — save/traces 집중
project: ai-native-team
tags: [우선순위, 스코프정리, save커맨드, traces, 슬랙]
framework_sections: ["우선순위를 정하는 방식"]
thinking_coverage: "3/4 steps"
---

# announce/briefing 제거 — save/traces 집중

## 날짜
2026-04-04

## 목적
슬랙으로 충분히 커버 가능한 announce/briefing 기능을 제거하고, `/save`와 traces 시스템에 집중

## 사고 프레임워크: 우선순위를 정하는 방식

### 사고 단계

| Step | 상태 | 내용 |
|------|------|------|
| Step 1: 반드시 달성해야 하는 한 가지 목표는? | Covered | save/traces에 집중 — 사고 과정을 구조화해서 저장하는 것이 핵심 |
| Step 2: 후보를 평가한다 | 해당 없음 | 직관적 판단 — announce/briefing은 슬랙 대비 추가 가치 없음이 명확 |
| Step 3: "안 하는 것"을 명시한다 | Covered | announce, briefing 완전 삭제. 재도입 계획 없음. 슬랙이 이미 커버 |
| Step 4: 되돌릴 수 있는가? | Covered | Two-way door — git으로 복구 가능하지만, 의도적으로 완전히 버림 |

### 사람이 확인한 것
- [x] "안 하는 것" 결정 — announce/briefing은 슬랙이 커버, 재도입 없음
- [x] 되돌림 판단 — 완전히 버리는 것으로 확정

## 결정사항
- announce, briefing 커맨드 완전 삭제 (재도입 계획 없음)
- `docs/shared/announcements/` 폴더 전체 삭제
- save.md에서 공지 관련 단계 및 "다른 팀원이 알아야 할 것" 섹션 제거
- 공지/브리핑은 슬랙에서 커버

## 인사이트
- 도구가 많다고 좋은 게 아님 — 슬랙이 이미 하는 일을 중복 구현할 필요 없음
- 이 프로젝트의 핵심 가치는 "사고 과정의 구조화된 기록(traces)"이지, 커뮤니케이션 도구가 아님
