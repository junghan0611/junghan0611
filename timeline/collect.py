#!/usr/bin/env python3
"""timeline/collect.py — read the existing surfaces, emit the LOCAL FULL event log.

    python3 timeline/collect.py --out events.jsonl

Three sources, no network, nothing invented: git repos under ~/repos, Denote notes
under ~/org, and the agent agenda under ~/org/botlog/agenda.

This is the LOCAL FULL. Titles and refs are kept exactly as they read on this machine.
What may be published is a separate and *later* question that deliberately does not live
here: a collector that decides what to hide is a wall, and the point of this axis is to
open one.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

SCHEMA_VERSION = "1"
COLLECTOR_VERSION = "0.2.0"

HOME = Path.home()
ORG = HOME / "org"
AGENDA_DIR = ORG / "botlog/agenda"
ROOTS = [HOME / "repos/gh", HOME / "repos/work"]
DOMAINS_FILE = Path(__file__).parent / "domains.json"

KST = timezone(timedelta(hours=9), "KST")
AUTHORS = ("junghan", "jhkim2")

log = lambda *a: print(*a, file=sys.stderr)  # noqa: E731


def _sh(cmd: list[str]) -> str:
    return subprocess.run(cmd, capture_output=True, text=True).stdout


# ---------------------------------------------------------------------------- time


class Reject(Exception):
    """A record that cannot be honestly normalized. Recorded, never coerced."""

    def __init__(self, reason: str, value: object = None):
        super().__init__(reason)
        self.reason, self.value = reason, value


def _tp(ts: str | None, date_kst: str, precision: str) -> dict:
    """A time point is a tagged union, not a datetime with a quality flag. An event known
    only to its day has NO instant — writing 00:00 would fabricate a coordinate that a
    naive consumer reads as fact."""
    return {"ts": ts, "date_kst": date_kst, "ts_precision": precision}


_LASTMOD_FORMS = [
    (re.compile(r"^\[(\d{4})-(\d{2})-(\d{2}) \w{3} (\d{2}):(\d{2})\]$"), "minute"),
    (re.compile(r"^<(\d{4})-(\d{2})-(\d{2}) \w{3} (\d{2}):(\d{2})>$"), "minute"),
    (re.compile(r"^Time-stamp:\s*<(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})"),
     "second"),
    (re.compile(r"^\[(\d{4})-(\d{2})-(\d{2})(?: \w{3})?\]$"), "day"),
]


def parse_lastmod(raw: str) -> dict:
    """`#+hugo_lastmod` -> time point. Roughly half of them carry no time of day."""
    v = raw.strip()
    for pat, precision in _LASTMOD_FORMS:
        m = pat.match(v)
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        d = date(g[0], g[1], g[2]).isoformat()
        if precision == "day":
            return _tp(None, d, "day")
        return _tp(datetime(*g, tzinfo=KST).isoformat(), d, precision)
    raise Reject("unparseable_lastmod", raw)


def parse_denote_id(ident: str) -> dict:
    """The creation coordinate the Denote identifier records — not a certified fact
    about when the thought began. Files move; identifiers get reused."""
    m = re.fullmatch(r"(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})", ident)
    if not m:
        raise Reject("bad_denote_identifier", ident)
    dt = datetime(*[int(x) for x in m.groups()], tzinfo=KST)
    return _tp(dt.isoformat(), dt.date().isoformat(), "second")


def parse_agenda_ts(day: str, hhmm: str) -> dict:
    y, mo, d = (int(x) for x in day.split("-"))
    h, mi = (int(x) for x in hhmm.split(":"))
    dt = datetime(y, mo, d, h, mi, tzinfo=KST)
    return _tp(dt.isoformat(), dt.date().isoformat(), "minute")


def normalize_git_ts(iso: str) -> dict:
    """The author timestamp exactly as the commit records it — a coordinate carried by
    the evidence, not a certification (an author date can be set). Offset-aware:
    convert, never assume. Hundreds of commits carry +0000, and a +0000 commit at 23:30
    belongs to the NEXT day in Seoul."""
    dt = datetime.fromisoformat(iso)
    if dt.tzinfo is None:
        raise Reject("naive_git_timestamp", iso)
    dt = dt.astimezone(KST)
    return _tp(dt.isoformat(), dt.date().isoformat(), "second")


def parse_kst(ts: str) -> datetime:
    """Parse and *check* the offset. A regex suffix test is not a parse."""
    dt = datetime.fromisoformat(ts)
    if dt.tzinfo is None or dt.utcoffset() != timedelta(hours=9):
        raise Reject("not_kst_offset", ts)
    return dt


def in_range(tp: dict, frm: datetime, as_of: datetime) -> bool:
    """Half-open [from, as_of) in KST. A day event has no instant, so it belongs to the
    window only when its whole day lies inside — the partial final day is excluded
    rather than guessed at."""
    if tp["ts_precision"] == "day":
        return frm.date() <= date.fromisoformat(tp["date_kst"]) < as_of.date()
    return frm <= parse_kst(tp["ts"]) < as_of


def sort_key(ev: dict) -> tuple:
    """Total order, so two runs cannot disagree. A day event sorts before the instants
    of the same day: it is the day, not a moment in it."""
    return (ev["date_kst"], 0 if ev["ts_precision"] == "day" else 1,
            ev["ts"] or "", ev["event_id"])


# ------------------------------------------------------------------------ identity


def time_component(tp: dict) -> str:
    return f"date:{tp['date_kst']}" if tp["ts_precision"] == "day" else tp["ts"]


def make_event_id(source: str, entity_id: str, time_kind: str, tp: dict,
                  native_id: str = "") -> str:
    key = (f"v{SCHEMA_VERSION}\x1f{source}\x1f{entity_id}\x1f{time_kind}"
           f"\x1f{time_component(tp)}\x1f{native_id}")
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def _h(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:16]


_SSH_REMOTE = re.compile(r"^(?:ssh://)?git@([^:/]+)[:/](.+)$")
_URL_REMOTE = re.compile(r"^[a-z+]+://(?:[^@/]+@)?([^/]+)/(.+)$")


def forge_id_from_remote(url: str) -> str | None:
    """`git@github.com:owner/repo.git` -> `github.com/owner/repo`. A folder name is not
    a repo name — `notes/` on disk is `notes.junghanacs.com` on the forge — so identity
    comes from the remote and never from the path."""
    url = url.strip().removesuffix(".git")
    m = _SSH_REMOTE.match(url) or _URL_REMOTE.match(url)
    if not m:
        return None
    host = re.sub(r"^github-[a-z]+\.com$", "github.com", m.group(1))
    parts = [p for p in m.group(2).split("/") if p]
    if len(parts) < 2:
        return None
    return f"{host}/{parts[-2]}/{parts[-1]}"


class Repos:
    """Where the clones are, and which domain each repo belongs to.

    `clones` keeps every checkout, because two clones of one repo can sit on different
    branches and hold different commits. `dirs` keeps one per repo — that is all a short
    sha needs to be expanded."""

    def __init__(self):
        self.clones: list[tuple[str, Path]] = []
        self.dirs: dict[str, Path] = {}
        self.unmapped: set[str] = set()
        self.domains: dict = (json.loads(DOMAINS_FILE.read_text())["repos"]
                              if DOMAINS_FILE.exists() else {})
        for root in ROOTS:
            if not root.is_dir():
                continue
            for d in sorted(root.iterdir()):
                if not (d / ".git").exists():
                    continue
                fid = forge_id_from_remote(
                    _sh(["git", "-C", str(d), "remote", "get-url", "origin"]))
                if fid:
                    self.clones.append((fid, d))
                    self.dirs.setdefault(fid, d)

    def domain_layer(self, fid: str) -> tuple[str, str]:
        d = self.domains.get(fid)
        if not d:
            self.unmapped.add(fid)
            return "unmapped", "unmapped"
        return d.get("domain", "unmapped"), d.get("layer", "unmapped")


class Source:
    """Every source reports what it could and could not do. Silently skipping an
    unreadable source is forbidden — a partial FULL circulating as a FULL is the worst
    thing this collector could hand anyone."""

    def __init__(self, name: str):
        self.name = name
        self.status = "ok"
        self.errors: list[str] = []
        self.rejected: list[dict] = []
        self.accepted = 0

    def reject(self, reason: str, where: str):
        self.rejected.append({"reason": reason, "where": where})

    def unreadable(self, msg: str):
        self.status = "unreadable"
        self.errors.append(msg)

    def done(self, n: int):
        self.accepted = n
        if self.status != "unreadable":
            self.status = "partial" if self.rejected else "ok"

    def report(self) -> dict:
        return {"name": self.name, "status": self.status, "accepted": self.accepted,
                "rejected": len(self.rejected), "errors": self.errors[:20]}


def _event(source: str, entity_id: str, time_kind: str, tp: dict, domain: str, layer: str,
           title: str, ref: dict | None, native_id: str, locator: str,
           tags: list[str] | None = None, extra: dict | None = None) -> dict:
    prov = {"adapter": source, "collector_version": COLLECTOR_VERSION,
            "native_id": native_id, "locator": locator, **(extra or {})}
    return {
        "schema_version": SCHEMA_VERSION,
        "event_id": make_event_id(source, entity_id, time_kind, tp, native_id),
        "entity_id": entity_id,
        "time_kind": time_kind,
        "ts": tp["ts"], "date_kst": tp["date_kst"], "ts_precision": tp["ts_precision"],
        "source": source, "domain": domain, "layer": layer,
        "title": title, "tags": tags or [],
        "ref": ref, "provenance": prov,
    }


# ----------------------------------------------------------------------------- git


def collect_git(repos: Repos, frm: datetime, as_of: datetime, src: Source) -> list[dict]:
    """One commit, one authored event. The entity keeps the FULL sha: truncating it to
    the 7 chars an agenda stamp happens to carry would join the two by baking a
    collision risk into identity itself.

    `--all`, not HEAD. Work that was abandoned on a branch still happened, and keeping
    only what got merged would leave a time axis that records nothing but the successes."""
    events, seen = [], set()
    for fid, d in sorted(repos.clones):
        out = _sh(["git", "-C", str(d), "log", "--all", "--no-merges",
                   "--pretty=format:%H\x1f%aI\x1f%an\x1f%s"])
        domain, layer = repos.domain_layer(fid)
        for line in out.splitlines():
            parts = line.split("\x1f")
            if len(parts) != 4:
                src.reject("malformed_log_line", fid)
                continue
            sha, ts, author, subject = parts
            if not any(a in author.lower() for a in AUTHORS):
                continue
            if sha in seen:                 # duplicate clones share history
                continue
            seen.add(sha)
            try:
                tp = normalize_git_ts(ts)
            except Reject as r:
                src.reject(r.reason, fid)
                continue
            if not in_range(tp, frm, as_of):
                continue
            events.append(_event(
                source="git", entity_id=f"git:{fid}@{sha}", time_kind="authored", tp=tp,
                domain=domain, layer=layer, title=subject,
                ref={"kind": "git", "value": f"{fid}@{sha}"},
                native_id=sha, locator=str(d)))
    return events


# --------------------------------------------------------------------------- notes

DENOTE_RE = re.compile(r"^(\d{8}T\d{6})--(.+?)(?:__(.+))?\.org$")
TITLE_RE = re.compile(r"^#\+title:\s*(.*)$", re.M)
LASTMOD_RE = re.compile(r"^#\+hugo_lastmod:\s*(.*)$", re.M)


def duplicate_ids(names: list[str]) -> set[str]:
    """A Denote identifier is supposed to name exactly one note. A few name two. A
    coordinate pointing at two places is not a coordinate, so BOTH sides are rejected
    and reported — guessing which note the id "really" means is a fabrication, and it is
    exactly how the wrong note would later ship under the right one's label."""
    seen: dict[str, int] = {}
    for n in names:
        m = DENOTE_RE.match(n)
        if m:
            seen[m.group(1)] = seen.get(m.group(1), 0) + 1
    return {i for i, c in seen.items() if c > 1}


