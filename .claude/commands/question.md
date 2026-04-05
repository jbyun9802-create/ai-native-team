# 질문 — GitHub 이슈 등록

질문을 GitHub 이슈로 바로 등록합니다.

## 입력

사용자가 `/question` 뒤에 텍스트를 입력하면 질문의 힌트로 사용합니다: $ARGUMENTS

## 실행 순서

### 1단계: GitHub CLI 확인
`gh auth status`를 실행하여 인증 상태를 확인합니다.
인증이 안 되어 있으면 다음 안내를 출력하고 중단합니다:

> GitHub CLI가 인증되지 않았습니다. 다음 명령어를 실행해주세요:
> 1. `gh` 설치: https://cli.github.com/
> 2. `gh auth login` 실행

### 2단계: 역할 확인
사용자에게 어떤 역할로 등록할지 물어봅니다:
- `pm` — PM
- `engineering` — 엔지니어링
- `design` — 디자인
- `uxr` — UX 리서치
- `gtm` — GTM

### 3단계: 질문 내용 정리
대화 내용 또는 사용자 입력($ARGUMENTS)을 분석하여 다음을 정리합니다:
- **제목**: 질문을 한 줄로 (간결하게)
- **맥락**: 이 질문이 나온 배경
- **구체적 질문**: 정확히 알고 싶은 것
- **관련 파일/코드**: 관련된 파일이 있다면

사용자에게 정리한 내용을 보여주고 수정할 부분이 있는지 확인합니다.

### 4단계: 이슈 생성
다음 명령어로 GitHub 이슈를 생성합니다:

```bash
gh issue create --title "[Question] {제목}" --body "{본문}" --label question --label {역할}
```

본문 형식:
```markdown
## 작성자
{역할} (YYYY-MM-DD)

## 맥락
{질문 배경}

## 질문
{구체적 질문}

## 관련 파일
{파일 목록 또는 "없음"}

---
> Created via `/question` command
```

### 5단계: 완료 메시지
생성된 이슈 URL을 알려줍니다.
