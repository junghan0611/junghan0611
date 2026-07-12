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

## 2. openclaw — 4년째 돌고 있는 봇 생태 (가장 저평가된 소재)

**경로:** `~/repos/gh/nixos-config/docker/openclaw`, `~/repos/gh/openclaw-config` (private)

### 운영 스냅샷 (README — 확인함)

| 항목 | 값 |
|---|---|
| OpenClaw | 2026.4.22 |
| 호스트 | **Oracle Cloud ARM (aarch64)**, 커널 6.19.12 |
| 채널 | Telegram **6개** — default · glg · gpt · gemini · mini · bbot |
| ACP backend | `acpx` (maxConcurrentSessions: 3) |
| 기본 모델 | `openai-codex/gpt-5.4` |
| 세션 격리 | `per-account-channel-peer` (사용자별 독립 세션) |
| 세션 통신 | `sessions.visibility: agent` (같은 에이전트 내 크로스 세션 허용) |

### 이 줄이 핵심이다 (README 원문)

> **시나리오**: 아버지가 glg 봇에게 질문 → 봇이 답변 불가 판단 → 정한 세션으로
> **에스컬레이션** → 정한이 개입/답변 → 결과가 아버지 세션으로 전달

**비개발자 사용자 + 에이전트 + 실패 시 전문가 에스컬레이션.**
그룹사 AI 인에이블먼트가 하는 일이 정확히 이 구조다.
대부분의 지원자는 "교육 경험 있습니다"로 끝난다. 여기엔 **아버지와 아내가 매일 쓰는 시스템**이 있다.

### 왜 만들었는가 (README 원문 — 세계관 축)

- 봇이 나의 지식베이스를 읽는다 — 노트 3,000+, 서지 8,000+
- 봇이 나의 활동을 안다 — 코딩 히스토리, 건강 데이터, 시간 추적
- **봇이 가족을 돕는다** — 아버지가 봇에게 묻고, 막히면 나에게 에스컬레이션
- 봇이 기록을 남긴다 — 대화와 리서치를 Denote 파일로 직접 작성 (**botlog**)

> "범용 AI가 '나의 닮은 존재'로 전환되려면, 나의 데이터에 접근하는 도구가 필요하다."

### 주의

`openclaw-config`가 private인 이유 = **봇의 기억이 그 안에 산다**. 이건 이미 프로필 README에 서술됨.
OpenClaw는 상류 소프트웨어이고, **내 것은 배포 층과 botlog 실천**이다. 이 구분을 흐리지 말 것.

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

## 5. 이 직무의 진짜 정체 (GLG의 판단 — 축 잡을 때 반영)

> "백엔드라고 이름은 들어가 있는데? 이게 거의 **사내 AX 전문가** 뽑는 거 아니야? 교육 문서 이런 것도?"

동의한다. 공고 제목은 "AI 전환 백엔드 개발"이지만 주요 업무 두 줄 중 하나가
**"그룹사 AI 관련 문서(가이드, 위키 등) 작성, 배포 및 교육 활동"**이다.
즉 **빌드 + 전파·인에이블** 이중 직무다.

힣봇의 지원 메모(botlog `20260331T172313`)도 같은 결론:

> 유일한 자기 점검: **"빌드 중심"인가 "전파·인에이블 중심"인가.**
> 2번(AX 백엔드)은 문서·교육 비중이 있음 — 힣의 가드너 기질엔 오히려 맞을 가능성.

**전파·인에이블 축의 증거는 이미 다 있다:**

| 증거 | 대상 |
|---|---|
| openclaw 6채널 + 크로스세션 에스컬레이션 | **아버지** (비개발자) |
| butlercli estate 키트 | **아내** (비개발자, 실제 이사 결정) |
| 사내 도메인 오너 에이전트 (VOC/인시던트) | **운영팀** (비개발자, 매일 아침 읽음) |
| 가든 2,200+ 페이지 · AGENTS.md/VOCABULARY.md/NEXT.md 문서 계약 | 사람 + 에이전트 |
| 40+ 스킬 | 다른 에이전트 |

→ **"에이전트를 사람에게 붙여본 횟수"가 남들과 다르다.** 축을 여기 놓을지 GLG가 결정.

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

## 7. 축 잡을 때 물어볼 것 (GLG에게)

1. **중심을 어디 둘 것인가** — "펌웨어부터 에이전트 루프까지의 세로축"인가,
   "에이전트를 사람에게 붙이는 사람"인가, "하네스를 만드는 사람"인가?
   지금 초안은 첫 번째로 서 있는데, 이 직무는 두 번째를 산다.
2. **가족 이야기(아버지·아내)를 서류에 쓸 것인가.** 가장 강한 증거인 동시에
   가장 사적인 이야기다. 공개면에 어디까지 올릴지 GLG가 정해야 한다.
3. **Track 2(만남·1KB 공개키)를 넣을 것인가.** 넣으면 이 사람이 누군지 드러나고,
   빼면 그냥 잘하는 엔지니어가 된다. 위험과 이득이 둘 다 크다.
4. **분량.** ①은 압축, ②는 상세. 지금 ①이 369줄인데 PDF로 몇 장이 적당한가.

---

*갱신: 2026-07-12*
