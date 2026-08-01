# Changelog

This file records durable, closed milestones. The live direction remains in
[`ROADMAP.md`](ROADMAP.md); machine-local next actions remain outside the public
repository.

## Unreleased

## v2026.8.1 — The public evidence record, live at four depths

The AX evidence record went from a first commit to a live public surface at
`ax.junghanacs.com`, and this tag closes that build-out. The observatory the previous
tag founded moved out to a shared skill, leaving this repository as one of its
consumers.

### One document, four depths

- Built the evidence record as a reproducible build from one authored Org source, and
  published it live behind a leak gate.
- Dissolved an employer's three upload slots — competency statement, portfolio,
  detailed Markdown — into slices of one document at increasing depth: the claim, the
  shape of the evidence, the events and numbers, and the ledger. No derivative is
  authored, so none can fall behind another.
- Cut the depths with `org-export-exclude-tags` rather than select-tags: selecting a
  heading drags its whole subtree along, and the wide read would have arrived carrying
  the ledger.
- Made the build refuse a non-monotonic depth tree, and made the gate count each cut's
  survivors against a manifest. Tag inheritance deletes a section with no error
  anywhere, and a section that was cut reads exactly like one that was never written.
- Added the depth dial to the web record, stamped at build time by walking the manifest
  and the shipped headings in the same document order, with the counts asserted rather
  than assumed.
- Filled the ledger tier with reproduction commands, paths, third-party evidence, and
  the honest failures per axis. What earns a place there is what a third party can
  check; closed company facts were left out rather than abstracted, because a blurred
  count is still unverifiable.
- Rebuilt the record to open with the stance the work comes from, the rules it holds
  itself to, and its own vocabulary, then land the five axes on the five public skills
  and the role entry points a hiring surface reads.
- Established the stance discipline: a sentence arrives carrying the place it was
  actually kept, or it does not go in. That single rule is the whole difference between
  the section and a manifesto.
- Promoted the time axis from the events tier to the evidence tier — it is the evidence
  for the stance's last constant, and a claim whose evidence was cut out of the same
  view is not a claim.
- Defined terms by what they do rather than by etymology, and added the record's
  vocabulary table against the canonical glossary. `PKM-AI` had been load-bearing on
  every identity surface, including the résumé headline, with no glossary entry at all.

### The live surface

- Added `run.sh` as the entry point a fresh session drives the whole edit → publish →
  live loop through, and documented the two invariants it guards.
- Separated the web root from the build directory, which also holds the TeX, the LaTeX
  logs, and private cuts that a server rooted there would hand out.
- Made publish set the web root **equal** to a declared set rather than merely copying
  into it, retiring the difference by name. A file nobody publishes any more is still
  served to anyone holding its URL — stale, unbuilt, and never rescanned.
- Kept the renamed PDFs' original URLs as aliases, proved byte-identical on every
  publish. They are honoured, never advertised.
- Added the shared head include after pandoc rather than through it — inlining would
  have broken the analytics id and the offline build — carrying the schema.org identity
  graph that mirrors the garden's canonical node, the analytics tag, and a
  self-contained favicon.
- Shipped `llms.txt`, `robots.txt`, and `sitemap.xml` as authored static files under the
  same leak scan, and claimed the site in Search Console through the injected head so
  the token is gated and verified like every other shipped byte.
- Made the live verifier discover the record's images from the shipped HTML instead of a
  hand-kept list, so a figure the document asks for but publish never shipped fails there
  instead of becoming a broken image on someone's phone.
- Measured reproducibility instead of asserting it: HTML and Markdown are byte-identical
  across two clean builds, the PDFs have identical extracted text, and layout is not
  compared. Made `repro` fingerprint its inputs so a source edited mid-run reports a
  moving input rather than a regression.
- Put both PDFs on A4 by transplanting the private build's proven geometry wiring, and
  made the gate measure the paper from the file rather than trust the source.

### What a gate cannot check

- Wrote the image evidence contract: the text gate skips binaries by construction, so a
  forbidden term drawn into a picture passes every check here. Clearance is a person
  opening the final file that would ship, and `images/README.md` is the tracked ledger of
  who cleared what.
- Made the leak gate name every file it could not read. A silent skip reads exactly like
  a pass.
- Cleared four diagrams and recorded the conditions clearance imposed on their captions;
  rejected three others and did not copy them into the repository.
- Removed 3.2MB of embedded base64 from the record rather than teaching the gate to skip
  it — an unscanned region carved into a public artifact is worse than a larger file.

### Layout

- Established the CSS-first document layout, then found it had been declaring the
  document column on every top-level block instead of on the container that holds them.
  Three rules took the column away: tables and the evidence mount shipped pinned to the
  viewport's left edge, and every paragraph floated to the middle. The column now lives
  on `body` alone, 216 top-level blocks sit on one left rail, and gates assert the
  column's home so no child rule can take it back.
- Constrained figures on mobile, where a 1600px bitmap took the page's horizontal scroll
  with it.

### Governance

