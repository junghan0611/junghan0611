# timeline — the KST time axis, collected once and queried many times

Nothing here is new data. Three surfaces that already exist are read and normalized onto
one axis:

| source | what it reads | events it produces |
|---|---|---|
| `git` | every ref (`--all`) in the clones under `~/repos/gh`, `~/repos/work` | `authored` — one per commit |
| `note` | Denote `.org` files under `~/org` | `created`, `modified` — up to two per note |
| `agenda` | `~/org/botlog/agenda/*.org` | `stamped` — one per stamp |

```
collect.py  →  events.jsonl (LOCAL FULL)  →  query.py  →  a slice
```

The LOCAL FULL keeps titles and refs exactly as they read on this machine. **Deciding what
may be published is a separate, later step and is deliberately not in the collector.** A
collector that decides what to hide is a wall, and the point of this axis is to open one.
`events*.jsonl` is gitignored; it does not leave the machine by accident.

## Run

```bash
python3 timeline/collect.py --as-of 2026-07-14 --out events.jsonl   # audit → stdout
python3 timeline/query.py events.jsonl --day 2026-07-13
python3 timeline/query.py events.jsonl --month 2026-07 --source git --count events
python3 timeline/test_timeline.py
```

`--as-of` is an **exclusive** upper bound at KST midnight. `--as-of 2026-07-14` includes
all of July 13th. It defaults to tomorrow, so a bare run includes today — but pin it
explicitly whenever you want to reproduce a run.

`query.py` with no range returns the whole file. It never asks the operating system what
day it is, so the same FULL yields the same slice on any day, in any timezone. `--from`
alone means everything since; `--to` alone, everything before.

## What "every ref" does and does not mean

The git source walks `--all`: every ref the local clone holds, not just the branch that
happens to be checked out. Work abandoned on a branch still happened, and keeping only
what got merged would leave a time axis that records nothing but the successes.

It is bounded by what is on this disk. **Not** included: repos never cloned here, remote
branches never fetched, and objects already pruned as unreachable. A commit seen in more
than one clone is counted once — dedup is by sha.

## The agenda is not a second copy of git

Commits are the record that is complete. A commit exists because work was written down at
the moment it happened, and it exists whether or not anyone chose to mark it afterwards.

Agenda stamps are not that. **The first stamp in the whole corpus is 2026-02-27** — before
that date the practice did not exist — and even after it, a stamp is written when an agent
marks a session worth marking, not once per commit. So the two sources are asymmetric on
purpose: git is the measure, the agenda is a sparse commentary laid over it. A month with
no stamps is not a month with no work, and an unstamped repo is not an idle one.

This is why `domains.json` is drawn around the repos that hold **commits**, and why a repo
known only from a stamp is left out of it. A stamp's URL carries whatever name the repo had
*that day*; the commit it names is found by sha, in whichever clone actually holds it, and
inherits that repo's domain. Registering the old name as if it were a second repo would put
a ghost in the registry and, worse, make the audit cry about a missing clone forever.

## The registry, and the one thing it cannot carry

`domains.json` is the registry: the repos this axis reads commits from, each with a domain
and a layer. It can disagree with the disk in two directions, and the audit names both.

- `unregistered_clones` — a repo on disk that the table does not know. Its commits are in
  the FULL, but with no domain, so a repo cannot slip into the axis unclassified and
  unnoticed. This one is meant to sit at zero.
- `uncloned_repos` — a repo the table names that this disk does not hold. Its commits
  cannot be read at all, and an unread repo leaves a gap that looks exactly like a stretch
  of doing nothing.

(`unmapped_repos` is the wider list: every forge id that ended up with no domain, including
ones known only from a stamp's URL because the repo is not on this disk. It does not fall
to zero, which is why the drift alarm above is kept separate from it.)

A few repos cannot be *named* in a committed public file — a client's, a colleague's, an
internal host's. They are read from `domains.local.json`, which is gitignored, merged after
the public table, and declared in the manifest under `registries`.

