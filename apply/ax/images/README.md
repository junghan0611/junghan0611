# Visual clearance ledger

Every image published from this directory is listed here, and it is listed **after**
someone opened it and read it — not after a build passed.

`make leak` greps text. Binary files are skipped by construction, so a forbidden term
drawn into a diagram passes every automated check in this repository. The gate now names
the files it could not read instead of passing over them silently, but naming is the whole
of what it can do — and a named file still ships unless somebody opens it.

This is the blind spot that matters most for diagrams specifically, because a diagram is
where a name is most likely to appear *without the author noticing*: it is drawn once from
a prompt, reviewed as a picture, and then carried into a document whose prose was written
under the denylist. The text gate reads the prose and reports a clean run. **Pictures are
cleared by reading them.**

The clearance question is never "does this image contain a string that looks internal" —
it is "does what is legible here identify an organisation, a customer, or a private
system". A functional name that describes what a tool does is not, by itself, an
identifier; a name that only exists inside one company is. That line is a judgement, it is
recorded per-row below with who made it, and it is not delegated to a grep.

## What clearance means

The reviewer opens the **final optimized file that would ship** — not the master, not an
earlier revision, not the prompt that produced it — and rejects it if any of these is
visible:

- an identifiable organisation, customer, or internal tool name
- a credential, host, path, or identifier belonging to a private system
- invented or corrupted strings (a generated diagram will happily letter a protocol that
  does not exist)
- a structure that disagrees with what the surrounding text claims
- a state ahead of what is actually implemented

A generated image is an explanatory panel, never the evidence. The claim is owned by the
caption and by the public surface cited next to it; if the picture were removed, the
argument must still stand on the link.

Rejected files are not copied into this repository at all. This ledger records approvals,
and it never spells out the term that caused a rejection — a ledger that names what it
forbids publishes it, the same reason the denylist itself is gitignored.

## Ledger

One row per file that is actually in this directory and cleared to ship. Nothing else
belongs here — not candidates, not rejections, not the reasons behind them. A public list
of what was turned away is itself a disclosure: it says which pictures of this work exist
and hints at what is in them. Review state lives in the session handoff, which is not
published.

An image may not be referenced from `ax.org` until it has a row here.

| file | depicted claim | visible labels checked | factual source | cleared by / date | status |
|---|---|---|---|---|---|
| `company-ax-layer.png` | one flow runs from a person's own knowledge practice to an organisation's agent surface, and the person keeps the orchestrator's judgement | 개인지식관리(PKM) · NixOS · Emacs · config · OpenClaw · andenken · entwurf · forge-config · 세션 · 지식베이스 · switch · AGENTS.md · NEXT.md · 스킬 계약 · 회사 도메인에 착지 · VOC·상담 · 운영 장애 · IoT·로그 · 읽기 전용·증거 우선 · voscli · incidentcli · 담당자가 owner · agent · 개발자 · 비개발자 · Embedded Linux · Backend · App · Cloud · 보안 경계 | the d1 overview — the five axes as one lineage, and the crosscutting documentation axis | Opus (read) / GLG (disclosure) / 2026-07-20 | cleared — see the note below on the two functional tool names |
| `openclaw-ops.png` | a regression is rolled back to the last verified build, not to the step before it, and the rule outlives the patch | LAST KNOWN GOOD · PREVIOUS · REGRESSION · CANDIDATE · ROLLBACK · OPERATING RULE | axis 1 — the rollback judgement and the promotion rules it left behind | Opus / 2026-07-20 | cleared |
| `andenken-rag.png` | Korean recall needs three layers over the embedding, and the fourth is not built | SESSIONS · GARDEN · VECTOR + FTS · DENOTE GRAPH · VOCABULARY · NORMALIZED SEARCH · DREAM ROADMAP | axis 2 — the three-layer retrieval and the score-normalized hybrid | Opus / 2026-07-20 | cleared — the caption must say the ghosted tier is unbuilt |
| `company-ax-arch.png` | the agent reaches live systems through a read-only boundary and is never given credentials | VOC · DEVICE LOGS · RUNTIME · READ ONLY · DOMAIN OWNER · CREDENTIALS | axis 4 — the read-only contract and what was deliberately withheld | Opus / 2026-07-20 | cleared |
| `product-stack.png` | one firmware ships unchanged to a connected and a closed-network deployment, and the work was handed on | FLUTTER APP · GO BACKEND · ZIG FIRMWARE · DEVICE · AWS IOT · LOCAL · HANDOFF · GLGMAN | axis 5 — the vertical stack and the two deployment topologies | Opus / 2026-07-20 | cleared |

Notes carried by the rows above, so they are not lost between sessions:

- `company-ax-layer.png` letters two tool names, `voscli` and `incidentcli`, inside the
  panel describing the landing in a company domain. **GLG read them and cleared them for
  publication**: each is a function name — a CLI over voice-of-customer records, a CLI over
  incidents — and a functional name is not an identifier. Neither the organisation nor any
  customer is named or inferable from them, and neither term is on the denylist, so the row
  ships as read. The clearance is recorded here rather than argued in the document, because
  the judgement belongs to a person and the ledger is where a person's decision is kept.
- The same panel generalises private work. The caption beside it in `ax.org` says so and
  points the weight at the five public layers to its left — a picture may explain a private
  structure, but it may never be offered as the evidence for one.

- `andenken-rag.png` draws the unbuilt tier as a translucent arch. That is the honest
  treatment and the reason it clears — but the picture alone does not say "not built yet",
  so the caption has to. Without that sentence the image claims a capability that does not
  exist, which is a rejection condition.
- `product-stack.png` carries `GLGMAN` as a signature. That is a declared public
  alternate name — it is already in this site's schema.org JSON-LD — so it is not a
  disclosure. It sits close enough to the stack labels to be misread as part of the
  architecture; a future regeneration should move it, and no caption should reference it.
