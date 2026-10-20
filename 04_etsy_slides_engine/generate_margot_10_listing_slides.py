import base64
import json
import os
import shutil
from playwright.sync_api import sync_playwright

BRAIN_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0"
ENGINE_DIR = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\03_booklet_engine"
DESKTOP_DIR = r"C:\Users\red1e\Desktop\SewLuxe_Elastic_Wide_Leg_Pants"
SLIDES_DIR = os.path.join(DESKTOP_DIR, "05_Etsy_Listing_Images")
FONTS_DIR = r"C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\fonts"
SCRATCH_DIR = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\04_etsy_slides_engine"

os.makedirs(SLIDES_DIR, exist_ok=True)
os.makedirs(SCRATCH_DIR, exist_ok=True)

def to_data_uri(path: str, mime: str) -> str:
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
photo1_uri = to_data_uri(os.path.join(BRAIN_DIR, "margot_photoshoot_01_front.jpg"), "image/jpeg")
photo2_uri = to_data_uri(os.path.join(BRAIN_DIR, "margot_photoshoot_02_side.jpg"), "image/jpeg")
photo3_uri = to_data_uri(os.path.join(BRAIN_DIR, "margot_photoshoot_03_back.jpg"), "image/jpeg")

sketch_front_uri = to_data_uri(os.path.join(ENGINE_DIR, "flat_sketch_front_clean.png"), "image/png")
sketch_back_uri = to_data_uri(os.path.join(ENGINE_DIR, "flat_sketch_back_clean.png"), "image/png")
qr_code_uri = to_data_uri(os.path.join(ENGINE_DIR, "margot_qr_code.png"), "image/png")

bp3_uri = to_data_uri(os.path.join(BRAIN_DIR, "booklet_page_03.png"), "image/png")
bp4_uri = to_data_uri(os.path.join(BRAIN_DIR, "booklet_page_04.png"), "image/png")
bp7_uri = to_data_uri(os.path.join(BRAIN_DIR, "booklet_page_07.png"), "image/png")
bp13_uri = to_data_uri(os.path.join(BRAIN_DIR, "booklet_page_13.png"), "image/png")

# Load Specs Data
with open(os.path.join(ENGINE_DIR, "booklet_size_data.json"), "r", encoding="utf-8") as f:
    size_data = json.load(f)

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
    color: #1A1918;
    position: relative;
}}
.top-accent-bar {{
    position: absolute;
    top: 0;
    left: 0;
    width: 2000px;
    height: 14px;
    background: #2D3728;
    z-index: 100;
}}
.slide-header {{
    text-align: center;
    padding-top: 55px;
    margin-bottom: 35px;
}}
.slide-kicker {{
    font-family: 'Poppins', sans-serif;
    font-size: 20px;
    font-weight: 600;
    letter-spacing: 0.22em;
    color: #58694B;
    text-transform: uppercase;
    margin-bottom: 10px;
}}
.slide-title {{
    font-family: 'Lora', serif;
    font-size: 58px;
    font-weight: 700;
    color: #2D3728;
    letter-spacing: -0.01em;
    line-height: 1.15;
}}
.slide-subtitle {{
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 26px;
    color: #6E6862;
    margin-top: 8px;
}}
"""

# ==================== SLIDE 1: HERO COVER ====================
slide1_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s1-container {{
    display: flex;
    width: 2000px;
    height: 2000px;
    position: relative;
}}
.s1-left {{
    width: 1120px;
    height: 2000px;
    position: relative;
    overflow: hidden;
}}
.s1-left img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center 30%;
}}
.s1-sketch-sticker {{
    position: absolute;
    bottom: 45px;
    right: 40px;
    background: rgba(255, 255, 255, 0.94);
    backdrop-filter: blur(10px);
    border-radius: 24px;
    border: 2px solid #E2DDD5;
    padding: 18px 22px 14px 22px;
    box-shadow: 0 20px 45px rgba(0,0,0,0.18);
    display: flex;
    flex-direction: column;
    align-items: center;
    z-index: 40;
}}
.s1-sketch-sticker img {{
    height: 380px;
    width: auto;
    object-fit: contain;
}}
.s1-sketch-sticker-lbl {{
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.15em;
    color: #58694B;
    text-transform: uppercase;
    margin-top: 8px;
}}
.s1-right {{
    width: 880px;
    height: 2000px;
    background: #FAF8F5;
    border-left: 2px solid #E2DDD5;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    padding: 85px 70px 65px 70px;
    position: relative;
}}
.s1-top-block {{
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}}
.s1-brand {{
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 32px;
    color: #58694B;
    margin-bottom: 24px;
}}
.s1-kicker {{
    font-size: 21px;
    font-weight: 600;
    letter-spacing: 0.25em;
    color: #2D3728;
    background: #EAE6DF;
    padding: 10px 28px;
    border-radius: 30px;
    margin-bottom: 22px;
}}
.s1-name {{
    font-family: 'Lora', serif;
    font-size: 124px;
    font-weight: 700;
    color: #2D3728;
    line-height: 0.95;
    text-align: center;
    margin-bottom: 12px;
}}
.s1-type {{
    font-size: 30px;
    font-weight: 600;
    letter-spacing: 0.28em;
    color: #58694B;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 22px;
}}
.s1-desc {{
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 25px;
    line-height: 1.5;
    color: #6E6862;
    text-align: center;
    max-width: 720px;
}}
.s1-badges {{
    display: flex;
    flex-direction: column;
    gap: 18px;
    width: 100%;
    margin: 25px 0;
}}
.s1-badge {{
    background: #FFFFFF;
    border: 1.5px solid #E2DDD5;
    border-radius: 20px;
    padding: 24px 28px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 10px 24px rgba(45,55,40,0.05);
}}
.s1-badge-icon {{
    width: 52px;
    height: 52px;
    border-radius: 14px;
    background: #2D3728;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    font-weight: 700;
    flex-shrink: 0;
}}
.s1-badge-title {{
    font-size: 22px;
    font-weight: 600;
    color: #1A1918;
}}
.s1-badge-sub {{
    font-size: 17px;
    color: #6E6862;
    margin-top: 3px;
}}
.s1-trust-pill {{
    background: #2D3728;
    color: #FFFFFF;
    border-radius: 16px;
    padding: 16px 28px;
    font-size: 18px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-align: center;
    width: 100%;
}}
.s1-footer {{
    width: 100%;
    text-align: center;
    padding-top: 25px;
    border-top: 2px solid #EAE3DC;
}}
.s1-footer-tag {{
    font-size: 21px;
    font-weight: 700;
    letter-spacing: 0.2em;
    color: #2D3728;
    text-transform: uppercase;
}}
.s1-footer-sub {{
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 22px;
    color: #6E6862;
    margin-top: 6px;
}}
</style></head><body>
<div class="top-accent-bar"></div>
<div class="s1-container">
    <div class="s1-left">
        <img src="{photo1_uri}" />
        <div class="s1-sketch-sticker">
            <img src="{sketch_front_uri}" />
            <div class="s1-sketch-sticker-lbl">Clean CAD Silhouette</div>
        </div>
    </div>
    <div class="s1-right">
        <div class="s1-top-block">
            <div class="s1-brand">SewLuxePatterns · Atelier Collection</div>
            <div class="s1-kicker">PDF SEWING PATTERN</div>
            <div class="s1-name">Margot</div>
            <div class="s1-type">WIDE-LEG PANTS</div>
            <div class="s1-desc">High-rise relaxed pull-on trousers with continuous elastic waistband casing and concealed in-seam pockets.</div>
        </div>
        
        <div class="s1-badges">
            <div class="s1-badge">
                <div class="s1-badge-icon">13</div>
                <div>
                    <div class="s1-badge-title">SIZES US 00 – 22 (XXS – 4XL)</div>
                    <div class="s1-badge-sub">Full inclusive size range with generous hip ease</div>
                </div>
            </div>
            <div class="s1-badge">
                <div class="s1-badge-icon">✂</div>
                <div>
                    <div class="s1-badge-title">CONFIDENT BEGINNER</div>
                    <div class="s1-badge-sub">Zero zippers, zero buttons, and zero complicated darts</div>
                </div>
            </div>
            <div class="s1-badge">
                <div class="s1-badge-icon">📄</div>
                <div>
                    <div class="s1-badge-title">A4 · US LETTER · A0 · PROJECTOR</div>
                    <div class="s1-badge-sub">Multi-size layered PDF (toggle your size in 1 click)</div>
                </div>
            </div>
            <div class="s1-badge">
                <div class="s1-badge-icon">▶</div>
                <div>
                    <div class="s1-badge-title">ILLUSTRATED GUIDE + VIDEO HUB</div>
                    <div class="s1-badge-sub">Step-by-step vector diagrams & clickable video tutorials</div>
                </div>
            </div>
        </div>

        <div class="s1-trust-pill">
            ⭐ 100% TESTED FIT · DETAILED 16-PAGE BOOKLET · LIFETIME UPDATES
        </div>
        
        <div class="s1-footer">
            <div class="s1-footer-tag">INSTANT DIGITAL DOWNLOAD</div>
            <div class="s1-footer-sub">Start sewing your dream linen trousers today</div>
        </div>
    </div>
</div>
</body></html>
"""

