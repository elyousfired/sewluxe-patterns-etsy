#!/usr/bin/env python3
"""
clean_instruction_panel.py
Automated pipeline to clean and frame any Tailornova/PatternFast instruction diagram:
- Reads SVG or image
- Ensures complete viewBox (no cropped text at top/bottom/sides)
- Renders at 300 DPI via PyMuPDF
- Auto-crops to active diagram borders
- Adds bold Poppins callout numbers (1., 2., 3., 4.)
- Wraps inside Gold Standard #F5F2EF container (radius=28, border #E2DDD8)
"""

import os
import re
import sys
from PIL import Image, ImageDraw, ImageFont
import pymupdf as fitz

FONTS_DIR = r"C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\fonts"
FONT_BOLD = os.path.join(FONTS_DIR, "Poppins-Bold.ttf")

def clean_and_frame_instruction(
    input_path: str,
    output_path: str,
    grid_layout: str = "2x2", # '1x1', '2x1' (horizontal), '1x2' (vertical), or '2x2' (4-panel)
    labels: list = None,
    dpi: int = 300,
    container_bg: str = "#F5F2EF",
    container_border: str = "#E2DDD8",
    num_font_size: int = 72,
    padding: int = 40
):
    if labels is None:
        if grid_layout == "2x2":
            labels = ["1.", "2.", "3.", "4."]
        elif grid_layout in ("2x1", "1x2"):
            labels = ["1.", "2."]
        else:
            labels = ["1."]

    # Step 1: Render if SVG, or open image
    if input_path.lower().endswith(".svg"):
        with open(input_path, "r", encoding="utf-8") as f:
            svg_text = f.read()

        # Sanitize Illustrator artifacts
        svg_clean = re.sub(r"<!DOCTYPE[^>]*\[[^\]]*\]>", "", svg_text, flags=re.S)
        svg_clean = re.sub(r'xmlns:(?:x|i|graph)="[^"]*"', "", svg_clean)
        svg_clean = re.sub(r"<foreignObject[^>]*>.*?</foreignObject>", "", svg_clean, flags=re.S)
        svg_clean = re.sub(r"</?switch>", "", svg_clean)

        # Inline CSS classes from <style> blocks (e.g. .st0, .st1, .st2)
        styles = {}
        for style_block in re.findall(r"<style[^>]*>(.*?)</style>", svg_clean, flags=re.S):
            for cls_name, props in re.findall(r"\.([\w\-]+)\s*\{([^}]*)\}", style_block):
                styles[cls_name.strip()] = props.strip()
        if styles:
            def repl_class(m):
                classes = m.group(1).split()
                inlined = "; ".join(styles.get(c, "") for c in classes if c in styles)
                return f'style="{inlined}"'
            svg_clean = re.sub(r'\bclass="([^"]+)"', repl_class, svg_clean)

        doc = fitz.open(stream=svg_clean.encode("utf-8"), filetype="svg")
        page = doc[0]
        pix = page.get_pixmap(dpi=dpi, alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    else:
        img = Image.open(input_path).convert("RGB")

    # Step 2: Auto-crop to active diagram bounds
    gray = img.convert("L")
    bw = gray.point(lambda p: 255 if p < 85 else 0)
    bbox = bw.getbbox()
    if bbox:
        # Add a tiny 4px safety breathing room
        x0 = max(0, bbox[0] - 4)
        y0 = max(0, bbox[1] - 4)
        x1 = min(img.width, bbox[2] + 4)
        y1 = min(img.height, bbox[3] + 4)
        cropped = img.crop((x0, y0, x1, y1))
    else:
        cropped = img.copy()

    w_c, h_c = cropped.size

    # Step 3: Overlay bold callouts based on grid layout
    draw_crop = ImageDraw.Draw(cropped)
    f_num = ImageFont.truetype(FONT_BOLD, num_font_size)

    if grid_layout == "2x2":
        mid_x = w_c // 2
        mid_y = h_c // 2
        draw_crop.text((45, 35), labels[0], font=f_num, fill="#000000")
        draw_crop.text((mid_x + 45, 35), labels[1], font=f_num, fill="#000000")
        draw_crop.text((45, mid_y + 35), labels[2], font=f_num, fill="#000000")
        draw_crop.text((mid_x + 45, mid_y + 35), labels[3], font=f_num, fill="#000000")
    elif grid_layout == "2x1":
        mid_x = w_c // 2
        draw_crop.text((45, 35), labels[0], font=f_num, fill="#000000")
        draw_crop.text((mid_x + 45, 35), labels[1], font=f_num, fill="#000000")
    elif grid_layout == "1x2":
        mid_y = h_c // 2
        draw_crop.text((45, 35), labels[0], font=f_num, fill="#000000")
        draw_crop.text((45, mid_y + 35), labels[1], font=f_num, fill="#000000")
    elif grid_layout == "1x1":
        draw_crop.text((45, 35), labels[0], font=f_num, fill="#000000")

    # Step 4: Wrap inside Gold Standard #F5F2EF container
    final_w = w_c + 2 * padding
    final_h = h_c + 2 * padding
    container = Image.new("RGB", (final_w, final_h), "#FAF8F6")
    draw_cont = ImageDraw.Draw(container)
    draw_cont.rounded_rectangle(
        [6, 6, final_w - 7, final_h - 7],
        radius=28,
        fill=container_bg,
        outline=container_border,
        width=4
    )

    container.paste(cropped, (padding, padding))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    container.save(output_path, quality=95)
    print(f"[OK] Cleaned & Framed: {output_path} ({final_w}x{final_h})")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) > 2:
        clean_and_frame_instruction(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python clean_instruction_panel.py <input_svg_or_png> <output_png> [grid_layout]")
