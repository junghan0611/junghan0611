;; build.el — profile cuts and XeLaTeX source from one authored Org file
;;
;; The PDF class wiring descends from memex-kb scripts/paper_build.el, already proven by
;; jacobian-lens/survey. This file adds only the dossier's profile selection and Korean
;; XeLaTeX path; it does not parse or transform document content itself.
;;
;; Usage:
;;   emacs -Q --batch --script build.el cut  ax.org landing    build/landing.org
;;   emacs -Q --batch --script build.el latex ax.org competency build/competency.tex

(require 'seq)
(require 'org)
(require 'ox-org)
(require 'ox-latex)

(setq debug-on-error nil
      backtrace-on-error-noninteractive nil
      org-export-with-broken-links t)

;; acmart loads newtx and conflicts with Org's default amssymb package.
(setq org-latex-default-packages-alist
      (seq-remove (lambda (pkg) (equal (cadr pkg) "amssymb"))
                  org-latex-default-packages-alist))

;; acmart pins `letterpaper' inside the class because ACM prints on US letter, and it does
;; not accept `a4paper' as a class option. geometry is already loaded by then, so
;; \usepackage[a4paper]{geometry} dies of an option clash. Re-calling \geometry is the only
;; door left, and it has to be part of the class definition — the same wiring the private
;; dossier proved, kept identical here on purpose so the two surfaces do not drift.
;;
;; `twoside=false' rather than `oneside': manuscript is twoside, so odd and even pages
;; disagree by 37pt (1.3cm) of margin. That is right for a bound page turned by hand and
;; wrong for a document read by scrolling — there it only ever looks like the text block
;; sliding left and right. `oneside' is a class option, not a geometry key (xkeyval:
;; `oneside' undefined in families `Gm'); the geometry spelling of the same intent is the
;; twoside boolean.
(defconst ax/geometry
  "\\geometry{a4paper,twoside=false,left=3cm,right=3cm,top=2.8cm,bottom=2.8cm}")

(add-to-list 'org-latex-classes
             `("axpaper"
               ,(concat "\\documentclass{acmart}\n" ax/geometry)
               ("\\section{%s}" . "\\section*{%s}")
               ("\\subsection{%s}" . "\\subsection*{%s}")
               ("\\subsubsection{%s}" . "\\subsubsection*{%s}")
               ("\\paragraph{%s}" . "\\paragraph*{%s}")
               ("\\subparagraph{%s}" . "\\subparagraph*{%s}")))

;; `ox-org' keeps an export block only when its type is ORG and silently drops every other
;; one, which is right for a rendering backend and wrong here: the cut is *transport* to
;; pandoc, not an output format. The HTML evidence mount vanished between ax.org and
;; build/record.org, and record.html shipped the heading with an empty body under it. A
;; raw block must survive the cut verbatim; pandoc is the one that decides what to do with
;; it. `make check' greps record.html for the mount, so this stays honest.
(defun ax/keep-export-block (export-block _contents _info)
  (let ((type (org-element-property :type export-block))
        (value (org-element-property :value export-block)))
    (format "#+begin_export %s\n%s#+end_export"
            (downcase type)
            (org-remove-indentation value))))

(org-export-define-derived-backend 'axorg 'org
  :translate-alist '((export-block . ax/keep-export-block)))


;;; Depth
;;
;; This is one document read at four depths, not five documents. d0 is the claim, d1 the
;; shape of the evidence, d2 the events and numbers, d3 the ledger. Every view is a slice
;; of the same source, so the PDFs cannot drift from the web record — there is nothing to
;; keep in sync.
;;
;; The cut runs on `org-export-exclude-tags', not `org-export-select-tags'. Select was
;; what the profile build used and it is the wrong tool here: selecting a heading pulls in
;; *all* of its descendants, so choosing d1 would drag the d3 ledger up with it. Exclude
;; drops whole subtrees and — this is the part that makes it work — org tags are inherited,
;; so a d3 heading nested under d2 is excluded at depth 1 by its own tag and at depth 0 by
;; its parent's. Depth N keeps a heading when neither it nor any ancestor is deeper than N.
;;
;; The inheritance that makes this cheap also makes one authoring mistake silent: a d1
;; heading placed under a d2 parent inherits d2 and vanishes from the d1 view with no
;; error anywhere. Nothing downstream would notice — a missing section looks exactly like
;; a section that was never written. So depth must not decrease as the tree descends, and
;; `ax/validate-depths' refuses to build when it does.

(defconst ax/depths '("d0" "d1" "d2" "d3")
  "Depth tags, shallowest first. Index is the depth.")

(defun ax/depth-of (tags)
  "The depth TAGS declare, or nil. Signals when they declare more than one."
  (let ((found (seq-filter (lambda (d) (member d tags)) ax/depths)))
    (when (cdr found)
      (error "A heading carries %d depth tags (%s); it must carry exactly one"
             (length found) (string-join found " ")))
    (when found (seq-position ax/depths (car found)))))

(defun ax/exclude-tags (max-depth)
  "Tags whose subtrees do not belong in a document cut at MAX-DEPTH."
  (cons "noexport" (seq-drop ax/depths (1+ max-depth))))

(defun ax/scan ()
  "Every heading as (LINE LEVEL DEPTH INHERITED-DEPTH CUSTOM-ID TITLE).
INHERITED-DEPTH is the deepest depth any ancestor declares."
  (let (rows (stack '()))
    (org-map-entries
     (lambda ()
       (let* ((level (org-current-level))
              (local (ax/depth-of (org-get-tags nil t)))
              (tags (org-get-tags)))
         ;; Ancestors still on the stack are the ones shallower than this heading.
         (setq stack (seq-filter (lambda (e) (< (car e) level)) stack))
         (let ((inherited (when stack (apply #'max (mapcar #'cdr stack)))))
           (unless (member "noexport" tags)
             (push (list (line-number-at-pos)
                         level local inherited
                         (org-entry-get nil "CUSTOM_ID")
                         (org-get-heading t t t t))
                   rows))
           (push (cons level (or local inherited 0)) stack))))
     nil 'file)
    (nreverse rows)))

(defun ax/validate-depths (rows)
  "Refuse ROWS that would silently drop a heading from a cut."
  (let (problems)
    (dolist (row rows)
      (seq-let (line level depth inherited _id title) row
        (cond
         ((null depth)
          (push (format "  line %d: %s%s — carries no depth tag"
                        line (make-string level ?*) (or title ""))
                problems))
         ((and inherited (< depth inherited))
          (push (format "  line %d: %s%s — d%d under a d%d ancestor; it would vanish \
from the d%d view without any error"
                        line (make-string level ?*) (or title "")
                        depth inherited depth)
                problems)))))
    (when problems
      (error "Depth is not monotonic down the tree:\n%s"
             (string-join (nreverse problems) "\n")))))

(defun ax/manifest (rows output)
  "Write ROWS as an ordered depth array for the web depth dial.

Ordered, not keyed by CUSTOM_ID: only 7 of the source's 42 headings carry one, so a
keyed map would have silently described a sixth of the document and the dial would have
left the rest permanently visible. The web record is the depth-3 cut, which keeps every
heading, and both this scan and pandoc's <section> emission follow document order — so
the Nth section is the Nth row, and `make check' asserts the two counts agree rather
than trusting that they do."
  (with-temp-file output
    (insert "[\n")
    (let ((last (car (last rows))))
      (dolist (row rows)
        (seq-let (_line level depth inherited id title) row
          (insert (format "  {\"depth\": %d, \"level\": %d, \"id\": %s, \"title\": %S}%s\n"
                          (or depth inherited 0)
                          level
                          (if id (format "%S" id) "null")
                          (or title "")
                          (if (eq row last) "" ","))))))
    (insert "]\n")))


(let* ((mode (pop command-line-args-left))
       (source (pop command-line-args-left))
       (depth (pop command-line-args-left))
       (output (pop command-line-args-left)))
  (unless (and (member mode '("cut" "latex" "manifest")) source depth output)
    (error "usage: build.el cut|latex|manifest SOURCE DEPTH OUTPUT"))
  (make-directory (file-name-directory (expand-file-name output)) t)
  (find-file source)
  (let ((rows (ax/scan))
        (max-depth (string-to-number depth)))
    (ax/validate-depths rows)
    (if (equal mode "manifest")
        (ax/manifest rows output)
      (let ((org-export-select-tags nil)
            (org-export-exclude-tags (ax/exclude-tags max-depth)))
        (pcase mode
          ("cut"
           (org-export-to-file 'axorg output nil nil nil nil
                               '(:with-tags nil)))
          ("latex"
           ;; The source carries an explicit acmart title block. Suppress Org's automatic
           ;; one. The table of contents goes too: a 4-page submission spent its first page
           ;; on a two-line "Contents", and acmart already prints one of its own. The web
           ;; record keeps its TOC — that is pandoc's, and there it earns the space.
           (org-export-to-file 'latex output nil nil nil nil
                               '(:with-title nil :with-author nil :with-date nil
                                 :with-tags nil :with-toc nil))))))))
