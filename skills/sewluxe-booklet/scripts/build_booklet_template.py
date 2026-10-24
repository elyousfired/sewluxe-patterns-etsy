import json
import os
import re
import pymupdf as fitz
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode import qr
from reportlab.graphics import renderPDF

SCRATCH_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\c675070e-91f4-406b-8086-d794cba1db24\scratch"
ARTIFACT_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\c675070e-91f4-406b-8086-d794cba1db24"
PROJECT_DIR = r"C:\Users\red1e\.gemini\antigravity\scratch\colette_wide_leg_trousers"
ASSET_DIR = os.path.join(SCRATCH_DIR, "booklet_assets")
FONTS_DIR = r"C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\fonts"

# 0. Re-render pieces_overview_clean.png at 1200 DPI with centered piece 8 number
pieces_svg_path = os.path.join(SCRATCH_DIR, "pieces_img.svg")
svg_txt = open(pieces_svg_path, encoding="utf-8").read()
def clean_piece_texts(match):
    full = match.group(0)
    content = match.group(1).strip()
    if content.isdigit():
        mx = re.search(r'x="([\d\.]+)"', full)
        my = re.search(r'y="([\d\.]+)"', full)
        if mx and my:
            x, y = float(mx.group(1)), float(my.group(1))
            if content == "8":
                x += 4.5
                y += 1.2
            elif content == "3":
                x += 3.0
                y += 1.0
            elif content == "5":
                y += 3.0
            elif content == "7":
                x += 1.2
                y += 3.0
            else:
                y += 1.5
            return f'<text x="{x:.3f}" y="{y:.3f}" font-size="5.0" font-weight="bold" fill="#8C3B47" font-family="Helvetica, Arial, sans-serif" style="text-anchor: middle">{content}</text>'
    if "rotate(90.0000" in full or "MAIN FABRIC" in content or "LINING:" in content or "FUSIBLE" in content or content in (
        "PANTS FRONT", "PANTS BACK", "WAISTBAND", "POCKET BAG", "FLY FACING",
        "POCKET LINING", "FLY INTERFACING", "BACK POCKET WELT",
        "BACK INNER POCKET BAG", "BACK OUTER POCKET BAG"
    ):
        return ""
    return full

svg_txt_clean = re.sub(r"<text[^>]*>(.*?)</text>", clean_piece_texts, svg_txt, flags=re.S)
vb = re.search(r'viewBox="([\d\.\-\s]+)"', svg_txt_clean)
if vb:
    parts = vb.group(1).split()
    svg_txt_clean = re.sub(
        r"(<svg[^>]*>)",
        rf'\1<rect x="{parts[0]}" y="{parts[1]}" width="{parts[2]}" height="{parts[3]}" fill="#FAF8F6"/>',
        svg_txt_clean,
        count=1,
    )
doc_svg = fitz.open(stream=svg_txt_clean.encode("utf-8"), filetype="svg")
pix_svg = doc_svg[0].get_pixmap(dpi=1200, alpha=False)
pieces_png = os.path.join(ASSET_DIR, "pieces_overview_clean.png")
pix_svg.save(pieces_png)

