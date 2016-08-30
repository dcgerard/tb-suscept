#!/usr/bin/env python3

import docx
import os
import sys
import pdb

# https://www.overleaf.com/latex/templates/template-for-submissions-to-scientific-reports/xyrztqvdccns#.V5Drne3L9z1
# http://tug.ctan.org/tex-archive/macros/latex/contrib/nature/naturemag.bst

doc_class = "\documentclass[fleqn,10pt]{wlscirep}\n"

# List of packages to be loaded in preamble
packages = ["fixltx2e",
            "epstopdf"] # Convert EPS to PDF

# LaTeX macro for labeling supplementary tables and figures.
# http://bytesizebio.net/2013/03/11/adding-supplementary-tables-and-figures-in-latex/
label_supp = """
\\newcommand{\\beginsupplement}{%
 \\setcounter{table}{0}
 \\renewcommand{\\thetable}{S\\arabic{table}}%
 \\setcounter{figure}{0}
 \\renewcommand{\\thefigure}{S\\arabic{figure}}%
 }

"""

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
    # Format author and affiliations. Example output below:
    #
    # \author[1,*]{Alice Author}
    # \affil[1]{Affiliation, department, city, postcode, country}
    # \affil[*]{corresponding.author@email.example}
    #
    if text == "":
        return text
    # If it starts with a superscript, it is an affiliation
    elif text[:17] == "\\textsuperscript{":
        num, name = text[17:].split("}")
        return "\\affil[%s]{%s}"%(num, name)
    # Otherwise it is the list of authors with their affiliation
    # numbers following their names.
    else:
        entries = text.split("},")
        result = ""
        for e in entries:
            parts = e.split("\\textsuperscript{")
            author = parts[0].lstrip(" ")
            affiliations = "".join([x.rstrip("}") for x in parts[1:]])
            result = result + "\\author[%s]{%s}\n"%(affiliations,
                                                    author)
        return result

def write_abstract(text):
    return "\\begin{abstract}\n%s\n\\end{abstract}\n"%(text)

def begin_document():
    return "\\begin{document}\n\\flushbottom\n\\maketitle\n\\thispagestyle{empty}\n"

def write_section(text):
    return "\\section*{%s}\n"%(text)

def write_subsection(text):
    return "\\subsection*{%s}\n"%(text)

def convert_run(run):
    result = run.text
    if run.font.subscript:
        result = "\\textsubscript{" + result + "}"
    elif run.font.superscript:
        result = "\\textsuperscript{" + result + "}"
    if run.italic:
        result = "\emph{" + result + "}"
    if run.bold:
        result = "\\textbf{" + result + "}"
    if run.underline:
        result = "\\underline{" + result + "}"
    return result

def use_packages(packages):
    # Packages is a list of strings.
    # Add to preamble with \usepackage{}
    result = ""
    for p in packages:
        result = result + "\\usepackage{" + p + "}\n"
    return result

if __name__ == "__main__":
    fname = sys.argv[1]
    assert fname[-4:] == "docx", "Input file is Word document"
    assert os.path.exists(fname), "Input file exists"
    sys.stdout.write(doc_class)
    sys.stdout.write(use_packages(packages))
    sys.stdout.write(label_supp)
    d = docx.Document(fname)
    for line in d.paragraphs:
        out = ""
        for run in line.runs:
            out = out + convert_run(run)
        style = line.style.name
        if style == "Title":
            out = write_title(out)
        elif style == "Author":
            out = write_author(out)
        elif style == "Abstract":
            out = write_abstract(out) + begin_document()
        elif style == "Heading 1":
            out = write_section(out)
            if "Supplementary Information" in out:
                out = "\\clearpage\\newpage\n\\beginsupplement\n" + out
        elif style == "Heading 2":
            out = write_subsection(out)
        sys.stdout.write(out + "\n")

    sys.stdout.write("\\end{document}\n")
