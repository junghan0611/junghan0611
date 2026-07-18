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

### `apply/ax/` is live — the `run.sh` loop

The AX evidence dossier is served at **https://ax.junghanacs.com**. It is not a file you
build and attach once; it is a public surface a reviewer's agent reads, so it stays live
and is updated in place. `run.sh` at the repo root is the entry point — a fresh session
(human or agent) drives the whole edit → live-update loop through it, without needing to
reconstruct the toolchain:

```bash
./run.sh publish     # build, pass the leak gate, copy the 8 public files to the web root → LIVE
./run.sh live        # read the live site from outside; compare its bytes to what was published
./run.sh axis        # regenerate timeline/projection.{md,org} from the LOCAL FULL (only when the axis moved)
./run.sh help        # every command
```

The usual loop is: edit `apply/ax/ax.org` → `./run.sh publish` → `./run.sh live`. If the
time axis moved (a fresh `events.jsonl` + `snapshot.json`), run `./run.sh axis` first,
because `ax.org` `#+include`s the reading.

Two invariants the script enforces and you must not route around:

- **The web root is `/home/junghan/docker-data/ax`, not `apply/ax/build/`.** `build/` also
  holds the `.tex`, LaTeX logs, and profile cuts; a server rooted there would leak them.
  Never drop a file into the web root outside `./run.sh publish` — `make publish` depends
  on `make check`, so the **leak gate is the only guard between the denylist and the URL**.
- **The document is the source of truth, not the server.** Analytics (Umami) and any other
  additive markup go into `ax.org` and ship through publish, never injected by the web
  server — if the live page and the authored source diverge, "the way the document was made
  is the claim" stops being true.

**Serving is not this repo's surface.** The Caddy vhost, TLS, directory-listing policy,
`.md` content-type, **Umami** analytics, and **Remark42** comments all live in
`nixos-config` and belong to its maintainer. When ax needs a serving change — a new
subdomain behaviour, analytics wiring, a comment thread — ask the nixos-config maintainer
through entwurf; do not reach into Caddy or the docker host from here.

## `timeline/` — the observatory

The time axis the identity documents cite is a normalized, KST-anchored event log of a
day at four depths — the time blocks the operator logs by hand, his own journal headings,
the agents' agenda stamps, and the commits and notes themselves. Its argument is one
sentence — **you can attach any number of agents, but you cannot manufacture time already
spent.** The observatory that builds it is now a **shared skill**
(`~/.claude/skills/timeline`, sourced from agent-config, usable from any session); this
repo is one consumer, and its `timeline/` holds only the committed `projection.{md,org}`
it cites.

The KST contract, the collector's known defects, and the run commands live in the skill:
`~/.claude/skills/timeline/SKILL.md` and its `README.md`. The current step lives in the
gitignored `NEXT.md`. What follows is only what a new session must not re-derive.

### Where the time axis comes from — know this before touching anything

**`timeline/` did not invent this axis.** The axis already exists as the operator's
org-agenda, it is read every day in Emacs, and it is already published at
`agenda.junghanacs.com`. The collector produces a normalized, machine-readable
*projection* of the same underlying time axis. An agent that does not know where the
axis lives will re-derive it wrongly.

| On disk | What it is | In the agenda view |
|---|---|---|
| git clones under `~/repos` | commits — the measure | — |
| `~/org/botlog/agenda/*.org` | agent stamps; device stamp files are named `…__agenda_<device>.org`, and the directory also contains non-device agenda files | `Agent(T)`, `Agent(O)`, … |
| `~/org/journal/*.org` | the operator's **own timestamped headings** | `Human` |
| `~/org/**/*.org` (Denote) | notes — output | — |

Three things follow, and each has already been gotten wrong once.

1. **Both agenda lanes are now collected.** Agent stamps and the Human journal
   headings both enter the axis, and a heading becomes an event on exactly the
   condition that puts it in org-agenda: an active timestamp attached to it. Before
   the journal adapter a day could look empty in the projection while the operator was
   recording illness or an intent — 2026-07-11 held two headings and zero events. Do
   not reintroduce that gap by reading only the artifact sources.
2. **An agenda stamp knows which machine stamped it**, from its filename. That is
   *not* the same as the manifest's `device`, which records the machine that ran the
   collection. A stamp made on one machine is routinely collected on another.
3. **Do not reimplement "show me today's axis."** Use the Emacs skill and open
   org-agenda for the date. `timeline/` exists to make the axis queryable in bulk and
   verifiable by reference, not to replace the view the operator already uses.

**Disclosure is already solved upstream — do not rebuild it here.** The journal is
exported to the public garden in full; anything the operator does not want published
is marked `:noexport:` in org. That mechanism already works. A second checkpoint
inside the collector is exactly the wall this work tore out once already.

`punchout` writes a daily summary heading into the journal, tagged `:PUNCHOUT:` —
commit count, per-repo breakdown, a prose timeline, and coarse health figures. **It
is a hand-made projection of this same axis**, and it is the closest thing to a
first rendering that already exists. Read it before designing one.

### The depth axis — 0, 1, 2, 3

The sources are not a flat list to be finished. They are **zoom levels on one day**, and
the operator named them:

| depth | what it shows | source | whose record |
|---|---|---|---|
| **0** | the life as lived — sleep, family, rest, reading, work blocks | aTimeLogger, via the `lifetract` skill | the operator's **intent** |
| **1** | when the operator marked something, and what he said | journal headings | the operator's **intent** |
| **2** | what the agents did, and when | agenda stamps | an **artifact's trace** |
| **3** | the detail: every commit, every note | git, Denote | an **artifact's trace** |

