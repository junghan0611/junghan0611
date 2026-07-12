# MATERIAL — 소재 창고

**이 파일은 완성 문서가 아니다.** 중심축은 아직 잡지 않았다.
GLG가 "이제 축 잡자"라고 할 때까지, 여기에 **주제와 검증된 사실만** 쌓는다.

- `README.md`, `portfolio.md`는 **1차 초안**이다. 축이 정해지면 다시 짠다.
- 여기 적힌 것은 전부 **실제 파일을 열어 확인한 사실**이다. 기억이나 추정으로 적지 않는다.
- 회사 비공개 사실은 여기 적지 않는다 → `PRIVATE.md`

---

## 0. 초안에서 이미 틀린 것 (반드시 반영)

| 초안의 서술 | 실제 |
|---|---|
| "React 자체는 안 썼다" (`README.md` §5.1, §7) | **틀렸다.** `butlercli/viewer/web`이 **React 19 + `@a2ui/react` 0.10.1 + `@a2ui/web_core` 0.10.3 + MapLibre GL 5.16 + Vite 8 + TS + zod**로 돌고 있다. 공백 절에서 빼야 한다 |
| A2UI를 homeagent 한 곳의 이야기로 씀 | **두 번 서로 다르게 구현했다.** homeagent=Lit, butlercli=React + `@a2ui/react` 어댑터. 두 번 다른 렌더러에 같은 개념을 얹었다는 게 진짜 증거다 |
| **openclaw를 "가족 봇"으로 읽음** | **축을 통째로 잘못 잡았다** (2026-07-13 GLG 교정). 실제 축은 **플랫폼 운영** — 2026.2.17→6.11 버전 관리, 인시던트·롤백·정책 명문화, andenken 메모리 계층, entwurf, forge-config sweeper 루프. → §2 전면 재작성 |
| 가족(아버지·아내)을 최강 증거로 배치 | **강조하지 않는다.** SLO가 실재했다는 각주로 내린다 |
| forge-config / sweeper 부재 | **JD의 "Agentic AI 활용 개발 경험"에 직격하는 소재였다.** → §4b 신설 |

---

## 1. butlercli — 가족 집사 에이전트 (개인, private repo)

**경로:** `~/repos/gh/butlercli` · 실사용자: **아내와 가족** · 표면: 텔레그램 힣봇(`@glg_junghanacs_bot`)

### 왜 이게 중요한가 (미정 — 축 잡을 때 결정)

비개발자(가족)가 매일 쓰는 에이전트다. 진짜 마감이 걸려 있다 — **2026-09-30 이사 결정**.
투자가 아니라 실제로 살 집을 고른다. 실패하면 가족이 손해를 본다.

### 아키텍처 (docs/butler-kit-architecture.md — 확인함)

```
butlercli (Clojure core + agent skill)
├── core       오케스트레이터 + store contract + 공통 명령 표면
├── kits       home / estate / finance / education / ceremony
├── adapters   real-estate · school · geo-map · finance-data · gogcli · naver-capture
└── surfaces   CLI · agent skill · 지도 뷰 · 텔레그램
```

설계 원칙 6개 중 인용할 만한 것:

1. **Clojure core가 본체, skill은 표면이다** (voscli 패턴). 도메인 결정과 계산은 CLI 안에
2. **상태는 컨텍스트가 아니라 store에 남긴다.** 에이전트가 기억을 들고 있지 않아도 store만 보면 복원된다
3. **본체는 adapter contract만 가진다.** 외부 API를 본체에 흡수하지 않고 어댑터 경계로 격리
5. **봇은 사용자 + 검수자, 호스트 에이전트가 구현자다.** 힣봇은 도메인을 쓰고 검수하고, 실제 구현은 Claude Code가 한다

→ 5번이 **AX 전환의 역할 분담 모델** 그 자체다. 축 잡을 때 살릴 것.

### A2UI 뷰어 (viewer/ — 확인함)

**스택:** React 19.2 · `@a2ui/react` 0.10.1 · `@a2ui/web_core` 0.10.3 · MapLibre GL 5.16 · Vite 8 · TypeScript 6 · zod · Ajv · oxlint

**계약 구조:**

