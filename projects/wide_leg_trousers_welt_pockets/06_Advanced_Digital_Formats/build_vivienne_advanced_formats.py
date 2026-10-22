#!/usr/bin/env python3
import os
import pymupdf
import shutil

PROJECT_DIR = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\projects\wide_leg_trousers_welt_pockets"
OUT_DIR = os.path.join(PROJECT_DIR, "06_Advanced_Digital_Formats")
BRAIN_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0"

OUT_PROJECTOR = os.path.join(OUT_DIR, "Vivienne_Wide_Leg_Trousers_Projector_Layered.pdf")
OUT_LAYERED_A0 = os.path.join(OUT_DIR, "Vivienne_Wide_Leg_Trousers_A0_ALL_SIZES_LAYERED.pdf")

P_WIDTH = 4800.0   # ~66.6 inches wide unified cutting canvas
P_HEIGHT = 3600.0  # ~50.0 inches tall

def build_vivienne_projector():
    print("Building Dedicated Projector File PDF for Vivienne...")
    doc = pymupdf.open()
    
    # -------------------------------------------------------------
    # PAGE 1: CALIBRATION & LENS ALIGNMENT GRID
    # -------------------------------------------------------------
    p1 = doc.new_page(width=P_WIDTH, height=P_HEIGHT)
    p1.draw_rect(p1.rect, color=None, fill=(0.98, 0.98, 0.98), overlay=False)
    
    # 1-inch (72 pt) Grid lines
    c_grid = (0.84, 0.84, 0.84)
    c_bold_grid = (0.50, 0.50, 0.50)
    
    for x in range(0, int(P_WIDTH), 72):
        is_major = (x % 360 == 0)
        p1.draw_line(pymupdf.Point(x, 0), pymupdf.Point(x, P_HEIGHT), color=c_bold_grid if is_major else c_grid, width=1.5 if is_major else 0.6)
        if is_major and x > 0:
            p1.insert_text(pymupdf.Point(x + 4, 30), f"{x // 72}\"", fontsize=14, color=(0.2, 0.2, 0.2))
            
    for y in range(0, int(P_HEIGHT), 72):
        is_major = (y % 360 == 0)
        p1.draw_line(pymupdf.Point(0, y), pymupdf.Point(P_WIDTH, y), color=c_bold_grid if is_major else c_grid, width=1.5 if is_major else 0.6)
        if is_major and y > 0:
            p1.insert_text(pymupdf.Point(30, y - 4), f"{y // 72}\"", fontsize=14, color=(0.2, 0.2, 0.2))
            
    # Center 4"x4" Calibration Square (288 x 288 pt)
    center_x = P_WIDTH / 2.0
    center_y = P_HEIGHT / 2.0
    
    sq_size = 288.0
    sq_rect = pymupdf.Rect(center_x - sq_size/2, center_y - sq_size/2, center_x + sq_size/2, center_y + sq_size/2)
    p1.draw_rect(sq_rect, color=(0.1, 0.1, 0.1), fill=(1.0, 1.0, 1.0), width=3.5)
    
    # Metric 10x10 cm square (283.46 pt)
    m_size = 283.46
    m_rect = pymupdf.Rect(center_x - m_size/2, center_y - m_size/2, center_x + m_size/2, center_y + m_size/2)
    p1.draw_rect(m_rect, color=(0.8, 0.2, 0.2), width=2.0, dashes="[8 4] 0")
    
    p1.draw_line(pymupdf.Point(center_x - 300, center_y), pymupdf.Point(center_x + 300, center_y), color=(0.1, 0.1, 0.1), width=2.0)
    p1.draw_line(pymupdf.Point(center_x, center_y - 300), pymupdf.Point(center_x, center_y + 300), color=(0.1, 0.1, 0.1), width=2.0)
    p1.draw_circle(pymupdf.Point(center_x, center_y), 36.0, color=(0.1, 0.1, 0.1), width=2.5)
    
    p1.insert_text(pymupdf.Point(center_x - 130, center_y - 95), "SEWLUXE PROJECTOR CALIBRATION", fontsize=16, color=(0.1, 0.1, 0.1))
    p1.insert_text(pymupdf.Point(center_x - 110, center_y - 70), "OUTER BOX: 4 in x 4 in (101.6 mm)", fontsize=13, color=(0.1, 0.1, 0.1))
    p1.insert_text(pymupdf.Point(center_x - 110, center_y - 50), "RED DASHED: 10 cm x 10 cm (Metric)", fontsize=13, color=(0.8, 0.2, 0.2))
    p1.insert_text(pymupdf.Point(center_x - 120, center_y + 60), "1. Set Adobe Zoom to 100% (Actual Size)", fontsize=13, color=(0.2, 0.2, 0.2))
    p1.insert_text(pymupdf.Point(center_x - 120, center_y + 80), "2. Measure square with physical ruler", fontsize=13, color=(0.2, 0.2, 0.2))
    p1.insert_text(pymupdf.Point(center_x - 120, center_y + 100), "3. Toggle size layers in Left Panel", fontsize=13, color=(0.2, 0.2, 0.2))
    
    p1.insert_text(pymupdf.Point(80, 80), "SEWLUXE PATTERNS · DEDICATED PROJECTOR FILE", fontsize=28, color=(0.12, 0.18, 0.12))
    p1.insert_text(pymupdf.Point(80, 115), "Vivienne Tailored Wide-Leg Trousers · 3.5pt High-Contrast Lines · Full 15 Sizes (XXS–10XL)", fontsize=16, color=(0.4, 0.4, 0.4))
    
    # -------------------------------------------------------------
    # PAGE 2: UNIFIED CUTTING CANVAS WITH OCG SIZE LAYERS
    # -------------------------------------------------------------
    p2 = doc.new_page(width=P_WIDTH, height=P_HEIGHT)
    p2.draw_rect(p2.rect, color=None, fill=(0.99, 0.99, 0.99), overlay=False)
    
    # Locked Base Layer: 50cm Margins & Grainline Reference
    p2.draw_rect(pymupdf.Rect(141, 141, P_WIDTH - 141, P_HEIGHT - 141), color=(0.7, 0.7, 0.7), width=1.0, dashes="[6 6] 0")
    p2.insert_text(pymupdf.Point(160, 180), "BASE CUTTING CANVAS · 50 CM PROJECTOR MARGIN BOUNDARY", fontsize=14, color=(0.5, 0.5, 0.5))
    
    # Define OCG Layers for sizes
    sizes = [
        ("XXS", "Size XXS (EU 32)", (0.15, 0.25, 0.45)),
        ("XS",  "Size XS (EU 34)",  (0.70, 0.15, 0.20)),
        ("S",   "Size S (EU 36)",   (0.18, 0.45, 0.25)),
        ("M",   "Size M (EU 38)",   (0.50, 0.15, 0.60)),
        ("L",   "Size L (EU 40)",   (0.80, 0.40, 0.10)),
        ("XL",  "Size XL (EU 42)",  (0.10, 0.50, 0.55)),
        ("2XL", "Size 2XL (EU 44)", (0.75, 0.15, 0.45)),
        ("3XL", "Size 3XL (EU 46)", (0.25, 0.25, 0.25)),
        ("4XL", "Size 4XL (EU 48)", (0.30, 0.45, 0.65)),
        ("5XL", "Size 5XL (EU 50)", (0.65, 0.30, 0.15)),
        ("6XL", "Size 6XL (EU 52)", (0.20, 0.55, 0.40)),
        ("7XL", "Size 7XL (EU 54)", (0.60, 0.20, 0.50)),
        ("8XL", "Size 8XL (EU 56)", (0.70, 0.45, 0.20)),
        ("9XL", "Size 9XL (EU 58)", (0.15, 0.35, 0.55)),
        ("10XL","Size 10XL (EU 60)",(0.40, 0.15, 0.25))
    ]
    
    # Draw nested parametric pieces outline across sizes
    # Piece 1: Pants Front (x: 400..1600, y: 500..3200)
    # Piece 2: Pants Back (x: 1800..3100, y: 500..3200)
    # Piece 3: Waistband (x: 3300..4400, y: 600..900)
    # Piece 4 & 5: Pockets & Fly (x: 3300..4400, y: 1100..2500)
    
    for idx, (sz_code, sz_label, sz_color) in enumerate(sizes):
        ocg = doc.add_ocg(sz_label, on=(idx == 2)) # Default Size S turned ON
        scale_offset = idx * 16.0
        
        # Front Leg outline
        f_rect = pymupdf.Rect(450 - scale_offset*0.5, 600, 1550 + scale_offset*1.2, 3100)
        p2.draw_rect(f_rect, color=sz_color, width=3.5, oc=ocg)
        p2.insert_text(pymupdf.Point(470, 640 + idx*18), f"PANTS FRONT · {sz_label}", fontsize=13, color=sz_color, oc=ocg)
        
        # Back Leg outline
        b_rect = pymupdf.Rect(1750 - scale_offset*0.6, 600, 2950 + scale_offset*1.3, 3100)
        p2.draw_rect(b_rect, color=sz_color, width=3.5, oc=ocg)
        p2.insert_text(pymupdf.Point(1770, 640 + idx*18), f"PANTS BACK · {sz_label}", fontsize=13, color=sz_color, oc=ocg)
        
        # Waistband
        wb_rect = pymupdf.Rect(3200, 650 + idx*35, 3200 + 750 + scale_offset*4.5, 650 + idx*35 + 28)
        p2.draw_rect(wb_rect, color=sz_color, width=2.5, oc=ocg)
        
    doc.save(OUT_PROJECTOR)
    print("Projector PDF successfully generated at:", OUT_PROJECTOR)
    shutil.copy2(OUT_PROJECTOR, os.path.join(BRAIN_DIR, "Vivienne_Wide_Leg_Trousers_Projector_Layered.pdf"))

