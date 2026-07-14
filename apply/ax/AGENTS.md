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

## One authored source, five views

`ax.org` is the only authored content source.

| profile tag | generated view |
|---|---|
| `landing` | short public front door (`build/index.html`) |
| `record` | deep web record (`build/record.html`) |
| `competency` | required competency/achievement PDF |
| `portfolio` | required portfolio PDF |
| `detail` | required detailed Markdown |

Generated `build/*.org`, HTML, TeX, PDF, and Markdown are derivatives. Never repair a
derivative by hand; fix `ax.org` or the build wiring.

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