- Routed agents to nested governance. The root file described `apply/ax/` and its publish
  loop without once naming the `AGENTS.md` that governs it, so a whole session edited that
  directory's stylesheet and prose without opening it. A rule in an unread file is not
  governance.
- Ruled that a job posting does not write a sentence in the record. Three `경계` lines
  disclaimed frameworks the document never claims; the nested rule that produced them
  contradicted the root rule against target-specific cuts, and now tests every boundary
  against whether the document makes a claim it has to bound.
- Stated that role names are entry points in the common language of hiring, never titles
  held, and kept them out of the schema.org field that would assert one.

### The observatory and the identity documents

- Extracted the observatory — collector, query, viewer, projection, tests, registries —
  into a shared skill any session can use, leaving this repository as one consumer that
  commits only the projection it cites.
- Published the axis as an allowlisted reading that never holds a title, ref, or locator,
  and made the build know that a regenerated projection must reach the PDFs.
- Matched Git authors by name or email so a historical display-name change stopped
  erasing 740 operator commits, and restored the private domain registry whose loss in
  the extraction had left 46 repositories unmapped instead of 8.
- Made each reading name the machine it was read on, so two legitimately different
  snapshots can be told apart instead of looking like a contradiction.
- Pulled the garden's correction on the WikiDocs mirror, which had gone stale in a way
  that inverted a claim while two surfaces served opposite facts.

## v2026.7.14 — Timeline observatory foundation

This is the repository's first tagged snapshot. It closes the foundation of the
KST time-axis observatory and bookmarks the identity and application surfaces on
which that observatory will be cited.

### Observatory

- Built `timeline/collect.py` and `timeline/query.py` to normalize Git commits,
  Denote notes, agent agenda stamps, journal headings, and deliberate time blocks
  onto one fixed `Asia/Seoul` axis.
- Established the four-depth reading model: life as lived, the operator's own
  timestamped voice, agent traces, and artifact detail.
- Kept events distinct from entities so one commit can be authored once and
  annotated by multiple agenda stamps without being counted twice.
- Joined commits by full SHA rather than repository name, preserving identity
  across renames, owner moves, mirrors, and reused names.
- Added machine-local snapshot provenance through `device`, `code_sha256`, and
  `events_sha256`; local branches remain part of the record by design.
- Added repository context through public and machine-local domain registries
  without filtering unclassified events from the FULL.
- Read depth 0 through the `lifetract` skill rather than duplicating its database
  parser, preserving its interval and start-day ownership contracts while keeping
  interval comments out of projections.
- Closed the 2026 depth-0 coverage through July 13 at 194 of 194 days and recorded
  the two golden days, 2026-02-07 and 2026-07-11, where artifact traces are silent
  and the lower depths carry the day.
- Published the timeline contract as a repository-local skill shared by Claude
  Code and pi.

### Correctness and failure visibility

- Fixed all time windows to half-open KST ranges and pinned the time-log child to
  KST so the caller's shell timezone cannot move a night to another day.
- Represented time blocks as spans with `duration_min` and no fabricated instant.
- Added explicit `empty`, `stale`, and `unreadable` source states so absence can no
  longer be reported as healthy data.
- Made a lagging depth-0 source stale only when another source testifies that the
  missing day was lived, avoiding both silent holes and daily false alarms.
- Added guards for ambiguous short SHAs, duplicate Denote identifiers, unstable
  agenda occurrence numbering, source ownership, query clock dependence, total
  ordering, registry drift, and timezone determinism.
- Verified the contracts by reverting guards to ensure tests fail and by checking
  live data rather than relying only on mocks.

### Interpretation and boundaries

- Established Git commits as the measure, agenda stamps as sparse annotations,
  Denote notes as output, journal headings as the operator's voice, and deliberate
  time blocks as the life beneath the artifacts.
- Documented that repository `domain` and `layer` describe context, not the meaning
  of an individual activity; activity interpretation belongs in downstream
  projections.
- Kept the FULL machine-local and payload-bearing `events.jsonl` ignored. A
  snapshot bounds time but does not pretend to freeze the refs present on every
  machine.
- Recorded accepted boundaries around retired repositories, rewritten histories,
  mutable note modification times, and sparse stamps rather than reconstructing a
  false claim of global completeness.
- Retired the earlier disclosure lattice, resolver, redaction scanner, and sealed
  export design after it grew into a checkpoint larger than the queryable product.
- Preserved hand-exported time logging as part of the research claim rather than
  replacing deliberate attention tracking with automatic telemetry.

### Identity and application surfaces

- Refreshed the coordinated public identity set around two research tracks,
  reproducible agent infrastructure, verifiable public evidence, and third-party
  adoption.
- Added the role-targeted `apply/` surface while keeping employer-specific facts in
  its ignored private companion.
- Recentered the application material on agent-platform operations without letting
  a job description alter the immutable FULL.
- Unified public garden links under `junghan0611/garden` and strengthened the
  repository governance for vocabulary, evidence, numbers, and language drift.

### Prior untagged history

- The tag also bookmarks the earlier profile evolution from the initial GitHub
  profile through the English identity set, résumé, vocabulary governance,
  reproducible environment, memory architecture, and public project evidence.
