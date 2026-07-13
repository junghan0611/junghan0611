#!/usr/bin/env python3
"""timeline/test_timeline.py — the properties that must hold, on synthetic data.

    python3 timeline/test_timeline.py

Deliberately NOT pinned to the live corpus. Today's real audit says 4 duplicate Denote
identifiers and 17 unparseable lastmods; if the operator fixes those files tomorrow the
numbers SHOULD change, and a test that fails for that reason is a test that punishes
housekeeping. So the fixtures assert the invariant instead: ambiguity is rejected, never
guessed.
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from collect import (KST, Reject, Repos, _event, check, device_name,  # noqa: E402
                     duplicate_ids, forge_id_from_remote, in_range, load_registry,
                     make_event_id, normalize_git_ts, parse_agenda_ts, parse_denote_id,
                     parse_kst, parse_lastmod, sha256, sort_key, time_component)

FAILED: list[str] = []


def ok(name: str, cond: bool, detail: str = ""):
    print(("  ok  " if cond else "  FAIL") + f"  {name}" + (f"  — {detail}" if detail else ""))
    if not cond:
        FAILED.append(name)


def raises(fn, reason: str) -> bool:
    try:
        fn()
    except Reject as r:
        return r.reason == reason
    return False


def test_time():
    day = parse_lastmod("[2026-07-12]")
    ok("day-only lastmod invents no instant",
       day["ts"] is None and day["ts_precision"] == "day"
       and day["date_kst"] == "2026-07-12")

    minute = parse_lastmod("[2026-07-12 Sun 14:30]")
    ok("minute lastmod is a KST instant",
       minute["ts"] == "2026-07-12T14:30:00+09:00" and minute["ts_precision"] == "minute")

    sec = parse_lastmod("Time-stamp: <2026-07-12 14:30:05>")
    ok("Time-stamp form parses to the second",
       sec["ts"] == "2026-07-12T14:30:05+09:00" and sec["ts_precision"] == "second")

    ok("garbage lastmod is rejected, not coerced",
       raises(lambda: parse_lastmod("last tuesday"), "unparseable_lastmod"))

    ok("naive git timestamp is rejected",
       raises(lambda: normalize_git_ts("2026-07-12T14:30:00"), "naive_git_timestamp"))

    # The whole reason the timezone is a contract and not a detail.
    late = normalize_git_ts("2026-07-12T20:00:00+00:00")
    ok("a +0000 commit late in the UTC day belongs to the NEXT day in Seoul",
       late["date_kst"] == "2026-07-13" and late["ts"] == "2026-07-13T05:00:00+09:00",
       "20:00Z -> 05:00 KST +1d")

    ok("denote id is a KST second", parse_denote_id("20260712T143005")["ts"]
       == "2026-07-12T14:30:05+09:00")
    ok("bad denote id is rejected",
       raises(lambda: parse_denote_id("2026-07-12"), "bad_denote_identifier"))
    ok("agenda stamp is a KST minute",
       parse_agenda_ts("2026-07-12", "14:30")["ts"] == "2026-07-12T14:30:00+09:00")
    ok("a non-KST offset is not silently accepted",
       raises(lambda: parse_kst("2026-07-12T14:30:00+00:00"), "not_kst_offset"))


def test_range():
    frm = parse_kst("2026-07-01T00:00:00+09:00")
    to = parse_kst("2026-07-13T00:00:00+09:00")
    inst = lambda d, t: {"ts": f"{d}T{t}+09:00", "date_kst": d, "ts_precision": "second"}
    dayev = lambda d: {"ts": None, "date_kst": d, "ts_precision": "day"}

    ok("[from, to) includes the lower bound", in_range(inst("2026-07-01", "00:00:00"),
                                                       frm, to))
    ok("[from, to) excludes the upper bound", not in_range(inst("2026-07-13", "00:00:00"),
                                                           frm, to))
    ok("the last instant before the bound is in",
       in_range(inst("2026-07-12", "23:59:59"), frm, to))
    ok("a day event whose whole day is inside is in", in_range(dayev("2026-07-12"),
                                                               frm, to))
    ok("a day event on the excluded final day is out — not guessed into the window",
       not in_range(dayev("2026-07-13"), frm, to))


def test_identity():
    tp = parse_denote_id("20260712T143005")
    sha = "45ac17609fc750d81c527fc9350d79057659d004"
    e1 = make_event_id("git", f"git:github.com/o/r@{sha}", "authored", tp, sha)
    e2 = make_event_id("git", f"git:github.com/o/r@{sha}", "authored", tp, sha)
    ok("event_id is deterministic", e1 == e2)
    ok("time_kind is part of identity",
       e1 != make_event_id("git", f"git:github.com/o/r@{sha}", "stamped", tp, sha))
    ok("a day event keys on the date, never on a fabricated midnight",
       time_component({"ts": None, "date_kst": "2026-07-12", "ts_precision": "day"})
       == "date:2026-07-12")

    ev = _event(source="git", entity_id=f"git:github.com/o/r@{sha}", time_kind="authored",
                tp=parse_agenda_ts("2026-07-12", "14:30"), domain="agent", layer="product",
                title="t", ref=None, native_id=sha, locator="/tmp/r")
    ok("the full sha survives into the entity — never truncated to 7",
       ev["entity_id"].endswith(sha) and len(sha) == 40)
    ok("a well-formed event passes the contract", check(ev) == [])

    bad = dict(ev, ts_precision="day")          # a day event still carrying an instant
    ok("an invented instant on a day event is caught",
       "day event carries an invented instant" in check(bad))
    bad2 = dict(ev, ts="2026-07-12T14:30:00+00:00")
    ok("a non-KST instant is caught", "ts is not a KST instant" in check(bad2))


def test_ambiguity_is_rejected():
    names = ["20260712T143005--a.org", "20260712T143005--b.org", "20260101T000000--c.org"]
    dupes = duplicate_ids(names)
    ok("a Denote id naming two notes is flagged — both sides, not a coin toss",
       dupes == {"20260712T143005"})
    ok("an id naming exactly one note is untouched", "20260101T000000" not in dupes)


def test_agenda_occurrence():
    """Two stamps, same file, same title, same minute. They are two events."""
    tp = parse_agenda_ts("2026-07-12", "14:30")
    from collect import _h
    n1 = _h("a.org", "stamp", time_component(tp), "1")
    n2 = _h("a.org", "stamp", time_component(tp), "2")
    ok("occurrence separates two identical stamps", n1 != n2)
    ok("the same occurrence is stable across runs",
       n1 == _h("a.org", "stamp", time_component(tp), "1"))
    e1 = make_event_id("agenda", f"agenda:{n1}", "stamped", tp, n1)
    e2 = make_event_id("agenda", f"agenda:{n2}", "stamped", tp, n2)
    ok("so their event ids differ", e1 != e2)


def test_stamp_identity_ignores_the_query_window():
    """A stamp's id must not depend on which range someone happened to ask for. Counting
    occurrence only among the stamps that survived the filter made the SECOND of two
    identical stamps become the first — and silently change its id."""
    import tempfile

    import collect

    body = ("**** did a thing\n<2026-07-12 Sun 14:30>\n"
            "**** did a thing\n<2026-07-12 Sun 14:30>\n"
            "**** later thing\n<2026-07-13 Mon 09:00>\n")
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "a.org").write_text(body)
        keep = collect.AGENDA_DIR
        try:
            collect.AGENDA_DIR = Path(tmp)
            src = collect.Source("agenda")
            ids = [s["native"] for s in collect.read_stamps(src)]
        finally:
            collect.AGENDA_DIR = keep
    ok("two identical stamps get two identities", ids[0] != ids[1] and len(ids) == 3)
    ok("occurrence is counted before any window, so a narrow query cannot renumber it",
       len(set(ids)) == 3)


JOURNAL_FIXTURE = """\
* 2026-07-11 Saturday
:PROPERTIES:
:CUSTOM_ID: h-2026-07-11
:END:
** 16:42 장염 복통
<2026-07-11 Sat 16:42>
** 18:26 인간 환멸
<2026-07-11 Sat 18:26>
some prose about the day
* 2026-07-12 Sunday
** DONE 13:45 식사 후
CLOSED: [2026-07-13 Mon 06:35]
<2026-07-12 Sun 13:45>
** a heading that only talks about a date
I wrote about <2026-07-12 Sun 09:00> but nothing happened at 09:00.
** quoting the agenda
#+begin_quote
<2026-07-12 Sun 10:00>
#+end_quote
** 20:00 same minute
<2026-07-12 Sun 20:00>
** 20:00 same minute
<2026-07-12 Sun 20:00>
"""


def journal_events(body: str = JOURNAL_FIXTURE):
    import tempfile

    import collect
    with tempfile.TemporaryDirectory() as tmp:
        # The locator must read as a path from ~/org, so the fixture mirrors the real
        # layout instead of the collector being loosened to accept a stray directory.
        jdir = Path(tmp) / "journal"
        jdir.mkdir()
        (jdir / "20260706T000000--2026-07-06__journal_week27.org").write_text(body)
        (jdir / "templates.org").write_text("** 09:00 template\n<2026-07-12 Sun 09:00>\n")
        keep_org, keep_j = collect.ORG, collect.JOURNAL_DIR
        try:
            collect.ORG, collect.JOURNAL_DIR = Path(tmp), jdir
            src = collect.Source("journal")
            frm, as_of = parse_kst("2026-01-01T00:00:00+09:00"), parse_kst(
                "2027-01-01T00:00:00+09:00")
            return collect.collect_journal(Repos.__new__(Repos), frm, as_of, src), src
        finally:
            collect.ORG, collect.JOURNAL_DIR = keep_org, keep_j


def test_journal_reads_the_lane_the_agenda_shows():
    """A heading is an event exactly when an ACTIVE timestamp is attached to it — the same
    condition that puts it in the operator's org-agenda.

    Two ways to get this wrong, and both are in the fixture. Scanning the body for any
    `<...>` collects the dates the operator merely wrote ABOUT, and reading inside a
    `#+begin_quote` collects the agenda he was quoting. Neither happened at that minute."""
    events, _ = journal_events()
    titles = [e["title"] for e in events]
    ok("the Saturday the axis called empty has two events",
       [e["title"] for e in events if e["date_kst"] == "2026-07-11"]
       == ["16:42 장염 복통", "18:26 인간 환멸"])
    ok("a date merely written about is not an event",
       not any("only talks about" in t for t in titles))
    ok("a timestamp inside a quote block is not an event",
       not any("quoting" in t for t in titles))
    ok("a planning line does not hide the timestamp behind it",
       "DONE 13:45 식사 후" in titles, "the 53 DONE headings")
    ok("templates are not records", not any("template" in t for t in titles))
    ok("every journal event passes the contract", not [e for e in events if check(e)])


def test_journal_identity_holds_still_while_the_heading_moves():
    """A workflow state and a tag are built to change; what happened at 16:42 is not.

    If identity keyed on them, marking a TODO done — or refiling it — would silently
    retire one event and mint another in its place, which is exactly the drift the line
    number was kept out of the id to avoid."""
    import collect
    plain = collect.stable_title("16:42 장염 복통")
    ok("a TODO state is not part of what happened",
       collect.stable_title("TODO 16:42 장염 복통") == plain)
    ok("neither is finishing it",
       collect.stable_title("DONE 16:42 장염 복통") == plain)
    ok("neither is a refile or an archive",
       collect.stable_title("DONE [#A] 16:42 장염 복통  :REFILED:ARCHIVE:") == plain)
    events, _ = journal_events()
    same_minute = [e for e in events if e["title"] == "20:00 same minute"]
    ok("two headings at the same minute are two events",
       len(same_minute) == 2
       and same_minute[0]["entity_id"] != same_minute[1]["entity_id"])


def test_journal_has_no_domain():
    """`domain` answers "what kind of repository did this land in". A heading lands in no
    repository, and `unmapped` does not mean "no repo" — it means "a repo nobody has
    classified yet". Filing the operator's own voice under it would put it in the same
    bucket as real repos and bend every slice by domain."""
    events, _ = journal_events()
    ok("no journal event claims a domain",
       all(e["domain"] is None and e["layer"] is None for e in events))
    ok("so a domain slice cannot swallow the human lane",
       not [e for e in events if e["domain"] == "unmapped"])


def test_remote_identity():
    ok("ssh remote -> forge id",
       forge_id_from_remote("git@github.com:junghan0611/notes.git")
       == "github.com/junghan0611/notes")
    ok("https remote -> forge id",
       forge_id_from_remote("https://github.com/junghan0611/notes")
       == "github.com/junghan0611/notes")
    ok("an unparseable remote yields no identity",
       forge_id_from_remote("/home/junghan/some/local/dir") is None)


def test_a_commit_is_found_by_sha_not_by_name():
    """The join must survive the three ways a name lies: the repo is renamed, it moves to
    another owner, and — the silent one — its old name is handed to a DIFFERENT repo. A
    stamp written years ago still names the commit correctly, because a sha is content."""
    import subprocess
    import tempfile
    from collect import Repos, commit_ref, resolve_shas

    with tempfile.TemporaryDirectory() as tmp:
        run = lambda *a: subprocess.run(["git", "-C", tmp, *a], capture_output=True,
                                        text=True, check=True)
        run("init", "-q", "-b", "main")
        run("config", "user.email", "t@t")
        run("config", "user.name", "junghan")
        run("commit", "-q", "--allow-empty", "-m", "the commit that outlives its name")
        full = run("rev-parse", "HEAD").stdout.strip()

        repos = Repos.__new__(Repos)          # the clone now answers to its NEW name
        repos.clones = [("github.com/junghan0611/garden_v5", Path(tmp))]
        repos.dirs = {"github.com/junghan0611/garden_v5": Path(tmp)}

        found, ambiguous = resolve_shas(repos, [full[:7]])
        ok("a stamp written under the OLD name still finds the commit",
           found.get(full[:7]) == (full, "github.com/junghan0611/garden_v5"),
           "old name in the URL, current repo in the entity")
        ok("nothing is ambiguous here", not ambiguous)

        missing, _ = resolve_shas(repos, ["deadbee"])
        ok("a commit that is not on this disk stays unresolved, never invented",
           "deadbee" not in missing)

    ok("a commit URL yields (named repo, short sha)",
       commit_ref("x [[https://github.com/junghanacs/andenken/commit/68b10f2][68b10f2]]")
       == ("github.com/junghanacs/andenken", "68b10f2"))
    ok("a release stamp is not a commit stamp",
       commit_ref("v1 https://github.com/junghan0611/entwurf/releases/tag/v1") is None)


def test_clones_that_disagree_about_a_prefix():
    """Two clones can expand the same 7-char prefix to two different commits. Taking the
    first one would be the same silent corruption as the name-based join, in a new hat."""
    from collect import merge_hits

    a, b = "github.com/o/a", "github.com/o/b"
    x = "45ac17609fc750d81c527fc9350d79057659d004"
    y = "45ac176ffffffffffffffffffffffffffffffff0"

    ok("one commit, mirrored in two clones, is still one commit",
       merge_hits([(a, x), (b, x)], False) == ("resolved", (x, a)),
       "first clone in sorted order names it — the same choice the git source makes")
    ok("two clones expanding one prefix to two commits is ambiguous, not a race",
       merge_hits([(a, x), (b, y)], False) == ("ambiguous", None))
    ok("a prefix nobody holds stays unresolved",
       merge_hits([], False) == ("unresolved", None))
    ok("git calling a prefix ambiguous inside one clone is still ambiguous",
       merge_hits([(a, x)], True) == ("ambiguous", None))


def test_tz_determinism():
    """The system clock's timezone must not touch a single byte."""
    def snapshot():
        return [
            parse_lastmod("[2026-07-12]"),
            parse_lastmod("[2026-07-12 Sun 14:30]"),
            parse_denote_id("20260712T143005"),
            normalize_git_ts("2026-07-12T20:00:00+00:00"),
            parse_agenda_ts("2026-07-12", "14:30"),
        ]

    before = os.environ.get("TZ")
    try:
        os.environ["TZ"] = "Asia/Seoul"
        time.tzset()
        seoul = snapshot()
        os.environ["TZ"] = "UTC"
        time.tzset()
        utc = snapshot()
        os.environ["TZ"] = "Pacific/Kiritimati"       # +14, the far edge
        time.tzset()
        far = snapshot()
    finally:
        if before is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = before
        time.tzset()
    ok("parsing is identical under Asia/Seoul, UTC and +14", seoul == utc == far)
    ok("KST is a fixed +09:00, with no DST to drift under",
       KST.utcoffset(datetime.now()) == timedelta(hours=9))


