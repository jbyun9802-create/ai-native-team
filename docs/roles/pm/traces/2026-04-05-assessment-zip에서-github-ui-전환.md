---
date: 2026-04-05
type: trace
role: pm
topic: Assessment 프로토타입 — zip 다운로드 → GitHub 레포 연동 UI 전환
project: ai-native-team
tags: [assessment, GitHub, zip제거, 프로토타입, UX, auth, .claude]
---

# Assessment 프로토타입 — zip 다운로드 → GitHub 레포 연동 UI 전환

## 날짜
2026-04-05

## 목적
4/4 미팅 결정(zip → GitHub 레포 연동)을 assessment.html 프로토타입에 반영. 팀에게 "이런 UX로 가자"를 보여주기 위한 컨셉 목업 구현.

## 핵심 내용
- `assessment.html`에서 zip 다운로드 버튼 2개(개인/팀)를 GitHub 연결 모달로 교체
- 모달: repo URL + PAT 입력 → 로딩 시뮬레이션 → `.claude/` 폴더 구조 + 커밋 URL 표시
- 실제 API 연동 없이 시뮬레이션만 — 컨셉 전달용 프로토타입
- JSZip 의존성 및 zip 관련 함수 전부 제거
- repo는 localStorage, token은 sessionStorage 저장으로 재입력 최소화

## 결정사항

| 결정 | 이유 |
|------|------|
| Auth 방식은 PAT 입력으로 프로토타입 구현 | 가장 빠르게 구현 가능. 실제 Auth 방식은 UX/개발팀이 제안하기로 함 |
| 파일 구조는 `.claude/` 폴더 | Claude Code가 자동으로 읽는 디렉토리에 맞춤 |
| 실제 API 연동 불필요 | 팀 컨셉 전달용 프로토타입일 뿐 |

## 인사이트
- Auth 방식(PAT vs OAuth Device Flow vs OAuth Web Flow)은 유저 프릭션과 구현 복잡도의 트레이드오프가 있어서 UX/개발 합의가 필요한 영역

## 다른 팀원이 알아야 할 것
- assessment.html 프로토타입이 zip → GitHub 연동 UI로 변경됨
- Auth 방식에 대한 UX/개발 제안이 필요 (PAT / OAuth Device Flow / OAuth Web Flow 3가지 옵션)