def collect_notes(repos: Repos, frm: datetime, as_of: datetime,
                  src: Source) -> list[dict]:
    """Two events per note, answering different questions. `created` is when the room was
    built; `modified` is when it was re-worked — and re-work happens *in place*, so a
    note polished ten times still shows one creation. Counting only creations is how the
    revision axis disappears."""
    if not ORG.is_dir():
        src.unreadable(f"{ORG} not found")
        return []
    files = sorted(ORG.rglob("*.org"))
    dupes = duplicate_ids([f.name for f in files])
    events = []
    for f in files:
        m = DENOTE_RE.match(f.name)
        if not m:
            continue
        ident, slug, tagstr = m.groups()
        rel = f.relative_to(ORG)
        if rel.parts[0] == "botlog" and "agenda" in rel.parts:
            continue                        # the agenda is its own source
        if ident in dupes:
            src.reject("duplicate_denote_identifier", ident)
            continue
        try:
            created = parse_denote_id(ident)
        except Reject as r:
            src.reject(r.reason, f.name)
            continue
        text = f.read_text(errors="replace")
        tm = TITLE_RE.search(text)
        common = dict(
            source="note", entity_id=f"denote:{ident}", domain="garden", layer="product",
            title=(tm.group(1).strip() if tm else slug.replace("-", " ")),
            tags=(tagstr.split("_") if tagstr else []),
            ref={"kind": "denote", "value": ident}, native_id=ident, locator=str(rel))
        if in_range(created, frm, as_of):
            events.append(_event(time_kind="created", tp=created, **common))
        lm = LASTMOD_RE.search(text)
        if lm and lm.group(1).strip():
            try:
                mod = parse_lastmod(lm.group(1))
            except Reject as r:
                src.reject(r.reason, f.name)
                continue
            if in_range(mod, frm, as_of):
                events.append(_event(time_kind="modified", tp=mod, **common))
    return events


