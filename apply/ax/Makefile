.PHONY: all cuts html pdf md check leak repro publish clean

SOURCE := ax.org
# `ax.org` #+includes the timeline reading, so the reading is a source of every view. Make
# could not see that — a regenerated projection left the .tex untouched and the PDFs kept
# printing the previous numbers while the build said OK. A document that cites an axis must
# rebuild when the axis moves.
INCLUDES := ../../timeline/projection.org
BUILD := build
# One document read at four depths — d0 the claim, d1 the shape of the evidence, d2 the
# events and numbers, d3 the ledger. These are not three documents that must be kept in
# step with each other: none of them is authored, so no view can fall behind another.
# (That removes drift between derivatives. It does not make the document consistent —
# two sentences in one source can still contradict, and only reading catches that.)
# The names say which slice, because "Competency" and "Portfolio" said which *document*
# and there is only one now.
OVERVIEW := $(BUILD)/KimJunghan_AX_Overview
RECORD := $(BUILD)/KimJunghan_AX_Record
DETAIL := $(BUILD)/KimJunghan_AX_Detail.md
MANIFEST := $(BUILD)/depth.json
LEAKWORDS := leakwords.txt
# A verbatim <head> include (Umami tag, JSON-LD identity schema, favicon) injected AFTER
# pandoc, on purpose: it holds an external <script src> that --embed-resources would inline
# (breaking Umami's data-website-id and forcing a network fetch), so it must not pass through
# pandoc. The injection is a static text insert before </head> — deterministic and offline.
HEAD := assets/head.html
# llms.txt is a static public file, not a pandoc output; it ships to the web root next to the
# five generated views. The leak gate already scans it because it is a text file in this dir.
LLMS := llms.txt
# robots.txt and sitemap.xml are static public files too — authored here, gated by the same
# leak scan (any text file in this dir), and shipped to the web root. The sitemap lists the
# canonical views + llms.txt (not itself or robots.txt) and carries no <lastmod>, so two clean
# builds stay byte-identical.
ROBOTS := robots.txt
SITEMAP := sitemap.xml
# The depth dial: style + behaviour for the one view where the reader chooses a depth.
# Kept out of $(HEAD) on purpose — that include carries the three site-level things (the
# analytics tag, the identity schema, the icon) and goes into both pages, while this goes
# into the record alone and is about reading, not identity.
DIAL := assets/depth.html

# Insert $(HEAD) verbatim before the first </head> of an HTML file, in place. awk reads the
# include fully (FNR==NR) then streams the target, emitting the buffer once at </head>.
define inject_head =
awk 'FNR==NR{h=h $$0 ORS; next} /<\/head>/ && !done{printf "%s", h; done=1} {print}' $(HEAD) $(1) > $(1).tmp && mv $(1).tmp $(1)
endef

# Same trick at the other end of the document.
define inject_dial =
awk 'FNR==NR{h=h $$0 ORS; next} /<\/body>/ && !done{printf "%s", h; done=1} {print}' $(DIAL) $(1) > $(1).tmp && mv $(1).tmp $(1)
endef

# Stamp each heading with the depth it was authored at, so the dial can hide tiers at
# runtime. Pandoc is not asked for --section-divs: this stylesheet is built on flat
# sibling selectors (`body > header + h1 ~ ul`), and wrapping every heading in a <section>
# would silently restyle the whole document to buy nesting the dial does not need — it
# hides a heading together with the siblings that follow it.
#
# The match is positional: the Nth heading carrying an id is the Nth manifest row. That
# holds because both build.el's scan and pandoc's output follow document order, and the
# record is the depth-3 cut, which keeps every heading. It is an invariant, not a hope, so
# `check` counts both sides rather than trusting them.
#
# This awk is line-based, which is a second, quieter assumption: a heading whose tag spans
# a newline is not seen, and — worse than going unstamped — it does not advance the
# counter, so every heading after it receives the depth belonging to its neighbour. Pandoc
# wrapped exactly two of them once (long Korean ids), and the dial would have revealed the
# wrong paragraphs with no error anywhere. Hence `--wrap=none` on the HTML writers. The
# count comparison in `check` is what caught it and is what would catch it again.
define stamp_depth =
awk 'FNR==NR { if (match($$0, /"depth": [0-9]+/)) \
                 d[++n] = substr($$0, RSTART + 9, RLENGTH - 9); \
               next } \
     /<h[1-6][^>]*id="/ { i++; sub(/<h[1-6]/, "& data-depth=\"" d[i] "\"") } \
     { print }' $(MANIFEST) $(1) > $(1).tmp && mv $(1).tmp $(1)
