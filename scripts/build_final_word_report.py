"""
Build Word Document (.docx) from IntelliCredit Capstone Final Report Markdown
=============================================================================
Converts reports/IntelliCredit_Capstone_Final_Report.md into a publication-grade
Word document with professional formatting, embedded charts, formatted tables,
custom typography, and executive layout.
"""

import os
import re
from PIL import Image

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
MD_PATH = os.path.join(REPORTS_DIR, "IntelliCredit_Capstone_Final_Report.md")
DOCX_PATH = os.path.join(REPORTS_DIR, "IntelliCredit_Capstone_Final_Report.docx")

# Color palette
COLOR_PRIMARY = RGBColor(0x1F, 0x4E, 0x79)    # Deep Navy Blue
COLOR_SECONDARY = RGBColor(0x2E, 0x40, 0x53)  # Slate Blue
COLOR_TEXT = RGBColor(0x26, 0x26, 0x26)       # Off-black
COLOR_MUTED = RGBColor(0x59, 0x59, 0x59)      # Charcoal Gray
COLOR_HIGHLIGHT = RGBColor(0xC0, 0x39, 0x2B)  # Crimson Accent

HEX_PRIMARY = "1F4E79"
HEX_ZEBRA = "F4F6F9"
HEX_WHITE = "FFFFFF"
HEX_BORDER = "D3D3D3"
HEX_CALLOUT_BG = "EBF5FB"


def sanitize_xml(text: str) -> str:
    """Filter out invalid XML control characters."""
    if not text:
        return ""
    return "".join(c for c in text if ord(c) in (9, 10, 13) or ord(c) >= 32)


def clean_latex(text: str) -> str:
    """Transform LaTeX math notation into clean, professional Unicode typography."""
    if not text:
        return ""
    text = sanitize_xml(text)
    # Block math
    text = re.sub(r'\$\$(.*?)\$\$', r'\1', text)
    # Inline math
    text = re.sub(r'\$(.*?)\$', r'\1', text)
    # Common LaTeX macros
    replacements = [
        (r'\\text\{([^}]*)\}', r'\1'),
        (r'\\mathbf\{([^}]*)\}', r'\1'),
        (r'\\mathit\{([^}]*)\}', r'\1'),
        (r'\\land', '∧'),
        (r'\\implies', '⇒'),
        (r'\\approx', '≈'),
        (r'\\times', '×'),
        (r'\\pm', '±'),
        (r'\\ge\b', '≥'),
        (r'\\geq\b', '≥'),
        (r'\\le\b', '≤'),
        (r'\\leq\b', '≤'),
        (r'\\sim', '~'),
        (r'\\Delta', 'Δ'),
        (r'\\beta', 'β'),
        (r'\\chi\^2', 'χ²'),
        (r'\\frac\{([^}]*)\}\{([^}]*)\}', r'(\1) / (\2)'),
        (r'\\min', 'min'),
        (r'\\max', 'max'),
        (r'\\left\(', '('),
        (r'\\right\)', ')'),
        (r'\\left\[', '['),
        (r'\\right\]', ']'),
        (r'\\_ ', '_ '),
        (r'\\_', '_'),
    ]
    for pattern, rep in replacements:
        text = re.sub(pattern, rep, text)
    return text


def set_cell_background(cell, hex_color):
    """Set background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner padding for table cell in twips (1 pt = 20 twips)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)


def set_table_borders(table, color="D3D3D3"):
    """Set elegant, subtle table borders."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
            <w:insideV w:val="none"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)


def add_formatted_text(paragraph, text: str, default_font_size=10.5, default_color=COLOR_TEXT, default_bold=False, default_italic=False):
    """Parse inline markdown (bold, italic, code, math) and add formatted runs."""
    text = clean_latex(text)
    
    # Tokenize by bold, italic, inline code
    # Matches: ***bold italic***, **bold**, *italic*, `code`
    token_pattern = re.compile(r'(\*\*\*.*?\*\*\*|\*\*.*?\*\*|\*.*?\*|`.*?`)')
    tokens = token_pattern.split(text)
    
    for token in tokens:
        if not token:
            continue
        is_bold = default_bold
        is_italic = default_italic
        is_code = False
        content = token
        
        if token.startswith('***') and token.endswith('***') and len(token) >= 6:
            is_bold = True
            is_italic = True
            content = token[3:-3]
        elif token.startswith('**') and token.endswith('**') and len(token) >= 4:
            is_bold = True
            content = token[2:-2]
        elif token.startswith('*') and token.endswith('*') and len(token) >= 2:
            is_italic = True
            content = token[1:-1]
        elif token.startswith('`') and token.endswith('`') and len(token) >= 2:
            is_code = True
            content = token[1:-1]
            
        content = sanitize_xml(content)
        run = paragraph.add_run(content)
        run.bold = is_bold
        run.italic = is_italic
        if is_code:
            run.font.name = "Consolas"
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(0x99, 0x00, 0x00)
        else:
            run.font.name = "Calibri"
            run.font.size = Pt(default_font_size)
            run.font.color.rgb = default_color