def test_query_never_reads_the_clock():
    """A query over a fixed FULL must return the same slice on any day, in any timezone.
    An earlier draft defaulted the upper bound to `date.today() + 1`, which quietly made
    the answer depend on when you asked."""
    import query

    class Args:
        day = month = frm = to = None

    inst = {"ts": "2030-01-01T00:00:00+09:00", "date_kst": "2030-01-01",
            "ts_precision": "second"}
    dayev = {"ts": None, "date_kst": "1999-12-31", "ts_precision": "day"}

    def unbounded_keeps_everything():
        frm, to = query.window(Args())
        return (frm, to) == (None, None) and all(
            query.within(e, frm, to) for e in (inst, dayev))

    before = os.environ.get("TZ")
    try:
        results = []
        for tz in ("Asia/Seoul", "UTC", "Pacific/Kiritimati"):
            os.environ["TZ"] = tz
            time.tzset()
            results.append(unbounded_keeps_everything())
    finally:
        if before is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = before
        time.tzset()
    ok("no range = the whole file, in any timezone — future and past events alike",
       all(results))

    src = Path(__file__).with_name("query.py").read_text()
    ok("query.py never calls date.today()", "date.today()" not in src)

    half = Args()
    half.frm = "2026-07-01"
    frm, to = query.window(half)
    ok("--from alone is open-ended upward",
       to is None and query.within(inst, frm, to)
       and not query.within(dayev, frm, to))