endef

# Same tracked inputs, same bytes. XeLaTeX and xdvipdfmx stamp a wall clock into every PDF
# unless these two are set, and then "the build is deterministic" is a claim the build does
# not keep. The epoch is the commit that last touched the source; an untracked tree falls
# back to 0, which still does not vary between two runs. `make repro` is the witness.
SOURCE_DATE_EPOCH := $(shell git log -1 --format=%ct -- $(SOURCE) 2>/dev/null | grep . || echo 0)
export SOURCE_DATE_EPOCH
export FORCE_SOURCE_DATE := 1

all: html pdf md $(MANIFEST)

# d0 is the front door; d3 is the whole document. The web record and the detailed Markdown
# are the same cut in two formats — there is no separate "detail" authoring pass.
cuts: $(BUILD)/d0.org $(BUILD)/d3.org $(MANIFEST)

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/d0.org: $(SOURCE) $(INCLUDES) build.el | $(BUILD)
	emacs -Q --batch --script build.el cut $(SOURCE) 0 $@

$(BUILD)/d3.org: $(SOURCE) $(INCLUDES) build.el | $(BUILD)
	emacs -Q --batch --script build.el cut $(SOURCE) 3 $@

$(MANIFEST): $(SOURCE) $(INCLUDES) build.el | $(BUILD)
	emacs -Q --batch --script build.el manifest $(SOURCE) 3 $@

html: $(BUILD)/index.html $(BUILD)/record.html $(BUILD)/paper.css

$(BUILD)/index.html: $(BUILD)/d0.org assets/paper.css $(HEAD)
	pandoc $< -f org -t html5 --standalone --embed-resources --wrap=none \
	  --css assets/paper.css --metadata title="에이전트 플랫폼 운영과 조직 AX 전환" -o $@
	$(call inject_head,$@)

# The record does NOT embed its resources, and the front door does. That asymmetry is the
# point, not an oversight.
#
# Embedding turned four cleared PNGs into 3.2MB of base64 inside a text file, and two
# things broke at once. The page went from 62KB to 3.3MB. And the leak gate — which reads
# text, and base64 is text — started matching a three-character denylisted term fifteen
# times in the noise, at exactly the rate random base64 produces a three-character string.
# A gate that cries wolf on its own artifact is worse than no gate, because the next real
# hit reads like more noise.
#
# Neither problem is fixed by teaching the gate to skip base64: that would carve out a
# region of a public artifact that nobody scans, which is the kind of hole this file
# exists to close. They are both fixed by not putting binary in the text. The images are
# published as files anyway, served from the same origin, and cached by the browser.
#
# index.html keeps embedding because it carries no images and stays one 15KB file someone
# can save or mail. paper.css is copied next to the record so the build directory and the
# web root resolve the stylesheet identically.
$(BUILD)/paper.css: assets/paper.css | $(BUILD)
	cp $< $@

$(BUILD)/record.html: $(BUILD)/d3.org $(BUILD)/paper.css $(HEAD) $(DIAL) $(MANIFEST) $(IMAGES)
	pandoc $< -f org -t html5 --standalone --toc --toc-depth=2 --wrap=none \
	  --css paper.css --metadata title="에이전트 플랫폼 운영과 조직 AX 전환 — 기록" -o $@
	$(call inject_head,$@)
	$(call stamp_depth,$@)
	$(call inject_dial,$@)

pdf: $(OVERVIEW).pdf $(RECORD).pdf

