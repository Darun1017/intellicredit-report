"""
Build the complete, professionally styled, and visual presentation deck
for IntelliCredit Review 2 in Final_Project_Presentation_Template.pptx.
Inserts all necessary figures, formats all tables, aligns layouts,
and adds executive takeaway banners on every slide without any duplication.
Includes a dedicated Literature Review & Comparative Study slide (Slide 3),
bringing the deck to a comprehensive 18 slides.
"""
import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

BAK_PATH = r"Final_Project_Presentation_Template.pptx.bak"
PPT_PATH = r"Final_Project_Presentation_Template.pptx"

# -------------------------------------------------------------------------
# Formatting Utilities & Corporate Color Palette
# -------------------------------------------------------------------------
NAVY = (20, 45, 78)           # Primary corporate dark navy (#142D4E)
DARK = (31, 41, 55)           # Body dark slate (#1F2937)
GRAY = (75, 85, 99)           # Muted secondary gray (#4B5563)
WHITE = (255, 255, 255)       # Crisp white (#FFFFFF)
LIGHT_BG = (240, 245, 247)    # Subtle table alternating / callout background (#F0F5F7)
BORDER_GRAY = (209, 213, 219) # Clean border gray (#D1D5DB)
GREEN = (22, 163, 74)         # High-conviction positive green (#16A34A)
RED = (220, 38, 38)           # High-risk warning red (#DC2626)

def clear_shape_text(shape):
    """Clear all paragraphs and runs in a shape."""
    tf = shape.text_frame
    for p in list(tf.paragraphs[1:]):
        p._p.getparent().remove(p._p)
    p0 = tf.paragraphs[0]
    for r_elem in list(p0._p.findall(qn('a:r'))):
        p0._p.remove(r_elem)
    return p0

def set_text(shape, text, font_size=None, bold=None, color=None, alignment=None):
    """Set text in a shape cleanly."""
    if shape is None:
        return
    p0 = clear_shape_text(shape)
    run = p0.add_run()
    run.text = text
    if font_size:
        run.font.size = Pt(font_size)
    if bold is not None:
        run.font.bold = bold
    if color:
        run.font.color.rgb = RGBColor(*color)
    if alignment:
        p0.alignment = alignment

def set_cell(table, row, col, text, font_size=8.5, bold=None, color=None, alignment=PP_ALIGN.LEFT, pad_top=3, pad_bottom=3):
    """Set text and format a table cell."""
    if row >= len(table.rows) or col >= len(table.columns):
        return
    cell = table.cell(row, col)
    tf = cell.text_frame
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    cell.margin_left = Pt(4)
    cell.margin_right = Pt(4)
    cell.margin_top = Pt(pad_top)
    cell.margin_bottom = Pt(pad_bottom)

    for p in list(tf.paragraphs[1:]):
        p._p.getparent().remove(p._p)
    p0 = tf.paragraphs[0]
    for r_elem in list(p0._p.findall(qn('a:r'))):
        p0._p.remove(r_elem)
    run = p0.add_run()
    run.text = text
    if font_size:
        run.font.size = Pt(font_size)
    if bold is not None:
        run.font.bold = bold
    if color is not None:
        run.font.color.rgb = RGBColor(*color)
    elif row == 0:
        # Default header row font color is crisp white for high contrast
        run.font.color.rgb = RGBColor(*WHITE)
    if alignment:
        p0.alignment = alignment

def set_col_widths(table, widths):
    """Set individual column widths for a table."""
    for i, w in enumerate(widths):
        if i < len(table.columns):
            table.columns[i].width = w

def set_row_heights(table, pt_height):
    """Set explicit height for each row in a table."""
    for r in table.rows:
        r.height = Pt(pt_height)

def get_shapes(slide):
    """Return dictionary of shapes indexed by name."""
    return {s.name: s for s in slide.shapes}

def remove_shape(slide, shape_name):
    """Remove a shape by name."""
    for s in list(slide.shapes):
        if s.name == shape_name:
            sp = s._element
            sp.getparent().remove(sp)
            return True
    return False

def add_takeaway(slide, text):
    """Add a polished, high-contrast Takeaway banner at the bottom of the slide."""
    left = 609600
    top = 5916168
    width = 10972800
    height = 430000

    # 1. Background box
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    bg.name = "Takeaway_BG"
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(*LIGHT_BG)
    bg.line.color.rgb = RGBColor(*BORDER_GRAY)
    bg.line.width = Pt(1)

    # 2. Left accent bar
    accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, 80000, height)
    accent.name = "Takeaway_Accent"
    accent.fill.solid()
    accent.fill.fore_color.rgb = RGBColor(*NAVY)
    accent.line.fill.background()

    # 3. Text box
    tb = slide.shapes.add_textbox(left + 120000, top, width - 140000, height)
    tb.name = "Takeaway_Text"
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT

    # Bold 'Takeaway   ' prefix
    r1 = p.add_run()
    r1.text = "Takeaway   "
    r1.font.bold = True
    r1.font.size = Pt(9.5)
    r1.font.color.rgb = RGBColor(*NAVY)

    # Main takeaway message
    r2 = p.add_run()
    r2.text = text
    r2.font.bold = False
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = RGBColor(*DARK)


