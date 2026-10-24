import base64
import json
import os
import numpy as np
from PIL import Image, ImageFilter
from playwright.sync_api import sync_playwright

SCRATCH_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\c675070e-91f4-406b-8086-d794cba1db24\scratch"
ARTIFACT_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\c675070e-91f4-406b-8086-d794cba1db24"
PROJECT_DIR = r"C:\Users\red1e\.gemini\antigravity\scratch\colette_wide_leg_trousers"
DESKTOP_DIR = r"C:\Users\red1e\Desktop\Colette_Wide_Leg_Trousers"
SLIDES_DIR = os.path.join(DESKTOP_DIR, "Etsy_Listing_Images")
FONTS_DIR = r"C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\fonts"

os.makedirs(SLIDES_DIR, exist_ok=True)

# 1. Create a true sticker PNG of the flat sketch (white interior fill inside the trousers, transparent outside)
sticker_path = os.path.join(PROJECT_DIR, "flat_sketch_transparent.png")

def to_data_uri(path: str, mime: str) -> str:
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"

font_lora_reg = to_data_uri(os.path.join(FONTS_DIR, "Lora-Regular.ttf"), "font/ttf")
font_lora_bold = to_data_uri(os.path.join(FONTS_DIR, "Lora-Bold.ttf"), "font/ttf")
font_lora_italic = to_data_uri(os.path.join(FONTS_DIR, "Lora-Italic.ttf"), "font/ttf")
font_pop_reg = to_data_uri(os.path.join(FONTS_DIR, "Poppins-Regular.ttf"), "font/ttf")
font_pop_med = to_data_uri(os.path.join(FONTS_DIR, "Poppins-Medium.ttf"), "font/ttf")
font_pop_bold = to_data_uri(os.path.join(FONTS_DIR, "Poppins-Bold.ttf"), "font/ttf")

photo1_uri = to_data_uri(os.path.join(ARTIFACT_DIR, "model_photo_1_front_1792265587295.jpg"), "image/jpeg")
photo2_uri = to_data_uri(os.path.join(ARTIFACT_DIR, "model_photo_2_back_1792265665659.jpg"), "image/jpeg")
photo3_uri = to_data_uri(os.path.join(ARTIFACT_DIR, "model_photo_3_side_three_quarter_1792265685202.jpg"), "image/jpeg")
photo4_uri = to_data_uri(os.path.join(ARTIFACT_DIR, "model_photo_4_lifestyle_1792265706320.jpg"), "image/jpeg")
sticker_uri = to_data_uri(sticker_path, "image/png")