def add_page_number_to_section(section):
    """Add footer with left text and right page number field."""
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    # Left text
    run_left = p.add_run("IntelliCredit: Capstone Final Report (23CSE452)\tPage ")
    run_left.font.name = "Calibri"
    run_left.font.size = Pt(9)
    run_left.font.color.rgb = COLOR_MUTED
    
    # XML Page field
    fldSimple = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
    p._p.append(fldSimple)
    
    run_of = p.add_run(" of ")
    run_of.font.name = "Calibri"
    run_of.font.size = Pt(9)
    run_of.font.color.rgb = COLOR_MUTED
    
    fldSimple_num = parse_xml(r'<w:fldSimple %s w:instr="NUMPAGES"/>' % nsdecls('w'))
    p._p.append(fldSimple_num)


def main():
    print(f"Reading markdown from: {MD_PATH}")
    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_content = f.read()

    doc = docx.Document()

    # 1. Page setup - Standard Letter / A4 with 1 inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        add_page_number_to_section(section)

    # Base styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = COLOR_TEXT

    # Split lines and parse blocks
    lines = md_content.splitlines()
    i = 0
    total_lines = len(lines)
    is_cover_page = True

    while i < total_lines:
        line = lines[i].strip()

        # Blank line
        if not line:
            i += 1
            continue

        # Horizontal rule / Page separator
        if line == "---":
            # Add subtle divider or skip
            i += 1
            continue

        # Title: # CAPSTONE PROJECT: FINAL REPORT
        if line.startswith("# CAPSTONE PROJECT: FINAL REPORT"):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(36)
            p.paragraph_format.space_after = Pt(8)
            run = p.add_run("CAPSTONE PROJECT: FINAL REPORT")
            run.font.name = "Calibri"
            run.font.size = Pt(13)
            run.bold = True
            run.font.color.rgb = COLOR_MUTED
            i += 1
            continue

        # Main Title: # IntelliCredit...
        if line.startswith("# IntelliCredit:"):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(12)
            run = p.add_run(line.replace("#", "").strip())
            run.font.name = "Calibri"
            run.font.size = Pt(24)
            run.bold = True
            run.font.color.rgb = COLOR_PRIMARY
            i += 1
            continue

        # Subtitle: ### Predicting default risk...
        if line.startswith("### Predicting default risk"):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(24)
            run = p.add_run(line.replace("###", "").strip())
            run.font.name = "Calibri"
            run.font.size = Pt(12)
            run.italic = True
            run.font.color.rgb = COLOR_MUTED
            i += 1
            continue

        # Heading 1: ## Section
        if line.startswith("## "):
            heading_text = line[3:].strip()
            
            # Determine if a page break should precede this section
            page_break_sections = [
                "Declaration and Acknowledgement",
                "Abstract",
                "Executive Summary",
                "Table of Contents",
                "1. Introduction",
                "2. Dataset Collection",
                "3. Exploratory Data Analysis",
                "4. Feature Engineering",
                "5. Advanced Analytics",
                "6. Combined Business Insights",
                "7. Production Interactive Application",
                "8. Reflections",
                "References",
                "Appendices"
            ]
            if any(heading_text.startswith(sec) for sec in page_break_sections):
                doc.add_page_break()

            h1 = doc.add_paragraph()
            h1.paragraph_format.space_before = Pt(18)
            h1.paragraph_format.space_after = Pt(6)
            h1.paragraph_format.keep_with_next = True
            run = h1.add_run(heading_text)
            run.font.name = "Calibri"
            run.font.size = Pt(16)
            run.bold = True
            run.font.color.rgb = COLOR_PRIMARY
            i += 1
            continue

        # Heading 2: ### Subsection
        if line.startswith("### "):
            h2_text = line[4:].strip()
            h2 = doc.add_paragraph()
            h2.paragraph_format.space_before = Pt(12)
            h2.paragraph_format.space_after = Pt(4)
            h2.paragraph_format.keep_with_next = True
            run = h2.add_run(h2_text)
            run.font.name = "Calibri"
            run.font.size = Pt(13)
            run.bold = True
            run.font.color.rgb = COLOR_SECONDARY
            i += 1
            continue

        # Heading 3: #### Sub-subsection
        if line.startswith("#### "):
            h3_text = line[5:].strip()
            h3 = doc.add_paragraph()
            h3.paragraph_format.space_before = Pt(8)
            h3.paragraph_format.space_after = Pt(2)
            h3.paragraph_format.keep_with_next = True
            run = h3.add_run(h3_text)
            run.font.name = "Calibri"
            run.font.size = Pt(11)
            run.bold = True
            run.font.color.rgb = COLOR_MUTED
            i += 1
            continue

        # Image detection: ![Alt text](path)
        img_match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
        if img_match:
            alt_text, img_rel_path = img_match.groups()
            img_full_path = os.path.join(REPORTS_DIR, img_rel_path)
            
            if os.path.exists(img_full_path):
                # Calculate proper dimensions so image fits page nicely
                with Image.open(img_full_path) as im:
                    orig_w, orig_h = im.size
                
                aspect = orig_h / orig_w
                # Max dimensions: 6.0 in width, 5.0 in height
                max_w = 6.0
                max_h = 4.8
                
                if (max_w * aspect) > max_h:
                    target_h = max_h
                    target_w = max_h / aspect
                else:
                    target_w = max_w
                    target_h = max_w * aspect

                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(10)
                p_img.paragraph_format.space_after = Pt(4)
                p_img.paragraph_format.keep_with_next = True
                run_img = p_img.add_run()
                run_img.add_picture(img_full_path, width=Inches(target_w), height=Inches(target_h))

                # Check if next line is a figure caption: *Figure X. ...*
                if i + 1 < total_lines and lines[i + 1].strip().startswith("*Figure"):
                    caption_text = lines[i + 1].strip().strip("*")
                    p_cap = doc.add_paragraph()
                    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p_cap.paragraph_format.space_before = Pt(2)
                    p_cap.paragraph_format.space_after = Pt(12)
                    run_cap = p_cap.add_run(caption_text)
                    run_cap.font.name = "Calibri"
                    run_cap.font.size = Pt(9.0)
                    run_cap.italic = True
                    run_cap.font.color.rgb = COLOR_MUTED
                    i += 2
                    continue
            i += 1
            continue

        # Markdown Table Detection
        if line.startswith("|") and line.endswith("|"):
            table_lines = []
            while i < total_lines and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                table_lines.append(lines[i].strip())
                i += 1

            if len(table_lines) >= 2:
                # Parse markdown table
                header_raw = [c.strip() for c in table_lines[0].split("|")[1:-1]]
                # Row 1 is divider (|---|---|)
                body_raw = []
                for row_line in table_lines[2:]:
                    cells = [c.strip() for c in row_line.split("|")[1:-1]]
                    # Ensure row has same column count
                    if len(cells) < len(header_raw):
                        cells += [""] * (len(header_raw) - len(cells))
                    body_raw.append(cells[:len(header_raw)])

                num_cols = len(header_raw)
                num_rows = 1 + len(body_raw)
                
                table = doc.add_table(rows=num_rows, cols=num_cols)
                table.alignment = WD_TABLE_ALIGNMENT.CENTER
                set_table_borders(table, color=HEX_BORDER)

                # Set column widths proportionally
                avail_width = 6.5  # inches
                col_w = avail_width / max(num_cols, 1)

                # Style Header Row
                hdr_row = table.rows[0]
                trPr = hdr_row._tr.get_or_add_trPr()
                trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
                trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

                for c_idx, cell_text in enumerate(header_raw):
                    cell = hdr_row.cells[c_idx]
                    cell.width = Inches(col_w)
                    set_cell_background(cell, HEX_PRIMARY)
                    set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
                    p = cell.paragraphs[0]
                    p.paragraph_format.space_before = Pt(0)
                    p.paragraph_format.space_after = Pt(0)
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    add_formatted_text(p, cell_text, default_font_size=9.5, default_color=RGBColor(0xFF, 0xFF, 0xFF), default_bold=True)

                # Style Body Rows
                for r_idx, row_data in enumerate(body_raw):
                    row = table.rows[r_idx + 1]
                    trPr = row._tr.get_or_add_trPr()
                    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

                    row_bg = HEX_ZEBRA if r_idx % 2 == 1 else HEX_WHITE
                    for c_idx, cell_text in enumerate(row_data):
                        cell = row.cells[c_idx]
                        cell.width = Inches(col_w)
                        set_cell_background(cell, row_bg)
                        set_cell_margins(cell, top=90, bottom=90, left=130, right=130)
                        p = cell.paragraphs[0]
                        p.paragraph_format.space_before = Pt(0)
                        p.paragraph_format.space_after = Pt(0)
                        
                        # Right-align if numeric / percentage, else left
                        clean_c = clean_latex(cell_text)
                        if re.match(r'^[\d.,%₹+\-x×\[\]\s]+$', clean_c) and len(clean_c) < 25:
                            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                        elif c_idx == 0:
                            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                        else:
                            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            
                        add_formatted_text(p, cell_text, default_font_size=9.0, default_color=COLOR_TEXT)

                # Caption after table (e.g. *Table X. Description*)
                if i < total_lines and lines[i].strip().startswith("*Table"):
                    caption_line = lines[i].strip().strip("*")
                    p_tcap = doc.add_paragraph()
                    p_tcap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p_tcap.paragraph_format.space_before = Pt(4)
                    p_tcap.paragraph_format.space_after = Pt(12)
                    run_tcap = p_tcap.add_run(caption_line)
                    run_tcap.font.name = "Calibri"
                    run_tcap.font.size = Pt(9.0)
                    run_tcap.italic = True
                    run_tcap.font.color.rgb = COLOR_MUTED
                    i += 1
                else:
                    # Small spacing after table
                    p_space = doc.add_paragraph()
                    p_space.paragraph_format.space_before = Pt(0)
                    p_space.paragraph_format.space_after = Pt(6)

            continue

        # Blockquote / Callout (> ...)
        if line.startswith("> "):
            callout_text = line[2:].strip()
            p_call = doc.add_paragraph()
            p_call.paragraph_format.left_indent = Inches(0.4)
            p_call.paragraph_format.right_indent = Inches(0.4)
            p_call.paragraph_format.space_before = Pt(6)
            p_call.paragraph_format.space_after = Pt(6)
            add_formatted_text(p_call, callout_text, default_font_size=10.0, default_color=COLOR_PRIMARY, default_italic=True)
            i += 1
            continue

        # Bullet List (- or *)
        if line.startswith("- ") or line.startswith("* "):
            list_text = line[2:].strip()
            p_list = doc.add_paragraph(style='List Bullet')
            p_list.paragraph_format.space_before = Pt(2)
            p_list.paragraph_format.space_after = Pt(2)
            p_list.paragraph_format.line_spacing = 1.15
            add_formatted_text(p_list, list_text, default_font_size=10.5, default_color=COLOR_TEXT)
            i += 1
            continue

        # Numbered List (1. , 2. )
        num_match = re.match(r'^(\d+)\.\s+(.*)$', line)
        if num_match:
            num_str, num_text = num_match.groups()
            p_num = doc.add_paragraph(style='List Number')
            p_num.paragraph_format.space_before = Pt(2)
            p_num.paragraph_format.space_after = Pt(2)
            p_num.paragraph_format.line_spacing = 1.15
            add_formatted_text(p_num, num_text, default_font_size=10.5, default_color=COLOR_TEXT)
            i += 1
            continue

        # Fenced code block (```)
        if line.startswith("```"):
            code_lines = []
            i += 1
            while i < total_lines and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            
            p_code = doc.add_paragraph()
            p_code.paragraph_format.left_indent = Inches(0.3)
            p_code.paragraph_format.space_before = Pt(4)
            p_code.paragraph_format.space_after = Pt(6)
            run_code = p_code.add_run("\n".join(code_lines))
            run_code.font.name = "Consolas"
            run_code.font.size = Pt(8.5)
            run_code.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
            continue

        # Regular Body Paragraph
        p_body = doc.add_paragraph()
        p_body.paragraph_format.space_before = Pt(0)
        p_body.paragraph_format.space_after = Pt(5)
        p_body.paragraph_format.line_spacing = 1.15
        add_formatted_text(p_body, line, default_font_size=10.5, default_color=COLOR_TEXT)
        i += 1

    print(f"Saving compiled Word document to: {DOCX_PATH}")
    doc.save(DOCX_PATH)
    file_size_kb = os.path.getsize(DOCX_PATH) / 1024
    print(f"Document successfully created! File size: {file_size_kb:.1f} KB")


if __name__ == "__main__":
    main()