$(OVERVIEW).tex: $(SOURCE) $(INCLUDES) build.el | $(BUILD)
	emacs -Q --batch --script build.el latex $(SOURCE) 1 $@

$(RECORD).tex: $(SOURCE) $(INCLUDES) build.el | $(BUILD)
	emacs -Q --batch --script build.el latex $(SOURCE) 2 $@

$(OVERVIEW).pdf: $(OVERVIEW).tex
	latexmk -xelatex -interaction=nonstopmode -output-directory=$(BUILD) $<

$(RECORD).pdf: $(RECORD).tex
	latexmk -xelatex -interaction=nonstopmode -output-directory=$(BUILD) $<

md: $(DETAIL)

$(DETAIL): $(BUILD)/d3.org
	pandoc $< -f org -t gfm --wrap=none --toc -o $@

# The gate greps what actually ships, not only what was authored — a term can reach a PDF
# through the build with the Org source clean, and the artifacts are what gets uploaded.
# It discovers its own inputs: every text file under this directory is a public surface once
# committed, and a hand-kept list goes stale the first time someone adds one. `grep -Iq .`
# is the binary filter. The terms live in a gitignored file, because a gate that spells out
# what it forbids publishes it. When that file is absent (a public checkout) the gate says
# so instead of passing quietly — a silent skip reads exactly like a pass.
leak: html pdf md
	@if [ ! -f $(LEAKWORDS) ]; then \
	  echo 'SKIP: local leakword gate unavailable ($(LEAKWORDS) absent)'; exit 0; fi; \
	tmp=$$(mktemp -d); \
	pdftotext $(OVERVIEW).pdf $$tmp/overview.txt; \
	pdftotext $(RECORD).pdf $$tmp/record.txt; \
	targets=$$(find . -type f -not -path './build/*' -not -path './.git/*' \
	  -not -name '$(LEAKWORDS)' -exec grep -Iq . {} \; -print | sort); \
	targets="$$targets $(BUILD)/index.html $(BUILD)/record.html $(DETAIL) \
	  $$tmp/overview.txt $$tmp/record.txt"; \
	hits=0; n=0; \
	while IFS= read -r w; do \
	  case "$$w" in ''|\#*) continue;; esac; \
	  n=$$((n+1)); \
	  found=$$(grep -lF -- "$$w" $$targets 2>/dev/null | tr '\n' ' '); \
	  if [ -n "$$found" ]; then echo "LEAK: a denylisted term appears in: $$found"; hits=1; fi; \
	done < $(LEAKWORDS); \
	rm -rf $$tmp; \
	[ $$hits -eq 0 ] || exit 1; \
	echo "OK: leak gate — $$n terms against $$(echo $$targets | wc -w) files (sources + shipped artifacts)"; \
	blind=$$(find . -type f -not -path './build/*' -not -path './.git/*' \
	  -not -name '$(LEAKWORDS)' -not -name '*.lock' \
	  -exec sh -c 'grep -Iq . "$$1" || echo "$$1"' _ {} \; | sort); \
	if [ -n "$$blind" ]; then \
	  echo "BLIND: this gate reads text. It did not read, and cannot read, these:"; \
	  echo "$$blind" | sed 's/^/         /'; \
	  echo "       A term rendered into an image passes every check in this file."; \
	  echo "       Images are cleared by reading them, not by running make."; \
	fi

check: all leak
	test -s $(BUILD)/index.html
	test -s $(BUILD)/record.html
	test -s $(OVERVIEW).pdf
	test -s $(RECORD).pdf
	test -s $(DETAIL)
	grep -q 'Read the record' $(BUILD)/index.html
	grep -q 'timeline-projection' $(BUILD)/record.html
# The post-pandoc head injection must actually land in both shipped HTML files. A silent
# failure of the inject step would ship pages with no analytics, no identity schema, no icon —
# and nothing else would say so, exactly the class of quiet gap this Makefile checks for.
	grep -q 'data-website-id="e3d37714' $(BUILD)/index.html
	grep -q 'data-website-id="e3d37714' $(BUILD)/record.html
	grep -q 'application/ld+json' $(BUILD)/index.html
	grep -q 'application/ld+json' $(BUILD)/record.html
	grep -q 'rel="icon"' $(BUILD)/index.html
