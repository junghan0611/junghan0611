#!/usr/bin/env bash
set -euo pipefail

# run.sh — edit → live-update loop for ax.junghanacs.com
#
# The AX evidence surface is LIVE. This script is the seam between an edit to the
# authored source and what a reviewer's agent reads at the public URL. It is written for
# a fresh session (human or agent) to enter cold: `./run.sh publish` builds, passes the
# leak gate, and copies the five public files to the web root Caddy serves — no server
# restart. Serving itself (Caddy, TLS, Umami, Remark42) is NOT here; that is the
# nixos-config maintainer's surface (see `help`).

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
info()    { echo -e "${BLUE}ℹ ${NC}$1"; }
success() { echo -e "${GREEN}✓${NC} $1"; }
warn()    { echo -e "${YELLOW}⚠${NC} $1"; }
error()   { echo -e "${RED}✗${NC} $1"; }

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AX="$REPO/apply/ax"
WEB_ROOT="${AX_WEB_ROOT:-/home/junghan/docker-data/ax}"   # == Makefile PUBLISH; Caddy mounts :ro
LIVE_URL="https://ax.junghanacs.com"
PUBLIC_FILES=(index.html record.html KimJunghan_AX_Competency.pdf KimJunghan_AX_Portfolio.pdf KimJunghan_AX_Detail.md)

# The dossier's toolchain (emacs, pandoc, xelatex, pdftotext, Korean fonts) comes from the
# flake, so every build runs inside `nix develop`. A shell that resolves these from the host
# silently substitutes fonts and drops the leak gate's pdftotext.
in_nix() { ( cd "$AX" && nix develop -c "$@" ); }

# The timeline reading is a committed artifact regenerated from the LOCAL FULL, not built by
# make. Run this only when the axis moved (a fresh events.jsonl + snapshot.json). A prose
# edit to ax.org does not need it.
cmd_axis() {
    if [[ ! -f "$REPO/events.jsonl" || ! -f "$REPO/snapshot.json" ]]; then
        error "no LOCAL FULL here — events.jsonl / snapshot.json missing"
        info  "the axis is collected on the machine that owns the sources; this may not be it."
        info  "regenerate the FULL with the timeline skill (collect.py) before --axis."
        return 2
    fi
    info "regenerating the public reading from the LOCAL FULL"
    python3 "$REPO/timeline/project.py" "$REPO/events.jsonl" --snapshot "$REPO/snapshot.json" \
        --md "$REPO/timeline/projection.md" --org "$REPO/timeline/projection.org"
    success "timeline/projection.{md,org} regenerated — now: ./run.sh publish"
}

cmd_build() { info "building 5 views (landing · record · 2 PDFs · detail md)"; in_nix make all; }
cmd_check() { info "build + gates (leak gate, emphasis, overfull, mount witness)"; in_nix make check; }
cmd_test()  { info "timeline contract tests"; python3 "$REPO/timeline/test_timeline.py"; }

# The one that changes what the world sees. `make publish` depends on `check`, so the leak
# gate is always between the denylist and the URL. Nothing else may enter the web root.
cmd_publish() {
    info "publishing to $WEB_ROOT (gated by make check)"
    AX_PUBLISH="$WEB_ROOT" in_nix env PUBLISH="$WEB_ROOT" make publish
    success "live at $LIVE_URL — verify with: ./run.sh live"
}

# Trust nothing: read the live site from outside and compare its bytes to what was published.
cmd_live() {
    command -v curl >/dev/null || { error "curl not found"; return 1; }
    info "checking $LIVE_URL from outside"
    local root code ct
    code=$(curl -so /dev/null -w '%{http_code}' "$LIVE_URL/") || true
    [[ "$code" == "200" ]] && success "landing: $code" || { error "landing: $code"; return 1; }
    for f in "${PUBLIC_FILES[@]}"; do
        code=$(curl -so /dev/null -w '%{http_code}' "$LIVE_URL/$f")
        if [[ -f "$WEB_ROOT/$f" ]]; then
            local a b; a=$(curl -s "$LIVE_URL/$f" | sha256sum | cut -c1-12)
            b=$(sha256sum "$WEB_ROOT/$f" | cut -c1-12)
            [[ "$a" == "$b" ]] && success "$f  $code  bytes match" || warn "$f  $code  LIVE≠LOCAL ($a vs $b)"
        else
            echo "  $f  $code  (not published locally)"
        fi
    done
    # Intermediates must not be reachable — the web root is not the build dir.
    for f in KimJunghan_AX_Competency.tex KimJunghan_AX_Competency.log record.org; do
        code=$(curl -so /dev/null -w '%{http_code}' "$LIVE_URL/$f")
        [[ "$code" == "404" ]] || warn "intermediate reachable: /$f -> $code (expected 404)"
    done
}

# The whole loop when the axis moved: reading → build+gate → live → verify.
cmd_all() { cmd_axis && cmd_publish && cmd_live; }

usage() {
    echo -e "$(cat <<EOF
${BLUE}ax.junghanacs.com — edit → live-update${NC}   (live: $LIVE_URL)

  ${YELLOW}./run.sh publish${NC}   build, pass the leak gate, copy 5 public files to the web root → LIVE
  ${YELLOW}./run.sh axis${NC}      regenerate timeline/projection.{md,org} from the LOCAL FULL
                     (only when the axis moved; a prose edit does not need it)
  ${YELLOW}./run.sh all${NC}       axis → publish → live  (full loop after a new FULL)

  ./run.sh build     5 views without publishing (apply/ax/build/)
  ./run.sh check     build + all gates, no publish
  ./run.sh live      read the live site from outside; compare bytes to what was published
  ./run.sh test      timeline contract tests (project.py / view.py / collect.py)

${YELLOW}Typical loop${NC}
  edit apply/ax/ax.org   →   ./run.sh publish   →   ./run.sh live
  (axis changed? ./run.sh axis first)

${YELLOW}web root${NC}  $WEB_ROOT   (Caddy read-only mount — NOT apply/ax/build/)
             Never drop a file here outside ./run.sh publish: the leak gate is the only guard.

${YELLOW}Serving is not here.${NC}  Caddy vhost, TLS, directory listing, .md content-type, Umami
  analytics, and Remark42 comments live in nixos-config and are the maintainer's surface.
  Route those through the nixos-config maintainer (entwurf), not this repo.
EOF
)"
}

case "${1:-help}" in
    axis)             cmd_axis ;;
    build)            cmd_build ;;
    check)            cmd_check ;;
    publish)          cmd_publish ;;
    live)             cmd_live ;;
    test)             cmd_test ;;
    all)              cmd_all ;;
    help|-h|--help|"") usage ;;
    *)                error "unknown command: $1"; echo; usage; exit 1 ;;
esac
