---
date: 2026-04-04
type: trace
role: pm
topic: TeamBrain PRD 설계 — 문제 정의부터 Assessment 프로덕트 확정까지
project: ai-native-team
tags: [TeamBrain, PRD, assessment, 인적성검사, 6축유형, CLAUDE.md, 오픈소스]
---

# TeamBrain PRD 설계 — 문제 정의부터 Assessment 프로덕트 확정까지

## 날짜
2026-04-04

## 목적
AI 협업 룰을 도출하는 프로덕트(TeamBrain)의 PRD를 작성하고, 여러 차례 피드백을 거쳐 제품 스코프/구조/질문 설계/출력물/아키텍처를 확정

## 핵심 내용

1. **문제 4레이어 정의**: 게을러짐 → 사고 룰 부재 → reasoning 유실 → 조직 뇌 부재. 이 중 L1+L2를 이 프로덕트가 해결, L3+L4는 PRD-2(별도 프로덕트)

2. **제품 스코프 대전환**: 처음에는 CLI 커맨드(interview/synthesize/generate-claude/handoff) + 대시보드(뇌구조/타임라인) 전체를 하나의 프로덕트로 기획 → 너무 복잡해서 "Assessment만"으로 축소. 뇌구조/타임라인/traces 시각화는 PRD-2로 분리

3. **AI 협업 인적성검사 설계**: MBTI/CliftonStrengths/DISC/OPQ 레퍼런스 연구 후, 6축 유형 체계 확정:
   - 축 1-4: AI 협업 (판단기점 S/A, 협업깊이 D/G, AI이해도 T/E, 품질관여 C/L)
   - 축 5-6: 팀 협업 (소통스타일 E/I, 갈등대처 F/B)
   - 강제 선택 60쌍 전문 완성 + AI 리터러시 직무별 경험 체크(PM/Eng/Design/UXR/Growth)

4. **출력물 확정**: {이름}.md (STOP/THINK 사고 강제 룰) + CLAUDE.md (팀 룰) + 리포트 → zip 다운로드/이메일

5. **아키텍처 확정**: 무료 서비스 / GitHub 연동 없음 / zip 다운 방식 / Supabase(임시저장+매직링크) + Resend(이메일) + JSZip + Claude API(1인당 ~120원)

6. **유저 플로우 확정**: 개인(접속→로그인→테스트20분→zip다운) + 팀(오너 초대→전원 완료→오너에게 zip 이메일)

## 결정사항

| 결정 | 이유 |
|------|------|
| 뇌구조/타임라인을 PRD-2로 분리 | 하나의 프로덕트에 너무 많음. PM이 팀에 설명 불가 |
| 시나리오 Phase 제거, 강제 선택 60쌍만 | 시나리오는 "정답"이 보임. 강제 선택이 게이밍 방지에 우월 |
| GitHub 연동 제거 → zip 다운로드 | 보안 문제(write 권한), 복잡도. zip이 훨씬 단순 |
| 무료 서비스 (우리가 API 비용 부담) | 100명 써도 ~12,000원. 진입 장벽 제거가 더 중요 |
| 매직 링크 로그인 | 비밀번호 없이 이메일만. Supabase Auth 무료 |
| STOP/THINK만 (AUTO 제거) | AUTO는 불명확. 사고 강제가 목적이면 STOP/THINK만 필요 |
| me.md → {이름}.md | 팀 전원의 파일이 같은 폴더에 있으니 이름으로 구분 |
| commands/ 폴더 제거 | 사고 룰은 전부 {이름}.md에 포함 |

## 인사이트

- "단순화 ≠ 내용 줄이기". 채널을 줄이고 리포트 깊이를 높이는 것이 정답
- MBTI가 93문항인데 강제 선택 쌍이라 게이밍이 어려움 — 이 구조를 그대로 가져감
- 리포트 퀄리티는 질문 수가 아니라 Claude API 프롬프트의 깊이에서 나옴
- {이름}.md의 핵심은 "사고 강제" — STOP(멈추고 사고 요구)과 THINK(단계별 안내)

## 다른 팀원이 알아야 할 것

PRD가 대폭 변경됨. 핵심 변경:
- **제품이 "Assessment"로 축소** — 테스트 → 리포트 → md 파일 생성이 전부
- **뇌구조/타임라인은 PRD-2로 분리**
- **6축 유형 체계 신설** (MBTI식 AI 협업 인적성)
- **GitHub 연동 없음** — zip 다운로드 방식
- **무료 서비스**
- 질문 구성 상세: `docs/shared/product/specs/assessment-questions.md`
