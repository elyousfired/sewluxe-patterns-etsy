import os
import re
import pymupdf as fitz
from PIL import Image, ImageDraw, ImageFont

SCRATCH_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\c675070e-91f4-406b-8086-d794cba1db24\scratch"
SVG_DIR = r"C:\Users\red1e\.gemini\antigravity\scratch\colette_wide_leg_trousers\source_instructions\svgs"
OUT_DIR = os.path.join(SCRATCH_DIR, "booklet_assets")
os.makedirs(OUT_DIR, exist_ok=True)

FONT_BOLD = r"C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\fonts\Poppins-Bold.ttf"
FONT_REG = r"C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\fonts\Poppins-Regular.ttf"
FONT_MED = r"C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\fonts\Poppins-Medium.ttf"

# 1. Clean pieces_img.svg for Page 7
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
            return f'<text x="{x:.3f}" y="{y+1.5:.3f}" font-size="5.2" font-weight="bold" fill="#8C3B47" font-family="Helvetica, Arial, sans-serif" style="text-anchor: middle">{content}</text>'
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
        rf'\1<rect x="{parts[0]}" y="{parts[1]}" width="{parts[2]}" height="{parts[3]}" fill="#FFFFFF"/>',
        svg_txt_clean,
        count=1,
    )

doc = fitz.open(stream=svg_txt_clean.encode("utf-8"), filetype="svg")
pix = doc[0].get_pixmap(dpi=300, alpha=False)
pieces_png = os.path.join(OUT_DIR, "pieces_overview_clean.png")
pix.save(pieces_png)
print("Saved pieces_overview_clean.png:", pix.width, pix.height)

# 3. Helper to frame single or two-panel step images like Odette Vest
def make_two_panel_box(img_left: Image.Image, img_right: Image.Image, label_left="1.", label_right="2.", out_name="step.png"):
    # Target canvas: 2200 x 1050 with #F5F2EF rounded container, two white boxes with 3px black border
    W, H = 2200, 1050
    canvas = Image.new("RGB", (W, H), (250, 248, 246)) # page bg #FAF8F6
    draw = ImageDraw.Draw(canvas)
    # Outer rounded rect #F5F2EF with border #E2DDD8
    draw.rounded_rectangle([4, 4, W-5, H-5], radius=24, fill=(245, 242, 239), outline=(226, 221, 216), width=3)
    pad = 36
    gap = 36
    box_w = (W - 2*pad - gap) // 2
    box_h = H - 2*pad
    font_num = ImageFont.truetype(FONT_BOLD, 44)
    for idx, (sub_img, lbl) in enumerate([(img_left, label_left), (img_right, label_right)]):
        bx0 = pad + idx * (box_w + gap)
        by0 = pad
        bx1 = bx0 + box_w
        by1 = by0 + box_h
        draw.rectangle([bx0, by0, bx1, by1], fill=(255, 255, 255), outline=(0, 0, 0), width=4)
        # Fit sub_img inside box with margin
        inner_w = box_w - 80
        inner_h = box_h - 100
        sub_copy = sub_img.copy()
        sub_copy.thumbnail((inner_w, inner_h), Image.Resampling.LANCZOS)
        ix = bx0 + (box_w - sub_copy.width) // 2
        iy = by0 + 60 + (inner_h - sub_copy.height) // 2
        canvas.paste(sub_copy, (ix, iy))
        draw.text((bx0 + 26, by0 + 18), lbl, fill=(0, 0, 0), font=font_num)
    out_path = os.path.join(OUT_DIR, out_name)
    canvas.save(out_path)
    print("Saved", out_name)

def make_single_panel_box(img_main: Image.Image, label="1.", out_name="step.png", box_w_ratio=0.62):
    W, H = 2200, 960
    box_w = int(W * box_w_ratio)
    pad = 36
    outer_w = box_w + 2*pad
    canvas = Image.new("RGB", (outer_w, H), (250, 248, 246))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle([4, 4, outer_w-5, H-5], radius=24, fill=(245, 242, 239), outline=(226, 221, 216), width=3)
    bx0, by0 = pad, pad
    bx1, by1 = outer_w - pad, H - pad
    draw.rectangle([bx0, by0, bx1, by1], fill=(255, 255, 255), outline=(0, 0, 0), width=4)
    inner_w = (bx1 - bx0) - 80
    inner_h = (by1 - by0) - 100
    sub_copy = img_main.copy()
    sub_copy.thumbnail((inner_w, inner_h), Image.Resampling.LANCZOS)
    ix = bx0 + ((bx1 - bx0) - sub_copy.width) // 2
    iy = by0 + 50 + (inner_h - sub_copy.height) // 2
    canvas.paste(sub_copy, (ix, iy))
    font_num = ImageFont.truetype(FONT_BOLD, 44)
    draw.text((bx0 + 26, by0 + 18), label, fill=(0, 0, 0), font=font_num)
    out_path = os.path.join(OUT_DIR, out_name)
    canvas.save(out_path)
    print("Saved", out_name)