pages_dir = os.path.join(SCRATCH_DIR, "colette_booklet_pages")
p1_uri = to_data_uri(os.path.join(pages_dir, "page_01.png"), "image/png")
p3_uri = to_data_uri(os.path.join(pages_dir, "page_03.png"), "image/png")
p4_uri = to_data_uri(os.path.join(pages_dir, "page_04.png"), "image/png")
p6_uri = to_data_uri(os.path.join(pages_dir, "page_06.png"), "image/png")
p7_uri = to_data_uri(os.path.join(pages_dir, "page_07.png"), "image/png")
p8_uri = to_data_uri(os.path.join(pages_dir, "page_08.png"), "image/png")
p11_uri = to_data_uri(os.path.join(pages_dir, "page_11.png"), "image/png")
p12_uri = to_data_uri(os.path.join(pages_dir, "page_12.png"), "image/png")

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
    background: #FAF8F6;
    font-family: 'Poppins', sans-serif;
    color: #1E1A19;
    position: relative;
}}
"""

# SLIDE 1: HERO COVER (2000x2000)
slide1_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.container {{
    display: flex;
    width: 2000px;
    height: 2000px;
    position: relative;
}}
.left-photo {{
    width: 1140px;
    height: 2000px;
    position: relative;
    overflow: hidden;
}}
.left-photo img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: 48% center;
}}
.right-panel {{
    width: 860px;
    height: 2000px;
    background: #FAF8F6;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 90px 65px 70px 65px;
    position: relative;
    border-left: 3px solid #EAE3DC;
}}
.top-accent {{
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 22px;
    background: #8C3B47;
}}
.kicker {{
    font-family: 'Poppins', sans-serif;
    font-weight: 500;
    font-size: 28px;
    letter-spacing: 9px;
    color: #8C3B47;
    text-transform: uppercase;
    margin-bottom: 18px;
}}
.title {{
    font-family: 'Lora', serif;
    font-weight: 400;
    font-size: 148px;
    line-height: 1.0;
    color: #1E1A19;
    margin-bottom: 14px;
}}
.subtitle {{
    font-family: 'Poppins', sans-serif;
    font-weight: 500;
    font-size: 40px;
    letter-spacing: 16px;
    color: #1E1A19;
    margin-bottom: 26px;
    padding-left: 16px;
}}
.rule {{
    width: 180px;
    height: 4px;
    background: #8C3B47;
    margin-bottom: 36px;
}}
.sketch-wrap {{
    width: 680px;
    height: 760px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 34px;
    position: relative;
}}
.sketch-wrap img {{
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}}
.badges {{
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-bottom: auto;
}}
.badge {{
    background: #FFFFFF;
    border: 2px solid #E5DDD5;
    border-left: 9px solid #8C3B47;
    border-radius: 14px;
    padding: 22px 30px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 8px 20px rgba(30,26,25,0.04);
}}
.badge-label {{
    font-size: 23px;
    font-weight: 500;
    letter-spacing: 3px;
    color: #8C3B47;
    text-transform: uppercase;
}}
.badge-val {{
    font-size: 27px;
    font-weight: 700;
    color: #1E1A19;
}}
.footer-brand {{
    margin-top: 30px;
    text-align: center;
}}
.instant-pill {{
    background: #1E1A19;
    color: #FFFFFF;
    font-size: 22px;
    font-weight: 500;
    letter-spacing: 6px;
    padding: 14px 40px;
    border-radius: 40px;
    margin-bottom: 20px;
    display: inline-block;
}}
.shop-name {{
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 46px;
    color: #8C3B47;
    display: block;
}}
</style></head>
<body>
<div class="container">
    <div class="left-photo">
        <img src="{photo1_uri}" />
    </div>
    <div class="right-panel">
        <div class="top-accent"></div>
        <div class="kicker">PDF SEWING PATTERN</div>
        <div class="title">Colette</div>
        <div class="subtitle">TROUSERS</div>
        <div class="rule"></div>
        <div class="sketch-wrap">
            <img src="{sticker_uri}" />
        </div>
        <div class="badges">
            <div class="badge">
                <span class="badge-label">SIZES INCLUDED</span>
                <span class="badge-val">US 00 – 22 (XXS – 4XL)</span>
            </div>
            <div class="badge">
                <span class="badge-label">SKILL LEVEL</span>
                <span class="badge-val">Intermediate</span>
            </div>
            <div class="badge">
                <span class="badge-label">PRINT FORMATS</span>
                <span class="badge-val">A4 · US Letter · A0</span>
            </div>
            <div class="badge">
                <span class="badge-label">SEWING GUIDE</span>
                <span class="badge-val">Illustrated Booklet + Videos</span>
            </div>
        </div>
        <div class="footer-brand">
            <div class="instant-pill">INSTANT DIGITAL DOWNLOAD</div>
            <span class="shop-name">SewLuxePatterns</span>
        </div>
    </div>
</div>
</body></html>
"""