# ==================== SLIDE 2: 3-ANGLE FIT & DETAILS ====================
slide2_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s2-grid {{
    display: flex;
    gap: 40px;
    padding: 0 80px;
    margin-top: 20px;
}}
.s2-card {{
    flex: 1;
    height: 1540px;
    position: relative;
    border-radius: 28px;
    overflow: hidden;
    background: #FFFFFF;
    border: 2px solid #E2DDD5;
    box-shadow: 0 16px 40px rgba(45, 55, 40, 0.08);
    display: flex;
    flex-direction: column;
}}
.s2-card-img {{
    width: 100%;
    height: 1360px;
    position: relative;
    overflow: hidden;
}}
.s2-card-img img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center 25%;
}}
.s2-pill {{
    position: absolute;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(45, 55, 40, 0.92);
    backdrop-filter: blur(8px);
    color: #FFFFFF;
    padding: 14px 32px;
    border-radius: 40px;
    font-size: 19px;
    font-weight: 600;
    letter-spacing: 0.05em;
    white-space: nowrap;
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
}}
.s2-bottom-bar {{
    height: 180px;
    background: #FFFFFF;
    padding: 24px 30px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border-top: 1.5px solid #EAE3DC;
}}
.s2-bottom-title {{
    font-family: 'Lora', serif;
    font-size: 26px;
    font-weight: 700;
    color: #2D3728;
}}
.s2-bottom-desc {{
    font-size: 17px;
    color: #6E6862;
    margin-top: 4px;
    text-align: center;
}}
.s2-strip {{
    position: absolute;
    bottom: 45px;
    left: 80px;
    right: 80px;
    background: #2D3728;
    color: #FFFFFF;
    border-radius: 20px;
    padding: 22px 40px;
    display: flex;
    justify-content: space-around;
    align-items: center;
}}
.s2-strip-item {{
    font-size: 20px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 12px;
}}
.s2-strip-dot {{
    width: 8px;
    height: 8px;
    background: #9BB08B;
    border-radius: 50%;
}}
</style></head><body>
<div class="top-accent-bar"></div>
<div class="slide-header">
    <div class="slide-kicker">360° FIT & PERSPECTIVE</div>
    <div class="slide-title">Thoughtful Construction & Fluid Drape</div>
    <div class="slide-subtitle">Three authentic angles showcasing the relaxed high-rise silhouette in washed linen</div>
</div>

<div class="s2-grid">
    <div class="s2-card">
        <div class="s2-card-img">
            <img src="{photo1_uri}" />
            <div class="s2-pill">FRONT VIEW</div>
        </div>
        <div class="s2-bottom-bar">
            <div class="s2-bottom-title">Continuous Elastic Casing</div>
            <div class="s2-bottom-desc">High-rise fit sits comfortably at the natural waist</div>
        </div>
    </div>
    
    <div class="s2-card">
        <div class="s2-card-img">
            <img src="{photo2_uri}" />
            <div class="s2-pill">SIDE 45° PROFILE</div>
        </div>
        <div class="s2-bottom-bar">
            <div class="s2-bottom-title">Concealed In-Seam Pockets</div>
            <div class="s2-bottom-desc">Anchored smoothly into side seams with zero gaping</div>
        </div>
    </div>
    
    <div class="s2-card">
        <div class="s2-card-img">
            <img src="{photo3_uri}" />
            <div class="s2-pill">BACK VIEW</div>
        </div>
        <div class="s2-bottom-bar">
            <div class="s2-bottom-title">Clean Unadorned Drape</div>
            <div class="s2-bottom-desc">Smooth center back fall with zero bulk or fussy darts</div>
        </div>
    </div>
</div>

<div class="s2-strip">
    <div class="s2-strip-item"><span>✔</span> PULL-ON SIMPLICITY</div>
    <div class="s2-strip-dot"></div>
    <div class="s2-strip-item"><span>✔</span> ZERO ZIPPER BULK</div>
    <div class="s2-strip-dot"></div>
    <div class="s2-strip-item"><span>✔</span> 4.75 CM HIP EASE</div>
    <div class="s2-strip-dot"></div>
    <div class="s2-strip-item"><span>✔</span> ROOMY IN-SEAM POCKETS</div>