def wrap_multi_panel_svg(svg_filename, out_name, recolor_red=False):
    p = os.path.join(SVG_DIR, svg_filename)
    txt = open(p, encoding="utf-8").read()
    txt_clean = re.sub(r"<!DOCTYPE[^>]*\[[^\]]*\]>", "", txt, flags=re.S)
    txt_clean = re.sub(r'xmlns:(?:x|i|graph)="[^"]*"', "", txt_clean)
    txt_clean = re.sub(r"<foreignObject[^>]*>.*?</foreignObject>", "", txt_clean, flags=re.S)
    txt_clean = re.sub(r"</?switch>", "", txt_clean)
    txt_clean = re.sub(r'\bi:\w+="[^"]*"', "", txt_clean)
    if recolor_red:
        txt_clean = txt_clean.replace("#ED1C24", "#000000").replace("#ed1c24", "#000000")
    styles = {}
    for style_block in re.findall(r"<style[^>]*>(.*?)</style>", txt_clean, flags=re.S):
        for cls_name, props in re.findall(r"\.([\w\-]+)\s*\{([^}]*)\}", style_block):
            styles[cls_name.strip()] = props.strip()
    if styles:
        def repl_class(m):
            classes = m.group(1).split()
            inlined = ";".join(styles.get(c, "") for c in classes if c in styles)
            return f'style="{inlined}"'
        txt_clean = re.sub(r'\bclass="([^"]+)"', repl_class, txt_clean)
    vb = re.search(r'viewBox="0 0 ([\d\.]+) ([\d\.]+)"', txt_clean)
    if vb:
        w_vb, h_vb = vb.group(1), vb.group(2)
        txt_clean = re.sub(
            r"(<svg[^>]*>)",
            rf'\1<rect x="0" y="0" width="{w_vb}" height="{h_vb}" fill="#F5F2EF"/>',
            txt_clean,
            count=1,
        )
    # Also make sure interior panel rects have white fill if they had none
    doc = fitz.open(stream=txt_clean.encode("utf-8"), filetype="svg")
    pix = doc[0].get_pixmap(dpi=300, alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    # Crop excess whitespace around the black panel borders
    gray = img.convert("L")
    # Find bounding box of pixels darker than 200
    bw = gray.point(lambda x: 0 if x < 200 else 255, "1")
    from PIL import ImageOps
    inv = ImageOps.invert(bw.convert("L"))
    bbox = inv.getbbox()
    if bbox:
        img = img.crop((max(0, bbox[0]-10), max(0, bbox[1]-10), min(img.width, bbox[2]+10), min(img.height, bbox[3]+10)))
    # Place on rounded #F5F2EF container
    pad = 36
    W, H = img.width + 2*pad, img.height + 2*pad
    canvas = Image.new("RGB", (W, H), (250, 248, 246))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle([4, 4, W-5, H-5], radius=24, fill=(245, 242, 239), outline=(226, 221, 216), width=3)
    # Replace exterior #F5F2EF vs interior white: actually the original PNG already has white interior and white exterior, so pasting img on #F5F2EF with white background looks great or we floodfill the outer margin of img with #F5F2EF!
    ImageDraw.floodfill(img, (0, 0), (245, 242, 239), thresh=10)
    ImageDraw.floodfill(img, (img.width-1, 0), (245, 242, 239), thresh=10)
    ImageDraw.floodfill(img, (0, img.height-1), (245, 242, 239), thresh=10)
    ImageDraw.floodfill(img, (img.width-1, img.height-1), (245, 242, 239), thresh=10)
    canvas.paste(img, (pad, pad))
    out_path = os.path.join(OUT_DIR, out_name)
    canvas.save(out_path)
    print("Saved", out_name, canvas.size)

# Step 1: 01_pleats_and_back_darts.png has BACK dart on left, FRONT pleats on right. Let's put FRONT pleats as 1. (left) and BACK dart as 2. (right)!
img01 = Image.open(os.path.join(SVG_DIR, "01_pleats_and_back_darts.png"))
w01, h01 = img01.size
back_dart_img = img01.crop((int(w01*0.05), int(h01*0.04), int(w01*0.52), int(h01*0.96)))
front_pleat_img = img01.crop((int(w01*0.53), int(h01*0.04), int(w01*0.95), int(h01*0.96)))
make_two_panel_box(front_pleat_img, back_dart_img, "1.", "2.", "step1_panels.png")

# Step 2: 03_side_pockets.svg
wrap_multi_panel_svg("03_side_pockets.svg", "step2_panels.png", recolor_red=True)

# Step 3: 04_back_welt_pockets.svg
wrap_multi_panel_svg("04_back_welt_pockets.svg", "step3_panels.png", recolor_red=False)

# Step 4: 05_zipper_fly.svg
wrap_multi_panel_svg("05_zipper_fly.svg", "step4_panels.png", recolor_red=False)

# Step 5: Inseams (1.) and Crotch seam (2.) side by side!
img06 = Image.open(os.path.join(SVG_DIR, "06_inseams.png"))
img07 = Image.open(os.path.join(SVG_DIR, "07_crotch_seam.png"))
make_two_panel_box(img06, img07, "1.", "2.", "step5_panels.png")

# Step 6: Side seams (1.)
img08 = Image.open(os.path.join(SVG_DIR, "08_side_seams.png"))
make_single_panel_box(img08, "1.", "step6_panels.png", box_w_ratio=0.68)

# Step 7: Waistband (09_waistband.svg)
wrap_multi_panel_svg("09_waistband.svg", "step7_panels.png", recolor_red=False)

# Step 8: Hem (10_hem.svg)
wrap_multi_panel_svg("10_hem.svg", "step8_panels.png", recolor_red=False)
