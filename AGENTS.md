# AGENTS.md

Governance for the identity-document set in this repository.

## Documents in scope

This repo holds three coordinated identity documents plus a glossary.

- `README.md` — manifesto. Long-form, narrative. The GitHub profile front door.
- `resume/README.md` — résumé. Compressed bullets, ATS-friendly.
- `llms.txt` — LLM-facing identity. Authored here; the notes garden pulls it on publish.
- `VOCABULARY.md` — canonical glossary. Single source of truth for load-bearing terms.

The garden repository (`notes.junghanacs.com`) re-publishes `llms.txt` from this repo.
There is no governance file in the garden repo because the garden is a publish target,
not an authoring location.

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
3. The author's name (`정한`) or signature/alias (`힣`, `힣 GLG`, `glg`) written
   alongside the English form.
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

- Counts in thousands round to the nearest 100. `3,300+`, `8,200+`.
- Day counts round to the nearest 100. `1,400+`.
- Recent windows ("last N days") are exact, with the measurement date stamped
  next to the number.
- The point is that the data exists and is publicly inspectable, not that the
  count is accurate to the unit.

Sources of truth:

- Note / journal / bibliography counts → geworfen live data (`agenda.junghanacs.com`).
- Commit counts → `gitcli` over `~/repos/`.
- Health and time-tracking counts → `lifetract`.

The résumé is allowed to keep specific verifiable metrics (e.g. `198 commits in
30 days`, `163 tests passing`) when they are scoped to a project window. The
manifesto and `llms.txt` keep rounded figures.

## Canonical direction

```
VOCABULARY.md  (terms)
      |
      v
README.md  (manifesto, uses terms in narrative)
      |
      +--> resume/README.md  (compresses manifesto + adds metrics)
      |
      +--> llms.txt          (LLM-facing glossary derived from VOCABULARY)
```

Workspace facts (commits, note counts, health records) feed all three documents
through the rounding rules above.

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
- Do not edit `notes/content/llms.txt` directly. Edit `llms.txt` here; the garden
  pulls it on publish.
