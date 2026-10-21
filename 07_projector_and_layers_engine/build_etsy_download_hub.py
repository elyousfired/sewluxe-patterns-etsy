#!/usr/bin/env python3
"""
build_etsy_download_hub.py
==========================
Generates the 1-Page Luxury Etsy Instant Download Hub PDF for Margot Elastic Wide-Leg Pants.
Features:
- SewLuxe atelier branding (Lora, Poppins, Olive #2D3728, Gold #C5A880, Alabaster #FAF8F5).
- Model photo & flat sketch thumbnails.
- 4 prominent, clickable download cards (US Letter, A4, A0 Copyshop, Projector File).
- 3-step printing and assembly quick-start reminder.
- 5-star customer support link.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

# Paths
FONTS_DIR = r"C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\fonts"
MODEL_PHOTO = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0\margot_olive_front_1792530617893.jpg"
FLAT_SKETCH = r"C:\Users\red1e\Desktop\SewLuxe_Elastic_Wide_Leg_Pants\01_Flat_Sketches\Elastic_Wide_Leg_Pants_Technical_Sketch.png"

OUT_DESKTOP = r"C:\Users\red1e\Desktop\SewLuxe_Elastic_Wide_Leg_Pants\07_Customer_Delivery_Guide\Margot_Elastic_Wide_Leg_Pants_Download_Hub.pdf"
OUT_BRAIN = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0\Margot_Elastic_Wide_Leg_Pants_Download_Hub.pdf"

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
C_OLIVE = colors.HexColor("#2D3728")
C_MUTED = colors.HexColor("#7C6E5E")
C_WHITE = colors.HexColor("#FFFFFF")
C_DARK = colors.HexColor("#1A1A1A")
C_ACCENT_BG = colors.HexColor("#ECE7E1")


def build_download_hub():
    W, H = A4  # 595.28 x 841.89
    c = canvas.Canvas(OUT_DESKTOP, pagesize=A4)
    
    # Background
    c.setFillColor(C_BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Double Luxury Border
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(1.2)
    c.rect(26, 26, W - 52, H - 52)
    
    c.setStrokeColor(C_OLIVE)
    c.setLineWidth(0.6)
    c.rect(32, 32, W - 64, H - 64)
    
    # Corner Gold Accents
    c.setFillColor(C_GOLD)
    for cx, cy in [(29, 29), (W - 29, 29), (29, H - 29), (W - 29, H - 29)]:
        c.circle(cx, cy, 2.2, fill=1, stroke=0)
        
    # Top Brand Header
    c.setFillColor(C_OLIVE)
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
        c.setStrokeColor(C_OLIVE)
        c.setLineWidth(0.8)
        c.rect(56, hero_y + 10, 138, 138, fill=0, stroke=1)
        
    # Flat Sketch Thumbnail
    if os.path.exists(FLAT_SKETCH):
        c.drawImage(FLAT_SKETCH, 204, hero_y + 10, width=110, height=138, preserveAspectRatio=True, anchor='c')
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.6)
        c.rect(204, hero_y + 10, 110, 138, fill=0, stroke=1)
        
    # Hero Text (Right of photos: tx = 326 to W-56)
    tx = 326
    c.setFillColor(C_GOLD)
    c.setFont("Poppins-Bold", 7.5)
    c.drawString(tx, hero_y + 134, "ATELIER SEWING PATTERN")
    
    c.setFillColor(C_OLIVE)
    c.setFont("Lora-Bold", 14)
    c.drawString(tx, hero_y + 116, "MARGOT WIDE-LEG")
    c.drawString(tx, hero_y + 100, "ELASTIC PANTS")
    
    c.setFillColor(C_MUTED)
    c.setFont("Lora-Italic", 8)
    c.drawString(tx, hero_y + 86, "Relaxed High-Rise · Pockets · Elastic Waist")
    
    # Key Badges
    badges = [
        ("Sizes Included:", "US 00 – 22 (XXS – 4XL)"),
        ("Seam Allowance:", "1 cm (3/8 in) Included"),
        ("Skill Level:", "Confident Beginner"),
        ("Formats:", "US Letter, A4, A0, Projector"),
    ]
    by = hero_y + 64
    for label, val in badges:
        c.setFont("Poppins-Bold", 7)
        c.setFillColor(C_OLIVE)
        c.drawString(tx, by, label)
        c.setFont("Poppins-Regular", 7)
        c.setFillColor(C_DARK)
        c.drawString(tx + 75, by, val)
        by -= 14
        
    # Section Heading: 4 Instant Download Cards
    cards_top = hero_y - 18
    c.setFillColor(C_OLIVE)
    c.setFont("Poppins-Bold", 9)
    c.drawCentredString(W / 2, cards_top, "INSTANT DOWNLOAD · CHOOSE YOUR PATTERN FORMAT")
    
    c.setStrokeColor(C_BORDER)
    c.setLineWidth(0.6)
    c.line(46, cards_top - 6, W - 46, cards_top - 6)
    
    # 4 Download Cards Grid (2 rows x 2 columns)
    card_w = (W - 92 - 12) / 2  # ~245 pt
    card_h = 82
    row1_y = cards_top - 14 - card_h
    row2_y = row1_y - card_h - 10
    
    download_items = [
        {
            "format": "US LETTER · PRINT AT HOME",
            "tag": "NORTH AMERICA (US & CANADA)",
            "desc": "Standard 8.5 x 11 in home printer format. All 13 sizes + 4x4 in calibration square.",
            "btn_text": "Download US Letter Pack",
            "url": "https://drive.google.com/drive/folders/sewluxe-margot-pants",
            "col": 0, "row": 0
        },
        {
            "format": "A4 · PRINT AT HOME",
            "tag": "UK, EUROPE & INTERNATIONAL",
            "desc": "Standard 210 x 297 mm international format. All 13 sizes + 10x10 cm calibration square.",
            "btn_text": "Download A4 Pack",
            "url": "https://drive.google.com/drive/folders/sewluxe-margot-pants",
            "col": 1, "row": 0
        },
        {
            "format": "A0 · COPYSHOP WIDE FORMAT",
            "tag": "PROFESSIONAL PRINT SHOPS",
            "desc": "Full-scale large sheets for PDFPlotting, Staples, or copyshops. Zero taping required.",
            "btn_text": "Download A0 Copyshop Pack",
            "url": "https://drive.google.com/drive/folders/sewluxe-margot-pants",
            "col": 0, "row": 1
        },
        {
            "format": "PROJECTOR SEWING FILE",
            "tag": "CEILING & TABLE PROJECTORS",
            "desc": "Single un-tiled canvas, 3.5pt thick cut lines, 1\" & 5cm calibration grids, toggleable layers.",
            "btn_text": "Download Projector File",
            "url": "https://drive.google.com/drive/folders/sewluxe-margot-pants",
            "col": 1, "row": 1
        },
    ]
    
    for item in download_items:
        cx = 46 + item["col"] * (card_w + 12)
        cy = row1_y if item["row"] == 0 else row2_y
        
        # Outer Card
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.8)
        c.roundRect(cx, cy, card_w, card_h, 6, fill=1, stroke=1)
        
        # Left Accent Bar
        c.setFillColor(C_OLIVE)
        c.roundRect(cx, cy, 4, card_h, 2, fill=1, stroke=0)
        
        # Card Header
        c.setFillColor(C_OLIVE)
        c.setFont("Poppins-Bold", 8)
        c.drawString(cx + 12, cy + card_h - 15, item["format"])
        
        # Region Tag
        c.setFillColor(C_GOLD)
        c.setFont("Poppins-Medium", 6.5)
        c.drawString(cx + 12, cy + card_h - 26, item["tag"])
        
        # Description
        c.setFillColor(C_MUTED)
        c.setFont("Poppins-Regular", 6.8)
        if item["col"] == 0 and item["row"] == 0:
            c.drawString(cx + 12, cy + card_h - 40, "Standard 8.5 x 11 in home printer format.")
            c.drawString(cx + 12, cy + card_h - 50, "All 13 sizes + 4x4 in calibration square.")
        elif item["col"] == 1 and item["row"] == 0:
            c.drawString(cx + 12, cy + card_h - 40, "Standard 210 x 297 mm international format.")
            c.drawString(cx + 12, cy + card_h - 50, "All 13 sizes + 10x10 cm calibration square.")
        elif item["col"] == 0 and item["row"] == 1:
            c.drawString(cx + 12, cy + card_h - 40, "Full-scale large sheets for PDFPlotting & copyshops.")
            c.drawString(cx + 12, cy + card_h - 50, "Zero home tiling or taping required.")
        else:
            c.drawString(cx + 12, cy + card_h - 40, "Single un-tiled canvas with 3.5pt thick lines.")
            c.drawString(cx + 12, cy + card_h - 50, "1\" & 5cm calibration grids + size layers.")
        
        # Clickable Button
        btn_w = card_w - 24
        btn_h = 18
        bx = cx + 12
        by = cy + 9
        
        c.setFillColor(C_CONTAINER)
        c.setStrokeColor(C_GOLD)
        c.setLineWidth(0.6)
        c.roundRect(bx, by, btn_w, btn_h, 4, fill=1, stroke=1)
        
        c.setFillColor(C_OLIVE)
        c.setFont("Poppins-Bold", 7.5)
        c.drawCentredString(bx + btn_w / 2, by + 5, f"↓  {item['btn_text']}")
        c.linkURL(item["url"], (bx, by, bx + btn_w, by + btn_h), relative=0)
        
    # Quick Start 3-Step Reminder Box
    steps_y = row2_y - 122
    steps_h = 106
    c.setFillColor(C_CONTAINER)
    c.setStrokeColor(C_BORDER)
    c.setLineWidth(0.8)
    c.roundRect(46, steps_y, W - 92, steps_h, 6, fill=1, stroke=1)
    
    c.setFillColor(C_OLIVE)
    c.setFont("Poppins-Bold", 8.5)
    c.drawString(58, steps_y + steps_h - 18, "3-STEP PRINTING & ASSEMBLY QUICK START")
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(0.6)
    c.line(58, steps_y + steps_h - 24, W - 58, steps_y + steps_h - 24)
    
    steps = [
        ("01", "Open with Adobe Acrobat Reader on a Computer", "Always open your PDF in free Adobe Acrobat Reader on Mac/PC (not phones/browsers) for 100% accurate scaling."),
        ("02", "Print Page 1 First at 100% Scale ('Actual Size')", "Never select 'Fit to Page'. Measure the 4x4 in (10x10 cm) test square with a physical ruler before printing remaining sheets."),
        ("03", "Follow the 16-Page Sewing Instruction Booklet", "Refer to Margot_Elastic_Wide_Leg_Pants_Sewing_Instructions.pdf for cutting layouts, step diagrams, and video tutorials."),
    ]
    
    sy = steps_y + steps_h - 43
    for num, title, detail in steps:
        # Number pill
        c.setFillColor(C_OLIVE)
        c.roundRect(58, sy - 2, 18, 14, 3, fill=1, stroke=0)
        c.setFillColor(C_WHITE)
        c.setFont("Poppins-Bold", 7.5)
        c.drawCentredString(67, sy + 2, num)
        
        # Step text
        c.setFillColor(C_DARK)
        c.setFont("Poppins-Bold", 7.5)
        c.drawString(82, sy + 3, title)
        
        c.setFillColor(C_MUTED)
        c.setFont("Poppins-Regular", 6.8)
        c.drawString(82, sy - 8, detail)
        
        sy -= 25
        
    # Customer Support & Care Footer Banner (Y: 52 to steps_y - 14)
    foot_y = 52
    foot_h = steps_y - 14 - foot_y
    c.setFillColor(C_WHITE)
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(0.8)
    c.roundRect(46, foot_y, W - 92, foot_h, 6, fill=1, stroke=1)
    
    c.setFillColor(C_OLIVE)
    c.setFont("Lora-Bold", 10.5)
    c.drawString(58, foot_y + foot_h - 24, "Need Help Downloading, Printing or Fitting?")
    
    c.setFillColor(C_MUTED)
    c.setFont("Poppins-Regular", 7.2)
    c.drawString(58, foot_y + foot_h - 42, "We are dedicated to your sewing success! If you have any questions regarding sizing, printing,")
    c.drawString(58, foot_y + foot_h - 54, "layers, or pattern adjustments, send us a direct message on Etsy. We respond quickly with expert help.")
    
    # Etsy Contact Button
    c_btn_w = 160
    c_btn_h = 26
    c_bx = W - 58 - c_btn_w
    c_by = foot_y + (foot_h - c_btn_h) / 2
    c.setFillColor(C_OLIVE)
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(0.6)
    c.roundRect(c_bx, c_by, c_btn_w, c_btn_h, 4, fill=1, stroke=1)
    
    c.setFillColor(C_WHITE)
    c.setFont("Poppins-Bold", 8)
    c.drawCentredString(c_bx + c_btn_w / 2, c_by + 9, "Message SewLuxe on Etsy →")
    c.linkURL("https://www.etsy.com/messages/new", (c_bx, c_by, c_bx + c_btn_w, c_by + c_btn_h), relative=0)
    
    c.save()
    print("Built Download Hub PDF successfully at:", OUT_DESKTOP)


if __name__ == "__main__":
    build_download_hub()
    import shutil
    shutil.copy(OUT_DESKTOP, OUT_BRAIN)
    print("Copied to Brain at:", OUT_BRAIN)
