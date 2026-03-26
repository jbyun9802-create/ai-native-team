---
date: 2026-03-25
type: role-overview
role: uxr
topic: UX 리서치 역할 정의, 폴더 구조, 운영 시스템
project: ai-native-team
---

# UX 리서치

## 담당자
- Ahrom Kim 김아롬 (헬스케어 회사, 미국)

## 역할
- 사용자 인터뷰 및 리서치
- 인사이트 도출 및 페인포인트 분석
- 사용성 테스트 및 검증
- 리서치 기반 의사결정 지원

## 핵심 관심사
- 사용자 중심 AI 통합
- AI 활용의 윤리적 고려 및 사용자 신뢰
- AI 기반 워크플로우에 맞춘 리서치 방법론

---

## 폴더 구조

```
uxr/
├── README.md                 # 이 파일
├── traces/                   # AI 대화 기록 & 의사결정
├── interviews/               # 인터뷰 세션 원본 + 노트
│   └── YYYY-MM-DD-참여자/
│       ├── raw-transcript.txt    # 트랜스크립트 원문 (가공 금지)
│       └── notes.md              # (선택) 구조화된 인터뷰 노트
├── analysis/                 # 리서치 종합 분석 & 인사이트
└── templates/                # UXR 전용 템플릿
```

---

## interviews/ 운영 규칙

### 폴더 네이밍
```
interviews/YYYY-MM-DD-참여자식별/
```
- 참여자 이름 대신 **식별 코드** 사용 (예: `P01`, `P02`, 또는 역할명 `pm-robin`)
- 같은 날 여러 인터뷰: `2026-03-25-P01/`, `2026-03-25-P02/`

### raw-transcript.txt
- 원문 그대로 붙여넣기. **절대 가공하지 않는다**
- Fireflies, Otter, Google Meet, Zoom 등 소스 무관 — 원문 보존이 원칙
- 파일 상단에 소스 표기 권장: `[Source: Fireflies]` 또는 `[Source: manual notes]`

### notes.md (선택)
인터뷰 직후 빠르게 정리하는 구조화된 노트.

```markdown
---
date: YYYY-MM-DD
type: research
role: uxr
topic: [인터뷰 주제 한 줄]
project: ai-native-team
method: interview
participant-count: 1
tags: [인터뷰, 관련태그]
---

# 인터뷰 노트 — [참여자 식별]

## 참여자 프로필
- 역할:
- AI 활용 수준:
- 주요 도구:

## 핵심 발견
- (가장 중요한 것 3개 이내)

## 주요 인용
> "원문 인용" — 맥락 설명

## 페인포인트
-

## 놀라웠던 점
- (예상과 달랐던 것)

## 다음 단계
- 추가 확인이 필요한 것
- 다른 팀원에게 공유할 것
```

---

## analysis/ 운영 규칙

여러 인터뷰를 종합한 분석 산출물을 저장한다.

### 파일 네이밍
```
analysis/YYYY-MM-DD-분석주제.md
```

### 메타데이터
```yaml
---
date: YYYY-MM-DD
type: research
role: uxr
topic: [분석 주제]
project: ai-native-team
method: interview  # 또는 survey, usability-test, competitive-analysis
participant-count: N
tags: [종합분석, 관련태그]
---
```

### 분석 문서에 포함할 것
- 리서치 질문 (무엇을 알고 싶었나)
- 방법론 (어떻게 했나)
- 참여자 개요 (익명화)
- 핵심 발견 (패턴, 테마)
- 인사이트 → 제품 임플리케이션
- 원본 데이터 링크 (`interviews/` 폴더 참조)

---

## traces/ 운영 규칙

다른 역할과 동일한 방식으로 운영한다.

- Claude Code에서 작업 후 `/save` 입력하면 자동으로 기록 생성
- 수동으로 할 경우: [TEMPLATE-trace.md](../TEMPLATE-trace.md) 복사 → `traces/YYYY-MM-DD-주제.md`로 저장
- 예시: `traces/2026-03-25-인터뷰-가이드-설계.md`

### 언제 기록하나?
- 모든 대화를 기록할 필요 없음
- **다른 팀원에게 영향을 주는 결정**을 했을 때
- **나중에 "왜 이렇게 했지?"라고 물어볼 만한 것**이 있을 때
- AI 대화에서 **생각이 바뀐 순간**이 있었을 때

---

## 워크플로우

```
1. 리서치 계획   → traces/ 에 설계 의사결정 기록
2. 인터뷰 실행   → interviews/YYYY-MM-DD-참여자/ 에 원문 저장
3. 개별 정리     → interviews/.../notes.md 에 빠른 정리 (선택)
4. 종합 분석     → analysis/ 에 패턴 & 인사이트 도출
5. 팀 공유       → docs/shared/announcements/ 에 공지 또는 PR
```
