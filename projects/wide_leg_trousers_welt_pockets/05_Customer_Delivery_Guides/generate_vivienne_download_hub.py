#!/usr/bin/env python3
import os
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

FONTS_DIR = r"C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\fonts"
PROJECT_DIR = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\projects\wide_leg_trousers_welt_pockets"
OUT_PDF = os.path.join(PROJECT_DIR, "05_Customer_Delivery_Guides", "Vivienne_Wide_Leg_Trousers_Download_Hub.pdf")
BRAIN_PDF = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0\Vivienne_Wide_Leg_Trousers_Download_Hub.pdf"

MODEL_PHOTO = os.path.join(PROJECT_DIR, "01_Model_Photos", "vivienne_photo_01_front.jpg")
FLAT_SKETCH = os.path.join(PROJECT_DIR, "02_Technical_Flat_Sketches", "Vivienne_Pants_Sketch_SideBySide.png")

# Register Fonts
pdfmetrics.registerFont(TTFont("Lora-Bold", os.path.join(FONTS_DIR, "Lora-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Lora-Regular", os.path.join(FONTS_DIR, "Lora-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Lora-Italic", os.path.join(FONTS_DIR, "Lora-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Bold", os.path.join(FONTS_DIR, "Poppins-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Medium", os.path.join(FONTS_DIR, "Poppins-Medium.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Regular", os.path.join(FONTS_DIR, "Poppins-Regular.ttf")))

# Palette
C_BG = colors.HexColor("#FAF8F5")
C_CONTAINER = colors.HexColor("#F5F2EF")
C_BORDER = colors.HexColor("#E2DDD8")
C_GOLD = colors.HexColor("#C5A880")
C_BURGUNDY = colors.HexColor("#8C3B47")
C_MUTED = colors.HexColor("#7C6E5E")
C_WHITE = colors.HexColor("#FFFFFF")
C_DARK = colors.HexColor("#1A1A1A")
C_ACCENT_BG = colors.HexColor("#ECE7E1")

def build_download_hub():
    W, H = A4
    c = canvas.Canvas(OUT_PDF, pagesize=A4)
    
    # Background
    c.setFillColor(C_BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Double Luxury Border
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(1.2)
    c.rect(26, 26, W - 52, H - 52)
    
    c.setStrokeColor(C_BORDER)
    c.setLineWidth(0.6)
    c.rect(30, 30, W - 60, H - 60)
    
    # Header Banner
    c.setFont("Lora-Bold", 16)
    c.setFillColor(C_BURGUNDY)
    c.drawCentredString(W / 2.0, H - 58, "S E W L U X E   P A T T E R N S")
    
    c.setFont("Poppins-Medium", 8)
    c.setFillColor(C_MUTED)
    c.drawCentredString(W / 2.0, H - 74, "DIGITAL PATTERN DOWNLOAD PORTAL · INSTANT ACCESS")
    
    # Thin divider
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(0.8)
    c.line(W / 2.0 - 120, H - 84, W / 2.0 + 120, H - 84)
    
    # Garment Title
    c.setFont("Lora-Regular", 22)
    c.setFillColor(C_DARK)
    c.drawCentredString(W / 2.0, H - 114, "Vivienne Tailored Wide-Leg Trousers")
    
    c.setFont("Poppins-Regular", 8.5)
    c.setFillColor(C_MUTED)
    c.drawCentredString(W / 2.0, H - 130, "High-Waisted Flat Front · Slanted Pockets · 15 Sizes (XXS–10XL) · Professional Pattern Suite")
    
    # Visual Showcase Box (Model Photo + Technical Sketch side-by-side)
    box_w = W - 92
    box_h = 175
    box_x = 46
    box_y = H - 322
    
    c.setFillColor(C_CONTAINER)
    c.setStrokeColor(C_BORDER)
    c.setLineWidth(1)
    c.roundRect(box_x, box_y, box_w, box_h, 8, fill=1, stroke=1)
    
    # Insert Model Photo (Left)
    if os.path.exists(MODEL_PHOTO):
        p_w = 155
        p_h = 155
        c.drawImage(MODEL_PHOTO, box_x + 12, box_y + 10, width=p_w, height=p_h, preserveAspectRatio=True)
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(1)
        c.rect(box_x + 12, box_y + 10, p_w, p_h, fill=0, stroke=1)
    
    # Insert Flat Sketch (Right)
    if os.path.exists(FLAT_SKETCH):
        s_w = box_w - 155 - 36
        s_h = 155
        c.drawImage(FLAT_SKETCH, box_x + 155 + 24, box_y + 10, width=s_w, height=s_h, preserveAspectRatio=True)
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(1)
        c.rect(box_x + 155 + 24, box_y + 10, s_w, s_h, fill=0, stroke=1)
        
    # Download Section Header
    y_cards_top = box_y - 28
    c.setFont("Lora-Bold", 13)
    c.setFillColor(C_BURGUNDY)
    c.drawString(46, y_cards_top, "Your Digital Pattern Library")
    
    c.setFont("Poppins-Regular", 8)
    c.setFillColor(C_MUTED)
    c.drawString(46, y_cards_top - 14, "Click any button below to download your complete ZIP archive directly:")
    
    # 4 Download Cards (2x2 Grid)
    card_w = (W - 92 - 14) / 2.0  # ~244 pt
    card_h = 72
    
    cards_data = [
        ("A4 PRINT-AT-HOME PACK", "15 Individual Sizes (XXS–10XL) + Multi-Size Layered PDF for European & International A4 home printers.", "A4"),
        ("US LETTER PRINT-AT-HOME", "15 Individual Sizes (XXS–10XL) + Multi-Size Layered PDF formatted for standard 8.5\" x 11\" North American paper.", "LETTER"),
        ("A0 COPYSHOP MASTER PACK", "Continuous large-format A0 blueprints (no tiling/taping required) for commercial wide-format copy shops.", "A0"),
        ("DEDICATED PROJECTOR FILE", "Optimized ultra-wide canvas, thick 3.5pt lines, 50cm margins, calibration grids & toggleable size layers.", "PROJECTOR")
    ]
    
    card_positions = [
        (46, y_cards_top - 32 - card_h),
        (46 + card_w + 14, y_cards_top - 32 - card_h),
        (46, y_cards_top - 32 - 2 * card_h - 10),
        (46 + card_w + 14, y_cards_top - 32 - 2 * card_h - 10)
    ]
    
    for (title, desc, tag), (cx, cy) in zip(cards_data, card_positions):
        # Card Background
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(1)
        c.roundRect(cx, cy, card_w, card_h, 6, fill=1, stroke=1)
        
        # Tag pill
        c.setFillColor(C_ACCENT_BG)
        c.roundRect(cx + 10, cy + card_h - 18, 55, 12, 3, fill=1, stroke=0)
        c.setFont("Poppins-Bold", 6)
        c.setFillColor(C_BURGUNDY)
        c.drawCentredString(cx + 10 + 27.5, cy + card_h - 14, tag)
        
        # Title
        c.setFont("Poppins-Bold", 8.5)
        c.setFillColor(C_DARK)
        c.drawString(cx + 72, cy + card_h - 15, title)
        
        # Description
        c.setFont("Poppins-Regular", 6.8)
        c.setFillColor(C_MUTED)
        # Wrap description across two lines
        words = desc.split()
        l1 = " ".join(words[:11])
        l2 = " ".join(words[11:])
        c.drawString(cx + 10, cy + card_h - 34, l1)
        c.drawString(cx + 10, cy + card_h - 45, l2)
        
        # Clickable Download Button
        btn_y = cy + 8
        c.setFillColor(C_BURGUNDY)
        c.roundRect(cx + 10, btn_y, card_w - 20, 18, 4, fill=1, stroke=0)
        c.setFont("Poppins-Medium", 7.5)
        c.setFillColor(C_WHITE)
        c.drawCentredString(cx + card_w / 2.0, btn_y + 5, f"↓  DOWNLOAD {tag} ARCHIVE (.ZIP)")
        
        # Link annotation
        c.linkURL(f"https://drive.google.com/drive/folders/sewluxe_{tag.lower()}", (cx + 10, btn_y, cx + card_w - 10, btn_y + 18), relative=0)
        
    # Quick Start Advice Box
    qs_y = card_positions[2][1] - 88
    c.setFillColor(C_CONTAINER)
    c.setStrokeColor(C_BORDER)
    c.setLineWidth(0.8)
    c.roundRect(46, qs_y, W - 92, 74, 6, fill=1, stroke=1)
    
    c.setFont("Lora-Bold", 10.5)
    c.setFillColor(C_BURGUNDY)
    c.drawString(58, qs_y + 56, "Essential Printing & Assembly Reminders:")
    
    tips = [
        "1. Open in Free Adobe Acrobat Reader on a computer (never print directly from web browsers or mobile).",
        "2. Print Page 1 first at 100% / 'Actual Size' and verify the 4\" x 4\" (101.5 mm) calibration square with a ruler.",
        "3. In the Multi-Size Layered PDF, click the Layers icon (👁️) on the left panel to display ONLY your size."
    ]
    ty = qs_y + 40
    for tip in tips:
        c.setFont("Poppins-Regular", 7.2)
        c.setFillColor(C_DARK)
        c.drawString(58, ty, tip)
        ty -= 12.5
        
    # Footer
    c.setFont("Poppins-Regular", 7.5)
    c.setFillColor(C_MUTED)
    c.drawCentredString(W / 2.0, 42, "Need assistance with downloading, printing or grading? Message us on Etsy anytime — we're here to help!")
    
    c.save()
    print("Download Hub PDF successfully generated at:", OUT_PDF)
    shutil.copy2(OUT_PDF, BRAIN_PDF)

if __name__ == "__main__":
    build_download_hub()
