---
date: 2026-04-11
type: trace
role: pm
topic: TeamBrain 웹 프로토타입 — BYOK + 스킬 기반 /save로 인적성검사→멘탈 모델→trace 생성 플로우 구현
project: ai-native-team
tags: [BYOK, 스킬화, TeamBrain, 웹프로토타입, 바닐라HTML, 파서포팅, 프레임워크참조, PRD, 디자인핸드오프]
framework_sections: ["3. PRD를 쓰는 방식", "2. 우선순위를 정하는 방식"]
thinking_coverage: "7/9 steps"
open_thinking: ["대화 중 이탈 시 auto-draft 저장 필요 여부", "BYOK 선택의 one-way/two-way door 판단", "1차 시연 대상 정의", "Vercel 배포 파이프라인 (docs/ 접근 문제)", "Claude Code ↔ 웹 스킬 완전 통합 시점", "무한로딩 이슈 재현 위치 미확인", "GitHub 커밋 실제 동작 end-to-end 미검증", "디자이너 브레인 UI/UX 리뷰 대기"]
---

# TeamBrain 웹 프로토타입 — BYOK + 스킬 기반 /save로 인적성검사→멘탈 모델→trace 생성 플로우 구현

## 날짜
2026-04-11

## 목적

인적성검사(assessment.html, Vercel 배포 중)에서 끝나던 흐름을 이어서, Git/Claude Code를 전혀 모르는 팀원(특히 세일즈)이 브라우저만으로 팀 멘탈 모델에 접근하고 직접 trace를 생성할 수 있는 프로토타입을 만드는 것.

**성공 기준**: 비엔지니어링 직군이 이 시스템으로 traces를 실제로 만들어냄.

## 사고 프레임워크: 3. PRD를 쓰는 방식

### 사고 단계

