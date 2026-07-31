# Agent-engineering evidence record

`ax.org` 한 장에서 공개 대문, 깊은 웹 기록면, 제출 파일 3종을 재현한다.

```text
ax.org (authored SSOT)
├── build/index.html                 짧은 대문
├── build/record.html                인터랙티브 깊은 기록면
├── build/KimJunghan_AX_Competency.pdf
├── build/KimJunghan_AX_Portfolio.pdf
└── build/KimJunghan_AX_Detail.md
```

## 왜 여기 있는가

J-space 재현 작업은 **Org 정본에서 HTML·인터랙티브 HTML·acmart PDF를 다시 만들 수
있다**는 형식 검증이었다. 이 디렉터리는 그 형식을 가져오되 내용은 전혀 가져오지 않는다.
중심은 모델 역량을 문서·도구·사람의 판단이 만나는 작업면으로 옮겨 온 기록과, 그것을 확인할 수 있는 공개 증거다. `ax`는 안정된 URL 이름일 뿐 AX 직무 지원서가 아니다.

`timeline/view.py`가 만든 루트의 `axis.html`은 LOCAL viewer다. 제목을 품으므로 이 문서에
복사하거나 iframe으로 싣지 않는다. 웹 기록면에는 별도의 allowlist projection만 연결한다.

## 빌드

```bash
cd apply/ax
nix develop -c make all
nix develop -c make check
```

빠른 웹/Markdown 확인은 시스템의 Emacs·Pandoc만으로도 가능하다.

```bash
make html md
```

PDF는 acmart의 `manuscript,nonacm` 한 단 양식과 XeLaTeX를 사용한다. 한글은 이미지가
아니라 검색·복사 가능한 텍스트로 남는다.

## 편집 규칙

- 내용은 `ax.org`만 고친다.
- `:landing:`, `:record:`, `:competency:`, `:portfolio:`, `:detail:` 태그가 export 범위다.
- 파생 파일은 `build/` 아래에만 둔다.
- JS가 필요하면 `assets/`에 두고 공개 allowlist 데이터만 받는다.
- 지원 회사명과 추천 정보는 `../PRIVATE.md`에만 둔다.

`ax.org`는 한 직무의 요구사항 대응표가 아니라, 모델 능력 → 문서·기억 → 실행·검증 →
사람의 판단과 인계로 이어지는 한 논증이다. 새 소재를 넣을 때는 검증된 사실을 이 흐름 안에
놓고, 파생물 전체를 다시 빌드한다.