def test_sort_is_total():
    tp = parse_agenda_ts("2026-07-12", "14:30")
    day = {"date_kst": "2026-07-12", "ts": None, "ts_precision": "day", "event_id": "z"}
    inst = {"date_kst": "2026-07-12", "ts": tp["ts"], "ts_precision": "minute",
            "event_id": "a"}
    ok("a day sorts before the instants inside it",
       sorted([inst, day], key=sort_key)[0] is day)


def test_a_snapshot_can_name_itself():
    """Two machines, same code, same --as-of, different FULLs — one holds a clone the other
    lacks, one has a branch that was never pushed. Both are honest. The manifest therefore
    has to carry enough to tell them apart, or one will quietly stand in for the other."""
    a = [{"event_id": "1", "x": 1}, {"event_id": "2", "x": 2}]
    b = [{"event_id": "1", "x": 1}, {"event_id": "2", "x": 3}]     # one event differs
    body = lambda evs: "".join(json.dumps(e, sort_keys=True) + "\n" for e in evs)

    ok("the same events fingerprint the same",
       sha256(body(a).encode()) == sha256(body(a).encode()))
    ok("one differing event changes the fingerprint — a FULL cannot be swapped unnoticed",
       sha256(body(a).encode()) != sha256(body(b).encode()))
    ok("the machine names itself, and it is never blank",
       isinstance(device_name(), str) and device_name().strip() != "")


