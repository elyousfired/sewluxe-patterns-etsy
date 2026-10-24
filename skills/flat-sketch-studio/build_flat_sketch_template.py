import os
import re
import fitz
from PIL import Image

out_dir = r"C:\Users\red1e\.gemini\antigravity\scratch\colette_wide_leg_trousers"

def clean_pants_svg(svg_path, is_front=True):
    raw = open(svg_path, encoding="utf-8").read()
    # Remove the stray crotch bounding construction lines
    raw = re.sub(r'<path d="M47\.03 107\.56L51\.37 105\.72"[^/]*/>', "", raw)
    raw = re.sub(r'<path d="M37\.91 102\.78L60\.96 110\.8"[^/]*/>', "", raw)
    # Upgrade stroke color to #48575B (exact studio charcoal-slate from Odette reference)
    raw = re.sub(r'stroke="#[0-9a-fA-F]+"', 'stroke="#48575B"', raw)
    # Ensure crisp stroke widths: outer & seam lines 0.38, pleats 0.26
    def fix_stroke_width(m):
        tag = m.group(0)
        # Pleat paths have fill="none" or stroke-width="" or small stroke-width
        if 'd="M40.95 81.43' in tag or 'd="M57.52 81.46' in tag or 'd="M38.47 79.62' in tag or 'd="M59.99 79.66' in tag:
            tag = re.sub(r'stroke-width="[^"]*"', 'stroke-width="0.28"', tag)
            if 'stroke=' not in tag:
                tag = tag.replace("<path ", '<path stroke="#48575B" fill="none" ')
            else:
                tag = re.sub(r'fill="[^"]*"', 'fill="none"', tag)
        else:
            tag = re.sub(r'stroke-width="[^"]*"', 'stroke-width="0.38"', tag)
        if 'stroke-linecap' not in tag:
            tag = tag.replace("<path ", '<path stroke-linecap="round" stroke-linejoin="round" ')
        return tag

    raw = re.sub(r"<path[^>]+>", fix_stroke_width, raw)
    raw = re.sub(r'<svg[^>]*>', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="18 68 64 136" width="1200" height="2550">', raw, count=1)
    return raw

front_svg_clean = clean_pants_svg("pants_pleated_svgFront.svg", True)
back_svg_clean = clean_pants_svg("pants_pleated_svgBack.svg", False)

front_svg_file = os.path.join(out_dir, "colette_front_clean.svg")
back_svg_file = os.path.join(out_dir, "colette_back_clean.svg")
with open(front_svg_file, "w", encoding="utf-8") as f:
    f.write(front_svg_clean)
with open(back_svg_file, "w", encoding="utf-8") as f:
    f.write(back_svg_clean)

# Render each at high resolution with transparent background, auto-crop, and compose onto 3600x3600 -> downsample LANCZOS to 1800x1800
def render_cropped_rgba(svg_file):
    doc = fitz.open(svg_file)
    pix = doc[0].get_pixmap(dpi=300, alpha=True)
    img = Image.frombytes("RGBA", [pix.width, pix.height], pix.samples)
    doc.close()
    bbox = img.getbbox()
    return img.crop(bbox)

front_img = render_cropped_rgba(front_svg_file)
back_img = render_cropped_rgba(back_svg_file)

# Save individual high-res front & back PNGs
front_img.save(os.path.join(out_dir, "colette_front_rgba.png"))
back_img.save(os.path.join(out_dir, "colette_back_rgba.png"))

# Compose 3600x3600 studio canvas matching Odette Vest reference layout:
# Front on left (height ~ 2750 px, top ~ 260 px, left ~ 260 px)
# Back on bottom-right (height ~ 1980 px, bottom-aligned near y=3340 px, right ~ 3340 px)
W, H = 3600, 3600
canvas_rgba = Image.new("RGBA", (W, H), (255, 255, 255, 0))

f_h = 2800
f_w = int(front_img.width * (f_h / front_img.height))
front_resized = front_img.resize((f_w, f_h), Image.Resampling.LANCZOS)

b_h = 2020
b_w = int(back_img.width * (b_h / back_img.height))
back_resized = back_img.resize((b_w, b_h), Image.Resampling.LANCZOS)

# Position Front on left, Back on lower-right
f_x = 280
f_y = 260
b_x = W - b_w - 280
b_y = H - b_h - 240

canvas_rgba.alpha_composite(front_resized, (f_x, f_y))
canvas_rgba.alpha_composite(back_resized, (b_x, b_y))

# Downsample 2x with LANCZOS to 1800x1800
final_rgba = canvas_rgba.resize((1800, 1800), Image.Resampling.LANCZOS)
final_rgba.save(os.path.join(out_dir, "flat_sketch_transparent.png"))

final_white = Image.new("RGB", (1800, 1800), (255, 255, 255))
final_white.paste(final_rgba, (0, 0), final_rgba)
final_white.save(os.path.join(out_dir, "flat_sketch_colette.png"), quality=98)
final_white.save(os.path.join(out_dir, "flat_sketch_colette.jpg"), quality=96)
print("Saved flat_sketch_colette.png (1800x1800) and flat_sketch_transparent.png")
