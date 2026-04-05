---
date: 2026-04-04
type: trace
role: pm
topic: TeamBrain 프로토타입 Claude API 연동 + Vercel 배포
project: ai-native-team
tags: [TeamBrain, 프로토타입, Claude API, Vercel, 배포, serverless]
---

# TeamBrain 프로토타입 Claude API 연동 + Vercel 배포

## 날짜
2026-04-04

## 목적
프로토타입의 리포트 품질을 높이기 위해 Claude API를 연동하고, Vercel에 배포하여 팀에게 공유 가능한 URL을 확보

## 핵심 내용

1. **프로토타입 리포트 품질 문제 진단**: JavaScript 조건문 템플릿으로는 MBTI급 깊이 불가. Claude API 연동으로 결정.
2. **Vercel 배포 구조 확정**: Next.js 불필요. 정적 HTML + `api/generate.js` serverless function으로 충분. Root Directory = `prototype/`.
3. **Claude API 프록시**: `api/generate.js`가 서버사이드에서 API 호출. CORS 문제 해결. API 키는 Vercel 환경변수에 저장.
4. **리포트 생성 흐름**: 60쌍 답변 완료 → `calcScores()` → Claude API에 점수+역할+리터러시 전송 → Claude가 리포트 마크다운 + {이름}.md 동시 생성 → 화면 렌더 + zip 다운로드.
5. **배포 완료**: GitHub push 후 Vercel 배포 + 환경변수 세팅.

## 결정사항

| 결정 | 이유 |
|------|------|
| Claude API 연동 (JS 템플릿 대신) | 64가지 유형 조합에 대해 텍스트 하드코딩 불가. API가 맥락 기반 풀 리포트 생성 |
| Vercel 정적 배포 (Next.js 아닌) | 프로토타입에 과한 세팅. HTML + serverless function이면 충분 |
| .env에 API 키 저장 + .gitignore | 보안. Vercel에는 환경변수로 등록 |

## 인사이트

- 정적 HTML도 Vercel serverless function과 조합하면 API 프록시가 가능 — Next.js 없이도 서버사이드 처리 가능
- 리포트 품질의 핵심은 프롬프트 설계 — robin.md 풀 예시를 few-shot으로 포함하면 같은 수준의 depth 보장

## 다른 팀원이 알아야 할 것

TeamBrain 프로토타입이 Vercel에 배포됨. URL로 접속하면 누구나 테스트 가능.
- 60쌍 강제 선택 + AI 리터러시 체크 → Claude API가 분석 → 개인 리포트 + {이름}.md 생성 → zip 다운로드
- API 비용 우리 부담 (~120원/건)
