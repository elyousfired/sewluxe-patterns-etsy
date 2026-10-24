#!/usr/bin/env python3
"""
draft_missing_panel.py
Procedural CAD generator for sewing techniques missing from Tailornova:
- Exposed zippers, custom welts, collarless facings, tailored vents.
- Renders true-to-pattern vector geometry with right/wrong fabric shading.
- Outputs 300 DPI Gold Standard #F5F2EF 2-panel or 1-panel layouts.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import pymupdf as fitz

FONTS_DIR = r"C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\fonts"
FONT_BOLD = os.path.join(FONTS_DIR, "Poppins-Bold.ttf")
FONT_MED = os.path.join(FONTS_DIR, "Poppins-Medium.ttf")
FONT_REG = os.path.join(FONTS_DIR, "Poppins-Regular.ttf")

def create_base_two_panel(width=2400, height=1200, title_1="1. STEP TITLE", title_2="2. STEP TITLE", sub_1="", sub_2=""):
    img = Image.new("RGBA", (width, height), (245, 242, 239, 255))
    draw = ImageDraw.Draw(img)

    # Outer rounded container
    draw.rounded_rectangle([15, 15, width - 15, height - 15], radius=32, fill="#F5F2EF", outline="#E2DDD8", width=3)

    # Inner boxes
    pw = 1115
    ph = 1100
    p1_x1, p1_y1 = 55, 50
    p2_x1, p2_y1 = 1230, 50

    draw.rectangle([p1_x1, p1_y1, p1_x1 + pw, p1_y1 + ph], fill="#FFFFFF", outline="#000000", width=4)
    draw.rectangle([p2_x1, p2_y1, p2_x1 + pw, p2_y1 + ph], fill="#FFFFFF", outline="#000000", width=4)

    # Fonts
    f_num = ImageFont.truetype(FONT_BOLD, 64)
    f_title = ImageFont.truetype(FONT_BOLD, 26)
    f_sub = ImageFont.truetype(FONT_MED, 17)

    # Header 1
    num1 = title_1.split(".")[0] + "." if "." in title_1 else "1."
    t1 = title_1.split(".", 1)[-1].strip() if "." in title_1 else title_1
    draw.text((p1_x1 + 40, p1_y1 + 25), num1, font=f_num, fill="#000000")
    draw.text((p1_x1 + 120, p1_y1 + 32), t1, font=f_title, fill="#111111")
    if sub_1:
        draw.text((p1_x1 + 120, p1_y1 + 70), sub_1, font=f_sub, fill="#666666")

    # Header 2
    num2 = title_2.split(".")[0] + "." if "." in title_2 else "2."
    t2 = title_2.split(".", 1)[-1].strip() if "." in title_2 else title_2
    draw.text((p2_x1 + 40, p2_y1 + 25), num2, font=f_num, fill="#000000")
    draw.text((p2_x1 + 120, p2_y1 + 32), t2, font=f_title, fill="#111111")
    if sub_2:
        draw.text((p2_x1 + 120, p2_y1 + 70), sub_2, font=f_sub, fill="#666666")

    return img

def render_svg_overlay_to_panel(base_img: Image.Image, svg_string: str, output_path: str):
    """Renders a transparent vector SVG overlay cleanly on top of the base frame."""
    doc = fitz.open(stream=svg_string.encode("utf-8"), filetype="svg")
    page = doc[0]
    pix = page.get_pixmap(dpi=72, alpha=True)
    overlay = Image.frombytes("RGBA", [pix.width, pix.height], pix.samples)
    if overlay.size != base_img.size:
        overlay = overlay.resize(base_img.size, Image.Resampling.LANCZOS)
    
    combined = Image.alpha_composite(base_img, overlay)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    combined.convert("RGB").save(output_path, quality=95)
    print(f"[OK] Saved procedural CAD panel: {output_path}")
    return output_path
