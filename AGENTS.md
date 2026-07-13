# AGENTS.md

Governance for the identity-document set in this repository.

## Documents in scope

This repo holds three coordinated identity documents plus a glossary.

- `README.md` — manifesto. Long-form, narrative. The GitHub profile front door.
- `resume/README.md` — résumé. Compressed bullets, ATS-friendly.
- `llms.txt` — LLM-facing identity. Mirrored *from* the garden. See below.
- `VOCABULARY.md` — canonical glossary. Single source of truth for load-bearing terms.

`apply/` and `timeline/` are separate surfaces and are **not** identity documents.
See below.

## `apply/` — job-application surface

`apply/README.md` (competency statement) and `apply/portfolio.md` (project detail)
are a **role-targeted cut** of the identity set, for AX-transformation and agent-platform
positions. They are public and reusable across employers.

Three rules govern this directory, and they invert the ones above.

1. **Korean, deliberately.** The Korean hiring market reads these. The English-only
   language policy below applies to the four identity documents *only* — it does not
   apply to `apply/`. Do not "fix" the Korean here; that is not drift, it is the point.
2. **`apply/PRIVATE.md` is never committed.** It holds referrer names, job postings,
   application routes, and closed company facts. It is gitignored. Keep it that way.
   Company-identifying material belongs there, not in the two public files.
3. **Claims must trace back.** Every large claim in `apply/` restates something the
   identity documents already establish, and carries the same public evidence link.
   When a figure changes, update the identity documents first, then mirror it here.
   The verifiability pairing rule and the numbers policy below both apply.

The résumé stays comprehensive; `apply/` is where the target-specific cut lives. Do
not let a job posting reshape `resume/README.md`.

### Where each document is authored

`README.md`, `resume/README.md`, and `VOCABULARY.md` are authored here. This repo
is their single source of truth.

`llms.txt` is **not**. It is served at `notes.junghanacs.com/llms.txt`, and the
garden exports daily, so corrections land there first. The real flow is:

```
garden (notes/content/llms.txt)  ──copy──▶  this repo (llms.txt)
        ^ authored, corrected daily              ^ mirror of record
```

Pull the garden copy first, then apply profile-side corrections (counts, skill
totals, repository list) and offer to push the same corrections back to the
garden. Do not edit this repo's `llms.txt` in isolation and assume the garden
will follow — it will not.

`VOCABULARY.md` remains authoritative for term *definitions* in both places. When
`llms.txt` and `VOCABULARY.md` disagree about what a term means, `VOCABULARY.md`
wins and `llms.txt` gets corrected.

## `timeline/` — the observatory

`timeline/` is the data layer the identity documents will eventually cite: a
normalized, KST-anchored event log of work that actually happened, collected from
git commits, Denote notes, and agent agenda stamps. Its argument is one sentence —
**you can attach any number of agents, but you cannot manufacture time already
spent.**

The KST contract, the collector's known defects, and the run commands live in
`timeline/README.md`. The current step lives in the gitignored `NEXT.md`. What
follows is only what a new session must not re-derive.

### The pillar rule — trunk, not completeness

**The axis does not claim global completeness or reconstruct every missing
historical minute and commit.** It holds the pillars and the main trunk. Within the
current clones, it still reads every locally visible non-merge author commit across
`--all`. Repositories were started and abandoned, commits were made and thrown away,
and whole tools stopped being used. What remains observable in the present source
surfaces is what the axis can record. It does not reconstruct discarded history
unless its absence changes a pillar.

**A gap is not automatically a defect.** Source unreadability and an unregistered
clone are defects; retired or rewritten history that does not move a pillar is an
accepted boundary. Do not spend a session recovering a handful of missing commits.
Name the boundary and move on.

### Measure, trace, output — the three sources are not peers

| Source | Role |
|---|---|
| **git commit** | **The measure.** Locally visible, non-merge commits attributed to the configured author identities, across every ref the clone holds. |
| agenda stamp | **A trace** the operator and the agents left. Sparse by design: the first stamp is 2026-02-27, and not every commit gets one. |
| Denote note | **Output.** Catches work that leaves no commit — notably repairs to existing notes, which create no new file. |

On a representative day, 45 commits carried 20 stamps. **That ratio is normal.**
Reading stamp sparsity as a hole in the axis inverts the hierarchy: a stamp is
evidence *about* a commit, never the measure of one. Likewise, a stamp naming a
commit this disk cannot resolve is not a defect — it means the repository was
retired or was never cloned here.

### `domain` is repo context, not activity

`domain` and `layer` answer **"what kind of repository did this event land in?"**
They do not answer **"what was actually being worked on at that moment."** A
repository hosts different kinds of work across its life; the label is a stable fact
about the repo, not a judgement about the commit.

