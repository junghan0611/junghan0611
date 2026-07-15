.PHONY: all cuts html pdf md check leak repro publish clean

SOURCE := ax.org
# `ax.org` #+includes the timeline reading, so the reading is a source of every view. Make
# could not see that — a regenerated projection left the .tex untouched and the PDFs kept
# printing the previous numbers while the build said OK. A document that cites an axis must
# rebuild when the axis moves.
INCLUDES := ../../timeline/projection.org
BUILD := build
COMPETENCY := $(BUILD)/KimJunghan_AX_Competency
PORTFOLIO := $(BUILD)/KimJunghan_AX_Portfolio
DETAIL := $(BUILD)/KimJunghan_AX_Detail.md
LEAKWORDS := leakwords.txt
# A verbatim <head> include (Umami tag, JSON-LD identity schema, favicon) injected AFTER
# pandoc, on purpose: it holds an external <script src> that --embed-resources would inline
# (breaking Umami's data-website-id and forcing a network fetch), so it must not pass through
# pandoc. The injection is a static text insert before </head> — deterministic and offline.
HEAD := assets/head.html
# llms.txt is a static public file, not a pandoc output; it ships to the web root next to the
# five generated views. The leak gate already scans it because it is a text file in this dir.
LLMS := llms.txt

# Insert $(HEAD) verbatim before the first </head> of an HTML file, in place. awk reads the
# include fully (FNR==NR) then streams the target, emitting the buffer once at </head>.
define inject_head =
awk 'FNR==NR{h=h $$0 ORS; next} /<\/head>/ && !done{printf "%s", h; done=1} {print}' $(HEAD) $(1) > $(1).tmp && mv $(1).tmp $(1)
endef

# Same tracked inputs, same bytes. XeLaTeX and xdvipdfmx stamp a wall clock into every PDF
# unless these two are set, and then "the build is deterministic" is a claim the build does
# not keep. The epoch is the commit that last touched the source; an untracked tree falls
# back to 0, which still does not vary between two runs. `make repro` is the witness.
SOURCE_DATE_EPOCH := $(shell git log -1 --format=%ct -- $(SOURCE) 2>/dev/null | grep . || echo 0)
export SOURCE_DATE_EPOCH
export FORCE_SOURCE_DATE := 1

all: html pdf md

cuts: $(BUILD)/landing.org $(BUILD)/record.org $(BUILD)/detail.org

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/landing.org: $(SOURCE) $(INCLUDES) build.el | $(BUILD)
	emacs -Q --batch --script build.el cut $(SOURCE) landing $@

$(BUILD)/record.org: $(SOURCE) $(INCLUDES) build.el | $(BUILD)
	emacs -Q --batch --script build.el cut $(SOURCE) record $@

$(BUILD)/detail.org: $(SOURCE) $(INCLUDES) build.el | $(BUILD)
	emacs -Q --batch --script build.el cut $(SOURCE) detail $@

html: $(BUILD)/index.html $(BUILD)/record.html

$(BUILD)/index.html: $(BUILD)/landing.org assets/paper.css $(HEAD)
	pandoc $< -f org -t html5 --standalone --embed-resources \
	  --css assets/paper.css --metadata title="에이전트 플랫폼 운영과 조직 AX 전환" -o $@
	$(call inject_head,$@)

$(BUILD)/record.html: $(BUILD)/record.org assets/paper.css $(HEAD)
	pandoc $< -f org -t html5 --standalone --embed-resources --toc --toc-depth=2 \
	  --css assets/paper.css --metadata title="에이전트 플랫폼 운영과 조직 AX 전환 — 기록" -o $@
	$(call inject_head,$@)

pdf: $(COMPETENCY).pdf $(PORTFOLIO).pdf

$(COMPETENCY).tex: $(SOURCE) $(INCLUDES) build.el | $(BUILD)
	emacs -Q --batch --script build.el latex $(SOURCE) competency $@

$(PORTFOLIO).tex: $(SOURCE) $(INCLUDES) build.el | $(BUILD)
	emacs -Q --batch --script build.el latex $(SOURCE) portfolio $@

$(COMPETENCY).pdf: $(COMPETENCY).tex
	latexmk -xelatex -interaction=nonstopmode -output-directory=$(BUILD) $<

$(PORTFOLIO).pdf: $(PORTFOLIO).tex
	latexmk -xelatex -interaction=nonstopmode -output-directory=$(BUILD) $<

md: $(DETAIL)