```
EstateSurfaceIR (JSON Schema 1장 = SSOT)
   ├─ Python: jsonschema / Pydantic
   └─ TS:     Ajv
        ↓ irToA2uiV09() (순수 변환)
   A2UI v0.9 message → MessageProcessor → A2uiSurface
```

- 계약 SSOT는 `schemas/estate-surface-v0.1.schema.json` **1장**. zod로 미러링하지 않는다
- 골격 4층: `builders.ts` · `irToA2uiV09.ts` · `catalog.ts`(basic + EstateTable/EstateMap 2 custom leaf) · App
- **안정축 = 2 custom leaf.** provider·표 UX는 render 내부에서만 교체
- 1차부터 박은 durable 자리: `metadata.revision`(증가만, 409는 2차), stable `candidate.id`/`marker.id`

**검증 순서 정책 (viewer/README §0) — 이 규율 자체가 소재다:**

1. 우리 손 local 검증 (봇 제외) — `curl POST → browser GET` 루프를 사람이 닫는다
2. Oracle 배포 — `estate.junghanacs.com`
3. 봇 통합 — 힣봇이 같은 서버로 POST

> **"힣봇은 1·2차에서 잊는다. 검증된 루프에 붙는 client일 뿐."**

에이전트를 먼저 붙이지 않는다. 루프를 사람이 먼저 닫는다. → AX 도입 실패 패턴에 대한 답.

### 외부 데이터 연동 (SKILL.md — 확인함)

- 아파트 실거래가: **data.go.kr 국토교통부**
- 법정동 코드: **data.go.kr 행정표준**
- 학교: **NEIS 학교정보**
- 지오코딩: **Kakao Local**

공공데이터 API를 에이전트가 쓸 수 있는 형태로 정규화한 사례. 스킬 스크립트 7개 (Python).
**"동네 가격 질문에 기억으로 답하지 마라. 스크립트가 실데이터를 조회할 수 있으면 그걸 써라"** — SKILL.md의 지시문.

---

## 2. openclaw — 에이전트 플랫폼 운영 (진짜 축. 2026-07-13 GLG 교정)

> **GLG 교정:** "openclaw 가족 봇 활용은 약해. 강조할 이야기는 아니야."
> 강조축은 **① 6개월 가까이 버전업을 관리하며 운영, ② andenken 시맨틱 메모리 계층을
> 가져와 로컬 세션·지식베이스 임베딩으로 활용, ③ 그게 entwurf로 이어지고,
> ④ forge-config에서 forgejo 개발 루프의 베이스가 되고, ⑤ 메이저 프로젝트를 주목하며
> sweeper 루프로 개발 에이전트를 운영하는 데까지 갔다.**

**경로:** `~/repos/gh/nixos-config/docker/openclaw` (public 구조면), `~/repos/gh/openclaw-config` (private runtime)
**운영 추적 SSOT:** llmlog `20260421T095342` — *§openclaw 업그레이드 추적 — 리포별 영향 히스토리*

### 2.1 업스트림 추적과 버전 운영 — 이게 JD 첫 줄이다

JD 주요업무 1번 = "AX 전환을 위한 시스템 인프라 구축, **관리** 및 서비스 설계, 개발, **운영**".
그 답이 여기 통째로 있다.

| 항목 | 값 (확인함) |
|---|---|
| 도입 → 현재 | **2026.2.17 → 2026.6.11** (약 5개월, 20+ 버전 사이클) |
| 호스트 | Oracle Cloud ARM (aarch64), Docker |
| `openclaw-config` 커밋 | **134** (2026-01 이후) |
| 채널 | Telegram 6 · Discord · Mattermost |
| 업스트림 유지자 | **1인(피터)** — *우리 쪽에 upstream 담당자가 없다* |

llmlog 원문의 규칙 문장이 이 축의 논지 그 자체다:

> "openclaw upstream은 피터 1인 유지 — 우리 쪽에 upstream 담당자가 없다.
> 즉 nixos-config가 사실상 openclaw 운영 담당이고, **업스트림 변경 의미는 여기서 재해석해야 산다.**"