Do not fix this by teaching the collector to classify each commit's meaning — that
rebuilds the disclosure checkpoint this work already tore out once. If a work-track
view is wanted, derive it downstream as a projection, never in the collector.

### Snapshots are machine-local

`--as-of` bounds time; it does not freeze local ref state. The collector walks
`--all`, so **unpushed local branches enter the axis** — deliberately, so the record
does not degrade into "only the work that succeeded."

It follows that **two machines legitimately produce different FULLs, and that is
correct.** Never force the numbers to agree: that would mean changing how the
operator actually commits in order to flatter a table. An axis that makes the person
conform to it is already lying.

Every quoted figure carries its snapshot — `device`, `code_sha256`, `events_sha256`.
A number without those three is not citable.

### Known holes — investigated, accepted, do not re-litigate

- **Retired tools whose commits are not on this disk.** `pi-skills` is archived;
  a few private repos are no longer cloned. Their stamps survive and name them;
  their commits do not enter the axis.
- **Rewritten histories.** Some clones exist but no longer contain the commit a
  stamp names — the repository was re-initialized or force-pushed.
- **`pi-shell-acp` is the former name of `entwurf`.** GitHub still redirects it.
  This rename is precisely why commit identity is keyed on the full SHA and never on
  a repository name.

The full list, including private repository names, lives in the gitignored
`NEXT.md`. **Do not copy those names into this file — this repository is public.**

## Language policy — STRICT

**All identity documents are written in English only.**

Files governed by this rule:

- `README.md`
- `resume/README.md`
- `llms.txt`
- `VOCABULARY.md`

Korean text must not appear in these files except in four explicit cases.

1. Hangul transliteration of a coined term, in parentheses, on first definition.
   Example: `Authology (어쏠로지)`, `Harnessing (하네싱)`.
2. Verbatim Korean strings inside fenced code blocks (e.g. agenda timeline
   samples, search-query examples).
3. The author's identity-equation alias set, written alongside the English form:
   `김정한`, `정한`, `힣`, `힣맨`, `힣 GLG`, `glg`, `GLG`, `GLGMAN`. This set is
   stated deliberately in `README.md`, `resume/README.md`, `llms.txt`, and
   `VOCABULARY.md` so that a public search resolving any one alias lands on the
   same author. Keep the set identical in all four; do not trim it to satisfy the
   drift check.
4. Verbatim Korean quotes from journals or agenda entries used as illustrative
   examples in prose, accompanied by an English gloss in parentheses.
   Example: `"밥먹고 올게" (going to eat)`.

### Why this rule exists

When the working conversation is in Korean, agents tend to translate edited
snippets back to Korean without realizing it. They see partial context, swap a
paragraph, and the document silently drifts bilingual. This rule must be
re-checked on every edit, not assumed.

### Drift check before staging

Run before staging any identity document:

```
grep -nP '[\x{AC00}-\x{D7AF}]' README.md resume/README.md llms.txt VOCABULARY.md
```

Every match must fit one of the four exceptions above. Anything else is a
regression — fix it before staging.

## Vocabulary

Load-bearing terms are defined once, in `VOCABULARY.md`. Identity documents use
those terms; they do not redefine them.

Do not introduce a new load-bearing term in `README.md`, `resume/README.md`, or
`llms.txt` without first adding it to `VOCABULARY.md`.

## Numbers policy

The standard is *approximate, public-verifiable* — not *exact, precise*.

- Counts in thousands round **down** to the nearest 100. `3,300+`, `8,200+`.
- Day counts round down to the nearest 100. `1,400+`.
- Recent windows ("last N days") are **not** frozen into identity documents. The
  live surface is the number. Do not reintroduce a static "commits in the last N
  days" row — see the duplicate-clone trap below for why such a figure is not
  trustworthy at authoring time.
- The point is that the data exists and is publicly inspectable, not that the
  count is accurate to the unit.

### Single source of truth: `agenda.junghanacs.com/api/stats`

Every figure in the Working Corpus and By the Numbers tables comes from one live
JSON endpoint:

```
curl -s https://agenda.junghanacs.com/api/stats
{"notes":…,"bibliography":…,"commits":…,"journal":…,"health":…,"garden":…}
```

`journal` and `health` are **day counts**, not record counts. Identity documents
must present them as days.

The route is `/api/stats`, not `/stats` — the homepage renders it client-side, so
a bare `/stats` returns 404 and a careless check will conclude, wrongly, that no
numbers surface exists.

geworfen serves this from the Oracle host's own checkouts. If those repositories
have not been pulled recently, the live figure lags the local workspace. That is
acceptable and intended: the published number is the one a reader can verify.

