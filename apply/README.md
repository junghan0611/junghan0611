# 역량 및 성과 기술서 — AX 전환 · 에이전트 플랫폼

김정한 (Junghan Kim)

[junghanacs@gmail.com](mailto:junghanacs@gmail.com) · [github.com/junghan0611](https://github.com/junghan0611) · [notes.junghanacs.com](https://notes.junghanacs.com) · [agenda.junghanacs.com](https://agenda.junghanacs.com)

---

## 이 문서에 대하여

[프로필](../README.md)과 [이력서](../resume/README.md)는 영문이고, 경력 전체를 담는다.
이 문서는 그 중에서 **AX 전환 · 에이전트 플랫폼 직무 축**만 잘라낸 국문 기술서다.
프로젝트 단위 상세는 [portfolio.md](portfolio.md)에 있다.

특정 회사를 위해 쓰지 않았다. 이 계열의 직무가 요구하는 것이 대체로 같기 때문에,
공개해 두고 필요할 때마다 그대로 낸다. 회사별 정보(지원 경로, 추천, 공고 원문)는
비공개 파일에 따로 둔다.

**읽는 방법.** 아래의 모든 주장 옆에는 지금 바로 열어볼 수 있는 공개 저장소가 있다.
회사 코드는 열 수 없으므로, 회사 주장은 언제나 공개 저장소 옆에 붙여 둔다.

---

## 한 줄

펌웨어부터 에이전트 루프까지 한 사람이 세로로 관통한다.
지금 하는 일은 그 세로축을 조직에 넘기는 것 — **도메인의 주인에게 에이전트를 붙이는 일**이다.

---

## 1. AX 전환 — 개념이 아니라 이미 하는 일

### 1.1 도메인 오너 에이전트 (2026.05 ~ 현재)

다른 팀에서 오는 요청은 "대시보드를 만들어 달라"가 아니다. **"나 없이도 돌아가게 해 달라"**이다.
그래서 대시보드를 만들지 않는다. 에이전트를 세워서 그 도메인의 주인에게 붙인다.

| 에이전트 | 하는 일 | 설계의 핵심 |
|---|---|---|
| **VOC 워크벤치** | 매일의 고객 상담 데이터 위에서 정량적 가추(abduction) | 모든 숫자의 단위·기간·포함정책을 고정하고, 근거를 개별 대화 id까지 역추적 가능하게 만든다. 기준선과 다른 신호를 잡고, 남는 잔차를 다음 사이클의 가설로 넘긴다 |
| **인시던트 워크벤치** | 장애·이슈의 증거를 살아 있는 원본에서 읽는다 | 덤프를 저장하지 않는 **읽기 전용**. 모든 시각을 KST 단일 시간축으로 정렬. VOC → 디바이스 → 런타임 사슬을 잇는다 |
| **비서실장(COS) 에이전트** | 내 회사 포트폴리오 자체를 얹은 작업면 | 트랙, 오너, 결정, 원장(ledger)을 에이전트가 들고 있는다 |
| **Forge 커넥터** | 대화를 리뷰 가능한 작업 항목으로 굳힌다 | 셀프호스팅 Forgejo 위에서 에이전트가 이슈·코멘트·라벨·PR을 돌린다 |

핵심은 마지막 줄이다. **말 걸 때만 답하는 에이전트는 채팅창이고, 작업 항목을 소유하고
거기로 되돌아오는 에이전트는 동료다.** 이 차이가 AX 전환의 성패를 가른다.

- 공개 증거: [abductcli](https://github.com/junghan0611/abductcli) — VOC 워크벤치의 추론 엔진이 된 공개 실험체
- 공개 증거: [forge-config](https://github.com/junghan0611/forge-config) — Forge 커넥터의 공개 골격

### 1.2 AI 인프라와 지식베이스 구축 (2025.06 ~ 2025.09)

입사 후 처음 맡은 일이 사내 AI 인프라를 바닥부터 세우는 것이었다.

- **GPU 클러스터** — RTX 5080 × 3, NixOS 25.11, 10G 네트워크, Docker 17개 서비스
- **계층형 에이전트 시스템** — n8n 40+ 노드 워크플로 + Supabase pgvector (문서 임베딩 2,945건)
- **데이터 파이프라인** — Airbyte 커넥터로 Channel.io · Notion · JIRA → PostgreSQL JSONB
- **사내 포털** — Cloudflare Zero Trust 뒤에 배치

이미 쓰고 있던 낡은 사내 시스템에 AI를 붙여 실제 업무 데이터를 쓰게 만드는 일이었다.
RAG는 데모로 끝내지 않았고, 운영으로 넘겼다.

### 1.3 이 축에서 배운 것

AX 전환의 병목은 모델이 아니라 **경계**다.
에이전트가 무엇을 읽어도 되고, 무엇을 쓰면 안 되고, 실패했을 때 누가 책임지는지가
설계되어 있지 않으면, 아무리 좋은 모델을 붙여도 조직은 그것을 신뢰하지 않는다.
그래서 나는 프롬프트로 금지하지 않고 **울타리(fence)를 만든다** → §5.2

---

## 2. Agentic AI — 쓰는 게 아니라 만든다

Claude Code와 Codex는 매일 쓰는 도구다. 다만 **활용 경험**이라는 칸에 넣기에는
한 층 아래에서 일해 왔다. 하네스 자체를 만들어 배포했다.

### 2.1 entwurf — 에이전트 하네스 디스패치 기층

[entwurf](https://github.com/junghan0611/entwurf) · [`@junghanacs/entwurf`](https://www.npmjs.com/package/@junghanacs/entwurf) (npm)

이미 존재하는 에이전트 하네스들(Claude Code, Codex, Antigravity, pi)이 **서로의 대화록·인증·런타임을
소유하지 않은 채로** 정체성(garden id)만으로 서로를 호출하게 하는 얇은 다리다.

OAuth 프록시도, CLI 대화록 스크래핑도, 백엔드 신원 교체도 없다. Claude Code는 메타브리지로,
pi는 컨트롤 소켓 어댑터로, Codex와 Antigravity는 전달 검증 프로브로 들어온다.
각자 자기 정체성을 유지하고, 기층은 **주소만 나른다.**

이게 왜 중요하냐면 — 조직에 에이전트를 도입할 때 진짜 문제는 모델 성능이 아니라
**위임·연속성·공유 도구가 세션보다 오래 살아남느냐**이기 때문이다. entwurf는 그 규약을 코드로 박은 것이다.

**제3자 검증** *(2026-07-10 기준)*

- npm 30일 설치 **1,395회**, GitHub stars 21
- 한 번도 만난 적 없는 외부 개발자가 **Snowflake Cortex Code ACP 백엔드**를 들고
  왔다 — [PR #40](https://github.com/junghan0611/entwurf/pull/40), 11개 파일 +885줄.
  내가 쓴 적 없는 **엔터프라이즈 에이전트 런타임**이다.
  그가 확장 경계를 아키텍처가 있다고 말한 그 자리에서 찾아 썼다.
  추상화에 대한 리뷰 중 유일하게 값이 나가는 종류다.

### 2.2 실측 — 에이전트와 함께 만든 결과물

주장이 아니라 숫자로 남은 것들:

| 결과 | 맥락 |
|---|---|
| **30일 198 커밋** | Zig로 쓴 Zigbee 허브 펌웨어. Claude를 짝 프로그래머로. **양산 출하됨** |
| **하루 24 커밋 · 테스트 163개 통과 · 파일 충돌 0** | 3-에이전트 병렬 개발 세션. 사람은 PM 역할만 |
| **19일** | geworfen 설계에서 배포까지 (Clojure + GraalVM native-image) |

3-에이전트 병렬 세션에서 **파일 충돌이 0**이었다는 게 핵심이다.
그건 모델이 똑똑해서가 아니라, 작업 경계를 사람이 미리 갈라 뒀기 때문이다.

### 2.3 에이전트가 쓸 수 있는 도구를 만든다

- [agent-config](https://github.com/junghan0611/agent-config) — PKM 네이티브 스킬 스택, **40개 이상의 에이전트 스킬**
- [andenken](https://github.com/junghan0611/andenken) — 시맨틱 메모리 (임베딩 + LanceDB, 크로스링궐)
- CLI 툴킷 — [denotecli](https://github.com/junghan0611/denotecli) · [dictcli](https://github.com/junghan0611/dictcli) · [gitcli](https://github.com/junghan0611/gitcli) · [lifetract](https://github.com/junghan0611/lifetract) · [abductcli](https://github.com/junghan0611/abductcli)

**3층 크로스링궐 검색** — 한국어 조직에서 RAG가 조용히 실패하는 지점을 정면으로 다룬다.

```
질의: "보편 학문에 대한 문서"

1층  임베딩 벡터    → [paideia, universalism] 태그가 붙은 노트
2층  Denote 그래프  → 메타노트 정규식 → 연결된 22개 노트
3층  개인 어휘 온톨로지 → dictcli expand("보편") → [universal, paideia, liberal arts]
```

1층만으로는 **이미 영어로 태그된 노트**밖에 못 찾는다. 같은 생각을 한국어 이름으로
주장하는 노트는 보이지 않는다. 세 층을 합쳐야 일반 RAG 스택이 뭉개버리는 노트 생태가 복원된다.
WordNet에 없는 개인 온톨로지까지 포함해서.

---

## 3. 문서와 교육 — 에이전트가 읽을 수 있는 문서 체계

AI 가이드·위키를 쓰고 교육하는 일은 대부분의 백엔드 엔지니어에게 부차적인 업무다.
나에게는 **주된 작업**이었고, 그 결과물이 공개되어 있다.

### 3.1 규모

| 항목 | 규모 |
|---|---|
| 공개 디지털 가든 | **2,200+ 페이지** ([notes.junghanacs.com](https://notes.junghanacs.com)) |
| org-mode 노트 | **3,500+** |
| 서지 항목 | **8,200+** |
| 커밋 | **8,500+** |
| 매일 저널 | **1,500+ 일 연속** |

*수치는 [`agenda.junghanacs.com/api/stats`](https://agenda.junghanacs.com/api/stats)의 라이브 데이터에서 100 단위로 내림. 2026-07-10 측정.*

### 3.2 문서를 잘 쓰는 게 아니라, 문서 계약을 설계했다

이 부분이 다른 지원자와 갈리는 자리라고 생각한다.
글솜씨가 아니라 **에이전트가 읽고 지킬 수 있는 문서 구조**를 만든 경험이다.

| 파일 | 역할 |
|---|---|
| `AGENTS.md` | 리포의 영속 기준선 — 정체성, 불변식, 작업 규칙. 에이전트가 세션마다 다시 읽는다 |
| `VOCABULARY.md` | 용어 단일 진실원(SSOT). 하중을 받는 낱말은 **한 번만** 정의한다 |
| `NEXT.md` | 핸드오프 — 다음 한 걸음. 세션이 끊겨도 다음 에이전트가 이어받는다 |
| `botlog` | 에이전트가 **자기 작업을 스스로 org 노트로 남긴다** |

이건 사람에게 읽히려고 쓴 문서가 아니라, **사람과 에이전트가 같이 읽는 계약서**다.
예컨대 이 저장소의 [`AGENTS.md`](../AGENTS.md)에는
"숫자는 100 단위로 내림한다", "정체성 문서에 한국어가 새어 들면 회귀다",
"신뢰의 근거가 될 항목은 최소 하나는 **제3자의 행동**이어야 한다" 같은 규칙이 박혀 있다.
에이전트가 매번 다시 검사한다.

### 3.3 memex-kb — 한국 조직이 전부 부딪히는 벽

[memex-kb](https://github.com/junghan0611/memex-kb)

위의 모든 것은 "문서가 평문 텍스트가 될 수 있다"를 전제한다. 한국에서는 대개 안 된다.

- `hwpx2org` — 어떤 툴체인도 건드리기 싫어하는 한글 워드프로세서 포맷
- `scanpdf2org` — 스캔된 종이를 비전 전사로
- `epub2org` · `html2epub` · `org2odtdoc` — 오피스 포맷으로의 왕복
- `textlint-ko` — 한국어 산문 린팅
- 제안서 파이프라인 — 실제로 예산을 결정하는 문서들

Org-mode를 **메타 문서**로 두고 전부 그리로 통과시킨다.
HWP, 세로형 관공서 양식, 스캔된 정부 PDF, 토크나이저 가정을 무너뜨리는 형태소.
**한국의 모든 조직이 이 벽에 부딪히고, 나는 그 벽에 대한 툴체인을 갖고 있다.**

### 3.4 넘겨준 경험

사내에서 에이전트를 다른 팀에 실제로 넘겼다 (§1.1).
문서를 쓰고 끝난 게 아니라, **받는 사람이 이어서 굴릴 수 있는 상태**까지 만들어 본 경험이다.
비개발 직군(운영팀)이 매일 아침 읽는 워크벤치가 그 결과물이다.

---

## 4. 백엔드 · 인프라 · Linux

### 4.1 언어

특정 언어를 고집하지 않는다. 문제에 맞는 것을 고른다.

| 언어 | 무엇을 만들었나 |
|---|---|
| **Go** | 스마트홈 허브 서버 (AWS IoT / 로컬 이중 백엔드), HomeAgent Matter 허브 (단일 바이너리, SSE 스트리밍, LLM 에이전트), denotecli, gitcli, lifetract |
| **Clojure** | geworfen (GraalVM native-image 43MB), abductcli, dictcli, durable-iot-migrate (Temporal + Saga — Go 대비 코드 62% 감소) |
| **Zig** | Zigbee/Wi-Fi 게이트웨이 펌웨어 — **양산 출하** |
| **C** | 레거시 Zigbee SDK, Matter CHIP C++ SDK 연동 |
| **TypeScript** | entwurf, agent-config, Lit 웹컴포넌트, Quartz 컴포넌트 |
| **Nix · Elisp · Bash** | 재현 가능한 기반 |

**Java/Spring은 쓰지 않았다.** BE 시스템 개발·운영 경험은 Go와 Clojure로 쌓았다.
JVM 자체는 Clojure와 GraalVM native-image를 다루며 계속 만지고 있다.

### 4.2 Linux — 개발이 아니라 거주

- **NixOS 선언적 관리 4대** — 노트북(ThinkPad), NUC, Oracle ARM, RPi5.
  flake 하나, `nixos-rebuild switch`, 동일한 환경. 기계가 죽으면 새 기계가 같은 세계를 부팅한다
- **Docker 17개 이상 서비스** — 전부 Nix로 선언
- **임베디드 Linux** — Yocto (scarthgap 5.0), ARM v7 glibc → **RISC-V(SG2000) 정적 musl** 포팅
- **재현성은 편의가 아니라 에이전트 신뢰의 전제조건이다.**
  환경이 결정론적임을 아는 에이전트만 확신을 갖고 행동할 수 있다

### 4.3 DB · MQ · 컨테이너 · 클라우드

| 층위 | 실제로 다룬 것 |
|---|---|
| **DB** | PostgreSQL JSONB, Supabase **pgvector** (임베딩 2,945건), SQLite, **LanceDB** (벡터), Datomic 계열 사고 |
| **MQ / 메시징** | **MQTT** + 상호 TLS 로컬 브로커, 섀도 미러링 + 단조 증가 버저닝, 루프백 이벤트 스트리밍, **Zigbee2MQTT** |
| **컨테이너 / VM** | Docker 17+ 서비스, GPU 컨테이너(CUDA), Oracle ARM VM, Yocto 이미지 |
| **클라우드** | **AWS IoT**, Oracle Cloud (ARM), Cloudflare Zero Trust, Netlify |
| **프로토콜** | ACP · MCP · A2A · JSON-RPC 2.0 · SSE · REST · emacsclient 소켓 |

**설계 사례 하나** — 하나의 프로토콜을 **교체 가능한 두 백엔드**가 서빙하게 설계했다.
연결형 배포에는 AWS IoT, 폐쇄망에는 로컬 백엔드. **펌웨어는 양쪽에서 수정 없이 그대로 나간다.**
이게 내가 생각하는 인프라 설계다. 붙이는 게 아니라, 갈아 끼울 수 있게 자르는 것.

---

## 5. 스택을 고르는 관점

### 5.1 프론트엔드 — 네 번 다르게 골랐고, 매번 이유가 있다

무슨 프레임워크를 쓰느냐는 그 자체로는 의미가 없다.
**전체 스택의 구성 부분을 내가 고르고, 왜 그것인지 아는가**가 문제다.
같은 "웹 UI"를 네 번 만들었고, 네 번 다른 답을 냈다.

| 표면 | 스택 | 왜 그것인가 |
|---|---|---|
| [notes.junghanacs.com](https://notes.junghanacs.com) — 가든 2,200+ 페이지 | **Quartz v4 포크: Preact + TypeScript + esbuild + SCSS** | 노트 3,500개를 정적 그래프로 굳혀야 한다. 컴포넌트를 직접 썼다 — `Remark42Comments.tsx`(셀프호스팅 댓글), `Webmentions.tsx`(IndieWeb microformats2). 테마를 얹은 게 아니라 컴포넌트 층을 뚫었다 |
| [junghanacs.com](https://www.junghanacs.com) — 홈페이지 | **Hugo + Hextra 모듈, 커스텀 layouts** | `head-end.html`로 **JSON-LD `@graph` 시맨틱 아이덴티티 레이어**를 주입. 사람이 아니라 **기계(LLM·검색엔진)가 읽을 표면**이 필요했다. Hugo 테마는 여러 개를 다뤄 보고 고른 것 |
| [agenda.junghanacs.com](https://agenda.junghanacs.com) — geworfen | **Clojure 서버 렌더 + 손으로 쓴 CSS 한 장** | **프레임워크를 안 쓴 것이 선택이다.** GraalVM native-image 43MB 단일 바이너리, 방문자 100명이 같은 날짜를 열어도 emacsclient 호출은 1회(캐시). SPA가 풀 문제가 아니었다 |
| [homeagent-config/ui](https://github.com/junghan0611/homeagent-config) — 스마트홈 월패드 | **Lit 3 + Vite + TypeScript 웹컴포넌트 (1,567줄)** | 임베디드 타깃에 Flutter를 올리기 전에 **웹으로 먼저 검증**한다. 웹컴포넌트는 어떤 셸에도 들어간다. 검증이 끝나면 Flutter가 셸을 맡는다 |

**Tailwind는 쓰지 않는다.** SCSS 변수와 디자인 토큰으로 처리한다
(`quartz/styles/variables.scss`, `custom.scss`). 유틸리티 클래스가 아니라 토큰을 고른 것도 선택이다.
Tailwind가 필요한 자리에 가면 하루면 붙는다. 그건 배우는 문제지 이해의 문제가 아니다.

**React 자체는 쓰지 않았지만 Preact/TSX 컴포넌트를 실서비스에 직접 작성했다.**
JSX, 컴포넌트 합성, 정적 빌드 파이프라인(esbuild), SCSS 토큰 — 그 층을 매일 만진다.

### 5.2 A2UI — 이 축에서 제일 하고 싶은 이야기

[`homeagent-config/docs/A2UI.md`](https://github.com/junghan0611/homeagent-config)

프론트엔드에서 내가 실제로 밀고 있는 방향은 프레임워크 선택이 아니라 **UI의 소유권**이다.

```
A2UI = Agent → JSON Surface → Viewer(렌더러)
```

에이전트가 **선언적 JSON으로 UI를 기술하면** 뷰어가 렌더링한다.
여기서 "에이전트"는 AI만이 아니다 — Go 룰 엔진일 수도, LLM일 수도, 자동화 규칙일 수도 있다.
둘 다 같은 JSON 포맷을 뱉고, 같은 렌더러가 그린다.

핵심 문장은 이것이다.

> **UI가 코드가 아닌 데이터로 선언된다. 코드를 보내면 보안 위험, 데이터를 보내면 안전하다.**

이게 AX 전환의 프론트엔드 답이라고 생각한다.
에이전트에게 화면을 그리게 하고 싶은데 코드 실행 권한은 주고 싶지 않다 —
그 긴장을 푸는 방법은 **UI를 데이터로 만드는 것**이다.

### 5.3 울타리(fence) — 프롬프트로 금지하지 않는다

[doomemacs-config](https://github.com/junghan0611/doomemacs-config) · `agent-server.el`

에이전트를 프롬프트로 제약하지 않는다("X 하지 마"). 대신 **울타리 친 놀이터**를 준다.

```
울타리 (agent-server.el)      놀이터 (에이전트의 자유)       보호자 (호스트/사람)
──────────────────────────    ────────────────────────────   ──────────────────────
경로 가드: 읽기 4개 디렉토리   REPL에서 새 함수 정의          모니터링, 복구
API: 아젠다·검색·서지·dblock   org 파싱, dblock 갱신          에스컬레이션, 재설계
쓰기: botlog + 추적 데이터만   질의 연쇄, 상호참조            최종 책임
```

**에이전트가 뭔가 부수면 그건 에이전트 문제가 아니라 시스템 설계 문제다.**
신뢰는 감시가 아니라 구조에서 온다.

Elisp로 10개 API를 emacsclient 소켓으로 노출한다.
Emacs가 사람에게 보여주는 바로 그 `agent-org-agenda-day` 함수를,
Oracle Cloud의 Docker 봇도 호출하고, geworfen이 웹에도 서빙한다.
**하나의 인터페이스, 세 개의 소비자.**

---

## 6. 검증 가능한 표면

에이전트 관련 주장은 꾸며내기 쉽다. 그래서 큰 주장마다 **지금 바로 열 수 있는 공개 저장소**를 붙인다.

| 주장 | 공개 증거 |
|---|---|
| 임베디드 층에서 일한다 | [homeagent-config](https://github.com/junghan0611/homeagent-config) |
| 에이전트 루프를 만든다 | [entwurf](https://github.com/junghan0611/entwurf) |
| 재현 가능한 기반 위에서 일한다 | [nixos-config](https://github.com/junghan0611/nixos-config) · [doomemacs-config](https://github.com/junghan0611/doomemacs-config) |
| 한국어 문서 문제를 다룬다 | [memex-kb](https://github.com/junghan0611/memex-kb) |
| **남들이 내 것 위에 만든다** | [entwurf#40](https://github.com/junghan0611/entwurf/pull/40) — 외부 기여자, 엔터프라이즈 ACP 백엔드 |
| **남들이 내 코드를 받아들였다** | [dakra/ghostel#343](https://github.com/dakra/ghostel/pull/343) · [#510](https://github.com/dakra/ghostel/pull/510) — 상류 머지 |

아래 두 줄이 중요하다. 내 저장소는 **능력**을 증명하지만 **수용**을 증명하지 못한다.
읽는 사람은 언제나 "저자가 유일한 심판인 닫힌 고리"를 의심할 수 있다.
그래서 근거가 **제3자의 행동**인 항목을 항상 최소 하나 유지한다.
머지된 PR, 외부 기여, 설치 수 — 위조하기 가장 어렵고, 회의적인 독자가 가장 먼저 확인하는 것들이다.

ghostel 두 건은 내가 소유하지 않은 코드베이스에서 **한국어·CJK 입력**을 고친 패치다.
memex-kb가 풀려는 것과 같은 종류의 문제를, 반대편에서 만난 것이다.

---

## 7. 공백 — 없는 것은 없다고 쓴다

| 요구 | 현재 |
|---|---|
| **Java / Spring** | 없다. BE는 Go와 Clojure로 했다. JVM은 Clojure·GraalVM으로 계속 만진다 |
| **React / Tailwind** | React 자체는 안 썼다. **Preact + TSX 컴포넌트를 실서비스에 직접 작성**했고(§5.1), Tailwind 대신 SCSS 토큰을 쓴다 |
| **BMAD** | 이름으로는 모른다. 같은 층위 — 에이전트 워크플로 규약 — 를 [entwurf](https://github.com/junghan0611/entwurf)와 40+ 스킬로 직접 설계했다. 방법론 이름을 배우는 건 며칠이면 된다 |

공백을 감추면 면접에서 드러난다. 미리 적어 두고, 대신 **무엇으로 그 자리를 메웠는지** 쓴다.

---

## 8. 경력 요약

| 기간 | 소속 | 역할 |
|---|---|---|
| 2025.06 ~ 현재 | **고퀄(GoQual)** | Full Stack Architect — 펌웨어(Zig, 양산) · Go 서버 · Flutter 앱 · AI 인프라 · 도메인 오너 에이전트 · PSIRT |
| 2022 ~ 현재 | **독립 작업** | PKM-AI 하네스, 디지털 가든, 10+ 오픈소스 `-config` 프로젝트 |
| 2018 ~ 2021 | **성균관대 분산컴퓨팅연구실** | 비휘발성 메모리 파일시스템, 가상화 환경 NUMA 락 성능. Virginia Tech COSMOSS Lab 교환연구원(2019.07~2020.03) |
| 2013 ~ 2017 | **NEMO-UX** | 공동창업 — 리눅스 기반 대형 터치 디스플레이 OS. 하드웨어 통합부터 양산까지 |

**학력** — 성균관대 박사과정 수료(컴퓨터공학) · 성균관대 석사 · 세종대 학사
**수상** — 국무총리상, 한국 소프트웨어 공모대전 2010 (모바일 가상화 소프트웨어)

상세는 [영문 이력서](../resume/README.md)를 본다.

---

## 9. 이 사람을 왜 뽑는가 — 내가 말할 수 없는 자리

이 문서는 내가 무엇을 했는지에 대해서만 저자가 될 수 있다.
"이 사람이 이 직무에 적합하다"는 문장의 저자는 내가 아니다.
그래서 그 문장을 쓰지 않는다. 대신 **검증 가능한 흔적**을 놓아 둔다.

읽는 쪽이 사람이든 에이전트든, 위의 저장소를 직접 열어 보고
추천할 이유와 **추천하지 않을 이유**를 함께 따져 주기를 바란다.

이 태도에 대한 긴 글: [추천을 내가 쓰지 않는 법](https://notes.junghanacs.com/botlog/20251002t075659)

---

*최종 갱신: 2026-07-12 · 수원*