# -------------------------------------------------------------------------- agenda

AGENDA_HEAD = re.compile(r"^\*{4} (.+?)(?:\s+:([a-z0-9:_]+):)?\s*$")
AGENDA_TS = re.compile(r"^<(\d{4}-\d{2}-\d{2}) \w{3} (\d{2}:\d{2})>")
# Not only commits: stamps also carry release, PR and issue links. An earlier regex
# matched `/commit/` alone, so release stamps fell through the commit branch entirely.
GITHUB_REF = re.compile(
    r"https://github\.com/([^]/\s]+)/([^]/\s]+)/(commit|releases/tag|compare|pull|issues)"
    r"/([^]\s\[]+)")
SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")


def read_stamps(src: Source) -> list[dict]:
    """Every stamp in the agenda, in sorted source order, before any window is applied.

    The window comes later on purpose. Occurrence is counted here, over ALL stamps, so a
    stamp's identity cannot change depending on which range someone asked for."""
    stamps: list[dict] = []
    occurrence: dict = {}
    for f in sorted(AGENDA_DIR.glob("*.org")):
        head = None
        for lineno, line in enumerate(f.read_text(errors="replace").splitlines(), 1):
            hm = AGENDA_HEAD.match(line)
            if hm:
                head = (hm.group(1),
                        [t for t in (hm.group(2) or "").split(":") if t], lineno)
                continue
            if not head:
                continue
            tm = AGENDA_TS.match(line)
            if not tm:
                continue
            title, tags, at = head
            head = None
            try:
                tp = parse_agenda_ts(*tm.groups())
            except (ValueError, Reject):
                src.reject("unparseable_agenda_timestamp", f"{f.name}:{at}")
                continue
            # Two stamps can share a file, a title AND a minute (23 pairs do). So a
            # stamp's own identity is (file, title, time, occurrence) — never the commit
            # it names, and never the line it sits on. Keying on the commit sha collapsed
            # two real stamps into one.
            key = (f.name, title, time_component(tp))
            occurrence[key] = occurrence.get(key, 0) + 1
            stamps.append({"file": f.name, "line": at, "title": title, "tags": tags,
                           "tp": tp,
                           "native": _h(f.name, title, time_component(tp),
                                        str(occurrence[key]))})
    return stamps


