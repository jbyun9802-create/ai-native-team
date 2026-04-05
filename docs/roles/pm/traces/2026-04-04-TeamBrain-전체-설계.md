---
date: 2026-04-04
type: trace
role: pm
topic: TeamBrain 프로덕트 전체 설계 — 문제 정의부터 프로토타입 배포까지
project: ai-native-team
tags: [TeamBrain, PRD, assessment, 6축유형, 프레임워크, 프로토타입, Vercel, Claude API, 오픈소스]
---

# TeamBrain 프로덕트 전체 설계 — 문제 정의부터 프로토타입 배포까지

## 날짜
2026-04-04

## 목적
AI 협업 룰을 도출하는 오픈소스 프로덕트(TeamBrain)를 구상하고, PRD 작성 → 테스트 설계 → 유형 체계 → 프로토타입 개발 → Vercel 배포까지 하루 만에 진행

## 핵심 내용

### 제품 방향의 진화 과정

1. **초기 구상**: CLI 커맨드(interview/synthesize/generate-claude/handoff) + 대시보드(뇌구조/타임라인) 전부를 하나의 프로덕트로
2. **1차 축소**: 너무 복잡 → "Assessment만"으로 축소. 뇌구조/타임라인은 PRD-2로 분리
3. **2차 축소**: 시나리오 Phase 제거, 강제 선택 60쌍이 유형 측정의 전부
4. **3차 결정**: GitHub 연동 제거 → zip 다운로드, 무료 서비스, Supabase+Resend+Claude API

### 최종 확정된 제품 구조

**TeamBrain Assessment (PRD)**:
- 테스트 20분 (프로파일 3문항 + AI 리터러시 ~25문항 + 강제 선택 60쌍)
- 6축 유형 체계: AI 협업 4축(S/A, D/G, T/E, C/L) + 팀 협업 2축(E/I, F/B)
- AI 리터러시 5레벨 (입문→활용→숙련→시스템설계→아키텍트)
- 개인 리포트 (Claude API 생성, MBTI급 수 페이지) + {이름}.md (STOP/THINK 사고 강제)
- 팀 리포트 (모든 페어 마찰 분석 + 파이프라인 + 인풋아웃풋)
- 출력: zip 다운로드 (개인) / 이메일 전송 (팀)

**TeamBrain Viz (PRD-2)**: 별도 프로덕트. traces → brain.py CLI 도구.

### 생성된 산출물

| 파일 | 내용 |
|------|------|
| `docs/shared/product/prd/PRD.md` | Assessment 프로덕트 PRD (최종) |
| `docs/shared/product/prd/PRD-2.md` | Viz 프로덕트 PRD (brain.py) |
| `docs/shared/product/specs/assessment-questions.md` | 질문 구성 + 출력 구조 + 리포트 구조 + 유저플로우 + 인프라 + 개발자용 변환 로직 (Part 1~7) |
| `docs/shared/product/specs/frameworks/*.md` | 5개 직무별 사고 프레임워크 (PM/Eng/Design/UXR/Growth) |
| `prototype/assessment.html` | 프로토타입 (60쌍 + Claude API 리포트) |
| `prototype/api/generate.js` | Vercel serverless Claude API 프록시 |

## 결정사항

| # | 결정 | 이유 |
|---|------|------|
| 1 | 4레이어 문제 구조 | 게을러짐→룰부재→reasoning유실→조직뇌부재 |
| 2 | Assessment + Viz 분리 | 한 프로덕트에 너무 많으면 설명 불가 |
| 3 | MBTI급 인적성검사 설계 | 강제 선택 쌍이 게이밍 방지에 최적 |
| 4 | 6축 유형 체계 | AI 특화 4축 + 팀 협업 2축 |
| 5 | STOP/THINK만 (AUTO 제거) | 사고 강제가 목적 |
| 6 | GitHub 연동 제거 → zip | 보안, 복잡도. zip이 단순 |
| 7 | 무료 서비스 | 100명 써도 ~12,000원 |
| 8 | 직무별 사고 프레임워크 | {이름}.md 품질의 핵심 |
| 9 | Claude API 2회 분리 호출 | Vercel 타임아웃 방지 |

## 인사이트

- "단순화 ≠ 내용 줄이기". 채널을 줄이고 리포트 깊이를 높이는 것이 정답
- 프로토타입을 빨리 만들어서 직접 써봐야 문제가 보인다
- {이름}.md의 핵심은 "사고 강제" — 역할별 일잘러 사고과정을 STOP/THINK 룰로 번역
- 리포트 품질은 질문 수가 아니라 Claude API 프롬프트 깊이 + 사고 프레임워크 레퍼런스에서 나옴
- 제품 방향이 하루에 3번 바뀌었지만, 매번 더 단순하고 명확해졌음

## 다른 팀원이 알아야 할 것

1. **PRD 확정** — `docs/shared/product/prd/PRD.md` (Assessment), `PRD-2.md` (Viz)
2. **직무별 사고 프레임워크 리뷰 필요** — 각자 `frameworks/{role}-thinking.md` 수정
3. **프로토타입 Vercel 배포됨** — URL로 테스트 가능
4. **개발 스펙 완성** — `assessment-questions.md` Part 7에 바로 구현 가능한 상세 로직