### The duplicate-clone trap

Do **not** derive commit counts by running `gitcli` over `~/repos/` and taking the
total. `~/repos/` holds multiple clones of the same repository — working copies,
and successor repositories that kept the original history under a new name. A
naive walk counts the same commit once per directory.

This is not hypothetical. `entwurf` and its former clones `pi-shell-acp-v1` /
`pi-shell-acp-v2` shared 851 identical commit hashes; summing the three yielded
roughly 2,300 phantom commits and inflated a 90-day figure from ~3,200 to 5,470.

If you must cross-check locally, deduplicate by commit hash across repositories
and exclude forks. Then trust `/api/stats` anyway.

The résumé is allowed to keep specific verifiable metrics (e.g. `198 commits in
30 days`, `163 tests passing`) when they are scoped to a project window. The
manifesto and `llms.txt` keep rounded figures.

## Document centers

Each document has one center. Material that does not serve it moves to a
repository list entry or leaves.

- `README.md` — the author as an **independent inquirer**, and the corpus that
  inquiry runs on. Not a project catalog. A project earns a prose section only if
  the current inquiry passes through it.
- `resume/README.md` — the claim that one person works **from firmware up to the
  agent loop**. This is not "full stack" in the conventional front-end/back-end
  sense, and the document must not read that way.
- `llms.txt` — what an external model needs in order to navigate the garden
  without flattening it.
- `VOCABULARY.md` — what each load-bearing word means, once.

### Verifiability pairing (résumé)

A hiring reader will test whether the agent claims are real. Every large claim
sits next to a public repository that can be opened immediately.

| Claim | Public evidence |
|---|---|
| Works at the embedded layer | `homeagent-config` |
| Builds agent loops | `entwurf` |
| Works on a reproducible foundation | `nixos-config`, `doomemacs-config` |
| Others build on his work | `entwurf#40` — outside contributor, enterprise ACP backend |
| Others accept his code | `dakra/ghostel#343`, `#510` — merged upstream |

Company repositories cannot be opened. Place unverifiable company claims adjacent
to verifiable public ones, never alone.

Self-owned repositories prove capability but not reception; a reader can always
suspect a closed loop where the author is the only judge. Keep at least one claim
whose evidence is a **third party's action** — a merged pull request, an outside
contribution, an install count. Those rows are the hardest to fake and the first
a skeptical reader checks. When they go stale, replace them; do not quietly drop
the category.

Adoption figures (stars, downloads, PR line counts) are volatile. Stamp them with
a measurement date rather than rounding them, and re-measure before any release
of the document set.

## Canonical direction

```
VOCABULARY.md  (terms — authoritative for meaning)
      |
      +--> README.md         (manifesto, uses terms in narrative)
      |          |
      |          +--> resume/README.md  (compresses manifesto + adds metrics)
      |
      +--> llms.txt          (LLM-facing glossary)
                 ^
                 |
           garden/content/llms.txt  (authored there, mirrored here)
```

Terms flow down from `VOCABULARY.md`. The `llms.txt` *file* flows in from the
garden. These are different axes — a term can be authoritative here while the
file that uses it is edited elsewhere.

Workspace facts (commits, note counts, journal days, health days) feed all documents through
the rounding rules above.

## Update workflow

1. New term or concept → `VOCABULARY.md` first.
2. New project or section → `README.md` first, then mirror to `resume/README.md`
   and `llms.txt` as needed.
3. Number change → measure from workspace, apply rounding policy, update all
   three.
4. Stage every affected identity document together. Do not commit one in
   isolation when cross-document consistency is being touched.
5. Run the drift check from the Language policy section before staging.

## What not to do

- Do not coin new load-bearing terms in `README.md`, `resume/README.md`, or
  `llms.txt`. Add them to `VOCABULARY.md` first.
- Do not let Korean prose leak into identity documents. Re-read after each edit.
- Do not pile workspace metrics into the manifesto. Keep metrics in the résumé
  and the live geworfen data.
- Do not commit a single identity document when the change affects shared
  vocabulary or shared facts.
- Do not treat this repo's `llms.txt` as the authoring copy. Pull from the garden
  first, correct, then sync back. See "Where each document is authored".
- Do not commit `NEXT.md`. This is a public profile repo; the handoff file names
  private work repositories, customer SDK coordinates, and unreleased product
  facts. It is gitignored — keep it that way.
- Do not treat an agenda stamp as the measure of work, or its absence as a hole.
  The commit is the measure; the stamp is a trace. See `timeline/`.
- Do not chase missing commits, and do not force two machines' snapshots to agree.
  The axis holds the trunk, not every minute.
