# AGENTS.md — public AX evidence dossier

This directory builds a public evidence surface for AX / agent-platform roles.
It is not an employer-specific application and it is not a research paper.

## Center

The document answers one question:

> In the last year of rapid AI change, what did the author actually build, operate,
> recover, hand over, and leave verifiable?

The answer is not tenure or self-description. It is a path from the reader's familiar
job-language into code, incidents, third-party actions, live aggregates, and a public
time-axis projection.

## Do not drift

- The Anthropic J-space paper is a **format and build baseline only**. Do not summarize,
  cite, imitate, or discuss that paper here.
- Do not turn this into `geworfen`, an academic paper, or a Track 2 manifesto.
- Do not make the local `axis.html` public. It embeds FULL titles and is deliberately
  gitignored. Only an allowlisted timeline projection may enter this document.
- Do not add a new document converter. Use Org's exporters, Pandoc, and the proven
  `memex-kb`/`jacobian-lens` build pattern.
- Do not name the employer, a referrer, an application route, a work location, or closed
  company facts. Those stay in `apply/PRIVATE.md`. This file is tracked and public, so it
  must not spell out the terms it forbids — the denylist lives in the gitignored
  `leakwords.txt` and `make check` greps it against the shipped artifacts.
- Do not claim direct use of a named framework that was not used. Map adjacent capability
  only after stating the boundary plainly.

## One document, four depths

`ax.org` is the only authored content source, and it is **one document** — not a bundle of
three. It began as an employer's three required uploads (competency statement, portfolio,
detailed Markdown), and those were their boxes, not its structure. What it actually is is a
single argument that descends from claim to ledger, so the views are **slices of one
document at increasing depth**. Nothing has to be kept in step with anything, because there
is only one thing.

| depth | what it carries | reading time |
|---|---|---|
| `d0` | the claim — who this is and what they did | 2 min |
| `d1` | the shape of the evidence — each axis and the judgement behind it | 5 min |
| `d2` | events and numbers — incidents, measurements, third-party actions, boundaries | 15 min |
| `d3` | the ledger — reproduction commands, paths, hash fingerprints, handoffs | open |

| view | depth | role |
|---|---|---|
| `build/index.html` | d0 | front door |
| `build/record.html` | d0–d3, with the dial | the document |
| `KimJunghan_AX_Overview.pdf` | d0–d1 | the wide read |
| `KimJunghan_AX_Record.pdf` | d0–d2 | the middle read |
| `KimJunghan_AX_Detail.md` | d0–d3, flat | agents, and anyone reading everything |

Generated `build/*.org`, HTML, TeX, PDF, and Markdown are derivatives. Never repair a
derivative by hand; fix `ax.org` or the build wiring.

### The invariant: depth must not decrease down the tree

Every heading carries exactly one depth tag. A cut at depth N excludes the subtrees tagged
deeper than N — `org-export-exclude-tags`, not `select-tags`, because selecting a heading
drags **all** of its descendants along and the d1 view would arrive carrying the d3 ledger.

Org inherits tags, which is what makes the cut nearly free, and it is also the trap: a `d1`
heading placed under a `d2` parent inherits `d2` and **disappears from the d1 view with no
error anywhere**. Nothing downstream notices, because a section that was cut looks exactly
like a section that was never written. So `build.el` refuses to build a non-monotonic tree,
and `make check` counts the survivors of each cut against `build/depth.json` instead of
trusting that they are all there.

Read this as an editing rule: when a depth placement feels wrong, **move the tag, not the
sentence**. Each depth has to read as a finished document on its own — if d0–d1 feels
truncated, the depths are mis-assigned, not the prose.

### The dial

`assets/depth.html` is injected before `</body>` of `build/record.html` only; the front door
is already the d0 cut. Build-time, `make` stamps `data-depth` onto each heading by walking
`build/depth.json` and the shipped headings in the same document order — a positional match,
which is exactly why `check` asserts the two counts agree rather than assuming it. Pandoc is
deliberately **not** given `--section-divs`: this stylesheet is built on flat sibling
selectors, and wrapping every heading in a `<section>` would restyle the document to buy
nesting the dial does not need.

## Head include, favicon, analytics, and llms.txt