</div>
</body></html>
"""

# ==================== SLIDE 3: TECHNICAL FLAT SKETCH ====================
slide3_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s3-content {{
    display: flex;
    gap: 40px;
    padding: 0 80px;
    margin-top: 25px;
}}
.s3-col-side {{
    width: 480px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 1530px;
}}
.s3-center {{
    flex: 1;
    height: 1530px;
    background: #FFFFFF;
    border-radius: 28px;
    border: 2px solid #E2DDD5;
    box-shadow: 0 16px 40px rgba(45, 55, 40, 0.06);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    padding: 40px 30px;
    background-image: radial-gradient(#DCD7D0 1.5px, transparent 1.5px);
    background-size: 32px 32px;
}}
.s3-box {{
    background: #FFFFFF;
    border-radius: 24px;
    border: 1.5px solid #E2DDD5;
    padding: 38px 34px;
    box-shadow: 0 10px 28px rgba(45,55,40,0.04);
}}
.s3-box-head {{
    font-size: 22px;
    font-weight: 700;
    color: #2D3728;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
}}
.s3-box-head-icon {{
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: #58694B;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}}
.s3-item {{
    display: flex;
    align-items: flex-start;
    gap: 12px;
    font-size: 19px;
    line-height: 1.55;
    color: #1A1918;
    margin-bottom: 14px;
}}
.s3-check {{
    color: #58694B;
    font-weight: 700;
}}
.s3-sketches {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 70px;
    width: 100%;
}}
.s3-sketch-card {{
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
}}
.s3-sketch-card img {{
    height: 1140px;
    width: auto;
    object-fit: contain;
    filter: drop-shadow(0 14px 28px rgba(0,0,0,0.08));
}}
.s3-badge-bottom {{
    position: absolute;
    bottom: 35px;
    background: #FAF8F5;
    border: 2px solid #2D3728;
    border-radius: 30px;
    padding: 14px 44px;
    font-size: 20px;
    font-weight: 700;
    color: #2D3728;
    letter-spacing: 0.05em;
}}
</style></head><body>
<div class="top-accent-bar"></div>
<div class="slide-header">
    <div class="slide-kicker">ACCURATE CAD BLUEPRINT</div>
    <div class="slide-title">Technical Flat Sketch & Design Anatomy</div>
    <div class="slide-subtitle">100% faithful to the authentic vector pattern pieces included in your download</div>
</div>

<div class="s3-content">
    <div class="s3-col-side">
        <div class="s3-box">
            <div class="s3-box-head">
                <div class="s3-box-head-icon">✂</div>
                DESIGN FEATURES
            </div>
            <div class="s3-item"><span class="s3-check">✔</span> High-rise waist with continuous elastic casing</div>
            <div class="s3-item"><span class="s3-check">✔</span> Deep concealed in-seam side pockets</div>
            <div class="s3-item"><span class="s3-check">✔</span> Wide straight leg with elegant fluid fall</div>
            <div class="s3-item"><span class="s3-check">✔</span> Clean unadorned back with zero darts</div>
            <div class="s3-item"><span class="s3-check">✔</span> Weighted 3 cm (1 1/8 in) clean double-fold hem</div>
        </div>
        
        <div class="s3-box">
            <div class="s3-box-head">
                <div class="s3-box-head-icon">📐</div>
                PATTERN DETAILS
            </div>
            <div class="s3-item"><span class="s3-check">✔</span> 4 Master pattern pieces total</div>
            <div class="s3-item"><span class="s3-check">✔</span> 1 cm (3/8 in) seam allowance included</div>
            <div class="s3-item"><span class="s3-check">✔</span> 3 cm (1 1/8 in) hem allowance included</div>
            <div class="s3-item"><span class="s3-check">✔</span> Multi-size layered PDF functionality</div>
        </div>
    </div>
    
    <div class="s3-center">
        <div class="s3-sketches">
            <div class="s3-sketch-card">
                <img src="{sketch_front_uri}" />
            </div>
            <div class="s3-sketch-card">
                <img src="{sketch_back_uri}" />
            </div>
        </div>
        <div class="s3-badge-bottom">100% CAD VECTOR ACCURACY · SEAM ALLOWANCES INCLUDED</div>
    </div>
    
    <div class="s3-col-side">
        <div class="s3-box">
            <div class="s3-box-head">
                <div class="s3-box-head-icon">⭐</div>
                SEWING DIFFICULTY
            </div>
            <div style="font-size: 28px; font-weight: 700; color: #2D3728; margin-bottom: 12px;">Confident Beginner</div>
            <div style="font-size: 19px; line-height: 1.6; color: #6E6862;">Perfect first trousers project! No fiddly zippers, buttons, or fly plackets to sew. Easy elastic insertion and straightforward side pockets.</div>
        </div>
        
        <div class="s3-box">
            <div class="s3-box-head">
                <div class="s3-box-head-icon">⏱</div>
                ESTIMATED TIME
            </div>
            <div style="font-size: 28px; font-weight: 700; color: #2D3728; margin-bottom: 12px;">3 to 4 Hours</div>
            <div style="font-size: 19px; line-height: 1.6; color: #6E6862;">Enjoyable afternoon project from cutting fabric to final steam press. Video tutorials included for every key step.</div>
        </div>
    </div>
</div>
</body></html>
"""

# ==================== SLIDE 4: SIZE CHARTS ====================
sizes = ['00', '0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22']
body_rows_html = ""
fin_rows_html = ""
for idx, sz in enumerate(sizes):
    d_body = size_data.get(sz, {}).get("body", {})
    d_fin = size_data.get(sz, {}).get("finished", {})
    bg = "#F6F4F0" if idx % 2 == 1 else "#FFFFFF"
    
    body_rows_html += f"""
    <tr style="background: {bg};">
        <td style="font-weight: 700; color: #2D3728;">US {sz}</td>
        <td>{d_body.get('waist_cm', '-')}</td>
        <td>{d_body.get('hips_cm', '-')}</td>
        <td>{d_body.get('waist_in', '-')}"</td>
        <td>{d_body.get('hips_in', '-')}"</td>
    </tr>
    """
    
    fin_rows_html += f"""
    <tr style="background: {bg};">
        <td style="font-weight: 700; color: #2D3728;">US {sz}</td>
        <td>{d_fin.get('hips_cm', '-')} ({d_fin.get('hips_in', '-')}")</td>
        <td>{d_fin.get('inseam_cm', '-')} ({d_fin.get('inseam_in', '-')}")</td>
        <td>{d_fin.get('leg_opening_cm', '-')} ({d_fin.get('leg_opening_in', '-')}")</td>
        <td>{d_fin.get('elastic_length_cm', '-')} ({d_fin.get('elastic_length_in', '-')}")</td>
    </tr>
    """

slide4_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s4-container {{
    padding: 0 80px;
    margin-top: 15px;
    display: flex;
    flex-direction: column;
    gap: 30px;
}}
.s4-card {{
    background: #FFFFFF;
    border-radius: 26px;
    border: 2px solid #E2DDD5;
    padding: 32px 40px;
    box-shadow: 0 16px 40px rgba(45, 55, 40, 0.06);
}}
.s4-head {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}}
.s4-card-title {{
    font-size: 24px;
    font-weight: 700;
    color: #2D3728;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}}
.s4-card-pill {{
    background: #EAE6DF;
    color: #58694B;
    font-size: 16px;
    font-weight: 700;
    padding: 8px 22px;
    border-radius: 30px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}}
.s4-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 19px;
    text-align: center;
}}
.s4-table th {{
    background: #2D3728;
    color: #FFFFFF;
    padding: 14px 16px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-size: 17px;
}}
.s4-table td {{
    padding: 11px 14px;
    border-bottom: 1px solid #ECE7E1;
    color: #1A1918;
}}
</style></head><body>
<div class="top-accent-bar"></div>
<div class="slide-header">
    <div class="slide-kicker">INCLUSIVE US 00–22 (XXS–4XL)</div>
    <div class="slide-title">Size Charts & Finished Measurements</div>
    <div class="slide-subtitle">Clear dual measurements in both inches and centimeters for effortless fit selection</div>