# Register Fonts
pdfmetrics.registerFont(TTFont("Poppins", os.path.join(FONTS_DIR, "Poppins-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Medium", os.path.join(FONTS_DIR, "Poppins-Medium.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Bold", os.path.join(FONTS_DIR, "Poppins-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Italic", os.path.join(FONTS_DIR, "Poppins-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Lora", os.path.join(FONTS_DIR, "Lora-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Lora-Bold", os.path.join(FONTS_DIR, "Lora-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Lora-Italic", os.path.join(FONTS_DIR, "Lora-Italic.ttf")))

# Colors (matching Odette Vest 100%)
BG_CREAM = HexColor("#FAF8F6")
BURGUNDY = HexColor("#8C3B47")
CHARCOAL = HexColor("#1E1A19")
TEXT_BODY = HexColor("#2C2624")
MUTED = HexColor("#6E655F")
RULE_LINE = HexColor("#DFD9D3")
TABLE_HEAD = HexColor("#1E1A19")
TABLE_ALT = HexColor("#F4EFEA")
TIP_BG = HexColor("#F6ECEA")
GRID_BG = HexColor("#F4EFEA")
WHITE = HexColor("#FFFFFF")

W, H = A4  # 595.275, 841.89
M_L = 50.0
M_R = W - 50.0
CONTENT_W = M_R - M_L

# Load size data
size_data = json.load(open(os.path.join(PROJECT_DIR, "booklet_size_data.json"), encoding="utf-8"))

# Image paths
PHOTO_FRONT = os.path.join(ARTIFACT_DIR, "model_photo_1_front_1792265587295.jpg")
PHOTO_BACK = os.path.join(ARTIFACT_DIR, "model_photo_2_back_1792265665659.jpg")
PHOTO_SIDE = os.path.join(ARTIFACT_DIR, "model_photo_3_side_three_quarter_1792265685202.jpg")
FLAT_SKETCH = os.path.join(PROJECT_DIR, "flat_sketch_transparent.png")

def draw_page_bg_and_chrome(c: canvas.Canvas, page_num: int, is_cover=False):
    c.setFillColor(BG_CREAM)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    if is_cover:
        c.setFillColor(BURGUNDY)
        c.rect(0, H - 16, W, 16, stroke=0, fill=1)
        return
    # Running Header
    c.setFont("Poppins", 7.0)
    c.setFillColor(MUTED)
    c.drawString(M_L, H - 34, "COLETTE TROUSERS  ·  SEWING GUIDE")
    c.drawRightString(M_R, H - 34, "SIZES US 00–22")
    c.setStrokeColor(RULE_LINE)
    c.setLineWidth(0.6)
    c.line(M_L, H - 42, M_R, H - 42)
    # Running Footer
    c.line(M_L, 48, M_R, 48)
    c.setFont("Lora-Italic", 9.5)
    c.setFillColor(BURGUNDY)
    c.drawString(M_L, 32, "SewLuxePatterns")
    c.setFont("Poppins", 8.0)
    c.setFillColor(MUTED)
    c.drawRightString(M_R, 32, str(page_num))

def draw_section_header(c: canvas.Canvas, kicker: str, title: str, y_top=H - 70) -> float:
    c.setFont("Poppins-Medium", 7.5)
    c.setFillColor(BURGUNDY)
    # Spaced kicker
    spaced = " ".join(list(kicker.upper())) if "  " not in kicker else kicker.upper()
    c.drawString(M_L, y_top, spaced)
    c.setFont("Lora", 28)
    c.setFillColor(CHARCOAL)
    c.drawString(M_L, y_top - 34, title)
    c.setStrokeColor(BURGUNDY)
    c.setLineWidth(1.3)
    c.line(M_L, y_top - 48, M_L + 110, y_top - 48)
    return y_top - 72

def wrap_lines(text: str, font_name: str, font_size: float, max_w: float):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(test, font_name, font_size) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_rich_paragraph(c: canvas.Canvas, x: float, y: float, text: str, max_w: float, font_size=9.5, leading=14.5, color=TEXT_BODY) -> float:
    """Supports **bold** inline spans without inserting extra spaces before attached punctuation."""
    # First parse into (text_chunk, is_bold)
    raw_parts = re.split(r"(\*\*.*?\*\*)", text)
    # Build space-separated word groups; each word group is a list of (sub_str, is_bold, font_name, width)
    word_groups = [[]]
    for p in raw_parts:
        if not p:
            continue
        is_b = p.startswith("**") and p.endswith("**")
        content = p[2:-2] if is_b else p
        fn = "Poppins-Medium" if is_b else "Poppins"
        # Split content by whitespace while preserving spaces as separators
        sub_tokens = re.split(r"(\s+)", content)
        for st in sub_tokens:
            if not st:
                continue
            if st.isspace():
                if word_groups[-1]:
                    word_groups.append([])
            else:
                ww = pdfmetrics.stringWidth(st, fn, font_size)
                word_groups[-1].append((st, is_b, fn, ww))
    word_groups = [wg for wg in word_groups if wg]

    lines = []
    cur_line = []
    cur_w = 0.0
    space_w = pdfmetrics.stringWidth(" ", "Poppins", font_size)
    for wg in word_groups:
        wg_w = sum(seg[3] for seg in wg)
        add_w = wg_w if not cur_line else space_w + wg_w
        if cur_w + add_w <= max_w:
            cur_line.append((wg, wg_w))
            cur_w += add_w
        else:
            lines.append(cur_line)
            cur_line = [(wg, wg_w)]
            cur_w = wg_w
    if cur_line:
        lines.append(cur_line)

    for line in lines:
        cx = x
        for wg, wg_w in line:
            for seg_str, is_b, fn, seg_w in wg:
                c.setFont(fn, font_size)
                c.setFillColor(CHARCOAL if is_b else color)
                c.drawString(cx, y, seg_str)
                cx += seg_w
            cx += space_w
        y -= leading
    return y

def draw_bullet(c: canvas.Canvas, x: float, y: float, text: str, max_w: float, font_size=9.3, leading=14.0) -> float:
    c.setFillColor(CHARCOAL)
    c.circle(x + 2.5, y + 3.2, 1.3, stroke=0, fill=1)
    y_next = draw_rich_paragraph(c, x + 12, y, text, max_w - 12, font_size=font_size, leading=leading)
    return y_next - 3.5

def draw_tip_box(c: canvas.Canvas, y_top: float, title: str, text: str) -> float:
    lines = wrap_lines(text, "Poppins", 8.8, CONTENT_W - 32)
    box_h = 28 + len(lines) * 13.0 + 10
    y_bot = y_top - box_h
    c.setFillColor(TIP_BG)
    c.rect(M_L, y_bot, CONTENT_W, box_h, stroke=0, fill=1)
    c.setFillColor(BURGUNDY)
    c.rect(M_L, y_bot, 3.0, box_h, stroke=0, fill=1)
    c.setFont("Poppins-Medium", 9.2)
    c.setFillColor(BURGUNDY)
    c.drawString(M_L + 16, y_top - 18, title)
    ty = y_top - 33
    c.setFont("Poppins", 8.8)
    c.setFillColor(TEXT_BODY)
    for ln in lines:
        c.drawString(M_L + 16, ty, ln)
        ty -= 13.0
    return y_bot - 14

def draw_step_header(c: canvas.Canvas, y: float, step_num: int, title: str, right_note: str) -> float:
    c.setFillColor(BURGUNDY)
    c.circle(M_L + 15, y + 6, 15, stroke=0, fill=1)
    c.setFont("Poppins-Medium", 11.5)
    c.setFillColor(WHITE)
    c.drawCentredString(M_L + 15, y + 2, str(step_num))
    c.setFont("Lora", 19.5)
    c.setFillColor(CHARCOAL)
    c.drawString(M_L + 40, y, title)
    c.setFont("Poppins", 8.2)
    c.setFillColor(MUTED)
    c.drawRightString(M_R, y + 2, right_note)
    c.setStrokeColor(RULE_LINE)
    c.setLineWidth(0.6)
    c.line(M_L, y - 14, M_R, y - 14)
    return y - 32

out_pdf_path = os.path.join(PROJECT_DIR, "Colette-Trousers_Sewing-Instructions.pdf")
c = canvas.Canvas(out_pdf_path, pagesize=A4)

# =========================================================================
# PAGE 1: COVER
# =========================================================================
draw_page_bg_and_chrome(c, 1, is_cover=True)
c.setFont("Poppins-Medium", 7.5)
c.setFillColor(BURGUNDY)
c.drawString(82, H - 46, "S E W I N G   P A T T E R N   ·   I N S T R U C T I O N   B O O K L E T")

c.setFont("Lora", 48)
c.setFillColor(CHARCOAL)
c.drawString(80, H - 96, "Colette")

c.setFont("Poppins-Medium", 11.5)
c.setFillColor(CHARCOAL)
c.drawString(82, H - 122, "T R O U S E R S")

c.setFont("Lora-Italic", 10.8)
c.setFillColor(TEXT_BODY)
c.drawString(82, H - 148, "High-waisted wide-leg tailored trousers with double front pleats,")
c.drawString(82, H - 163, "slanted side pockets, back single-welt pockets, and a classic zipper fly.")

# Cover Photo (square 431 x 431)
photo_sz = 431
c.drawImage(PHOTO_FRONT, (W - photo_sz) / 2, H - 205 - photo_sz, width=photo_sz, height=photo_sz, preserveAspectRatio=True, mask="auto")

# Spec rules & 4-col bar
y_spec = H - 205 - photo_sz - 24
c.setStrokeColor(BURGUNDY)
c.setLineWidth(1.0)
c.line(82, y_spec, W - 82, y_spec)

cols_x = [82, 160, 278, 412]
specs_cover = [
    ("S I Z E S", "US 00 – 22"),
    ("L E V E L", "Intermediate"),
    ("S E A M   A L L O W A N C E", "1 cm (3/8 in) included"),
    ("F O R M A T S", "A4 · US Letter · A0"),
]
for cx_col, (lbl, val) in zip(cols_x, specs_cover):
    c.setFont("Poppins-Medium", 6.5)
    c.setFillColor(BURGUNDY)
    c.drawString(cx_col, y_spec - 15, lbl)
    c.setFont("Poppins", 8.5)
    c.setFillColor(CHARCOAL)
    c.drawString(cx_col, y_spec - 28, val)

c.setFont("Poppins", 6.5)
c.setFillColor(MUTED)
c.drawCentredString(W / 2, y_spec - 54, "H E L P F U L   V I D E O   G U I D E S   I N C L U D E D   ·   C L I C K A B L E   L I N K S   A N D   Q R   C O D E S   O N   P A G E   8")

c.setFont("Lora-Italic", 14.5)
c.setFillColor(BURGUNDY)
c.drawCentredString(W / 2, 72, "SewLuxePatterns")
c.showPage()

# =========================================================================
# PAGE 2: WELCOME / MEET THE COLETTE TROUSERS
# =========================================================================
draw_page_bg_and_chrome(c, 2)
y = draw_section_header(c, "W E L C O M E", "Meet the Colette Trousers")
intro = (
    "Thank you for choosing the Colette Trousers. Designed for **medium-weight woven suiting fabrics**, "
    "these high-waisted wide-leg trousers combine classic tailoring with relaxed, everyday comfort. "
    "Two soft front pleats on each side release smoothly from the straight waistband into a full-length wide leg, "
    "while back waist darts and single-welt pockets shape the seat cleanly."
)
y = draw_rich_paragraph(c, M_L, y, intro, CONTENT_W, font_size=9.5, leading=14.8)

# Left: Flat sketch, Right: Design features
y_sketch_top = y - 16
sketch_w = 248
sketch_h = 248
c.drawImage(FLAT_SKETCH, M_L, y_sketch_top - sketch_h, width=sketch_w, height=sketch_h, preserveAspectRatio=True, mask="auto")

rx = M_L + sketch_w + 18
rw = M_R - rx
ry = y_sketch_top - 10
c.setFont("Poppins-Medium", 10.5)
c.setFillColor(BURGUNDY)
c.drawString(rx, ry, "Design features")
ry -= 18
features = [
    "High-waisted, full-length wide-leg silhouette",
    "Double front pleats (two on each side) for effortless drape",
    "Slanted front side pockets anchored into the waist and side seams",
    "Tailored back waist darts and functional single-welt back pockets",
    "Classic front zipper fly with a 1-button straight waistband and fly shield",
    "No belt loops for a sleek, clean-lined waist",
    "3 cm (1 1/8 in) deep blind or machine-stitched hem",
]
for f in features:
    ry = draw_bullet(c, rx, ry, f, rw, font_size=9.1, leading=13.5)

y_inc = min(y_sketch_top - sketch_h - 24, ry - 18)
c.setFont("Poppins-Medium", 10.5)
c.setFillColor(BURGUNDY)
c.drawString(M_L, y_inc, "What is included")
y_inc -= 18
included = [
    "This 16-page illustrated sewing instruction booklet.",
    "Printable pattern files in A4 and US Letter (print at home) and A0 (copy shop), one file per size, sizes US 00 to 22 (XXS to 4XL).",
    "Helpful video guides for the key tailoring techniques, with clickable links and QR codes (page 8).",
]
for item in included:
    y_inc = draw_bullet(c, M_L, y_inc, item, CONTENT_W, font_size=9.3, leading=14.0)
c.showPage()

# =========================================================================
# PAGE 3: READ THIS FIRST / BEFORE YOU BEGIN
# =========================================================================
draw_page_bg_and_chrome(c, 3)
y = draw_section_header(c, "R E A D   T H I S   F I R S T", "Before You Begin")
c.setFont("Poppins", 9.5)
c.setFillColor(TEXT_BODY)
c.drawString(M_L, y, "Five minutes here saves hours later. Tick each point before you cut your fabric.")
y -= 24

checklist = [
    "**Print the test square first.** Print page 1 of your pattern file at 100% / Actual size (turn off \"Fit to page\"). Measure the square: it must be exactly 10 cm × 10 cm (4 in × 4 in).",
    "**Choose your size from your body waist and hip measurements (page 4),** not from your ready-to-wear size. The trousers have about 1.5 cm (5/8 in) of ease at the waist and 2.5 to 7 cm (1 to 2 3/4 in) of ease at the hips before the front pleats open. If you are between sizes at the waist and hips, grade smoothly between sizes along the side seam.",
    "**Check the length.** The pattern is drafted for a height of 168 cm (5 ft 6 in) with a finished inseam of 73 cm (28 3/4 in). To lengthen or shorten, adjust equally along the knee line on the Pants Front (1) and Pants Back (2).",
    "**Transfer every marking to the fabric with tailor's chalk or washable marker:** the front pleat lines, back waist darts, back welt pocket placement line, center front line, zipper stop circle, and all seam notches (clip notches no deeper than 3 mm / 1/8 in).",
    "**Allowances:** 1 cm (3/8 in) seam allowance is included on all construction seams, and 2 cm to 3 cm (3/4 in to 1 1/8 in) is included at the lower hem. All allowances are already built into the pattern pieces.",
    "**Test on a scrap of your suiting fabric:** check your stitch tension, press temperature with a pressing cloth, fusible interfacing bond, and the waistband buttonhole.",
    "**The two most rewarding tailoring steps are the back welt pockets (Step 3) and the zipper fly (Step 4).** Read both steps through once and baste before final stitching.",
]
for item in checklist:
    # Draw checkbox
    c.setStrokeColor(MUTED)
    c.setLineWidth(0.8)
    c.rect(M_L, y - 1, 8.5, 8.5, stroke=1, fill=0)
    y = draw_rich_paragraph(c, M_L + 18, y, item, CONTENT_W - 18, font_size=9.2, leading=14.0)
    y -= 8.0

y -= 4
draw_tip_box(
    c, y,
    "Pressing tailored trousers",
    "Press every pleat, dart, pocket, and seam as you go using steam and a pressing cloth (silk organza or plain cotton muslin) so you never leave shine marks on wool or twill suiting. Let each pressed area cool flat on the ironing board before moving the fabric."
)
c.showPage()

# =========================================================================
# PAGE 4: CHOOSE YOUR SIZE / SIZE CHARTS
# =========================================================================
draw_page_bg_and_chrome(c, 4)
y = draw_section_header(c, "C H O O S E   Y O U R   S I Z E", "Size Charts")
y = draw_rich_paragraph(
    c, M_L, y,
    "Measure over light underwear: waist at the natural narrowest crease and hips at the fullest part. Match your waist and hips to the chart below; if your hips fall in a larger size than your waist, blend between the two sizes between the waist and hip notches.",
    CONTENT_W, font_size=9.2, leading=13.8
)
y -= 10

# Body measurements table
c.setFont("Poppins-Medium", 10.5)
c.setFillColor(BURGUNDY)
c.drawString(M_L, y, "Body measurements")
y -= 10

body_rows = [
    ("00", "80", "63.5", "87.75", "31 1/2", "25", "34 1/2"),
    ("0",  "82.5", "66", "90.25", "32 1/2", "26", "35 1/2"),
    ("2",  "85", "68.75", "92.75", "33 1/2", "27 1/8", "36 1/2"),
    ("4",  "87.75", "71.25", "95.25", "34 1/2", "28", "37 1/2"),
    ("6",  "90.25", "73.75", "98", "35 1/2", "29", "38 5/8"),
    ("8",  "92.75", "76.25", "100.25", "36 1/2", "30", "39 1/2"),
    ("10", "95.25", "78.75", "102.75", "37 1/2", "31", "40 1/2"),
    ("12", "99.25", "82.75", "106.5", "39 1/8", "32 5/8", "41 7/8"),
    ("14", "104.25", "87.5", "111", "41", "34 1/2", "43 3/4"),
    ("16", "109.25", "93.25", "115.5", "43", "36 3/4", "45 1/2"),
    ("18", "114.25", "99", "120.75", "45", "39", "47 1/2"),
    ("20", "119.25", "104.75", "125.75", "47", "41 1/4", "49 1/2"),
    ("22", "124.25", "110.5", "130.75", "48 7/8", "43 1/2", "51 1/2"),
]
col_x_body = [M_L + 6, M_L + 78, M_L + 148, M_L + 220, M_L + 292, M_L + 362, M_L + 434]
row_h = 15.2
c.setFillColor(TABLE_HEAD)
c.rect(M_L, y - row_h, CONTENT_W, row_h, stroke=0, fill=1)
c.setFont("Poppins-Medium", 7.5)
c.setFillColor(WHITE)
for cx_b, h_txt in zip(col_x_body, ["US SIZE", "BUST cm", "WAIST cm", "HIPS cm", "BUST in", "WAIST in", "HIPS in"]):
    c.drawString(cx_b, y - 10.5, h_txt)
y -= row_h

for idx, r in enumerate(body_rows):
    if idx % 2 == 1:
        c.setFillColor(TABLE_ALT)
        c.rect(M_L, y - row_h, CONTENT_W, row_h, stroke=0, fill=1)
    c.setStrokeColor(RULE_LINE)
    c.setLineWidth(0.4)
    c.line(M_L, y - row_h, M_R, y - row_h)
    c.setFont("Poppins", 7.8)
    c.setFillColor(CHARCOAL)
    for cx_b, val in zip(col_x_body, r):
        c.drawString(cx_b, y - 10.5, val)
    y -= row_h

# Letter size strip
y -= 8
c.setFillColor(TABLE_HEAD)
c.rect(M_L, y - 14, CONTENT_W, 14, stroke=0, fill=1)
c.setFillColor(TABLE_ALT)
c.rect(M_L, y - 28, CONTENT_W, 14, stroke=0, fill=1)
c.setFont("Poppins-Medium", 7.2)
c.setFillColor(WHITE)
c.drawString(M_L + 6, y - 9.8, "US SIZE")
c.setFont("Poppins", 7.2)
c.setFillColor(CHARCOAL)
c.drawString(M_L + 6, y - 23.8, "LETTER")
us_szs = ["00", "0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22"]
let_szs = ["XXS", "XS", "XS", "S", "S", "M", "M", "L", "L", "XL", "2XL", "3XL", "4XL"]
for i, (u_s, l_s) in enumerate(zip(us_szs, let_szs)):
    sx = M_L + 65 + i * 33.0
    c.setFont("Poppins-Medium", 7.2)
    c.setFillColor(WHITE)
    c.drawCentredString(sx, y - 9.8, u_s)
    c.setFont("Poppins", 7.2)
    c.setFillColor(CHARCOAL)
    c.drawCentredString(sx, y - 23.8, l_s)
y -= 42

# Finished garment measurements table
c.setFont("Poppins-Medium", 10.5)
c.setFillColor(BURGUNDY)
c.drawString(M_L, y, "Finished garment measurements")
y -= 10

col_x_fin = [M_L + 6, M_L + 52, M_L + 165, M_L + 278, M_L + 388]
c.setFillColor(TABLE_HEAD)
c.rect(M_L, y - row_h, CONTENT_W, row_h, stroke=0, fill=1)
c.setFont("Poppins-Medium", 7.5)
c.setFillColor(WHITE)
for cx_f, h_txt in zip(col_x_fin, ["US SIZE", "FINISHED WAIST*", "FINISHED HIPS*", "LEG OPENING (CIRC.)", "INSEAM / OUTSEAM"]):
    c.drawString(cx_f, y - 10.5, h_txt)
y -= row_h

def cm_to_in_frac(cm_val: float) -> str:
    inches = cm_val / 2.54
    whole = int(inches)
    eighths = round((inches - whole) * 8)
    if eighths == 8:
        whole += 1
        eighths = 0
    frac_map = {0: "", 1: " 1/8", 2: " 1/4", 3: " 3/8", 4: " 1/2", 5: " 5/8", 6: " 3/4", 7: " 7/8"}
    return f"{whole}{frac_map[eighths]} in"

for idx, entry in enumerate(size_data):
    sz = entry["size"]
    sp = entry["specs"]
    # Waist & Hips & Bottom opening in PatternFast specs are half-circumferences
    w_cm = sp["Waist"]["val"] * 2.0
    h_cm = sp["Hips"]["val"] * 2.0
    leg_cm = sp["Bottom opening"]["val"] * 2.0
    ins_cm = sp["Inseam length"]["val"]
    out_cm = sp["Pants side seam length"]["val"]
    row_vals = [
        sz,
        f"{w_cm:.1f} cm / {cm_to_in_frac(w_cm)}",
        f"{h_cm:.1f} cm / {cm_to_in_frac(h_cm)}",
        f"{leg_cm:.1f} cm / {cm_to_in_frac(leg_cm)}",
        f"{ins_cm:.0f} cm ({sp['Inseam length']['in_str']}) / {out_cm:.0f} cm",
    ]
    if idx % 2 == 1:
        c.setFillColor(TABLE_ALT)
        c.rect(M_L, y - row_h, CONTENT_W, row_h, stroke=0, fill=1)
    c.setStrokeColor(RULE_LINE)
    c.setLineWidth(0.4)
    c.line(M_L, y - row_h, M_R, y - row_h)
    c.setFont("Poppins", 7.6)
    c.setFillColor(CHARCOAL)
    for cx_f, val in zip(col_x_fin, row_vals):
        c.drawString(cx_f, y - 10.5, val)
    y -= row_h

draw_rich_paragraph(
    c, M_L, y - 10,
    "* Finished waist and hips are full circumferences measured with the front pleats closed. The four front pleats add extra fullness across the front hip. Finished waistband height is 3 cm (1 1/8 in) across all sizes.",
    CONTENT_W, font_size=7.0, leading=10.5, color=MUTED
)
c.showPage()

# =========================================================================
# PAGE 5: MATERIALS / FABRIC & NOTIONS
# =========================================================================
draw_page_bg_and_chrome(c, 5)
y = draw_section_header(c, "M A T E R I A L S", "Fabric & Notions")

c.setFont("Poppins-Medium", 10.5)
c.setFillColor(BURGUNDY)
c.drawString(M_L, y, "Suggested fabrics")
y -= 16
fab_text = (
    "Medium-weight woven suiting fabrics with a soft, fluid drape (180–280 gsm / 5.3–8.2 oz): "
    "brushed wool-linen twill, wool gabardine, wool crepe, heavy linen or linen-viscose suiting, Tencel/lyocell twill, "
    "cotton-linen cavalry twill, or fine-wale needlecord. Avoid stiff canvas or high-stretch knits. "
    "For the pocket bags (Pieces 6 and 9), use a lightweight cotton lawn, poplin, or Bemberg lining so the pockets lie flat without bulk."
)
y = draw_rich_paragraph(c, M_L, y, fab_text, CONTENT_W, font_size=9.3, leading=14.2)
y -= 10

c.setFont("Poppins-Medium", 10.5)
c.setFillColor(BURGUNDY)
c.drawString(M_L, y, "Fabric requirements (main fabric)")
y -= 10

fab_rows = [
    ("00 – 6",  "1.8 m / 2 yd",     "00 – 6",  "2.3 m / 2 1/2 yd"),
    ("8 – 14",  "2.1 m / 2 3/8 yd", "8 – 14",  "2.6 m / 2 7/8 yd"),
    ("16 – 22", "2.4 m / 2 5/8 yd", "16 – 22", "2.9 m / 3 1/4 yd"),
]
col_x_fab = [M_L + 8, M_L + 95, M_L + 260, M_L + 350]
row_h_fab = 18.0
c.setFillColor(TABLE_HEAD)
c.rect(M_L, y - row_h_fab, CONTENT_W, row_h_fab, stroke=0, fill=1)
c.setFont("Poppins-Medium", 7.8)
c.setFillColor(WHITE)
for cx_fb, h_txt in zip(col_x_fab, ["US SIZES", "150 cm / 60 in wide", "US SIZES", "115 cm / 45 in wide"]):
    c.drawString(cx_fb, y - 12, h_txt)
y -= row_h_fab
for idx, r in enumerate(fab_rows):
    if idx % 2 == 1:
        c.setFillColor(TABLE_ALT)
        c.rect(M_L, y - row_h_fab, CONTENT_W, row_h_fab, stroke=0, fill=1)
    c.setStrokeColor(RULE_LINE)
    c.setLineWidth(0.4)
    c.line(M_L, y - row_h_fab, M_R, y - row_h_fab)
    c.setFont("Poppins", 8.2)
    c.setFillColor(CHARCOAL)
    for cx_fb, val in zip(col_x_fab, r):
        c.drawString(cx_fb, y - 12, val)
    y -= row_h_fab

c.setFont("Poppins", 7.2)
c.setFillColor(MUTED)
c.drawString(M_L, y - 11, "Plain fabric without nap or one-way design. Add 15–20% extra for plaid matching or directional pile fabrics.")
c.drawString(M_L, y - 21, "Pre-wash or steam-shrink your main fabric and pocket lining before cutting.")
y -= 40

c.setFont("Poppins-Medium", 10.5)
c.setFillColor(BURGUNDY)
c.drawString(M_L, y, "Notions")
y -= 16
notions = [
    "**Zipper:** 1 nylon trouser zipper, 20 to 23 cm (8 to 9 in) long (can be shortened to fit the 18 cm / 7 1/8 in fly opening in Step 4).",
    "**Button:** 1 trouser button, 10 to 12 mm (3/8 to 1/2 in) in diameter, for the front waistband overlap.",
    "**Lining fabric (for pockets):** 0.5 m / 5/8 yd of lightweight cotton poplin or lining fabric, 115–150 cm (45–60 in) wide (Pieces 6 and 9).",
    "**Fusible interfacing:** 0.5 m / 5/8 yd of lightweight woven fusible interfacing, 90 cm (36 in) wide (for Waistband 3, Fly Interfacing 7, and Back Pocket Welt 8).",
    "Matching all-purpose polyester or silk-finish thread, zipper foot, buttonhole foot, hand-sewing needle, tailor's chalk, and pressing cloth.",
]
for n in notions:
    y = draw_bullet(c, M_L, y, n, CONTENT_W, font_size=9.1, leading=13.8)

y -= 8
c.setFont("Poppins-Medium", 10.5)
c.setFillColor(BURGUNDY)
c.drawString(M_L, y, "Printing and assembling the pattern")
y -= 16
printing = [
    "Download the ZIP folder for your print format (A4, US Letter or A0) and unzip it. Each size is a separate PDF: open the file for your size in Adobe Acrobat Reader (not in a browser preview).",
    "Print page 1 at 100% / Actual size and check the 10 cm × 10 cm (4 in × 4 in) test square before printing the rest.",
    "A4 / US Letter: each tile has a dashed border and a grid number such as 1/1, 1/2. Pages with the same first number form one horizontal row. Trim the right and bottom margins along the dashed lines, overlap matching triangles, and tape rows together.",
    "A0: send the single-size A0 file to a copy shop and request printing at 100% scale.",
]
for p_item in printing:
    y = draw_bullet(c, M_L, y, p_item, CONTENT_W, font_size=9.1, leading=13.8)
c.showPage()

# =========================================================================
# PAGE 6: CUTTING / PATTERN PIECES & CUTTING
# =========================================================================
draw_page_bg_and_chrome(c, 6)
y = draw_section_header(c, "C U T T I N G", "Pattern Pieces & Cutting")

pieces_table = [
    ("1",  "Pants Front",            "Main fabric",                        "2 (a mirrored pair)"),
    ("2",  "Pants Back",             "Main fabric",                        "2 (a mirrored pair)"),
    ("3",  "Waistband",              "Main fabric + fusible interfacing",  "1 + 1 interfacing"),
    ("4",  "Pocket Bag (Outer/Facing)", "Main fabric",                     "2 (a mirrored pair)"),
    ("5",  "Fly Facing (Fly Shield)", "Main fabric + fusible interfacing", "1 + 1 interfacing"),
    ("6",  "Pocket Lining (Front)",  "Lining fabric",                      "2 (a mirrored pair)"),
    ("7",  "Fly Interfacing",        "Fusible interfacing",                "2 (left & right fly)"),
    ("8",  "Back Pocket Welt",       "Main fabric + fusible interfacing",  "2 + 2 interfacing"),
    ("9",  "Back Inner Pocket Bag",  "Lining fabric",                      "2 (a mirrored pair)"),
    ("10", "Back Outer Pocket Bag",  "Main fabric",                        "2 (a mirrored pair)"),
]
col_x_pc = [M_L + 8, M_L + 36, M_L + 188, M_L + 365]
row_h_pc = 16.5
c.setFillColor(TABLE_HEAD)
c.rect(M_L, y - row_h_pc, CONTENT_W, row_h_pc, stroke=0, fill=1)
c.setFont("Poppins-Medium", 7.6)
c.setFillColor(WHITE)
for cx_p, h_txt in zip(col_x_pc, ["#", "PIECE", "CUT FROM", "CUT"]):
    c.drawString(cx_p, y - 11.2, h_txt)
y -= row_h_pc
for idx, r in enumerate(pieces_table):
    if idx % 2 == 1:
        c.setFillColor(TABLE_ALT)
        c.rect(M_L, y - row_h_pc, CONTENT_W, row_h_pc, stroke=0, fill=1)
    c.setStrokeColor(RULE_LINE)
    c.setLineWidth(0.4)
    c.line(M_L, y - row_h_pc, M_R, y - row_h_pc)
    c.setFont("Poppins", 8.0)
    c.setFillColor(CHARCOAL)
    for cx_p, val in zip(col_x_pc, r):
        c.drawString(cx_p, y - 11.2, val)
    y -= row_h_pc

y -= 18
c.setFont("Poppins-Medium", 10.5)
c.setFillColor(BURGUNDY)
c.drawString(M_L, y, "Cutting tips")
y -= 16
cut_tips = [
    "Fold the fabric right sides together, selvages parallel, and align the long grainline arrow on every pattern piece parallel to the selvage.",
    "Every pattern piece is drafted as a full flat piece (no pieces are placed on a fold). For \"2 (a mirrored pair)\", cut through two layers of fabric placed right sides together so you get a left and a right piece.",
    "**Right Pants Front (1):** notice the note \"CUT ON LEFT FRONT\" along the fly extension on Piece 1. Cut both Pants Fronts with the fly extension first; when preparing the zipper fly in Step 4, you will trim the excess extension on the right side along the zipper tape.",
    "Fuse the lightweight interfacing to the wrong side of the Waistband (3), Fly Facing (5), Back Pocket Welts (8), and the two front fly extensions using Fly Interfacing (7) before you start sewing.",
    "Reinforce the wrong side of the Back Welt Pocket placement line on each Pants Back (2) with a 4 cm × 16 cm (1 1/2 in × 6 1/4 in) strip of fusible interfacing so the slashed corners stay crisp.",
]
for ct in cut_tips:
    y = draw_bullet(c, M_L, y, ct, CONTENT_W, font_size=8.9, leading=13.2)

y -= 10
c.setFont("Poppins-Medium", 10.5)
c.setFillColor(BURGUNDY)
c.drawString(M_L, y, "Sewing order at a glance")
y -= 10

# 4x3 grid (9 steps across 3 rows of 4 cols, matching Odette Vest Page 6)
order_cells = [
    [("1 ", "Front pleats & darts"), ("2 ", "Slanted front pockets"), ("3 ", "Back welt pockets"), ("4 ", "Zipper fly & shield")],
    [("5 ", "Inseams & crotch seam"), ("6 ", "Side seams"), ("7 ", "Waistband & button"), ("8 ", "Hem the trousers")],
    [("9 ", "Finishing"), ("", ""), ("", ""), ("", "")],
]
cell_w = (CONTENT_W - 6) / 4.0
cell_h = 28.0
for r_idx, row_cells in enumerate(order_cells):
    ry_top = y - r_idx * (cell_h + 2)
    for c_idx, (num_str, lbl_str) in enumerate(row_cells):
        cx_box = M_L + c_idx * (cell_w + 2)
        c.setFillColor(GRID_BG)
        c.rect(cx_box, ry_top - cell_h, cell_w, cell_h, stroke=0, fill=1)
        if num_str:
            c.setFont("Poppins-Medium", 8.2)
            c.setFillColor(BURGUNDY)
            c.drawString(cx_box + 8, ry_top - 17, num_str)
            nw = pdfmetrics.stringWidth(num_str, "Poppins-Medium", 8.2)
            c.setFont("Poppins", 8.0)
            c.setFillColor(CHARCOAL)
            c.drawString(cx_box + 8 + nw, ry_top - 17, lbl_str)

y_after_grid = y - 3 * (cell_h + 2) - 8
draw_rich_paragraph(
    c, M_L, y_after_grid,
    "Stitch all seams with a 1 cm (3/8 in) seam allowance, right sides together, unless stated otherwise. Finish raw edges with an overlocker or zigzag stitch.",
    CONTENT_W, font_size=7.3, leading=10.5, color=MUTED
)
c.showPage()

# =========================================================================
# PAGE 7: YOUR PATTERN / PIECES & MARKINGS
# =========================================================================
draw_page_bg_and_chrome(c, 7)
y = draw_section_header(c, "Y O U R   P A T T E R N", "Pieces & Markings")
y = draw_rich_paragraph(
    c, M_L, y,
    "The pattern pieces as they appear on your pattern sheet (size 12 shown). The solid outer line is the cutting line; the inner dashed line is the 1 cm (3/8 in) stitching line.",
    CONTENT_W, font_size=9.3, leading=14.0
)

# Draw pieces_overview_clean.png
diag_h = 295
diag_w = diag_h * (2324.0 / 1792.0)
c.drawImage(pieces_png, M_L - 6, y - diag_h - 4, width=diag_w, height=diag_h, preserveAspectRatio=True, mask="auto")

# Compact legend of piece numbers on the right of the diagram
leg_x = M_L + diag_w + 2
leg_y = y - 20
c.setFont("Poppins-Medium", 8.2)
c.setFillColor(BURGUNDY)
c.drawString(leg_x, leg_y, "Pattern pieces key")
leg_y -= 14.5
piece_names = [
    ("1", "Pants Front"),
    ("2", "Pants Back"),
    ("3", "Waistband"),
    ("4", "Pocket Bag (Front)"),
    ("5", "Fly Facing (Shield)"),
    ("6", "Pocket Lining (Front)"),
    ("7", "Fly Interfacing"),
    ("8", "Back Pocket Welt"),
    ("9", "Back Inner Pocket Bag"),
    ("10", "Back Outer Pocket Bag"),
]
for pnum, pname in piece_names:
    c.setFont("Poppins-Medium", 7.6)
    c.setFillColor(BURGUNDY)
    c.drawString(leg_x, leg_y, pnum)
    c.setFont("Poppins", 7.4)
    c.setFillColor(TEXT_BODY)
    c.drawString(leg_x + 13, leg_y, pname)
    leg_y -= 14.0

y = y - diag_h - 20
c.setFont("Poppins-Medium", 10.5)
c.setFillColor(BURGUNDY)
c.drawString(M_L, y, "What the markings mean")
y -= 16
markings = [
    "**Notches:** small triangles along the seam lines. Match them to the notches on the adjoining piece at the waist, hip, knee, and pocket opening.",
    "**Front pleats (1):** two pairs of vertical lines with directional arrows at the upper waist of the Pants Front (1). Fold along the line and bring it to meet the partner line in the direction of the arrow.",
    "**Back waist dart (2) & Back welt pocket (2):** the V-shaped dart folds to a point above the horizontal welt pocket line (12 cm / 4 3/4 in wide, 2.5 cm / 1 in tall).",
    "**Center front & Fly extension (1):** the curved extension at the top of the front rise forms the zipper fly; the small circle near the base of the fly marks the zipper stop.",
    "**Waistband button & buttonhole (3):** the circle with a cross marks the 10 mm (3/8 in) button; the horizontal bar marks the buttonhole.",
    "**Hemline (1, 2):** the horizontal line near the bottom of each leg marks the finished hem fold.",
    "**Grainline:** the long straight arrow on every piece must run parallel to the fabric selvage.",
]
for mk in markings:
    y = draw_bullet(c, M_L, y, mk, CONTENT_W, font_size=8.8, leading=13.0)
c.showPage()

# =========================================================================
# PAGE 8: EXTRA HELP / HELPFUL VIDEO GUIDES
# =========================================================================
draw_page_bg_and_chrome(c, 8)
y = draw_section_header(c, "E X T R A   H E L P", "Helpful Video Guides")
y = draw_rich_paragraph(
    c, M_L, y,
    "Short video tutorials for the key tailoring techniques used in these trousers. Click a link, or scan the QR code with your phone camera.",
    CONTENT_W, font_size=9.5, leading=14.2
)
y -= 28

videos = [
    ("Sewing front pleats & darts", "Used in Step 1", "https://www.youtube.com/results?search_query=how+to+sew+front+pleats+and+darts+on+trousers"),
    ("Slanted front trouser pockets", "Used in Step 2", "https://www.youtube.com/results?search_query=how+to+sew+slanted+side+pockets+on+trousers"),
    ("Single-welt back pockets", "Used in Step 3", "https://www.youtube.com/results?search_query=how+to+sew+single+welt+pocket+on+trousers"),
    ("Trouser zipper fly & waistband", "Used in Steps 4 and 7", "https://www.youtube.com/results?search_query=how+to+sew+a+trouser+zipper+fly+and+waistband"),
]

qr_positions = [
    (M_L + 8, y - 92),
    (M_L + 260, y - 92),
    (M_L + 8, y - 230),
    (M_L + 260, y - 230),
]
for idx, ((vtitle, vstep, vurl), (qx, qy)) in enumerate(zip(videos, qr_positions)):
    qrw = qr.QrCodeWidget(vurl)
    bounds = qrw.getBounds()
    bw_qr = bounds[2] - bounds[0]
    bh_qr = bounds[3] - bounds[1]
    qr_size = 86.0
    d = Drawing(qr_size, qr_size, transform=[qr_size / bw_qr, 0, 0, qr_size / bh_qr, 0, 0])
    qrw.barFillColor = CHARCOAL
    d.add(qrw)
    renderPDF.draw(d, c, qx, qy)

    tx = qx + qr_size + 16
    ty = qy + qr_size - 16
    c.setFont("Poppins-Medium", 10.0)
    c.setFillColor(CHARCOAL)
    c.drawString(tx, ty, vtitle)
    c.setFont("Poppins", 8.2)
    c.setFillColor(MUTED)
    c.drawString(tx, ty - 16, vstep)
    c.setFont("Poppins", 8.5)
    c.setFillColor(BURGUNDY)
    link_txt = "Watch the video"
    c.drawString(tx, ty - 32, link_txt)
    lw = pdfmetrics.stringWidth(link_txt, "Poppins", 8.5)
    c.setStrokeColor(BURGUNDY)
    c.setLineWidth(0.6)
    c.line(tx, ty - 33.5, tx + lw, ty - 33.5)
    c.linkURL(vurl, (tx, ty - 36, tx + lw, ty - 22), relative=0)

c.setStrokeColor(RULE_LINE)
c.setLineWidth(0.5)
c.line(M_L, y - 118, M_R, y - 118)

c.setFont("Poppins", 7.8)
c.setFillColor(MUTED)
c.drawString(M_L, y - 270, "Videos are made by independent creators and may use slightly different seam allowances. Always follow the measurements in this")
c.drawString(M_L, y - 282, "guide for the Colette Trousers.")
c.showPage()

# =========================================================================
# PAGE 9: LET'S SEW / STEP 1: FRONT PLEATS & BACK DARTS
# =========================================================================
draw_page_bg_and_chrome(c, 9)
y = draw_section_header(c, "L E T ' S   S E W", "Sewing Instructions")
y -= 4
y = draw_step_header(c, y, 1, "Sew the front pleats and back darts", "Pieces 1 and 2 · pictures 1–2")

step1_bullets = [
    "**Front pleats:** on the right side of each Pants Front (1), fold each of the two waist pleats along the solid pleat line and bring the fold to meet the partner line in the direction of the printed arrow (toward the side seam). Pin and machine-baste across the upper waist edge 6 mm (1/4 in) from the raw edge to hold both pleats in place (picture 1).",
    "**Back waist darts:** on the wrong side of each Pants Back (2), fold the waist dart right sides together along the center line, matching the waist notches. Stitch from the waist edge down to a smooth point at the dart tip, leaving long thread tails and tying a double knot at the point instead of backstitching (picture 2).",
    "Press the front pleats lightly near the waist (do not press a hard crease down the leg) and press the back waist darts toward the center back.",
    "Video help: **Sewing front pleats & darts** (QR code on page 8).",
]
for b in step1_bullets:
    y = draw_bullet(c, M_L, y, b, CONTENT_W)

y -= 6
img1_path = os.path.join(ASSET_DIR, "step1_panels.png")
img1_h = CONTENT_W * (1050.0 / 2200.0)
c.drawImage(img1_path, M_L, y - img1_h, width=CONTENT_W, height=img1_h, preserveAspectRatio=True, mask="auto")
y = y - img1_h - 14

draw_tip_box(
    c, y,
    "Beginner tip",
    "When sewing the back waist darts, let the last 3–4 stitches skim the very edge of the fold before running off the tip. Tying the thread tails by hand prevents a dimple or pucker at the point of the dart."
)
c.showPage()

# =========================================================================
# PAGE 10: STEP 2: SLANTED FRONT POCKETS
# =========================================================================
draw_page_bg_and_chrome(c, 10)
y = draw_step_header(c, H - 78, 2, "Sew the slanted front pockets", "Pieces 1, 4 and 6 · pictures 1–5")

step2_bullets = [
    "Place one **Pocket Lining (6)** onto the slanted pocket edge of the corresponding **Pants Front (1)**, right sides together, matching the notches. Stitch along the slanted pocket opening line at 1 cm (3/8 in) (picture 1).",
    "Trim the seam allowance to 5 mm (3/16 in), press the Pocket Lining and seam allowance away from the garment, and **understitch** on the Pocket Lining 2 mm (1/16 in) from the seamline so the lining rolls slightly to the inside (picture 2).",
    "Turn the Pocket Lining to the wrong side of the Pants Front along the slanted fold, press the pocket edge crisp, and topstitch 6 mm (1/4 in) from the slanted edge (picture 3).",
    "Place the **Pocket Bag (4)** right sides together against the Pocket Lining (6), matching the curved lower edge and the waist/side edges. Stitch around the curved bottom of the pocket bag at 1 cm (3/8 in) and finish the raw seam with an overlocker or zigzag stitch (picture 4).",
    "Align the outer waist and side edges of the completed pocket with the waist and side seam of the Pants Front (1), and baste in place within the 1 cm (3/8 in) seam allowance (picture 5). Repeat for the second front leg.",
]
for b in step2_bullets:
    y = draw_bullet(c, M_L, y, b, CONTENT_W, font_size=9.0, leading=13.4)

y -= 4
img2_path = os.path.join(ASSET_DIR, "step2_panels.png")
img2_h = CONTENT_W * (2320.0 / 3378.0)
c.drawImage(img2_path, M_L, y - img2_h, width=CONTENT_W, height=img2_h, preserveAspectRatio=True, mask="auto")
y = y - img2_h - 12

draw_tip_box(
    c, y,
    "Beginner tip",
    "Understitching in picture 2 is the secret to a professional slanted pocket that never gapes or shows the lining from the outside. Baste the top and side of the pocket flat before moving to the next step."
)
c.showPage()

# =========================================================================
# PAGE 11: STEP 3: BACK SINGLE-WELT POCKETS
# =========================================================================
draw_page_bg_and_chrome(c, 11)
y = draw_step_header(c, H - 78, 3, "Sew the back single-welt pockets", "Pieces 2, 8, 9 and 10 · pictures 1–9")

step3_bullets = [
    "Transfer the horizontal welt pocket marking (12 cm / 4 3/4 in long) below the dart on each **Pants Back (2)**. Fuse interfacing to the wrong side of each **Back Pocket Welt (8)**, fold it lengthwise wrong sides together, and press (pictures 1–2).",
    "Pin and baste the folded Welt (8) onto the right side of the Pants Back (2) with its raw edge aligned along the lower pocket line (picture 3).",
    "Pin the **Back Inner Pocket Bag (9)** over the welt and the **Back Outer Pocket Bag (10)** along the upper line, right sides together with the garment. Stitch two parallel lines 12 cm (4 3/4 in) long and 1.2 cm (1/2 in) apart, backstitching securely at all four ends (pictures 4–5).",
    "Slash straight between the two stitching lines from the center, stopping 1 cm (3/8 in) from each end, and clip diagonally into all four corners right up to—but not through—the last stitch (picture 6).",
    "Pull both pocket bags through the opening to the wrong side, push the welt up to fill the rectangular frame, and press neatly (picture 7).",
    "On the wrong side, fold the garment away and stitch across the small triangular ends at each side of the welt to lock the corners, then stitch around the curved edges of the two pocket bags together and finish the raw edge (picture 8). Edgestitch the short ends of the welt from the right side if desired (picture 9).",
]
for b in step3_bullets:
    y = draw_bullet(c, M_L, y, b, CONTENT_W, font_size=8.6, leading=12.4)

y -= 2
img3_path = os.path.join(ASSET_DIR, "step3_panels.png")
# Fit cleanly above footer
avail_h = y - 62
img3_w_fit = avail_h * (3483.0 / 4517.0)
if img3_w_fit > CONTENT_W:
    img3_w_fit = CONTENT_W
    avail_h = CONTENT_W * (4517.0 / 3483.0)
c.drawImage(img3_path, M_L + (CONTENT_W - img3_w_fit) / 2, y - avail_h, width=img3_w_fit, height=avail_h, preserveAspectRatio=True, mask="auto")
c.showPage()

# =========================================================================
# PAGE 12: STEP 4: ZIPPER FLY & FLY SHIELD
# =========================================================================
draw_page_bg_and_chrome(c, 12)
y = draw_step_header(c, H - 78, 4, "Install the zipper fly and fly shield", "Pieces 1, 5 and 7 · pictures 1–8")

step4_bullets = [
    "Fuse **Fly Interfacing (7)** to the wrong side of both front fly extensions. If your zipper is longer than the fly opening, whipstitch across the teeth 2 cm (3/4 in) below the circle marking and trim the excess bottom (first panel).",
    "Place the two **Pants Fronts (1)** right sides together. Stitch the center front seam from 2.5 cm (1 in) above the inseam up to the circle marking, backstitching at the circle, then **machine-baste** from the circle up to the waist edge. Clip the right fly allowance just below the circle and press the center front seam open (pictures 1–2.1).",
    "Fold the right fly extension in half wrong sides together and press. Place the closed zipper face up under the folded right edge, teeth close to the fold, and stitch along the fold with a zipper foot (picture 3).",
    "Turn the Pants Fronts right side up, fold the left fly extension out flat, and topstitch 3 mm (1/8 in) to the left of the zipper teeth (picture 4). Flip the zipper and right extension onto the left fly extension on the wrong side and stitch the loose left zipper tape to the left fly extension ONLY—do not catch the front of the trousers (picture 5).",
    "On the right side of the trousers, pin through the left fly extension, remove the center front basting stitches, and topstitch the curved **J-stitch** along the left front fly line down to the circle (picture 6).",
    "Fold the **Fly Facing / Shield (5)** lengthwise wrong sides together, finish its raw edges, pin it behind the right zipper tape on the inside so it covers the zipper teeth, stitch along the right extension seam, and add a short bar tack at the base of the J-stitch catching all layers (pictures 7–8).",
]
for b in step4_bullets:
    y = draw_bullet(c, M_L, y, b, CONTENT_W, font_size=8.6, leading=12.4)

y -= 4
img4_path = os.path.join(ASSET_DIR, "step4_panels.png")
img4_h = CONTENT_W * (3534.0 / 4534.0)
if y - img4_h < 60:
    img4_h = y - 60
    img4_w = img4_h * (4534.0 / 3534.0)
else:
    img4_w = CONTENT_W
c.drawImage(img4_path, M_L + (CONTENT_W - img4_w) / 2, y - img4_h, width=img4_w, height=img4_h, preserveAspectRatio=True, mask="auto")
c.showPage()

# =========================================================================
# PAGE 13: STEP 5: INSEAMS & CROTCH SEAM
# =========================================================================
draw_page_bg_and_chrome(c, 13)
y = draw_step_header(c, H - 78, 5, "Sew the inseams and crotch seam", "Pieces 1 and 2 · pictures 1–2")

step5_bullets = [
    "**Inseams:** place each **Pants Back (2)** onto its matching **Pants Front (1)**, right sides together, aligning the inner leg edges from the crotch point down to the ankle hem and matching the knee notches (picture 1).",
    "Pin and stitch both inseams at 1 cm (3/8 in) from the crotch down to the hem. Finish the raw seam allowances separately and press the inseams open.",
    "**Crotch seam:** turn one trouser leg right side out and slip it inside the other leg so the two legs are **right sides together** along the curved crotch seam. Match the center front seam, the inseam junction, and the back rise notches (picture 2).",
    "Stitch the remaining lower front rise (from 2.5 cm / 1 in above the inseam, overlapping the end of your Step 4 stitching) continuously around the crotch curve and up the center back rise to the waist edge.",
    "**Reinforce the curve:** stitch a second line of smaller stitches (2.0 mm) directly on top of the first line through the lower crotch curve for durability. Trim the curved seam allowances slightly, finish the raw edges together, and press the crotch seam open toward the top.",
]
for b in step5_bullets:
    y = draw_bullet(c, M_L, y, b, CONTENT_W, font_size=9.2, leading=14.0)

y -= 10
img5_path = os.path.join(ASSET_DIR, "step5_panels.png")
img5_h = CONTENT_W * (1050.0 / 2200.0)
c.drawImage(img5_path, M_L, y - img5_h, width=CONTENT_W, height=img5_h, preserveAspectRatio=True, mask="auto")
y = y - img5_h - 16

draw_tip_box(
    c, y,
    "Beginner tip",
    "When sewing the crotch curve in picture 2, open the inseam allowances flat at the four-way junction and pin right in the ditch of the inseam so the front and back leg seams meet in a clean cross."
)
c.showPage()

# =========================================================================
# PAGE 14: STEP 6: SIDE SEAMS
# =========================================================================
draw_page_bg_and_chrome(c, 14)
y = draw_step_header(c, H - 78, 6, "Sew the side seams", "Pieces 1 and 2 · picture 1")

step6_bullets = [
    "Turn both trouser legs wrong side out. Pin the outer side edges of the **Pants Front (1)** and **Pants Back (2)** right sides together from the waist down to the ankle hem, matching the hip and knee notches (picture 1).",
    "Along the upper hip, make sure you pin through the outer side edge of the Pocket Bag (4) and Pocket Lining (6) that you basted in Step 2, while keeping the slanted front pocket opening free.",
    "Stitch both side seams from the waist down to the hem at a 1 cm (3/8 in) seam allowance.",
    "Finish the raw edges of each side seam allowance separately with an overlocker or zigzag stitch. Press the side seams open from the hem up to the base of the pocket bag, and press the upper pocket section toward the front.",
    "**Fit check:** baste or pin the waist closed and try the trousers on before attaching the waistband. You can easily fine-tune the waist or hip fit along the two side seams or the center back seam now.",
]
for b in step6_bullets:
    y = draw_bullet(c, M_L, y, b, CONTENT_W, font_size=9.2, leading=14.0)

y -= 12
img6_path = os.path.join(ASSET_DIR, "step6_panels.png")
# step6_panels.png is 1568 x 960
img6_w = CONTENT_W * 0.76
img6_h = img6_w * (960.0 / 1568.0)
c.drawImage(img6_path, M_L + (CONTENT_W - img6_w) / 2, y - img6_h, width=img6_w, height=img6_h, preserveAspectRatio=True, mask="auto")
y = y - img6_h - 18

draw_tip_box(
    c, y,
    "Beginner tip",
    "At the bottom of the slanted pocket opening (hip notch), sew a tiny 6 mm (1/4 in) horizontal bar tack or a few backstitches right at the lower corner of the pocket opening from the right side to prevent the pocket from pulling under stress."
)
c.showPage()

# =========================================================================
# PAGE 15: STEP 7: WAISTBAND & BUTTON + STEP 8: HEM THE TROUSERS
# =========================================================================
draw_page_bg_and_chrome(c, 15)
y = draw_step_header(c, H - 78, 7, "Attach the waistband and button", "Piece 3 · pictures 1–5")

step7_bullets = [
    "Press the upper long seam allowance (1 cm / 3/8 in) of the interfaced **Waistband (3)** to the wrong side and trim it slightly so it lies flat (picture 1).",
    "Pin the unpressed lower edge of the Waistband right sides together to the upper waist edge of the trousers, matching the center back, side seam, and front notches. Stitch at 1 cm (3/8 in), trim/grade the seam allowance, and press the seam allowances up into the waistband (picture 2).",
    "Fold the Waistband lengthwise along the center foldline, **right sides together**, and stitch across both short front ends at the fly overlap and underlap. Trim the corners and turn the waistband right side out (picture 3).",
    "Pin the pressed inner edge of the waistband over the waist seam on the inside of the trousers. Slipstitch by hand or stitch-in-the-ditch from the right side, then edgestitch around the waistband if desired (picture 4).",
    "Work a horizontal buttonhole on the overlapping left end of the waistband at the marking, and sew the 10 mm (3/8 in) button to the matching marking on the right waistband extension (picture 5).",
]
for b in step7_bullets:
    y = draw_bullet(c, M_L, y, b, CONTENT_W, font_size=8.6, leading=12.4)

y -= 2
img7_path = os.path.join(ASSET_DIR, "step7_panels.png")
img7_h = 216.0
img7_w = img7_h * (3321.0 / 2736.0)
c.drawImage(img7_path, M_L + (CONTENT_W - img7_w) / 2, y - img7_h, width=img7_w, height=img7_h, preserveAspectRatio=True, mask="auto")
y = y - img7_h - 24

y = draw_step_header(c, y, 8, "Hem the trousers", "Hem · pictures 1–2")
step8_bullets = [
    "Finish the lower raw edge of each trouser leg with an overlocker or zigzag stitch. Turn the hem up to the wrong side along the hemline marking (2 to 3 cm / 3/4 to 1 1/8 in) and press a crisp crease around the ankle.",
    "Secure the hem either by machine topstitching close to the finished upper edge (picture 1) or invisibly with a hand or machine blind-hem stitch (picture 2).",
]
for b in step8_bullets:
    y = draw_bullet(c, M_L, y, b, CONTENT_W, font_size=8.6, leading=12.4)

y -= 2
img8_path = os.path.join(ASSET_DIR, "step8_panels.png")
img8_h = 126.0
img8_w = img8_h * (2708.0 / 1169.0)
c.drawImage(img8_path, M_L + (CONTENT_W - img8_w) / 2, y - img8_h, width=img8_w, height=img8_h, preserveAspectRatio=True, mask="auto")
c.showPage()

# =========================================================================
# PAGE 16: STEP 9: FINISHING & ENJOY YOUR COLETTE TROUSERS
# =========================================================================
draw_page_bg_and_chrome(c, 16)
y = draw_step_header(c, H - 78, 9, "Finishing", "Whole trousers")

step9_bullets = [
    "Remove all visible basting threads at the waist pleats, pockets, and center front fly, and clip any loose thread ends.",
    "Give the trousers a final steam press through a pressing cloth: press the waistband, pocket openings, side seams, inseams, and hems. Leave the front pleats soft and uncreased down the leg for a relaxed modern drape, or press a classic center leg crease if you prefer a formal look.",
]
for b in step9_bullets:
    y = draw_bullet(c, M_L, y, b, CONTENT_W, font_size=9.0, leading=13.2)

y -= 4
y = draw_tip_box(
    c, y,
    "Neat inside",
    "Tack the bottom corners of the front pocket bags lightly to the side seam allowance with two hand stitches so the pockets always stay anchored forward when you walk."
)

y -= 2
y = draw_section_header(c, "Y O U   M A D E   I T", "Enjoy Your Colette Trousers", y_top=y)

# Two square photos side by side (matching Odette Vest Page 16)
p_sz = 192.0
c.drawImage(PHOTO_SIDE, M_L, y - p_sz + 8, width=p_sz, height=p_sz, preserveAspectRatio=True, mask="auto")
c.drawImage(PHOTO_BACK, M_L + p_sz + 24, y - p_sz + 8, width=p_sz, height=p_sz, preserveAspectRatio=True, mask="auto")
y = y - p_sz - 12

c.setFont("Poppins-Medium", 10.2)
c.setFillColor(BURGUNDY)
c.drawString(M_L, y, "Styling ideas")
y -= 14
styling = [
    "Tucked in with a fine-ribbed cream knit top or silk blouse to showcase the double pleats and single-button waistband.",
    "With a relaxed linen button-down shirt and leather loafers for effortless office-to-weekend tailoring.",
    "Sewn in brushed wool twill for autumn and winter, or in washed heavy linen for warm summer days.",
    "Paired with a cropped cardigan or structured blazer that hits right at the high waist.",
]
for st in styling:
    y = draw_bullet(c, M_L, y, st, CONTENT_W, font_size=8.8, leading=12.6)

y -= 4
c.setFont("Poppins-Medium", 10.2)
c.setFillColor(BURGUNDY)
c.drawString(M_L, y, "Care")
y -= 14
y = draw_rich_paragraph(
    c, M_L, y,
    "Follow the care instructions of your suiting fabric. Wool and wool-blend suitings should be dry-cleaned or gently hand-washed cold and steamed on a trouser hanger; linen and cotton-twill versions can be machine-washed cold on a gentle cycle and line-dried.",
    CONTENT_W, font_size=8.8, leading=12.6
)

y -= 6
y = draw_tip_box(
    c, y,
    "Need help?",
    "If a step is unclear, message us through our Etsy shop, SewLuxePatterns. We are happy to help, and we would love to see your finished Colette Trousers."
)

c.setFont("Poppins", 7.3)
c.setFillColor(MUTED)
c.drawString(M_L, 58, "© SewLuxePatterns. This pattern is for personal use. Please do not copy, share or resell the pattern files or this guide.")
c.showPage()

c.save()

# Strip all ReportLab / PDF generator metadata and render all 16 pages to PNG for visual inspection
doc_out = fitz.open(out_pdf_path)
doc_out.set_metadata({"title": "", "author": "", "subject": "", "keywords": "", "creator": "", "producer": ""})
clean_pdf_path = out_pdf_path + ".tmp"
doc_out.save(clean_pdf_path, garbage=4, deflate=True)
doc_out.close()
os.replace(clean_pdf_path, out_pdf_path)

# Render all 16 pages at 120 DPI for visual inspection
doc_verify = fitz.open(out_pdf_path)
print("Total pages generated:", len(doc_verify))
render_dir = os.path.join(SCRATCH_DIR, "colette_booklet_pages")
os.makedirs(render_dir, exist_ok=True)
for i, page in enumerate(doc_verify):
    pix = page.get_pixmap(dpi=120)
    pix.save(os.path.join(render_dir, f"page_{i+1:02d}.png"))
doc_verify.close()
print("All 16 pages rendered to", render_dir)