The two HTML views carry a shared `<head>` include, `assets/head.html`, injected verbatim
before `</head>` **after** pandoc — never through it. It holds three site-level things: the
Umami analytics tag (external `<script src>`, this site's own `data-website-id`), the
schema.org JSON-LD identity graph, and a self-contained SVG favicon (data URI). It is
post-injected on purpose: `--embed-resources` would inline the Umami script and break both its
`data-website-id` and the offline/deterministic build. `make check` greps the shipped HTML for
the tag, the schema, and the icon so a silent inject failure cannot pass.

- The JSON-LD Person mirrors the garden's canonical node (same `alternateName`/`sameAs`) so an
  AI knowledge graph merges this dossier with `notes.junghanacs.com`. Keep dates static (from
  the source), never wall-clock, or `make repro` breaks.
- Caddy injects no analytics (`ax.junghanacs.com` is a plain file server); the tag lives in the
  source because the authored artifact is the SSOT. The Umami *server* and the website-id
  registration are the nixos-config maintainer's surface.
- `llms.txt` is a tracked static file (not a pandoc output). It ships to the web root as the
  sixth public file. The leak gate already scans it — it is a text file in this dir — so it is
  gated like every other surface. Turning on Umami's public "share URL" is declined: it would
  expose visitor referrers (an application route), which the leak gate cannot scrub.
- `robots.txt` and `sitemap.xml` ship the same way — static files authored here, not pandoc
  outputs, gated by the same leak scan, and copied to the web root by `make publish` (eight
  public files now, not six). The sitemap lists the five views and `llms.txt` — not itself or
  `robots.txt` — and carries no `<lastmod>`, so two clean builds stay byte-identical.

## Reading sequence

The deep record follows the role's vocabulary in this order:

1. Main work: AX infrastructure build/manage/design/develop/operate; documentation,
   distribution, and education.
2. Qualifications: Linux; Claude Code/Codex and Agentic AI; backend systems; AX in
   development and non-development domains.
3. Preferred capabilities: web frameworks; DB/MQ/VM/containers; LLM/RAG; structured AI
   workflows such as BMAD; cloud; frontend; collaboration; developer/non-developer docs.
4. Project records and verification surfaces.

Every claim descends through the same ladder:

`role keyword → direct answer → real case → engineering judgement → measured trace → public evidence → boundary`

Use progressive disclosure. The landing page stays short; the record carries the mass.

## Evidence rules

- Prefer the last year where it answers the role better than total career length.
- A large claim needs a reachable public surface next to it.
- Distinguish capability (self-owned repository) from reception (outside contribution,
  upstream merge, install count, real handoff).
- Counts follow the repository-wide numbers policy and the live stats endpoint.
- Private incidents may be described only at the level already allowed by root
  `AGENTS.md` and `apply/PRIVATE.md`.
- Interactive components consume public allowlisted data. They never fetch LOCAL FULL,
  raw journal titles, refs, locators, or time-block comments.

## Build contract

```bash
nix develop -c make all
nix develop -c make check
nix develop -c make repro
```

What reproducibility this build actually has is **measured, not asserted** — `make repro`
builds twice from clean and compares. The result, as of the font change:

- HTML and Markdown are **byte-identical** across two clean builds.
- The PDFs have **identical extracted text**. Their bytes differ: XeLaTeX's writer
  regenerates the trailer's file identifier on every run, and this toolchain has no flag to
  suppress it. `SOURCE_DATE_EPOCH` and `FORCE_SOURCE_DATE` are set, so the creation date is
  pinned and nothing else varies. **Layout is not compared** — do not say it is.

So a PDF hash is not citable here; the extracted text is. Do not restore a blanket "the
build is deterministic" claim without a witness that survives being reverted.

PDF export uses XeLaTeX so Korean stays searchable, copyable text rather than an image.
The Hangul faces come from the flake (`Pretendard`, `D2Coding`) with `FONTCONFIG_FILE`
pinned to the closure — Noto Sans CJK is a variable-weight TTC that xetexko cannot index,
and a shell that resolves fonts from the host silently substitutes them instead of failing.
HTML is generated from Org cuts and may mount local JS bundles later; the component chosen
follows the evidence, never the other way around.
