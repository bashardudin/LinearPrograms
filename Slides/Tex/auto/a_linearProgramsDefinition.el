(TeX-add-style-hook
 "a_linearProgramsDefinition"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("beamer" "32pt" "aspectratio=169")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8")))
   (TeX-run-style-hooks
    "latex2e"
    "beamer"
    "beamer10"
    "inputenc")
   (LaTeX-add-labels
    "eq:positivityCondition")))