def commit_ref(title: str) -> tuple[str, str] | None:
    """(forge id as the stamp wrote it, short sha) for a stamp that names a commit."""
    m = GITHUB_REF.search(title)
    if not m or m.group(3) != "commit" or not SHA_RE.match(m.group(4)):
        return None
    return f"github.com/{m.group(1)}/{m.group(2)}", m.group(4)


def merge_hits(hits: list[tuple[str, str]], ambiguous_in_a_clone: bool) -> tuple[str, tuple | None]:
    """Decide one short prefix from what every clone said about it.

    `hits` is (forge id, full sha) for each clone that resolved the prefix, in sorted
    clone order. The same commit sitting in several clones is not ambiguity — it is one
    commit, and the first clone in sorted order names it, which is exactly the choice the
    git source makes when it dedups by sha. But a prefix that expands to DIFFERENT full
    shas in different clones is genuinely ambiguous, and taking the first one would be
    the same silent corruption we just removed from the name-based join, wearing a
    different hat."""
    if ambiguous_in_a_clone:
        return "ambiguous", None
    fulls = {full for _, full in hits}
    if not fulls:
        return "unresolved", None
    if len(fulls) > 1:
        return "ambiguous", None
    full = fulls.pop()
    return "resolved", (full, next(fid for fid, f in hits if f == full))


