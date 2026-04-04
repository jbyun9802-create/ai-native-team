# AI-Native Team Project

## 이 레포지토리는

이 레포지토리는 우리 팀의 **지식과 의사결정을 저장하는 곳**이자, **프로덕트 코드를 관리하는 곳**입니다.

- 팀의 모든 지식, 맥락, 의사결정 근거를 Git에 기록합니다
- 각 팀원의 AI 에이전트가 이 레포를 참조하여 팀의 컨텍스트를 공유합니다
- 프로덕트 코드도 함께 관리됩니다

---

## 웨비나

### 목적

AI-native하게 일하는 팀이 어디까지 가능한지 보여줍니다. AI를 단순한 도구가 아닌 팀 워크플로우의 핵심으로 통합했을 때, 팀이 어떤 수준까지 도달할 수 있는지를 시연합니다.

### 타겟 오디언스

AI를 현업에 더 잘 활용하고 싶은 모든 사람. 테크에 익숙한 실무자부터 AI에 덜 익숙한 임원/관리자까지.

### 노스스타

> "AI로 일하는 팀은 이렇게까지 가능하다"

---

## 프로덕트

### 목적

우리 팀이 직접 겪고 있는 문제를 해결하기 위한 제품을 만듭니다.

### 문제 정의

> "개인이 AI를 쓰는 방법은 알지만, AI가 만든 것을 어떻게 다음으로 넘길지를 설계하는 방법을 모른다. 팀원들이 각자 AI와 대화하는데 그 컨텍스트가 개인 채팅창에서 사라진다. 저 사람의 고민이 뭔지, 우선순위가 뭔지, 왜 저런 선택을 했는지 모르겠다."

### 타겟

우리 팀, 그리고 비슷한 문제를 겪고 있는 AI-native 팀들.

### 상세 문서

- [문제 분석 및 우선순위](docs/shared/product/planning/problem-analysis.md)
- [팀 워크플로우 & MVP 다이어그램](docs/shared/product/diagrams/team-workflow.html)

---

## 레포지토리 구조

```
ai-native-team/
├── README.md
├── docs/
│   ├── _standards/          # 팀 공통 표준/템플릿
│   │   ├── metadata-standard.md
│   │   └── TEMPLATE-trace.md
│   ├── shared/              # 팀 전체 공유 문서
│   │   ├── announcements/   # 팀 공지
│   │   ├── meetings/        # 미팅 기록 (원문 + 요약)
│   │   │   └── YYYY-MM-DD-주제/
│   │   │       ├── raw-chat.txt
│   │   │       ├── raw-transcript.txt
│   │   │       └── summary.md
│   │   └── product/         # 프로덕트 문서 (단계별)
│   │       ├── planning/    # 기획: PRD, 문제 분석
│   │       ├── design/      # 디자인: 와이어프레임, 목업
│   │       ├── specs/       # 개발 명세: API, 데이터 모델
│   │       ├── validation/  # 검증: 테스트, 피드백
│   │       └── diagrams/    # 다이어그램
│   └── roles/               # 롤별 개인 작업 공간
│       ├── pm/
│       ├── engineering/
│       ├── design/
│       ├── uxr/
│       └── gtm/
└── src/                     # 프로덕트 코드 (추후)
```

## 미팅 기록

미팅 원문(채팅, 트랜스크립트)을 그대로 보관합니다. → [가이드](docs/shared/meetings/README.md)

- [킥오프 (2/16)](docs/shared/meetings/2026-02-16-kickoff/)
- [워크플로우 논의 (2/17)](docs/shared/meetings/2026-02-17-workflow-discussion/)
- [문제 선정 (3/14)](docs/shared/meetings/2026-03-14-problem-selection/)
- [현재 세션 (3/14)](docs/shared/meetings/2026-03-14-current-session/)

## 팀 멤버

- **Robin** - PM/GTM, Bridgeleaf (뉴욕, 미국)
- **김건희** - 엔지니어링, 투스텝스어헤드 (서울, 한국)
- **dddesign (우석)** - 디자인, Data Driven Design Agency (서울, 한국)
- **Ahrom Kim** - UX 리서치, Healthcare Company (미국)