# Search Console verifies by fetching the root URL, so the token must survive into index.html.
# Losing it silently un-verifies the property — Search Console stops reporting and says nothing
# here.
	grep -q 'name="google-site-verification"' $(BUILD)/index.html
# The shipped pages, not only the source stylesheet, must retain the CSS-first accessibility
# baseline: visible keyboard focus, anchor landing clearance, horizontally scrollable tables,
# and figures constrained to the content box. Without the last rule a 1600px diagram overflows
# a phone viewport and drags the page's horizontal scroll with it — the figure's own box is
# already constrained by `body > *`, so the image is the one thing that escapes.
	grep -q 'focus-visible' $(BUILD)/index.html
	grep -q '<link rel="stylesheet" href="paper.css"' $(BUILD)/record.html
	grep -q 'focus-visible' $(BUILD)/paper.css
	grep -q 'scroll-margin-top' $(BUILD)/paper.css
	grep -q 'overflow-x: auto' $(BUILD)/paper.css
	grep -A6 '^figure img {' $(BUILD)/paper.css | grep -q 'max-width: 100%'
# No binary may re-enter the text artifacts. base64 both bloats the record and fills the
# leak gate with false matches, so its absence is checked rather than remembered.
	! grep -q 'base64,' $(BUILD)/record.html
	test -s $(LLMS)
	test -s $(ROBOTS)
	test -s $(SITEMAP)
# robots.txt opens the whole site and names exactly one canonical sitemap; sitemap.xml lists
# exactly the six public URLs (five views + llms.txt) and nothing else — not itself, not
# robots.txt — and carries no <lastmod>, which would put a wall clock in a tracked file and
# break `make repro`. These name the URLs, not any prose, so a content edit does not disturb them.
	grep -q '^Sitemap: https://ax.junghanacs.com/sitemap.xml$$' $(ROBOTS)
	test "$$(grep -c '<loc>' $(SITEMAP))" -eq 6
	grep -q '<loc>https://ax.junghanacs.com/</loc>' $(SITEMAP)
	grep -q '<loc>https://ax.junghanacs.com/record.html</loc>' $(SITEMAP)
	grep -q '<loc>https://ax.junghanacs.com/KimJunghan_AX_Overview.pdf</loc>' $(SITEMAP)
	grep -q '<loc>https://ax.junghanacs.com/KimJunghan_AX_Record.pdf</loc>' $(SITEMAP)
	grep -q '<loc>https://ax.junghanacs.com/KimJunghan_AX_Detail.md</loc>' $(SITEMAP)
	grep -q '<loc>https://ax.junghanacs.com/llms.txt</loc>' $(SITEMAP)
	! grep -q 'lastmod' $(SITEMAP)
	pdftotext $(OVERVIEW).pdf - | grep -q '에이전트 플랫폼 운영'
	pdftotext $(RECORD).pdf - | grep -q '에이전트 플랫폼 운영'
