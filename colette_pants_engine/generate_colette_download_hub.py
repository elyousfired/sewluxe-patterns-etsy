#!/usr/bin/env python3
"""
generate_colette_download_hub.py
================================
Generates the 1-Page Luxury Etsy Instant Download Hub PDF for Colette Double-Pleated Palazzo Trousers.
Features:
- SewLuxe atelier branding (Lora, Poppins, Burgundy #8C3B47, Gold #C5A880, Warm Sand #F5F2EF).
- Approved Editorial Model Photo & Technical Flat Sketch thumbnails.
- 4 prominent, clickable download cards (US Letter, A4, A0 Copyshop, Dedicated Projector File).
- 3-step printing and assembly quick-start reminder.
- 5-star customer support link.
"""

import os
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

FONTS_DIR = r"C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\fonts"
BRAIN_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0"
OUT_DESKTOP = r"C:\Users\red1e\Desktop\SewLuxe_Colette_Tailored_Pants\07_Customer_Delivery_Guide\Colette_Palazzo_Trousers_Download_Hub.pdf"
OUT_BRAIN = os.path.join(BRAIN_DIR, "Colette_Palazzo_Trousers_Download_Hub.pdf")

MODEL_PHOTO = os.path.join(BRAIN_DIR, "colette_photo_01_front.jpg")
FLAT_SKETCH = os.path.join(BRAIN_DIR, "Colette_Sketch_SideBySide.png")

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
    c = canvas.Canvas(OUT_DESKTOP, pagesize=A4)
    
    # Background
    c.setFillColor(C_BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Double Luxury Border
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(1.2)
    c.rect(26, 26, W - 52, H - 52)
    
    c.setStrokeColor(C_BURGUNDY)
    c.setLineWidth(0.6)
    c.rect(32, 32, W - 64, H - 64)
    
    # Corner Gold Accents
    c.setFillColor(C_GOLD)
    for cx, cy in [(29, 29), (W - 29, 29), (29, H - 29), (W - 29, H - 29)]:
        c.circle(cx, cy, 2.2, fill=1, stroke=0)
        
    # Top Brand Header
    c.setFillColor(C_BURGUNDY)
    c.setFont("Poppins-Bold", 11)
    c.drawCentredString(W / 2, H - 54, "S E W L U X E   P A T T E R N S")
    
    c.setFillColor(C_MUTED)
    c.setFont("Poppins-Medium", 7.5)
    c.drawCentredString(W / 2, H - 68, "DIGITAL PATTERN DOWNLOAD HUB · ATELIER ACCESS PORTAL")
    
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(0.8)
    c.line(W / 2 - 60, H - 76, W / 2 + 60, H - 76)
    c.circle(W / 2, H - 76, 1.8, fill=1, stroke=0)
    
    # Hero Card (Y: H - 85 to H - 245)
    hero_y = H - 242
    hero_h = 158
    c.setFillColor(C_CONTAINER)
    c.setStrokeColor(C_BORDER)
    c.setLineWidth(0.8)
    c.roundRect(46, hero_y, W - 92, hero_h, 8, fill=1, stroke=1)
    
    # Model Photo Thumbnail
    if os.path.exists(MODEL_PHOTO):
        c.drawImage(MODEL_PHOTO, 56, hero_y + 10, width=138, height=138, preserveAspectRatio=True, anchor='c')
        c.setStrokeColor(C_BURGUNDY)
        c.setLineWidth(0.8)
        c.rect(56, hero_y + 10, 138, 138, fill=0, stroke=1)
        
    # Flat Sketch Thumbnail
    if os.path.exists(FLAT_SKETCH):
        c.drawImage(FLAT_SKETCH, 204, hero_y + 10, width=110, height=138, preserveAspectRatio=True, anchor='c')
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.6)
        c.rect(204, hero_y + 10, 110, 138, fill=0, stroke=1)
        
    # Hero Text (Right of photos: tx = 326)
    tx = 326
    c.setFillColor(C_GOLD)
    c.setFont("Poppins-Bold", 7.5)
    c.drawString(tx, hero_y + 134, "ATELIER SEWING PATTERN")
    
    c.setFillColor(C_BURGUNDY)
    c.setFont("Lora-Bold", 13.5)
    c.drawString(tx, hero_y + 116, "COLETTE PALAZZO")
    c.drawString(tx, hero_y + 100, "TAILORED TROUSERS")
    
    c.setFillColor(C_MUTED)
    c.setFont("Lora-Italic", 8)
    c.drawString(tx, hero_y + 86, "Double Pleats · Center Creases · Concealed Closure")
    
    badges = [
        ("Sizes Included:", "US 00 – 22 (XXS – 4XL)"),
        ("Seam Allowance:", "1 cm (3/8 in) Included"),
        ("Skill Level:", "Intermediate Tailoring"),
        ("Formats:", "US Letter, A4, A0, Projector"),
    ]
    by = hero_y + 64
    for label, val in badges:
        c.setFont("Poppins-Bold", 7)
        c.setFillColor(C_BURGUNDY)
        c.drawString(tx, by, label)
        c.setFont("Poppins-Regular", 7)
        c.setFillColor(C_DARK)
        c.drawString(tx + 75, by, val)
        by -= 14
        
    # Section Heading: 4 Instant Download Cards
    cards_top = hero_y - 18
    c.setFillColor(C_BURGUNDY)
    c.setFont("Poppins-Bold", 9)
    c.drawCentredString(W / 2, cards_top, "INSTANT DOWNLOAD · CHOOSE YOUR PATTERN FORMAT")
    
    c.setStrokeColor(C_BORDER)
    c.setLineWidth(0.6)
    c.line(46, cards_top - 6, W - 46, cards_top - 6)
    
    card_w = (W - 92 - 12) / 2
    card_h = 82
    row1_y = cards_top - 14 - card_h
    row2_y = row1_y - card_h - 10
    
    download_items = [
        {
            "format": "US LETTER · PRINT AT HOME",
            "tag": "NORTH AMERICA (US & CANADA)",
            "desc1": "Standard 8.5 x 11 in home printer format.",
            "desc2": "All 13 sizes + 4x4 in calibration square.",
            "btn_text": "Download US Letter Pack",
            "url": "https://drive.google.com/drive/folders/sewluxe-colette-trousers",
            "col": 0, "row": 0
        },
        {
            "format": "A4 · PRINT AT HOME",
            "tag": "UK, EUROPE & INTERNATIONAL",
            "desc1": "Standard 210 x 297 mm international format.",
            "desc2": "All 13 sizes + 10x10 cm calibration square.",
            "btn_text": "Download A4 Pack",
            "url": "https://drive.google.com/drive/folders/sewluxe-colette-trousers",
            "col": 1, "row": 0
        },
        {
            "format": "A0 · COPYSHOP WIDE FORMAT",
            "tag": "PROFESSIONAL PRINT SHOPS",
            "desc1": "Full-scale large sheets for PDFPlotting & copyshops.",
            "desc2": "Multi-Size Layered OCG + Single-size sheets.",
            "btn_text": "Download A0 Copyshop Pack",
            "url": "https://drive.google.com/drive/folders/sewluxe-colette-trousers",
            "col": 0, "row": 1
        },
        {
            "format": "PROJECTOR SEWING FILE",
            "tag": "CEILING & TABLE PROJECTORS",
            "desc1": "Single un-tiled canvas, 3.5pt thick cut lines.",
            "desc2": "1\" & metric calibration grids, toggleable layers.",
            "btn_text": "Download Projector File",
            "url": "https://drive.google.com/drive/folders/sewluxe-colette-trousers",
            "col": 1, "row": 1
        },
    ]
    
    for item in download_items:
        cx = 46 + item["col"] * (card_w + 12)
        cy = row1_y if item["row"] == 0 else row2_y
        
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.8)
        c.roundRect(cx, cy, card_w, card_h, 6, fill=1, stroke=1)
        
        c.setFillColor(C_BURGUNDY)
        c.roundRect(cx, cy, 4, card_h, 2, fill=1, stroke=0)
        
        c.setFillColor(C_BURGUNDY)
        c.setFont("Poppins-Bold", 8)
        c.drawString(cx + 12, cy + card_h - 15, item["format"])
        
        c.setFillColor(C_GOLD)
        c.setFont("Poppins-Medium", 6.5)
        c.drawString(cx + 12, cy + card_h - 26, item["tag"])
        
        c.setFillColor(C_MUTED)
        c.setFont("Poppins-Regular", 6.8)
        c.drawString(cx + 12, cy + card_h - 40, item["desc1"])
        c.drawString(cx + 12, cy + card_h - 50, item["desc2"])
        
        btn_w = 150
        btn_h = 18
        btn_x = cx + 12
        btn_y = cy + 10
        c.setFillColor(C_BURGUNDY)
        c.roundRect(btn_x, btn_y, btn_w, btn_h, 3, fill=1, stroke=0)
        c.setFillColor(C_WHITE)
        c.setFont("Poppins-Bold", 6.8)
        c.drawCentredString(btn_x + btn_w / 2, btn_y + 5, f"{item['btn_text']} →")
        c.linkURL(item["url"], (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h), relative=0)
        
    # Quick Start 3-Step Reminder
    qs_top = row2_y - 20
    c.setFillColor(C_BURGUNDY)
    c.setFont("Poppins-Bold", 8.5)
    c.drawString(46, qs_top, "QUICK-START PRINTING REMINDER")
    
    c.setStrokeColor(C_BORDER)
    c.setLineWidth(0.6)
    c.line(46, qs_top - 4, W - 46, qs_top - 4)
    
    step_w = (W - 92 - 16) / 3
    step_h = 68
    step_y = qs_top - 12 - step_h
    
    steps = [
        ("1. PRINT CALIBRATION PAGE", "Print Page 1 only at 100% Actual Size (uncheck 'Fit to Page'). Measure the 4x4\" (10x10cm) test square with a ruler."),
        ("2. CUT OR TILE TILES", "Trim right & bottom margins along dashed lines. Match grid codes (1/1, 1/2) and tape sheets with scotch tape."),
        ("3. SEW WITH BOOKLET", "Open your 16-page Luxury Sewing Booklet for full illustrated step-by-step guidance & video QR links.")
    ]
    for idx, (st_title, st_desc) in enumerate(steps):
        sx = 46 + idx * (step_w + 8)
        c.setFillColor(C_CONTAINER)
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.6)
        c.roundRect(sx, step_y, step_w, step_h, 5, fill=1, stroke=1)
        
        c.setFillColor(C_BURGUNDY)
        c.setFont("Poppins-Bold", 6.8)
        c.drawString(sx + 8, step_y + step_h - 14, st_title)
        
        c.setFillColor(C_MUTED)
        c.setFont("Poppins-Regular", 6.2)
        words = st_desc.split()
        line = ""
        ly = step_y + step_h - 26
        for w in words:
            test_line = line + " " + w if line else w
            if c.stringWidth(test_line, "Poppins-Regular", 6.2) < step_w - 16:
                line = test_line
            else:
                c.drawString(sx + 8, ly, line)
                ly -= 9.5
                line = w
        if line:
            c.drawString(sx + 8, ly, line)
            
    # Support Footer Banner
    foot_y = 44
    c.setFillColor(C_ACCENT_BG)
    c.setStrokeColor(C_BORDER)
    c.setLineWidth(0.6)
    c.roundRect(46, foot_y, W - 92, 42, 6, fill=1, stroke=1)
    
    c.setFillColor(C_BURGUNDY)
    c.setFont("Poppins-Bold", 7.8)
    c.drawString(58, foot_y + 26, "NEED HELP WITH YOUR DIGITAL PATTERN?")
    
    c.setFillColor(C_MUTED)
    c.setFont("Poppins-Regular", 6.8)
    c.drawString(58, foot_y + 12, "Message us on Etsy anytime for same-day assistance: etsy.com/shop/SewLuxePatterns")
    
    btn_s_w = 110
    btn_s_h = 22
    btn_s_x = W - 46 - btn_s_w - 12
    btn_s_y = foot_y + 10
    c.setFillColor(C_BURGUNDY)
    c.roundRect(btn_s_x, btn_s_y, btn_s_w, btn_s_h, 3, fill=1, stroke=0)
    c.setFillColor(C_WHITE)
    c.setFont("Poppins-Bold", 6.8)
    c.drawCentredString(btn_s_x + btn_s_w / 2, btn_s_y + 7, "Message Support →")
    c.linkURL("https://www.etsy.com/shop/SewLuxePatterns", (btn_s_x, btn_s_y, btn_s_x + btn_s_w, btn_s_y + btn_s_h), relative=0)
    
    c.save()
    print(f"[SUCCESS] Download Hub PDF created: {OUT_DESKTOP}")
    shutil.copy2(OUT_DESKTOP, OUT_BRAIN)
    print(f"  -> Copied to {OUT_BRAIN}")

if __name__ == "__main__":
    build_download_hub()