그래서 만든 것이 **리포별 영향 번역 문서**다. upstream 릴리즈 노트를 내 리포(nixos-config /
agent-config / andenken / openai-codex) 관점으로 번역해 "여기 봐야 해" 시그널을 남긴다.
→ **"AI 관련 문서(가이드·위키) 작성·배포"가 이미 내 운영 습관이다.** 주요업무 2번의 증거.

### 2.2 인시던트 2건 — 서류에 넣을 하드 증거 (llmlog 확인함)

**① 2026-04-28 EMERGENCY ROLLBACK 4.26 → 4.23 (lazy-staging 인시던트)**

| 단계 | 내용 |
|---|---|
| 증상 | 4.24→4.26 two-version jump 후 응답 latency 급증. `stuck session: state=processing age=164s` |
| 계측 | gateway PID **102% CPU spinning** (단일 node thread, no child spawn). 부팅 **88s** (4.23은 11s) |
| 가설 배제 | **fresh boot에서도 재현** → operator config 오류가 아님을 입증 (TTS config 추가 *전* 발현) |
| 근본 원인 가설 | 4.25 cold-persisted plugin registry ↔ `doctor --fix` 충돌 → registry rebuild가 active plugin 7→3 축소 → 첫 inbound가 **hot path 한복판에서 npm install 트리거** |
| 롤백 타깃 선택 | 4.22가 아니라 **4.23** — 이미지 생성이 `gpt-image-2`를 Codex OAuth flat-rate로 라우팅(#70703). 4.22는 별도 API key 필요. **4.23 = latest known-good** |
| 검증 | ready 11.3s, plugins 6, CPU 0.07% idle, stuck-session 진단 0 |
| **정책 명문화** | no two-version jumps · wait-and-watch · **비프로덕션 에이전트에 먼저 ≥24h stage 후 승격** · `stuck session` 한 줄도 pause 사유 · **응답성이 SLO, 체감 latency = P0** |
| 비용 | 운영자 attention **5시간** |

**② 2026-05-03 v5.2 직행 — 업스트림 릴리즈 노트에서 내 인시던트의 정공법 fix를 식별**

upstream 5.2 릴리즈 노트에서 이 두 줄을 찾아냈다:

> `Plugins/runtime: scope broad runtime preloads to the effective plugin ids derived from config…`
> `Tools/plugins: cache plugin tool descriptors… so repeated prompt-time planning can skip plugin runtime loading` (#76079)

4.29 재시도 → **10분 만에 동일 인시던트 재현** → 5.2 직행 결정.

| 지표 | before | after |
|---|---|---|
| 부팅 | 45.4s | **7.3s** → hardening 후 **5.8s** |
| 메모리 | 816 MiB (4.23) | **246 MiB** |
| hot path `staging bundled runtime deps` | 발생 | **0** |

동반: ACPX 운영 retire, dangling/stale 세션 정리(72 → 16),
hardening = `NODE_COMPILE_CACHE` + `OPENCLAW_NO_RESPAWN`.

**③ 6.9 strict plugin discovery** — 죽은 `plugins.load.paths`(pi-shell-acp 잔재) hard-fail →
crash loop → surgical 제거로 복구. config warnings 0.

### 2.3 판단의 규율 — 도구의 권고를 검증 없이 따르지 않는다

`doctor`의 보안 권고(credentials chmod 700 / gpt-image-2 교체 / 멀티유저 위험)를
**우리 deployment context에서 false positive로 검증하고 미적용**했다. llmlog 원문:

> 사용자 피드백 "이유 모른 채 무조건 따르면 위험" → 메모리 저장
> (`feedback_security_advice_validation.md`)

`doctor --fix`도 미사용 — 설정 재작성 위험 때문. 결과 gemini 드리프트 0.
→ **AX 도입에서 가장 흔한 실패(도구가 시키는 대로 함)에 대한 실증적 반례.**

### 2.4 계보 — 하나의 세로축으로 이어진다 (여기가 서류의 등뼈)

```
openclaw 운영 (업스트림 추적 · 버전 · 인시던트 · 메모리 계층)
   │
   ├─→ andenken     메모리를 분리해 독립 계층으로. openclaw builtin md memory 로직 +
   │                 LanceDB 백엔드 → 로컬 세션 임베딩 + 지식베이스(가든) 임베딩
   │
   ├─→ entwurf      openclaw/pi 운영 경험이 dispatch substrate로
   │
   └─→ forge-config forgejo 개발 루프. openclaw를 베이스로 쌓음 →
                     forgebot · auto-fix 레인 · sweeper 루프
```

**"에이전트 하네스를 쓴 사람"이 아니라 "에이전트 플랫폼을 운영하고, 그 위에 자기 계층을
쌓아 올린 사람"이다.** 이 계보가 서류의 세로축이 되어야 한다.

### 2.5 주의 (유지)

- `openclaw-config`가 private인 이유 = **봇의 기억이 그 안에 산다**.
- OpenClaw는 상류 소프트웨어. **내 것은 운영층 · 메모리 계층 · 개발 루프**다. 이 구분을 흐리지 말 것.
- llmlog의 SLO 문장이 "가족 봇 응답성"으로 되어 있다 → 서류에서는 **"실사용자 트래픽 SLO"**로
  번역한다. 가족을 강조하지 않되, **SLO가 실재했다는 사실**은 남긴다.
- ⚠️ `openclaw-config/README.md`의 *Current environment*가 **6.9로 stale** (실제 6.11).
  서류에 수치 인용 전 재확인할 것.

---

## 3. RAG — 스펙을 정확히 (andenken README 확인함)

초안의 RAG 서술이 뭉뚱그려져 있다. 실제 스펙:

### andenken — 메모리 축 3개

```
active memory  │ 답변 전 차단형 리콜. 하네스 쪽 (pi-extensions / openclaw 플러그인 패턴).
 (recall)      │ 타임아웃 경계, 실패 시 graceful degrade. andenken을 백엔드로 소비.
               │ ── 이 리포에 미구현 ──

embedding      │ ← 이 리포.
 (semantic)    │ 벡터 + BM25 하이브리드 검색.
               │ Sessions: Qwen3-Embedding-8B (4096d)
               │ MD (공개 가든 export): Qwen3-Embedding-8B (4096d)
               │ Org: 4B/2560d — 현재 비활성 (상류 R&D)
               │ 라이브 트랙 2개: sessions, md

dream          │ 야간 통합. 최근 기억을 증류 단위로 압축. 별도 축, 별도 로드맵.
 (consolidation)│ ── 미구현 ──
```

- **LanceDB** + 하이브리드 리트리벌 (vector + FTS, **score 정규화**)
- 한↔영 크로스링궐은 **dictcli expand** 경유
- **recall tracking** — 기억 통합(consolidation)을 위한 회수 추적

→ "RAG 파이프라인(청킹·임베딩·벡터DB·검색 품질)" 요구에 1:1로 답할 수 있는 자리.
→ 특히 **메모리를 세 축으로 갈랐다**는 게 일반 RAG 스택과 다른 지점.

### 회사 쪽 (botlog가 언급 — PRIVATE에 상세)

- **reranker-server** — 리랭킹 단 직접 서빙
- **notion-embedding** — 임베딩 단 직접 서빙
- Supabase pgvector, 문서 임베딩 2,945건, n8n 40+ 노드

### 정직한 프레이밍 (botlog 원문)

> **파인튜닝(LoRA) 중심은 아닙니다. 정직하게 밝힙니다.**
> 대신 임베딩 서빙·리랭킹·검색 품질 최적화·프롬프트/체인 설계라는
> **실서비스 최적화 축**에서 강합니다.

이 문장 그대로 살릴 것.

---

## 4. 레거시 시스템 연동 Agent (JD의 숨은 축)

초안에 이름이 빠졌다. 회사 도구 두 개가 정확히 이 축이다.

- **incidentcli** (Clojure) — IoT 클라우드 플랫폼 DDL 카탈로그 · DMS 쿼리 플래너 ·
  디바이스 로그 · StarRocks 런타임 미러를 **단일 KST 시간축**으로 회수·정렬.
  덤프를 저장하지 않는 **read-only** 증거 도구.
- **voscli** — VOC/상담 데이터를 에이전트가 다룰 형태로 정규화.
  단위·기간·포함정책 고정, 근거를 개별 대화 id까지 역추적.

> "이미 돌아가는 낡은 시스템에 에이전트 접점을 붙여, 자연어를 실데이터로 회수한다."

→ JD 우대사항의 "DB·MQ·컨테이너 이해"보다 **한 층 위**의 답이다.
→ 추천서의 *"이미 쓰고 있는 낡은 시스템에 AI를 붙여서 실제 업무 데이터를 활용하게 만드는 일"* 과 직결.

---

## 4b. forge-config — 개발 에이전트 루프와 sweeper (2026-07-13 신설)

**경로:** `~/repos/gh/forge-config` (public) · 셀프호스팅 **Forgejo** · 봇: `forgebot`
**계보:** openclaw를 베이스로 쌓음(§2.4). botment(가든 댓글면)의 **코드면 자매**.

### 운영 루프 (README — 확인함)

```
도메인 오너가 도메인 봇과 대화 (예: vocbot)
  → 대화가 서버에 JSONL로 기록
  → 요구/버그/반복되는 고통이 감지됨 (봇 또는 sweeper)
  → 라벨 + 소스 컨텍스트를 달아 Forgejo 이슈 생성
  → forgebot이 라벨/웹훅으로 깨어남
  → forgebot이 해당 owner agent에게 read-only 1차 리뷰를 요청
  → owner agent가 reality check · owner repo · risk · scope ·
     구현필요여부 · 우선순위 · 코멘트 요약을 반환
  → forgebot이 리뷰를 Forgejo에 기록하고 triage 사이클 종료
  → GLG가 정렬된 백로그를 보고, focused batch로 구현을 부른다
```

### 설계에서 **하지 않기로 한 것** — 여기가 진짜 값어치다

README가 명시적으로 박아둔 non-goal:

> ❌ 자동 코딩 factory · ❌ 운영팀용 대시보드 제품 · ❌ GLG가 무엇을 구현할지 정하는 걸 대체하는 것
> "요점은 'AI가 어딘가에서 코드를 쓴다'가 아니다. **durable context · 명시적 소유권 ·
> 리뷰 가능한 흔적**을 가진 에이전트 네트워크다."

- `forgebot`은 **dispatcher/recorder이지 implementer가 아니다.**
- `agent:done`은 **1차 리뷰 triage 완료**이지 **구현 완료가 아니다.**
- 자동화의 초기 타깃은 **capture + first review + sorting**. 구현은 나중에 GLG 주도 배치로.

→ GitHub Copilot·호스팅 코딩 에이전트를 타깃으로 삼지 **않은** 이유를 문서로 설명할 수 있다.
→ **AX 도입 실패의 전형(에이전트에게 구현을 통째로 맡김)에 대한 설계적 답.**

### sweeper / auto-fix 레인 — 안전 문법 (ROADMAP — 확인함)

ClawSweeper의 **safety grammar**를 의도적으로 차용하되, 제품 파이프라인은 복사하지 않았다:

| 차용한 것 | 복사하지 않은 것 |
|---|---|
| conservative default · **review-before-mutation** · durable report · marker-backed comment · **snapshot drift guard** · deterministic mutation gate | Plan/Review/Apply 제품 파이프라인 · GitHub-scale 기계 |

**상태 권위(state authority) 설계 — 면접에서 먹힐 디테일:**
template marker가 `schema` · `report_id` · `session_key` · `issue_updated_at` ·
lifecycle/sorted 라벨 · provider/model · forge-config commit을 기록한다.
목적은 하나 — **"OpenClaw 세션 메모리와 웹훅 replay가 현재 Forgejo 상태를 절대 이기지 못하게."**
→ 에이전트의 기억보다 durable store가 권위를 갖는다. §1의 butlercli 원칙 2와 같은 규율.

### 실증 착지 (NEXT.md — 확인함)

- **auto-fix v0 GREEN**: `sandbox#13`, `voscli#15` — `agent:ready + auto-fix` → report skeleton →
  `agent:done + auto-fix`. **replay/idempotency smoke에서 리포트 중복 생성 없음.**
- **v1 seed GREEN**: `voscli#14` bounded workspace guard patch 수행 + 리포트 기록 /
  `voscli#16` `rg` no-match를 또 하나의 nonfatal sweep case로 노출 / `voscli#17` post-fix 회귀 통과.

### 책임 경계 (NEXT.md 원문)

> OpenClaw는 transport/runtime/auth/model/gateway/lifecycle wiring을 **"forgebot이 깨어날 때"까지**
> 소유하고, forge-config는 **lifecycle protocol · auto-fix semantics · sweeper semantics ·
> validation loops · follow-up issue rules**를 소유한다.

→ 상류/내 것의 경계를 문장으로 그을 수 있다는 것 자체가 플랫폼 운영자의 표식이다.

---

## 5. 이 직무의 진짜 정체 (GLG의 판단 — 축 잡을 때 반영)

> "백엔드라고 이름은 들어가 있는데? 이게 거의 **사내 AX 전문가** 뽑는 거 아니야? 교육 문서 이런 것도?"

동의한다. 공고 제목은 "AI 전환 백엔드 개발"이지만 주요 업무 두 줄 중 하나가
**"그룹사 AI 관련 문서(가이드, 위키 등) 작성, 배포 및 교육 활동"**이다.
즉 **빌드 + 전파·인에이블** 이중 직무다.

힣봇의 지원 메모(botlog `20260331T172313`)도 같은 결론:

> 유일한 자기 점검: **"빌드 중심"인가 "전파·인에이블 중심"인가.**
> 2번(AX 백엔드)은 문서·교육 비중이 있음 — 힣의 가드너 기질엔 오히려 맞을 가능성.

**하지만 "빌드"의 정체를 잘못 읽고 있었다 (2026-07-13 GLG 교정).**

이 직무가 말하는 빌드는 "AI 기능이 붙은 백엔드 서비스를 만든다"가 아니라
**"에이전트 플랫폼을 세우고, 관리하고, 운영한다"**이다. 그 증거의 무게중심은
가족 인에이블이 아니라 §2(플랫폼 운영) + §4b(개발 에이전트 루프)에 있다.

| 축 | 증거 | JD 대응 |
|---|---|---|
| **플랫폼 운영** | openclaw 2026.2.17→6.11, 20+ 버전 사이클, 인시던트 2건 + 롤백 판단 + 정책 명문화 | 주요업무 ① *인프라 구축·관리·운영* |
| **메모리 계층** | andenken — 세션 임베딩 + 지식베이스 임베딩, LanceDB, 하이브리드 리트리벌 | 우대 *LLM·RAG 이해* |
| **개발 에이전트 루프** | forge-config — forgebot · auto-fix · **sweeper**, idempotency/replay 안전 | 자격 *Agentic AI를 활용한 개발 경험* |
| **문서·전파** | 업스트림 → 리포별 영향 번역 문서, AGENTS.md/NEXT.md 문서 계약, 가든 2,200+ | 주요업무 ② *문서 작성·배포·교육* |
| **레거시 연동** | incidentcli · voscli (도메인 오너 에이전트) | 추천서의 *"낡은 시스템에 AI를 붙여"* |

→ 대부분의 지원자는 **"Claude Code를 써봤다"**로 끝난다.
→ 여기엔 **에이전트 하네스를 5개월간 프로덕션으로 운영하며 20+ 버전을 올리고, 회귀를 계측해
   롤백하고, 메모리 계층을 갈아끼우고, 그 위에 개발 에이전트 루프를 세운** 기록이 있다.
→ 가족은 **축이 아니라 SLO가 실재했다는 각주**로 내려간다.

---

## 6. 아직 안 캔 광맥 (다음에 확인할 것)

- [ ] **pi-shell / pi 하네스** — botlog가 "ACP 셸·런타임을 직접 만들었다"고 함. entwurf의 전신.
      README에는 "pi-shell-acp에서 자라 나왔다"고만 있음. 별도 서술 가치 있는지 판단 필요
- [ ] **geworfen Track 1 / jacobian-lens** — "하네스가 협업을 바꾸는가"를 측정하려는 연구 축.
      채용 서류에 넣을지 말지는 축 잡을 때 결정 (넣으면 강하지만 산만해질 위험)
- [ ] **legoagent-config** — 체현된 토이 에이전트. 교육/데모 소재로 쓸 수 있는지
- [ ] **logickocli** — 한국어 논증 ↔ 논리 좌표계. AX와 직접 관계는 약하나 독창성 증거
- [ ] **durable-iot-migrate** — Temporal + Saga, Clojure가 Go보다 62% 적은 코드.
      "레거시 이관" 축에 붙일 수 있음
- [ ] **회사 GPU 클러스터 / n8n / Airbyte** 상세 — 초안에 있으나 얕음
- [ ] **PSIRT** — 제품 보안 대응. AX와 직접 관계는 약하나 "혼자서 새 역할을 만든다"의 증거
- [ ] **NEMO-UX 공동창업 (2013~2017)** — 리눅스 대형 터치 디스플레이 OS 양산.
      "펌웨어부터 제품까지"의 첫 번째 사례. 초안에서 한 줄로 눌려 있음
- [ ] **두 번째 공고 (LLM 기술 개발 / LLM서비스개발팀)** — 힣봇 메모가 2순위로 둠.
      AX 서류가 이 공고에도 쓰이는지, 별도 컷이 필요한지

---

## 7. 축 — 2026-07-13 GLG 교정으로 대부분 확정됨

### 확정 (GLG 발언 기준)

1. **중심축 = 에이전트 플랫폼을 운영하고 그 위에 자기 계층을 쌓는 사람.**
   세 후보("펌웨어→앱 세로축" / "사람에게 붙이는 사람" / "하네스를 만드는 사람") 중
   **어느 것도 아니었다.** 실제 축은 §2.4의 계보다:
   **openclaw 운영 → andenken(메모리) → entwurf(디스패치) → forge-config(개발 루프·sweeper).**
2. **가족 이야기 = 축이 아니다.** ("openclaw 가족 봇 활용은 약해. 강조할 이야기는 아니야.")
   SLO의 실재성만 남기고, 서사의 무게는 빼기. → Q2 해소.
3. **펌웨어→앱 세로축은 추천서가 이미 맡았다.** 서류가 같은 자리를 또 밟으면 낭비다.
   PRIVATE.md의 원칙(*"추천서와 서류가 같은 사실을 다른 자리에서 가리키게 둔다"*)을
   축 결정에 확장 적용한 결과. SKS Hub는 **배경 신뢰도**로 쓰되 중심에 두지 않는다.

### 남은 결정 (GLG가 답할 것)

- [ ] **Track 2(만남·1KB 공개키)를 넣을 것인가.**
      권고: ①② PDF에는 넣지 않고, **인터랙티브 판의 마지막 층에 링크로만.**
      jacobian-lens 서베이의 아치와 동형 — *"문의 이야기는 하되 열지 않는다."*
- [ ] **분량.** 권고: ① 3~4장(압축) · ② 8~10장(상세) · ③ md/인터랙티브는 상한 없음.
- [ ] **두 번째 공고(LLM 기술 개발)** 를 같은 소재로 커버할 것인가, 별도 컷을 낼 것인가.

---

## 8. 형식 — 인터랙티브 문서 (2026-07-13 GLG 결정)

**org SSOT 한 장 → `make`로 제출물 3종 전부.** 노트 `20251021T105353`의 명제
(*"org=SSOT, LaTeX/Typst 없이 인터랙티브 문서 생성"*)를 채용 서류에 적용한다.

| 제출물 | 산출 경로 |
|---|---|
| ① 역량·성과 기술서 **PDF** | org → `build.el` → acmart → PDF |
| ② 포트폴리오 **PDF** | 〃 |
| ③ 상세 **md** | org → pandoc → md |
| (+) 인터랙티브 HTML | org → pandoc `--citeproc` → 자기 도메인 게시 |

파이프 레퍼런스: `jacobian-lens/survey/Makefile` · `geworfen/docs/paper/Makefile`
(둘 다 memex-kb `paper_build.el` 벤더링. 검증 baseline = jacobian-lens).

**왜 이게 축과 맞물리는가:** JD 주요업무 ②가 "AI 문서 작성·배포"다.
서류가 그걸 *주장하는* 대신, **서류가 만들어진 방식이 그 주장이 된다.**
T인터뷰(라이브 코딩 + Claude Code)에서 `make`를 돌려 제출물을 재생성해 보이면
서류와 면접이 한 줄로 이어진다.

---

*갱신: 2026-07-13 — GLG 교정(openclaw 축 재정의) + 인터랙티브 문서 형식 결정 반영*