Read the right-hand column before adding anything. **Depths 0 and 1 are deliberate acts
of recording; depths 2 and 3 are residue.** Time-logging is not telemetry the operator
happens to leak — it is the Lyubishchev/Drucker discipline of knowing where the time
actually goes, performed on purpose, and it is prior to any output the other depths can
show. A harness that reads only the residue can describe what got produced and nothing
about the life that produced it.

This is the instrument of **Track 1 (PKM-AI harness research)**, not decoration for a
résumé. The question is whether a shared, reproducible record changes how a human and
agents work together over years; the depth axis is how that record is read.

**Depth 0 is collected, and the collector does not parse it.** The blocks sit in a sqlite
database the `lifetract` skill owns; the collector shells out to the skill and takes a
day's minutes per category. A test fails if anyone turns that subprocess into a direct
database read.

That is the general rule, and it is the direction of this whole file:

> **A source another skill already owns is consumed through that skill, never re-parsed
> here.** The collector is meant to *shrink* toward the skills. `gitcli`, `denotecli` and
> the agenda own parsers `collect.py` still duplicates; depth 0 is the first source where
> it stopped. When a skill is missing something the axis needs, the fix belongs in that
> skill — file it, do not work around it with a private parser.

**Expect every skill to have a hole here, and do not read it as a defect in the skill.**
The skills were built before this axis existed, so none of them was written against a time
contract — fixed KST, half-open ranges, an honest answer about staleness. The observatory
is the first thing that asks them for one, which is exactly why consuming a skill surfaces
a gap: `lifetract` computes its dates from `$TZ`, and under `TZ=UTC` it files the same
blocks on different days. That is not a bug report so much as a retrofit list, and it will
grow as the collector shrinks toward `gitcli`, `denotecli` and the agenda. Coordinate the
set from here: name the gap, fix it in the skill that owns it, and never route around it
with a private parser — that is how the checkpoint this work already tore out gets rebuilt.

Consuming the skill also settled three problems that were never ours: a block is an
interval and events are moments; sleep crosses midnight nearly every night, so some rule
must say which day owns it; and 150 blocks carry a comment naming who was there.
`lifetract` reports minutes already filed under the day the block **started**, and never
hands over the comments. The event is therefore a span with a day for a coordinate —
`ts: null`, `duration_min: 514.0` — because writing an instant for a nine-hour block
fabricates a coordinate exactly the way `00:00` on a day-only note does.

Two failure modes are guarded and must stay guarded:

- **`$TZ` is pinned for the child.** The skill reads it, and under `TZ=UTC` the same blocks
  land on different days — one day lost 220 minutes. A shell must not get to decide which
  day a night belonged to.
- **A missing skill is a hole, not a zero.** No `lifetract` means the source reports
  `unreadable`, loudly. It never falls back to the database. A depth-0 gap presented as
  zero minutes is a lie about a life.

Depth 0 also depends on data the collector cannot reach: aTimeLogger lives on a phone and
is exported by hand into `self-tracking-data`. **If the export is stale, depth 0 is stale,
and it must say so rather than presenting an old bottom as the present.** The app exports
two files. Take the **`database.db3`** — sqlite, table `time_interval2`, epoch seconds —
which is what `lifetract` already imports. The `.atl2bkp` is the same data as XML, nothing
reads it, and its interval `comment` fields carry family names in plain text; it does not
belong in a repository.

**The comments are the disclosure boundary of depth 0.** 150 blocks carry one, and a
comment says who was there and what it was. The FULL is gitignored and may hold them, but
no projection may put a block's comment on a public surface. A duration and a category can
go out; the comment cannot.

**Do not automate that export away.** The temptation is to treat the manual step as
friction and replace it with a background sync. That would delete the finding. The point
this axis exists to demonstrate is that a person deliberately manages his own attention on
a time axis — the hand-logging is not a defect in the pipeline, it *is* the thesis. An
axis that harvests a life automatically is measuring a different thing entirely.

**SNS is not a source.** By the operator's ROSSE principle the raw material lands in the
garden first; anything worth collecting is already there. Do not add a social adapter.

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

**But an empty day in the axis is still not evidence of an empty day.** The journal
adapter closed the largest version of this hole — the operator's own voice is now on
the axis — but the axis still sees only what was written down. A day with no commit,
no note, no stamp and no heading is a day nobody recorded, which is not the same as a
day nobody worked. Do not read that silence as rest, and do not present it as one.

### Measure, trace, output, voice — the sources are not peers

| Source | Role | Collected? |
|---|---|---|
| **git commit** | **The measure.** Locally visible, non-merge commits attributed to the configured author identities, across every ref the clone holds. | yes |
| agenda stamp | **A trace** the operator and the agents left. Sparse by design: the first stamp is 2026-02-27, and not every commit gets one. | yes |
| Denote note | **Output.** Catches work that leaves no commit — notably repairs to existing notes, which create no new file. | yes |
| journal heading | **The operator's own voice**, at a timestamp. Not an artifact trace — a message. Carries the constraints the other three cannot see: the body, the family, the commute, the intent. | yes |
| time block | **The life as lived**, on purpose. Sleep, family, rest, reading, work — logged by hand, in the Lyubishchev sense. Depth 0, read through `lifetract`. | yes |

The journal heading is the one source that is not a repository event, and it is given
**no `domain` and no `layer`** — `null`, not `unmapped`. `unmapped` means "a repo
nobody has classified yet"; a heading lands in no repo at all. Filing the operator's
own voice under a repo label would bend every slice by domain. The practice of
timestamping headings began in **2026** — earlier journals are prose, and their
absence from the axis is the record, not a defect to repair.

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