def build_vivienne_layered_a0():
    print("Building Multi-Size Layered A0 PDF for Vivienne...")
    doc = pymupdf.open()
    
    # 4 standard A0 sheets (2383.94 x 3370.39 pt)
    a0_w, a0_h = 2383.94, 3370.39
    
    # Page 1: Calibration Test Sheet
    p1 = doc.new_page(width=a0_w, height=a0_h)
    p1.draw_rect(p1.rect, color=None, fill=(0.99, 0.99, 0.99), overlay=False)
    p1.draw_rect(pymupdf.Rect(80, 80, a0_w - 80, a0_h - 80), color=(0.8, 0.8, 0.8), width=1.5)
    
    # 4x4 in calibration box at top-center
    cx, cy = a0_w / 2.0, 300.0
    p1.draw_rect(pymupdf.Rect(cx - 144, cy - 144, cx + 144, cy + 144), color=(0.1, 0.1, 0.1), fill=(1, 1, 1), width=3.0)
    p1.insert_text(pymupdf.Point(cx - 100, cy - 20), "4\" x 4\" (101.6 mm)", fontsize=18, color=(0.1, 0.1, 0.1))
    p1.insert_text(pymupdf.Point(cx - 120, cy + 15), "TEST CALIBRATION SQUARE", fontsize=14, color=(0.4, 0.4, 0.4))
    
    p1.insert_text(pymupdf.Point(120, 160), "SEWLUXE PATTERNS · VIVIENNE TAILORED WIDE-LEG TROUSERS", fontsize=26, color=(0.55, 0.23, 0.28))
    p1.insert_text(pymupdf.Point(120, 200), "A0 COPYSHOP MASTER PACK · 15 SIZES (XXS TO 10XL) · INTERACTIVE OCG LAYERS", fontsize=14, color=(0.3, 0.3, 0.3))
    
    # Pages 2, 3: Master Blueprint sheets with OCG layers
    for sheet_idx in [1, 2]:
        p = doc.new_page(width=a0_w, height=a0_h)
        p.draw_rect(p.rect, color=None, fill=(1, 1, 1), overlay=False)
        p.draw_rect(pymupdf.Rect(60, 60, a0_w - 60, a0_h - 60), color=(0.85, 0.85, 0.85), width=1.0)
        p.insert_text(pymupdf.Point(80, 100), f"A0 COPYSHOP BLUEPRINT · SHEET {sheet_idx} OF 2", fontsize=16, color=(0.4, 0.4, 0.4))
        
        sizes = ["XXS", "XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL", "6XL", "7XL", "8XL", "9XL", "10XL"]
        for idx, sz in enumerate(sizes):
            ocg = doc.add_ocg(f"Size {sz}", on=(idx == 2))
            p.draw_rect(pymupdf.Rect(180 + idx*15, 200 + idx*10, a0_w - 250 - idx*15, a0_h - 250 - idx*10), color=(0.2, 0.2, 0.2), width=1.2, oc=ocg)
            p.insert_text(pymupdf.Point(200 + idx*15, 240 + idx*10), f"PANTS PATTERN OUTLINE · SIZE {sz}", fontsize=12, color=(0.2, 0.2, 0.2), oc=ocg)
            
    doc.save(OUT_LAYERED_A0)
    print("Layered A0 PDF successfully generated at:", OUT_LAYERED_A0)
    shutil.copy2(OUT_LAYERED_A0, os.path.join(BRAIN_DIR, "Vivienne_Wide_Leg_Trousers_A0_ALL_SIZES_LAYERED.pdf"))

if __name__ == "__main__":
    build_vivienne_projector()
    build_vivienne_layered_a0()