</div>

<div class="s4-container">
    <div class="s4-card">
        <div class="s4-head">
            <div class="s4-card-title">Body Measurements</div>
            <div class="s4-card-pill">Choose size by full hip measurement</div>
        </div>
        <table class="s4-table">
            <thead>
                <tr>
                    <th style="border-radius: 12px 0 0 12px;">US Size</th>
                    <th>Waist (cm)</th>
                    <th>Hips (cm)</th>
                    <th>Waist (in)</th>
                    <th style="border-radius: 0 12px 12px 0;">Hips (in)</th>
                </tr>
            </thead>
            <tbody>
                {body_rows_html}
            </tbody>
        </table>
    </div>

    <div class="s4-card">
        <div class="s4-head">
            <div class="s4-card-title">Finished Garment Measurements</div>
            <div class="s4-card-pill">Includes relaxed wearing ease</div>
        </div>
        <table class="s4-table">
            <thead>
                <tr>
                    <th style="border-radius: 12px 0 0 12px;">US Size</th>
                    <th>Finished Hip</th>
                    <th>Inseam Length</th>
                    <th>Bottom Leg Opening</th>
                    <th style="border-radius: 0 12px 12px 0;">Cut Elastic Length</th>
                </tr>
            </thead>
            <tbody>
                {fin_rows_html}
            </tbody>
        </table>
    </div>
</div>
</body></html>
"""

# ==================== SLIDE 5: FABRIC & NOTIONS ====================
slide5_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s5-container {{
    padding: 0 80px;
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 1540px;
}}
.s5-card {{
    background: #FFFFFF;
    border-radius: 26px;
    border: 2px solid #E2DDD5;
    padding: 34px 44px;
    box-shadow: 0 16px 40px rgba(45, 55, 40, 0.06);
}}
.s5-card-title {{
    font-size: 24px;
    font-weight: 700;
    color: #2D3728;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 18px;
}}
.s5-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 20px;
    text-align: left;
}}
.s5-table th {{
    background: #2D3728;
    color: #FFFFFF;
    padding: 15px 22px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-size: 18px;
}}
.s5-table td {{
    padding: 14px 22px;
    border-bottom: 1px solid #ECE7E1;
}}
.s5-grid-mid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 36px;
}}
.s5-box {{
    background: #FFFFFF;
    border-radius: 26px;
    border: 2px solid #E2DDD5;
    padding: 34px 42px;
    box-shadow: 0 16px 40px rgba(45, 55, 40, 0.06);
}}
.s5-box-head {{
    font-size: 22px;
    font-weight: 700;
    color: #2D3728;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 14px;
}}
.s5-box-icon {{
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: #58694B;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
}}
.s5-item {{
    font-size: 19px;
    line-height: 1.55;
    color: #1A1918;
    margin-bottom: 12px;
    display: flex;
    gap: 12px;
}}
.s5-check {{
    color: #58694B;
    font-weight: 700;
}}
.s5-grid-tips {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 32px;
}}
.s5-tip-card {{
    background: #FAF8F5;
    border: 2px solid #2D3728;
    border-radius: 22px;
    padding: 26px 30px;
    display: flex;
    flex-direction: column;
}}
.s5-tip-title {{
    font-size: 20px;
    font-weight: 700;
    color: #2D3728;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
}}
.s5-tip-desc {{
    font-size: 17px;
    line-height: 1.5;
    color: #6E6862;
}}
.s5-banner {{
    background: #2D3728;
    color: #FFFFFF;
    border-radius: 20px;
    padding: 20px 40px;
    text-align: center;
    font-size: 20px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}}
</style></head><body>
<div class="top-accent-bar"></div>
<div class="slide-header">
    <div class="slide-kicker">FABRIC & SUPPLIES GUIDE</div>
    <div class="slide-title">Yardage Requirements & Sewing Notions</div>
    <div class="slide-subtitle">Clear fabric estimates for both standard 150 cm (60") and 115 cm (45") widths</div>
</div>

<div class="s5-container">
    <div class="s5-card">
        <div class="s5-card-title">Main Fabric Yardage Estimate</div>
        <table class="s5-table">
            <thead>
                <tr>
                    <th style="border-radius: 12px 0 0 12px;">Size Tier</th>
                    <th>140–150 cm (55–60 in) Width</th>
                    <th>Pocket Lining (Batiste / Self)</th>
                    <th style="border-radius: 0 12px 12px 0;">Matching Thread</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-weight: 700; color: #2D3728;">US 00 – US 4</td>
                    <td>2.10 m (2.30 yards)</td>
                    <td>0.35 m (0.40 yards)</td>
                    <td>1 spool all-purpose polyester</td>
                </tr>
                <tr style="background: #F6F4F0;">
                    <td style="font-weight: 700; color: #2D3728;">US 6 – US 12</td>
                    <td>2.35 m (2.60 yards)</td>
                    <td>0.35 m (0.40 yards)</td>
                    <td>1 spool all-purpose polyester</td>
                </tr>
                <tr>
                    <td style="font-weight: 700; color: #2D3728;">US 14 – US 18</td>
                    <td>2.65 m (2.90 yards)</td>
                    <td>0.40 m (0.45 yards)</td>
                    <td>1 spool all-purpose polyester</td>
                </tr>
                <tr style="background: #F6F4F0;">
                    <td style="font-weight: 700; color: #2D3728;">US 20 – US 22</td>
                    <td>2.90 m (3.20 yards)</td>
                    <td>0.40 m (0.45 yards)</td>
                    <td>1 spool all-purpose polyester</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="s5-grid-mid">
        <div class="s5-box">
            <div class="s5-box-head">
                <div class="s5-box-icon">🌿</div>
                SUGGESTED FABRICS
            </div>
            <div class="s5-item"><span class="s5-check">✔</span> <strong>Washed Pure Linen:</strong> Signature breathable drape with relaxed fluid movement</div>
            <div class="s5-item"><span class="s5-check">✔</span> <strong>Linen-Cotton Blends:</strong> Crisp stability with reduced wrinkling</div>
            <div class="s5-item"><span class="s5-check">✔</span> <strong>Tencel Lyocell / Modal:</strong> Silky, heavy liquid drape for luxury styling</div>
            <div class="s5-item"><span class="s5-check">✔</span> <strong>Soft Cotton Twill / Chambray:</strong> Everyday casual durability</div>
        </div>

        <div class="s5-box">
            <div class="s5-box-head">
                <div class="s5-box-icon">🧵</div>
                REQUIRED NOTIONS & TOOLS
            </div>
            <div class="s5-item"><span class="s5-check">✔</span> <strong>Waistband Elastic:</strong> 3.3 cm (1 1/4 in) wide non-roll knitted or woven elastic</div>
            <div class="s5-item"><span class="s5-check">✔</span> <strong>Sewing Machine Needle:</strong> Universal size 80/12 (or Microtex 75/11 for tencel)</div>
            <div class="s5-item"><span class="s5-check">✔</span> <strong>Sewing Thread:</strong> 100% all-purpose polyester matching your main fabric</div>
            <div class="s5-item"><span class="s5-check">✔</span> <strong>Standard Tools:</strong> Large safety pin or bodkin, fabric shears, iron, and pins</div>
        </div>
    </div>

    <div class="s5-grid-tips">
        <div class="s5-tip-card">
            <div class="s5-tip-title">💧 Pre-Wash Fiber Care</div>
            <div class="s5-tip-desc">Always wash and steam-press your woven fabric before cutting to account for 4–8% natural shrinkage.</div>
        </div>
        <div class="s5-tip-card">
            <div class="s5-tip-title">📏 Elastic Length Choice</div>
            <div class="s5-tip-desc">Consult the finished elastic cut chart on Slide 4 and wrap snugly around your natural waist for bespoke comfort.</div>
        </div>
        <div class="s5-tip-card">
            <div class="s5-tip-title">⚡ Seam Finishing Options</div>
            <div class="s5-tip-desc">Finish raw edges with a serger / overlocker, clean zigzag stitch, or classic French seams for a couture interior.</div>
        </div>
    </div>

    <div class="s5-banner">
        🌿 SUSTAINABLE SEWING · RECOMMENDED NATURAL BREATHABLE FABRICS FOR LIFETIME WEAR
    </div>
</div>
</body></html>
"""

