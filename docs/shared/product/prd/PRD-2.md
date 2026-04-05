---
date: 2026-04-04
type: product
role: pm
topic: PRD-2 — TeamBrain Viz (팀 멘탈 모델 시각화)
project: ai-native-team
tags: [PRD, 멘탈모델, traces, 시각화, brain.py, CLI]
phase: planning
status: draft
---

# TeamBrain Viz — PRD-2

| 항목 | 내용 |
|------|------|
| 제품명 | TeamBrain Viz |
| 한 줄 요약 | /save로 쌓인 traces를 읽어서 팀원별 사고 흐름을 터미널에서 바로 보여주는 도구 |
| 상태 | Draft → 프로토타입 완료 |
| 선행 조건 | PRD의 Assessment + /save 커맨드가 작동해야 함 |

---

## 관계

```
PRD (Assessment)              PRD-2 (Viz)
─────────────────             ─────────────────
테스트 → 리포트 → CLAUDE.md    traces → 팀 멘탈 모델
                              
Layer 1+2 해결                 Layer 3+4 해결
(사고 강제 + 룰 도출)          (reasoning 보존 + 조직의 뇌)

Assessment가 만드는 것          Viz가 만드는 것
  zip: CLAUDE.md, {이름}.md      zip에 포함: brain.py, /save
  → 사고를 강제하는 룰            → 사고를 기록하고 시각화
```

---

## Problem (PRD-2가 해결하는 것)

### Layer 3. Reasoning이 유실된다

다음 사람에게 넘기는 순간 "왜 이렇게 했는지"가 사라진다.
- UXR → PM: 인터뷰 뉘앙스, 맥락 유실
- PM → Design: 전략적 의도, 제약 조건 유실
- Design → Eng: 기각된 옵션, 판단 레이어 유실

### Layer 4. 조직의 뇌를 볼 수 없다

팀 전체가 지금 무슨 생각을 하고 있는지, 누가 어떤 영역을 담당하는지, 어디가 사각지대인지를 볼 수 없다.

---

## Solution

### 핵심 결정: 대시보드가 아니라 CLI

처음에는 3D 뇌 구조 시각화, 브라우저 대시보드 등을 검토했으나, 핵심 니즈를 다시 보면:

> "이 사람이 무슨 생각을 주로 하면서 살고, 어떤 사고 과정을 거쳐 지금에 왔는지"

이걸 보려면 fancy한 온톨로지가 아니라 **traces 데이터를 바로 읽어서 보여주는 것**이 본질이다.

**결정:**
- 별도 대시보드 대신 **CLI 도구 (brain.py)**
- team.zip에 포함되어 배포
- /save 커맨드와 직접 연동 — 추가 설정 없음
- `pip install rich` 하나로 설치 완료

### 아키텍처

```
/save 커맨드                    brain.py
────────────                   ─────────
작업 후 3개 질문 →              traces 파일 자동 감지 →
docs/roles/{역할}/traces/       역할별 사고 흐름 표시
  {날짜}-{주제}.md              
                               "지금 머릿속" (최근 traces의 topic + insight)
YAML frontmatter               "사고 흐름" (전체 타임라인)
  date, type, role, topic       meetings도 함께 표시
  tags                         
                               기간 필터: 1일 / 7일 / 30일 / 전체
```

---

## 핵심 기능

### 1. /save 커맨드 (기존)

작업 후 3개 질문: 뭘 결정했어? / 거의 할 뻔한 다른 방법은? / 확신 못하는 부분은?
→ `docs/roles/{역할}/traces/{날짜}-{주제}.md`로 저장

### 2. brain.py — 팀 멘탈 모델 뷰어

**두 가지 뷰:**

**View 1 — "지금 머릿속" (사람 중심)**
- 역할별 최근 traces의 topic + insight를 자연어로 표시
- 가장 최근 것이 강조
- 기간 선택: 1일 / 7일 / 30일 / 전체 (CLI 인자)

**View 2 — "사고 흐름" (시간 중심)**
- 전체 타임라인, 날짜별 그룹
- traces + meetings 함께 표시
- 각 항목: topic, insight, decision, 파일 경로

**사용법:**
```bash
python tools/brain.py              # 전체 팀 (최근 30일)
python tools/brain.py pm           # PM의 사고 흐름
python tools/brain.py uxr 7        # UXR 최근 7일
python tools/brain.py engineering 0 # Eng 전체 기간
```

### 3. team.zip 배포

Assessment 완료 후 오너가 받는 team.zip:

```
team.zip/
  .claude/
    CLAUDE.md                   ← 팀 룰
    {이름}.md × 전원             ← 개인 사고 강제 룰
    commands/
      save.md                   ← traces 생성 커맨드
  tools/
    brain.py                    ← 팀 멘탈 모델 뷰어
    README.md                   ← 설치 안내 (pip install rich)
  reports/
    team-report.md              ← 팀 리포트
    {이름}-report.md × 전원      ← 개인 리포트
```

오너가 zip 풀어서 프로젝트 루트에 넣고 git push → 끝.
팀원들은 /save로 기록하고, brain.py로 팀 상태를 본다.

---

## 기각된 방향

| 방향 | 기각 이유 |
|------|----------|
| 3D 뇌 구조 시각화 (Three.js) | 멋있지만 "매일 열어서 상황 파악하는 도구"로는 과함 |
| 브라우저 대시보드 | 별도 앱을 열어야 해서 마찰 큼. CLI가 작업 흐름에 더 가까움 |
| 태그 기반 Focus Areas | 메타데이터 태깅이 부실하면 의미 없는 결과. topic/insight 자연어가 더 정확 |
| Textual TUI (인터랙티브) | 터미널 호환성 문제. 정적 출력이 더 안정적이고 어디서나 동작 |
| 토픽 중심 뷰 | traces 수가 적을 때는 사람 중심 + 시간 중심이 더 유용 |

---

## 기술 스택

- **Python 3.10+**
- **rich** — 터미널 포매팅 (유일한 의존성)
- YAML frontmatter 파싱은 자체 구현 (외부 의존성 없음)
- /save 커맨드가 생성하는 파일 형식과 100% 호환

---

## 향후 확장 (지금은 안 함)

- **"다음에 할 것" 필드**: /save에 질문 하나 추가 → 예정 작업 표시
- **브라우저 시각화**: traces가 충분히 쌓이면 3D/2D 대시보드 의미 있음
- **Claude API 연동**: traces를 AI가 요약 → "이번 주 팀 요약" 자동 생성
- **사각지대 감지**: 역할 간 traces 겹침/빈 곳 자동 경고

---

## 참고

- 프로토타입: `prototype/brain.py` (작동 확인 완료)
- /save 커맨드: `.claude/commands/save.md`
- traces 템플릿: `docs/_standards/TEMPLATE-trace.md`
- 기존 traces: `docs/roles/pm/traces/`, `docs/roles/uxr/traces/`
