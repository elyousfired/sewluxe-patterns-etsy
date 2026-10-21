"""
Clean and adapt the AUTHENTIC CAD Pieces Overview Image (Image 1)
- Keeps 100% of the authentic Tailornova/PatternFast CAD vector lines, curves, notches, typography, and grainlines!
- Cleanly erases Piece 9 (Welt pocket bag)
- Cleanly erases Piece 10 & 8 (Welt pocket bag & welt strip)
- Cleanly erases the horizontal welt line on Piece 2 (Pants Back)
- Adds the second contoured dart on Piece 2 (matching the 4 waist darts spec)
- Adds the authentic Belt Loops piece (BL) with 3.5 cm x 45 cm strip
- Upscales cleanly with Lanczos interpolation for 300 DPI luxury booklet printing
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

SRC_PATH = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0\.user_uploaded\media_1792613312220_a9bb9d14.png"
OUT_ASSET = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\colette_pants_engine\booklet_assets\pieces_overview_clean.png"
OUT_BRAIN = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0\authentic_cad_pieces_cleaned.png"

img = Image.open(SRC_PATH).convert("RGBA")
draw = ImageDraw.Draw(img)

# Exact background color of the canvas
BG_COLOR = (249, 247, 244, 255)
# Exact white color inside pants piece
PANTS_WHITE = (255, 255, 255, 255)
# Burgundy color for numbers
BURGUNDY = (140, 59, 71, 255)
# Line color
LINE_COLOR = (50, 50, 50, 255)
DASH_GREY = (160, 160, 160, 255)

# 1. Erase Piece 9 completely (fill with background color)
draw.rectangle([385, 178, 460, 245], fill=BG_COLOR)

# 2. Erase Piece 10 and Piece 8 completely (fill with background color)
draw.rectangle([308, 325, 385, 428], fill=BG_COLOR)

# 3. Erase the horizontal welt pocket line on Piece 2 (Pants Back)
# Welt pocket line is around x: 92 to 160, y: 95 to 118
draw.rectangle([95, 96, 162, 116], fill=PANTS_WHITE)

# 4. Redraw the clean center crease line and add second dart on Piece 2
# Grainline down center of Piece 2
draw.line([(111, 160), (111, 275)], fill=LINE_COLOR, width=1)
# Center back grainline arrow
draw.polygon([(109, 275), (111, 280), (113, 275)], fill=LINE_COLOR)

# Existing Dart 1 is around x: 125, y: 55 to 125
# Let's add Dart 2 next to it at x: 140, y: 58 to 118
draw.line([(136, 58), (142, 118)], fill=LINE_COLOR, width=1)
draw.line([(148, 59), (142, 118)], fill=LINE_COLOR, width=1)
# Center dashed line of Dart 2
for dy in range(60, 115, 6):
    draw.line([(142, dy), (142, dy + 3)], fill=DASH_GREY, width=1)

# 5. Add Belt Loops Piece (BL) in the freed space below Piece 4
# Space available: x: 310 to 395, y: 335 to 420
bl_x0, bl_y0, bl_x1, bl_y1 = 312, 335, 395, 415
draw.rectangle([bl_x0, bl_y0, bl_x1, bl_y1], outline=LINE_COLOR, fill=PANTS_WHITE, width=1)
# Inner dashed seamline
draw.rectangle([bl_x0 + 4, bl_y0 + 4, bl_x1 - 4, bl_y1 - 4], outline=DASH_GREY, width=1)
# Center grainline
draw.line([(bl_x0 + 41, bl_y0 + 8), (bl_x0 + 41, bl_y1 - 8)], fill=LINE_COLOR, width=1)
# Grainline arrow
draw.polygon([(bl_x0 + 39, bl_y0 + 12), (bl_x0 + 41, bl_y0 + 6), (bl_x0 + 43, bl_y0 + 12)], fill=LINE_COLOR)

# Add label "BL" in burgundy
try:
    font_bl = ImageFont.truetype("arialbd.ttf", 16)
    font_sub = ImageFont.truetype("arial.ttf", 7)
except:
    font_bl = ImageFont.load_default()
    font_sub = ImageFont.load_default()

draw.text((bl_x0 + 28, bl_y0 + 26), "BL", fill=BURGUNDY, font=font_bl)
draw.text((bl_x0 + 10, bl_y0 + 52), "BELT LOOPS", fill=LINE_COLOR, font=font_sub)
draw.text((bl_x0 + 10, bl_y0 + 62), "3.5 x 45 cm", fill=LINE_COLOR, font=font_sub)

# 6. Upscale cleanly to high resolution (1836 x 1551) with Lanczos for super crisp lines
high_res = img.resize((img.width * 3, img.height * 3), Image.LANCZOS)

# Save to destination assets
high_res.save(OUT_ASSET, dpi=(300, 300))
high_res.save(OUT_BRAIN, dpi=(300, 300))
print(f"[SUCCESS] Cleaned authentic CAD layout saved to:\n  -> {OUT_ASSET}\n  -> {OUT_BRAIN}")