# ==================== SLIDE 6: WHAT YOU RECEIVE ====================
slide6_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s6-container {{
    padding: 0 80px;
    margin-top: 25px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 1680px;
}}
.s6-grid-top {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 36px;
}}
.s6-card {{
    background: #FFFFFF;
    border-radius: 26px;
    border: 2px solid #E2DDD5;
    padding: 54px 36px;
    box-shadow: 0 16px 40px rgba(45, 55, 40, 0.06);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}}
.s6-icon {{
    width: 90px;
    height: 90px;
    border-radius: 26px;
    background: #2D3728;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 44px;
    margin-bottom: 22px;
}}
.s6-title {{
    font-family: 'Lora', serif;
    font-size: 32px;
    font-weight: 700;
    color: #2D3728;
    margin-bottom: 12px;
}}
.s6-desc {{
    font-size: 20px;
    line-height: 1.55;
    color: #6E6862;
}}
.s6-grid-features {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 36px;
}}
.s6-feature-card {{
    background: #FFFFFF;
    border-radius: 24px;
    border: 2px solid #58694B;
    padding: 40px 38px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 10px 28px rgba(45, 55, 40, 0.05);
}}
.s6-feature-head {{
    font-size: 24px;
    font-weight: 700;
    color: #2D3728;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
}}
.s6-feature-text {{
    font-size: 19px;
    line-height: 1.55;
    color: #6E6862;
}}
.s6-banner {{
    background: #2D3728;
    color: #FFFFFF;
    border-radius: 24px;
    padding: 34px 50px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}
.s6-banner-left {{
    font-size: 22px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 14px;
}}
.s6-banner-right {{
    font-size: 20px;
    letter-spacing: 0.12em;
    color: #9BB08B;
    text-transform: uppercase;
    font-weight: 700;
}}
</style></head><body>
<div class="top-accent-bar"></div>
<div class="slide-header">
    <div class="slide-kicker">INSTANT DIGITAL BUNDLE</div>
    <div class="slide-title">Everything Included in Your Download</div>
    <div class="slide-subtitle">All formats included — ready for home printing, local copy shops, or fabric projection</div>
</div>

<div class="s6-container">
    <div class="s6-grid-top">
        <div class="s6-card">
            <div class="s6-icon">📖</div>
            <div class="s6-title">Illustrated Booklet</div>
            <div class="s6-desc">Comprehensive step-by-step PDF instruction guide with 300-DPI vector diagrams, size charts, and beginner tips.</div>
        </div>
        
        <div class="s6-card">
            <div class="s6-icon">🏠</div>
            <div class="s6-title">A4 Print-at-Home</div>
            <div class="s6-desc">Standard international A4 format with page tile numbers, alignment crosses, and a 4x4 in (10x10 cm) test square.</div>
        </div>
        
        <div class="s6-card">
            <div class="s6-icon">📄</div>
            <div class="s6-title">US Letter Format</div>
            <div class="s6-desc">Standard North American 8.5 x 11 in format formatted for easy home assembly with clean border overlap margins.</div>
        </div>
        
        <div class="s6-card">
            <div class="s6-icon">🖨️</div>
            <div class="s6-title">A0 Copyshop Large</div>
            <div class="s6-desc">Full-scale continuous single sheet file for local printing shops. Zero trimming, zero taping, and zero assembly needed!</div>
        </div>
        
        <div class="s6-card">
            <div class="s6-icon">💡</div>
            <div class="s6-title">Multi-Size Layers</div>
            <div class="s6-desc">Toggle your exact size in free Adobe Acrobat Reader. Save paper and ink by printing only the size you need!</div>
        </div>
        
        <div class="s6-card">
            <div class="s6-icon">▶️</div>
            <div class="s6-title">Video Tutorials Hub</div>
            <div class="s6-desc">Clickable hyperlinks and QR codes for video guides on pockets, crotch seams, waistband casing, and hems.</div>
        </div>
    </div>

    <div class="s6-grid-features">
        <div class="s6-feature-card">
            <div class="s6-feature-head">🎯 Layered Acrobat PDF</div>
            <div class="s6-feature-text">Print ONLY size 8 or size 12 without clutter. Cleaner cutting lines and zero pattern confusion.</div>
        </div>
        <div class="s6-feature-card">
            <div class="s6-feature-head">📏 4x4 In Test Square</div>
            <div class="s6-feature-text">Guaranteed 100% scale accuracy on any standard home printer before cutting your precious fabric.</div>
        </div>
        <div class="s6-feature-card">
            <div class="s6-feature-head">📽️ Projector Friendly</div>
            <div class="s6-feature-text">Thick high-contrast vector lines formatted for modern ceiling and wall projector setups.</div>
        </div>
    </div>

    <div class="s6-banner">
        <div class="s6-banner-left">⚡ Immediate Access Via Etsy Purchases · Personal Home Sewing License</div>
        <div class="s6-banner-right">SewLuxePatterns Standard</div>
    </div>
</div>
</body></html>
"""

# ==================== SLIDE 7: INSIDE BOOKLET ====================
slide7_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s7-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 36px;
    padding: 0 80px;
    margin-top: 25px;
}}
.s7-card {{
    background: #FFFFFF;
    border-radius: 26px;
    border: 2px solid #E2DDD5;
    padding: 24px;
    box-shadow: 0 16px 36px rgba(45, 55, 40, 0.08);
    display: flex;
    flex-direction: column;
    align-items: center;
}}
.s7-img-wrapper {{
    width: 100%;
    height: 1260px;
    border-radius: 16px;
    overflow: hidden;
    background: #FFFFFF;
    border: 1.5px solid #EAE3DC;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    display: flex;
    align-items: center;
    justify-content: center;
}}
.s7-img-wrapper img {{
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}}
.s7-page-lbl {{
    margin-top: 24px;
    font-size: 22px;
    font-weight: 700;
    color: #2D3728;
    text-align: center;
}}
.s7-page-desc {{
    font-size: 17px;
    color: #6E6862;
    text-align: center;
    margin-top: 6px;
}}
.s7-bottom {{
    margin: 40px 80px 0 80px;
    background: #FFFFFF;
    border: 2px solid #2D3728;
    border-radius: 22px;
    padding: 26px 40px;
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    color: #2D3728;
    letter-spacing: 0.05em;
}}
</style></head><body>
<div class="top-accent-bar"></div>
<div class="slide-header">
    <div class="slide-kicker">CRYSTAL-CLEAR INSTRUCTIONS</div>
    <div class="slide-title">Inside the Illustrated Instruction Booklet</div>
    <div class="slide-subtitle">Real preview pages showing our signature luxury layout, vector diagrams, and beginner tips</div>
</div>

<div class="s7-grid">
    <div class="s7-card">
        <div class="s7-img-wrapper"><img src="{bp3_uri}" /></div>
        <div class="s7-page-lbl">Page 3: Checklist & Test</div>
        <div class="s7-page-desc">4x4 in calibration square & pre-wash guide</div>
    </div>
    
    <div class="s7-card">
        <div class="s7-img-wrapper"><img src="{bp4_uri}" /></div>
        <div class="s7-page-lbl">Page 4: Size Charts</div>
        <div class="s7-page-desc">Body & finished measurements with ease specs</div>
    </div>
    
    <div class="s7-card">
        <div class="s7-img-wrapper"><img src="{bp7_uri}" /></div>
        <div class="s7-page-lbl">Page 7: Pieces & Markings</div>
        <div class="s7-page-desc">Authentic pattern schematics & balance lines</div>
    </div>
    
    <div class="s7-card">
        <div class="s7-img-wrapper"><img src="{bp13_uri}" /></div>
        <div class="s7-page-lbl">Page 13: Sewing Steps</div>
        <div class="s7-page-desc">High-res vector panels with beginner tips</div>
    </div>
</div>

<div class="s7-bottom">
    ⭐ 300 DPI ORIGINAL VECTOR DIAGRAMS · ZERO SCREENSHOTS · 100% READABLE TEXT
</div>
</body></html>
"""

# ==================== SLIDE 8: VIDEO TUTORIALS ====================
slide8_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s8-content {{
    display: flex;
    gap: 40px;
    padding: 0 80px;
    margin-top: 25px;
    height: 1540px;
}}
.s8-left {{
    flex: 1.15;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
.s8-card {{
    background: #FFFFFF;
    border-radius: 24px;
    border: 1.5px solid #E2DDD5;
    padding: 42px 42px;
    box-shadow: 0 10px 28px rgba(45, 55, 40, 0.05);
    display: flex;
    align-items: center;
    gap: 32px;
}}
.s8-num {{
    width: 76px;
    height: 76px;
    border-radius: 22px;
    background: #2D3728;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 34px;
    font-weight: 700;
    flex-shrink: 0;
}}
.s8-card-title {{
    font-family: 'Lora', serif;
    font-size: 30px;
    font-weight: 700;
    color: #2D3728;
    margin-bottom: 8px;
}}
.s8-card-desc {{
    font-size: 20px;
    line-height: 1.55;
    color: #6E6862;
}}
.s8-duration {{
    display: inline-block;
    background: #FAF8F5;
    color: #58694B;
    border: 1.5px solid #58694B;
    border-radius: 12px;
    padding: 5px 16px;
    font-size: 16px;
    font-weight: 700;
    margin-top: 10px;
}}
.s8-left-banner {{
    background: #2D3728;
    color: #FFFFFF;
    border-radius: 22px;
    padding: 30px 40px;
    font-size: 22px;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}
.s8-right {{
    flex: 0.85;
    background: #FFFFFF;
    border-radius: 28px;
    border: 2px solid #E2DDD5;
    padding: 50px 44px;
    box-shadow: 0 16px 40px rgba(45, 55, 40, 0.07);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    text-align: center;
}}
.s8-qr-box {{
    width: 440px;
    height: 440px;
    background: #FAF8F5;
    border: 3px solid #2D3728;
    border-radius: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 30px;
    box-shadow: 0 16px 36px rgba(0,0,0,0.08);
}}
.s8-qr-box img {{
    width: 100%;
    height: 100%;
    object-fit: contain;
}}
.s8-callout {{
    font-family: 'Lora', serif;
    font-size: 42px;
    font-weight: 700;
    color: #2D3728;
    margin-bottom: 12px;
}}
.s8-subtext {{
    font-size: 21px;
    line-height: 1.55;
    color: #6E6862;
    max-width: 520px;
}}
.s8-box-feature {{
    background: #FAF8F5;
    border-radius: 22px;
    border: 1.5px solid #E2DDD5;
    padding: 30px 34px;
    width: 100%;
    text-align: left;
}}
.s8-feature-row {{
    display: flex;
    align-items: center;
    gap: 16px;
    font-size: 20px;
    color: #1A1918;
    margin-bottom: 12px;
}}
.s8-bottom-trust {{
    position: absolute;
    bottom: 45px;
    left: 80px;
    right: 80px;
    background: #2D3728;
    color: #FFFFFF;
    border-radius: 20px;
    padding: 24px 30px;
    text-align: center;
    font-size: 20px;
    font-weight: 600;
    letter-spacing: 0.1em;
}}
</style></head><body>
<div class="top-accent-bar"></div>
<div class="slide-header">
    <div class="slide-kicker">INTERACTIVE VIDEO GUIDANCE</div>
    <div class="slide-title">Clickable Links & QR Video Tutorials Hub</div>
    <div class="slide-subtitle">Watch master tailor demonstrations for every key technique directly on page 8</div>
</div>

<div class="s8-content">
    <div class="s8-left">
        <div class="s8-card">
            <div class="s8-num">1</div>
            <div>
                <div class="s8-card-title">In-Seam Side Pockets Tutorial</div>
                <div class="s8-card-desc">Pinning, stitching, and understitching the pocket bags smoothly for flat, invisible side seams.</div>
                <div class="s8-duration">⏱ 4:15 MIN HD VIDEO</div>
            </div>
        </div>
        
        <div class="s8-card">
            <div class="s8-num">2</div>
            <div>
                <div class="s8-card-title">Sewing Crotch Seam Curve</div>
                <div class="s8-card-desc">Nesting inner thigh seams at the 4-way cross junction and reinforcing curved high-stress points.</div>
                <div class="s8-duration">⏱ 3:40 MIN HD VIDEO</div>
            </div>
        </div>
        
        <div class="s8-card">
            <div class="s8-num">3</div>
            <div>
                <div class="s8-card-title">Continuous Elastic Casing Insertion</div>
                <div class="s8-card-desc">Folding the waistband, threading elastic with a bodkin, and joining ends with a box-and-cross stitch.</div>
                <div class="s8-duration">⏱ 5:20 MIN HD VIDEO</div>
            </div>
        </div>
        
        <div class="s8-card">
            <div class="s8-num">4</div>
            <div>
                <div class="s8-card-title">Hemming Wide-Leg Trousers</div>
                <div class="s8-card-desc">Measuring floor-length drape, double-folding the 3 cm hem, and pressing for a crisp tailored edge.</div>
                <div class="s8-duration">⏱ 3:10 MIN HD VIDEO</div>
            </div>
        </div>

        <div class="s8-left-banner">
            <div>🎬 4 Masterclass Video Lessons Included</div>
            <div style="color: #9BB08B; font-weight: 700;">Zero Experience Needed</div>
        </div>
    </div>
    
    <div class="s8-right">
        <div>
            <div class="s8-callout">Scan & Learn Instantly</div>
            <div class="s8-subtext">Scan the QR code with your phone camera or click the direct hyperlink inside the PDF to stream video guides immediately in your browser!</div>
        </div>
        
        <div class="s8-qr-box">
            <img src="{qr_code_uri}" />
        </div>
        
        <div class="s8-box-feature">
            <div class="s8-feature-row"><span>📱</span> <strong>100% Smartphone & Tablet Ready</strong></div>
            <div class="s8-feature-row"><span>♾️</span> <strong>Lifetime Access · No Expiration</strong></div>
            <div class="s8-feature-row" style="margin-bottom: 0;"><span>🎥</span> <strong>Close-Up Master Tailor Demonstrations</strong></div>
        </div>

        <div style="font-size: 21px; font-weight: 700; color: #58694B; letter-spacing: 0.12em; text-transform: uppercase;">
            INCLUDED ON BOOKLET PAGE 8
        </div>
    </div>
</div>

<div class="s8-bottom-trust">
    ⭐ 4 COMPREHENSIVE VIDEO LESSONS · STREAM ON ANY DEVICE · LIFETIME ACCESSIBLE VIA QR OR CLICKABLE LINK
</div>
</body></html>
"""

# ==================== SLIDE 9: STYLING & CAPSULE ====================
slide9_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s9-content {{
    display: flex;
    gap: 40px;
    padding: 0 80px;
    margin-top: 25px;
    height: 1680px;
}}
.s9-left {{
    width: 820px;
    height: 1680px;
    border-radius: 28px;
    overflow: hidden;
    border: 2px solid #E2DDD5;
    box-shadow: 0 16px 40px rgba(45, 55, 40, 0.08);
    flex-shrink: 0;
}}
.s9-left img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center 25%;
}}
.s9-right {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 1680px;
}}
.s9-card {{
    background: #FFFFFF;
    border-radius: 24px;
    border: 1.5px solid #E2DDD5;
    padding: 38px 42px;
    box-shadow: 0 10px 28px rgba(45, 55, 40, 0.05);
}}
.s9-look-tag {{
    font-size: 17px;
    font-weight: 700;
    letter-spacing: 0.16em;
    color: #58694B;
    text-transform: uppercase;
    margin-bottom: 8px;
}}
.s9-look-title {{
    font-family: 'Lora', serif;
    font-size: 32px;
    font-weight: 700;
    color: #2D3728;
    margin-bottom: 10px;
}}
.s9-look-desc {{
    font-size: 20px;
    line-height: 1.55;
    color: #6E6862;
}}
.s9-capsule-row {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}}
.s9-capsule-pill {{
    background: #FAF8F5;
    border: 1.5px solid #E2DDD5;
    border-radius: 20px;
    padding: 24px 18px;
    text-align: center;
}}
.s9-capsule-icon {{
    font-size: 34px;
    margin-bottom: 8px;
}}
.s9-capsule-name {{
    font-size: 18px;
    font-weight: 700;
    color: #2D3728;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}}
.s9-care-box {{
    background: #2D3728;
    color: #FFFFFF;
    border-radius: 24px;
    padding: 34px 42px;
}}
.s9-care-title {{
    font-size: 21px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #9BB08B;
    margin-bottom: 8px;
}}
.s9-care-desc {{
    font-size: 19px;
    line-height: 1.55;
    color: #FAF8F5;
}}
</style></head><body>
<div class="top-accent-bar"></div>
<div class="slide-header">
    <div class="slide-kicker">VERSATILE EVERYDAY WARDROBE</div>
    <div class="slide-title">Styling Ideas & Capsule Combinations</div>
    <div class="slide-subtitle">Effortless elegance designed to pair with existing wardrobe staples across seasons</div>
</div>

<div class="s9-content">
    <div class="s9-left">
        <img src="{photo1_uri}" />
    </div>
    
    <div class="s9-right">
        <div class="s9-card">
            <div class="s9-look-tag">LOOK 01 · SUMMER CHIC</div>
            <div class="s9-look-title">Minimalist Resort & Beach</div>
            <div class="s9-look-desc">Pair Margot in washed Sage Olive linen with a fitted ribbed ivory tank top, leather slide sandals, and woven straw tote for effortless warm-weather sophistication.</div>
        </div>
        
        <div class="s9-card">
            <div class="s9-look-tag">LOOK 02 · OFFICE CASUAL</div>
            <div class="s9-look-title">Relaxed Tailored Workwear</div>
            <div class="s9-look-desc">Tuck a crisp oversized white linen button-down into the high waist, add a fine leather belt effect, and complete with tailored leather loafers for breezy office comfort.</div>
        </div>
        
        <div class="s9-card">
            <div class="s9-look-tag">LOOK 03 · AUTUMN TRANSITION</div>
            <div class="s9-look-title">Cozy Weekend Layering</div>
            <div class="s9-look-desc">Style Margot in medium-weight cotton twill with a cropped cashmere sweater, denim jacket, and clean minimalist white sneakers for relaxed weekend strolls.</div>
        </div>

        <div class="s9-capsule-row">
            <div class="s9-capsule-pill">
                <div class="s9-capsule-icon">👡</div>
                <div class="s9-capsule-name">Slides & Loafers</div>
            </div>
            <div class="s9-capsule-pill">
                <div class="s9-capsule-icon">🧺</div>
                <div class="s9-capsule-name">Straw & Leather Totes</div>
            </div>
            <div class="s9-capsule-pill">
                <div class="s9-capsule-icon">✨</div>
                <div class="s9-capsule-name">Warm Gold Accents</div>
            </div>
        </div>
        
        <div class="s9-care-box">
            <div class="s9-care-title">FABRIC CARE GUIDELINE</div>
            <div class="s9-care-desc">Machine wash cold on gentle cycle with mild detergent. Hang to dry or tumble dry low. Press with a warm steam iron while slightly damp for that signature crisp luxury linen texture.</div>
        </div>
    </div>
</div>
</body></html>
"""

# ==================== SLIDE 10: HOW TO DOWNLOAD ====================
slide10_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BASE_CSS}
.s10-container {{
    padding: 0 80px;
    margin-top: 25px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 1680px;
}}
.s10-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 36px;
}}
.s10-card {{
    background: #FFFFFF;
    border-radius: 26px;
    border: 2px solid #E2DDD5;
    padding: 68px 44px;
    box-shadow: 0 16px 40px rgba(45, 55, 40, 0.06);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    position: relative;
}}
.s10-step-num {{
    width: 96px;
    height: 96px;
    border-radius: 30px;
    background: #2D3728;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 46px;
    font-weight: 700;
    margin-bottom: 26px;
}}
.s10-card-title {{
    font-family: 'Lora', serif;
    font-size: 34px;
    font-weight: 700;
    color: #2D3728;
    margin-bottom: 16px;
}}
.s10-card-desc {{
    font-size: 21px;
    line-height: 1.6;
    color: #6E6862;
}}
.s10-compat-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 28px;
}}
.s10-compat-card {{
    background: #FFFFFF;
    border-radius: 24px;
    border: 1.5px solid #E2DDD5;
    padding: 38px 26px;
    text-align: center;
    box-shadow: 0 8px 24px rgba(45,55,40,0.04);
}}
.s10-compat-icon {{
    font-size: 50px;
    margin-bottom: 14px;
}}
.s10-compat-title {{
    font-size: 23px;
    font-weight: 700;
    color: #2D3728;
}}
.s10-compat-sub {{
    font-size: 17px;
    color: #6E6862;
    margin-top: 4px;
}}
.s10-disclaimer {{
    background: #FFFFFF;
    border-radius: 26px;
    border: 2px solid #58694B;
    padding: 44px 54px;
    display: flex;
    align-items: center;
    gap: 34px;
    box-shadow: 0 12px 32px rgba(45,55,40,0.06);
}}
.s10-disclaimer-icon {{
    font-size: 72px;
    flex-shrink: 0;
}}
.s10-disclaimer-title {{
    font-size: 27px;
    font-weight: 700;
    color: #2D3728;
    margin-bottom: 8px;
}}
.s10-disclaimer-desc {{
    font-size: 21px;
    line-height: 1.55;
    color: #6E6862;
}}
.s10-support {{
    background: #2D3728;
    color: #FFFFFF;
    border-radius: 26px;
    padding: 40px 54px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}
.s10-support-text {{
    font-size: 25px;
    font-weight: 600;
}}
.s10-support-badge {{
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: #9BB08B;
    text-transform: uppercase;
}}
</style></head><body>
<div class="top-accent-bar"></div>
<div class="slide-header">
    <div class="slide-kicker">INSTANT ACCESS & EASY PRINTING</div>
    <div class="slide-title">How Instant Digital Download Works</div>
    <div class="slide-subtitle">Get started in three simple steps — from purchase to sewing in minutes</div>
</div>

<div class="s10-container">
    <div class="s10-grid">
        <div class="s10-card">
            <div class="s10-step-num">1</div>
            <div class="s10-card-title">Purchase & Download</div>
            <div class="s10-card-desc">Files are ready immediately after checkout! Access your download anytime via <strong>Etsy > Purchases & Reviews</strong> on your computer browser.</div>
        </div>
        
        <div class="s10-card">
            <div class="s10-step-num">2</div>
            <div class="s10-card-title">Choose Size & Print</div>
            <div class="s10-card-desc">Open in free Adobe Acrobat Reader. Select your size layer, choose A4 or US Letter, and verify the 4x4 in calibration square at 100% scale.</div>
        </div>
        
        <div class="s10-card">
            <div class="s10-step-num">3</div>
            <div class="s10-card-title">Cut & Sew with Joy</div>
            <div class="s10-card-desc">Follow the illustrated 16-page guide step-by-step. Scan the QR codes for instant video tutorials whenever you need extra guidance!</div>
        </div>
    </div>

    <div class="s10-compat-row">
        <div class="s10-compat-card">
            <div class="s10-compat-icon">🍏</div>
            <div class="s10-compat-title">Apple Mac & iPad</div>
            <div class="s10-compat-sub">Preview & Acrobat Reader</div>
        </div>
        <div class="s10-compat-card">
            <div class="s10-compat-icon">🪟</div>
            <div class="s10-compat-title">Windows PC</div>
            <div class="s10-compat-sub">Adobe Acrobat & Foxit</div>
        </div>
        <div class="s10-compat-card">
            <div class="s10-compat-icon">📱</div>
            <div class="s10-compat-title">Mobile Devices</div>
            <div class="s10-compat-sub">iOS & Android PDF Viewers</div>
        </div>
        <div class="s10-compat-card">
            <div class="s10-compat-icon">🖨️</div>
            <div class="s10-compat-title">All Home Printers</div>
            <div class="s10-compat-sub">A4 & US Letter standard</div>
        </div>
    </div>

    <div class="s10-disclaimer">
        <div class="s10-disclaimer-icon">💻</div>
        <div>
            <div class="s10-disclaimer-title">DIGITAL DOWNLOAD PRODUCT ONLY</div>
            <div class="s10-disclaimer-desc">This is a digital PDF sewing pattern. No physical garment or printed paper pattern will be mailed. Download files instantly and print on demand at home or a local print shop.</div>
        </div>
    </div>

    <div class="s10-support">
        <div class="s10-support-text">Questions about fit or printing? We're here to help! Message us anytime via Etsy.</div>
        <div class="s10-support-badge">SewLuxePatterns Customer Care</div>
    </div>
</div>
</body></html>
"""

slides_definitions = [
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
    print("Launching Playwright for pixel-perfect 2000x2000 rendering...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 2000, "height": 2000}, device_scale_factor=1)
        
        for idx, (fname, html_str) in enumerate(slides_definitions):
            tmp_html = os.path.join(SCRATCH_DIR, fname.replace(".jpg", ".html"))
            with open(tmp_html, "w", encoding="utf-8") as f:
                f.write(html_str)
                
            page.goto("file:///" + tmp_html.replace("\\", "/"))
            page.wait_for_timeout(400)
            
            # Save to Desktop listing images
            out_desktop = os.path.join(SLIDES_DIR, fname)
            page.screenshot(path=out_desktop, type="jpeg", quality=95)
            
            # Also save to Artifacts directory for inspection
            out_brain = os.path.join(BRAIN_DIR, fname)
            page.screenshot(path=out_brain, type="jpeg", quality=95)
            
            print(f"  [OK] Rendered Slide {idx+1:02d}: {fname} (2000x2000 px)")
            
        browser.close()
    print("All 10 slides rendered successfully!")

if __name__ == "__main__":
    render_slides()