# Both PDFs must be A4. acmart hard-codes letterpaper inside the class — it is an ACM
# format and ACM prints on US letter — so the page size is not something the document asks
# for and gets; it is something `build.el` has to take back with a \geometry re-call. A
# silent revert of that line yields a document that still builds, still passes every other
# gate here, and quietly ships on the wrong paper to a reader who prints it. Measured from
# the file rather than from the source: pdfinfo reports what the writer actually wrote.
# 595x842pt is A4 to the point; the tolerance absorbs pdfinfo's rounding, nothing more.
	@for p in $(OVERVIEW).pdf $(RECORD).pdf; do \
	   sz=$$(pdfinfo $$p | sed -n 's/^Page size: *\([0-9.]*\) x \([0-9.]*\) .*/\1 \2/p' | head -1); \
	   w=$${sz%% *}; h=$${sz##* }; \
	   awk -v w="$$w" -v h="$$h" -v p="$$p" 'BEGIN{ \
	     if (w < 594 || w > 597 || h < 840 || h > 843) { \
	       printf "PAPER: %s is %s x %s pt — not A4 (595 x 842). acmart pins letterpaper\n", p, w, h; \
	       printf "       inside the class; the \\geometry re-call in build.el is what undoes it.\n"; \
	       exit 1 } \
	     printf "  ok  %s — A4 %s x %s pt\n", p, w, h }'; \
	 done
# Exactly one title block. `ax.org` carries a raw acmart topmatter block because ox-latex
# emits no \subtitle, \affiliation or \email for this class, and Org will happily print a
# second one of its own on top of it — both PDFs shipped the title twice and the author as
# "김정한 and 김정한". The export plist cannot stop it: an in-buffer #+options beats the
# plist, the same way it already defeats toc:nil (see the note at the top of ax.org). The
# fix belongs in #+options; this is the witness that it stayed fixed. Counting \maketitle
# names the defect exactly and does not depend on a single word of the prose.
	test "$$(grep -c '\\maketitle' $(OVERVIEW).tex)" -eq 1
	test "$$(grep -c '\\maketitle' $(RECORD).tex)" -eq 1
	! pdftotext $(OVERVIEW).pdf - | grep -q 'and 김정한'
	! pdftotext $(RECORD).pdf - | grep -q 'and 김정한'
# The depth machine, checked against the manifest rather than against any sentence. Org
# tag inheritance is what makes the cut cheap, and it is also what makes a bad cut silent:
# a heading that inherits a deeper tag than it declares simply does not appear, and a
# missing section looks exactly like one that was never written. `build.el' refuses a
# non-monotonic tree; these three lines confirm the survivors were actually counted out.
#
# The last one is load-bearing beyond this file: the depth dial stamps data-depth onto
# pandoc's <section> elements positionally, which is only safe while the Nth section is
# the Nth manifest row. Assert it here, where it is cheap, instead of discovering it as a
# dial that reveals the wrong paragraphs.
	@m=$(MANIFEST); \
	 for d in 1 2; do \
	   want=$$(grep -oE '"depth": [0-'$$d']' $$m | wc -l); \
	   case $$d in 1) tex=$(OVERVIEW).tex;; 2) tex=$(RECORD).tex;; esac; \
	   got=$$(grep -cE '^\\(sub)*section' $$tex); \
	   [ "$$want" -eq "$$got" ] || { \
	     echo "DEPTH: d$$d expected $$want headings, .tex has $$got"; exit 1; }; \
	   echo "  ok  d$$d — $$got headings"; \
	 done; \
	 want=$$(grep -c '"depth"' $$m); \
	 got=$$(grep -oE '<h[1-6][^>]*id="' $(BUILD)/record.html | wc -l); \
	 [ "$$want" -eq "$$got" ] || { \
	   echo "DEPTH: manifest has $$want headings, record.html has $$got —"; \
	   echo "       positional data-depth stamping would be off by $$((want-got))"; exit 1; }; \
	 stamped=$$(grep -oE '<h[1-6] data-depth="[0-9]"' $(BUILD)/record.html | wc -l); \
	 [ "$$want" -eq "$$stamped" ] || { \
	   echo "DEPTH: $$want headings but $$stamped carry data-depth — the dial would leave"; \
	   echo "       the unstamped ones permanently visible"; exit 1; }; \
	 grep -q '\.depth-dial {' $(BUILD)/record.html || { \
	   echo 'DEPTH: the dial stylesheet did not reach record.html'; exit 1; }; \
	 grep -q 'ax-depth' $(BUILD)/record.html || { \
	   echo 'DEPTH: the dial script did not reach record.html'; exit 1; }; \
	 echo "  ok  d3 — $$got headings, all stamped, dial present"
