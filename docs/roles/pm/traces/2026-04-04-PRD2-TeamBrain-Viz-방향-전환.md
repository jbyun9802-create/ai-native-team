---
date: 2026-04-04
type: trace
role: pm
topic: PRD-2 TeamBrain Viz — 3D ���에서 CLI+HTML 대시보드로 방향 전환
project: ai-native-team
tags: [PRD-2, 시각화, brain.py, TUI, CLI, HTML대시보드, 의미검색, traces]
---

# PRD-2 TeamBrain Viz — 3D 뇌에서 CLI+HTML 대시보드로 방향 전���

## 날짜
2026-04-04

## 목���
PRD-2(팀 멘탈 ���델 시각화)의 프로토타입을 만들고, 실제 traces 데이터와 연��되는 도구로 확정

## 핵심 내용
- 처음 3D 뇌 구조 시각화(Three.js)로 시���했으나, "매일 쓰는 ��구"로는 과하다는 판단으로 방향 전환
- HTML 대시보드(사람별 사고 ���름 + 타임라인) → CLI(brain.py) → 다시 HTML로 돌아오는 ��정을 ��침
- 최종: brain.py가 traces 파싱 + --html로 대시보드 생성 + TUI(brain-tui.py)로 터��널 인터랙티브 뷰
- TUI에 Claude API 기반 의미 검색 추�� — 키워드 매칭이 아니라 맥락으로 관련 traces를 찾고 excerpt 표시
- Focus Areas를 태그 바 차트에서 "지금 머릿속"(최근 traces의 topic + insight 자연어)으로 교체

## 결정사��
- **3D 뇌 시각화 기각**: 멋있지만 실용적이지 않음. "조직의 뇌를 본다"는 경험은 traces 데이터를 ��로 보여��는 것이 본질
- **CLI + HTML 병행**: brain.py는 ��른 조회 + --html로 비주얼 대시보드 생성
- **TUI(brain-tui.py) 유지**: 터미널에서 인터랙티브하게 사람 전환, 기간 ���터, 의미 검색
- **team.zip에 brain.py + /save 포함**: Assessment 완료 후 배포되는 zip에 traces 도구 세트로 동��
- **태그 기반 Focus Areas 기각**: 메타데이터 태깅이 부실하면 의미 없음. topic/insight 자연어가 더 정확
- **의��� 검색에 Claude Haiku 사용**: 단��� 텍스트 매칭 대신 맥락 기반 검색 + excerpt 반환
- **날짜 기준을 가장 최신 trace���**: datetime.now() 대신 traces 중 최신 날짜를 기��으�� 기간 필터링

## 인사이트
- "조직의 멘탈 모델"은 fancy한 시각화가 아니라 "이 사람이 지�� 뭘 생각하고 있는지"를 바로 볼 수 ��는 것이 핵심
- 프로토타입을 여러 번 만들어보면서 "뭘 빼야 하는지"가 더 ���요한 결정이었음 — 3D, ���픽 뷰, 태그 바 차트 등을 빼면�� 본질에 가까워짐
- TUI�� VS Code 터미널 호환성 이슈가 있어서 디버깅에 시간 소요
- traces의 YAML frontmatter(date, role, topic)가 이미 시각���에 필요한 모든 메타데이터를 갖고 있음

## 다른 팀원이 알아야 ��� 것
- PRD-2.md 업데이트 완료 — 3D 뇌에서 CLI+HTML 대시보드로 방향 변경, 기각 사유 포��
- prototype/ 폴더에 brain.py, brain-tui.py, brain-viz.html, team-mental-model.html 생성됨
- brain.py는 하드코딩 없이 traces 파일에서 자동 감지 — /save와 바로 연동
- team.zip 배포 구조��� tools/brain.py + commands/save.md 포함 예정
