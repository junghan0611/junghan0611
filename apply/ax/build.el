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

(add-to-list 'org-latex-classes
             '("axpaper"
               "\\documentclass{acmart}"
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

(let* ((mode (pop command-line-args-left))
       (source (pop command-line-args-left))
       (profile (pop command-line-args-left))
       (output (pop command-line-args-left)))
  (unless (and (member mode '("cut" "latex")) source profile output)
    (error "usage: build.el cut|latex SOURCE PROFILE OUTPUT"))
  (make-directory (file-name-directory (expand-file-name output)) t)
  (find-file source)
  (let ((org-export-select-tags (list profile))
        (org-export-exclude-tags '("noexport")))
    (pcase mode
      ("cut"
       (org-export-to-file 'axorg output nil nil nil nil
                           '(:with-tags nil)))
      ("latex"
       ;; The source carries an explicit acmart title block. Suppress Org's automatic one.
       ;; The table of contents goes too: a 4-page submission spent its first page on a
       ;; two-line "Contents", and acmart already prints one of its own. The web record
       ;; keeps its TOC — that is pandoc's, and there it earns the space.
       (org-export-to-file 'latex output nil nil nil nil
                           '(:with-title nil :with-author nil :with-date nil
                             :with-tags nil :with-toc nil))))))