def resolve_shas(repos: Repos, shorts: list[str]) -> tuple[dict, set]:
    """short prefix -> (full sha, the forge id of the clone that holds it).

    Identity by CONTENT, not by name. A commit is unchanged when its repo is renamed,
    when it moves to another owner, and — the dangerous one — when its old name is later
    handed to a DIFFERENT repo. A name-based join breaks on all three, and it breaks
    silently, which is the worst way to break. The sha does not care.

    EVERY clone is asked about EVERY prefix. Stopping at the first hit would be faster and
    would quietly pick a winner whenever two clones disagree about what a 7-char prefix
    means. Offline, and it refuses to guess: disagreement is rejected, absence stays
    unresolved."""
    if not shorts:
        return {}, set()
    hits: dict[str, list[tuple[str, str]]] = {s: [] for s in shorts}
    clone_ambiguous: set[str] = set()
    payload = "\n".join(shorts) + "\n"
    for fid, d in sorted(repos.clones):
        r = subprocess.run(["git", "-C", str(d), "cat-file", "--batch-check"],
                           input=payload, capture_output=True, text=True)
        # One output line per input line, in order: "<full sha> commit <size>", or
        # "<input> missing", or "<input> ambiguous".
        for short, line in zip(shorts, r.stdout.splitlines()):
            parts = line.split()
            if len(parts) == 3 and parts[1] == "commit":
                hits[short].append((fid, parts[0]))
            elif len(parts) >= 2 and parts[1] == "ambiguous":
                clone_ambiguous.add(short)

    found: dict[str, tuple[str, str]] = {}
    ambiguous: set[str] = set()
    for short in shorts:
        status, value = merge_hits(hits[short], short in clone_ambiguous)
        if status == "resolved":
            found[short] = value
        elif status == "ambiguous":
            ambiguous.add(short)
    return found, ambiguous


def collect_agenda(repos: Repos, frm: datetime, as_of: datetime,
                   src: Source) -> list[dict]:
    """A stamp naming a commit is a second event ABOUT that commit, not a copy of it — so
    it joins the commit's entity when the sha resolves, and keeps an identity of its own
    when it does not."""
    if not AGENDA_DIR.is_dir():
        src.unreadable(f"{AGENDA_DIR} not found")
        return []
    src.unresolved_short = 0
    stamps = [s for s in read_stamps(src) if in_range(s["tp"], frm, as_of)]
    found, ambiguous = resolve_shas(
        repos, sorted({cr[1] for s in stamps if (cr := commit_ref(s["title"]))}))

    events: list[dict] = []
    for s in stamps:
        tp, native = s["tp"], s["native"]
        entity, ref = f"agenda:{native}", None
        domain, layer = "agent", "product"
        m = GITHUB_REF.search(s["title"])
        if m:
            # The ref is kept exactly as the stamp wrote it, old repo name and all. The
            # LOCAL FULL records what the source said; only the ENTITY is normalized to
            # the commit the sha actually names.
            ref = {"kind": "url", "value": m.group(0)}
            named = fid = f"github.com/{m.group(1)}/{m.group(2)}"
            cr = commit_ref(s["title"])
            if cr:
                short = cr[1]
                if short in ambiguous:
                    src.reject("ambiguous_short_sha", short)
                    continue
                if short in found:
                    full, home = found[short]
                    entity, fid = f"git:{home}@{full}", home   # joins the commit itself
                else:
                    entity = f"git:{named}@short:{short}"      # honestly unresolved
                    src.unresolved_short += 1
            # Ask the domain table only about the repo we actually landed on. Asking it
            # about the name in the URL too would count long-dead names — a repo's maiden
            # name, an owner it left years ago — as repos missing from the table.
            domain, layer = repos.domain_layer(fid)
        events.append(_event(
            source="agenda", entity_id=entity, time_kind="stamped", tp=tp,
            domain=domain, layer=layer, title=s["title"], tags=s["tags"], ref=ref,
            native_id=native, locator=f"{s['file']}:{s['line']}"))
    return events


# ------------------------------------------------------------------------ contract

TIME_KINDS = {"authored", "created", "modified", "stamped", "tracked"}
PRECISIONS = {"second", "minute", "day"}


