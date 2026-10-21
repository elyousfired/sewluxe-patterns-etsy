#!/usr/bin/env python3
"""
retheme_tailornova_sewing_tips.py
=================================
Transforms the original 11-page Tailornova Sewing Tips section (Pages 17–27)
into the luxury SewLuxePatterns Atelier Edition:
- Page 1: Bespoke SewLuxe Title & Table of Contents Cover
- Pages 2–10: 100% Vector Fidelity Original Diagrams & Instructions with
  SewLuxe Alabaster Palette (#FAF8F5), Running Headers, Footers, and Luxury Framing.
- Page 11: Personal Tailoring Notes & Project Log.

Output:
  C:\\Users\\red1e\\Desktop\\SewLuxe_Elastic_Wide_Leg_Pants\\07_Customer_Delivery_Guide\\SewLuxe_Complete_Sewing_Tips_Guide.pdf
"""

import os
import pymupdf

# Paths
ORIG_PDF = r"C:\Users\red1e\Desktop\SewLuxe_Elastic_Wide_Leg_Pants\02_Sewing_Instructions\Tailornova_Official_Sewing_Instructions_27_Pages.pdf"
FONTS_DIR = r"C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\fonts"
OUT_PDF_DESKTOP = r"C:\Users\red1e\Desktop\SewLuxe_Elastic_Wide_Leg_Pants\07_Customer_Delivery_Guide\SewLuxe_Complete_Sewing_Tips_Guide.pdf"
OUT_PDF_BRAIN = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0\SewLuxe_Complete_Sewing_Tips_Guide.pdf"
PREVIEW_DIR = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\06_sewing_tips_engine\preview_pages"

# Fonts
POPPINS_BOLD = os.path.join(FONTS_DIR, "Poppins-Bold.ttf")
POPPINS_MED = os.path.join(FONTS_DIR, "Poppins-Medium.ttf")
POPPINS_REG = os.path.join(FONTS_DIR, "Poppins-Regular.ttf")
LORA_BOLD = os.path.join(FONTS_DIR, "Lora-Bold.ttf")
LORA_REG = os.path.join(FONTS_DIR, "Lora-Regular.ttf")
LORA_IT = os.path.join(FONTS_DIR, "Lora-Italic.ttf")

# Color Palette (RGB tuples 0.0 - 1.0)
COLOR_BG = (250/255, 248/255, 245/255)         # #FAF8F5 Alabaster Cream
COLOR_CONTAINER = (245/255, 242/255, 239/255)  # #F5F2EF
COLOR_BORDER = (226/255, 221/255, 216/255)     # #E2DDD8
COLOR_GOLD = (197/255, 168/255, 128/255)       # #C5A880 Warm Gold
COLOR_OLIVE = (45/255, 55/255, 40/255)         # #2D3728 Deep Olive Green
COLOR_MUTED = (124/255, 110/255, 94/255)       # #7C6E5E Muted Warm Taupe
COLOR_TEXT = (40/255, 40/255, 40/255)          # Charcoal Text
COLOR_WHITE = (1.0, 1.0, 1.0)
COLOR_RULE = (220/255, 214/255, 206/255)       # #DCD6CE

# Font objects for measuring widths
font_poppins_bold = pymupdf.Font(fontfile=POPPINS_BOLD)
font_poppins_med = pymupdf.Font(fontfile=POPPINS_MED)
font_poppins_reg = pymupdf.Font(fontfile=POPPINS_REG)
font_lora_bold = pymupdf.Font(fontfile=LORA_BOLD)
font_lora_reg = pymupdf.Font(fontfile=LORA_REG)
font_lora_it = pymupdf.Font(fontfile=LORA_IT)


def draw_centered_text(page, text, y, font_obj, font_file, font_name, font_size, color, min_x=0, max_x=595.28):
    w = font_obj.text_length(text, fontsize=font_size)
    x = min_x + (max_x - min_x - w) / 2
    page.insert_text(pymupdf.Point(x, y), text, fontfile=font_file, fontname=font_name, fontsize=font_size, color=color)
    return x, w


