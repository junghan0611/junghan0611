# Roadmap

This roadmap names the durable direction of the public profile and its time-axis
observatory. It is not a task database. Machine-local next actions and private
operational decisions remain outside this repository.

## Current position

The source foundation is complete: the observatory can read the four depths of a
day through one fixed KST contract. The remaining distance is expression — making
a public projection that lets another reader inspect the record without changing
what the FULL contains.

## M1 — First public projection

1. Stabilize snapshot identity where volatile source locators can change bytes
   without changing an event's native identity.
2. Produce one projection anchored on **2026-02-07**, contrasted with
   **2026-07-11**, and accompanied by a compact 2026 coverage summary.
3. Carry the snapshot triple (`device`, `code_sha256`, `events_sha256`) with every
   cited aggregate.
4. Publish only aggregates and safe references. Never expose time-block comments
   or reshape FULL membership to make the projection cleaner.
5. Cross-check representative days against the existing journal `PUNCHOUT`
   rendering rather than designing an unrelated summary from a blank page.

Exit criteria:

- Both golden days remain visible.
- Collection is byte-identical under UTC, KST, and UTC+14 for the same inputs.
- Aggregate counts are checked against real source data and a hand-read daily
  rendering.
- The projection can be regenerated from documented commands.

## M2 — Connect the identity surfaces

- Add a concise, evidence-linked observatory claim to `resume/README.md`.
- Let `README.md` introduce the inquiry without turning into a metrics catalog.
- Let `llms.txt` tell external models how to navigate from claims to the public
  projection and its provenance.
- Keep `apply/` as a role-targeted cut whose large claims point back to the same
  public evidence.

Exit criteria:

- Every large new claim has an immediately reachable public evidence surface.
- The four governed identity documents remain vocabulary- and alias-consistent.
- No application target changes the collector's inclusion rules.

## M3 — Longitudinal readings

- Add reproducible day, week, month, and year views only after the first projection
  proves which summaries are useful.
- Compare machine-local FULLs only when their difference changes an interpretation;
  do not build a merger merely to make two machines report the same number.
- Derive activity or work-track views downstream. Keep repository `domain` and
  `layer` as stable context rather than teaching the collector to judge each
  commit's meaning.
- Preserve snapshot provenance so mutable note history and changing local refs are
  visible characteristics, not hidden noise.

## Later decisions

- Decide whether Track 2 appears only as a doorway from the public profile. It does
  not enter the measured model.
- Decide whether a multi-machine native-identity merge is justified by an observed
  interpretive need.
- Promote time contracts into other source-owning skills as the observatory exposes
  concrete gaps; never route around those skills with private parsers.

## Non-goals

- Global reconstruction of every historical commit or unrecorded minute.
- Automatic phone telemetry replacing deliberate hand-logged time.
- Publishing time-block comments or other private payloads.
- Scoring, radar charts, or collector-side semantic classification of work.
- Adding sources merely because data exists. A source enters only when a reading
  demonstrates a missing depth that changes the argument.