def check(ev: dict) -> list[str]:
    """The whole contract, in one function. If an event needs more than this to be
    trusted, the shape is wrong — not the checker."""
    errs = []
    if ev["time_kind"] not in TIME_KINDS:
        errs.append("time_kind")
    if ev["ts_precision"] not in PRECISIONS:
        errs.append("ts_precision")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", ev["date_kst"] or ""):
        errs.append("date_kst")
    if ev["ts_precision"] == "day":
        if ev["ts"] is not None:
            errs.append("day event carries an invented instant")
    else:
        try:
            if parse_kst(ev["ts"]).date().isoformat() != ev["date_kst"]:
                errs.append("date_kst disagrees with ts")
        except (Reject, TypeError, ValueError):
            errs.append("ts is not a KST instant")
    if not ev["event_id"] or not ev["entity_id"]:
        errs.append("identity")
    return errs


def tally(items) -> dict:
    out: dict = {}
    for i in items:
        out[i] = out.get(i, 0) + 1
    return dict(sorted(out.items()))


# ---------------------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description="collect the LOCAL FULL event log")
    ap.add_argument("--from", dest="frm", default="2015-01-01", metavar="YYYY-MM-DD")
    ap.add_argument("--as-of", metavar="YYYY-MM-DD",
                    help="EXCLUSIVE upper bound at KST midnight. Default is tomorrow, "
                         "so today is fully included; pass it explicitly to reproduce a "
                         "run byte for byte.")
    ap.add_argument("--out", default="", metavar="FILE",
                    help="events JSONL; manifest and audit go to stdout either way")
    args = ap.parse_args()

    as_of_day = args.as_of or (datetime.now(KST).date() + timedelta(days=1)).isoformat()
    frm = parse_kst(f"{args.frm}T00:00:00+09:00")
    as_of = parse_kst(f"{as_of_day}T00:00:00+09:00")

    repos = Repos()
    sources = {n: Source(n) for n in ("git", "note", "agenda")}
    events: list[dict] = []
    for name, fn in (("git", collect_git), ("note", collect_notes),
                     ("agenda", collect_agenda)):
        src = sources[name]
        evs = fn(repos, frm, as_of, src)
        src.done(len(evs))
        events += evs
        log(f"[{name}] {src.status} accepted={src.accepted} rejected={len(src.rejected)}")

    broken = [{"event_id": e["event_id"], "errors": errs}
              for e in events if (errs := check(e))]
    if broken:
        log(f"FATAL: {len(broken)} events fail the shape. First 3:")
        for b in broken[:3]:
            log("   ", json.dumps(b, ensure_ascii=False))
        return 1

    events.sort(key=sort_key)
    entities = {e["entity_id"] for e in events}
    rejected = [r for n in ("git", "note", "agenda") for r in sources[n].rejected]

    # No wall clock anywhere in the output: the same inputs and the same --as-of must
    # produce the same bytes, on any machine, under any TZ.
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "collector_version": COLLECTOR_VERSION,
        "timezone": "Asia/Seoul",
        "from": frm.isoformat(),
        "as_of": as_of.isoformat(),
        "as_of_is": "exclusive upper bound",
        "counts": {"events": len(events), "entities": len(entities)},
        "sources": [sources[n].report() for n in ("git", "note", "agenda")],
    }
    audit = {
        "events_by_source": tally(e["source"] for e in events),
        "events_by_time_kind": tally(e["time_kind"] for e in events),
        "events_by_precision": tally(e["ts_precision"] for e in events),
        "entities_by_kind": tally(e.split(":")[0] for e in entities),
        "span": {"first": events[0]["date_kst"] if events else None,
                 "last": events[-1]["date_kst"] if events else None},
        "rejected": tally(r["reason"] for r in rejected),
        "rejected_samples": sorted(
            ({"reason": r["reason"], "where": r["where"]} for r in rejected),
            key=lambda r: (r["reason"], r["where"]))[:10],
        "unresolved_short_sha": sources["agenda"].unresolved_short,
        "unmapped_repos": len(repos.unmapped),
    }

    if args.out:
        with open(args.out, "w") as fh:
            for e in events:
                fh.write(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n")
        log(f"wrote {len(events)} events -> {args.out}")

    json.dump({"manifest": manifest, "audit": audit}, sys.stdout,
              ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")

    dead = [n for n in sources if sources[n].status == "unreadable"]
    if dead:
        log(f"FATAL: source unreadable: {', '.join(dead)} — this is not a FULL.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