Be exact about what that second file buys, because the temptation is to claim more. It does
not decide what may be published, it filters no event, it scrubs no name: every clone is
walked either way, and a repo missing from the registry still lands in the FULL under its
real name, marked `unmapped`. What the overlay preserves is those repos' **domain and
layer** — drop it and this year's unmapped commits go from 2% to 11%, so a slice by domain
stops describing the work it is meant to describe. The disclosure boundary is elsewhere,
and always has been: `events.jsonl` is gitignored.

## The time contract

- Canonical timezone is `Asia/Seoul`. Every instant on the wire is RFC3339 with `+09:00`.
- Ranges are half-open `[from, as_of)` in KST.
- Git times come from the **offset-aware author timestamp**, converted to KST. A naive git
  timestamp is rejected, never assumed. A commit written at 20:00 UTC belongs to the *next*
  day in Seoul, and hundreds of commits carry `+0000`.
- Denote identifiers and agenda stamps are KST-local by construction.
- `time_kind` ∈ `authored | created | modified | stamped | tracked`.
- `ts_precision` ∈ `second | minute | day`.
- **A day-only time has no instant.** It carries `ts: null` and lives on `date_kst`.
  Writing `00:00` would fabricate a coordinate that a naive consumer reads as fact.
- Entities and events are different things. One note is up to two events; one commit is an
  `authored` event *and* every agenda stamp written about it. So `--count events` and
  `--count entities` answer different questions and the caller must say which.
- Git entities keep the **full sha**. An agenda stamp carries a 7-char prefix; it joins the
  commit only when a local clone expands that prefix to exactly one full sha. Ambiguous →
  rejected. Not expandable → kept as `git:<repo>@short:<prefix>`, honestly unresolved.
- **A commit is found by its sha, not by its repo's name.** The stamp's URL is recorded
  as written, but the *entity* is whatever commit that sha actually names, in whichever
  clone holds it.
- The output is deterministic: same inputs and same `--as-of` produce the same bytes, on any
  machine, under any system timezone. There is no wall clock anywhere in the output.

```bash
# the check that matters
TZ=UTC       python3 timeline/collect.py --as-of 2026-07-14 --out /tmp/a.jsonl > /tmp/a.json
TZ=Asia/Seoul python3 timeline/collect.py --as-of 2026-07-14 --out /tmp/b.jsonl > /tmp/b.json
cmp /tmp/a.jsonl /tmp/b.jsonl && cmp /tmp/a.json /tmp/b.json
```

## Known source defects

Recorded in the audit as rejections, never guessed at. These are properties of the raw
material *today*; if the files are fixed, the numbers should change:

- **Duplicate Denote identifiers.** A handful of ids name two notes each. An identifier that
  points at two places is not a coordinate, so *both* sides are rejected and reported.
- **Unparseable `#+hugo_lastmod`.** A few dozen notes carry a lastmod no format matches.
  The note's `created` event still lands; only the `modified` event is dropped.
- **Unresolvable short shas.** An agenda stamp whose commit is on no clone here has no local
  object to expand its 7-char prefix against. It stays unresolved rather than being
  force-joined to a guess.

## Why the join is by sha and not by name

A repo name is not a stable identifier, and this axis spans years of them changing. Names
lie in three ways, and the third is the dangerous one:

- a repo is **renamed** (`garden` → `garden_v5`);
- it **moves to another owner** (`junghanacs/andenken` → `junghan0611/andenken`);
- its old name is **handed to a different repo** — `garden` is freed, then reused for what
  used to be `notes`. Now one string means two repos, and only the era tells them apart.

A table of old→new names survives the first, cannot express the second, and is actively
*wrong* about the third: it would quietly drag the new `garden` onto the old one's identity.
So there is no such table. A stamp's URL is kept exactly as written, and the commit it names
is found by asking the clones which one holds that sha. A commit does not change when its
repo is renamed, sold, or replaced.

## Deliberately not here

Publication decisions, URL liveness checks, sensitive-term handling, HTML or MCP surfaces,
and any source beyond the three above. They belong downstream of a FULL that is already
trustworthy — and they are exactly what turned an earlier attempt into a checkpoint bigger
than the thing it was checking.

Repos absent from `domains.json` collect as `domain: unmapped`. That is a gap in the table,
not a claim about the repo.