def draw_right_text(page, text, right_x, y, font_obj, font_file, font_name, font_size, color):
    w = font_obj.text_length(text, fontsize=font_size)
    x = right_x - w
    page.insert_text(pymupdf.Point(x, y), text, fontfile=font_file, fontname=font_name, fontsize=font_size, color=color)
    return x, w


def build_cover_page(page):
    """Builds a luxury SewLuxe cover for Page 1."""
    # Underlay background
    page.draw_rect(page.rect, color=None, fill=COLOR_BG, overlay=False)
    
    # Double Luxury Border
    page.draw_rect(pymupdf.Rect(28, 28, 567, 814), color=COLOR_GOLD, width=1.2)
    page.draw_rect(pymupdf.Rect(34, 34, 561, 808), color=COLOR_OLIVE, width=0.6)
    
    # 4 Corner Ornaments (Gold Diamonds)
    for cx, cy in [(31, 31), (564, 31), (31, 811), (564, 811)]:
        page.draw_circle(pymupdf.Point(cx, cy), 2.2, color=COLOR_GOLD, fill=COLOR_GOLD)
        
    # Top Brand Emblem
    draw_centered_text(page, "S E W L U X E   P A T T E R N S", 75, font_poppins_bold, POPPINS_BOLD, "Poppins-Bold", 11, COLOR_OLIVE)
    draw_centered_text(page, "ATELIER SEWING COMPANION · MASTER CONSTRUCTION MANUAL", 92, font_poppins_med, POPPINS_MED, "Poppins-Medium", 7.5, COLOR_MUTED)
    
    # Decorative rule under header
    page.draw_line(pymupdf.Point(235, 105), pymupdf.Point(360, 105), color=COLOR_GOLD, width=1.0)
    page.draw_circle(pymupdf.Point(297.6, 105), 2.0, color=COLOR_GOLD, fill=COLOR_GOLD)
    
    # Hero Title Card
    container_rect = pymupdf.Rect(58, 130, 537, 335)
    page.draw_rect(container_rect, color=COLOR_BORDER, fill=COLOR_CONTAINER, width=1.0)
    
    inner_card = pymupdf.Rect(72, 144, 523, 321)
    page.draw_rect(inner_card, color=COLOR_OLIVE, fill=COLOR_WHITE, width=1.2)
    
    draw_centered_text(page, "ATELIER TECHNIQUE REFERENCE", 172, font_poppins_bold, POPPINS_BOLD, "Poppins-Bold", 8, COLOR_GOLD)
    draw_centered_text(page, "SEWING TIPS", 218, font_lora_bold, LORA_BOLD, "Lora-Bold", 32, COLOR_OLIVE)
    draw_centered_text(page, "& Master Construction Methods", 246, font_lora_it, LORA_IT, "Lora-Italic", 15, (75/255, 95/255, 65/255))
    
    # Title gold accent
    page.draw_line(pymupdf.Point(255, 262), pymupdf.Point(340, 262), color=COLOR_GOLD, width=1.5)
    
    desc_line1 = "A comprehensive visual reference guide to fine garment construction, seam finishing,"
    desc_line2 = "dart manipulation, edge grading, waistline facings, and full lining insertion."
    draw_centered_text(page, desc_line1, 282, font_poppins_reg, POPPINS_REG, "Poppins-Regular", 8, COLOR_MUTED)
    draw_centered_text(page, desc_line2, 296, font_poppins_reg, POPPINS_REG, "Poppins-Regular", 8, COLOR_MUTED)
    draw_centered_text(page, "Margot Elastic Wide-Leg Pants Collection · Tailoring Reference", 312, font_poppins_med, POPPINS_MED, "Poppins-Medium", 7.5, COLOR_OLIVE)
    
    # Table of Contents Card
    toc_rect = pymupdf.Rect(58, 355, 537, 680)
    page.draw_rect(toc_rect, color=COLOR_BORDER, fill=COLOR_WHITE, width=1.0)
    
    draw_centered_text(page, "TABLE OF CONTENTS & MASTER TECHNIQUES", 382, font_poppins_bold, POPPINS_BOLD, "Poppins-Bold", 9.5, COLOR_OLIVE)
    page.draw_line(pymupdf.Point(80, 396), pymupdf.Point(515, 396), color=COLOR_BORDER, width=0.8)
    
    modules = [
        ("01", "SEAM BASICS & EASING TECHNIQUES", "Easestitch, Slipstitch, Topstitch, Gathering, Seam Finishing for Knits", "Page 02"),
        ("02", "PROFESSIONAL SEAM FINISHES", "Pinking Shears, Zigzag, Turned & Stitched Edge, Overlock / Serger", "Page 03"),
        ("03", "CURVED SEAMS & DART MANIPULATION", "Concave/Convex Style Lines, Straight Tapered Darts & Double Fisheye Darts", "Pages 03–04"),
        ("04", "SEAM REDUCTION & PRESSING", "Trimming Corners, Grading Layers, Notching Inner/Outer Curves, Interfacing", "Pages 04–05"),
        ("05", "LINING INSERTION & WAIST FACINGS", "Waistline Facing Alignment, Clean Joining, Enclosed Seam Allowances", "Pages 06–07"),
        ("06", "NECK FACINGS, ARMHOLES & HEMS", "Lining to Neck & Armholes, Double-Fold Hemming, Concealed Zipper Finish", "Pages 08–10"),
    ]
    
    y_start = 422
    for num, title, desc, pnum in modules:
        # Number badge
        page.draw_rect(pymupdf.Rect(80, y_start - 12, 102, y_start + 10), color=COLOR_GOLD, fill=COLOR_CONTAINER, width=0.6)
        draw_centered_text(page, num, y_start + 3, font_poppins_bold, POPPINS_BOLD, "Poppins-Bold", 8.5, COLOR_OLIVE, min_x=80, max_x=102)
        
        # Module Title
        page.insert_text(pymupdf.Point(114, y_start - 1), title, fontfile=POPPINS_BOLD, fontname="Poppins-Bold", fontsize=8.5, color=COLOR_OLIVE)
        # Page Number
        draw_right_text(page, pnum, 515, y_start - 1, font_poppins_med, POPPINS_MED, "Poppins-Medium", 8, COLOR_GOLD)
        
        # Description
        page.insert_text(pymupdf.Point(114, y_start + 12), desc, fontfile=POPPINS_REG, fontname="Poppins-Regular", fontsize=7.5, color=COLOR_MUTED)
        
        # Subtle divider line
        if num != "06":
            page.draw_line(pymupdf.Point(114, y_start + 24), pymupdf.Point(515, y_start + 24), color=(240/255, 236/255, 230/255), width=0.5)
            
        y_start += 42
        
    # TOC Footer Note
    page.draw_line(pymupdf.Point(80, 650), pymupdf.Point(515, 650), color=COLOR_BORDER, width=0.8)
    draw_centered_text(page, "Personal Tailoring Notes & Pattern Modification Log included on Page 11", 667, font_lora_it, LORA_IT, "Lora-Italic", 8, COLOR_MUTED)
    
    # Bottom Brand Footer
    draw_centered_text(page, "·   SEWLUXE PATTERNS   ·", 725, font_poppins_bold, POPPINS_BOLD, "Poppins-Bold", 8.5, COLOR_GOLD)
    draw_centered_text(page, "SewLuxePatterns © 2026 · Personal Home Sewing License · All Rights Reserved", 743, font_poppins_reg, POPPINS_REG, "Poppins-Regular", 7.5, (130/255, 130/255, 130/255))
    draw_centered_text(page, "Authentic Vector Construction Systems · Tailornova Patternfast Standard · High-Definition Print", 758, font_poppins_reg, POPPINS_REG, "Poppins-Regular", 7, (160/255, 160/255, 160/255))


