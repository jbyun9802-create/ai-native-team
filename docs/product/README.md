---
date: 2026-03-15
type: guide
role: pm
topic: Product 폴더 구조 가이드
project: ai-native-team
tags: [product, structure, guide]
---

# Product 폴더 구조

프로덕트 관련 문서를 **단계(Phase)별**로 정리합니다. 실제 코드는 루트의 `src/`에 위치합니다.

## 폴더 구조

```
docs/product/
├── planning/        기획 단계
├── design/          디자인 단계
│   └── assets/      이미지, 피그마 캡처 등
├── specs/           개발 명세
├── validation/      검증 단계
└── diagrams/        다이어그램 (단계 무관)
```

## 각 폴더에 넣는 것

| 폴더 | 넣는 것 | 주로 작성하는 역할 |
|------|---------|------------------|
| `planning/` | 문제 분석, PRD, 유저 스토리, 시장 조사 | PM, GTM, UXR |
| `design/` | 와이어프레임, IA 구조, 프로토타입 문서 | Design |
| `design/assets/` | PNG, PDF 등 디자인 바이너리 파일 | Design |
| `specs/` | API 명세, 데이터 모델, 기술 스펙 | Engineering |
| `validation/` | 유저빌리티 테스트 결과, 베타 피드백, QA 리포트 | UXR, Engineering |
| `diagrams/` | 워크플로우, 아키텍처 등 시각 자료 | 누구나 |

## 파일 작명 규칙

```
YYYY-MM-DD-주제.md
```

예시:
- `2026-03-15-problem-analysis.md`
- `2026-04-01-wireframe-save-flow.md`
- `2026-04-10-api-save-endpoint.md`

## 메타데이터

모든 문서에 YAML frontmatter를 붙입니다. `phase` 필드로 단계를 표시합니다.

```yaml
---
date: 2026-03-15
type: product
role: pm
topic: 문제 분석
project: ai-native-team
phase: planning          # planning | design | spec | validation
tags: [mvp, problem]
---
```

자세한 메타데이터 규격은 [metadata-standard.md](../metadata-standard.md)를 참고하세요.
