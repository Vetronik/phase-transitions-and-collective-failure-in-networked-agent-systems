"""Convert the LaTeX manuscript into a readable, styled DOCX.

This is a deterministic converter for this repository's article. It preserves
headings, equations as readable text, figures, tables, inline author-year
citations, and the bibliography.
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "paper" / "main.tex"
OUT = ROOT / "paper" / "main.docx"

ACCENT = "0F766E"
INK = "1F2933"
MUTED = "52606D"
LIGHT = "E6F4F1"

CITATION_LABELS = {
    "degroot1974": "DeGroot, 1974",
    "friedkin_johnsen1990": "Friedkin and Johnsen, 1990",
    "bikhchandani1992": "Bikhchandani et al., 1992",
    "golub_jackson2010": "Golub and Jackson, 2010",
    "lorenz2011": "Lorenz et al., 2011",
    "becker2017": "Becker et al., 2017",
    "jayles2017": "Jayles et al., 2017",
    "binder1981": "Binder, 1981",
    "hong2007": "Hong et al., 2007",
    "physics_of_agents_2026": "El et al., 2026",
    "interaction_tax_2026": "Ann et al., 2026",
    "du_et_al_2023": "Du et al., 2023",
}

REF_LABELS = {
    "eq:update": "Eq. (1)",
    "eq:stationary": "Eq. (2)",
    "eq:j0baseline": "Eq. (3)",
    "eq:oracle": "Eq. (4)",
    "eq:neff": "Eq. (5)",
    "tab:design": "Table 1",
    "tab:mainresults": "Table 2",
    "tab:primaryuncertainty": "Table 3",
    "tab:robustness": "Table 4",
    "tab:covariance": "Table 5",
    "tab:scaling": "Table 6",
    "tab:critical": "Table 7",
    "tab:confirmation": "Table 1",
    "fig:independent": "Figure 1",
    "fig:correlated": "Figure 2",
    "fig:scalingcorrelated": "Figure 3",
    "fig:scalingindependent": "Figure 4",
}


def _extract_braced(text: str, open_index: int) -> tuple[str, int]:
    """Return a balanced braced block and the index after its closing brace."""
    depth = 0
    for i in range(open_index, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[open_index + 1:i], i + 1
    return text[open_index + 1:], len(text)


def extract_command(text: str, command: str) -> str:
    marker = "\\" + command + "{"
    start = text.find(marker)
    if start < 0:
        return ""
    content, _ = _extract_braced(text, start + len(marker) - 1)
    return content


def balanced_command(text: str, command: str) -> str:
    """Remove a simple LaTeX command while retaining its braced argument."""
    pattern = "\\" + command + "{"
    while pattern in text:
        start = text.index(pattern)
        content, end = _extract_braced(text, start + len(pattern) - 1)
        text = text[:start] + content + text[end:]
    return text


def math_to_text(text: str) -> str:
    """Turn the small mathematical vocabulary used by the article into text."""
    replacements = {
        "\\mathrm": "", "\\mathbf": "", "\\mathbb": "", "\\operatorname": "",
        "\\Pr": "P", "\\propto": "\u221d", "\\sum": "\u03a3", "\\in": "\u2208",
        "\\mid": "|", "\\geq": "\u2265", "\\leq": "\u2264", "\\ne": "\u2260",
        "\\approx": "\u2248", "\\infty": "\u221e", "\\sigma": "\u03c3",
        "\\pi": "\u03c0", "\\rho": "\u03c1", "\\bar": "", "\\left": "",
        "\\right": "", "\\!": "", "\\,": " ", "\\quad": " ",
        "\\to": "\u2192", "\\gets": "\u2190", "\\times": "\u00d7",
        "\\{": "{", "\\}": "}", "&": " ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"(\1)/(\2)", text)
    text = re.sub(r"\^\{([^}]+)\}", r"^\1", text)
    text = re.sub(r"_\{([^}]+)\}", r"_\1", text)
    text = text.replace("\\\\", "; ")
    text = re.sub(r"\\[a-zA-Z]+", "", text)
    text = text.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", text).strip()


def latex_to_text(text: str) -> str:
    text = text.replace("~", " ").replace("---", "\u2014").replace("--", "\u2013")
    text = text.replace("\\%", "%").replace("\\&", "&").replace("\\_", "_")
    text = text.replace("{\\'o}", "ó").replace("{\\'e}", "é").replace("{\\'e}", "é")
    text = text.replace("\\noindent", " ")
    text = re.sub(r"\\vspace\{[^{}]*\}", " ", text)
    text = re.sub(r"\\\\(?:\[[^\]]*\])?", " ", text)
    for command in ["texttt", "textit", "emph", "textbf", "textrm", "mathrm", "mathbf"]:
        text = balanced_command(text, command)
    text = re.sub(r"\\citep?\{([^}]+)\}", lambda m: "(" + "; ".join(CITATION_LABELS.get(k.strip(), k.strip()) for k in m.group(1).split(",")) + ")", text)
    def replace_labeled_phrase(match: re.Match[str]) -> str:
        prefix = match.group(1)
        label = REF_LABELS.get(match.group(2), match.group(2))
        if prefix.lower() == "equation" and label.startswith("Eq. "):
            return f"{prefix} {label[4:]}"
        if prefix.lower() in {"table", "figure"} and label.lower().startswith(prefix.lower() + " "):
            return label
        return f"{prefix} {label}"
    text = re.sub(r"\b(Table|Figure|Equation|equation)\s+\\ref\{([^}]+)\}", replace_labeled_phrase, text)
    text = re.sub(r"\\ref\{([^}]+)\}", lambda m: REF_LABELS.get(m.group(1), m.group(1)), text)
    text = re.sub(r"\\\[(.*?)\\\]", lambda m: math_to_text(m.group(1)), text, flags=re.S)
    text = re.sub(r"\$([^$]+)\$", lambda m: math_to_text(m.group(1)), text)
    text = re.sub(r"\\\((.*?)\\\)", lambda m: math_to_text(m.group(1)), text)
    text = re.sub(r"\\[a-zA-Z]+\*?", "", text)
    text = text.replace("\\\\", " ")
    text = text.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", text).strip()


def _bib_entries(raw: str) -> list[tuple[str, str]]:
    entries = []
    pos = 0
    while True:
        at = raw.find("@", pos)
        if at < 0:
            break
        brace = raw.find("{", at)
        comma = raw.find(",", brace)
        if brace < 0 or comma < 0:
            break
        key = raw[brace + 1:comma].strip()
        body, end = _extract_braced(raw, brace)
        entries.append((key, body[body.find(",") + 1:] if "," in body else ""))
        pos = end
    return entries


def _bib_fields(body: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    i = 0
    while i < len(body):
        match = re.search(r"([A-Za-z][A-Za-z0-9_]*)\s*=\s*", body[i:])
        if not match:
            break
        name = match.group(1).lower()
        start = i + match.end()
        if start < len(body) and body[start] == "{":
            value, end = _extract_braced(body, start)
        else:
            end = body.find(",", start)
            if end < 0:
                end = len(body)
            value = body[start:end].strip()
        fields[name] = value.strip().strip('"')
        i = end + 1
    return fields


def parse_bibliography(path: Path) -> list[str]:
    result = []
    for _, body in _bib_entries(path.read_text(encoding="utf-8")):
        fields = _bib_fields(body)
        authors = latex_to_text(fields.get("author", "")).replace(" and ", "; ")
        title = latex_to_text(fields.get("title", ""))
        venue = latex_to_text(fields.get("journal", ""))
        if not venue and fields.get("eprint"):
            venue = "arXiv preprint arXiv:" + fields["eprint"]
        year = fields.get("year", "")
        volume = fields.get("volume", "")
        number = fields.get("number", "")
        pages = fields.get("pages", "").replace("--", "–")
        journal_detail = venue
        if volume:
            journal_detail += f", {volume}"
            if number:
                journal_detail += f"({number})"
        if pages:
            journal_detail += f", {pages}"
        line = f"{authors}. {title}. {journal_detail} ({year})."
        if fields.get("doi"):
            line += f" https://doi.org/{fields['doi']}."
        result.append(line)
    return result


def set_cell_shading(cell, fill: str):
    properties = cell._tc.get_or_add_tcPr()
    shading = properties.find(qn("w:shd"))
    if shading is None:
        shading = OxmlElement("w:shd")
        properties.append(shading)
    shading.set(qn("w:fill"), fill)


def add_table(doc: Document, lines: list[str], table_number: int) -> int:
    caption = ""
    rows: list[list[str]] = []
    in_tabular = False
    for raw in lines:
        line = raw.strip()
        if line.startswith("\\caption"):
            caption = latex_to_text(line)
        if line.startswith("\\begin{tabular"):
            in_tabular = True
            continue
        if line.startswith("\\end{tabular"):
            in_tabular = False
            continue
        if not in_tabular or line in {r"\toprule", r"\midrule", r"\bottomrule"}:
            continue
        line = line.split("\\\\", 1)[0].strip()
        if line:
            rows.append([latex_to_text(cell.strip()) for cell in line.split("&")])
    if caption:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(f"Table {table_number}. {caption}")
        run.bold = True
        run.font.color.rgb = RGBColor.from_string(ACCENT)
    if rows:
        table = doc.add_table(rows=len(rows), cols=len(rows[0]))
        table.autofit = True
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                cell = table.cell(r, c)
                cell.text = value
                cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                for paragraph in cell.paragraphs:
                    paragraph.paragraph_format.space_after = Pt(0)
                    if r == 0:
                        for run in paragraph.runs:
                            run.bold = True
                            run.font.color.rgb = RGBColor(255, 255, 255)
                if r == 0:
                    set_cell_shading(cell, ACCENT)
                elif r % 2 == 0:
                    set_cell_shading(cell, LIGHT)
    return table_number + 1


def add_figure(doc: Document, image: Path, caption: str, number: int):
    if image.exists():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(image), width=Inches(6.35))
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(f"Figure {number}. {caption}")
    run.italic = True
    run.font.color.rgb = RGBColor.from_string(MUTED)


def convert() -> Path:
    source = TEX.read_text(encoding="utf-8")
    body = source.split(r"\begin{document}", 1)[1].split(r"\end{document}", 1)[0]
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.78)
    section.bottom_margin = Inches(0.72)
    section.left_margin = Inches(0.82)
    section.right_margin = Inches(0.82)
    section.different_first_page_header_footer = True
    section.first_page_header.paragraphs[0].text = ""
    section.first_page_footer.paragraphs[0].text = ""

    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"
    normal.font.size = Pt(10.2)
    normal.font.color.rgb = RGBColor.from_string(INK)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.12
    for style_name, size, color in [("Title", 20, INK), ("Heading 1", 14, ACCENT), ("Heading 2", 11.5, INK)]:
        style = doc.styles[style_name]
        style.font.name = "Aptos Display" if style_name != "Title" else "Aptos Display"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(color)

    header = section.header.paragraphs[0]
    header.text = "COMMUNICATION, CORRELATION, AND COLLECTIVE FAILURE                                      VERONIKA LORAN"
    header.style = doc.styles["Header"]
    for run in header.runs:
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor.from_string(MUTED)
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run("Research manuscript  •  ")
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    footer._p.append(field)

    title = extract_command(source, "title") or "Manuscript"
    author = extract_command(source, "author")
    date = extract_command(source, "date")
    p = doc.add_paragraph(style="Title")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(latex_to_text(title))
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(latex_to_text(author))
    run.italic = True
    run.font.color.rgb = RGBColor.from_string(MUTED)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(latex_to_text(date))
    run.italic = True
    run.font.color.rgb = RGBColor.from_string(MUTED)
    doc.add_page_break()
    p = doc.add_paragraph(style="Title")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("Inhaltsangabe / Table of Contents")
    toc_entries = []
    for raw in body.splitlines():
        match = re.match(r"\\(section|subsection)\*?\{(.*)\}", raw.strip())
        if match:
            toc_entries.append((match.group(1), latex_to_text(match.group(2))))
    for kind, entry in toc_entries:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.22 if kind == "subsection" else 0)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(entry)
        run.font.size = Pt(10 if kind == "section" else 9.2)
        if kind == "section":
            run.bold = True
            run.font.color.rgb = RGBColor.from_string(ACCENT)
        else:
            run.font.color.rgb = RGBColor.from_string(MUTED)
    doc.add_page_break()

    lines = body.splitlines()
    i = 0
    in_abstract = False
    in_titlepage = False
    figure_number = 1
    table_number = 1
    while i < len(lines):
        line = lines[i].strip()
        if line == r"\begin{titlepage}":
            in_titlepage = True
            i += 1
            continue
        if in_titlepage:
            if line == r"\end{titlepage}":
                in_titlepage = False
            i += 1
            continue
        if not line or line.startswith("%") or line in {r"\maketitle", r"\thispagestyle{plain}", r"\tableofcontents", r"\clearpage", r"\newpage", r"\appendix", r"\begin{center}", r"\end{center}", r"\begin{minipage}{0.82\textwidth}", r"\end{minipage}", r"\vfill"} or line.startswith((r"\vspace", r"\pagenumbering", r"\setcounter", r"\thispagestyle", r"\color", r"\rule")):
            i += 1
            continue
        if line == r"\begin{abstract}":
            in_abstract = True
            doc.add_heading("Abstract", level=1)
            i += 1
            continue
        if line == r"\end{abstract}":
            in_abstract = False
            i += 1
            continue
        heading = re.match(r"\\(section|subsection|subsubsection)\*?\{(.*)\}", line)
        if heading:
            level = {"section": 1, "subsection": 2, "subsubsection": 3}[heading.group(1)]
            doc.add_heading(latex_to_text(heading.group(2)), level=level)
            i += 1
            continue
        if line == r"\begin{table}[t]" or line.startswith(r"\begin{table}"):
            block = []
            i += 1
            while i < len(lines) and lines[i].strip() != r"\end{table}":
                block.append(lines[i])
                i += 1
            table_number = add_table(doc, block, table_number)
            i += 1
            continue
        if line == r"\begin{figure}[t]" or line.startswith(r"\begin{figure}"):
            image = None
            caption = ""
            i += 1
            while i < len(lines) and lines[i].strip() != r"\end{figure}":
                candidate = lines[i].strip()
                match = re.search(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", candidate)
                if match:
                    image = (ROOT / "paper" / match.group(1)).resolve()
                if candidate.startswith(r"\caption"):
                    caption = latex_to_text(candidate)
                i += 1
            add_figure(doc, image, caption.replace("Caption", "").strip(), figure_number)
            figure_number += 1
            i += 1
            continue
        if line.startswith(r"\begin{equation") or line == r"\[":
            equation = []
            closing = r"\end{equation}"
            if line == r"\[":
                closing = r"\]"
            i += 1
            while i < len(lines) and not lines[i].strip().startswith(closing):
                if not lines[i].strip().startswith(r"\label"):
                    equation.append(lines[i].strip())
                i += 1
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(math_to_text(" ".join(equation)))
            run.font.name = "Cambria Math"
            run.italic = True
            i += 1
            continue
        if line in {r"\begin{itemize}", r"\end{itemize}", r"\begin{enumerate}", r"\end{enumerate}", r"\toprule", r"\midrule", r"\bottomrule"} or line.startswith(r"\label") or line.startswith(r"\bibliograph"):
            i += 1
            continue
        if line.startswith(r"\item"):
            add_body_paragraph(doc, line[len(r"\item"):].strip(), style="List Bullet", italic=in_abstract)
            i += 1
            continue
        paragraph = line
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"\\(section|subsection|subsubsection|begin|end|title|author|date|item)", lines[i].strip()):
            nxt = lines[i].strip()
            if nxt.startswith(r"\label") or nxt.startswith(r"\bibliograph") or nxt in {r"\toprule", r"\midrule", r"\bottomrule"}:
                i += 1
                continue
            paragraph += " " + nxt
            i += 1
        add_body_paragraph(doc, paragraph, italic=in_abstract)

    doc.add_heading("References", level=1)
    for reference in parse_bibliography(ROOT / "paper" / "references.bib"):
        p = doc.add_paragraph(reference)
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.paragraph_format.space_after = Pt(4)
        for run in p.runs:
            run.font.size = Pt(9)
    doc.core_properties.title = latex_to_text(title)
    doc.core_properties.author = latex_to_text(author)
    doc.save(OUT)
    return OUT


def add_body_paragraph(doc: Document, text: str, *, style: str | None = None, italic: bool = False):
    text = latex_to_text(text)
    if not text:
        return
    p = doc.add_paragraph(style=style)
    run = p.add_run(text)
    run.italic = italic


if __name__ == "__main__":
    print(convert())
