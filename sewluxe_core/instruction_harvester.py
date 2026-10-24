#!/usr/bin/env python3
"""
instruction_harvester.py
========================
Official PatternFast/Tailornova Instruction Harvester & Luxury Panel Engine:
1. Connects to official API: https://api.patternfast.com/api/sewing-instructions
2. Downloads official instructions PDF & JSON manifest.
3. Automatically strips raw generic body text (below y=285 pt) to prevent text collisions.
4. Auto-detects single or dual-piece diagrams, auto-splits side-by-side figures.
5. Assembles Gold Standard Argon panels:
   - Luxury #F5F2EF rounded container (radius=28, border #E2DDD8).
   - Distinct white inner rectangular boxes (#FFFFFF) with crisp 4px black outlines.
   - Bold Poppins-Bold callout numbers (1., 2., 3., 4.).
   - Clean professional titles and subtitles.
   - Strict Zero-Overlap typography.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from typing import Dict, List, Any, Optional
import pymupdf as fitz
from PIL import Image, ImageDraw, ImageFont

FONTS_DIR = r"C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\fonts"
FONT_BOLD = os.path.join(FONTS_DIR, "Poppins-Bold.ttf")
FONT_MED = os.path.join(FONTS_DIR, "Poppins-Medium.ttf")

class InstructionHarvester:
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json"
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}" if not self.token.startswith("Bearer") else self.token

    def fetch_official_instructions_pdf(
        self,
        elem_ids: str,
        mannequin_id: str,
        category_code: str,
        out_pdf_path: str
    ) -> str:
        """Downloads the official 28-page Tailornova sewing instructions PDF directly from the API."""
        payload = json.dumps({
            "sketchFront": "<svg></svg>",
            "sketchBack": "<svg></svg>",
            "name": "Garment Instructions"
        }).encode("utf-8")

        qs = urllib.parse.urlencode({
            "elementIds": elem_ids,
            "mannequinId": mannequin_id,
            "categoryCode": category_code,
            "format": "pdf",
            "orientation": "portrait",
            "seamAllowance": "1",
            "fabricType": "1",
            "fit": "2"
        })
        url = f"https://api.patternfast.com/api/sewing-instructions?{qs}"
        req = urllib.request.Request(
            url,
            data=payload,
            headers={**self.headers, "Content-Type": "application/json; charset=UTF-8"}
        )
        os.makedirs(os.path.dirname(os.path.abspath(out_pdf_path)), exist_ok=True)
        with urllib.request.urlopen(req, timeout=30) as resp, open(out_pdf_path, "wb") as f:
            f.write(resp.read())
        print(f"[OK] Downloaded official instruction PDF: {out_pdf_path} ({os.path.getsize(out_pdf_path)} bytes)")
        return out_pdf_path

    @staticmethod
    def extract_pure_drawing(
        doc: fitz.Document,
        page_index: int,
        out_png_path: str,
        y_min_pt: float = 285.0,
        y_max_pt: float = 650.0,
        dpi: int = 300
    ) -> str:
        """Renders vector drawing strictly below y_min_pt to strip raw colliding body text."""
        page = doc[page_index]
        clip_rect = fitz.Rect(30, y_min_pt, page.rect.width - 30, y_max_pt)
        pix = page.get_pixmap(clip=clip_rect, dpi=dpi)
        
        # Save temp render and tight-crop
        os.makedirs(os.path.dirname(os.path.abspath(out_png_path)), exist_ok=True)
        pix.save(out_png_path)

        im = Image.open(out_png_path)
        gray = im.convert("L")
        bw = gray.point(lambda p: 255 if p < 245 else 0)
        bbox = bw.getbbox()
        if bbox:
            tight = im.crop((
                max(0, bbox[0] - 15),
                max(0, bbox[1] - 15),
                min(im.width, bbox[2] + 15),
                min(im.height, bbox[3] + 15)
            ))
            tight.save(out_png_path)
        print(f"[OK] Extracted pure drawing: {out_png_path}")
        return out_png_path

    @staticmethod
    def split_side_by_side_pieces(image_path: str) -> tuple[str, str]:
        """Auto-detects vertical whitespace gap and splits into Left and Right pieces."""
        im = Image.open(image_path)
        w, h = im.size
        gray = im.convert("L")
        bw = gray.point(lambda p: 255 if p < 245 else 0)

        # Scan middle third
        col_sums = []
        for x in range(w // 3, 2 * w // 3):
            col = sum(bw.getpixel((x, y)) for y in range(h))
            col_sums.append((col, x))

        col_sums.sort()
        _, split_x = col_sums[0]

        left_im = im.crop((0, 0, split_x, h))
        right_im = im.crop((split_x, 0, w, h))

        dir_name = os.path.dirname(image_path)
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        p_left = os.path.join(dir_name, f"{base_name}_left.png")
        p_right = os.path.join(dir_name, f"{base_name}_right.png")

        left_im.save(p_left)
        right_im.save(p_right)
        return p_left, p_right

    @staticmethod
    def build_dual_panel_box(
        piece_left_path: str,
        piece_right_path: str,
        output_path: str,
        title_1: str,
        title_2: str,
        sub_1: str = "",
        sub_2: str = "",
        canvas_w: int = 2400,
        canvas_h: int = 1200
    ) -> str:
        """Assembles Gold Standard dual-panel box with luxury container and zero text overlaps."""
        img = Image.new("RGB", (canvas_w, canvas_h), "#FAF8F6")
        draw = ImageDraw.Draw(img)

        # Outer container
        draw.rounded_rectangle(
            [15, 15, canvas_w - 16, canvas_h - 16],
            radius=28,
            fill="#F5F2EF",
            outline="#E2DDD8",
            width=3
        )

        box_w = 1115
        box_h = 1090
        gap = 80
        m_left = (canvas_w - (2 * box_w + gap)) // 2
        y_top = (canvas_h - box_h) // 2

        b1_x0, b1_y0 = m_left, y_top
        b1_x1, b1_y1 = b1_x0 + box_w, b1_y0 + box_h

        b2_x0, b2_y0 = b1_x1 + gap, y_top
        b2_x1, b2_y1 = b2_x0 + box_w, b2_y0 + box_h

        draw.rectangle([b1_x0, b1_y0, b1_x1, b1_y1], fill="#FFFFFF", outline="#000000", width=4)
        draw.rectangle([b2_x0, b2_y0, b2_x1, b2_y1], fill="#FFFFFF", outline="#000000", width=4)

        f_num = ImageFont.truetype(FONT_BOLD, 56)
        f_title = ImageFont.truetype(FONT_BOLD, 26)
        f_sub = ImageFont.truetype(FONT_MED, 18)

        # Header 1
        num_1 = title_1.split(".")[0] + "." if "." in title_1 else "1."
        t1_text = title_1.split(".", 1)[-1].strip() if "." in title_1 else title_1
        draw.text((b1_x0 + 35, b1_y0 + 25), num_1, font=f_num, fill="#000000")
        draw.text((b1_x0 + 115, b1_y0 + 32), t1_text, font=f_title, fill="#111111")
        if sub_1:
            draw.text((b1_x0 + 115, b1_y0 + 72), sub_1, font=f_sub, fill="#666666")

        # Header 2
        num_2 = title_2.split(".")[0] + "." if "." in title_2 else "2."
        t2_text = title_2.split(".", 1)[-1].strip() if "." in title_2 else title_2
        draw.text((b2_x0 + 35, b2_y0 + 25), num_2, font=f_num, fill="#000000")
        draw.text((b2_x0 + 115, b2_y0 + 32), t2_text, font=f_title, fill="#111111")
        if sub_2:
            draw.text((b2_x0 + 115, b2_y0 + 72), sub_2, font=f_sub, fill="#666666")

        def tight_crop(im):
            g = im.convert("L")
            bw = g.point(lambda p: 255 if p < 245 else 0)
            bb = bw.getbbox()
            return im.crop(bb) if bb else im

        p1_tight = tight_crop(Image.open(piece_left_path))
        p2_tight = tight_crop(Image.open(piece_right_path))

        avail_w = box_w - 70
        avail_h = box_h - 150
        area_y0 = b1_y0 + 120

        # Scale 1
        s1 = min(avail_w / p1_tight.width, avail_h / p1_tight.height, 1.25)
        w1, h1 = int(p1_tight.width * s1), int(p1_tight.height * s1)
        p1_s = p1_tight.resize((w1, h1), Image.Resampling.LANCZOS)
        img.paste(p1_s, (b1_x0 + (box_w - w1) // 2, area_y0 + (avail_h - h1) // 2))

        # Scale 2
        s2 = min(avail_w / p2_tight.width, avail_h / p2_tight.height, 1.25)
        w2, h2 = int(p2_tight.width * s2), int(p2_tight.height * s2)
        p2_s = p2_tight.resize((w2, h2), Image.Resampling.LANCZOS)
        img.paste(p2_s, (b2_x0 + (box_w - w2) // 2, area_y0 + (avail_h - h2) // 2))

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        img.save(output_path, quality=95)
        print(f"[OK] Generated Gold Standard dual-panel box: {output_path}")
        return output_path