| Step | 상태 | 내용 |
|------|------|------|
| Step 1: 프레스 릴리즈 (Working Backwards) | Covered | "Git 모르는 세일즈가 링크 받고 1분 안에 로그인해 팀 결정을 훑고, 첫 trace를 직접 생성·저장"이라는 한 문장 가치가 명확히 정의됨. 이 문장이 설계 전반의 기준선 역할을 함 |
| Step 2: 성공 지표 | Covered (보충) | **비엔지니어링 직군이 traces를 만들어내면 성공**. 정량 숫자보다는 "경로가 끝까지 작동하느냐"의 이진 판단. 첫 세일즈/디자인/UXR trace 생성 시점이 마일스톤 |
| Step 3: 스코프 | Covered | v1 범위 + "안 하는 것" 명시. 범위 밖: Google OAuth, 스트리밍, 자동 새로고침, 모바일 최적화, 실명 마스킹, Claude Code↔웹 스킬 완전 통합 |
| Step 4: 리스크 | Covered (보충) | 가장 큰 가정이었던 "세일즈가 Anthropic API 키를 발급받을 수 있다"를 PM이 확인 — **AI native를 지향하는 조직이면 API 키 발급은 기본**. 따라서 BYOK 게이트가 유저 차단 리스크가 아님. 부차 리스크는 구현 중 대응 (CORS preflight → 타임아웃+skip 버튼, Vercel docs/ 접근 → 후속 작업, localStorage XSS → 프로토타입 단계 수용) |
| Step 5: 유저 시나리오 | Partially | 해피 패스는 상세히 정의. 엣지케이스(대화 중 이탈, 키 만료, ```trace 블록 누락 응답, 동시 커밋 충돌)는 체계적 전수 안 됨. 방어 코드 일부 추가 (8초 타임아웃, 에러 위치 표시, skip validation, GitHub API SHA 조회) |

### 사람이 확인한 것
- [x] 유저 시나리오의 현실성 (API 키 발급 전제) — PM 확인: AI native 지향 조직에 기본
- [x] "안 하는 것" 결정 — 플랜 파일 "범위 밖" 섹션
- [ ] 기술적 제약 정합성 — CORS direct browser access, Vercel docs/ 접근은 로컬 검증만, 배포 검증 전
- [ ] 엣지케이스 전수 — 대화 중 이탈 처리는 skip됨 (열린 질문)

## 사고 프레임워크: 2. 우선순위를 정하는 방식

### 사고 단계

| Step | 상태 | 내용 |
|------|------|------|
| Step 1: 반드시 달성해야 할 한 가지 목표 | Covered | "비엔지니어링 직군이 웹에서 trace를 만들어내는 경로가 끝까지 작동" — 측정 가능(이진), 다른 모든 결정의 기준선. 팀 동의는 거치지 않았으나 PM 단독 명확 |
| Step 2: 후보 평가 (RICE 등) | Not covered (skip) | 대안 비교 없이 유저 피드백 기반으로 즉시 재설계. Next.js → 바닐라 HTML, 서버 프록시 → BYOK 같은 큰 전환이 RICE 없이 이뤄짐. 보충 질문 skip — 프로토타입 단계에선 수용 |
| Step 3: "안 하는 것" 명시 | Covered | 플랜 파일의 "범위 밖 (프로토타입 이후)" 섹션에 7개 항목 나열 |
| Step 4: 되돌릴 수 있는가 (One-way vs Two-way) | Not covered (skip) | 큰 선택들(BYOK, 바닐라 HTML, 스킬 이관)의 되돌림 난이도 판단 미수행. 보충 질문 skip — 열린 질문으로 이관 |

### 사람이 확인한 것
- [x] "안 하는 것" 명시 ✓
- [ ] 팀 에너지/번아웃 — 확인 안 함
- [ ] 이해관계자의 정치적 맥락 (시연 대상) — skip됨 (열린 질문)

## 결정사항

1. **스택: 바닐라 HTML + serverless 2개 (Next.js 제외)**
   - 이유: assessment.html이 이미 바닐라+Vercel serverless로 배포 중 → 일관성. 프로토타입 단계엔 프레임워크 오버헤드 불필요. 디자이너가 넘겨받아 수정하기도 쉬움

2. **BYOK (Bring Your Own Key)** — 브라우저↔Anthropic 직통, 서버 프록시 없음
   - 이유: (a) 비용 분산 — 관리자가 전체 팀 사용량 부담 안 함 (b) 프라이버시 — 대화가 서버 경유 안 함 (c) 오픈소스 친화 — 포크하는 팀이 중앙 API 키 불필요 (d) 권한 분리 — 키 자체가 게이트, OAuth/allowlist 인프라 불필요
   - 전제: AI native 조직에 API 키 발급이 기본이라는 PM 판단

3. **/save를 스킬로 이관** — `.claude/commands/save.md` → `.claude/skills/save/SKILL.md`
   - 이유: Claude Code와 웹이 같은 스킬 파일을 각자 환경에서 실행할 수 있게 함. "실행 컨텍스트"를 추상화
   - 환경 분기는 wrapper system prompt의 "대화 규칙"에서 흡수 (SKILL.md 본문 안 건드림). 후속 통합 시점에 SKILL.md 2단계 본문을 "컨텍스트에 있으면 사용, 없으면 Read"로 한 줄 수정 예정

4. **/api/context가 5개 프레임워크 전체 반환** — `current_framework`(save flow용) + `all_frameworks`(뷰어용)
   - 이유: Phase B 뷰어가 "모든 역할의 사고법"을 보여줘야 한다는 요구 — 신규 멤버가 "다른 역할이 어떻게 생각하는지" 이해하는 경로가 멘탈 모델의 핵심

5. **GTM traces 0개 상황을 데모 페이로드로 활용** — 세일즈가 "첫 GTM trace를 만드는" 경험이 자연스러운 시연 포인트 + 성공 기준과 정확히 일치

6. **포트 3002 사용 (3001 대신)** — 3001이 다른 프로세스 점유 중. server.js에 `PORT` 환경변수 지원 추가

7. **키 검증 건너뛰기 옵션 + 8초 타임아웃** — Anthropic CORS preflight 차단 가능성 대비 우회 경로. 명시적 에러 위치 표시로 "보이지 않는 에러" 제거

8. **TUI 파서 Python → JS 포팅 시 day-granular cutoff** — millisecond 비교가 시간대 경계에서 trace를 잘못 제외하는 버그 발견 → `toISOString().slice(0,10)` 문자열 비교로 전환

## 인사이트

- **Claude Code는 제품이 아니라 클라이언트**. 진짜 제품은 "스킬 + 프레임워크 + traces"라는 기질(substrate). Claude Code, 웹, 향후 다른 UI는 같은 기질을 다르게 소비하는 클라이언트일 뿐. 이 관점이 서면 "Git 친숙도" 제약이 자연스럽게 풀림 — 프론트엔드 교체 문제였음.

- **BYOK가 프라이버시·비용·권한 3가지를 동시에 해결한다**. 서버 API 키 관리는 화이트리스트/쿼터/감사로그 인프라가 폭발하는데, BYOK는 이 복잡도를 유저 쪽으로 위임하면서 유저도 프라이버시 이득. win-win.

- **/save 스킬화의 진짜 가치는 "실행 컨텍스트 추상화"**. 같은 스킬이 Claude Code에선 Read 툴로, 웹에선 서버 사전 주입으로 프레임워크를 얻음. "어떻게 로드하느냐"는 클라이언트 책임, "무엇을 해야 하느냐"는 스킬 책임. 이 분리가 새 프론트엔드를 저비용으로 추가할 수 있게 만드는 핵심.

- **brain-tui.py 파서의 JS 포팅이 놀랍게 깔끔했다**. 정규식만 옮기면 1:1. 함수 단위 파서로 작성된 덕분. 메서드 체인이나 OOP로 얽혔다면 포팅 비용이 폭발했을 것. → 미래의 새 프론트엔드를 대비해 파서는 계속 함수 단위로 유지.

- **무한로딩은 "에러가 보이지 않는 에러"가 가장 해롭다**. 타임아웃 + 에러 위치 표시 + 우회 경로(skip validation) 세 가지가 함께 없으면 유저는 "안 됨"밖에 말 못 함. 이번에 방어막 3종 세트를 추가하면서 "침묵하는 실패"를 "말하는 실패"로 바꾸는 패턴 확립.

- **"빨리 보고 싶다" 압력 하에서 플랜 모드가 3번 거부됨**. 아키텍처 진화 속도 vs 플랜 파일 동기화 비용의 긴장. 이 프로젝트처럼 플랜 파일 자체가 문서화 자산인 경우엔 필요 비용이지만, 승인 단계는 줄일 여지 있음. 다음부터는 큰 변경만 플랜 갱신, 작은 조정은 직접 구현 후 요약.

- **유저가 "pm thinking framework 적용이 안된거같아"라고 지적한 것 자체가 이 프로젝트의 가치 증명**. 프레임워크가 있고, 누군가 그걸 적용했는지 확인할 수 있다는 것. 지금 이 trace가 그 확인의 결과물.

## 열린 질문

1. **대화 중 이탈 시 auto-draft 저장 필요한가** — 현재 Phase C의 chat state는 메모리에만 존재, 브라우저 닫으면 사라짐
2. **BYOK 선택이 one-way인가 two-way인가** — 나중에 서버 프록시 + 팀 공용 키 방식으로 전환할 수 있는지 명시적 판단 필요
3. **1차 시연 대상은 누구인가** — 누구에게 보이는 프로토타입인지에 따라 다듬어야 할 부분이 달라짐
4. **Vercel 배포 파이프라인** — `docs/`가 `prototype/` 밖에 있어 serverless 함수가 런타임에 못 읽음. 로컬은 OK. 배포하려면 빌드 스텝에서 `docs/` 복사 or Vercel 루트를 레포 루트로 이동 필요
5. **Claude Code ↔ 웹 스킬 완전 통합 시점** — 현재 `commands/save.md`와 `skills/save/SKILL.md`가 중복. 오픈소스 공개 시점에 통합하기로 잠정 결정했으나 시기 미확정
6. **무한로딩 이슈 재현 위치 미확인** — 유저가 Phase A/B 어디서 걸렸는지 아직 보고 대기 중. 타임아웃+에러 표시 방어막을 추가했으므로 다음 피드백 때 드러날 것
7. **GitHub 커밋 실제 동작 end-to-end 미검증** — PAT 필요, 유저가 아직 실제 커밋까지 테스트 안 함
8. **디자이너 브레인 UI/UX 리뷰 대기** — 팔로업 예정, 아래 핸드오프 섹션 참조

## 다른 팀원이 알아야 할 것 — PM → Design 핸드오프

디자이너가 이 작업을 팔로업할 예정. [PM 프레임워크 섹션 7 PM→Design 핸드오프](../../../shared/product/specs/frameworks/pm-thinking.md) 형식으로 정리.

### 유저 문제 (JTBD)

> **When** Git/Claude Code를 모르는 팀원(특히 세일즈)이 팀 멘탈 모델에 접근하고 자기 현장 지식을 시스템에 남기고 싶을 때,
>
> **I want** 브라우저 링크 하나로 로그인해서 다른 역할들의 사고법을 훑고, Claude와 자연스럽게 대화하면서 내 trace를 자동으로 구조화해 저장할 수 있기를,
>
> **So I can** 내 현장 경험(고객 반응, 경쟁사 언급, 가격 피드백)이 팀 공통 기억으로 들어가 PM/엔지니어의 의사결정에 피드백된다.

### 전략적 의도 — 왜 이 방향

- **단일 기질, 복수 프론트엔드**: Claude Code는 엔지니어 전용 편집기, 웹은 비엔지니어 전용 접근점. 둘은 같은 traces/프레임워크/스킬 파일을 공유. 디자이너가 리디자인하거나 새 버전을 만들 때 **데이터 스키마는 그대로**
- **사고의 동반자 대화 모델**: 단순 폼이 아니라 Claude와의 대화에서 프레임워크 기반 7단계 save가 일어남. 유저는 "오늘 있었던 일"을 자연스럽게 말하고, 구조화는 자동
- **첫 GTM trace를 만드는 경험이 성공 순간**: 세일즈가 brain.html에서 첫 trace를 만들어내면 "이 시스템이 실제로 작동한다"는 증명

### 기각한 대안과 이유

| 대안 | 기각 이유 |
|------|-----------|
| Next.js + Google OAuth + 서버 LLM 프록시 | 세일즈는 Git·설치·OAuth App 등록 친숙도 0. 서버 API 키 관리는 오버킬. 관리자가 모든 사용량 부담. BYOK로 해결됨 |
| 폼 기반 trace 입력 (채팅 없음) | /save의 진짜 가치는 "프레임워크 기반 사고 검증"인데 폼으론 그게 안 됨. Claude와 대화해야 섹션 매칭·보충 질문·열린 질문 감지가 가능 |
| 별도 DB (Supabase 등) | "진실은 마크다운 + git"이라는 원칙 깨짐. 두 군데 동기화 비용. Claude Code와 웹이 같은 파일을 공유한다는 핵심 아키텍처 흔들림 |
| Slack/이메일 봇 | 마찰은 최소지만 봇 인프라 필요. 프로토타입 범위 초과. v2 이상 |

### 제약 조건

- **CSS 베이스**: [assessment.html](../../../../prototype/assessment.html)의 dark theme + 클래스 네이밍(`.bt bp`, `.cd`, `.ri`, `.rpt`)과 일관성 유지. 두 페이지가 같은 브라우저 세션에서 연결돼 보여야 함
- **단일 HTML 파일 원칙**: [brain.html](../../../../prototype/brain.html)은 한 파일에 CSS+JS+HTML 전부 포함. 외부 의존성은 marked.js CDN 1개뿐. 빌드 스텝 없음
- **브라우저-direct Claude 호출**: `anthropic-dangerous-direct-browser-access: true` 헤더로 직통. 디자인 요소가 추가 fetch를 유발하지 않아야 함 (매 상호작용마다 Claude 호출하면 비용 폭발)
- **데이터 읽기는 /api/traces, /api/context 두 엔드포인트만**: 새 데이터 필요 시 이 엔드포인트를 확장. 새 엔드포인트 추가는 [prototype/server.js](../../../../prototype/server.js) 수정 필요
- **민감 정보**: `docs/roles/*/traces/*.md`에 팀원 실명·회사명·인터뷰 원문이 있음. 디자인 시 실수로 외부 시연 화면에 노출되지 않게 주의 (특히 스크린샷 캡처 시)

### 해석 여지가 있는 부분 (디자이너 자유 판단)

- **Phase B 탭 전환 방식**: 현재 [프레임워크]/[타임라인] 2탭으로 분리. 한 화면에 섞는 방식(예: 각 프레임워크 섹션 밑에 관련 traces를 같이)도 가능
- **프레임워크 카드 UI**: 좌측 사이드바에 5개 역할 카드로 표시 중. 다른 형태(그리드, 아코디언, 허브&스포크, 마인드맵)로 대체 OK
- **trace 카드 레이아웃**: 핵심/결정/인사이트 3섹션을 세로로 쌓음. 카드 전체 클릭 → 원문 모달 여는 인터랙션 아직 없음 — 추가할지 판단 필요
- **채팅 UI의 Save 버튼 위치/디자인**: 지금은 우측 하단 녹색 버튼. 대화 흐름에서 더 자연스러운 타이밍에 나타나는 방식("충분히 말했어요" 감지 후 제안)도 가능
- **마크다운 미리보기 박스**: 녹색 카드로 표시. "저장하기 직전의 긴장감/안도감"을 어떻게 표현할지가 핵심 UX 지점. 지금은 다소 기술적으로 보임
- **Phase A (BYOK) 카피**: "Anthropic API 키 입력"이라는 기술적 용어가 세일즈에게 부담스러울 수 있음. 대체 카피/온보딩 스텝 가능

### 디자이너가 바로 확인할 수 있는 것

- **브라우저 접속**: `http://localhost:3002/brain.html`
- **서버 실행**: `cd prototype && PORT=3002 node server.js`
- **전체 플로우 시연**: `http://localhost:3002/assessment.html` → 인적성검사 완주 → "팀 브레인 열기" → BYOK → Phase B (프레임워크 탭 + 타임라인 탭) → Phase C (채팅 + Save)
- **주요 파일**:
  - [prototype/brain.html](../../../../prototype/brain.html) — UI/UX 주 수정 대상. 단일 파일 ~800줄
  - [prototype/assessment.html](../../../../prototype/assessment.html) — 기존 디자인 베이스
  - [prototype/api/context.js](../../../../prototype/api/context.js) — 새 데이터 필요 시 확장
  - [.claude/skills/save/SKILL.md](../../../../.claude/skills/save/SKILL.md) — save flow 전개 방식 참고 (디자인 결정 아님)
  - [plan 파일](../../../../../.claude/plans/valiant-strolling-marble.md) — 전체 설계 맥락

### 디자이너에게 묻고 싶은 것

1. **프레임워크 카드 5개 UI의 시각적 위계** — 5개 역할이 동등한데 지금은 수직 리스트. 더 나은 표현?
2. **Phase C의 채팅 → Save → 미리보기 → GitHub 커밋 흐름 시각화** — 지금은 수직으로 쌓임. "저장 직전 긴장감"을 어떻게 표현할지?
3. **Phase A의 압박감 완화** — 기술적 용어(API 키, `sk-ant-`) 노출이 세일즈에게 부담. 대체 카피/온보딩 스텝?
4. **Phase C 진입 후 "뭘 말해야 할지 모르겠음" 문제** — 현재는 placeholder 힌트 한 줄뿐. 대화 시작점을 디자인적으로 유도할 방법?