# Emphasis must have been *rendered*, not printed. Org marks bold `*so*`; writing Markdown's
# `**so**` in the source is not an error anywhere in the toolchain — it simply sets the
# asterisks in the page, and 64 lines of the two PDFs shipped that way. Korean makes it
# sharper: a closing marker followed immediately by a particle (`*운영*했습니다`) is not
# emphasis to Org or to pandoc either, so it also prints. The extracted text is the witness
# — a submitted PDF has no business containing an asterisk at all.
	! pdftotext $(OVERVIEW).pdf - | grep -q '[*]'
	! pdftotext $(RECORD).pdf - | grep -q '[*]'
	grep -q '<strong>' $(BUILD)/record.html
# Verbatim has the same failure as emphasis, and one more way to reach it: `=like this=`
# cannot cross a line break. A caption wrapped mid-span printed `=DENOTE GRAPH=` into both
# PDFs with nothing complaining — Org saw two unbalanced markers on two lines and did the
# only thing it could, which was to set them. The .tex is the witness: had Org rendered the
# span it would read \texttt{...}, so a bare `=` before a capital is markup that did not
# take. Measured against the current document this matches the one real defect and nothing
# else — every legitimate `=` here is followed by a lowercase letter or a digit. A shell
# assignment like PATH=/usr in a source block would trip it; that is the safe direction,
# because the alternative is shipping the markers again.
# Scanned from \begin{document} on, not over the whole file. The defect is Org markup that
# did not render, and Org markup exists only in the body — everything above \begin{document}
# is `#+latex_header:` passed through literally, where `=` before a capital is ordinary
# LaTeX (`[Ligatures=TeX]`, and any key=Value a future preamble adds). Scanning the preamble
# made the gate fail on its own typesetting the day A4 arrived. The alternative — a
# whitelist of known-good spellings — grows a line every time the preamble does, and each
# line is a hole aimed at exactly the region the gate cannot see into. Narrowing the window
# to where the defect can occur keeps the assertion absolute inside it.
	! sed -n '/\\begin{document}/,$$p' $(OVERVIEW).tex | grep -qE '=[A-Z]'
	! sed -n '/\\begin{document}/,$$p' $(RECORD).tex | grep -qE '=[A-Z]'
# A table wider than the text block does not wrap — it runs off the right edge of the page
# and the reader loses the column. LaTeX says so in the log and nothing else does.
	! grep -q 'Overfull \\hbox' $(BUILD)/KimJunghan_AX_Overview.log
	! grep -q 'Overfull \\hbox' $(BUILD)/KimJunghan_AX_Record.log
	@printf 'OK: one Org source -> one document at four depths (d0 door, d1+d2 PDFs, d3 record + Markdown)\n'
	@if grep -q 'data-placeholder="true"' $(BUILD)/record.html; then \
	  printf 'PLACEHOLDER: the timeline mount carries no projection yet — replace it or hide\n'; \
	  printf '             the section before this record is submitted.\n'; fi

# What the build actually guarantees, measured instead of asserted. It builds twice from
# clean and compares each shipped artifact, and it reports the PDF bytes rather than
# assuming them: an earlier version of this target printed "PDF bytes differ" without ever
# comparing them, which is the same sin — a sentence louder than its evidence — that the
# whole file exists to avoid.
#
# HTML, Markdown, and the PDFs' extracted text must be identical; a difference there is a
# failure. The PDF *bytes* are reported and not enforced: XeLaTeX's writer regenerates the
# trailer's file identifier on every run and this toolchain has no flag to suppress it.
# Layout is not compared at all — do not claim it is.
# Two builds only compare if they were given the same inputs. They were not, once: a
# sibling session edited ax.org between them, every artifact came out DIFFERS, and the
# obvious reading — "the build stopped reproducing" — was wrong. A repro run that cannot
# tell a real regression from a moving source is not a witness, so it takes the inputs'
# fingerprint before the first build and again after the second, and calls the difference
# by its name instead of blaming the build. A prose rule ("only run this on a quiet tree")
# would not have caught it; nobody reads a rule at the moment they are about to break it.
INPUTS := $(SOURCE) $(INCLUDES) build.el assets/paper.css $(HEAD) $(DIAL) \
          $(LLMS) $(ROBOTS) $(SITEMAP)
