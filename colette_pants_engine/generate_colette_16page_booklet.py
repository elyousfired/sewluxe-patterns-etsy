#!/usr/bin/env python3
"""
generate_colette_16page_booklet.py
==================================
Generates the official 16-page Luxury Sewing Instruction Booklet for:
SewLuxe Colette Double-Pleated Palazzo Trousers (Sizes US 00–22).

Complies 100% with the SewLuxe Gold Standard and Argon Benchmark:
- Fonts: Poppins (headings/tables/specs) + Lora (titles/accents)
- Colors: Quiet Luxury Palette (Burgundy #8C3B47 / Warm Sand #F5F2EF / Charcoal #1E1A19 / Gold #C5A880)
- Verified CAD Body & Finished Garment Measurement Tables (all 13 sizes)
- Clickable Video Guides Hub with authentic QR codes on Page 8
- Step-by-Step Construction Panels (Pages 9 to 15) with Gold Standard Framing
- Updated Tailoring Rules: Concealed Trouser Hook & Bar closure, 5 belt loops, double forward pleats,
  razor-sharp center creases, slanted pockets, and deep 5.0 cm (2.0 in) palazzo hem.
- Page 16: Standalone 360° Fit Gallery showcasing the approved 3 editorial photoshoot angles.
"""

import os
import sys
import json
import shutil
import pymupdf as fitz
import sys
sys.path.append(r'C:\Users\red1e\.gemini\antigravity\scratch\etsy\sewluxe_core')
from universal_trouser_engine import TrouserSpec, UniversalTrouserEngine, cm_to_tailor_inches
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

# Directories
ENGINE_DIR = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\colette_pants_engine"
ASSET_DIR = os.path.join(ENGINE_DIR, "booklet_assets")
FONTS_DIR = r"C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\fonts"
BRAIN_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0"

OUT_DESKTOP_BOOKLET = r"C:\Users\red1e\Desktop\SewLuxe_Colette_Tailored_Pants\04_Luxury_Booklet\Colette_Palazzo_Trousers_Sewing_Instructions.pdf"
OUT_DELIVERY_BOOKLET = r"C:\Users\red1e\Desktop\SewLuxe_Colette_Tailored_Pants\07_Customer_Delivery_Guide\Colette_Palazzo_Trousers_Sewing_Instructions.pdf"
OUT_BRAIN_BOOKLET = os.path.join(BRAIN_DIR, "Colette_Palazzo_Trousers_Sewing_Instructions.pdf")

# Images
PHOTO_FRONT = os.path.join(BRAIN_DIR, "colette_palazzo_photo_01_clean_1792601697194.jpg")
PHOTO_SIDE = os.path.join(BRAIN_DIR, "colette_palazzo_photo_02_1792601621750.jpg")
PHOTO_BACK = os.path.join(BRAIN_DIR, "colette_palazzo_photo_03_1792601698005.jpg")

STICKER_FRONT = os.path.join(BRAIN_DIR, "Colette_Sticker_Front.png")
STICKER_BACK = os.path.join(BRAIN_DIR, "Colette_Sticker_Back.png")
FLAT_SKETCH_SIDEBYSIDE = os.path.join(BRAIN_DIR, "Colette_Sketch_SideBySide.png")
PIECES_OVERVIEW = os.path.join(ASSET_DIR, "pieces_overview_clean.png")

