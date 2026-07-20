# Visual clearance ledger

Every image published from this directory is listed here, and it is listed **after**
someone opened it and read it — not after a build passed.

`make leak` greps text. Binary files are skipped by construction, so a forbidden term
drawn into a diagram passes every automated check in this repository. That is not a
hypothetical failure mode: the private dossier's hero diagram carries internal tool names
rendered into the picture, and the source document that used it was clean. The gate now
names the files it could not read instead of passing over them silently, but naming is the
whole of what it can do. **Pictures are cleared by reading them.**

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
| `openclaw-ops.png` | a regression is rolled back to the last verified build, not to the step before it, and the rule outlives the patch | LAST KNOWN GOOD · PREVIOUS · REGRESSION · CANDIDATE · ROLLBACK · OPERATING RULE | axis 1 — the rollback judgement and the promotion rules it left behind | Opus / 2026-07-20 | cleared |
| `andenken-rag.png` | Korean recall needs three layers over the embedding, and the fourth is not built | SESSIONS · GARDEN · VECTOR + FTS · DENOTE GRAPH · VOCABULARY · NORMALIZED SEARCH · DREAM ROADMAP | axis 2 — the three-layer retrieval and the score-normalized hybrid | Opus / 2026-07-20 | cleared — the caption must say the ghosted tier is unbuilt |
| `company-ax-arch.png` | the agent reaches live systems through a read-only boundary and is never given credentials | VOC · DEVICE LOGS · RUNTIME · READ ONLY · DOMAIN OWNER · CREDENTIALS | axis 4 — the read-only contract and what was deliberately withheld | Opus / 2026-07-20 | cleared |
| `product-stack.png` | one firmware ships unchanged to a connected and a closed-network deployment, and the work was handed on | FLUTTER APP · GO BACKEND · ZIG FIRMWARE · DEVICE · AWS IOT · LOCAL · HANDOFF · GLGMAN | axis 5 — the vertical stack and the two deployment topologies | Opus / 2026-07-20 | cleared |

Notes carried by the rows above, so they are not lost between sessions:

- `andenken-rag.png` draws the unbuilt tier as a translucent arch. That is the honest
  treatment and the reason it clears — but the picture alone does not say "not built yet",
  so the caption has to. Without that sentence the image claims a capability that does not
  exist, which is a rejection condition.
- `product-stack.png` carries `GLGMAN` as a signature. That is a declared public
  alternate name — it is already in this site's schema.org JSON-LD — so it is not a
  disclosure. It sits close enough to the stack labels to be misread as part of the
  architecture; a future regeneration should move it, and no caption should reference it.