def test_the_registry_can_be_read_from_two_files():
    """The public table cannot name every repo. The FULL still has to see them, so the
    registry is read from a committed file and a gitignored one — and the run must say
    which, or a thinner FULL could pass for the same FULL."""
    import json as _json
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        pub, loc = Path(td) / "domains.json", Path(td) / "domains.local.json"
        pub.write_text(_json.dumps({"repos": {
            "github.com/me/open": {"domain": "garden", "layer": "product"},
            "github.com/me/both": {"domain": "unmapped", "layer": "unmapped"}}}))
        loc.write_text(_json.dumps({"repos": {
            "github.com/me/both": {"domain": "infra", "layer": "forge"},
            "github.com/client/secret": {"domain": "embedded", "layer": "product"}}}))

        only_public, used = load_registry([pub])
        ok("without the overlay the public table stands alone",
           set(only_public) == {"github.com/me/open", "github.com/me/both"})
        ok("and the manifest names the one registry it read", used == ["domains.json"])

        merged, used = load_registry([pub, loc])
        ok("a repo the public table cannot name still reaches the FULL",
           merged["github.com/client/secret"]["domain"] == "embedded")
        ok("the overlay wins where the two disagree",
           merged["github.com/me/both"]["domain"] == "infra")
        ok("the public entries survive untouched",
           merged["github.com/me/open"]["domain"] == "garden")
        ok("a FULL collected with the overlay cannot be mistaken for one without",
           used == ["domains.json", "domains.local.json"])

        loc.unlink()
        _, used = load_registry([pub, loc])
        ok("a missing overlay is simply absent, never an error",
           used == ["domains.json"])