# SLIDE 2: ANGLES & CONSTRUCTION DETAILS
slide2_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.page {{
    padding: 85px 95px 75px 95px;
    height: 2000px;
    display: flex;
    flex-direction: column;
}}
.top-bar {{
    position: absolute; top: 0; left: 0; right: 0; height: 18px; background: #8C3B47;
}}
.header {{
    text-align: center;
    margin-bottom: 50px;
}}
.kicker {{
    font-size: 26px; font-weight: 500; letter-spacing: 8px; color: #8C3B47; margin-bottom: 12px;
}}
.title {{
    font-family: 'Lora', serif; font-size: 74px; color: #1E1A19;
}}
.photos-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 48px;
    height: 1160px;
    margin-bottom: 52px;
}}
.photo-card {{
    position: relative;
    border-radius: 22px;
    overflow: hidden;
    box-shadow: 0 18px 40px rgba(30,26,25,0.10);
    border: 4px solid #FFFFFF;
}}
.photo-card img {{
    width: 100%; height: 100%; object-fit: cover;
}}
.photo-tag {{
    position: absolute;
    bottom: 28px; left: 28px;
    background: rgba(250, 248, 246, 0.94);
    border-left: 7px solid #8C3B47;
    padding: 16px 28px;
    border-radius: 10px;
    font-size: 26px;
    font-weight: 500;
    color: #1E1A19;
}}
.features-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 28px;
    margin-bottom: auto;
}}
.feat-box {{
    background: #FFFFFF;
    border: 2px solid #E5DDD5;
    border-top: 6px solid #8C3B47;
    border-radius: 16px;
    padding: 28px 30px;
}}
.feat-title {{
    font-size: 26px; font-weight: 700; color: #1E1A19; margin-bottom: 8px;
}}
.feat-desc {{
    font-size: 22px; color: #5A524C; line-height: 1.45;
}}
.footer {{
    display: flex; justify-content: space-between; align-items: center;
    border-top: 2px solid #DFD9D3; padding-top: 26px;
    font-size: 24px; color: #6E655F;
}}
.footer .brand {{ font-family: 'Lora', serif; font-style: italic; font-size: 34px; color: #8C3B47; }}
</style></head>
<body>
<div class="top-bar"></div>
<div class="page">
    <div class="header">
        <div class="kicker">COLETTE WIDE-LEG TROUSERS</div>
        <div class="title">Thoughtful Tailoring Details</div>
    </div>
    <div class="photos-grid">
        <div class="photo-card">
            <img src="{photo3_uri}" />
            <div class="photo-tag">Front Pleats & Slanted Side Pockets</div>
        </div>
        <div class="photo-card">
            <img src="{photo2_uri}" />
            <div class="photo-tag">Back Waist Darts & Single-Welt Pockets</div>
        </div>
    </div>
    <div class="features-grid">
        <div class="feat-box">
            <div class="feat-title">Double Front Pleats</div>
            <div class="feat-desc">Two soft pleats on each side release smoothly into a relaxed, full-length wide leg.</div>
        </div>
        <div class="feat-box">
            <div class="feat-title">Front & Back Pockets</div>
            <div class="feat-desc">Deep slanted front pockets plus tailored single-welt back pockets below the waist darts.</div>
        </div>
        <div class="feat-box">
            <div class="feat-title">Classic Zipper Fly</div>
            <div class="feat-desc">Clean 3 cm (1 1/8") straight 1-button waistband with a traditional J-stitch fly & shield.</div>
        </div>
    </div>
    <div class="footer">
        <span class="brand">SewLuxePatterns</span>
        <span>SIZES US 00–22 (XXS–4XL)  ·  1 CM (3/8 IN) SEAM ALLOWANCE INCLUDED</span>
    </div>
</div>
</body></html>
"""

# SLIDE 3: TECHNICAL FLAT SKETCH & SPECIFICATIONS
slide3_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.page {{ padding: 85px 95px 75px 95px; height: 2000px; display: flex; flex-direction: column; }}
.top-bar {{ position: absolute; top: 0; left: 0; right: 0; height: 18px; background: #8C3B47; }}
.header {{ text-align: center; margin-bottom: 45px; }}
.kicker {{ font-size: 26px; font-weight: 500; letter-spacing: 8px; color: #8C3B47; margin-bottom: 12px; }}
.title {{ font-family: 'Lora', serif; font-size: 74px; color: #1E1A19; }}
.main-grid {{
    display: grid;
    grid-template-columns: 1000px 1fr;
    gap: 50px;
    height: 1440px;
    margin-bottom: auto;
}}
.sketch-card {{
    background: #FFFFFF;
    border-radius: 24px;
    border: 2px solid #E5DDD5;
    padding: 50px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: 0 14px 34px rgba(30,26,25,0.06);
}}
.sketch-card img {{
    width: 100%; height: 1240px; object-fit: contain;
}}
.sketch-caption {{
    font-size: 24px; letter-spacing: 5px; color: #6E655F; font-weight: 500; margin-top: 15px;
}}
.specs-col {{
    display: flex; flex-direction: column; gap: 34px;
}}
.spec-card {{
    background: #FFFFFF;
    border-radius: 20px;
    border: 2px solid #E5DDD5;
    border-left: 10px solid #8C3B47;
    padding: 38px 42px;
    box-shadow: 0 10px 26px rgba(30,26,25,0.04);
}}
.spec-card h3 {{
    font-family: 'Lora', serif;
    font-size: 42px;
    color: #8C3B47;
    margin-bottom: 22px;
}}
.spec-list {{
    list-style: none;
    display: flex; flex-direction: column; gap: 16px;
}}
.spec-list li {{
    font-size: 25px; line-height: 1.45; color: #2C2624;
    padding-left: 42px; position: relative;
}}
.spec-list li::before {{
    content: "✓";
    position: absolute; left: 0; top: 0;
    color: #8C3B47; font-weight: 700;
}}
.footer {{
    display: flex; justify-content: space-between; align-items: center;
    border-top: 2px solid #DFD9D3; padding-top: 26px;
    font-size: 24px; color: #6E655F;
}}
.footer .brand {{ font-family: 'Lora', serif; font-style: italic; font-size: 34px; color: #8C3B47; }}
</style></head>
<body>
<div class="top-bar"></div>
<div class="page">
    <div class="header">
        <div class="kicker">TECHNICAL OVERVIEW</div>
        <div class="title">Flat Sketch & Pattern Specifications</div>
    </div>
    <div class="main-grid">
        <div class="sketch-card">
            <img src="{sticker_uri}" />
            <div class="sketch-caption">FRONT & BACK TECHNICAL VIEW</div>
        </div>
        <div class="specs-col">
            <div class="spec-card">
                <h3>Design Features</h3>
                <ul class="spec-list">
                    <li>High-waisted, full-length wide-leg silhouette</li>
                    <li>Double front pleats (two on each side) for fluid drape</li>
                    <li>Slanted front side pockets anchored at waist & hip</li>
                    <li>Back waist darts & functional single-welt back pockets</li>
                    <li>Classic zipper fly with 1-button waistband & fly shield</li>
                    <li>Sleek belt-loop-free waist & 3 cm (1 1/8") deep hem</li>
                </ul>
            </div>
            <div class="spec-card">
                <h3>Pattern Details</h3>
                <ul class="spec-list">
                    <li><strong>13 Individual Sizes:</strong> US 00 to 22 (XXS to 4XL)</li>
                    <li><strong>10 Pattern Pieces:</strong> Full flat pieces with grainlines & notches</li>
                    <li><strong>Seam Allowance Included:</strong> 1 cm (3/8 in) on all seams</li>
                    <li><strong>Drafted Height:</strong> 168 cm (5 ft 6 in) · Inseam 73 cm (28 3/4 in)</li>
                    <li><strong>Print Formats:</strong> A4, US Letter (home) & A0 (copy shop)</li>
                </ul>
            </div>
        </div>
    </div>
    <div class="footer">
        <span class="brand">SewLuxePatterns</span>
        <span>PROFESSIONALLY DRAFTED DIGITAL SEWING PATTERN</span>
    </div>
</div>
</body></html>
"""

# SLIDE 4: SIZE CHARTS (renders page_04.png or crisp HTML table)
size_data = json.load(open(os.path.join(PROJECT_DIR, "booklet_size_data.json"), encoding="utf-8"))
body_rows = [
    ("00", "XXS", "63.5 cm / 25\"", "87.8 cm / 34 1/2\"", "64.8 cm / 25 1/2\"", "90.2 cm / 35 1/2\"", "73 cm / 28 3/4\""),
    ("0",  "XS",  "66.0 cm / 26\"", "90.3 cm / 35 1/2\"", "67.3 cm / 26 1/2\"", "92.6 cm / 36 1/2\"", "73 cm / 28 5/8\""),
    ("2",  "XS",  "68.8 cm / 27 1/8\"", "92.8 cm / 36 1/2\"", "70.1 cm / 27 5/8\"", "95.0 cm / 37 3/8\"", "72 cm / 28 3/8\""),
    ("4",  "S",   "71.3 cm / 28\"", "95.3 cm / 37 1/2\"", "72.7 cm / 28 5/8\"", "97.4 cm / 38 3/8\"", "72 cm / 28 1/4\""),
    ("6",  "S",   "73.8 cm / 29\"", "98.0 cm / 38 5/8\"", "75.2 cm / 29 5/8\"", "100.0 cm / 39 3/8\"", "71 cm / 28\""),
    ("8",  "M",   "76.3 cm / 30\"", "100.3 cm / 39 1/2\"", "77.8 cm / 30 5/8\"", "102.2 cm / 40 1/4\"", "71 cm / 27 3/4\""),
    ("10", "M",   "78.8 cm / 31\"", "102.8 cm / 40 1/2\"", "80.3 cm / 31 5/8\"", "104.4 cm / 41 1/8\"", "70 cm / 27 5/8\""),
    ("12", "L",   "82.8 cm / 32 5/8\"", "106.5 cm / 41 7/8\"", "84.4 cm / 33 1/4\"", "107.8 cm / 42 3/8\"", "71 cm / 27 7/8\""),
    ("14", "L",   "87.5 cm / 34 1/2\"", "111.0 cm / 43 3/4\"", "89.2 cm / 35 1/8\"", "111.8 cm / 44\"", "70 cm / 27 5/8\""),
    ("16", "XL",  "93.3 cm / 36 3/4\"", "115.5 cm / 45 1/2\"", "95.1 cm / 37 1/2\"", "115.8 cm / 45 5/8\"", "69 cm / 27 1/4\""),
    ("18", "2XL", "99.0 cm / 39\"", "120.8 cm / 47 1/2\"", "101.0 cm / 39 3/4\"", "126.1 cm / 49 5/8\"", "68 cm / 27\""),
    ("20", "3XL", "104.8 cm / 41 1/4\"", "125.8 cm / 49 1/2\"", "106.8 cm / 42 1/8\"", "132.0 cm / 52\"", "68 cm / 26 5/8\""),
    ("22", "4XL", "110.5 cm / 43 1/2\"", "130.8 cm / 51 1/2\"", "112.7 cm / 44 3/8\"", "137.9 cm / 54 1/4\"", "67 cm / 26 3/8\""),
]
rows_html = ""
for idx, r in enumerate(body_rows):
    bg = "#F4EFEA" if idx % 2 == 1 else "#FFFFFF"
    rows_html += f"""
    <tr style="background:{bg};">
        <td style="font-weight:700; color:#8C3B47;">{r[0]}</td>
        <td style="font-weight:500;">{r[1]}</td>
        <td>{r[2]}</td>
        <td>{r[3]}</td>
        <td>{r[4]}</td>
        <td>{r[5]}</td>
        <td>{r[6]}</td>
    </tr>"""

slide4_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.page {{ padding: 80px 90px 70px 90px; height: 2000px; display: flex; flex-direction: column; }}
.top-bar {{ position: absolute; top: 0; left: 0; right: 0; height: 18px; background: #8C3B47; }}
.header {{ text-align: center; margin-bottom: 40px; }}
.kicker {{ font-size: 26px; font-weight: 500; letter-spacing: 8px; color: #8C3B47; margin-bottom: 10px; }}
.title {{ font-family: 'Lora', serif; font-size: 72px; color: #1E1A19; }}
.table-wrap {{
    background: #FFFFFF;
    border-radius: 20px;
    overflow: hidden;
    border: 2px solid #DFD9D3;
    box-shadow: 0 14px 32px rgba(30,26,25,0.06);
    margin-bottom: 34px;
}}
table {{ width: 100%; border-collapse: collapse; text-align: center; }}
th {{
    background: #1E1A19; color: #FFFFFF;
    font-size: 22px; font-weight: 500; letter-spacing: 2px;
    padding: 24px 16px;
}}
td {{
    font-size: 25px; color: #1E1A19;
    padding: 20px 16px;
    border-bottom: 1px solid #EAE3DC;
}}
.note-box {{
    background: #F6ECEA;
    border-left: 8px solid #8C3B47;
    padding: 26px 34px;
    border-radius: 12px;
    font-size: 24px;
    line-height: 1.5;
    color: #2C2624;
    margin-bottom: auto;
}}
.footer {{
    display: flex; justify-content: space-between; align-items: center;
    border-top: 2px solid #DFD9D3; padding-top: 26px;
    font-size: 24px; color: #6E655F;
}}
.footer .brand {{ font-family: 'Lora', serif; font-style: italic; font-size: 34px; color: #8C3B47; }}
</style></head>
<body>
<div class="top-bar"></div>
<div class="page">
    <div class="header">
        <div class="kicker">CHOOSE YOUR PERFECT FIT</div>
        <div class="title">Body & Finished Garment Measurements</div>
    </div>
    <div class="table-wrap">
        <table>
            <thead>
                <tr>
                    <th>US SIZE</th>
                    <th>LETTER</th>
                    <th>BODY WAIST</th>
                    <th>BODY HIPS</th>
                    <th>FINISHED WAIST*</th>
                    <th>FINISHED HIPS*</th>
                    <th>INSEAM</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    <div class="note-box">
        <strong>* Fitting & Ease Note:</strong> Finished waist and hip measurements are measured with the four front pleats closed (approx. 1.5 cm / 5/8 in waist ease and 2.5–7 cm / 1–2 3/4 in hip ease, plus extra front pleat fullness). Drafted for 168 cm (5 ft 6 in) height; easily lengthen or shorten along the knee line.
    </div>
    <div class="footer">
        <span class="brand">SewLuxePatterns</span>
        <span>BOTH METRIC (CM) & IMPERIAL (INCHES) INCLUDED</span>
    </div>
</div>
</body></html>
"""

# SLIDE 5: FABRIC & NOTIONS GUIDE
slide5_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.page {{ padding: 85px 95px 75px 95px; height: 2000px; display: flex; flex-direction: column; }}
.top-bar {{ position: absolute; top: 0; left: 0; right: 0; height: 18px; background: #8C3B47; }}
.header {{ text-align: center; margin-bottom: 48px; }}
.kicker {{ font-size: 26px; font-weight: 500; letter-spacing: 8px; color: #8C3B47; margin-bottom: 12px; }}
.title {{ font-family: 'Lora', serif; font-size: 74px; color: #1E1A19; }}
.table-wrap {{
    background: #FFFFFF; border-radius: 20px; overflow: hidden;
    border: 2px solid #DFD9D3; box-shadow: 0 12px 28px rgba(30,26,25,0.05);
    margin-bottom: 48px;
}}
table {{ width: 100%; border-collapse: collapse; text-align: center; }}
th {{ background: #1E1A19; color: #FFFFFF; font-size: 25px; font-weight: 500; padding: 26px 20px; letter-spacing: 2px; }}
td {{ font-size: 28px; padding: 28px 20px; border-bottom: 1px solid #EAE3DC; color: #1E1A19; }}
.cards-row {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 44px; margin-bottom: auto;
}}
.card {{
    background: #FFFFFF; border-radius: 20px; border: 2px solid #E5DDD5;
    border-top: 8px solid #8C3B47; padding: 42px 44px;
    box-shadow: 0 12px 28px rgba(30,26,25,0.04);
}}
.card h3 {{ font-family: 'Lora', serif; font-size: 44px; color: #8C3B47; margin-bottom: 24px; }}
.card ul {{ list-style: none; display: flex; flex-direction: column; gap: 18px; }}
.card li {{ font-size: 25px; line-height: 1.48; color: #2C2624; padding-left: 42px; position: relative; }}
.card li::before {{ content: "✓"; position: absolute; left: 0; top: 0; color: #8C3B47; font-weight: 700; }}
.footer {{
    display: flex; justify-content: space-between; align-items: center;
    border-top: 2px solid #DFD9D3; padding-top: 26px; font-size: 24px; color: #6E655F;
}}
.footer .brand {{ font-family: 'Lora', serif; font-style: italic; font-size: 34px; color: #8C3B47; }}
</style></head>
<body>
<div class="top-bar"></div>
<div class="page">
    <div class="header">
        <div class="kicker">MATERIALS & YARDAGE</div>
        <div class="title">Fabric Requirements & Notions</div>
    </div>
    <div class="table-wrap">
        <table>
            <thead>
                <tr>
                    <th>US SIZES</th>
                    <th>LETTER SIZES</th>
                    <th>150 cm (60 in) WIDE FABRIC</th>
                    <th>115 cm (45 in) WIDE FABRIC</th>
                </tr>
            </thead>
            <tbody>
                <tr style="background:#FFFFFF;">
                    <td style="font-weight:700; color:#8C3B47;">US 00 – 6</td>
                    <td>XXS – S</td>
                    <td><strong>1.8 m</strong>  (2 yd)</td>
                    <td><strong>2.3 m</strong>  (2 1/2 yd)</td>
                </tr>
                <tr style="background:#F4EFEA;">
                    <td style="font-weight:700; color:#8C3B47;">US 8 – 14</td>
                    <td>M – L</td>
                    <td><strong>2.1 m</strong>  (2 3/8 yd)</td>
                    <td><strong>2.6 m</strong>  (2 7/8 yd)</td>
                </tr>
                <tr style="background:#FFFFFF;">
                    <td style="font-weight:700; color:#8C3B47;">US 16 – 22</td>
                    <td>XL – 4XL</td>
                    <td><strong>2.4 m</strong>  (2 5/8 yd)</td>
                    <td><strong>2.9 m</strong>  (3 1/4 yd)</td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="cards-row">
        <div class="card">
            <h3>Suggested Fabrics</h3>
            <ul>
                <li><strong>Medium-weight woven suiting (180–280 gsm):</strong> brushed wool-linen twill, wool gabardine, wool crepe</li>
                <li>Heavy linen, linen-viscose suiting, or Tencel/lyocell twill for warm-weather drape</li>
                <li>Cotton cavalry twill or fine-wale needlecord</li>
                <li><strong>Pocket Lining (Pieces 6 & 9):</strong> lightweight cotton lawn, poplin, or Bemberg lining (0.5 m / 5/8 yd)</li>
            </ul>
        </div>
        <div class="card">
            <h3>Required Notions</h3>
            <ul>
                <li><strong>1 Nylon Trouser Zipper:</strong> 20–23 cm (8–9 in) long (shortened in Step 4 to fit the fly)</li>
                <li><strong>1 Trouser Button:</strong> 10–12 mm (3/8–1/2 in) diameter for the front waistband overlap</li>
                <li><strong>Fusible Interfacing:</strong> 0.5 m (5/8 yd) lightweight woven fusible interfacing (Waistband, Fly & Welts)</li>
                <li>Matching polyester thread, zipper foot & tailor's chalk</li>
            </ul>
        </div>
    </div>
    <div class="footer">
        <span class="brand">SewLuxePatterns</span>
        <span>YARDAGE SHOWN FOR PLAIN FABRIC WITHOUT NAP</span>
    </div>
</div>
</body></html>
"""

# SLIDE 6: INSIDE THE INSTRUCTION BOOKLET
slide6_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.page {{ padding: 80px 90px 70px 90px; height: 2000px; display: flex; flex-direction: column; }}
.top-bar {{ position: absolute; top: 0; left: 0; right: 0; height: 18px; background: #8C3B47; }}
.header {{ text-align: center; margin-bottom: 42px; }}
.kicker {{ font-size: 26px; font-weight: 500; letter-spacing: 8px; color: #8C3B47; margin-bottom: 10px; }}
.title {{ font-family: 'Lora', serif; font-size: 72px; color: #1E1A19; }}
.pages-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 28px;
    margin-bottom: 44px;
}}
.page-preview {{
    background: #FFFFFF;
    border-radius: 14px;
    overflow: hidden;
    border: 2px solid #DFD9D3;
    box-shadow: 0 16px 36px rgba(30,26,25,0.10);
}}
.page-preview img {{ width: 100%; height: auto; display: block; }}
.highlights-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
    margin-bottom: auto;
}}
.hl-card {{
    background: #FFFFFF;
    border: 2px solid #E5DDD5;
    border-left: 8px solid #8C3B47;
    border-radius: 16px;
    padding: 30px 32px;
}}
.hl-card h4 {{ font-size: 27px; font-weight: 700; color: #1E1A19; margin-bottom: 10px; }}
.hl-card p {{ font-size: 23px; color: #5A524C; line-height: 1.45; }}
.footer {{
    display: flex; justify-content: space-between; align-items: center;
    border-top: 2px solid #DFD9D3; padding-top: 26px; font-size: 24px; color: #6E655F;
}}
.footer .brand {{ font-family: 'Lora', serif; font-style: italic; font-size: 34px; color: #8C3B47; }}
</style></head>
<body>
<div class="top-bar"></div>
<div class="page">
    <div class="header">
        <div class="kicker">16-PAGE ILLUSTRATED SEWING GUIDE</div>
        <div class="title">Step-by-Step Diagrams & Video Help</div>
    </div>
    <div class="pages-grid">
        <div class="page-preview"><img src="{p7_uri}" /></div>
        <div class="page-preview"><img src="{p8_uri}" /></div>
        <div class="page-preview"><img src="{p11_uri}" /></div>
        <div class="page-preview"><img src="{p12_uri}" /></div>
    </div>
    <div class="highlights-grid">
        <div class="hl-card">
            <h4>Illustrated Every Step</h4>
            <p>Crystal-clear technical diagrams for the front pleats, slanted pockets, back single-welt pockets, and zipper fly.</p>
        </div>
        <div class="hl-card">
            <h4>QR & Clickable Videos</h4>
            <p>Scan the QR codes or click the links on Page 8 to watch video tutorials for every tailoring technique.</p>
        </div>
        <div class="hl-card">
            <h4>Print at Home or Copyshop</h4>
            <p>Includes A4, US Letter, and A0 large-format PDFs with individual size files (US 00 to 22) ready to print.</p>
        </div>
    </div>
    <div class="footer">
        <span class="brand">SewLuxePatterns</span>
        <span>INSTANT DIGITAL DOWNLOAD  ·  NO PHYSICAL ITEM SHIPPED</span>
    </div>
</div>
</body></html>
"""

# SLIDE 7: LIFESTYLE & HOW INSTANT DOWNLOAD WORKS
slide7_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.container {{ display: flex; width: 2000px; height: 2000px; }}
.left-col {{
    width: 960px; height: 2000px; padding: 95px 75px 75px 85px;
    display: flex; flex-direction: column;
}}
.right-photo {{ width: 1040px; height: 2000px; overflow: hidden; border-left: 3px solid #EAE3DC; }}
.right-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.top-bar {{ position: absolute; top: 0; left: 0; right: 0; height: 18px; background: #8C3B47; z-index: 10; }}
.kicker {{ font-size: 25px; font-weight: 500; letter-spacing: 7px; color: #8C3B47; margin-bottom: 12px; }}
.title {{ font-family: 'Lora', serif; font-size: 66px; color: #1E1A19; line-height: 1.12; margin-bottom: 42px; }}
.step-list {{ display: flex; flex-direction: column; gap: 28px; margin-bottom: auto; }}
.step-card {{
    background: #FFFFFF; border-radius: 18px; border: 2px solid #E5DDD5;
    padding: 30px 34px; display: flex; gap: 26px; align-items: flex-start;
    box-shadow: 0 10px 24px rgba(30,26,25,0.04);
}}
.step-num {{
    width: 56px; height: 56px; border-radius: 28px; background: #8C3B47; color: #FFFFFF;
    font-size: 28px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}}
.step-body h4 {{ font-size: 27px; font-weight: 700; color: #1E1A19; margin-bottom: 6px; }}
.step-body p {{ font-size: 22px; color: #5A524C; line-height: 1.45; }}
.disclaimer {{
    background: #F6ECEA; border-left: 8px solid #8C3B47; padding: 24px 28px;
    border-radius: 12px; font-size: 22px; color: #2C2624; line-height: 1.45; margin-top: 24px;
}}
</style></head>
<body>
<div class="top-bar"></div>
<div class="container">
    <div class="left-col">
        <div class="kicker">START SEWING TODAY</div>
        <div class="title">How Instant Download Works</div>
        <div class="step-list">
            <div class="step-card">
                <div class="step-num">1</div>
                <div class="step-body">
                    <h4>Download Immediately</h4>
                    <p>After checkout, open <strong>Etsy &gt; Purchases and Reviews</strong> on your computer browser to download your files right away.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-num">2</div>
                <div class="step-body">
                    <h4>Pick Your Size & Format</h4>
                    <p>Unzip your chosen format folder (<strong>A4</strong>, <strong>US Letter</strong>, or <strong>A0 Copyshop</strong>) and open the PDF file for your size (US 00–22).</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-num">3</div>
                <div class="step-body">
                    <h4>Check the 10 × 10 cm (4 × 4") Square</h4>
                    <p>Print Page 1 at <strong>100% / Actual Size</strong> in Adobe Acrobat Reader and verify the test square before printing the pattern.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-num">4</div>
                <div class="step-body">
                    <h4>Sew with the Illustrated Guide</h4>
                    <p>Follow the 16-page step-by-step booklet and scan the QR codes for helpful video tutorials!</p>
                </div>
            </div>
        </div>
        <div class="disclaimer">
            <strong>Digital PDF Pattern Only:</strong> No physical garment or printed paper pattern will be shipped in the mail.
        </div>
    </div>
    <div class="right-photo">
        <img src="{photo4_uri}" />
    </div>
</div>
</body></html>
"""

slides = [
    ("01_Etsy_Cover.jpg", slide1_html),
    ("02_Angles_Details.jpg", slide2_html),
    ("03_Technical_Sketch.jpg", slide3_html),
    ("04_Size_Chart.jpg", slide4_html),
    ("05_Fabric_Notions.jpg", slide5_html),
    ("06_Inside_Booklet.jpg", slide6_html),
    ("07_How_To_Download.jpg", slide7_html),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 2000, "height": 2000}, device_scale_factor=1)
    for fname, html_str in slides:
        tmp_html = os.path.join(SCRATCH_DIR, fname.replace(".jpg", ".html"))
        with open(tmp_html, "w", encoding="utf-8") as f:
            f.write(html_str)
        page.goto("file:///" + tmp_html.replace("\\", "/"))
        page.wait_for_timeout(300)
        out_jpg = os.path.join(SLIDES_DIR, fname)
        page.screenshot(path=out_jpg, type="jpeg", quality=95)
        # Also copy to ARTIFACT_DIR for embedding in chat
        out_art = os.path.join(ARTIFACT_DIR, fname)
        page.screenshot(path=out_art, type="jpeg", quality=95)
        print("Rendered:", out_jpg)
    browser.close()