# The image set is discovered when the fingerprint runs, not when make parses this file.
# `$(IMAGES)` is a parse-time wildcard, so hashing it would have frozen the file list at
# startup: an image *added* mid-run would land in the second build and leave the after
# fingerprint unchanged — the one direction of drift the check exists to catch. Hashing
# `find` output covers additions, deletions and edits alike, because the paths are part of
# what gets hashed.
INPUT_FP = { cat $(INPUTS) 2>/dev/null; \
             find images -type f 2>/dev/null | sort | xargs -r sha256sum; \
           } | sha256sum | cut -d' ' -f1
# Expanded once, when make parses this file — which is before either build runs, so it is
# the "before" reading with no temp file to carry it across the two clean builds.
INPUTS_FP := $(shell $(INPUT_FP))

repro:
	@$(MAKE) --no-print-directory clean >/dev/null
	@$(MAKE) --no-print-directory all >/dev/null 2>&1 || { echo 'repro: first build failed'; exit 1; }
	@a=$$(mktemp -d); b=$$(mktemp -d); \
	 snap() { d=$$1; cp $(BUILD)/index.html $(BUILD)/record.html $(DETAIL) \
	            $(OVERVIEW).pdf $(RECORD).pdf $$d/; \
	          pdftotext $(OVERVIEW).pdf $$d/overview.txt; \
	          pdftotext $(RECORD).pdf $$d/record.txt; }; \
	 snap $$a; \
	 $(MAKE) --no-print-directory clean >/dev/null; \
	 $(MAKE) --no-print-directory all >/dev/null 2>&1 || { echo 'repro: second build failed'; exit 1; }; \
	 snap $$b; \
	 after=$$($(INPUT_FP)); \
	 if [ "$$after" != "$(INPUTS_FP)" ]; then \
	   rm -rf $$a $$b; \
	   echo 'NON-STATIONARY INPUT: a source changed while repro was running.'; \
	   echo "  before  $(INPUTS_FP)"; \
	   echo "  after   $$after"; \
	   echo '  The two builds were given different inputs, so any difference between them'; \
	   echo '  says nothing about reproducibility. Re-run once the tree is quiet.'; \
	   exit 1; \
	 fi; \
	 fail=0; \
	 for f in index.html record.html $(notdir $(DETAIL)) overview.txt record.txt; do \
	   if cmp -s $$a/$$f $$b/$$f; then echo "  same     $$f"; \
	   else echo "  DIFFERS  $$f"; fail=1; fi; \
	 done; \
	 for f in $(notdir $(OVERVIEW)).pdf $(notdir $(RECORD)).pdf; do \
	   if cmp -s $$a/$$f $$b/$$f; then echo "  same     $$f (bytes)"; \
	   else echo "  differ   $$f — $$(cmp -l $$a/$$f $$b/$$f | wc -l) of $$(stat -c%s $$a/$$f) bytes (trailer file id; not enforced)"; fi; \
	 done; \
	 rm -rf $$a $$b; \
	 [ $$fail -eq 0 ] || { echo 'DIFFERS: the build did not reproduce'; exit 1; }; \
	 echo 'OK: two clean builds — identical HTML, Markdown, and extracted PDF text'

# The web root is not the build directory. `build/` also holds the .tex, the LaTeX logs, the
# .xdv, and the profile cuts — intermediates that say how the document was made and would be
# served to anyone who guessed the filename. So publishing copies out the eight files that are
# meant to be read — the five generated views, llms.txt, and the robots.txt / sitemap.xml pair
# — into a directory that holds nothing else.
#
# It runs `check` first, and that is the point: the leak gate is what stands between the
# denylist and a public URL. Never wire a web server at `build/`, and never publish by
# copying past this target.
PUBLISH ?= /home/junghan/docker-data/ax

