# Changelog

This file records durable, closed milestones. The live direction remains in
[`ROADMAP.md`](ROADMAP.md); machine-local next actions remain outside the public
repository.

## Unreleased

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
