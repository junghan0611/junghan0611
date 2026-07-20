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

| file | depicted claim | visible labels checked | factual source | cleared by / date | status |
|---|---|---|---|---|---|
| _(none yet)_ | | | | | |

## Pending decisions

These are the candidates under review. They are **not** in this directory yet and must not
be referenced from `ax.org` until they appear in the ledger above.

| candidate | status |
|---|---|
| `company-ax-arch.png` | candidate — needs clearance and a caption checked against current fact |
| `openclaw-ops.png` | candidate — same |
| `andenken-rag.png` | candidate — same |
| `product-stack.png` | candidate — same |
| `platform-lineage.png` | conditional — its transport labels must be verified against the current entwurf contract, not accepted as approximately right |
| `company-ax-layer.png` | rejected — internal tool names rendered into the image |
| `entwurf-hero.png` | rejected — carries an invented protocol string, and its boundary drawing misleads |

A conditional candidate is cleared by checking the drawing against the code and the written
contract, then either adopting it or regenerating it. "Close enough" is a rejection.