# What the web root is allowed to hold, as data rather than as a number. A literal count
# was wrong the moment a second kind of published file appeared; images will make it wrong
# again. Everything below derives from these two lists.
# Content images ship as files, not only as embeds. The HTML views inline them and the PDFs
# carry them, but `KimJunghan_AX_Detail.md` references them by relative path — publish the
# document without the pictures and the Markdown view, the one an agent reads, arrives full
# of broken links. `images/README.md` is the clearance ledger and stays here: it is how we
# decide what may ship, not something that ships.
IMAGES := $(wildcard images/*.png) $(wildcard images/*.jpg) $(wildcard images/*.svg)

VIEWS := index.html record.html paper.css $(notdir $(OVERVIEW)).pdf $(notdir $(RECORD)).pdf \
         $(notdir $(DETAIL)) $(LLMS) $(ROBOTS) $(SITEMAP) $(IMAGES)

# Legacy URL aliases, as `served-name:view-it-copies`. These are not extra artifacts —
# each is a byte-identical copy of a view that was renamed, kept so a URL that has been
# public since 2026-07-15 keeps resolving. The canonical names are what sitemap.xml and
# llms.txt advertise; an alias is never advertised, only honoured. Retire one by deleting
# its line, which makes that URL 404 on the next publish, deliberately and visibly.
ALIASES := KimJunghan_AX_Competency.pdf:$(notdir $(OVERVIEW)).pdf \
           KimJunghan_AX_Portfolio.pdf:$(notdir $(RECORD)).pdf

PUBLISHED := $(VIEWS) $(foreach a,$(ALIASES),$(firstword $(subst :, ,$(a))))

publish: check
	@mkdir -p $(PUBLISH)
	@cp build/index.html build/record.html build/paper.css $(OVERVIEW).pdf $(RECORD).pdf $(DETAIL) \
	  $(LLMS) $(ROBOTS) $(SITEMAP) $(PUBLISH)/
	@if [ -n "$(IMAGES)" ]; then mkdir -p $(PUBLISH)/images && cp $(IMAGES) $(PUBLISH)/images/; fi
	@for a in $(ALIASES); do \
	   old=$${a%%:*}; new=$${a##*:}; \
	   cp $(PUBLISH)/$$new $(PUBLISH)/$$old; \
	   cmp -s $(PUBLISH)/$$old $(PUBLISH)/$$new || { \
	     echo "ALIAS: $$old is not byte-identical to $$new"; exit 1; }; \
	   printf '  alias    %s == %s\n' "$$old" "$$new"; \
	 done
# Copying alone cannot keep the promise above. Rename a view — as the depth redesign
# renamed both PDFs — and the old file keeps being served from its old URL: stale, no
# longer produced by any build, and never re-examined by a leak gate that only ever sees
# what the current source generates. An alias is that same file kept *on purpose* and
# proved identical; anything else that survives here is an accident. So publishing states
# the set it intends and then makes the directory equal to it.
	@cd $(PUBLISH) && find . -type f -printf '%P\n' | sort > /tmp/ax-actual.$$$$; \
	 printf '%s\n' $(PUBLISHED) | sort > /tmp/ax-want.$$$$; \
	 comm -23 /tmp/ax-actual.$$$$ /tmp/ax-want.$$$$ | while read -r f; do \
	   printf '  retired  %s (its URL now 404s)\n' "$$f"; rm -f "$$f"; \
	 done; \
	 find . -type f -printf '%P\n' | sort > /tmp/ax-actual.$$$$; \
	 if ! diff -q /tmp/ax-want.$$$$ /tmp/ax-actual.$$$$ >/dev/null; then \
	   echo 'PUBLISH: the web root does not equal the published set:'; \
	   diff /tmp/ax-want.$$$$ /tmp/ax-actual.$$$$ | sed 's/^/    /'; \
	   rm -f /tmp/ax-want.$$$$ /tmp/ax-actual.$$$$; exit 1; \
	 fi; \
	 n=$$(wc -l < /tmp/ax-want.$$$$); \
	 rm -f /tmp/ax-want.$$$$ /tmp/ax-actual.$$$$; \
	 printf 'OK: web root == published set (%s files: %s views + %s legacy aliases) -> $(PUBLISH)\n' \
	   "$$n" "$(words $(VIEWS))" "$(words $(ALIASES))"

clean:
	rm -rf $(BUILD)