# -------------------------------------------------------------------------
# Build Process
# -------------------------------------------------------------------------
def main():
    print("Resetting presentation from clean backup...")
    if not os.path.exists(BAK_PATH):
        raise FileNotFoundError(f"Backup template not found at {BAK_PATH}")
    shutil.copyfile(BAK_PATH, PPT_PATH)
    prs = Presentation(PPT_PATH)
    print("Opened clean presentation template.")

    # ---------------------------------------------------------------------
    # SLIDE 1: Title & Presentation Header
    # ---------------------------------------------------------------------
    s1 = prs.slides[0]
    sh1 = get_shapes(s1)
    set_text(sh1['Rectangle 6'], "23CSE452 BUSINESS ANALYTICS  |  FINAL PROJECT DEFENSE", font_size=11, bold=True, color=NAVY)
    set_text(sh1['Rectangle 1'], "IntelliCredit: FinTech Micro-Lending Risk & Alternative Credit Scoring Engine", font_size=21, bold=True, color=DARK)
    set_text(sh1['Rectangle 3'], "Final Project Review 2: Advanced Analytics & Underwriter Decision Cockpit", font_size=13, bold=False, color=GRAY)
    set_text(sh1['Rectangle 4'],
        "Team 5: Darun R G (CB.SC.U4CSE23114)  ·  Vimalharihar S K (CB.SC.U4CSE23120)  ·  Abhinav Juturu (CB.SC.U4CSE23103)\n"
        "Gowtham Reddy (CB.SC.U4CSE23119)  ·  Adithya (CB.SC.U4CSE23101)",
        font_size=11, bold=False, color=DARK)
    set_text(sh1['Rectangle 5'],
        "Department of Computer Science & Engineering  |  Amrita Vishwa Vidyapeetham\n"
        "Faculty Guide: Rohini S  |  Presentation Date: November 2026",
        font_size=10, bold=False, color=GRAY)

    # ---------------------------------------------------------------------
    # SLIDE 2: Project Overview
    # ---------------------------------------------------------------------
    s2 = prs.slides[1]
    sh2 = get_shapes(s2)
    set_text(sh2['Rectangle 7'], "PROJECT OVERVIEW", font_size=11, bold=True, color=NAVY)
    set_text(sh2['Rectangle 1'], "Business problem and objectives", font_size=20, bold=True, color=DARK)

    set_text(sh2['Rectangle 3'],
        "Business problem: Over 1.4 billion gig-economy workers and thin-file individuals lack traditional credit scores "
        "(CIBIL/FICO). Lenders either exclude them unfairly or lend blind, resulting in prohibitive delinquency and high default rates.",
        font_size=10.5, color=DARK)

    set_text(sh2['Rectangle 4'],
        "Objectives: (1) ML Default Prediction: Develop interpretable Machine Learning classifiers beating baseline models "
        "(AUC > 0.70) on held-out test applicants with TreeSHAP explainability. (2) Advanced Analytics: Forecast monthly portfolio "
        "default rates under macroeconomic shocks (SARIMAX) and uncover conjunctive delinquency traps (Association Rules).",
        font_size=10.5, color=DARK)

    set_text(sh2['Rectangle 5'],
        "Business decision: Enable underwriter decision automation (auto-approve, manual conditional review, or auto-decline) "
        "and dynamically calibrate credit limits and capital loss reserves (ECL in ₹ Crore) as macroeconomic cycles turn.",
        font_size=10.5, color=DARK)

    set_text(sh2['Rectangle 6'],
        "Expected output: Production-grade underwriting decision cockpit: calibrated applicant default probability, 93 behavioral "
        "warning badges, dynamic Point-in-Time stress multiplier, and a live Streamlit dashboard.",
        font_size=10.5, color=DARK)

    add_takeaway(s2, "IntelliCredit replaces blunt credit bureau exclusion with an interpretable, macro-aware risk analytics engine.")

    # ---------------------------------------------------------------------
    # SLIDE 3: Literature Review & Comparative Study (Streamlined Punchy Matrix)
    # ---------------------------------------------------------------------
    new_s = prs.slides.add_slide(prs.slide_layouts[5])
    sldIdLst = prs.slides._sldIdLst
    elem = sldIdLst[-1]
    sldIdLst.remove(elem)
    sldIdLst.insert(2, elem)

    s3 = prs.slides[2]

    # Category Tracker
    tb_hdr = s3.shapes.add_textbox(609600, 342900, 10477500, 285750)
    set_text(tb_hdr, "LITERATURE REVIEW & BENCHMARKS", font_size=11, bold=True, color=NAVY)

    # Title
    tb_title = s3.shapes.add_textbox(609600, 680000, 10972800, 550000)
    set_text(tb_title, "Related works and comparative study", font_size=20, bold=True, color=DARK)

    # Top Literature Box (2 clean, readable lines)
    lit_left = 609600
    lit_top = 1300000
    lit_width = 10972800
    lit_height = 720000

    lit_bg = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, lit_left, lit_top, lit_width, lit_height)
    lit_bg.fill.solid()
    lit_bg.fill.fore_color.rgb = RGBColor(*LIGHT_BG)
    lit_bg.line.color.rgb = RGBColor(*BORDER_GRAY)
    lit_bg.line.width = Pt(1)

    accent = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, lit_left, lit_top, 80000, lit_height)
    accent.fill.solid()
    accent.fill.fore_color.rgb = RGBColor(*NAVY)
    accent.line.fill.background()

    tb_lit = s3.shapes.add_textbox(lit_left + 120000, lit_top + 10000, lit_width - 150000, lit_height - 20000)
    tf_lit = tb_lit.text_frame
    tf_lit.word_wrap = True
    tf_lit.margin_top = Pt(3)
    tf_lit.margin_bottom = Pt(3)
    tf_lit.margin_left = Pt(2)
    tf_lit.margin_right = Pt(2)

    p0 = tf_lit.paragraphs[0]
    r = p0.add_run()
    r.text = "Foundations in Literature: "
    r.font.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(*NAVY)
    r2 = p0.add_run()
    r2.text = "Alternative scoring (Khandani et al., 2010; Óskarsdóttir et al., 2019) proved cash-flow signals predict default, but lacked macro stress links. Macro risk literature (Pesaran et al., 2006; Basel/IFRS 9) modeled top-down stress, but remained disconnected from borrower underwriting."
    r2.font.size = Pt(9.0)
    r2.font.color.rgb = RGBColor(*DARK)

    p1 = tf_lit.add_paragraph()
    p1.space_before = Pt(2)
    r3 = p1.add_run()
    r3.text = "IntelliCredit Contribution: "
    r3.font.bold = True
    r3.font.size = Pt(9.5)
    r3.font.color.rgb = RGBColor(*NAVY)
    r4 = p1.add_run()
    r4.text = "Unites granular alternative signals (ML), dynamic macro forecasting (SARIMAX), and 93 delinquency warning rules into a single live decision cockpit."
    r4.font.size = Pt(9.0)
    r4.font.color.rgb = RGBColor(*DARK)

    # 4. Streamlined 4-Column x 5-Row Table (Larger 9.5pt font, short punchy phrases)
    t_top = 2150000
    t_h = 3600000
    t_shape = s3.shapes.add_table(5, 4, lit_left, t_top, lit_width, t_h)
    t3_comp = t_shape.table
    col_w = [2100000, 2800000, 2800000, 3272800]
    set_col_widths(t3_comp, col_w)

    table_data = [
        ("Evaluation Dimension", "Traditional Bureaus (CIBIL/FICO)", "Standard Academic ML", "IntelliCredit (Our Proposed Work)"),
        ("Target Borrower Cohort", "Salaried, prime borrowers only\n(excludes 1.4B unbanked)", "Formally banked credit applicants\n(struggles on volatile gig income)", "Thin-file & gig-economy workers\n(₹14k–₹48k/mo; unlocks inclusion)"),
        ("Data Modality & Ingestion", "Historical debt trade-lines & formal salary slips (static)", "Cross-sectional tabular application forms (offline snapshot)", "Alternative cash-flow signals + Live FRED/World Bank macro APIs"),
        ("Macroeconomic Awareness", "Static Through-The-Cycle (TTC)\n(insensitive to live macro cycles)", "Zero macro linkage\n(assumes static economic regime)", "Dynamic Point-in-Time (PiT)\nSARIMAX forecasting with ₹ Crore ECL"),
        ("Explainability & Underwriting", "Opaque 300–900 bureau score\n(rigid pass/fail scorecards)", "Global feature importance only\n(black-box tree ensembles)", "Local TreeSHAP waterfalls +\n93 Fisher-pruned rules (100% test gen.)")
    ]

    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = t3_comp.cell(r_idx, c_idx)
            cell.margin_left = Pt(6)
            cell.margin_right = Pt(6)
            cell.margin_top = Pt(4)
            cell.margin_bottom = Pt(4)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if r_idx == 0:
                cell.fill.fore_color.rgb = RGBColor(*NAVY)
            elif r_idx % 2 == 1:
                cell.fill.fore_color.rgb = RGBColor(*WHITE)
            else:
                cell.fill.fore_color.rgb = RGBColor(*LIGHT_BG)
            
            p = cell.text_frame.paragraphs[0]
            r = p.add_run()
            r.text = val
            if r_idx == 0:
                r.font.size = Pt(10)
                r.font.bold = True
                r.font.color.rgb = RGBColor(*WHITE)
            elif c_idx == 0:
                r.font.size = Pt(9.5)
                r.font.bold = True
                r.font.color.rgb = RGBColor(*DARK)
            elif c_idx == 3:
                r.font.size = Pt(9.2)
                r.font.bold = True
                r.font.color.rgb = RGBColor(*NAVY)
            else:
                r.font.size = Pt(9.0)
                r.font.color.rgb = RGBColor(*DARK)

    # Slide number placeholder
    r2_tb = s3.shapes.add_textbox(10953750, 6343650, 619125, 238125)
    r2_tb.name = "Rectangle 2"
    set_text(r2_tb, "03", font_size=10, bold=False, color=GRAY, alignment=PP_ALIGN.RIGHT)

    # Takeaway banner
    add_takeaway(s3, "IntelliCredit replaces blunt bureau exclusion with an interpretable, macro-grounded credit analytics engine.")

    # ---------------------------------------------------------------------
    # SLIDE 4: Units 1 to 3 Complete Workflow
    # ---------------------------------------------------------------------
    s4 = prs.slides[3]
    sh4 = get_shapes(s4)
    set_text(sh4['Rectangle 5'], "UNITS 1 TO 3", font_size=11, bold=True, color=NAVY)
    set_text(sh4['Rectangle 1'], "Complete project workflow", font_size=20, bold=True, color=DARK)

    t4 = sh4['Table 3'].table
    set_col_widths(t4, [2200000, 8772800])
    set_cell(t4, 0, 0, "Stage", font_size=10, bold=True, color=WHITE)
    set_cell(t4, 0, 1, "Your implementation", font_size=10, bold=True, color=WHITE)

    set_cell(t4, 1, 0, "Unit 1", font_size=9.5, bold=True, color=DARK)
    set_cell(t4, 1, 1,
        "Programmatic data generation (30,000 borrowers, 360,000 transactions); KNN missing imputation, IQR outlier winsorization; "
        "38 EDA visualisations with chi-square & Mann-Whitney tests; 14 engineered alternative behavioral features, VIF, WoE/IV, PCA, SMOTE.", font_size=9)

    set_cell(t4, 2, 0, "Unit 2", font_size=9.5, bold=True, color=DARK)
    set_cell(t4, 2, 1,
        "5 baseline + 4 tuned ML algorithms (LR, RF, LightGBM, Tuned XGBoost); voting & stacking ensembles; leak-free 5-fold CV with "
        "SMOTE pipeline; ROC/PR curves, KS test, TreeSHAP waterfall explainability; INR cost-optimal threshold (₹81.9k vs ₹9.7k).", font_size=9)

    set_cell(t4, 3, 0, "Unit 3", font_size=9.5, bold=True, color=DARK)
    set_cell(t4, 3, 1,
        "Method 1: Time-series portfolio default forecasting (SARIMAX with live FRED/World Bank macro regressors, 40-origin backtest, "
        "3 stress scenarios) and Method 2: Association rule mining (Apriori vs FP-Growth, 93 warning rules, 100% test generalization).", font_size=9)

    set_cell(t4, 4, 0, "Final application", font_size=9.5, bold=True, color=DARK)
    set_cell(t4, 4, 1,
        "Production Streamlit underwriter dashboard (dashboard/app.py): 5 interactive tabs including Dataset Explorer, Real-time "
        "Scoring with TreeSHAP, Active Warning Badges, Portfolio Forecasts, and Macro Stress Testing. Plus standalone HTML report.", font_size=9)

    sh4['Table 3'].top = 1800000
    sh4['Table 3'].height = 3400000

    sh4['Rectangle 4'].top = 5380000
    sh4['Rectangle 4'].height = 420000
    set_text(sh4['Rectangle 4'],
        "Completion status: 100% implementation delivered and verified across all 3 analytical units, 8 notebooks, dashboard, and technical report.",
        font_size=10, bold=True, color=NAVY)

    add_takeaway(s4, "Every analytical unit is integrated end-to-end: one validated dataset, one leak-free chronological split, and one unified dashboard.")

    # ---------------------------------------------------------------------
    # SLIDE 5: Dataset Across Units 1 to 3
    # ---------------------------------------------------------------------
    s5 = prs.slides[4]
    sh5 = get_shapes(s5)
    set_text(sh5['Rectangle 7'], "DATASET ACROSS UNITS 1 TO 3", font_size=11, bold=True, color=NAVY)
    set_text(sh5['Rectangle 1'], "Overall dataset description", font_size=20, bold=True, color=DARK)

    set_text(sh5['Rectangle 3'],
        "Source and collection: Programmatic statistical generation (NumPy distributions + Faker en_IN) for 30,000 borrowers and 360,000 "
        "transactions. Live institutional macroeconomic APIs from FRED (CPI inflation, call-money rate, 10y G-sec, INR/USD) and World Bank "
        "(unemployment, real GDP growth, lending rate). No pre-built Kaggle/UCI datasets used.", font_size=10, color=DARK)

    set_text(sh5['Rectangle 4'],
        "Final dataset size: 30,000 borrower profiles × 39 demographic/behavioral variables; 360,000 monthly transactions across 12 months; "
        "108 monthly macro observations (2017–2025); 30,000 originated loans × 250,191 loan-months over 72 months (2019–2024).", font_size=10, color=DARK)

    set_text(sh5['Rectangle 5'],
        "Coverage: Indian gig-economy and thin-file cohort; monthly income ₹14k–₹48k; gig platforms Swiggy, Zomato, Ola, Uber, Urban Company; "
        "7 institutional macroeconomic series; COVID lockdown and second-wave disruption event dummies included.", font_size=10, color=DARK)

    set_text(sh5['Rectangle 6'],
        "Unit mapping: Unit 1–2 use borrower profiles & 12-month transactions (default prediction). Unit 3 Method 1 uses monthly portfolio "
        "default rate panel & macro indicators (time-series). Unit 3 Method 2 uses 19 discretized behavioral flags on 24k training borrowers (ARM).", font_size=10, color=DARK)

    add_takeaway(s5, "An original, frozen, and reproducible data architecture linking micro borrower transactions to macroeconomic cycles.")

    # ---------------------------------------------------------------------
    # SLIDE 6: Sample Dataset and Key Variables
    # ---------------------------------------------------------------------
    s6 = prs.slides[5]
    sh6 = get_shapes(s6)
    set_text(sh6['Rectangle 6'], "FINAL PROJECT DATA", font_size=11, bold=True, color=NAVY)
    set_text(sh6['Rectangle 1'], "Sample dataset and key variables", font_size=20, bold=True, color=DARK)

    t6 = sh6['Table 3'].table
    set_col_widths(t6, [2400000, 1800000, 2200000, 4572800])
    set_row_heights(t6, 26)
    set_cell(t6, 0, 0, "Borrower ID / Platform", font_size=9, bold=True, color=WHITE)
    set_cell(t6, 0, 1, "Avg Monthly Income", font_size=9, bold=True, color=WHITE)
    set_cell(t6, 0, 2, "Loan Amount & Tenure", font_size=9, bold=True, color=WHITE)
    set_cell(t6, 0, 3, "Behavioral Metrics & Target", font_size=9, bold=True, color=WHITE)

    set_cell(t6, 1, 0, "BRW-000001 (Swiggy)", font_size=8.5, bold=True)
    set_cell(t6, 1, 1, "₹21,583 / mo", font_size=8.5)
    set_cell(t6, 1, 2, "₹1,16,166 (24 mos)", font_size=8.5)
    set_cell(t6, 1, 3, "Volatility: 0.18 | Utility: 92% | Target: Non-Default (0)", font_size=8.5)

    set_cell(t6, 2, 0, "BRW-000002 (Zomato)", font_size=8.5, bold=True)
    set_cell(t6, 2, 1, "₹25,132 / mo", font_size=8.5)
    set_cell(t6, 2, 2, "₹1,26,490 (24 mos)", font_size=8.5)
    set_cell(t6, 2, 3, "Volatility: 0.22 | Utility: 83% | Target: Non-Default (0)", font_size=8.5)

    set_cell(t6, 3, 0, "BRW-000014 (Ola)", font_size=8.5, bold=True)
    set_cell(t6, 3, 1, "₹16,420 / mo", font_size=8.5)
    set_cell(t6, 3, 2, "₹65,000 (12 mos)", font_size=8.5)
    set_cell(t6, 3, 3, "Volatility: 0.48 | Utility: 42% | Target: Defaulted (1)", font_size=8.5, color=RED)

    sh6['Table 3'].top = 1700000

    sh6['Rectangle 4'].top = 3300000
    sh6['Rectangle 4'].height = 1000000
    set_text(sh6['Rectangle 4'],
        "Key variables: loan_default_status (binary prediction target, 7.87% baseline default rate); avg_monthly_income (₹ continuous); "
        "income_volatility_index (std/mean income); utility_reliability_score (ratio of on-time utility payments); savings_buffer_ratio "
        "(end-of-month balance / monthly outflow); gig_tenure_months (platform stability).", font_size=9.5, color=DARK)

    sh6['Rectangle 5'].top = 4500000
    sh6['Rectangle 5'].height = 1000000
    set_text(sh6['Rectangle 5'],
        "Linked datasets: monthly_transactions.csv (12-month transaction logs); macro_india_monthly.csv (7 live FRED/World Bank macro indicators); "
        "portfolio/loan_book.csv & loan_performance.csv (macro-linked loan repayment panel for time-series). Samples in data/sample/.", font_size=9.5, color=DARK)

    add_takeaway(s6, "Multi-attribute feature vectors capture both willingness-to-pay (utility discipline) and cash-flow capacity (income volatility).")

    # ---------------------------------------------------------------------
    # SLIDE 7: Overall Dataset Validation
    # ---------------------------------------------------------------------
    s7 = prs.slides[6]
    sh7 = get_shapes(s7)
    set_text(sh7['Rectangle 5'], "OVERALL VALIDATION FOR UNITS 1 TO 3", font_size=11, bold=True, color=NAVY)
    set_text(sh7['Rectangle 1'], "Dataset validation and preparation", font_size=20, bold=True, color=DARK)

    t7 = sh7['Table 3'].table
    set_col_widths(t7, [2400000, 4200000, 4372800])
    set_row_heights(t7, 22)
    sh7['Table 3'].top = 1500000

    set_cell(t7, 0, 0, "Check", font_size=9, bold=True, color=WHITE, pad_top=2, pad_bottom=2)
    set_cell(t7, 0, 1, "Finding", font_size=9, bold=True, color=WHITE, pad_top=2, pad_bottom=2)
    set_cell(t7, 0, 2, "Correction / Evidence", font_size=9, bold=True, color=WHITE, pad_top=2, pad_bottom=2)

    set_cell(t7, 1, 0, "Missing values & duplicates", font_size=8, bold=True, pad_top=2, pad_bottom=2)
    set_cell(t7, 1, 1, "0 duplicate borrower IDs; 6,319 missing ages in txns; structural nulls in default_month.", font_size=8, pad_top=2, pad_bottom=2)
    set_cell(t7, 1, 2, "KNN imputation for missing ages; structural nulls verified. Retained 30k unique borrowers.", font_size=8, pad_top=2, pad_bottom=2)

    set_cell(t7, 2, 0, "Types, ranges & consistency", font_size=8, bold=True, pad_top=2, pad_bottom=2)
    set_cell(t7, 2, 1, "Income outliers detected via IQR; month_label had duplicates; unmapped ordinals.", font_size=8, pad_top=2, pad_bottom=2)
    set_cell(t7, 2, 2, "IQR winsorization applied; fixed dates with pd.date_range; corrected ordinal maps in config.", font_size=8, pad_top=2, pad_bottom=2)

    set_cell(t7, 3, 0, "Suitability across units", font_size=8, bold=True, pad_top=2, pad_bottom=2)
    set_cell(t7, 3, 1, "Units require borrower features (1-2), 72-month portfolio panel (M1), 19 binary flags (M2).", font_size=8, pad_top=2, pad_bottom=2)
    set_cell(t7, 3, 2, "Leak-free 80/20 split; SMOTE applied only within CV folds; fitted on train only. 21 checks pass.", font_size=8, pad_top=2, pad_bottom=2)

    set_cell(t7, 4, 0, "Synthetic data realism checks", font_size=8, bold=True, pad_top=2, pad_bottom=2)
    set_cell(t7, 4, 1, "Borrowers/txns synthetic. All 7 macro indicators 100% real from FRED & World Bank APIs.", font_size=8, pad_top=2, pad_bottom=2)
    set_cell(t7, 4, 2, "Validated against MFIN Micrometer (7.87% default), PLFS 2022-23 (₹14k-48k income), CGAP reports.", font_size=8, pad_top=2, pad_bottom=2)

    sh7['Rectangle 4'].top = 3150000
    sh7['Rectangle 4'].height = 420000
    set_text(sh7['Rectangle 4'],
        "Final validated dataset: 30,000 borrowers (borrower_profiles.csv), 360,000 transactions (monthly_transactions.csv), "
        "108 macro observations (macro_india_monthly.csv), 250,191 loan-months (data/portfolio/).", font_size=9, bold=True, color=NAVY)

    if os.path.exists("reports/presentation_figures/pipeline_architecture.png"):
        s7.shapes.add_picture("reports/presentation_figures/pipeline_architecture.png", 609600, 3750000, width=10972800, height=1850000)

    add_takeaway(s7, "Audited and leak-free: zero pipeline leakage, fixed timestamps, and benchmarked against real Indian financial data.")

    # ---------------------------------------------------------------------
    # SLIDE 8: Unit 1 Exploratory Analysis & Preprocessing
    # ---------------------------------------------------------------------
    s8 = prs.slides[7]
    sh8 = get_shapes(s8)
    set_text(sh8['Rectangle 6'], "UNIT 1", font_size=11, bold=True, color=NAVY)
    set_text(sh8['Rectangle 1'], "Exploratory analysis and preprocessing", font_size=20, bold=True, color=DARK)

    remove_shape(s8, 'Rectangle 3')
    if os.path.exists("reports/presentation_figures/eda_chart1.png"):
        s8.shapes.add_picture("reports/presentation_figures/eda_chart1.png", 609600, 1750000, width=5300000, height=2300000)
    if os.path.exists("reports/presentation_figures/eda_chart2.png"):
        s8.shapes.add_picture("reports/presentation_figures/eda_chart2.png", 6150000, 1750000, width=5300000, height=2300000)

    sh8['Rectangle 4'].top = 4150000
    sh8['Rectangle 4'].height = 800000
    set_text(sh8['Rectangle 4'],
        "Key findings: (1) Gig tenure < 12 months displays a 2.3× higher default rate than tenure > 36 months. (2) Income volatility index > 0.4 "
        "correlates strongly with delinquency (Mann-Whitney p < 0.001); the top risk decile defaults at 23% (2.9× lift over baseline).",
        font_size=10, color=DARK)

    sh8['Rectangle 5'].top = 5000000
    sh8['Rectangle 5'].height = 800000
    set_text(sh8['Rectangle 5'],
        "Preparation: KNN imputation for missing ages; IQR winsorization on skewed financial values; ordinal encoding (education, location); "
        "one-hot encoding (gig platform); 14 engineered features (income volatility, utility reliability, savings buffer, trend slope); VIF < 5; WoE/IV screen.",
        font_size=10, color=DARK)

    add_takeaway(s8, "Alternative cash-flow stability and utility discipline carry significant predictive power for thin-file applicants.")

    # ---------------------------------------------------------------------
    # SLIDE 9: Unit 2 Predictive Modelling and Final Evaluation
    # ---------------------------------------------------------------------
    s9 = prs.slides[8]
    sh9 = get_shapes(s9)
    set_text(sh9['Rectangle 6'], "UNIT 2", font_size=11, bold=True, color=NAVY)
    set_text(sh9['Rectangle 1'], "Predictive modelling and final evaluation", font_size=20, bold=True, color=DARK)

    # Left: Table + Text cards (width = 5,400,000), Right: ML Model Comparison Plot (width = 5,382,400)
    t9 = sh9['Table 3'].table
    sh9['Table 3'].left = 609600
    sh9['Table 3'].top = 1750000
    sh9['Table 3'].width = 5400000
    set_col_widths(t9, [2200000, 1100000, 1000000, 1100000])
    set_row_heights(t9, 26)

    set_cell(t9, 0, 0, "Model Architecture", font_size=9, bold=True, color=WHITE)
    set_cell(t9, 0, 1, "AUC-ROC", font_size=9, bold=True, color=WHITE)
    set_cell(t9, 0, 2, "PR-AUC", font_size=9, bold=True, color=WHITE)
    set_cell(t9, 0, 3, "Recall / F1", font_size=9, bold=True, color=WHITE)

    set_cell(t9, 1, 0, "Tuned XGBoost [BEST]", font_size=8.5, bold=True, color=NAVY)
    set_cell(t9, 1, 1, "0.738 (85% Max)", font_size=8.5, bold=True)
    set_cell(t9, 1, 2, "0.204", font_size=8.5, bold=True)
    set_cell(t9, 1, 3, "0.682 / 0.247", font_size=8.5, bold=True)

    set_cell(t9, 2, 0, "Tuned LGBM / Logistic Reg.", font_size=8.5)
    set_cell(t9, 2, 1, "0.735 / 0.728", font_size=8.5)
    set_cell(t9, 2, 2, "0.201 / 0.197", font_size=8.5)
    set_cell(t9, 2, 3, "0.614 / 0.256", font_size=8.5)

    sh9['Rectangle 4'].left = 609600
    sh9['Rectangle 4'].width = 5400000
    sh9['Rectangle 4'].top = 2950000
    sh9['Rectangle 4'].height = 1350000
    set_text(sh9['Rectangle 4'],
        "Evaluation setup: Target = loan_default_status (7.87% positive class). Chronological 80/20 train/test split (24,000 train / 6,000 held-out test). "
        "SMOTE applied inside imblearn pipeline during 5-fold stratified CV only to prevent synthetic leakage. Oracle ceiling AUC = 0.781.",
        font_size=9, color=DARK)

    sh9['Rectangle 5'].left = 609600
    sh9['Rectangle 5'].width = 5400000
    sh9['Rectangle 5'].top = 4450000
    sh9['Rectangle 5'].height = 1350000
    set_text(sh9['Rectangle 5'],
        "Selected model & cutoff: Tuned XGBoost captures 85.3% of achievable discrimination. At INR cost-optimal threshold (missed default cost ₹81.9k "
        "vs wrong rejection ₹9.7k): 74.7% approved with an approved default rate of only 4.4% (vs 7.87% baseline). Top SHAP drivers: gig tenure, income trend, utility reliability.",
        font_size=9, color=DARK)

    # Insert ML model comparison graphic on right
    if os.path.exists("reports/presentation_figures/ml_model_comparison.png"):
        s9.shapes.add_picture("reports/presentation_figures/ml_model_comparison.png", 6200000, 1750000, width=5382400, height=4000000)

    add_takeaway(s9, "Tuned XGBoost captures 85% of theoretical discrimination; cost-optimal cutoff slashes approved default rates by 44%.")

    # ---------------------------------------------------------------------
    # SLIDE 10: Unit 3 Selected Advanced Analytics Methods
    # ---------------------------------------------------------------------
    s10 = prs.slides[9]
    sh10 = get_shapes(s10)
    set_text(sh10['Rectangle 5'], "UNIT 3", font_size=11, bold=True, color=NAVY)
    set_text(sh10['Rectangle 1'], "Selected advanced analytics methods", font_size=20, bold=True, color=DARK)

    t10 = sh10['Table 3'].table
    set_col_widths(t10, [3000000, 3972800, 4000000])
    set_cell(t10, 0, 0, "Selected Method", font_size=10, bold=True, color=WHITE)
    set_cell(t10, 0, 1, "Business Question Answered", font_size=10, bold=True, color=WHITE)
    set_cell(t10, 0, 2, "Data Fields & Subsets Used", font_size=10, bold=True, color=WHITE)

    set_cell(t10, 1, 0, "Method 1: Time-Series Portfolio Forecasting", font_size=9.5, bold=True, color=DARK)
    set_cell(t10, 1, 1, "When will portfolio defaults rise, and by how much under macroeconomic stress scenarios?", font_size=9.5)
    set_cell(t10, 1, 2, "72 monthly portfolio default rates (2019–2024) + 7 live macro indicators from FRED & World Bank APIs (108 monthly observations).", font_size=9)

    set_cell(t10, 2, 0, "Method 2: Association Rule Mining", font_size=9.5, bold=True, color=DARK)
    set_cell(t10, 2, 1, "Which specific combinations of alternative borrower behaviors signal severe delinquency risk?", font_size=9.5)
    set_cell(t10, 2, 2, "19 discretized behavioral flags across 24,000 training borrowers (cash-flow trend, volatility, utility delays, savings buffer).", font_size=9)

    sh10['Table 3'].top = 1950000
    sh10['Table 3'].height = 2500000

    sh10['Rectangle 4'].top = 4750000
    sh10['Rectangle 4'].height = 950000
    set_text(sh10['Rectangle 4'],
        "Methodology rationale: Method 1 provides top-down portfolio loss forecasting to quantify capital buffers; Method 2 provides bottom-up "
        "conjunctive warning patterns that catch localized risk that ML gradients smooth over. Both methods directly feed the underwriter dashboard.",
        font_size=10, color=DARK)

    add_takeaway(s10, "Two complementary advanced methods: macro portfolio risk horizon (Method 1) combined with granular behavioral traps (Method 2).")

    # ---------------------------------------------------------------------
    # SLIDE 11: Unit 3 Method 1 Implementation (Time Series)
    # ---------------------------------------------------------------------
    s11 = prs.slides[10]
    sh11 = get_shapes(s11)
    set_text(sh11['Rectangle 7'], "UNIT 3", font_size=11, bold=True, color=NAVY)
    set_text(sh11['Rectangle 1'], "Method 1 implementation: SARIMAX with macro drivers", font_size=20, bold=True, color=DARK)

    for rect_name, top, h in [('Rectangle 3', 1800000, 750000), ('Rectangle 4', 2600000, 1100000), ('Rectangle 5', 3750000, 1050000), ('Rectangle 6', 4850000, 950000)]:
        sh11[rect_name].left = 609600
        sh11[rect_name].width = 5300000
        sh11[rect_name].top = top
        sh11[rect_name].height = h

    set_text(sh11['Rectangle 3'],
        "Selected method: Time-Series Forecasting using SARIMAX with exogenous macroeconomic regressors to forecast portfolio default rates "
        "and quantify Expected Credit Loss (ECL) under stress.", font_size=9.5, color=DARK)

    set_text(sh11['Rectangle 4'],
        "Input & preparation: 72 monthly default rates (2019–2024). ADF and KPSS tests confirmed non-stationarity in levels; stationary after first-order "
        "differencing (d=1, p < 0.001). STL decomposition isolated 12-month seasonality & COVID disruption. Granger causality verified unemployment (p=0.008), "
        "call money (p=0.019), and CPI (p=0.024) lead defaults by 2 months.", font_size=9.5, color=DARK)

    set_text(sh11['Rectangle 5'],
        "Implementation: SARIMAX(1,1,1)(1,1,1,12) with 4 macro regressors (unemployment rate, CPI inflation, call-money rate, COVID lockdown dummy). "
        "Benchmarked against 6 alternatives (Gradient Boosting, Holt-Winters, SARIMA, Seasonal Naive, STL+ETS, STL+ARIMA) across 40-origin expanding-window backtests.",
        font_size=9.5, color=DARK)

    set_text(sh11['Rectangle 6'],
        "Output: SARIMAX achieves lowest hold-out error (MAE 0.054 pp, MAPE 16%). Macro effects: unemployment +1 pp → +21% defaults; CPI +1 pp → +15%; "
        "COVID lockdown → 5.7× default surge. Residuals are white noise (Ljung-Box p=0.12).", font_size=9.5, color=DARK)

    if os.path.exists("reports/presentation_figures/ts_historical_trend.png"):
        s11.shapes.add_picture("reports/presentation_figures/ts_historical_trend.png", 6100000, 1800000, width=5400000, height=3950000)

    add_takeaway(s11, "First-order differencing and Granger-causal macro regressors deliver stationary, lead-indicator forecasting power.")

    # ---------------------------------------------------------------------
    # SLIDE 12: Unit 3 Method 1 Evaluation and Scenarios
    # ---------------------------------------------------------------------
    s12 = prs.slides[11]
    sh12 = get_shapes(s12)
    set_text(sh12['Rectangle 6'], "UNIT 3", font_size=11, bold=True, color=NAVY)
    set_text(sh12['Rectangle 1'], "Method 1 evaluation and macro stress scenarios", font_size=20, bold=True, color=DARK)

    t12 = sh12['Table 3'].table
    sh12['Table 3'].left = 609600
    sh12['Table 3'].width = 5300000
    sh12['Table 3'].top = 1800000
    set_col_widths(t12, [2200000, 1000000, 1000000, 1100000])
    set_row_heights(t12, 26)

    set_cell(t12, 0, 0, "Model Architecture", font_size=9, bold=True, color=WHITE)
    set_cell(t12, 0, 1, "Hold-out MAE", font_size=9, bold=True, color=WHITE)
    set_cell(t12, 0, 2, "MAPE %", font_size=9, bold=True, color=WHITE)
    set_cell(t12, 0, 3, "Backtest MAE", font_size=9, bold=True, color=WHITE)

    set_cell(t12, 1, 0, "SARIMAX + Macro [BEST]", font_size=8.5, bold=True, color=NAVY)
    set_cell(t12, 1, 1, "0.054 pp", font_size=8.5, bold=True)
    set_cell(t12, 1, 2, "16.4%", font_size=8.5, bold=True)
    set_cell(t12, 1, 3, "0.124 pp", font_size=8.5, bold=True)

    set_cell(t12, 2, 0, "Gradient Boosting / Holt-Winters", font_size=8.5)
    set_cell(t12, 2, 1, "0.063 / 0.075", font_size=8.5)
    set_cell(t12, 2, 2, "21.2% / 23.9%", font_size=8.5)
    set_cell(t12, 2, 3, "— / 0.208", font_size=8.5)

    if os.path.exists("reports/presentation_figures/ts_scenarios_ecl.png"):
        s12.shapes.add_picture("reports/presentation_figures/ts_scenarios_ecl.png", 6150000, 1800000, width=5350000, height=2300000)

    sh12['Rectangle 4'].top = 4200000
    sh12['Rectangle 4'].height = 750000
    set_text(sh12['Rectangle 4'],
        "Evaluation data & validation: 60 training months (2019–2023), 12 held-out test months (2024). 40-origin expanding-window backtest validates "
        "stability across regimes. Ljung-Box test confirms white-noise residuals (p = 0.12). 80% prediction interval covers 91.7% of actual 2024 observations.",
        font_size=9.5, color=DARK)

    sh12['Rectangle 5'].top = 5050000
    sh12['Rectangle 5'].height = 750000
    set_text(sh12['Rectangle 5'],
        "Translating forecasts into capital (ECL in ₹): Baseline Scenario (0.28% avg monthly default rate) → ₹1.59 Crore ECL. "
        "Adverse Scenario (Unemployment +1.5 pp, GDP -3 pp) → ₹1.95 Crore ECL (+₹36 Lakhs capital overlay). "
        "Severe Scenario (COVID-scale shock) → ₹4.32 Crore ECL (+₹2.74 Crore capital buffer).",
        font_size=9.5, color=DARK)

    add_takeaway(s12, "SARIMAX with live macro APIs beats all baselines; stress scenarios translate rates into actionable capital buffers in ₹ Crore.")

    # ---------------------------------------------------------------------
    # SLIDE 13: Unit 3 Method 2 Implementation (ARM)
    # ---------------------------------------------------------------------
    s13 = prs.slides[12]
    sh13 = get_shapes(s13)
    set_text(sh13['Rectangle 7'], "UNIT 3", font_size=11, bold=True, color=NAVY)
    set_text(sh13['Rectangle 1'], "Method 2 implementation: Delinquency rule mining", font_size=20, bold=True, color=DARK)

    for rect_name, top, h in [('Rectangle 3', 1800000, 750000), ('Rectangle 4', 2600000, 1050000), ('Rectangle 5', 3700000, 1100000), ('Rectangle 6', 4850000, 950000)]:
        sh13[rect_name].left = 609600
        sh13[rect_name].width = 5300000
        sh13[rect_name].top = top
        sh13[rect_name].height = h

    set_text(sh13['Rectangle 3'],
        "Selected method: Association Rule Mining (Apriori vs FP-Growth) to discover specific conjunctive combinations of borrower "
        "behaviors (income volatility, utility delays, low savings) that signal high delinquency risk, complementing the ML default probability.",
        font_size=9.5, color=DARK)

    set_text(sh13['Rectangle 4'],
        "Input and preparation: 19 behavioral flags discretized across 24,000 training borrowers (DECLINING_INCOME, INCOME_VOLATILE, "
        "LOW_SAVINGS_BUFFER, HIGH_BNPL_USAGE, UTILITY_DELAY_HIGH, LOW_DIGITAL_ACTIVITY, RURAL_LOCATION, NEW_GIG_TENURE). Structured as dense binary itemsets.",
        font_size=9.5, color=DARK)

    set_text(sh13['Rectangle 5'],
        "Implementation: Apriori vs FP-Growth (mlxtend) with min_support = 0.5%. Both algorithms discover identical 2,852 frequent itemsets. "
        "Apriori executed faster (0.62s vs 1.13s) due to low array overhead on dense binary structures. Multi-stage pruning: Confidence ≥ 15%, "
        "Lift ≥ 1.50, Bonferroni-corrected Fisher exact p < 0.05, and subset redundancy removal → 93 high-conviction warning rules.",
        font_size=9.5, color=DARK)

    set_text(sh13['Rectangle 6'],
        "Output: 93 validated delinquency rules. Top rule: DECLINING_INCOME ∧ INCOME_VOLATILE ∧ LOW_SAVINGS_BUFFER → DEFAULT (24.7% default rate, "
        "3.14× lift). Routing applicants with ≥ 3 rules to manual review flags 14% of volume and catches 34% of all portfolio defaults.",
        font_size=9.5, color=DARK)

    # Insert ARM runtime comparison plot on right
    if os.path.exists("reports/presentation_figures/arm_runtime_benchmark.png"):
        s13.shapes.add_picture("reports/presentation_figures/arm_runtime_benchmark.png", 6100000, 1800000, width=5400000, height=3950000)

    add_takeaway(s13, "Rigorous statistical pruning and held-out validation eliminate spurious rules and prevent false alarms.")

    # ---------------------------------------------------------------------
    # SLIDE 14: Unit 3 Method 2 Evaluation and Interpretation
    # ---------------------------------------------------------------------
    s14 = prs.slides[13]
    sh14 = get_shapes(s14)
    set_text(sh14['Rectangle 6'], "UNIT 3", font_size=11, bold=True, color=NAVY)
    set_text(sh14['Rectangle 1'], "Method 2 evaluation and delinquency patterns", font_size=20, bold=True, color=DARK)

    t14 = sh14['Table 3'].table
    sh14['Table 3'].top = 1750000
    set_col_widths(t14, [5000000, 1800000, 1900000, 2272800])
    set_row_heights(t14, 26)

    set_cell(t14, 0, 0, "Top Validated Delinquency Rules (Antecedents → Default)", font_size=9, bold=True, color=WHITE)
    set_cell(t14, 0, 1, "Confidence", font_size=9, bold=True, color=WHITE)
    set_cell(t14, 0, 2, "Train Lift", font_size=9, bold=True, color=WHITE)
    set_cell(t14, 0, 3, "Test Lift (Held-out)", font_size=9, bold=True, color=WHITE)

    set_cell(t14, 1, 0, "DECLINING_INCOME + INCOME_VOLATILE + LOW_SAVINGS_BUFFER", font_size=8.5, bold=True)
    set_cell(t14, 1, 1, "24.7%", font_size=8.5)
    set_cell(t14, 1, 2, "3.14×", font_size=8.5)
    set_cell(t14, 1, 3, "3.14× [100% Generalization]", font_size=8.5, bold=True, color=GREEN)

    set_cell(t14, 2, 0, "INCOME_VOLATILE + LOW_SAVINGS_BUFFER + NEW_GIG_TENURE", font_size=8.5, bold=True)
    set_cell(t14, 2, 1, "24.5%", font_size=8.5)
    set_cell(t14, 2, 2, "3.11×", font_size=8.5)
    set_cell(t14, 2, 3, "3.11× [100% Generalization]", font_size=8.5, bold=True, color=GREEN)

    remove_shape(s14, 'Rectangle 4')
    if os.path.exists("reports/presentation_figures/arm_rules_chart.png"):
        s14.shapes.add_picture("reports/presentation_figures/arm_rules_chart.png", 609600, 3350000, width=10972800, height=1950000)

    sh14['Rectangle 5'].top = 5350000
    sh14['Rectangle 5'].height = 500000
    set_text(sh14['Rectangle 5'],
        "Evaluation summary: 100% of the 93 rules generalize on 6,000 unseen test borrowers (Test Lift ≥ 1.30×). Triggered rules create a 5× risk spread "
        "(0 rules → 4.9% default; ≥ 6 rules → 24.7% default).", font_size=9.5, bold=True, color=NAVY)

    add_takeaway(s14, "All 93 rules hold on unseen test borrowers; triggering 6+ rules signals a 5x surge in delinquency probability.")

    # ---------------------------------------------------------------------
    # SLIDE 15: Business Outcomes & Combined Insights
    # ---------------------------------------------------------------------
    s15 = prs.slides[14]
    sh15 = get_shapes(s15)
    set_text(sh15['Rectangle 5'], "BUSINESS OUTCOMES", font_size=11, bold=True, color=NAVY)
    set_text(sh15['Rectangle 1'], "Combined insights and recommendations", font_size=20, bold=True, color=DARK)

    # Left: Table 3 (width = 5,500,000), Right: Heatmap Image (width = 5,282,400)
    t15 = sh15['Table 3'].table
    sh15['Table 3'].left = 609600
    sh15['Table 3'].width = 5500000
    sh15['Table 3'].top = 1800000
    set_col_widths(t15, [1800000, 1900000, 1800000])
    set_row_heights(t15, 26)

    set_cell(t15, 0, 0, "Evidence from the Project", font_size=8.5, bold=True, color=WHITE)
    set_cell(t15, 0, 1, "Recommended Underwriting Action", font_size=8.5, bold=True, color=WHITE)
    set_cell(t15, 0, 2, "Expected Financial Benefit", font_size=8.5, bold=True, color=WHITE)

    set_cell(t15, 1, 0,
        "Rules detect risk ML PD misses: In Band A (<3%), ≥ 6 rules defaults at 5.6% vs 1.8% with 0 rules (3.1× spread).",
        font_size=8)
    set_cell(t15, 1, 1,
        "Two-tier underwriting: Auto-approve Bands A–B (<3 rules); conditional review for ≥ 3 rules; decline Bands D–E.",
        font_size=8)
    set_cell(t15, 1, 2,
        "Reduces approved defaults from 7.87% to 4.4%. Route 14% to manual review to catch 34% of defaults.",
        font_size=8)

    set_cell(t15, 2, 0,
        "SARIMAX forecasts default surges under macro stress. Point-in-Time multiplier converts TTC PD to macro state.",
        font_size=8)
    set_cell(t15, 2, 1,
        "Dynamic policy: Auto-contract approvals from 75% (baseline) to 48% (severe) under same break-even rule.",
        font_size=8)
    set_cell(t15, 2, 2,
        "Avoids catastrophic wave; protects ₹2.74 Cr in severe shocks while maintaining lending in benign cycles.",
        font_size=8)

    if os.path.exists("reports/presentation_figures/combined_heatmap.png"):
        s15.shapes.add_picture("reports/presentation_figures/combined_heatmap.png", 6300000, 1800000, width=5282400, height=3500000)

    sh15['Rectangle 4'].top = 5420000
    sh15['Rectangle 4'].height = 420000
    set_text(sh15['Rectangle 4'],
        "Business objective addressed: IntelliCredit answers WHO will default (ML), WHICH behavioral patterns signal delinquency (rules), "
        "WHEN defaults will surge (SARIMAX), and WHAT the underwriter should do now (dashboard).", font_size=9.5, bold=True, color=NAVY)

    add_takeaway(s15, "Synthesizing ML PD, warning rules, and macro multipliers yields an automated, macro-resilient credit underwriting engine.")

    # ---------------------------------------------------------------------
    # SLIDE 16: Mandatory Live Demonstration
    # ---------------------------------------------------------------------
    s16 = prs.slides[15]
    sh16 = get_shapes(s16)
    set_text(sh16['Rectangle 7'], "MANDATORY LIVE DEMONSTRATION", font_size=11, bold=True, color=NAVY)
    set_text(sh16['Rectangle 1'], "Interactive dashboard or website", font_size=20, bold=True, color=DARK)

    for rn in ['Rectangle 3', 'Rectangle 4', 'Rectangle 5', 'Rectangle 6']:
        remove_shape(s16, rn)

    if os.path.exists("reports/screenshots/dash_underwriter.png"):
        s16.shapes.add_picture("reports/screenshots/dash_underwriter.png", 609600, 1750000, width=5300000, height=2700000)
    if os.path.exists("reports/screenshots/dash_portfolio.png"):
        s16.shapes.add_picture("reports/screenshots/dash_portfolio.png", 6100000, 1750000, width=5300000, height=2700000)

    tb_left = s16.shapes.add_textbox(609600, 4550000, 5300000, 1300000)
    tf_l = tb_left.text_frame
    tf_l.word_wrap = True
    p1 = tf_l.paragraphs[0]
    p1.text = "Application & Live Demo Flow:"
    p1.font.bold = True
    p1.font.size = Pt(10)
    p1.font.color.rgb = RGBColor(*NAVY)

    p2 = tf_l.add_paragraph()
    p2.text = "• Production Streamlit Dashboard (dashboard/app.py) & Standalone Plotly HTML (reports/interactive_dashboard.html).\n" \
              "• Flow: (1) Select applicant or adjust sliders; (2) Inspect real-time TreeSHAP waterfall explaining risk; (3) Review active delinquency badges; (4) Toggle macro scenarios."
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = RGBColor(*DARK)

    tb_right = s16.shapes.add_textbox(6100000, 4550000, 5300000, 1300000)
    tf_r = tb_right.text_frame
    tf_r.word_wrap = True
    p3 = tf_r.paragraphs[0]
    p3.text = "Underwriting Business Scenario:"
    p3.font.bold = True
    p3.font.size = Pt(10)
    p3.font.color.rgb = RGBColor(*NAVY)

    p4 = tf_r.add_paragraph()
    p4.text = "• Delivery worker earning ₹18,000/mo (8 mos tenure, 3 warning rules) applies for ₹50,000 loan.\n" \
              "• Baseline economy: Approved conditionally with micro-ticket.\n" \
              "• Adverse shock: Automatically declined as macro multiplier pushes PiT PD past break-even threshold."
    p4.font.size = Pt(8.5)
    p4.font.color.rgb = RGBColor(*DARK)

    add_takeaway(s16, "A fully operational loan underwriting cockpit enabling real-time, explainable, and macro-aware credit decisions.")

    # ---------------------------------------------------------------------
    # SLIDE 17: 100% Project Implementation & Contributions
    # ---------------------------------------------------------------------
    s17 = prs.slides[16]
    sh17 = get_shapes(s17)
    set_text(sh17['Rectangle 5'], "100% PROJECT IMPLEMENTATION", font_size=11, bold=True, color=NAVY)
    set_text(sh17['Rectangle 1'], "Completion and individual contribution", font_size=20, bold=True, color=DARK)

    t17 = sh17['Table 3'].table
    sh17['Table 3'].top = 1750000
    set_col_widths(t17, [2800000, 5500000, 2672800])
    set_row_heights(t17, 26)

    set_cell(t17, 0, 0, "Team Member", font_size=9.5, bold=True, color=WHITE)
    set_cell(t17, 0, 1, "Completed Responsibility & Primary Deliverable Scope", font_size=9.5, bold=True, color=WHITE)
    set_cell(t17, 0, 2, "Evidence & Sprint Tasks", font_size=9.5, bold=True, color=WHITE)

    set_cell(t17, 1, 0, "Darun R G (CB.SC.U4CSE23114)", font_size=9, bold=True)
    set_cell(t17, 1, 1, "Data architecture, synthetic data generator (30k borrowers), feature engineering (14 features, WoE/IV), ARM data prep, dataset validation summary & benchmarks.", font_size=8.5)
    set_cell(t17, 1, 2, "data_generation.py, notebooks/01-05, DATASET_VALIDATION_SUMMARY.md; Tasks #2, #3, #6, #13, #18", font_size=8.5)

    set_cell(t17, 2, 0, "Vimalharihar S K (CB.SC.U4CSE23120)", font_size=9, bold=True)
    set_cell(t17, 2, 1, "Lead — Method 1 SARIMAX forecasting (7 models, backtesting, macro APIs) & Method 2 Association Rule Mining (Apriori/FP-Growth, 93 rules, Fisher pruning). Predictive model tuning.", font_size=8.5)
    set_cell(t17, 2, 2, "notebooks/06_R2_M1, 07_R2_M2, src/macro_api.py, models/arm_model_comparison.csv; Tasks #7, #11-#15", font_size=8.5)

    set_cell(t17, 3, 0, "Abhinav Juturu (CB.SC.U4CSE23103)", font_size=9, bold=True)
    set_cell(t17, 3, 1, "Portfolio simulation engine, 72-month DPD migration panel, 38 exploratory data analysis charts, statistical hypothesis testing, scenario loss quantification.", font_size=8.5)
    set_cell(t17, 3, 2, "src/portfolio_simulation.py, notebooks/02_M2, data/portfolio/; Tasks #5, #11", font_size=8.5)

    set_cell(t17, 4, 0, "Gowtham Reddy (CB.SC.U4CSE23119)", font_size=9, bold=True)
    set_cell(t17, 4, 1, "Interactive Streamlit 5-tab application (dashboard/app.py), TreeSHAP waterfall integration, data cleaning/preprocessing, standalone Plotly HTML report.", font_size=8.5)
    set_cell(t17, 4, 2, "dashboard/app.py, notebooks/01_M1, reports/interactive_dashboard.html; Tasks #4, #16, #17", font_size=8.5)

    set_cell(t17, 5, 0, "Adithya (CB.SC.U4CSE23101)", font_size=9, bold=True)
    set_cell(t17, 5, 1, "Model evaluation & TreeSHAP explainability, combined business insights synthesis, quality assurance audit, technical report & 15-min panel presentation slides.", font_size=8.5)
    set_cell(t17, 5, 2, "notebooks/05_M5, 08_R2, Review_2_Final_Report.md, Review_2_Presentation_Slides.md; Tasks #8, #15, #17, #19", font_size=8.5)

    sh17['Rectangle 4'].top = 5450000
    sh17['Rectangle 4'].height = 380000
    set_text(sh17['Rectangle 4'],
        "Project Board: github.com/Darun1017/credit-scoring-engine (19 tracked tasks)     Repositories: Darun1017/credit-scoring-engine  &  Goldmauler/intellicredit-review2",
        font_size=9.5, bold=True, color=NAVY)

    # ---------------------------------------------------------------------
    # SLIDE 18: Final Project Outcome, Conclusions & Limitations
    # ---------------------------------------------------------------------
    s18 = prs.slides[17]
    sh18 = get_shapes(s18)
    set_text(sh18['Rectangle 7'], "FINAL PROJECT OUTCOME", font_size=11, bold=True, color=NAVY)
    set_text(sh18['Rectangle 1'], "Conclusion and limitations", font_size=20, bold=True, color=DARK)

    set_text(sh18['Rectangle 3'],
        "Main outcome: 100% end-to-end implementation delivered across Units 1, 2, and 3: interpretable ML default prediction (AUC 0.738), "
        "macro-driven portfolio forecasting (SARIMAX, MAE 0.054 pp), 93 validated delinquency warning rules, and a 5-tab live decision dashboard.",
        font_size=10, color=DARK)

    set_text(sh18['Rectangle 4'],
        "Business value: Enables lenders to safely score thin-file borrowers (74.7% approved at 4.4% default rate), provision capital under "
        "macro stress (₹1.59 Cr baseline to ₹4.32 Cr severe), and flag high-risk combinations invisible to ML alone (≥ 6 rules → 5× default rate).",
        font_size=10, color=DARK)

    set_text(sh18['Rectangle 5'],
        "Honest limitations: Borrowers and transactions are synthetic (validated against MFIN, PLFS, RBI benchmarks); FRED CPI ends March 2025; "
        "rules are associative, not causal; SMOTE models overstate raw PD (dashboard resolves this via separately calibrated model).",
        font_size=10, color=DARK)

    set_text(sh18['Rectangle 6'],
        "Future scope: Ingest live UPI transaction streams, connect to RBI CRILC / Account Aggregator framework, calibrate PiT multipliers "
        "against empirical economic cycles, and deploy on cloud microservices.",
        font_size=10, color=DARK)

    add_takeaway(s18, "IntelliCredit proves that alternative behavioral data and macroeconomic intelligence can safely expand credit inclusion.")

    # ---------------------------------------------------------------------
    # Global Slide Numbering Verification (Slides 01 to 18)
    # ---------------------------------------------------------------------
    for i, slide in enumerate(prs.slides):
        sh_dict = get_shapes(slide)
        if 'Rectangle 2' in sh_dict:
            set_text(sh_dict['Rectangle 2'], f"{i+1:02d}", font_size=10, bold=False, color=GRAY, alignment=PP_ALIGN.RIGHT)

    # ---------------------------------------------------------------------
    # Save Presentation
    # ---------------------------------------------------------------------
    prs.save(PPT_PATH)
    print(f"[SUCCESS] Presentation successfully written to {PPT_PATH}")
    print(f"Total slides: {len(prs.slides)}")


if __name__ == '__main__':
    main()