def decorate_content_page(page, page_num, total_pages=11):
    """Applies warm alabaster underlay, running headers, footers, and delicate framing to Pages 2 to 10."""
    # Underlay background
    page.draw_rect(page.rect, color=None, fill=COLOR_BG, overlay=False)
    
    # Subtle margin guide line
    page.draw_rect(pymupdf.Rect(34, 18, 561, 824), color=(232/255, 226/255, 217/255), width=0.5)
    
    # Running Header
    # Separator hairline
    page.draw_line(pymupdf.Point(38, 36), pymupdf.Point(557, 36), color=COLOR_GOLD, width=0.7)
    # Brand left
    page.insert_text(pymupdf.Point(42.5, 27), "SEWLUXE PATTERNS", fontfile=POPPINS_BOLD, fontname="Poppins-Bold", fontsize=8, color=COLOR_OLIVE)
    # Dot ornament
    page.draw_circle(pymupdf.Point(135, 24.5), 1.5, color=COLOR_GOLD, fill=COLOR_GOLD)
    # Subtitle right
    draw_right_text(page, "MASTER SEWING & TAILORING TECHNIQUES", 552.8, 27, font_poppins_med, POPPINS_MED, "Poppins-Medium", 7, COLOR_MUTED)
    
    # Running Footer
    # Separator hairline
    page.draw_line(pymupdf.Point(38, 794), pymupdf.Point(557, 794), color=COLOR_GOLD, width=0.7)
    # Brand left (shortened to prevent collision)
    page.insert_text(pymupdf.Point(42.5, 808), "SewLuxePatterns © 2026", fontfile=POPPINS_REG, fontname="Poppins-Regular", fontsize=7.5, color=(100/255, 110/255, 100/255))
    # Center reference
    draw_centered_text(page, "Margot Collection · Atelier Sewing Reference", 808, font_lora_it, LORA_IT, "Lora-Italic", 7.5, (140/255, 140/255, 140/255))
    # Page right
    draw_right_text(page, f"Page {page_num:02d} of {total_pages:02d}", 552.8, 808, font_poppins_bold, POPPINS_BOLD, "Poppins-Bold", 8, COLOR_OLIVE)


