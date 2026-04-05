---
date: 2026-04-04
type: guide
role: all
topic: 신규 멤버 온보딩 가이드
project: ai-native-team
tags: [onboarding, guide, 온보딩]
---

# 온보딩 가이드

처음 이 레포에 들어온 분을 위한 안내입니다. 아래 순서대로 읽고, 프로토타입을 직접 써보세요.

---

## 1. 먼저 읽어야 할 문서 (순서대로)

### Step 1: 프로젝트 전체 그림

| 순서 | 문서 | 내용 | 소요 |
|------|------|------|------|
| 1 | [README.md](../../README.md) | 레포 목적, 폴더 구조, 팀 멤버 | 3분 |
| 2 | [PRD.md](product/prd/PRD.md) | 우리가 만드는 제품 (TeamBrain Assessment) — 문제 정의, 솔루션 | 10분 |
| 3 | [PRD-2.md](product/prd/PRD-2.md) | 두 번째 제품 (TeamBrain Viz) — traces 기반 팀 멘탈 모델 뷰어 | 5분 |

### Step 2: 제품 스펙

| 순서 | 문서 | 내용 |
|------|------|------|
| 4 | [assessment-questions.md](product/specs/assessment-questions.md) | Assessment 질문 구성, 측정 축, 출력 구조 명세 |
| 5 | [product/README.md](product/README.md) | Product 폴더 구조 — 어떤 문서를 어디에 넣는지 |

### Step 3: 맥락 파악 (선택)

더 깊은 맥락이 필요하면:

- [문제 분석](product/prd/problem-analysis.md) — 문제 선정 과정과 우선순위
- [UXR 교차 분석](../roles/uxr/analysis/2026-03-25-cross-interview-analysis.md) — 4인 인터뷰에서 나온 인사이트
- [킥오프 미팅](meetings/2026-02-16-kickoff/summary.md) — 프로젝트 시작점

---

## 2. 프로토타입 써보기

현재 두 가지 프로토타입이 있습니다.

### Prototype A: TeamBrain Assessment (웹)

**팀원의 AI 협업 방식을 진단하는 테스트입니다.**

Vercel에 배포되어 있습니다: **https://ai-native-team.vercel.app**

**체험 방법:**
1. URL 접속
2. 이름, 역할, 시니어리티 입력
3. AI 리터러시 체크 (약 25문항)
4. 강제 선택 60쌍 (핵심 파트 — 두 선택지 중 하나를 고르는 방식)
5. 완료 후 Claude API가 개인 리포트 생성
6. zip 다운로드 (리포트 + {이름}.md 파일 포함)

**소요 시간:** 약 10분

**로컬에서 돌리고 싶다면:**
```bash
cd prototype
npm install
# .env 파일에 ANTHROPIC_API_KEY 설정 필요
echo "ANTHROPIC_API_KEY=your-key-here" > .env
npm start
# http://localhost:3001 접속
```

> 참고: Claude API 호출이 포함되어 있어 API 키가 없으면 리포트 생성 단계가 작동하지 않습니다. 배포된 URL로 테스트하는 것을 권장합니다.

### Prototype B: TeamBrain TUI (터미널)

**팀원들의 traces(사고 기록)를 터미널에서 시각화하는 도구입니다.**

```bash
# 의존성 설치
pip install textual rich anthropic

# 실행 (레포 루트에서)
python prototype/brain-tui.py

# 또는 특정 레포 경로 지정
python prototype/brain-tui.py --repo /path/to/repo
```

**조작법:**
- 터미널에서 역할별 사고 흐름(traces)을 탐색
- 기간 필터: 1일 / 7일 / 30일 / 전체
- `docs/roles/*/traces/` 폴더의 기존 traces 데이터를 읽어서 표시

> 참고: Python 3.10+ 필요. `textual`, `rich`, `anthropic` 라이브러리가 설치되어야 합니다. API 키 없이도 기본 기능은 작동하지만, 시맨틱 검색과 사고 에너지 분석에는 `ANTHROPIC_API_KEY`가 필요합니다.

---

## 3. 도구 설치

### GitHub CLI (필수)

이슈 등록 커맨드(`/bug`, `/question`, `/feedback`)를 사용하려면 GitHub CLI가 필요합니다.

```bash
# 설치
# Mac: brew install gh
# Windows: winget install GitHub.cli

# 인증 (한 번만)
gh auth login
# → GitHub.com 선택 → HTTPS → 브라우저로 인증
```

### Claude Code

AI 대화 후 사고 기록 저장(`/save`)과 이슈 등록에 사용합니다.
설치: https://claude.ai/code

---

## 4. 의견 남기는 방법

### 슬래시 커맨드로 GitHub 이슈 등록 (권장)

Claude Code에서 다음 커맨드를 사용하면 바로 GitHub 이슈가 생성됩니다:

| 커맨드 | 용도 | 예시 |
|--------|------|------|
| `/bug` | 버그 리포트 | `/bug 프로토타입에서 리포트 생성 안 됨` |
| `/question` | 질문 | `/question traces 파일 형식이 궁금합니다` |
| `/feedback` | 피드백/제안 | `/feedback 온보딩 문서에 TUI 조작법 더 필요` |

각 이슈에는 타입 라벨(`bug`/`question`/`feedback`) + 역할 라벨(`pm`/`engineering`/`design`/`uxr`/`gtm`)이 자동으로 붙습니다.

### 사고 기록 저장

AI와 대화 후 의미 있는 사고 과정이 있었다면:

```
/save
```

역할별 사고 프레임워크에 맞춰 체크하고, 구조화된 trace 파일을 `docs/roles/{역할}/traces/`에 저장합니다.

### 팀 채널

빠른 논의가 필요하면 슬랙에서 직접 대화.

---

## 5. 폴더 구조 요약

```
ai-native-team/
├── README.md                    ← 시작점
├── docs/
│   ├── shared/                  ← 팀 전체 공유 문서
│   │   ├── meetings/            ← 미팅 기록
│   │   ├── product/             ← PRD, 스펙, 리서치 등
│   │   └── onboarding.md        ← 이 문서
│   └── roles/                   ← 롤별 개인 작업 공간
│       ├── pm/traces/           ← PM 사고 기록
│       ├── engineering/         ← 엔지니어링
│       ├── design/              ← 디자인
│       ├── uxr/                 ← UX 리서치
│       └── gtm/                 ← GTM
├── prototype/                   ← MVP 프로토타입 코드
│   ├── assessment.html          ← Assessment 웹 UI
│   ├── brain-tui.py             ← TUI 뷰어
│   ├── server.js                ← 로컬 서버 (API 프록시)
│   ├── api/generate.js          ← Vercel serverless function
│   └── package.json
└── .claude/commands/            ← 슬래시 커맨드
    ├── save.md                  ← /save (사고 기록 저장)
    ├── bug.md                   ← /bug (버그 이슈)
    ├── question.md              ← /question (질문 이슈)
    └── feedback.md              ← /feedback (피드백 이슈)
```

---

## 6. 작업 시작 전 체크리스트

- [ ] README.md 읽음
- [ ] PRD, PRD-2 읽음
- [ ] Assessment 프로토타입 직접 테스트 완료
- [ ] TUI 프로토타입 로컬에서 실행해봄
- [ ] 자신의 역할 폴더(`docs/roles/{역할}/`) 확인
- [ ] GitHub CLI 설치 및 인증 (`gh auth login`)
- [ ] 궁금한 점이나 첫인상은 `/bug`, `/question`, `/feedback`으로 이슈 등록
