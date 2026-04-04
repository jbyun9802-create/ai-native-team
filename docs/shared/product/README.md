---
date: 2026-04-04
type: guide
role: all
topic: Product 폴더 구조 가이드
project: ai-native-team
tags: [product, structure, guide]
---

# Product 폴더 구조

프로덕트팀이 만드는 **산출물 종류별**로 문서를 정리한다. 실제 코드는 루트의 `src/`에 위치한다.

## 폴더 구조

```
docs/shared/product/
├── prd/            PRD (Product Requirements Document)
├── specs/          기능 스펙, API 스펙, 데이터 모델
├── storybook/      컴포넌트 문서, 디자인 시스템 연동
├── research/       시장조사, 경쟁분석 등 프로덕트 리서치
├── assets/         와이어프레임, 목업, 다이어그램 등 시각자료
└── validation/     QA 리포트, 베타 피드백, 테스트 결과
```

## 각 폴더에 넣는 것

| 폴더 | 넣는 것 | 주로 작성하는 역할 |
|------|---------|------------------|
| `prd/` | PRD, 문제 분석, 유저 스토리, 요구사항 정의 | PM, GTM |
| `specs/` | 기능 스펙, API 명세, 데이터 모델, 기술 스펙 | Engineering, PM |
| `storybook/` | 컴포넌트 문서, 디자인 토큰, 디자인 시스템 연동 가이드 | Design, Engineering |
| `research/` | 시장조사, 경쟁사 분석, 트렌드 리서치 | PM, GTM, UXR |
| `assets/` | PNG, PDF, 피그마 캡처, 워크플로우 다이어그램 | 누구나 |
| `validation/` | 유저빌리티 테스트 결과, 베타 피드백, QA 리포트 | UXR, Engineering |

## 파일 작명 규칙

```
YYYY-MM-DD-주제.md
```

예시:
- `2026-03-14-problem-analysis.md`
- `2026-04-10-api-save-endpoint.md`
- `2026-04-15-button-component.md`

## 메타데이터

모든 문서에 YAML frontmatter를 붙인다. `category` 필드로 산출물 종류를 표시한다.

```yaml
---
date: 2026-04-04
type: product
role: pm
topic: 문제 분석
project: ai-native-team
category: prd          # prd | spec | storybook | research | validation
tags: [mvp, problem]
---
```

자세한 메타데이터 규격은 [metadata-standard.md](../../_standards/metadata-standard.md)를 참고한다.