def build_notes_page(page, page_num=11, total_pages=11):
    """Builds a luxury Personal Tailoring Notes page for Page 11."""
    # Underlay background
    page.draw_rect(page.rect, color=None, fill=COLOR_BG, overlay=False)
    
    # Redact original bare "NOTES" text
    page.draw_rect(pymupdf.Rect(40, 40, 300, 75), color=None, fill=COLOR_BG)
    
    # Subtle margin guide line
    page.draw_rect(pymupdf.Rect(34, 18, 561, 824), color=(232/255, 226/255, 217/255), width=0.5)
    
    # Running Header
    page.draw_line(pymupdf.Point(38, 36), pymupdf.Point(557, 36), color=COLOR_GOLD, width=0.7)
    page.insert_text(pymupdf.Point(42.5, 27), "SEWLUXE PATTERNS", fontfile=POPPINS_BOLD, fontname="Poppins-Bold", fontsize=8, color=COLOR_OLIVE)
    page.draw_circle(pymupdf.Point(135, 24.5), 1.5, color=COLOR_GOLD, fill=COLOR_GOLD)
    draw_right_text(page, "PERSONAL TAILORING NOTES & PROJECT LOG", 552.8, 27, font_poppins_med, POPPINS_MED, "Poppins-Medium", 7, COLOR_MUTED)
    
    # Running Footer
    page.draw_line(pymupdf.Point(38, 794), pymupdf.Point(557, 794), color=COLOR_GOLD, width=0.7)
    page.insert_text(pymupdf.Point(42.5, 808), "SewLuxePatterns © 2026", fontfile=POPPINS_REG, fontname="Poppins-Regular", fontsize=7.5, color=(100/255, 110/255, 100/255))
    draw_centered_text(page, "Margot Collection · Atelier Sewing Reference", 808, font_lora_it, LORA_IT, "Lora-Italic", 7.5, (140/255, 140/255, 140/255))
    draw_right_text(page, f"Page {page_num:02d} of {total_pages:02d}", 552.8, 808, font_poppins_bold, POPPINS_BOLD, "Poppins-Bold", 8, COLOR_OLIVE)
    
    # Main Header
    page.insert_text(pymupdf.Point(42.5, 62), "PERSONAL TAILORING NOTES & PROJECT LOG", fontfile=LORA_BOLD, fontname="Lora-Bold", fontsize=16, color=COLOR_OLIVE)
    page.insert_text(pymupdf.Point(42.5, 78), "Record your measurements, fabric behavior, needle choices, and custom fit adjustments.", fontfile=LORA_IT, fontname="Lora-Italic", fontsize=8.5, color=COLOR_MUTED)
    
    # Project Info Box
    card_rect = pymupdf.Rect(42.5, 92, 552.8, 212)
    page.draw_rect(card_rect, color=COLOR_BORDER, fill=COLOR_CONTAINER, width=0.8)
    
    # Inner white sub-card
    inner_rect = pymupdf.Rect(50, 98, 545.3, 206)
    page.draw_rect(inner_rect, color=COLOR_BORDER, fill=COLOR_WHITE, width=0.5)
    
    # Field rows - clean vector lines instead of text underscores
    page.insert_text(pymupdf.Point(60, 118), "Garment / Pattern:", fontfile=POPPINS_BOLD, fontname="Poppins-Bold", fontsize=8, color=COLOR_OLIVE)
    page.insert_text(pymupdf.Point(145, 118), "Margot Elastic Wide-Leg Pants", fontfile=POPPINS_REG, fontname="Poppins-Regular", fontsize=8, color=COLOR_TEXT)
    
    page.insert_text(pymupdf.Point(325, 118), "Pattern Size Cut:", fontfile=POPPINS_BOLD, fontname="Poppins-Bold", fontsize=8, color=COLOR_OLIVE)
    page.draw_line(pymupdf.Point(405, 119), pymupdf.Point(535, 119), color=COLOR_RULE, width=0.6)
    
    page.insert_text(pymupdf.Point(60, 140), "Date Started:", fontfile=POPPINS_BOLD, fontname="Poppins-Bold", fontsize=8, color=COLOR_OLIVE)
    page.draw_line(pymupdf.Point(125, 141), pymupdf.Point(205, 141), color=COLOR_RULE, width=0.6)
    page.insert_text(pymupdf.Point(215, 140), "Date Finished:", fontfile=POPPINS_BOLD, fontname="Poppins-Bold", fontsize=8, color=COLOR_OLIVE)
    page.draw_line(pymupdf.Point(282, 141), pymupdf.Point(365, 141), color=COLOR_RULE, width=0.6)
    
    page.insert_text(pymupdf.Point(375, 140), "Graded Sizes:", fontfile=POPPINS_BOLD, fontname="Poppins-Bold", fontsize=8, color=COLOR_OLIVE)
    page.draw_line(pymupdf.Point(440, 141), pymupdf.Point(535, 141), color=COLOR_RULE, width=0.6)
    
    page.insert_text(pymupdf.Point(60, 162), "Fabric Description:", fontfile=POPPINS_BOLD, fontname="Poppins-Bold", fontsize=8, color=COLOR_OLIVE)
    page.draw_line(pymupdf.Point(150, 163), pymupdf.Point(535, 163), color=COLOR_RULE, width=0.6)
    
    page.insert_text(pymupdf.Point(60, 184), "Needle Type / Size:", fontfile=POPPINS_BOLD, fontname="Poppins-Bold", fontsize=8, color=COLOR_OLIVE)
    page.draw_line(pymupdf.Point(150, 185), pymupdf.Point(275, 185), color=COLOR_RULE, width=0.6)
    page.insert_text(pymupdf.Point(285, 184), "Thread Used:", fontfile=POPPINS_BOLD, fontname="Poppins-Bold", fontsize=8, color=COLOR_OLIVE)
    page.draw_line(pymupdf.Point(350, 185), pymupdf.Point(535, 185), color=COLOR_RULE, width=0.6)
    
    # Ruled Notes Area
    page.insert_text(pymupdf.Point(42.5, 234), "CONSTRUCTION OBSERVATIONS & CUSTOM FIT MODIFICATIONS", fontfile=POPPINS_BOLD, fontname="Poppins-Bold", fontsize=8.5, color=COLOR_OLIVE)
    
    # 21 Ruled horizontal lines
    y_rule = 256
    while y_rule <= 770:
        page.draw_line(pymupdf.Point(42.5, y_rule), pymupdf.Point(552.8, y_rule), color=COLOR_RULE, width=0.5)
        # Left margin guide line for bullet checkboxes
        page.draw_circle(pymupdf.Point(52, y_rule - 4), 1.2, color=COLOR_GOLD, fill=None)
        y_rule += 24.5


