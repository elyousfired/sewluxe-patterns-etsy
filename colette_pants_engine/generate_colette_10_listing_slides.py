#!/usr/bin/env python3
"""
generate_colette_10_listing_slides.py
=====================================
Generates all 10 high-converting Etsy listing slides (2000x2000 px) for:
SewLuxe Colette Double-Pleated Palazzo Trousers.
Renders pixel-perfect HTML/CSS templates via Playwright Chromium.
"""

import base64
import json
import os
import shutil
from playwright.sync_api import sync_playwright

BRAIN_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0"
ENGINE_DIR = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\colette_pants_engine"
DESKTOP_DIR = r"C:\Users\red1e\Desktop\SewLuxe_Colette_Tailored_Pants"
SLIDES_DIR = os.path.join(DESKTOP_DIR, "05_Etsy_Listing_Images")
FONTS_DIR = r"C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\fonts"
SCRATCH_DIR = os.path.join(ENGINE_DIR, "slides_html")

os.makedirs(SLIDES_DIR, exist_ok=True)
os.makedirs(SCRATCH_DIR, exist_ok=True)

def to_data_uri(path: str, mime: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"

# Load Fonts
font_lora_reg = to_data_uri(os.path.join(FONTS_DIR, "Lora-Regular.ttf"), "font/ttf")
font_lora_bold = to_data_uri(os.path.join(FONTS_DIR, "Lora-Bold.ttf"), "font/ttf")
font_lora_italic = to_data_uri(os.path.join(FONTS_DIR, "Lora-Italic.ttf"), "font/ttf")
font_pop_reg = to_data_uri(os.path.join(FONTS_DIR, "Poppins-Regular.ttf"), "font/ttf")
font_pop_med = to_data_uri(os.path.join(FONTS_DIR, "Poppins-Medium.ttf"), "font/ttf")
font_pop_bold = to_data_uri(os.path.join(FONTS_DIR, "Poppins-Bold.ttf"), "font/ttf")

# Load Images
photo1_uri = to_data_uri(os.path.join(BRAIN_DIR, "colette_photo_01_front.jpg"), "image/jpeg")
photo2_uri = to_data_uri(os.path.join(BRAIN_DIR, "colette_photo_02_side.jpg"), "image/jpeg")
photo3_uri = to_data_uri(os.path.join(BRAIN_DIR, "colette_photo_03_back.jpg"), "image/jpeg")

sketch_sidebyside_uri = to_data_uri(os.path.join(BRAIN_DIR, "Colette_Sketch_SideBySide.png"), "image/png")
sketch_front_uri = to_data_uri(os.path.join(BRAIN_DIR, "Colette_Sticker_Front.png"), "image/png")
sketch_back_uri = to_data_uri(os.path.join(BRAIN_DIR, "Colette_Sticker_Back.png"), "image/png")

bp1_uri = to_data_uri(os.path.join(BRAIN_DIR, "booklet_preview_p1.png"), "image/png")
bp8_uri = to_data_uri(os.path.join(BRAIN_DIR, "booklet_preview_p8.png"), "image/png")
bp9_uri = to_data_uri(os.path.join(BRAIN_DIR, "booklet_preview_p9.png"), "image/png")
bp15_uri = to_data_uri(os.path.join(BRAIN_DIR, "booklet_preview_p15.png"), "image/png")
bp16_uri = to_data_uri(os.path.join(BRAIN_DIR, "booklet_preview_p16.png"), "image/png")
hub_uri = to_data_uri(os.path.join(BRAIN_DIR, "hub_preview.png"), "image/png")

BASE_CSS = f"""
@font-face {{ font-family: 'Lora'; src: url('{font_lora_reg}') format('truetype'); font-weight: 400; }}
@font-face {{ font-family: 'Lora'; src: url('{font_lora_bold}') format('truetype'); font-weight: 700; }}
@font-face {{ font-family: 'Lora'; src: url('{font_lora_italic}') format('truetype'); font-weight: 400; font-style: italic; }}
@font-face {{ font-family: 'Poppins'; src: url('{font_pop_reg}') format('truetype'); font-weight: 400; }}
@font-face {{ font-family: 'Poppins'; src: url('{font_pop_med}') format('truetype'); font-weight: 500; }}
@font-face {{ font-family: 'Poppins'; src: url('{font_pop_bold}') format('truetype'); font-weight: 700; }}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    width: 2000px;
    height: 2000px;
    overflow: hidden;
    background: #FAF8F5;
    font-family: 'Poppins', sans-serif;
    color: #1E1A19;
    position: relative;
}}
.top-accent-bar {{
    position: absolute;
    top: 0;
    left: 0;
    width: 2000px;
    height: 20px;
    background: #8C3B47;
    z-index: 100;
}}
.slide-header {{
    text-align: center;
    padding-top: 65px;
    margin-bottom: 40px;
}}
.slide-kicker {{
    font-size: 24px;
    font-weight: 500;
    letter-spacing: 10px;
    color: #8C3B47;
    text-transform: uppercase;
    margin-bottom: 12px;
}}
.slide-title {{
    font-family: 'Lora', serif;
    font-size: 80px;
    font-weight: 700;
    color: #1E1A19;
    line-height: 1.1;
}}
.slide-sub {{
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 32px;
    color: #6E655F;
    margin-top: 8px;
}}
.gold-line {{
    width: 140px;
    height: 4px;
    background: #C5A880;
    margin: 18px auto 0 auto;
    border-radius: 2px;
}}
"""

# =============================================================================
# SLIDE 1: HERO COVER (2000x2000)
# =============================================================================
slide1_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s1-wrap {{ display: flex; width: 2000px; height: 2000px; }}
.s1-left {{ width: 1160px; height: 2000px; position: relative; overflow: hidden; }}
.s1-left img {{ width: 100%; height: 100%; object-fit: cover; object-position: center; }}
.s1-right {{
    width: 840px; height: 2000px; background: #FAF8F5;
    display: flex; flex-direction: column; align-items: center;
    padding: 85px 60px 60px 60px; position: relative;
    border-left: 3px solid #E2DDD8;
}}
.s1-kicker {{ font-size: 26px; font-weight: 500; letter-spacing: 8px; color: #8C3B47; text-transform: uppercase; margin-bottom: 14px; }}
.s1-title {{ font-family: 'Lora', serif; font-size: 135px; font-weight: 700; color: #1E1A19; line-height: 1.0; margin-bottom: 8px; }}
.s1-subtitle {{ font-size: 36px; font-weight: 600; letter-spacing: 14px; color: #8C3B47; text-transform: uppercase; margin-bottom: 20px; }}
.s1-rule {{ width: 160px; height: 4px; background: #C5A880; margin-bottom: 30px; border-radius: 2px; }}
.s1-sketch {{ width: 660px; height: 720px; display: flex; align-items: center; justify-content: center; margin-bottom: 30px; }}
.s1-sketch img {{ max-width: 100%; max-height: 100%; object-fit: contain; filter: drop-shadow(0 15px 25px rgba(0,0,0,0.06)); }}
.s1-badges {{ width: 100%; display: flex; flex-direction: column; gap: 16px; margin-bottom: auto; }}
.s1-badge {{
    background: #FFFFFF; border: 2px solid #E2DDD8; border-left: 8px solid #8C3B47;
    border-radius: 12px; padding: 20px 28px; display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 6px 16px rgba(0,0,0,0.03);
}}
.s1-badge-lbl {{ font-size: 21px; font-weight: 600; letter-spacing: 3px; color: #8C3B47; text-transform: uppercase; }}
.s1-badge-val {{ font-size: 25px; font-weight: 700; color: #1E1A19; }}
.s1-footer {{ text-align: center; margin-top: 25px; }}
.s1-pill {{ background: #1E1A19; color: #FFFFFF; font-size: 20px; font-weight: 600; letter-spacing: 5px; padding: 12px 35px; border-radius: 30px; display: inline-block; margin-bottom: 14px; }}
.s1-brand {{ font-family: 'Lora', serif; font-style: italic; font-size: 42px; color: #8C3B47; }}
</style></head>
<body>
<div class="top-accent-bar"></div>
<div class="s1-wrap">
    <div class="s1-left"><img src="{photo1_uri}" /></div>
    <div class="s1-right">
        <div class="s1-kicker">ATELIER SEWING PATTERN</div>
        <div class="s1-title">Colette</div>
        <div class="s1-subtitle">PALAZZO TROUSERS</div>
        <div class="s1-rule"></div>
        <div class="s1-sketch"><img src="{sketch_front_uri}" /></div>
        <div class="s1-badges">
            <div class="s1-badge"><span class="s1-badge-lbl">SIZES INCLUDED</span><span class="s1-badge-val">US 00 – 22 (13 SIZES)</span></div>
            <div class="s1-badge"><span class="s1-badge-lbl">TAILORED DETAILS</span><span class="s1-badge-val">DOUBLE PLEATS & CREASES</span></div>
            <div class="s1-badge"><span class="s1-badge-lbl">WAIST CLOSURE</span><span class="s1-badge-val">CONCEALED HOOK & BAR</span></div>
            <div class="s1-badge"><span class="s1-badge-lbl">PRINT FORMATS</span><span class="s1-badge-val">A4 · LETTER · A0 · PROJECTOR</span></div>
        </div>
        <div class="s1-footer">
            <div class="s1-pill">INSTANT DIGITAL DOWNLOAD</div><br/>
            <span class="s1-brand">SewLuxePatterns</span>
        </div>
    </div>
</div>
</body></html>"""

# =============================================================================
# SLIDE 2: MULTI-ANGLE EDITORIAL SHOWCASE (2000x2000)
# =============================================================================
slide2_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s2-grid {{
    display: grid; grid-template-columns: repeat(3, 580px); gap: 40px;
    padding: 0 70px; margin-top: 30px;
}}
.s2-card {{
    background: #FFFFFF; border: 2px solid #E2DDD8; border-radius: 18px;
    overflow: hidden; box-shadow: 0 15px 35px rgba(0,0,0,0.04);
}}
.s2-img {{ width: 580px; height: 1250px; overflow: hidden; }}
.s2-img img {{ width: 100%; height: 100%; object-fit: cover; }}
.s2-info {{ padding: 35px 30px; background: #FFFFFF; text-align: center; border-top: 2px solid #E2DDD8; }}
.s2-num {{ font-size: 20px; font-weight: 600; letter-spacing: 5px; color: #8C3B47; text-transform: uppercase; margin-bottom: 8px; }}
.s2-h {{ font-family: 'Lora', serif; font-size: 38px; font-weight: 700; color: #1E1A19; margin-bottom: 10px; }}
.s2-p {{ font-size: 22px; color: #6E655F; line-height: 1.4; }}
</style></head>
<body>
<div class="top-accent-bar"></div>
<div class="slide-header">
    <div class="slide-kicker">360° RUNWAY PROPORTIONS</div>
    <div class="slide-title">Effortless Quiet-Luxury Silhouette</div>
    <div class="slide-sub">Double pleats, razor-sharp creases, and sweeping palazzo legs</div>
    <div class="gold-line"></div>
</div>
<div class="s2-grid">
    <div class="s2-card">
        <div class="s2-img"><img src="{photo1_uri}" /></div>
        <div class="s2-info">
            <div class="s2-num">VIEW 01 · FRONT</div>
            <div class="s2-h">Tailored Front Waist</div>
            <div class="s2-p">Double forward pleats, razor-sharp vertical creases, and clean concealed closure.</div>
        </div>
    </div>
    <div class="s2-card">
        <div class="s2-img"><img src="{photo2_uri}" /></div>
        <div class="s2-info">
            <div class="s2-num">VIEW 02 · 45° ANGLE</div>
            <div class="s2-h">Fluid Waterfall Drape</div>
            <div class="s2-p">Deep slanted hip pockets and generous wide palazzo leg cascading to floor length.</div>
        </div>
    </div>
    <div class="s2-card">
        <div class="s2-img"><img src="{photo3_uri}" /></div>
        <div class="s2-info">
            <div class="s2-num">VIEW 03 · REAR</div>
            <div class="s2-h">Clean Pocketless Back</div>
            <div class="s2-p">Four contoured waist darts shaping smoothly over the hips with zero bulky pockets.</div>
        </div>
    </div>
</div>
</body></html>"""

# =============================================================================
# SLIDE 3: MASTER TECHNICAL FLAT SKETCH & CALLOUTS (2000x2000)
# =============================================================================
slide3_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s3-wrap {{ display: flex; padding: 20px 80px; gap: 60px; align-items: center; justify-content: center; }}
.s3-sketch-box {{
    width: 960px; height: 1380px; background: #FFFFFF; border: 3px solid #E2DDD8;
    border-radius: 24px; padding: 40px; display: flex; align-items: center; justify-content: center;
    box-shadow: 0 15px 35px rgba(0,0,0,0.05);
}}
.s3-sketch-box img {{ max-width: 100%; max-height: 100%; object-fit: contain; }}
.s3-callouts {{ width: 800px; display: flex; flex-direction: column; gap: 24px; }}
.s3-card {{
    background: #FFFFFF; border: 2px solid #E2DDD8; border-left: 8px solid #8C3B47;
    border-radius: 16px; padding: 26px 30px; box-shadow: 0 8px 20px rgba(0,0,0,0.03);
}}
.s3-card-h {{ font-size: 26px; font-weight: 700; color: #8C3B47; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 2px; }}
.s3-card-p {{ font-size: 23px; color: #2C2624; line-height: 1.45; }}
</style></head>
<body>
<div class="top-accent-bar"></div>
<div class="slide-header">
    <div class="slide-kicker">PRECISION CAD SCHEMATICS</div>
    <div class="slide-title">1:1 Technical Flat Sketch</div>
    <div class="slide-sub">Engineered to match real pattern pieces with 100% anatomical accuracy</div>
    <div class="gold-line"></div>
</div>
<div class="s3-wrap">
    <div class="s3-sketch-box"><img src="{sketch_sidebyside_uri}" /></div>
    <div class="s3-callouts">
        <div class="s3-card">
            <div class="s3-card-h">1. Concealed Waist Closure</div>
            <div class="s3-card-p">Concealed trouser hook & bar on inside extension tab. <b>Zero exterior button</b> on waistband for a smooth luxury front.</div>
        </div>
        <div class="s3-card">
            <div class="s3-card-h">2. 5 Tailored Belt Loops</div>
            <div class="s3-card-p">2 front loops aligned directly over pleats & creases, 2 over pocket tops, and 1 centered at back seam.</div>
        </div>
        <div class="s3-card">
            <div class="s3-card-h">3. Double Forward Pleats</div>
            <div class="s3-card-p">Deep tailored pleats releasing volume into fluid leg drape with razor-sharp center creases down to hem.</div>
        </div>
        <div class="s3-card">
            <div class="s3-card-h">4. Slanted Hip Pockets</div>
            <div class="s3-card-p">Deep Italian slant pockets reinforced with stay-tape to prevent gaping when walking.</div>
        </div>
        <div class="s3-card">
            <div class="s3-card-h">5. Clean Pocketless Rear</div>
            <div class="s3-card-p">4 contoured waist darts (2 per side) shaping the seat smoothly without bulky pockets.</div>
        </div>
        <div class="s3-card">
            <div class="s3-card-h">6. Deep 5.0 cm (2.0 in) Weighted Hem</div>
            <div class="s3-card-p">Generous fold-up hem adding substantial downward weight for dramatic palazzo sweep.</div>
        </div>
    </div>
</div>
</body></html>"""

# =============================================================================
# SLIDE 4: SIZE CHART & FINISHED MEASUREMENTS (2000x2000)
# =============================================================================
slide4_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s4-wrap {{ padding: 10px 80px 0 80px; }}
.s4-table-card {{
    background: #FFFFFF; border: 2px solid #E2DDD8; border-radius: 20px;
    padding: 35px 40px; margin-bottom: 35px; box-shadow: 0 10px 30px rgba(0,0,0,0.03);
}}
.s4-table-title {{ font-size: 28px; font-weight: 700; color: #8C3B47; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 20px; }}
table {{ width: 100%; border-collapse: collapse; text-align: center; }}
th {{ background: #1E1A19; color: #FFFFFF; font-size: 20px; font-weight: 600; padding: 14px 10px; letter-spacing: 2px; }}
td {{ font-size: 20px; color: #2C2624; padding: 10.5px 8px; border-bottom: 1px solid #ECE7E1; }}
tr:nth-child(even) td {{ background: #F8F5F0; }}
.s4-note {{ font-size: 20px; font-style: italic; color: #6E655F; text-align: center; margin-top: 15px; }}
</style></head>
<body>
<div class="top-accent-bar"></div>
<div class="slide-header">
    <div class="slide-kicker">INCLUSIVE SIZE SPECTRUM</div>
    <div class="slide-title">Body & Finished Garment Charts</div>
    <div class="slide-sub">Standard North American Alvanon Fit · Sizes US 00 to 22 (XXS to 4XL)</div>
    <div class="gold-line"></div>
</div>
<div class="s4-wrap">
    <div class="s4-table-card">
        <div class="s4-table-title">1. Body Measurements Guide</div>
        <table>
            <tr><th>US SIZE</th><th>LETTER</th><th>WAIST (IN)</th><th>WAIST (CM)</th><th>HIPS (IN)</th><th>HIPS (CM)</th></tr>
            <tr><td>00</td><td>XXS</td><td>25.0"</td><td>63.5 cm</td><td>34.5"</td><td>87.8 cm</td></tr>
            <tr><td>0 – 2</td><td>XS</td><td>26.0" – 27.1"</td><td>66.0 – 68.8 cm</td><td>35.5" – 36.5"</td><td>90.3 – 92.8 cm</td></tr>
            <tr><td>4 – 6</td><td>S</td><td>28.0" – 29.0"</td><td>71.3 – 73.8 cm</td><td>37.5" – 38.6"</td><td>95.3 – 98.0 cm</td></tr>
            <tr><td>8 – 10</td><td>M</td><td>30.0" – 31.0"</td><td>76.3 – 78.8 cm</td><td>39.5" – 40.5"</td><td>100.3 – 102.8 cm</td></tr>
            <tr><td>12 – 14</td><td>L</td><td>32.6" – 34.5"</td><td>82.8 – 87.5 cm</td><td>41.9" – 43.8"</td><td>106.5 – 111.0 cm</td></tr>
            <tr><td>16</td><td>XL</td><td>36.8"</td><td>93.3 cm</td><td>45.5"</td><td>115.5 cm</td></tr>
            <tr><td>18 – 20</td><td>2XL–3XL</td><td>39.0" – 41.3"</td><td>99.0 – 104.8 cm</td><td>47.5" – 49.5"</td><td>120.8 – 125.8 cm</td></tr>
            <tr><td>22</td><td>4XL</td><td>43.5"</td><td>110.5 cm</td><td>51.5"</td><td>130.8 cm</td></tr>
        </table>
    </div>
    <div class="s4-table-card">
        <div class="s4-table-title">2. Finished Garment Measurements</div>
        <table>
            <tr><th>US SIZE</th><th>FINISHED WAIST</th><th>FINISHED HIPS*</th><th>LEG SWEEP (CIRC.)</th><th>FINISHED INSEAM</th></tr>
            <tr><td>00 – 0</td><td>25.5" – 26.5" (65–67 cm)</td><td>35.5" – 36.5" (90–93 cm)</td><td>23.8" – 24.4" (60–62 cm)</td><td>28.7" (73 cm)</td></tr>
            <tr><td>2 – 4</td><td>27.6" – 28.6" (70–73 cm)</td><td>37.4" – 38.4" (95–97 cm)</td><td>25.0" – 25.6" (64–65 cm)</td><td>28.3" (72 cm)</td></tr>
            <tr><td>6 – 8</td><td>29.6" – 30.6" (75–78 cm)</td><td>39.4" – 40.3" (100–102 cm)</td><td>26.4" – 27.0" (67–69 cm)</td><td>27.8" (71 cm)</td></tr>
            <tr><td>10 – 12</td><td>31.6" – 33.3" (80–84 cm)</td><td>41.1" – 42.4" (104–108 cm)</td><td>27.6" – 28.5" (70–73 cm)</td><td>27.6" (70 cm)</td></tr>
            <tr><td>14 – 16</td><td>35.1" – 37.5" (89–95 cm)</td><td>44.0" – 45.6" (112–116 cm)</td><td>29.8" – 30.9" (75–78 cm)</td><td>27.4" (69 cm)</td></tr>
            <tr><td>18 – 20</td><td>39.8" – 42.1" (101–107 cm)</td><td>49.6" – 52.0" (126–132 cm)</td><td>33.4" – 34.9" (85–89 cm)</td><td>26.8" (68 cm)</td></tr>
            <tr><td>22</td><td>44.4" (113 cm)</td><td>54.3" (138 cm)</td><td>36.5" (93 cm)</td><td>26.4" (67 cm)</td></tr>
        </table>
    </div>
    <div class="s4-note">* Finished hips measured with pleats pressed flat. Generous living ease built into palazzo silhouette.</div>
</div>
</body></html>"""

# =============================================================================
# SLIDE 5: FABRIC REQUIREMENTS & NOTIONS (2000x2000)
# =============================================================================
slide5_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s5-grid {{ display: grid; grid-template-columns: 920px 920px; gap: 40px; padding: 20px 60px; }}
.s5-card {{
    background: #FFFFFF; border: 2px solid #E2DDD8; border-radius: 20px;
    padding: 40px 45px; box-shadow: 0 10px 30px rgba(0,0,0,0.03);
}}
.s5-card-h {{ font-size: 28px; font-weight: 700; color: #8C3B47; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 25px; border-bottom: 2px solid #E2DDD8; padding-bottom: 15px; }}
.s5-p {{ font-size: 23px; color: #2C2624; line-height: 1.5; margin-bottom: 20px; }}
.s5-row {{ display: flex; justify-content: space-between; padding: 14px 0; border-bottom: 1px solid #ECE7E1; font-size: 23px; }}
.s5-row-lbl {{ font-weight: 600; color: #8C3B47; }}
.s5-row-val {{ font-weight: 700; color: #1E1A19; }}
.s5-item {{ margin-bottom: 18px; }}
.s5-item-t {{ font-size: 23px; font-weight: 700; color: #1E1A19; margin-bottom: 4px; }}
.s5-item-d {{ font-size: 21px; color: #6E655F; line-height: 1.4; }}
</style></head>
<body>
<div class="top-accent-bar"></div>
<div class="slide-header">
    <div class="slide-kicker">MATERIALS SPECIFICATION</div>
    <div class="slide-title">Fabric Recommendations & Notions</div>
    <div class="slide-sub">Curated for fluid drape, weight, and timeless quiet-luxury elegance</div>
    <div class="gold-line"></div>
</div>
<div class="s5-grid">
    <div class="s5-card">
        <div class="s5-card-h">Recommended Textiles</div>
        <div class="s5-p">Medium-weight woven fabrics with fluid, elegant drape (180–280 gsm):</div>
        <div class="s5-item">
            <div class="s5-item-t">• Washed Linen-Viscose Melange</div>
            <div class="s5-item-d">Two-tone slub texture with soft crinkle and heavy fluid drape.</div>
        </div>
        <div class="s5-item">
            <div class="s5-item-t">• Tencel / Lyocell Twill</div>
            <div class="s5-item-d">Silky matte texture with exceptional fluid movement.</div>
        </div>
        <div class="s5-item">
            <div class="s5-item-t">• Tropical Wool Gabardine / Crepe</div>
            <div class="s5-item-d">Classic four-season tailoring fabric holding razor-sharp pleats.</div>
        </div>
        <div class="s5-card-h" style="margin-top: 30px;">Fabric Yardage (With 10% Buffer)</div>
        <div class="s5-row"><span class="s5-row-lbl">Sizes 00 – 08 (60" / 150cm Width)</span><span class="s5-row-val">2.60 m (2.85 yds)</span></div>
        <div class="s5-row"><span class="s5-row-lbl">Sizes 10 – 14 (60" / 150cm Width)</span><span class="s5-row-val">2.85 m (3.10 yds)</span></div>
        <div class="s5-row"><span class="s5-row-lbl">Sizes 16 – 22 (60" / 150cm Width)</span><span class="s5-row-val">3.20 m (3.50 yds)</span></div>
        <div class="s5-row"><span class="s5-row-lbl">All Sizes (45" / 115cm Width)</span><span class="s5-row-val">3.40 – 4.10 m (3.75 – 4.5 yds)</span></div>
    </div>
    <div class="s5-card">
        <div class="s5-card-h">Notions & Tailoring Hardware</div>
        <div class="s5-item">
            <div class="s5-item-t">• Concealed Trouser Hook & Bar</div>
            <div class="s5-item-d">1x heavy-duty metal hook & bar closure for inside waistband extension + 1x optional flat anchor button.</div>
        </div>
        <div class="s5-item">
            <div class="s5-item-t">• Trouser Zipper</div>
            <div class="s5-item-d">1x nylon coil or metal trouser zipper (18–20 cm / 7–8 in).</div>
        </div>
        <div class="s5-item">
            <div class="s5-item-t">• Fusible Interfacing</div>
            <div class="s5-item-d">0.50 m lightweight woven interfacing for waistband & fly facing.</div>
        </div>
        <div class="s5-item">
            <div class="s5-item-t">• Pocket Stay-Tape</div>
            <div class="s5-item-d">0.50 m bias stay-tape to prevent slant pocket edge from stretching.</div>
        </div>
        <div class="s5-item">
            <div class="s5-item-t">• Pocket Lining Fabric</div>
            <div class="s5-item-d">0.40 m lightweight cotton voile or Bemberg lining for flat pockets.</div>
        </div>
        <div class="s5-item">
            <div class="s5-item-t">• Thread & Tools</div>
            <div class="s5-item-d">All-purpose polyester thread, zipper foot, tailor's ham & steam iron.</div>
        </div>
    </div>
</div>
</body></html>"""

# =============================================================================
# SLIDE 6: COMPLETE TURNKEY BUNDLE BREAKDOWN (2000x2000)
# =============================================================================
slide6_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s6-grid {{ display: grid; grid-template-columns: repeat(2, 900px); gap: 40px; padding: 20px 80px; justify-content: center; }}
.s6-card {{
    background: #FFFFFF; border: 2px solid #E2DDD8; border-radius: 20px;
    padding: 35px 40px; display: flex; gap: 30px; align-items: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.03);
}}
.s6-icon {{
    width: 90px; height: 90px; background: #FAF8F5; border: 2px solid #8C3B47;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-family: 'Lora', serif; font-size: 38px; font-weight: 700; color: #8C3B47; flex-shrink: 0;
}}
.s6-body h3 {{ font-size: 26px; font-weight: 700; color: #1E1A19; margin-bottom: 6px; }}
.s6-body p {{ font-size: 21px; color: #6E655F; line-height: 1.4; }}
</style></head>
<body>
<div class="top-accent-bar"></div>
<div class="slide-header">
    <div class="slide-kicker">COMPLETE TURNKEY PACKAGE</div>
    <div class="slide-title">What You Receive With Your Order</div>
    <div class="slide-sub">Instant high-resolution digital download · Everything included</div>
    <div class="gold-line"></div>
</div>
<div class="s6-grid">
    <div class="s6-card">
        <div class="s6-icon">16</div>
        <div class="s6-body">
            <h3>16-Page Luxury Illustrated Booklet</h3>
            <p>Step-by-step illustrated construction guide with gold standard framed diagrams, size tables, and fabric layouts.</p>
        </div>
    </div>
    <div class="s6-card">
        <div class="s6-icon">39</div>
        <div class="s6-body">
            <h3>Full Single-Size PDF Suite (39 Files)</h3>
            <p>Individual files for every size (US 00–22) in A4, US Letter, and A0 CopyShop with 4x4" calibration test squares.</p>
        </div>
    </div>
    <div class="s6-card">
        <div class="s6-icon">A0</div>
        <div class="s6-body">
            <h3>Multi-Size Layered A0 Copyshop PDF</h3>
            <p>All 13 sizes nested on master A0 sheets with toggleable Adobe Acrobat layers (OCG). Print only the size you need!</p>
        </div>
    </div>
    <div class="s6-card">
        <div class="s6-icon">PR</div>
        <div class="s6-body">
            <h3>Dedicated High-Contrast Projector File</h3>
            <p>Ultra-thick vector lines, 1" & metric calibration targets, and individual size layers for table/ceiling projection.</p>
        </div>
    </div>
    <div class="s6-card">
        <div class="s6-icon">QR</div>
        <div class="s6-body">
            <h3>Interactive Video Guides Hub</h3>
            <p>Clickable tutorial links & smartphone QR codes covering front pleats, slant pockets, zipper fly, and waistband closure.</p>
        </div>
    </div>
    <div class="s6-card">
        <div class="s6-icon">✦</div>
        <div class="s6-body">
            <h3>Universal Printing & Sewing Guides</h3>
            <p>Includes SewLuxe Tiling & Assembly Guide (6 pages) plus Complete Atelier Sewing Tips Guide (11 pages).</p>
        </div>
    </div>
</div>
</body></html>"""

# =============================================================================
# SLIDE 7: INSIDE THE 16-PAGE BOOKLET (2000x2000)
# =============================================================================
slide7_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s7-spread {{
    display: flex; gap: 35px; justify-content: center; padding: 20px 60px;
    margin-top: 10px;
}}
.s7-page {{
    width: 420px; height: 1280px; background: #FFFFFF; border: 2px solid #E2DDD8;
    border-radius: 12px; overflow: hidden; box-shadow: 0 15px 35px rgba(0,0,0,0.06);
}}
.s7-page img {{ width: 100%; height: 100%; object-fit: contain; background: #FAF8F5; }}
.s7-banner {{
    width: 1780px; margin: 40px auto 0 auto; background: #FFFFFF; border: 2px solid #E2DDD8;
    border-radius: 16px; padding: 25px 40px; display: flex; justify-content: space-around;
    text-align: center;
}}
.s7-feat-h {{ font-size: 24px; font-weight: 700; color: #8C3B47; margin-bottom: 4px; }}
.s7-feat-p {{ font-size: 20px; color: #6E655F; }}
</style></head>
<body>
<div class="top-accent-bar"></div>
<div class="slide-header">
    <div class="slide-kicker">COUTURE CRAFTSMANSHIP</div>
    <div class="slide-title">Inside the 16-Page Sewing Booklet</div>
    <div class="slide-sub">Gold Standard framed diagrams, verified size tables, and expert tailoring tips</div>
    <div class="gold-line"></div>
</div>
<div class="s7-spread">
    <div class="s7-page"><img src="{bp1_uri}" /></div>
    <div class="s7-page"><img src="{bp8_uri}" /></div>
    <div class="s7-page"><img src="{bp9_uri}" /></div>
    <div class="s7-page"><img src="{bp16_uri}" /></div>
</div>
<div class="s7-banner">
    <div><div class="s7-feat-h">Gold Standard Panels</div><div class="s7-feat-p">#F5F2EF rounded vector boxes with bold callouts</div></div>
    <div><div class="s7-feat-h">Beginner to Advanced Tips</div><div class="s7-feat-p">Understitching, clapper pressing, and seam grading</div></div>
    <div><div class="s7-feat-h">360° Fit Verification</div><div class="s7-feat-p">Runway photos comparing real proportions</div></div>
</div>
</body></html>"""

# =============================================================================
# SLIDE 8: VIDEO TUTORIALS HUB (2000x2000)
# =============================================================================
slide8_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s8-wrap {{ display: flex; padding: 20px 80px; gap: 60px; align-items: center; justify-content: center; }}
.s8-page-box {{
    width: 820px; height: 1350px; background: #FFFFFF; border: 2px solid #E2DDD8;
    border-radius: 20px; overflow: hidden; box-shadow: 0 15px 35px rgba(0,0,0,0.06);
}}
.s8-page-box img {{ width: 100%; height: 100%; object-fit: contain; }}
.s8-cards {{ width: 920px; display: flex; flex-direction: column; gap: 28px; }}
.s8-card {{
    background: #FFFFFF; border: 2px solid #E2DDD8; border-left: 8px solid #8C3B47;
    border-radius: 16px; padding: 28px 35px; box-shadow: 0 8px 20px rgba(0,0,0,0.03);
}}
.s8-card-t {{ font-size: 26px; font-weight: 700; color: #8C3B47; margin-bottom: 6px; }}
.s8-card-p {{ font-size: 22px; color: #2C2624; line-height: 1.45; }}
</style></head>
<body>
<div class="top-accent-bar"></div>
<div class="slide-header">
    <div class="slide-kicker">SEW WITH CONFIDENCE</div>
    <div class="slide-title">Interactive Video Tutorial Hub</div>
    <div class="slide-sub">Scan QR codes with your smartphone camera or click links inside your PDF</div>
    <div class="gold-line"></div>
</div>
<div class="s8-wrap">
    <div class="s8-page-box"><img src="{bp8_uri}" /></div>
    <div class="s8-cards">
        <div class="s8-card">
            <div class="s8-card-t">1. Double Front Pleats & Center Crease</div>
            <div class="s8-card-p">Master the directional fold of the forward pleats and press razor-sharp vertical creases running from waist to hem.</div>
        </div>
        <div class="s8-card">
            <div class="s8-card-t">2. Slanted Italian Hip Pockets</div>
            <div class="s8-card-p">Learn how stay-tape reinforcement and crisp understitching keep the pocket lining invisible from the outside.</div>
        </div>
        <div class="s8-card">
            <div class="s8-card-t">3. Front Fly Zipper & J-Stitch</div>
            <div class="s8-card-p">Step-by-step guidance on stitching the curved J-stitch topstitching and attaching the protective inner fly shield.</div>
        </div>
        <div class="s8-card">
            <div class="s8-card-t">4. Concealed Hook & Bar Waistband</div>
            <div class="s8-card-p">Install heavy-duty metal trouser closures cleanly inside the waistband tab for a seamless couture front.</div>
        </div>
    </div>
</div>
</body></html>"""

# =============================================================================
# SLIDE 9: QUIET-LUXURY CAPSULE STYLING (2000x2000)
# =============================================================================
slide9_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s9-grid {{ display: grid; grid-template-columns: 880px 880px; gap: 40px; padding: 20px 80px; justify-content: center; }}
.s9-card {{
    background: #FFFFFF; border: 2px solid #E2DDD8; border-radius: 20px;
    padding: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.03);
}}
.s9-card-h {{ font-size: 28px; font-weight: 700; color: #8C3B47; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 25px; border-bottom: 2px solid #E2DDD8; padding-bottom: 15px; }}
.s9-item {{ margin-bottom: 25px; }}
.s9-item-t {{ font-size: 25px; font-weight: 700; color: #1E1A19; margin-bottom: 6px; }}
.s9-item-d {{ font-size: 22px; color: #6E655F; line-height: 1.45; }}
</style></head>
<body>
<div class="top-accent-bar"></div>
<div class="slide-header">
    <div class="slide-kicker">TIMELESS ATELIER ELEGANCE</div>
    <div class="slide-title">Capsule Wardrobe Styling Guide</div>
    <div class="slide-sub">Versatile quiet-luxury styling from morning boardroom to evening soiree</div>
    <div class="gold-line"></div>
</div>
<div class="s9-grid">
    <div class="s9-card">
        <div class="s9-card-h">Everyday Minimalist Chic</div>
        <div class="s9-item">
            <div class="s9-item-t">• Crisp Tucked Linen Shirt</div>
            <div class="s9-item-d">Tuck in a classic white or ecru linen button-down with rolled cuffs to highlight the high waistline and belt loops.</div>
        </div>
        <div class="s9-item">
            <div class="s9-item-t">• Ribbed Cashmere / Silk Tank</div>
            <div class="s9-item-d">A slim-fitting ribbed tank balances the generous volume of the palazzo wide legs for effortless Parisian chic.</div>
        </div>
        <div class="s9-item">
            <div class="s9-item-t">• Footwear Proportions</div>
            <div class="s9-item-d">Style with minimal leather slide sandals, pointed-toe mules, or minimalist sneakers peeking beneath the wide 5cm hem.</div>
        </div>
    </div>
    <div class="s9-card">
        <div class="s9-card-h">Tailored Evening & Office</div>
        <div class="s9-item">
            <div class="s9-item-t">• Structured Cropped Blazer</div>
            <div class="s9-item-d">Pair with a cropped boxy wool blazer hitting right at the waistband to accentuate the clean concealed waist closure.</div>
        </div>
        <div class="s9-item">
            <div class="s9-item-t">• Leather Belt Accent</div>
            <div class="s9-item-d">Slide a 2.5 cm (1 in) slim leather belt through the 5 tailored loops for polished corporate tailoring.</div>
        </div>
        <div class="s9-item">
            <div class="s9-item-t">• Four-Season Versatility</div>
            <div class="s9-item-d">Sew in washed linen for warm summer days, or tropical wool gabardine for timeless autumn and winter sophistication.</div>
        </div>
    </div>
</div>
</body></html>"""

# =============================================================================
# SLIDE 10: INSTANT DOWNLOAD HOW-TO (2000x2000)
# =============================================================================
slide10_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s10-wrap {{ display: flex; padding: 20px 80px; gap: 60px; align-items: center; justify-content: center; }}
.s10-hub-box {{
    width: 820px; height: 1350px; background: #FFFFFF; border: 2px solid #E2DDD8;
    border-radius: 20px; overflow: hidden; box-shadow: 0 15px 35px rgba(0,0,0,0.06);
}}
.s10-hub-box img {{ width: 100%; height: 100%; object-fit: contain; }}
.s10-steps {{ width: 920px; display: flex; flex-direction: column; gap: 24px; }}
.s10-card {{
    background: #FFFFFF; border: 2px solid #E2DDD8; border-radius: 16px;
    padding: 26px 30px; display: flex; gap: 25px; align-items: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.03);
}}
.s10-num {{
    width: 65px; height: 65px; background: #8C3B47; color: #FFFFFF;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: 32px; font-weight: 700; flex-shrink: 0;
}}
.s10-card-body h4 {{ font-size: 24px; font-weight: 700; color: #1E1A19; margin-bottom: 4px; }}
.s10-card-body p {{ font-size: 20px; color: #6E655F; line-height: 1.4; }}
.s10-badge {{
    background: #F5F2EF; border: 2px dashed #8C3B47; border-radius: 16px;
    padding: 25px 30px; text-align: center; margin-top: 10px;
}}
.s10-badge-t {{ font-size: 22px; font-weight: 700; color: #8C3B47; margin-bottom: 4px; }}
.s10-badge-p {{ font-size: 19px; color: #6E655F; }}
</style></head>
<body>
<div class="top-accent-bar"></div>
<div class="slide-header">
    <div class="slide-kicker">INSTANT ATELIER ACCESS</div>
    <div class="slide-title">How Digital Download Works</div>
    <div class="slide-sub">Zero waiting · Download immediately after checkout</div>
    <div class="gold-line"></div>
</div>
<div class="s10-wrap">
    <div class="s10-hub-box"><img src="{hub_uri}" /></div>
    <div class="s10-steps">
        <div class="s10-card">
            <div class="s10-num">1</div>
            <div class="s10-card-body">
                <h4>Instant Checkout on Etsy</h4>
                <p>Immediately after purchase, access your files under <b>Etsy &gt; Purchases and Reviews</b> via computer browser.</p>
            </div>
        </div>
        <div class="s10-card">
            <div class="s10-num">2</div>
            <div class="s10-card-body">
                <h4>Open Your 1-Page Download Hub</h4>
                <p>Click your desired format (A4, US Letter, A0 Copyshop, or Projector) for instant cloud access to all sizes.</p>
            </div>
        </div>
        <div class="s10-card">
            <div class="s10-num">3</div>
            <div class="s10-card-body">
                <h4>Verify 4x4" (10x10cm) Test Square</h4>
                <p>Print Page 1 at 100% Actual Size in Adobe Acrobat Reader and measure test square before printing full pattern.</p>
            </div>
        </div>
        <div class="s10-card">
            <div class="s10-num">4</div>
            <div class="s10-card-body">
                <h4>Sew with Illustrated 16-Page Booklet</h4>
                <p>Follow clear step-by-step guidance and scan QR codes for technique videos whenever you need extra help!</p>
            </div>
        </div>
        <div class="s10-badge">
            <div class="s10-badge-t">✦ 100% Customer Satisfaction Promise ✦</div>
            <div class="s10-badge-p">Need fitting advice or printing support? Message us anytime via Etsy for same-day dedicated support!</div>
        </div>
    </div>
</div>
</body></html>"""

SLIDES = [
    ("01_Cover.jpg", slide1_html),
    ("02_Angles_Details.jpg", slide2_html),
    ("03_Technical_Sketch.jpg", slide3_html),
    ("04_Size_Chart.jpg", slide4_html),
    ("05_Fabric_Notions.jpg", slide5_html),
    ("06_What_You_Receive.jpg", slide6_html),
    ("07_Inside_Booklet.jpg", slide7_html),
    ("08_Video_Tutorials.jpg", slide8_html),
    ("09_Styling_Capsule.jpg", slide9_html),
    ("10_How_To_Download.jpg", slide10_html),
]

def render_slides():
    print("==========================================================")
    print(" Launching Playwright to render all 10 slides (2000x2000) ")
    print("==========================================================")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 2000, "height": 2000}, device_scale_factor=1)
        
        for idx, (fname, html_str) in enumerate(SLIDES):
            tmp_html = os.path.join(SCRATCH_DIR, fname.replace(".jpg", ".html"))
            with open(tmp_html, "w", encoding="utf-8") as f:
                f.write(html_str)
                
            page.goto("file:///" + tmp_html.replace("\\", "/"))
            page.wait_for_timeout(350)
            
            out_desktop = os.path.join(SLIDES_DIR, fname)
            page.screenshot(path=out_desktop, type="jpeg", quality=95)
            
            out_brain = os.path.join(BRAIN_DIR, f"colette_slide_{fname}")
            page.screenshot(path=out_brain, type="jpeg", quality=95)
            
            print(f"  [OK] Rendered Slide {idx+1:02d}: {fname} (2000x2000 px)")
            
        browser.close()
    print("All 10 listing slides rendered successfully!")

if __name__ == "__main__":
    render_slides()
