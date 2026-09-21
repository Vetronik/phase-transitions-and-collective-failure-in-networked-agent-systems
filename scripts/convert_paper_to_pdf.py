"""Build a polished PDF from the repository's LaTeX manuscript.

The workspace does not provide a TeX engine, so this deterministic ReportLab
fallback preserves the article structure, equations as readable text, tables,
figures, author-year citations, and references. If a TeX engine is installed,
the LaTeX source remains the canonical typesetting route.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from convert_paper_to_word import (
    REF_LABELS,
    ROOT,
    TEX,
    extract_command,
    latex_to_text,
    math_to_text,
    parse_bibliography,
)


OUT = ROOT / "paper" / "main.pdf"
ACCENT = HexColor("#0F766E")
INK = HexColor("#1F2933")
MUTED = HexColor("#52606D")
LIGHT = HexColor("#E6F4F1")


def register_fonts():
    regular = Path(r"C:\Windows\Fonts\arial.ttf")
    bold = Path(r"C:\Windows\Fonts\arialbd.ttf")
    italic = Path(r"C:\Windows\Fonts\ariali.ttf")
    if regular.exists() and bold.exists() and italic.exists():
        pdfmetrics.registerFont(TTFont("Article", str(regular)))
        pdfmetrics.registerFont(TTFont("Article-Bold", str(bold)))
        pdfmetrics.registerFont(TTFont("Article-Italic", str(italic)))
        return "Article", "Article-Bold", "Article-Italic"
    return "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"


def para_text(text: str) -> str:
    return html.escape(latex_to_text(text), quote=False)


def parse_table(block: list[str], regular: str, bold: str, table_number: int):
    caption = ""
    rows: list[list[str]] = []
    in_tabular = False
    for raw in block:
        line = raw.strip()
        if line.startswith(r"\caption"):
            caption = latex_to_text(line)
        if line.startswith(r"\begin{tabular"):
            in_tabular = True
            continue
        if line.startswith(r"\end{tabular"):
            in_tabular = False
            continue
        if not in_tabular or line in {r"\toprule", r"\midrule", r"\bottomrule"}:
            continue
        line = line.split(r"\\", 1)[0].strip()
        if line:
            rows.append([latex_to_text(cell.strip()) for cell in line.split("&")])
    flowables = []
    if caption:
        flowables.append(Paragraph(f"<font color='{ACCENT.hexval()}'><b>Table {table_number}.</b></font> {html.escape(caption)}", ParagraphStyle("TableCaption", fontName=regular, fontSize=8.8, leading=11, spaceBefore=4, spaceAfter=4)))
    if rows:
        cell_style = ParagraphStyle("TableCell", fontName=regular, fontSize=7.3, leading=8.5, textColor=INK, alignment=TA_LEFT)
        header_style = ParagraphStyle("TableHeader", fontName=bold, fontSize=7.3, leading=8.5, textColor=colors.white, alignment=TA_LEFT)
        wrapped_rows = []
        for row_index, row in enumerate(rows):
            style = header_style if row_index == 0 else cell_style
            wrapped_rows.append([Paragraph(html.escape(value), style) for value in row])
        width_sets = {
            5: [1.15, 0.72, 0.88, 0.88, 2.67],
            6: [1.55, 0.72, 0.85, 0.85, 0.85, 1.05],
            7: [1.52, 0.48, 0.48, 0.78, 0.78, 0.82, 1.1],
        }
        widths = width_sets.get(len(rows[0]))
        if table_number == 3 and len(rows[0]) == 5:
            widths = [1.65, 0.45, 1.55, 1.95, 0.75]
        if widths is None:
            widths = [6.35 / len(rows[0])] * len(rows[0])
        table = Table(wrapped_rows, colWidths=[width * inch for width in widths], repeatRows=1, hAlign="LEFT")
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), bold),
            ("FONTNAME", (0, 1), (-1, -1), regular),
            ("FONTSIZE", (0, 0), (-1, -1), 8.2),
            ("LEADING", (0, 0), (-1, -1), 10),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
            ("GRID", (0, 0), (-1, -1), 0.25, HexColor("#B8C6C4")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        flowables.append(table)
        flowables.append(Spacer(1, 6))
    return flowables


def build():
    regular, bold, italic = register_fonts()
    source = TEX.read_text(encoding="utf-8")
    body = source.split(r"\begin{document}", 1)[1].split(r"\end{document}", 1)[0]
    title = extract_command(source, "title") or "Manuscript"
    author = extract_command(source, "author")
    date = extract_command(source, "date")

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("ArticleBody", parent=styles["BodyText"], fontName=regular, fontSize=9.55, leading=13.25, alignment=TA_JUSTIFY, textColor=INK, spaceAfter=6.5))
    styles.add(ParagraphStyle("ArticleTitle", parent=styles["Title"], fontName=bold, fontSize=19.5, leading=23, alignment=TA_CENTER, textColor=INK, spaceAfter=8))
    styles.add(ParagraphStyle("ArticleAuthor", parent=styles["Normal"], fontName=italic, fontSize=10.2, leading=13, alignment=TA_CENTER, textColor=MUTED, spaceAfter=3))
    styles.add(ParagraphStyle("ArticleH1", parent=styles["Heading1"], fontName=bold, fontSize=13.3, leading=16, textColor=ACCENT, spaceBefore=10, spaceAfter=5))
    styles.add(ParagraphStyle("ArticleH2", parent=styles["Heading2"], fontName=bold, fontSize=10.8, leading=13.4, textColor=INK, spaceBefore=8, spaceAfter=3))
    styles.add(ParagraphStyle("ArticleEquation", parent=styles["Normal"], fontName=italic, fontSize=9.4, leading=12.5, alignment=TA_CENTER, textColor=INK, spaceBefore=3, spaceAfter=6))
    styles.add(ParagraphStyle("ArticleCaption", parent=styles["Normal"], fontName=italic, fontSize=8.5, leading=10.7, alignment=TA_LEFT, textColor=MUTED, spaceBefore=3, spaceAfter=8))
    styles.add(ParagraphStyle("ArticleRef", parent=styles["Normal"], fontName=regular, fontSize=8.55, leading=10.8, alignment=TA_LEFT, textColor=INK, leftIndent=13, firstLineIndent=-13, spaceAfter=3.5))
    styles.add(ParagraphStyle("ArticleBullet", parent=styles["ArticleBody"], leftIndent=13, firstLineIndent=-8, bulletIndent=0, alignment=TA_LEFT, spaceAfter=4))
    styles.add(ParagraphStyle("ArticleKeyword", parent=styles["ArticleBody"], fontName=regular, textColor=MUTED, alignment=TA_LEFT, spaceBefore=2, spaceAfter=8))
    styles.add(ParagraphStyle("CoverTitle", parent=styles["Title"], fontName=bold, fontSize=22, leading=27, alignment=TA_CENTER, textColor=INK, spaceAfter=8))
    styles.add(ParagraphStyle("CoverSubtitle", parent=styles["Normal"], fontName=regular, fontSize=13.2, leading=17, alignment=TA_CENTER, textColor=INK, spaceAfter=13))
    styles.add(ParagraphStyle("CoverMeta", parent=styles["Normal"], fontName=regular, fontSize=10, leading=14, alignment=TA_LEFT, textColor=INK, spaceAfter=2))
    styles.add(ParagraphStyle("CoverNote", parent=styles["Normal"], fontName=italic, fontSize=9.2, leading=12.5, alignment=TA_JUSTIFY, textColor=MUTED, spaceBefore=12))
    styles.add(ParagraphStyle("TocEntry", parent=styles["Normal"], fontName=regular, fontSize=9.2, leading=11, textColor=INK, leftIndent=0, spaceAfter=1.5))
    styles.add(ParagraphStyle("TocSubentry", parent=styles["Normal"], fontName=regular, fontSize=8.5, leading=9.8, textColor=MUTED, leftIndent=16, spaceAfter=1))

    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4, rightMargin=0.78 * inch, leftMargin=0.78 * inch,
        topMargin=0.72 * inch, bottomMargin=0.68 * inch,
        title=latex_to_text(title), author=latex_to_text(author),
    )
    cover_title = latex_to_text(title).replace("; ", " ")
    cover_parts = [part.strip() for part in re.split(r"\\\\(?:\[[^]]*\])?", title) if part.strip()]
    if len(cover_parts) >= 2:
        cover_title = latex_to_text(cover_parts[0])
        cover_subtitle = latex_to_text(cover_parts[1])
    else:
        cover_subtitle = "Correlated Collective Failure in Networked Binary Agents"
    toc_entries = []
    for raw in body.splitlines():
        match = re.match(r"\\(section|subsection)\*?\{(.*)\}", raw.strip())
        if match:
            toc_entries.append((match.group(1), latex_to_text(match.group(2))))
    story = [
        HRFlowable(width="100%", thickness=1.2, color=ACCENT, spaceAfter=28),
        Spacer(1, 18),
        Paragraph(para_text(cover_title), styles["CoverTitle"]),
        Paragraph(para_text(cover_subtitle), styles["CoverSubtitle"]),
        Spacer(1, 105),
        Table([
            [Paragraph("<b>Author</b>", styles["CoverMeta"]), Paragraph(para_text(author), styles["CoverMeta"])],
            [Paragraph("<b>Manuscript type</b>", styles["CoverMeta"]), Paragraph("Full research manuscript / computational study", styles["CoverMeta"])],
            [Paragraph("<b>Version</b>", styles["CoverMeta"]), Paragraph("Results-aware preprint, version 1.1", styles["CoverMeta"])],
            [Paragraph("<b>Date</b>", styles["CoverMeta"]), Paragraph(para_text(date), styles["CoverMeta"])],
        ], colWidths=[1.35 * inch, 4.95 * inch], style=TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ])),
        Spacer(1, 90),
        Paragraph(para_text("This manuscript reports a reproducible stochastic-agent study. Its principal contribution is a controlled account of how shared input errors and repeated communication alter collective performance. The finite-horizon mechanism is supported by the executed evidence package; a thermodynamic phase transition is not claimed."), styles["CoverNote"]),
        Spacer(1, 20),
        HRFlowable(width="100%", thickness=1.2, color=ACCENT, spaceAfter=10),
        PageBreak(),
        Paragraph("Inhaltsangabe / Table of Contents", styles["ArticleTitle"]),
        Spacer(1, 8),
    ]
    for kind, entry in toc_entries:
        story.append(Paragraph(para_text(entry), styles["TocEntry" if kind == "section" else "TocSubentry"]))
    story.append(PageBreak())

    lines = body.splitlines()
    i = 0
    in_abstract = False
    figure_number = 1
    table_number = 1
    in_titlepage = False
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
            story.append(Paragraph("Abstract", styles["ArticleH1"]))
            in_abstract = True
            i += 1
            continue
        if line == r"\end{abstract}":
            in_abstract = False
            i += 1
            continue
        heading = re.match(r"\\(section|subsection|subsubsection)\*?\{(.*)\}", line)
        if heading:
            style = styles["ArticleH1"] if heading.group(1) == "section" else styles["ArticleH2"]
            story.append(Paragraph(para_text(heading.group(2)), style))
            i += 1
            continue
        if line == r"\begin{table}[t]" or line.startswith(r"\begin{table}"):
            block = []
            i += 1
            while i < len(lines) and lines[i].strip() != r"\end{table}":
                block.append(lines[i])
                i += 1
            story.extend(parse_table(block, regular, bold, table_number))
            table_number += 1
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
            if image and image.exists():
                pic = Image(str(image))
                pic._restrictSize(6.35 * inch, 3.65 * inch)
                pic.hAlign = "CENTER"
                story.append(pic)
            story.append(Paragraph(f"<font color='{MUTED.hexval()}'><b>Figure {figure_number}.</b></font> {html.escape(caption)}", styles["ArticleCaption"]))
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
            story.append(Paragraph(html.escape(math_to_text(" ".join(equation))), styles["ArticleEquation"]))
            i += 1
            continue
        if line in {r"\begin{itemize}", r"\end{itemize}", r"\begin{enumerate}", r"\end{enumerate}", r"\toprule", r"\midrule", r"\bottomrule"} or line.startswith(r"\label") or line.startswith(r"\bibliograph"):
            i += 1
            continue
        if line.startswith(r"\item"):
            story.append(Paragraph("• " + para_text(line[len(r"\item"):].strip()), styles["ArticleBullet"]))
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
        style = styles["ArticleBody"]
        if paragraph.startswith(r"\noindent\textbf{Keywords:"):
            style = styles["ArticleKeyword"]
        if in_abstract:
            style = ParagraphStyle("AbstractBody", parent=style, fontName=italic)
        story.append(Paragraph(para_text(paragraph), style))

    story.append(Paragraph("References", styles["ArticleH1"]))
    for reference in parse_bibliography(ROOT / "paper" / "references.bib"):
        story.append(Paragraph(para_text(reference), styles["ArticleRef"]))

    def draw_page(canvas, doc_obj):
        if doc_obj.page == 1:
            return
        canvas.saveState()
        width, height = A4
        canvas.setStrokeColor(ACCENT)
        canvas.setLineWidth(0.35)
        canvas.line(doc_obj.leftMargin, height - 0.49 * inch, width - doc_obj.rightMargin, height - 0.49 * inch)
        canvas.setFont(regular, 7.6)
        canvas.setFillColor(MUTED)
        canvas.drawString(doc_obj.leftMargin, height - 0.39 * inch, "COMMUNICATION, CORRELATION, AND COLLECTIVE FAILURE")
        canvas.drawRightString(width - doc_obj.rightMargin, height - 0.39 * inch, "VERONIKA LORAN")
        canvas.drawCentredString(width / 2, 0.34 * inch, str(doc_obj.page))
        canvas.restoreState()

    doc.build(story, onFirstPage=draw_page, onLaterPages=draw_page)
    return OUT


if __name__ == "__main__":
    print(build())