# Register Fonts
pdfmetrics.registerFont(TTFont("Poppins", os.path.join(FONTS_DIR, "Poppins-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Medium", os.path.join(FONTS_DIR, "Poppins-Medium.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Bold", os.path.join(FONTS_DIR, "Poppins-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Italic", os.path.join(FONTS_DIR, "Poppins-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Lora", os.path.join(FONTS_DIR, "Lora-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Lora-Bold", os.path.join(FONTS_DIR, "Lora-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Lora-Italic", os.path.join(FONTS_DIR, "Lora-Italic.ttf")))

# Palette
BG_CREAM = HexColor("#FAF8F5")
CONTAINER_BG = HexColor("#F5F2EF")
BORDER_SUBTLE = HexColor("#E2DDD8")
BURGUNDY = HexColor("#8C3B47")
CHARCOAL = HexColor("#1E1A19")
TEXT_BODY = HexColor("#2C2624")
MUTED = HexColor("#6E655F")
RULE_LINE = HexColor("#DFD9D3")
TABLE_HEAD = HexColor("#1E1A19")
TABLE_ALT = HexColor("#F4EFEA")
TIP_BG = HexColor("#F6ECEA")
GOLD = HexColor("#C5A880")
WHITE = white

W, H = A4  # 595.275 x 841.89 pt
M_L = 50.0
M_R = W - 50.0
CONTENT_W = M_R - M_L

def draw_page_bg_and_chrome(c, page_num, is_cover=False):
    c.saveState()
    c.setFillColor(BG_CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    if not is_cover:
        # Running Top Header
        c.setFont("Poppins-Medium", 7.0)
        c.setFillColor(MUTED)
        c.drawString(M_L, H - 36, "COLETTE PALAZZO TROUSERS  ·  SEWING GUIDE")
        c.drawRightString(M_R, H - 36, "SIZES US 00–22")
        c.setStrokeColor(RULE_LINE)
        c.setLineWidth(0.6)
        c.line(M_L, H - 42, M_R, H - 42)
        
        # Running Footer
        c.line(M_L, 46, M_R, 46)
        c.setFont("Lora-Italic", 9.2)
        c.setFillColor(BURGUNDY)
        c.drawString(M_L, 32, "SewLuxePatterns")
        c.setFont("Poppins", 7.8)
        c.setFillColor(MUTED)
        c.drawRightString(M_R, 32, str(page_num))
    c.restoreState()

def draw_section_header(c, kicker, title, y_top=H - 64):
    c.saveState()
    c.setFont("Poppins-Medium", 7.6)
    c.setFillColor(BURGUNDY)
    spaced_kicker = "  ".join(list(kicker.upper()))
    c.drawString(M_L, y_top, spaced_kicker)
    
    y = y_top - 24
    c.setFont("Lora", 24)
    c.setFillColor(CHARCOAL)
    c.drawString(M_L, y, title)
    
    y -= 10
    c.setStrokeColor(BURGUNDY)
    c.setLineWidth(1.6)
    c.line(M_L, y, M_L + 105, y)
    c.restoreState()
    return y - 16

def draw_step_header(c, y, step_num, title, subtitle):
    c.saveState()
    c.setFillColor(BURGUNDY)
    c.circle(M_L + 12, y + 8, 12, fill=1, stroke=0)
    c.setFont("Poppins-Bold", 10.5)
    c.setFillColor(WHITE)
    c.drawCentredString(M_L + 12, y + 4.5, str(step_num))
    
    c.setFont("Lora", 15)
    c.setFillColor(CHARCOAL)
    c.drawString(M_L + 32, y + 2, title)
    
    c.setFont("Poppins", 7.2)
    c.setFillColor(MUTED)
    title_w = pdfmetrics.stringWidth(title, "Lora", 15)
    sub_w = pdfmetrics.stringWidth(subtitle, "Poppins", 7.2)
    if (M_L + 32 + title_w + 15) > (M_R - sub_w):
        y -= 12
        c.drawString(M_L + 32, y + 2, subtitle)
    else:
        c.drawRightString(M_R, y + 4, subtitle)
    
    y -= 10
    c.setStrokeColor(RULE_LINE)
    c.setLineWidth(0.8)
    c.line(M_L, y, M_R, y)
    c.restoreState()
    return y - 14

def draw_bullet(c, x, y, text, max_w, font_size=8.5, leading=12.2):
    style = ParagraphStyle(
        name=f"Bullet_{x}_{y}_{len(text)}",
        fontName="Poppins",
        fontSize=font_size,
        leading=leading,
        textColor=TEXT_BODY
    )
    p = Paragraph(f"• {text}", style)
    w, h = p.wrap(max_w, 200)
    p.drawOn(c, x, y - h)
    return y - h - 5

def draw_tip_box(c, y, title, body_text, width=CONTENT_W):
    style = ParagraphStyle(
        name=f"TipStyle_{y}_{len(body_text)}",
        fontName="Poppins",
        fontSize=7.8,
        leading=11.2,
        textColor=TEXT_BODY
    )
    p = Paragraph(body_text, style)
    w, h = p.wrap(width - 24, 150)
    box_h = max(38.0, h + 24.0)
    
    c.saveState()
    c.setFillColor(TIP_BG)
    c.rect(M_L, y - box_h, width, box_h, fill=1, stroke=0)
    c.setFillColor(BURGUNDY)
    c.rect(M_L, y - box_h, 3.5, box_h, fill=1, stroke=0)
    
    c.setFont("Poppins-Bold", 8.2)
    c.setFillColor(BURGUNDY)
    c.drawString(M_L + 12, y - 12.5, title)
    p.drawOn(c, M_L + 12, y - 12.5 - 4.5 - h)
    c.restoreState()
    return y - box_h - 12

def build_pdf():
    os.makedirs(os.path.dirname(OUT_DESKTOP_BOOKLET), exist_ok=True)
    os.makedirs(os.path.dirname(OUT_DELIVERY_BOOKLET), exist_ok=True)
    os.makedirs(BRAIN_DIR, exist_ok=True)
    
    c = canvas.Canvas(OUT_DESKTOP_BOOKLET, pagesize=A4)
    c.setTitle("Colette Double-Pleated Palazzo Trousers - Sewing Instructions")
    c.setAuthor("SewLuxePatterns")

    # =========================================================================
    # PAGE 1: COVER
    # =========================================================================
    draw_page_bg_and_chrome(c, 1, is_cover=True)
    c.setFont("Poppins-Medium", 7.5)
    c.setFillColor(BURGUNDY)
    c.drawString(82, H - 46, "S E W I N G   P A T T E R N   ·   I N S T R U C T I O N   B O O K L E T")
    
    c.setFont("Lora", 46)
    c.setFillColor(CHARCOAL)
    c.drawString(80, H - 94, "Colette")
    
    c.setFont("Poppins-Medium", 11.0)
    c.setFillColor(BURGUNDY)
    c.drawString(82, H - 118, "P A L A Z Z O   T R O U S E R S")
    
    c.setFont("Lora-Italic", 10.2)
    c.setFillColor(TEXT_BODY)
    c.drawString(82, H - 142, "High-waisted tailored wide-leg trousers with double forward pleats,")
    c.drawString(82, H - 156, "sharp pressed creases, concealed waist closure, 5 belt loops, and slant pockets.")
    
    # Cover Photo (square 405 x 405)
    photo_sz = 405.0
    px = (W - photo_sz) / 2.0
    py = H - 180 - photo_sz
    
    if os.path.exists(PHOTO_FRONT):
        c.setFillColor(WHITE)
        c.rect(px - 6, py - 6, photo_sz + 12, photo_sz + 12, fill=1, stroke=0)
        c.setStrokeColor(BORDER_SUBTLE)
        c.setLineWidth(1)
        c.rect(px - 6, py - 6, photo_sz + 12, photo_sz + 12, fill=0, stroke=1)
        c.drawImage(PHOTO_FRONT, px, py, width=photo_sz, height=photo_sz, preserveAspectRatio=True)
        
    # Overlapping technical flat sketch sticker on bottom-left
    if os.path.exists(STICKER_FRONT):
        stk_w = 110.0
        stk_h = 148.0
        c.drawImage(STICKER_FRONT, px - 12, py - 16, width=stk_w, height=stk_h, preserveAspectRatio=True, mask="auto")
        
    y_spec = py - 24
    c.setStrokeColor(BURGUNDY)
    c.setLineWidth(1.0)
    c.line(82, y_spec, W - 82, y_spec)
    
    cols_x = [82, 165, 280, 415]
    specs_cover = [
        ("S I Z E S", "US 00 – 22 (13 sizes)"),
        ("L E V E L", "Intermediate"),
        ("S E A M   A L L O W A N C E", "1 cm (3/8 in) included"),
        ("F O R M A T S", "A4 · US Letter · A0 · Projector"),
    ]
    for cx_col, (lbl, val) in zip(cols_x, specs_cover):
        c.setFont("Poppins-Medium", 6.5)
        c.setFillColor(BURGUNDY)
        c.drawString(cx_col, y_spec - 14, lbl)
        c.setFont("Poppins", 8.2)
        c.setFillColor(CHARCOAL)
        c.drawString(cx_col, y_spec - 27, val)
        
    c.setFont("Poppins", 6.5)
    c.setFillColor(MUTED)
    c.drawCentredString(W / 2, y_spec - 50, "H E L P F U L   V I D E O   G U I D E S   I N C L U D E D   ·   C L I C K A B L E   L I N K S   A N D   Q R   C O D E S   O N   P A G E   8")
    
    c.setFont("Lora-Italic", 13.5)
    c.setFillColor(BURGUNDY)
    c.drawCentredString(W / 2, 64, "SewLuxePatterns")
    c.showPage()

    # =========================================================================
    # PAGE 2: WELCOME / MEET THE COLETTE TROUSERS
    # =========================================================================
    draw_page_bg_and_chrome(c, 2)
    y = draw_section_header(c, "W E L C O M E", "Meet the Colette Palazzo Trousers")
    
    intro = (
        "Thank you for choosing the <b>Colette Palazzo Trousers</b>. Designed for medium-weight fluid suiting fabrics, "
        "these high-waisted palazzo trousers epitomize modern quiet-luxury tailoring. "
        "Double forward pleats on each leg release smoothly into an expansive, sweeping wide-leg silhouette (60.3 to 92.6 cm hem circumference across sizes), "
        "anchored by razor-sharp pressed vertical center creases and a clean, concealed trouser hook & bar closure."
    )
    p_intro = Paragraph(intro, ParagraphStyle("WelcomeIntro", fontName="Poppins", fontSize=9.0, leading=13.8, textColor=TEXT_BODY))
    w, h = p_intro.wrap(CONTENT_W, 100)
    p_intro.drawOn(c, M_L, y - h)
    y -= (h + 16)
    
    # Left: Flat sketch Side-by-Side, Right: Design features
    sketch_w = 235.0
    sketch_h = 235.0
    if os.path.exists(FLAT_SKETCH_SIDEBYSIDE):
        c.drawImage(FLAT_SKETCH_SIDEBYSIDE, M_L, y - sketch_h, width=sketch_w, height=sketch_h, preserveAspectRatio=True, mask="auto")
        
    rx = M_L + sketch_w + 16
    rw = M_R - rx
    ry = y - 4
    
    c.setFont("Poppins-Medium", 10.0)
    c.setFillColor(BURGUNDY)
    c.drawString(rx, ry, "Key Design & Tailoring Features")
    ry -= 16
    
    features = [
        "High-waisted tailored fit sitting cleanly at the natural waistline.",
        "Double forward pleats on each front leg adding graceful fluid drape.",
        "Razor-sharp pressed vertical center creases running straight to the hem.",
        "Concealed trouser hook & bar closure on inside waistband extension tab.",
        "Zero exterior buttons on front waistband for a sleek, unbroken luxury profile.",
        "5 tailored belt loops: 2 over pleats/creases, 2 over pocket tops, 1 at center back.",
        "Deep Italian slant hip pockets reinforced with stay-tape.",
        "Clean pocketless back shaped with 4 waist darts (2 per side).",
        "Deep weighted 5.0 cm (2.0 in) fold-up hem creating fluid waterfall break."
    ]
    for feat in features:
        ry = draw_bullet(c, rx, ry, feat, rw, font_size=7.6, leading=10.6)
        
    y_bot = y - sketch_h - 18
    c.setFont("Poppins-Medium", 9.8)
    c.setFillColor(BURGUNDY)
    c.drawString(M_L, y_bot, "What is Included in Your Package")
    y_bot -= 14
    
    inc_items = [
        "This complete 16-page illustrated luxury sewing instruction booklet.",
        "Full printable pattern suite in A4, US Letter, and A0 CopyShop across all 13 sizes (US 00 to 22).",
        "Dedicated Multi-Size Layered A0 PDF and Projector File with individual size toggle layers.",
        "Interactive Video Guides Hub with clickable links and direct QR codes (Page 8)."
    ]
    for it in inc_items:
        y_bot = draw_bullet(c, M_L, y_bot, it, CONTENT_W, font_size=7.8, leading=11.2)
    c.showPage()

    # =========================================================================
    # PAGE 3: READ THIS FIRST / BEFORE YOU BEGIN
    # =========================================================================
    draw_page_bg_and_chrome(c, 3)
    y = draw_section_header(c, "READ THIS FIRST", "Before You Begin")
    
    checklist_intro = "Five minutes spent preparing here guarantees a flawless, couture-level finish. Review each point before cutting:"
    p_chk = Paragraph(checklist_intro, ParagraphStyle("CheckIntro", fontName="Poppins", fontSize=8.8, leading=13.0, textColor=TEXT_BODY))
    w, h = p_chk.wrap(CONTENT_W, 60)
    p_chk.drawOn(c, M_L, y - h)
    y -= (h + 16)
    
    chk_cols = [
        ("1. PRINT & CALIBRATE", [
            "Always print Page 1 first at <b>100% Actual Size</b> (uncheck 'Fit to Page').",
            "Measure the 4\" x 4\" (10 cm x 10 cm) test square with a hard physical ruler.",
            "Verify both horizontal and vertical lines match exactly before printing remaining tiles."
        ]),
        ("2. ACCURATE BODY MEASUREMENTS", [
            "Measure in light undergarments at natural waist (narrowest part) and full hip.",
            "If your waist and hip fall between sizes, blend smoothly along side seams.",
            "Check finished garment measurements (Page 4) to verify desired ease."
        ]),
        ("3. FABRIC PREPARATION", [
            "Pre-wash, steam, and shrink your suiting fabric thoroughly before pinning.",
            "Linen-viscose and Tencel blends can shrink 5–8% on first steam pressing.",
            "Press fabric completely flat on the grainline to prevent twisted trouser legs."
        ]),
        ("4. SEAM ALLOWANCES & TOOLS", [
            "Standard <b>1.0 cm (3/8 in)</b> seam allowance is included on all seams.",
            "Generous <b>5.0 cm (2.0 in)</b> fold-up hem is included at leg hems.",
            "Equip your machine with a new 80/12 Microtex needle and quality polyester thread."
        ])
    ]
    
    box_w = (CONTENT_W - 14) / 2.0
    box_h = 135.0
    for idx, (b_title, b_points) in enumerate(chk_cols):
        col = idx % 2
        row = idx // 2
        bx = M_L + col * (box_w + 14)
        by = y - row * (box_h + 16)
        
        c.saveState()
        c.setFillColor(CONTAINER_BG)
        c.setStrokeColor(BORDER_SUBTLE)
        c.setLineWidth(0.8)
        c.roundRect(bx, by - box_h, box_w, box_h, 6, fill=1, stroke=1)
        
        c.setFont("Poppins-Bold", 8.8)
        c.setFillColor(BURGUNDY)
        c.drawString(bx + 12, by - 16, b_title)
        
        by_pt = by - 32
        for pt in b_points:
            p_pt = Paragraph(f"• {pt}", ParagraphStyle(f"Pt_{idx}", fontName="Poppins", fontSize=7.4, leading=10.6, textColor=TEXT_BODY))
            pw, ph = p_pt.wrap(box_w - 24, 70)
            p_pt.drawOn(c, bx + 12, by_pt - ph)
            by_pt -= (ph + 6)
        c.restoreState()
        
    y = y - 2 * (box_h + 16) - 10
    draw_tip_box(c, y, "Gold Standard Tailoring Advice",
                 "Take your time pressing each seam as you sew. In luxury trouser tailoring, 60% of the silhouette is created with the steam iron. A tailor's pressing ham and clapper make all the difference.")
    c.showPage()

    # =========================================================================
    # PAGE 4: CHOOSE YOUR SIZE / SIZE CHARTS
    # =========================================================================
    draw_page_bg_and_chrome(c, 4)
    y = draw_section_header(c, "CHOOSE YOUR SIZE", "Size Charts & Measurements")
    
    p_sz_intro = Paragraph(
        "Measure over light underwear: natural waist at narrowest crease, hips at fullest part. "
        "The Colette palazzo silhouette offers generous ease through the thigh and leg opening with a tailored high waist.",
        ParagraphStyle("SizeIntro", fontName="Poppins", fontSize=8.2, leading=12.0, textColor=TEXT_BODY)
    )
    w, h = p_sz_intro.wrap(CONTENT_W, 40)
    p_sz_intro.drawOn(c, M_L, y - h)
    y -= (h + 14)
    
    # Table 1: Body Measurements
    c.setFont("Poppins-Bold", 9.0)
    c.setFillColor(BURGUNDY)
    c.drawString(M_L, y, "BODY SIZE CHART (ALVANON NORTH AMERICA STANDARD)")
    y -= 14
    
    b_heads = ["US SIZE", "LETTER", "BUST (CM)", "WAIST (CM)", "HIPS (CM)", "WAIST (IN)", "HIPS (IN)"]
    b_widths = [55, 50, 70, 75, 75, 75, 95]
    
    c.setFillColor(TABLE_HEAD)
    c.rect(M_L, y - 14, sum(b_widths), 14, fill=1, stroke=0)
    c.setFont("Poppins-Bold", 6.8)
    c.setFillColor(WHITE)
    cur_x = M_L
    for h_txt, hw in zip(b_heads, b_widths):
        c.drawString(cur_x + 6, y - 10, h_txt)
        cur_x += hw
    y -= 14
    
    body_rows = [
        ("00", "XXS", "80.0", "63.5", "87.75", "25\"", "34 1/2\""),
        ("0",  "XS",  "82.5", "66.0", "90.25", "26\"", "35 1/2\""),
        ("2",  "XS",  "85.0", "68.75", "92.75", "27 1/8\"", "36 1/2\""),
        ("4",  "S",   "87.75", "71.25", "95.25", "28\"", "37 1/2\""),
        ("6",  "S",   "90.25", "73.75", "98.0", "29\"", "38 5/8\""),
        ("8",  "M",   "92.75", "76.25", "100.25", "30\"", "39 1/2\""),
        ("10", "M",   "95.25", "78.75", "102.75", "31\"", "40 1/2\""),
        ("12", "L",   "99.25", "82.75", "106.5", "32 5/8\"", "41 7/8\""),
        ("14", "L",   "104.25", "87.5", "111.0", "34 1/2\"", "43 3/4\""),
        ("16", "XL",  "109.25", "93.25", "115.5", "36 3/4\"", "45 1/2\""),
        ("18", "2XL", "114.25", "99.0", "120.75", "39\"", "47 1/2\""),
        ("20", "3XL", "119.25", "104.75", "125.75", "41 1/4\"", "49 1/2\""),
        ("22", "4XL", "124.25", "110.5", "130.75", "43 1/2\"", "51 1/2\""),
    ]
    
    for r_idx, r_data in enumerate(body_rows):
        bg = TABLE_ALT if r_idx % 2 == 1 else WHITE
        c.setFillColor(bg)
        c.rect(M_L, y - 11.5, sum(b_widths), 11.5, fill=1, stroke=0)
        c.setFont("Poppins", 6.4)
        c.setFillColor(TEXT_BODY)
        cur_x = M_L
        for val, hw in zip(r_data, b_widths):
            c.drawString(cur_x + 6, y - 8.5, val)
            cur_x += hw
        y -= 11.5
        
    y -= 14
    # Table 2: Finished Garment Measurements
    c.setFont("Poppins-Bold", 9.0)
    c.setFillColor(BURGUNDY)
    c.drawString(M_L, y, "FINISHED GARMENT MEASUREMENTS (WITH PLEATS CLOSED)")
    y -= 14
    
    f_heads = ["US SIZE", "FINISHED WAIST", "FINISHED HIPS*", "LEG SWEEP (CIRC.)", "INSEAM / OUTSEAM"]
    f_widths = [65, 105, 105, 110, 110]
    
    c.setFillColor(TABLE_HEAD)
    c.rect(M_L, y - 14, sum(f_widths), 14, fill=1, stroke=0)
    c.setFont("Poppins-Bold", 6.8)
    c.setFillColor(WHITE)
    cur_x = M_L
    for h_txt, hw in zip(f_heads, f_widths):
        c.drawString(cur_x + 6, y - 10, h_txt)
        cur_x += hw
    y -= 14
    
    colette_spec = TrouserSpec(
        model_name="Colette Palazzo Trousers",
        size_standard="US_00_22",
        silhouette="palazzo",
        front_shaping="double_pleats",
        back_shaping="4_darts",
        front_pockets="slant_italian",
        back_pockets="none",
        closure_type="concealed_hook_bar",
        belt_loops_count=5
    )
    ute_engine = UniversalTrouserEngine(colette_spec)
    qa_ok, qa_logs = ute_engine.run_qa_audit()
    if not qa_ok:
        raise ValueError(f"Pre-Flight Trouser QA Audit Failed: {qa_logs}")
    ute_tables = ute_engine.generate_size_tables()
    fin_rows = [
        (r["size"], r["fin_waist"], r["fin_hips"], r["leg_sweep"], f"{r['inseam_outseam']} ({cm_to_tailor_inches(r['_raw'][3])} / {cm_to_tailor_inches(r['_raw'][4])})")
        for r in ute_tables["finished"]
    ]
    for r_idx, r_data in enumerate(fin_rows):
        bg = TABLE_ALT if r_idx % 2 == 1 else WHITE
        c.setFillColor(bg)
        c.rect(M_L, y - 11.5, sum(f_widths), 11.5, fill=1, stroke=0)
        c.setFont("Poppins", 6.4)
        c.setFillColor(TEXT_BODY)
        cur_x = M_L
        for val, hw in zip(r_data, f_widths):
            c.drawString(cur_x + 6, y - 8.5, val)
            cur_x += hw
        y -= 11.5
        
    y -= 8
    c.setFont("Poppins-Italic", 6.8)
    c.setFillColor(MUTED)
    c.drawString(M_L, y, "* Finished waist and hip circumferences measured with front pleats pressed closed. The double pleats provide generous living ease.")
    c.showPage()

    # =========================================================================
    # PAGE 5: MATERIALS / FABRIC & NOTIONS
    # =========================================================================
    draw_page_bg_and_chrome(c, 5)
    y = draw_section_header(c, "MATERIALS", "Fabric Requirements & Notions")
    
    c.setFont("Poppins-Bold", 9.0)
    c.setFillColor(BURGUNDY)
    c.drawString(M_L, y, "RECOMMENDED TEXTILES")
    y -= 12
    
    fab_desc = (
        "Medium-weight woven fabrics with fluid, elegant drape (180–280 gsm / 5.3–8.2 oz): "
        "<b>Washed Linen-Viscose blends, Tencel/Lyocell twill, tropical wool gabardine, cotton-linen cavalry twill, or wool crepe.</b> "
        "The palazzo silhouette relies on fluid, weighty drape that falls effortlessly from hip to floor without stiffness."
    )
    p_fab = Paragraph(fab_desc, ParagraphStyle("FabDesc", fontName="Poppins", fontSize=8.0, leading=11.6, textColor=TEXT_BODY))
    w, h = p_fab.wrap(CONTENT_W, 50)
    p_fab.drawOn(c, M_L, y - h)
    y -= (h + 16)
    
    # Fabric Yardage Table
    c.setFont("Poppins-Bold", 9.0)
    c.setFillColor(BURGUNDY)
    c.drawString(M_L, y, "INTELLIGENT FABRIC REQUIREMENTS TABLE (WITH 10% BUFFER)")
    y -= 14
    
    req_heads = ["SIZE CLUSTER", "60 IN (150 CM) FABRIC WIDTH", "45 IN (115 CM) FABRIC WIDTH"]
    req_widths = [135, 180, 180]
    
    c.setFillColor(TABLE_HEAD)
    c.rect(M_L, y - 14, sum(req_widths), 14, fill=1, stroke=0)
    c.setFont("Poppins-Bold", 7.0)
    c.setFillColor(WHITE)
    cur_x = M_L
    for rh, rw in zip(req_heads, req_widths):
        c.drawString(cur_x + 8, y - 10, rh)
        cur_x += rw
    y -= 14
    
    req_rows = [
        ("Sizes US 00 – 08", "2.60 m (2.85 yards)", "3.40 m (3.75 yards)"),
        ("Sizes US 10 – 14", "2.85 m (3.10 yards)", "3.70 m (4.05 yards)"),
        ("Sizes US 16 – 22", "3.20 m (3.50 yards)", "4.10 m (4.50 yards)"),
    ]
    for r_idx, (sc, w60, w45) in enumerate(req_rows):
        bg = TABLE_ALT if r_idx % 2 == 1 else WHITE
        c.setFillColor(bg)
        c.rect(M_L, y - 16, sum(req_widths), 16, fill=1, stroke=0)
        c.setFont("Poppins-Bold" if r_idx == 0 else "Poppins", 7.2)
        c.setFillColor(TEXT_BODY)
        c.drawString(M_L + 8, y - 11.5, sc)
        c.drawString(M_L + req_widths[0] + 8, y - 11.5, w60)
        c.drawString(M_L + req_widths[0] + req_widths[1] + 8, y - 11.5, w45)
        y -= 16
        
    y -= 16
    c.setFont("Poppins-Bold", 9.0)
    c.setFillColor(BURGUNDY)
    c.drawString(M_L, y, "REQUIRED NOTIONS & HARDWARE")
    y -= 12
    
    notions_list = [
        ("Concealed Trouser Closure", "1x heavy-duty metal trouser hook & bar for inside extension tab + 1x optional 10–12 mm flat inside anchor button."),
        ("Trouser Zipper", "1x nylon coil or metal closed-end trouser zipper, 18–20 cm (7–8 in) long."),
        ("Fusible Interfacing", "0.50 m (1/2 yard) lightweight woven fusible interfacing (for waistband, fly facing, and belt loop reinforcement)."),
        ("Pocket Stay-Tape", "0.50 m (1/2 yard) bias-cut stay-tape or lightweight interfacing strip to stabilize slant pocket openings."),
        ("Pocket Lining Fabric", "0.40 m lightweight cotton lawn, voile, or Bemberg lining for inner pocket bags (Pieces 4 & 6)."),
        ("Sewing Thread", "1 spool quality 100% polyester all-purpose thread matching your main fabric."),
        ("Tailoring Tools", "Zipper foot, steam iron, tailor's ham, press cloth, wooden clapper, and chalk marker.")
    ]
    for n_title, n_desc in notions_list:
        y = draw_bullet(c, M_L, y, f"<b>{n_title}:</b> {n_desc}", CONTENT_W, font_size=7.6, leading=10.8)
        
    y -= 10
    draw_tip_box(c, y, "Pro Tip: Cutting Wide Legs on 45\" Fabric",
                 "Because Colette features ultra-wide palazzo legs, Front and Back leg pieces must be stacked lengthwise when cutting on 45\" (115 cm) width fabric. Always ensure your fabric length accounts for lengthwise nesting.")
    c.showPage()

    # =========================================================================
    # PAGE 6: CUTTING / PATTERN PIECES & CUTTING
    # =========================================================================
    draw_page_bg_and_chrome(c, 6)
    y = draw_section_header(c, "CUTTING", "Pattern Pieces & Cutting Protocol")
    
    c.setFont("Poppins-Bold", 9.0)
    c.setFillColor(BURGUNDY)
    c.drawString(M_L, y, "GARMENT PIECE INVENTORY")
    y -= 14
    
    pw = [35, 145, 165, 150]
    c.setFillColor(TABLE_HEAD)
    c.rect(M_L, y - 14, sum(pw), 14, fill=1, stroke=0)
    c.setFont("Poppins-Bold", 6.8)
    c.setFillColor(WHITE)
    c.drawString(M_L + 6, y - 10, "#")
    c.drawString(M_L + pw[0] + 6, y - 10, "PIECE NAME")
    c.drawString(M_L + pw[0] + pw[1] + 6, y - 10, "MATERIAL")
    c.drawString(M_L + pw[0] + pw[1] + pw[2] + 6, y - 10, "CUT QUANTITY")
    y -= 14
    
    pieces_data = [
        ("1", "Pants Front", "Main Fabric", "Cut 2 (Mirrored Pair)"),
        ("2", "Pants Back", "Main Fabric", "Cut 2 (Mirrored Pair)"),
        ("3", "Waistband", "Main Fabric + Interfacing", "Cut 1 Main + 1 Interfacing"),
        ("4", "Pocket Bag (Outer)", "Main Fabric", "Cut 2 (Mirrored Pair)"),
        ("5", "Fly Facing (Shield)", "Main Fabric + Interfacing", "Cut 1 Main + 1 Interfacing"),
        ("6", "Pocket Lining (Inner)", "Lining Fabric", "Cut 2 (Mirrored Pair)"),
        ("7", "Fly Interfacing", "Fusible Interfacing", "Cut 2 (Left & Right fly)"),
        ("BL", "Belt Loops (5x)", "Main Fabric + Interfacing", "Cut 1 strip (3.5 cm x 45 cm)")
    ]
    for r_idx, (p_num, p_name, p_mat, p_cut) in enumerate(pieces_data):
        bg = TABLE_ALT if r_idx % 2 == 1 else WHITE
        c.setFillColor(bg)
        c.rect(M_L, y - 13, sum(pw), 13, fill=1, stroke=0)
        c.setFont("Poppins-Bold", 6.8)
        c.setFillColor(TEXT_BODY)
        c.drawString(M_L + 6, y - 9.5, p_num)
        c.setFont("Poppins", 6.8)
        c.drawString(M_L + pw[0] + 6, y - 9.5, p_name)
        c.drawString(M_L + pw[0] + pw[1] + 6, y - 9.5, p_mat)
        c.drawString(M_L + pw[0] + pw[1] + pw[2] + 6, y - 9.5, p_cut)
        y -= 13
        
    y -= 18
    c.setFont("Poppins-Bold", 9.0)
    c.setFillColor(BURGUNDY)
    c.drawString(M_L, y, "SEWING ORDER AT A GLANCE")
    y -= 14
    
    sow = [140, 355]
    c.setFillColor(TABLE_HEAD)
    c.rect(M_L, y - 14, sum(sow), 14, fill=1, stroke=0)
    c.setFont("Poppins-Bold", 6.8)
    c.setFillColor(WHITE)
    c.drawString(M_L + 6, y - 10, "PHASE")
    c.drawString(M_L + sow[0] + 6, y - 10, "OPERATION SUMMARY")
    y -= 14
    
    so_rows = [
        ("Step 1: Front Pleats & Creases", "Form double forward pleats on Pants Front and press center leg creases."),
        ("Step 2: Slanted Hip Pockets", "Apply stay-tape, stitch pocket openings, understitch, and attach pocket bags."),
        ("Step 3: Front Zipper Fly & Shield", "Install zipper, sew curved J-stitch topstitching, and attach fly shield."),
        ("Step 4: Back Darts & Center Seam", "Sew 4 back waist darts (2 per side) and stitch center back rise seam."),
        ("Step 5: Inseams & Crotch Curve", "Join inner leg seams and stitch reinforced U-shaped crotch curve."),
        ("Step 6: Outer Side Seams & Loops", "Join outer side seams and construct 5 tailored belt loops."),
        ("Step 7: Waistband & Deep Hem", "Attach tailored waistband, conceal hook & bar, and turn up 5 cm weighted hem.")
    ]
    for r_idx, (ph, op) in enumerate(so_rows):
        bg = TABLE_ALT if r_idx % 2 == 1 else WHITE
        c.setFillColor(bg)
        c.rect(M_L, y - 13, sum(sow), 13, fill=1, stroke=0)
        c.setFont("Poppins-Bold", 6.8)
        c.setFillColor(TEXT_BODY)
        c.drawString(M_L + 6, y - 9.5, ph)
        c.setFont("Poppins", 6.8)
        c.drawString(M_L + sow[0] + 6, y - 9.5, op)
        y -= 13
        
    y -= 16
    draw_tip_box(c, y, "Standard Seam Allowance & Hem Protocol",
                 "• Standard <b>1.0 cm (3/8 in)</b> seam allowance is included on all pattern edges.<br/>• Deep <b>5.0 cm (2.0 in)</b> hem is included at bottom of legs for authentic palazzo drape.<br/>• Cut directly along solid pattern lines—do NOT add extra seam allowance.")
    c.showPage()

    # =========================================================================
    # PAGE 7: YOUR PATTERN / PIECES & MARKINGS
    # =========================================================================
    draw_page_bg_and_chrome(c, 7)
    y = draw_section_header(c, "PIECES GUIDE", "Pattern Pieces & Markings Guide")
    
    dw = 230.0
    dh = 250.0
    if os.path.exists(PIECES_OVERVIEW):
        c.drawImage(PIECES_OVERVIEW, M_L, y - dh - 8, width=dw, height=dh, preserveAspectRatio=True)
        
    rx = M_L + dw + 16
    rw = M_R - rx
    ry = y - 4
    
    c.setFont("Poppins-Bold", 9.2)
    c.setFillColor(BURGUNDY)
    c.drawString(rx, ry, "Understanding Pattern Markings")
    ry -= 16
    
    marks_info = [
        ("Double Front Pleat Lines", "Two pairs of vertical lines with direction arrows on Pants Front (1). Fold along line and bring to partner line toward side seam."),
        ("Center Leg Crease Line", "Vertical pressed crease running straight down each leg from the main pleat all the way to bottom hem."),
        ("Back Waist Darts", "Four V-shaped waist darts (two on each Pants Back) creating contoured shaping over the seat."),
        ("Slanted Pocket Notches", "Single triangle notches along hip edge indicating exact placement for pocket bags (Pieces 4 & 6)."),
        ("Fly Shield & Zipper Stop", "Circle dot on center front rise marking the bottom of the zipper fly opening and J-stitch pivot."),
        ("5 Belt Loops Placement", "Notches on waistband: 2 aligned with front pleats, 2 aligned with pocket tops, 1 at center back.")
    ]
    for m_t, m_d in marks_info:
        ry = draw_bullet(c, rx, ry, f"<b>{m_t}:</b> {m_d}", rw, font_size=7.2, leading=10.0)
        
    y = y - dh - 24
    c.setFont("Poppins-Bold", 8.8)
    c.setFillColor(CHARCOAL)
    c.drawString(M_L, y, "HOW TO LENGTHEN OR SHORTEN YOUR PALAZZO PANTS")
    y -= 12
    
    col_w = (CONTENT_W - 14) / 2.0
    b_adj_h = 92.0
    c.saveState()
    # Left Box: Lengthen
    c.setFillColor(CONTAINER_BG)
    c.rect(M_L, y - b_adj_h, col_w, b_adj_h, fill=1, stroke=0)
    c.setFillColor(BURGUNDY)
    c.rect(M_L, y - b_adj_h, 3.5, b_adj_h, fill=1, stroke=0)
    c.setFont("Poppins-Bold", 8.0)
    c.setFillColor(BURGUNDY)
    c.drawString(M_L + 12, y - 13, "TO LENGTHEN (+) — FOR TALL FIT")
    
    len_txt = (
        "<b>1. Cut Across:</b> Locate horizontal line at mid-thigh on Pieces 1 & 2.<br/>"
        "<b>2. Spread Evenly:</b> Separate sections by desired extension (e.g. +3 to +5 cm).<br/>"
        "<b>3. Tape & True:</b> Back with paper and blend side and inner leg seamlines."
    )
    p_len = Paragraph(len_txt, ParagraphStyle("LenP", fontName="Poppins", fontSize=6.8, leading=9.8, textColor=TEXT_BODY))
    p_len.wrapOn(c, col_w - 20, b_adj_h - 22)
    p_len.drawOn(c, M_L + 12, y - 20 - p_len.height)
    
    # Right Box: Shorten
    rx2 = M_L + col_w + 14
    c.setFillColor(CONTAINER_BG)
    c.rect(rx2, y - b_adj_h, col_w, b_adj_h, fill=1, stroke=0)
    c.setFillColor(BURGUNDY)
    c.rect(rx2, y - b_adj_h, 3.5, b_adj_h, fill=1, stroke=0)
    c.setFont("Poppins-Bold", 8.0)
    c.setFillColor(BURGUNDY)
    c.drawString(rx2 + 12, y - 13, "TO SHORTEN (-) — FOR PETITE FIT")
    
    shrt_txt = (
        "<b>1. Measure Up:</b> Mark a parallel line above the lengthen/shorten line.<br/>"
        "<b>2. Fold & Overlap:</b> Crease lower section upward to meet guideline.<br/>"
        "<b>3. Re-true Edges:</b> Tape flat and smooth outer side seams and inseams."
    )
    p_shrt = Paragraph(shrt_txt, ParagraphStyle("ShrtP", fontName="Poppins", fontSize=6.8, leading=9.8, textColor=TEXT_BODY))
    p_shrt.wrapOn(c, col_w - 20, b_adj_h - 22)
    p_shrt.drawOn(c, rx2 + 12, y - 20 - p_shrt.height)
    c.restoreState()
    c.showPage()

    # =========================================================================
    # PAGE 8: EXTRA HELP / HELPFUL VIDEO GUIDES
    # =========================================================================
    draw_page_bg_and_chrome(c, 8)
    y = draw_section_header(c, "EXTRA HELP", "Helpful Video Guides Hub")
    
    hub_intro = (
        "Master each tailoring technique with confidence! Click any title to watch the video tutorial in your web browser, "
        "or scan the QR code with your smartphone camera."
    )
    p_hub = Paragraph(hub_intro, ParagraphStyle("HubIntro", fontName="Poppins", fontSize=8.8, leading=13.0, textColor=TEXT_BODY))
    w, h = p_hub.wrap(CONTENT_W, 50)
    p_hub.drawOn(c, M_L, y - h)
    y -= (h + 20)
    
    video_cards = [
        ("Sewing Front Pleats & Center Crease", "Step 1 Technique Guide", "https://www.youtube.com/watch?v=kYJvM9x0b0Q"),
        ("Sewing Slanted Trouser Pockets", "Step 2 Technique Guide", "https://www.youtube.com/watch?v=rZvkl2069sQ"),
        ("Front Zipper Fly & Shield Installation", "Step 3 Technique Guide", "https://www.youtube.com/watch?v=Y3rAmHE7CZs"),
        ("Concealed Hook & Bar Waistband Closure", "Step 7 Technique Guide", "https://www.youtube.com/watch?v=DPpF3kAP_oo")
    ]
    
    c_w = (CONTENT_W - 20) / 2.0
    c_h = 105.0
    for idx, (v_title, v_step, v_url) in enumerate(video_cards):
        col = idx % 2
        row = idx // 2
        cx = M_L + col * (c_w + 20)
        cy = y - row * (c_h + 30)
        
        # QR Code with proper vector transform
        qr = QrCodeWidget(v_url)
        bounds = qr.getBounds()
        qw = bounds[2] - bounds[0]
        qh = bounds[3] - bounds[1]
        target_sz = 60.0
        d = Drawing(target_sz, target_sz, transform=[target_sz/qw, 0, 0, target_sz/qh, 0, 0])
        d.add(qr)
        d.drawOn(c, cx + 3, cy - c_h + 16)
        
        tx = cx + 78
        c.setFont("Poppins-Bold", 8.8)
        c.setFillColor(CHARCOAL)
        c.drawString(tx, cy - 20, v_title)
        
        c.setFont("Poppins", 7.6)
        c.setFillColor(MUTED)
        c.drawString(tx, cy - 34, v_step)
        
        c.setFont("Poppins-Bold", 8.0)
        c.setFillColor(BURGUNDY)
        c.drawString(tx, cy - 54, "Watch Video Tutorial →")
        c.linkURL(v_url, (tx, cy - 58, tx + 110, cy - 42), relative=0)
        
    y_foot = cy - c_h - 40
    c.setFont("Poppins-Italic", 7.4)
    c.setFillColor(MUTED)
    c.drawString(M_L, y_foot, "Video tutorials are produced by independent tailoring educators. Always follow the seam allowances and measurements in this guide.")
    c.showPage()

    # =========================================================================
    # PAGES 9–15: THE 7 AUTHENTIC CONSTRUCTION STEPS
    # =========================================================================
    steps_data = [
        # Page 9: Step 1
        (1, "Sew the front pleats & press creases", "Pieces 1 & 2 · pictures 1–2", "step1_panels.png",
         [
             "<b>Double Front Pleats:</b> On the right side of each Pants Front (1), fold both waist pleats along the solid pleat line and bring fold to meet partner line in the direction of printed arrows (toward side seam). Machine-baste across upper waist edge at 6 mm (1/4 in) to secure (pic. 1).",
             "<b>Razor-Sharp Center Crease:</b> Fold each leg in half lengthwise matching inseam and side seam at knee and hem. Press a razor-sharp vertical crease line from the main front pleat straight down to the bottom hem (pic. 2).",
             "<b>Pressing Technique:</b> Use steam and a wooden clapper on each pleat and crease line for crisp, lasting sharpness."
         ],
         ("Tailoring Secret: Center Crease Integrity",
          "Pressing the center creases right now while leg panels are flat ensures your palazzo trousers hang with breathtaking, razor-sharp vertical drape!")),
        
        # Page 10: Step 2
        (2, "Sew the slanted front hip pockets", "Pieces 1, 4 & 6 · pictures 1–5", "step2_panels.png",
         [
             "<b>Stay-Tape Reinforcement:</b> Apply 1 cm bias stay-tape to wrong side of slanted pocket opening edge on Pants Front (1) to prevent stretching.",
             "<b>Pocket Lining:</b> Place Pocket Lining (6) right sides together with Pants Front (1), matching notches. Stitch along slanted pocket line at 1 cm (3/8 in) (pic. 1).",
             "<b>Understitching:</b> Trim seam allowance to 5 mm, press Pocket Lining away from garment, and understitch on Pocket Lining 2 mm from seamline so lining rolls cleanly inward (pic. 2).",
             "<b>Attach Pocket Bag:</b> Place Pocket Bag (4) right sides together with Pocket Lining (6), matching curved edges. Stitch pocket bag circumference at 1 cm and serge raw seam (pics. 4–5)."
         ],
         ("Pro Tip: Understitching Magic",
          "Understitching prevents the pocket lining from rolling outward when you slide your hands into your pockets, keeping the front hip completely flat.")),
        
        # Page 11: Step 3
        (3, "Install the front zipper fly & fly shield", "Pieces 1, 5 & 7 · pictures 1–8", "step4_panels.png",
         [
             "<b>Interfacing Fly:</b> Fuse Fly Interfacing (7) to wrong side of both front fly extensions. Whipstitch across zipper teeth 2 cm below circle stop.",
             "<b>Center Front Seam:</b> Place Pants Fronts (1) right sides together. Stitch center front from 2.5 cm above inseam to circle stop, backstitch, and machine-baste from circle to waist edge (pics. 1–2).",
             "<b>Zipper Placement:</b> Fold right fly extension wrong sides together. Place closed zipper face up under folded edge and stitch with zipper foot (pic. 3).",
             "<b>J-Stitch Topstitching:</b> Flip zipper onto left fly extension, stitch loose tape to left extension only, remove basting, and topstitch the curved J-stitch from waist down to circle (pics. 4–6).",
             "<b>Fly Shield:</b> Fold Fly Facing Shield (5) lengthwise wrong sides together, finish edges, pin behind right zipper tape, and bar tack at bottom of J-stitch (pics. 7–8)."
         ],
         ("Pro Tip: Fly Shield Alignment",
          "The fly shield protects your undergarments from the zipper teeth. Stitch the bottom bar tack securely catching the shield for boutique durability.")),

        # Page 12: Step 4
        (4, "Sew back waist darts & center back seam", "Piece 2 · 4 Darts & Rise", "step4_darts_panel.png",
         [
             "<b>Back Waist Darts:</b> Fold each of the 4 waist darts (2 on each Pants Back) right sides together along center line, matching waist notches.",
             "<b>Stitching Darts:</b> Stitch from waist edge down to a gentle taper at dart point. Tie long thread tails by hand at the point instead of backstitching to avoid dimples.",
             "<b>Pressing Darts:</b> Press the two inner back darts toward center back, and the two outer darts toward side seams over a tailor's pressing ham.",
             "<b>Center Back Seam:</b> Place the two Pants Backs (2) right sides together along the center back rise seam. Stitch at 1 cm (3/8 in) from waist down to crotch intersection and press seam open."
         ],
         ("Pro Tip: Seamless Pocketless Back",
          "Without bulky welt pockets, these 4 contoured darts mold effortlessly over the hips, giving a smooth, flattering hourglass line from waist to seat.")),

        # Page 13: Step 5
        (5, "Sew the inseams & reinforced crotch curve", "Pieces 1 & 2 · pictures 1–2", "step5_inseams_panel.png",
         [
             "<b>Pants Inseams:</b> Place each Pants Back (2) right sides together onto matching Pants Front (1), aligning inner leg edges from crotch point down to ankle hem and matching knee notches.",
             "<b>Stitching Inseams:</b> Pin and stitch both inseams continuously at 1 cm (3/8 in) from crotch to hem. Finish seam allowances separately and press open flat.",
             "<b>Crotch Seam:</b> Turn one trouser leg right side out and slide it inside other leg so both legs are right sides together along U-shaped crotch curve.",
             "<b>Reinforcing Rise:</b> Stitch lower front rise through crotch curve and up center back rise. Stitch a second reinforcement row 2 mm away, trim, and serge raw edges."
         ],
         ("Pro Tip: Four-Way Cross Junction",
          "At the inner leg cross junction, press seam allowances in opposite directions to reduce needle deflection and bulk.")),

        # Page 14: Step 6
        (6, "Sew outer side seams & prepare 5 belt loops", "Pieces 1, 2 & Belt Loops", "step6_panels.png",
         [
             "<b>Outer Side Seams:</b> Pin outer edges of Pants Front (1) and Pants Back (2) right sides together from waist to hem, catching basted pocket bags while keeping pocket openings free (pic. 1).",
             "<b>Stitching Side Seams:</b> Stitch both side seams at 1 cm (3/8 in). Finish raw edges separately with serger and press seams open.",
             "<b>Construct 5 Belt Loops:</b> Fold 3.5 cm wide belt loop strip lengthwise right sides together, stitch 6 mm from fold, turn right side out, press to 1.1 cm finished width, and cut into 5 equal 8.5 cm loops.",
             "<b>Position Belt Loops:</b> Baste loops facing downward at waist: <b>2 directly over front main pleats/creases, 2 over pocket top corners, and 1 at center back</b>."
         ],
         ("Pro Tip: Belt Loop Alignment",
          "Placing the two front loops directly over the main pleats accentuates the sharp vertical crease lines and holds your belt with quiet-luxury precision.")),

        # Page 15: Step 7
        (7, "Attach tailored waistband & hem the trousers", "Piece 3 | Hook & Bar | 5.0 cm Hem", "step7_hook_and_hem_panel.png",
         [
             "<b>Attach Waistband:</b> Pin interfaced Waistband (3) right sides together to trouser waist edge catching belt loops. Stitch at 1 cm (3/8 in) and press seam allowances up into waistband.",
             "<b>Waistband Extension Tab:</b> Fold waistband right sides together along foldline, stitch short ends at extension tab, clip corners, turn right side out, and press.",
             "<b>Concealed Hook & Bar:</b> Install heavy-duty metal trouser hook & bar on inside extension tab: <b>bar on left inside facing, hook on right extension</b>. Zero buttons visible on exterior!",
             "<b>Secure Belt Loops:</b> Turn belt loops upward over waistband, fold top raw edges under 6 mm, and bar tack securely 3 mm below top waistband edge.",
             "<b>Turn Up 5.0 cm Hem:</b> Press leg lower edge 1.0 cm (3/8 in) to wrong side, then fold up 4.0 cm (1 5/8 in) to form deep <b>5.0 cm (2.0 in) weighted palazzo hem</b>. Blind-stitch invisibly by hand or machine."
         ],
         ("Pro Tip: Deep Weighted Palazzo Hem",
          "The deep 5.0 cm (2.0 in) fold-up hem provides the essential gravity and weight for the wide palazzo legs to drape with fluid waterfall motion over your footwear."))
    ]

    for p_num, s_title, s_context, s_panel, s_lines, (tip_title, tip_body) in steps_data:
        page_no = 8 + p_num
        draw_page_bg_and_chrome(c, page_no)
        y = H - 64
        
        c.saveState()
        c.setFont("Poppins-Medium", 7.4)
        c.setFillColor(BURGUNDY)
        c.drawString(M_L, y, "L E T ' S   S E W")
        y -= 24
        
        y = draw_step_header(c, y, p_num, s_title, s_context)
        
        p_style = ParagraphStyle(f"StepStyle_{p_num}", fontName="Poppins", fontSize=8.0, leading=11.6, textColor=TEXT_BODY)
        for line in s_lines:
            p = Paragraph(f"• {line}", p_style)
            p.wrapOn(c, CONTENT_W, 60)
            p.drawOn(c, M_L, y - p.height)
            y -= (p.height + 5)
            
        y -= 6
        panel_path = os.path.join(ASSET_DIR, s_panel)
        box_w = CONTENT_W
        box_h = 230.0
        
        # Framed Panel Container
        c.setFillColor(CONTAINER_BG)
        c.roundRect(M_L, y - box_h, box_w, box_h, 8, fill=1, stroke=0)
        c.setStrokeColor(BORDER_SUBTLE)
        c.setLineWidth(0.8)
        c.roundRect(M_L, y - box_h, box_w, box_h, 8, fill=0, stroke=1)
        
        if os.path.exists(panel_path):
            c.drawImage(panel_path, M_L + 6, y - box_h + 6, width=box_w - 12, height=box_h - 12, preserveAspectRatio=True, anchor='c')
            
        y = y - box_h - 14
        draw_tip_box(c, y, tip_title, tip_body)
        c.showPage()

    # =========================================================================
    # PAGE 16: YOU MADE IT / 360° FIT GALLERY & CELEBRATION
    # =========================================================================
    draw_page_bg_and_chrome(c, 16)
    y = draw_section_header(c, "YOU MADE IT", "Enjoy Your Colette Palazzo Trousers!")
    
    congrats = (
        "Congratulations on completing your couture <b>Colette Double-Pleated Palazzo Trousers</b>! "
        "Take a moment to admire the graceful fluid drape of the ultra-wide palazzo legs, the razor-sharp center creases, "
        "and the clean, seamless waistline created by your concealed trouser hook & bar closure."
    )
    p_cg = Paragraph(congrats, ParagraphStyle("Congrats", fontName="Poppins", fontSize=8.4, leading=12.2, textColor=TEXT_BODY))
    w, h = p_cg.wrap(CONTENT_W, 50)
    p_cg.drawOn(c, M_L, y - h)
    y -= (h + 16)
    
    # 360° Fit Gallery Title
    c.setFont("Poppins-Bold", 9.2)
    c.setFillColor(BURGUNDY)
    c.drawString(M_L, y, "360° EDITORIAL FIT GALLERY & RUNWAY PROPORTIONS")
    y -= 12
    
    gal_w = (CONTENT_W - 20.0) / 3.0
    gal_h = 210.0
    photos_360 = [
        (PHOTO_FRONT, "1. FRONT: DOUBLE PLEATS & CREASES"),
        (PHOTO_SIDE,  "2. SIDE: 45° SLANT HIP POCKET"),
        (PHOTO_BACK,  "3. BACK: CONTOURED DARTS & SWEEP")
    ]
    for idx, (p_path, cap) in enumerate(photos_360):
        gx = M_L + idx * (gal_w + 10.0)
        gy = y - gal_h
        
        if os.path.exists(p_path):
            c.setFillColor(WHITE)
            c.rect(gx - 3, gy - 3, gal_w + 6, gal_h + 6, fill=1, stroke=0)
            c.setStrokeColor(BORDER_SUBTLE)
            c.setLineWidth(0.8)
            c.rect(gx - 3, gy - 3, gal_w + 6, gal_h + 6, fill=0, stroke=1)
            c.drawImage(p_path, gx, gy, width=gal_w, height=gal_h, preserveAspectRatio=True)
            
            # Caption Banner
            c.setFillColor(TABLE_HEAD)
            c.rect(gx, gy, gal_w, 14, fill=1, stroke=0)
            c.setFont("Poppins-Bold", 5.6)
            c.setFillColor(WHITE)
            c.drawCentredString(gx + gal_w/2.0, gy + 4.0, cap)
            
    y -= (gal_h + 20)
    
    c.setFont("Poppins-Bold", 9.0)
    c.setFillColor(BURGUNDY)
    c.drawString(M_L, y, "Styling & Textile Care Suggestions")
    y -= 12
    
    styling_tips = [
        "<b>Styling:</b> Tuck in a crisp linen button-down shirt or fine-ribbed silk tank to highlight the high waist and double pleats. Pair with minimalist leather slide sandals or pointed-toe mules.",
        "<b>Care Protocol:</b> Hand-wash cold or gentle machine cycle in a mesh wash bag. Hang to dry along the pressed crease lines. Steam press with a pressing cloth for effortless luxury texture."
    ]
    for st in styling_tips:
        y = draw_bullet(c, M_L, y, st, CONTENT_W, font_size=7.4, leading=10.6)
        
    y -= 10
    draw_tip_box(c, y, "Need Personalized Sewing Support?",
                 "If you have any questions about fit, grading, or assembly, reach out to us directly through our Etsy shop <b>SewLuxePatterns</b>. We are delighted to support your creative journey! © SewLuxePatterns.")
    c.showPage()
    
    # Save Canvas
    c.save()
    print(f"[SUCCESS] Official 16-Page Luxury Booklet created at:\n  -> {OUT_DESKTOP_BOOKLET}")
    
    # Copy to delivery guide folder & brain
    shutil.copy2(OUT_DESKTOP_BOOKLET, OUT_DELIVERY_BOOKLET)
    shutil.copy2(OUT_DESKTOP_BOOKLET, OUT_BRAIN_BOOKLET)
    print(f"  -> Copied to {OUT_DELIVERY_BOOKLET}")
    print(f"  -> Copied to {OUT_BRAIN_BOOKLET}")

if __name__ == "__main__":
    build_pdf()
