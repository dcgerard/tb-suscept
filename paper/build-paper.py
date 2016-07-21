#!/usr/bin/env python3

import docx
import os
import sys

# https://www.overleaf.com/latex/templates/template-for-submissions-to-scientific-reports/xyrztqvdccns#.V5Drne3L9z1
# http://tug.ctan.org/tex-archive/macros/latex/contrib/nature/naturemag.bst

doc_class = "\documentclass[fleqn,10pt]{wlscirep}\n"

def convert_style_to_macro(style):
    if style == "Title":
        return "title"
    if style == "Author":
        return "author"
    if style == "Abstract":
        return "abstract"
    return None

def write_title(text):
    return "\\title{%s}\n"%(text)

def write_author(text):
    return "\\author{%s}"%(text)

def write_abstract(text):
    return "\\begin{abstract}\n%s\n\\end{abstract}\n"%(text)

def begin_document():
    return "\\begin{document}\n\\flushbottom\n\\maketitle\n\\thispagestyle{empty}\n"

def write_section(text):
    return "\\section*{%s}\n"%(text)

if __name__ == "__main__":
    fname = sys.argv[1]
    assert fname[-4:] == "docx", "Input file is Word document"
    assert os.path.exists(fname), "Input file exists"
    sys.stdout.write(doc_class)
    d = docx.Document(fname)
    for line in d.paragraphs:
        out = line.text
        style = line.style.name
        if style == "Title":
            out = write_title(out)
        elif style == "Author":
            out = write_author(out)
        elif style == "Abstract":
            out = write_abstract(out) + begin_document()
        elif style == "Heading 2":
            out = write_section(out)
        sys.stdout.write(out + "\n")

    sys.stdout.write("\\end{document}\n")