def test_the_registry_reports_both_of_its_gaps():
    """domains.json is the list of repos this axis means to observe. It can disagree with
    the disk in two directions, and each means something different."""
    r = Repos.__new__(Repos)
    r.unmapped = set()
    r.dirs = {"github.com/a/here": "/repos/here", "github.com/a/stranger": "/repos/x"}
    r.domains = {"github.com/a/here": {"domain": "infra", "layer": "forge"},
                 "github.com/a/elsewhere": {"domain": "agent", "layer": "product"}}

    ok("a registered repo with no clone here is named — the work happened, this disk "
       "just cannot read it", r.uncloned() == ["github.com/a/elsewhere"])
    ok("a repo that is both registered and cloned is not a gap",
       "github.com/a/here" not in r.uncloned())
    ok("a cloned repo missing from the registry collects as unmapped, not as a guess",
       r.domain_layer("github.com/a/stranger") == ("unmapped", "unmapped"))
    ok("...and it is named, so a new repo cannot enter the axis unclassified and unseen",
       r.unregistered_clones() == ["github.com/a/stranger"])

    # A stamp can name a repo this disk does not hold. That forge id gets no domain either,
    # but it is not drift and it will not go away — so it must not sit in the alarm that is
    # supposed to read zero.
    r.domain_layer("github.com/a/only-ever-stamped")
    ok("a repo known only from a stamp does not raise the drift alarm",
       r.unregistered_clones() == ["github.com/a/stranger"])
    ok("...though it is still reported as having no domain",
       "github.com/a/only-ever-stamped" in r.unmapped)


def main() -> int:
    for t in (test_time, test_range, test_identity, test_ambiguity_is_rejected,
              test_agenda_occurrence, test_stamp_identity_ignores_the_query_window,
              test_journal_reads_the_lane_the_agenda_shows,
              test_journal_identity_holds_still_while_the_heading_moves,
              test_journal_has_no_domain,
              test_remote_identity, test_a_commit_is_found_by_sha_not_by_name,
              test_clones_that_disagree_about_a_prefix, test_tz_determinism,
              test_query_never_reads_the_clock, test_sort_is_total,
              test_a_snapshot_can_name_itself,
              test_the_registry_can_be_read_from_two_files,
              test_the_registry_reports_both_of_its_gaps):
        print(f"\n{t.__name__}")
        t()
    print()
    if FAILED:
        print(f"FAILED {len(FAILED)}: {', '.join(FAILED)}")
        return 1
    print("all green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