def retheme_pdf():
    print("Opening source PDF:", ORIG_PDF)
    src_doc = pymupdf.open(ORIG_PDF)
    assert len(src_doc) >= 27, f"Expected 27 pages, got {len(src_doc)}"
    
    out_doc = pymupdf.open()
    
    # 1. Page 1: Fresh Cover Page
    print("Building Page 1: SewLuxe Title & Table of Contents Cover...")
    p1 = out_doc.new_page(width=595.28, height=841.89)
    build_cover_page(p1)
    
    # 2. Pages 2 to 10: Original Pages 18 to 26 (indices 17 to 25)
    print("Importing & Theming Pages 2 to 10 (Vector Construction Steps)...")
    out_doc.insert_pdf(src_doc, from_page=17, to_page=25)
    
    for page_idx in range(1, 10):
        page_num = page_idx + 1
        page = out_doc[page_idx]
        print(f"  Decorating Page {page_num:02d} of 11...")
        decorate_content_page(page, page_num=page_num, total_pages=11)
        
    # 3. Page 11: Original Page 27 (index 26) - Themed as Personal Tailoring Notes
    print("Importing & Theming Page 11 (Personal Tailoring Notes)...")
    out_doc.insert_pdf(src_doc, from_page=26, to_page=26)
    p11 = out_doc[10]
    build_notes_page(p11, page_num=11, total_pages=11)
    
    # Save output PDF
    os.makedirs(os.path.dirname(OUT_PDF_DESKTOP), exist_ok=True)
    out_doc.save(OUT_PDF_DESKTOP, deflate=True)
    print("Saved Desktop PDF to:", OUT_PDF_DESKTOP)
    
    os.makedirs(os.path.dirname(OUT_PDF_BRAIN), exist_ok=True)
    out_doc.save(OUT_PDF_BRAIN, deflate=True)
    print("Saved Brain PDF to:", OUT_PDF_BRAIN)
    
    # Render all 11 pages as preview images for visual QA
    os.makedirs(PREVIEW_DIR, exist_ok=True)
    brain_dir = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0"
    for i, p in enumerate(out_doc):
        pix = p.get_pixmap(dpi=150)
        preview_path = os.path.join(PREVIEW_DIR, f"page_{i+1:02d}.png")
        pix.save(preview_path)
        brain_preview = os.path.join(brain_dir, f"complete_tips_page_{i+1:02d}.png")
        pix.save(brain_preview)
        print(f"  Rendered preview {i+1:02d}/11 -> {preview_path}")

    print("\n[SUCCESS] Completed SewLuxe Complete Sewing Tips Guide Generation!")


if __name__ == "__main__":
    retheme_pdf()