$(DETAIL): $(BUILD)/detail.org
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
	pdftotext $(COMPETENCY).pdf $$tmp/competency.txt; \
	pdftotext $(PORTFOLIO).pdf $$tmp/portfolio.txt; \
	targets=$$(find . -type f -not -path './build/*' -not -path './.git/*' \
	  -not -name '$(LEAKWORDS)' -exec grep -Iq . {} \; -print | sort); \
	targets="$$targets $(BUILD)/index.html $(BUILD)/record.html $(DETAIL) \
	  $$tmp/competency.txt $$tmp/portfolio.txt"; \
	hits=0; n=0; \
	while IFS= read -r w; do \
	  case "$$w" in ''|\#*) continue;; esac; \
	  n=$$((n+1)); \
	  found=$$(grep -lF -- "$$w" $$targets 2>/dev/null | tr '\n' ' '); \
	  if [ -n "$$found" ]; then echo "LEAK: a denylisted term appears in: $$found"; hits=1; fi; \
	done < $(LEAKWORDS); \
	rm -rf $$tmp; \
	[ $$hits -eq 0 ] || exit 1; \
	echo "OK: leak gate — $$n terms against $$(echo $$targets | wc -w) files (sources + shipped artifacts)"

check: all leak
	test -s $(BUILD)/index.html
	test -s $(BUILD)/record.html
	test -s $(COMPETENCY).pdf
	test -s $(PORTFOLIO).pdf
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
	test -s $(LLMS)
	pdftotext $(COMPETENCY).pdf - | grep -q '에이전트 플랫폼 운영'
	pdftotext $(PORTFOLIO).pdf - | grep -q '포트폴리오'
# Emphasis must have been *rendered*, not printed. Org marks bold `*so*`; writing Markdown's
# `**so**` in the source is not an error anywhere in the toolchain — it simply sets the
# asterisks in the page, and 64 lines of the two PDFs shipped that way. Korean makes it
# sharper: a closing marker followed immediately by a particle (`*운영*했습니다`) is not
# emphasis to Org or to pandoc either, so it also prints. The extracted text is the witness
# — a submitted PDF has no business containing an asterisk at all.
	! pdftotext $(COMPETENCY).pdf - | grep -q '[*]'
	! pdftotext $(PORTFOLIO).pdf - | grep -q '[*]'
	grep -q '<strong>' $(BUILD)/record.html
# A table wider than the text block does not wrap — it runs off the right edge of the page
# and the reader loses the column. LaTeX says so in the log and nothing else does.
	! grep -q 'Overfull \\hbox' $(BUILD)/KimJunghan_AX_Competency.log
	! grep -q 'Overfull \\hbox' $(BUILD)/KimJunghan_AX_Portfolio.log
	@printf 'OK: one Org source -> landing + record + 2 PDFs + detailed Markdown\n'
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
repro:
	@$(MAKE) --no-print-directory clean >/dev/null
	@$(MAKE) --no-print-directory all >/dev/null 2>&1 || { echo 'repro: first build failed'; exit 1; }
	@a=$$(mktemp -d); b=$$(mktemp -d); \
	 snap() { d=$$1; cp $(BUILD)/index.html $(BUILD)/record.html $(DETAIL) \
	            $(COMPETENCY).pdf $(PORTFOLIO).pdf $$d/; \
	          pdftotext $(COMPETENCY).pdf $$d/competency.txt; \
	          pdftotext $(PORTFOLIO).pdf $$d/portfolio.txt; }; \
	 snap $$a; \
	 $(MAKE) --no-print-directory clean >/dev/null; \
	 $(MAKE) --no-print-directory all >/dev/null 2>&1 || { echo 'repro: second build failed'; exit 1; }; \
	 snap $$b; \
	 fail=0; \
	 for f in index.html record.html $(notdir $(DETAIL)) competency.txt portfolio.txt; do \
	   if cmp -s $$a/$$f $$b/$$f; then echo "  same     $$f"; \
	   else echo "  DIFFERS  $$f"; fail=1; fi; \
	 done; \
	 for f in $(notdir $(COMPETENCY)).pdf $(notdir $(PORTFOLIO)).pdf; do \
	   if cmp -s $$a/$$f $$b/$$f; then echo "  same     $$f (bytes)"; \
	   else echo "  differ   $$f — $$(cmp -l $$a/$$f $$b/$$f | wc -l) of $$(stat -c%s $$a/$$f) bytes (trailer file id; not enforced)"; fi; \
	 done; \
	 rm -rf $$a $$b; \
	 [ $$fail -eq 0 ] || { echo 'DIFFERS: the build did not reproduce'; exit 1; }; \
	 echo 'OK: two clean builds — identical HTML, Markdown, and extracted PDF text'

# The web root is not the build directory. `build/` also holds the .tex, the LaTeX logs, the
# .xdv, and the profile cuts — intermediates that say how the document was made and would be
# served to anyone who guessed the filename. So publishing copies out the six files that are
# meant to be read — the five generated views plus llms.txt — into a directory that holds
# nothing else.
#
# It runs `check` first, and that is the point: the leak gate is what stands between the
# denylist and a public URL. Never wire a web server at `build/`, and never publish by
# copying past this target.
PUBLISH ?= /home/junghan/docker-data/ax

publish: check
	@mkdir -p $(PUBLISH)
	@cp build/index.html build/record.html $(COMPETENCY).pdf $(PORTFOLIO).pdf $(DETAIL) \
	  $(LLMS) $(PUBLISH)/
	@printf 'OK: published 6 files -> $(PUBLISH)\n'
	@ls -1 $(PUBLISH)

clean:
	rm -rf $(BUILD)
