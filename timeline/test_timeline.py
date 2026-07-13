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

import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from collect import (KST, AMBIGUOUS, Reject, _event, check, duplicate_ids,  # noqa: E402
                     forge_id_from_remote, in_range, make_event_id, normalize_git_ts,
                     parse_agenda_ts, parse_denote_id, parse_kst, parse_lastmod,
                     sort_key, time_component)

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
    # AMBIGUOUS is a sentinel, not a string: it can never be mistaken for a real sha.
    ok("the ambiguous marker cannot pass as a sha",
       not isinstance(AMBIGUOUS, str))


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


def test_remote_identity():
    ok("ssh remote -> forge id",
       forge_id_from_remote("git@github.com:junghan0611/notes.git")
       == "github.com/junghan0611/notes")
    ok("https remote -> forge id",
       forge_id_from_remote("https://github.com/junghan0611/notes")
       == "github.com/junghan0611/notes")
    ok("a confirmed rename lands on the current identity",
       forge_id_from_remote("git@github.com:junghan0611/pi-shell-acp.git")
       == "github.com/junghan0611/entwurf")
    ok("an unparseable remote yields no identity",
       forge_id_from_remote("/home/junghan/some/local/dir") is None)


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


def main() -> int:
    for t in (test_time, test_range, test_identity, test_ambiguity_is_rejected,
              test_agenda_occurrence, test_remote_identity, test_tz_determinism,
              test_query_never_reads_the_clock, test_sort_is_total):
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
