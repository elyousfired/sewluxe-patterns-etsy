#!/usr/bin/env python3
"""
build_projector_and_layered_patterns.py
========================================
Builds the two advanced digital pattern deliverables for SewLuxe Margot Wide-Leg Pants:
1. Margot_Wide_Leg_Pants_A0_ALL_SIZES_LAYERED.pdf (Multi-Size OCG Layered A0 Copyshop PDF)
2. Margot_Elastic_Wide_Leg_Pants_Projector_Layered.pdf (Dedicated High-Contrast Projector File)
"""

import os
import pymupdf

# Source directory containing cleaned single-size A0 PDFs
A0_DIR = r"C:\Users\red1e\Desktop\SewLuxe_Elastic_Wide_Leg_Pants\03_Patterns_PDF\A0_CopyShop"
FONTS_DIR = r"C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\fonts"

OUT_A0_LAYERED = r"C:\Users\red1e\Desktop\SewLuxe_Elastic_Wide_Leg_Pants\03_Patterns_PDF\Margot_Wide_Leg_Pants_A0_ALL_SIZES_LAYERED.pdf"
OUT_PROJECTOR = r"C:\Users\red1e\Desktop\SewLuxe_Elastic_Wide_Leg_Pants\03_Patterns_PDF\Margot_Elastic_Wide_Leg_Pants_Projector_Layered.pdf"

OUT_DESKTOP_GUIDE_DIR = r"C:\Users\red1e\Desktop\SewLuxe_Elastic_Wide_Leg_Pants\07_Customer_Delivery_Guide"
OUT_BRAIN_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0"

# Sizes that share the identical 4-sheet A0 Copyshop grid
ORDERED_SIZES = [
    ("US_00", "US 00 (XXS)", (0.15, 0.25, 0.45)),  # Deep Navy
    ("US_0",  "US 0 (XS)",   (0.70, 0.15, 0.20)),  # Crimson
    ("US_2",  "US 2 (XS)",   (0.18, 0.45, 0.25)),  # Forest Green
    ("US_4",  "US 4 (S)",    (0.50, 0.15, 0.60)),  # Royal Purple
    ("US_6",  "US 6 (S)",    (0.80, 0.40, 0.10)),  # Burnt Orange
    ("US_8",  "US 8 (M)",    (0.10, 0.50, 0.55)),  # Teal
    ("US_10", "US 10 (M)",   (0.75, 0.15, 0.45)),  # Magenta
    ("US_14", "US 14 (L)",   (0.25, 0.25, 0.25)),  # Charcoal
    ("US_16", "US 16 (XL)",  (0.30, 0.45, 0.65)),  # Slate Blue
    ("US_18", "US 18 (2XL)", (0.65, 0.30, 0.15)),  # Rust Amber
]


def build_a0_layered():
    print("\n--- BUILDING MULTI-SIZE LAYERED A0 PDF ---")
    doc_out = pymupdf.open()
    
    # 1. Base Document Structure: Copy Pages 1, 2, 3 from Size US 0 as the Base Overview & Calibration
    ref_file = os.path.join(A0_DIR, "SewLuxe_Wide_Leg_Pants_Size_US_0_A0.pdf")
    doc_ref = pymupdf.open(ref_file)
    
    # Page 1: Calibration Test Page (Locked Base Layer)
    p1 = doc_out.new_page(width=doc_ref[0].rect.width, height=doc_ref[0].rect.height)
    p1.show_pdf_page(p1.rect, doc_ref, pno=0)
    
    # Page 2: Sizing & Layers Guide
    p2 = doc_out.new_page(width=doc_ref[1].rect.width, height=doc_ref[1].rect.height)
    p2.show_pdf_page(p2.rect, doc_ref, pno=1)
    
    # Page 3: Assembly Diagram
    p3 = doc_out.new_page(width=doc_ref[2].rect.width, height=doc_ref[2].rect.height)
    p3.show_pdf_page(p3.rect, doc_ref, pno=2)
    
    # Pages 4, 5, 6, 7: The 4 Master A0 Sheets (2x2 grid)
    # Sheet dimensions: 2383.94 x 3370.39 pt
    a0_w, a0_h = 2383.94, 3370.39
    
    for _ in range(4):
        doc_out.new_page(width=a0_w, height=a0_h)
        
    # Create OCG Layers for each size
    print(f"Creating OCG layers for {len(ORDERED_SIZES)} sizes...")
    for s_code, s_label, s_color in ORDERED_SIZES:
        src_file = os.path.join(A0_DIR, f"SewLuxe_Wide_Leg_Pants_Size_{s_code}_A0.pdf")
        if not os.path.exists(src_file):
            print(f"  Warning: {src_file} not found, skipping.")
            continue
            
        src_doc = pymupdf.open(src_file)
        if len(src_doc) < 7:
            print(f"  Warning: {src_file} has {len(src_doc)} pages (expected 7), skipping.")
            continue
            
        # Add OCG Layer for this size
        ocg_xref = doc_out.add_ocg(s_label)
        
        # Overlay each of the 4 A0 sheets (Pages 3, 4, 5, 6 in 0-indexed)
        for sheet_idx in range(4):
            target_page = doc_out[3 + sheet_idx]
            target_page.show_pdf_page(
                target_page.rect,
                src_doc,
                pno=3 + sheet_idx,
                keep_proportion=True,
                overlay=True,
                oc=ocg_xref
            )
        print(f"  Added OCG Layer: {s_label} (xref {ocg_xref})")
        
    doc_out.save(OUT_A0_LAYERED, deflate=True)
    print(f"[SUCCESS] Saved Layered A0 PDF to: {OUT_A0_LAYERED}")
    
    # Copy to customer delivery directory
    out_delivery_a0 = os.path.join(OUT_DESKTOP_GUIDE_DIR, "Margot_Wide_Leg_Pants_A0_ALL_SIZES_LAYERED.pdf")
    doc_out.save(out_delivery_a0, deflate=True)
    doc_out.save(os.path.join(OUT_BRAIN_DIR, "Margot_Wide_Leg_Pants_A0_ALL_SIZES_LAYERED.pdf"), deflate=True)


def build_projector_file():
    print("\n--- BUILDING DEDICATED PROJECTOR FILE (LAYERED PDF) ---")
    doc_out = pymupdf.open()
    
    # Canvas for Projector: Wide Unified Format (2400 x 3400 pt)
    P_WIDTH = 2400.0
    P_HEIGHT = 3400.0
    
    # =========================================================
    # PAGE 1: PROJECTOR CALIBRATION & ALIGNMENT PAGE
    # =========================================================
    print("Building Page 1: High-Contrast Calibration & Lens Alignment...")
    p1 = doc_out.new_page(width=P_WIDTH, height=P_HEIGHT)
    
    # Light neutral background
    p1.draw_rect(p1.rect, color=None, fill=(0.98, 0.98, 0.98), overlay=False)
    
    # Calibration Grid: 1-inch (72 pt) grid lines
    c_grid = (0.82, 0.82, 0.82)
    c_bold_grid = (0.50, 0.50, 0.50)
    
    # Vertical grid lines every 1 inch (72 pt)
    for x in range(0, int(P_WIDTH), 72):
        is_major = (x % 360 == 0)
        p1.draw_line(
            pymupdf.Point(x, 0),
            pymupdf.Point(x, P_HEIGHT),
            color=c_bold_grid if is_major else c_grid,
            width=1.5 if is_major else 0.6
        )
        if is_major and x > 0:
            p1.insert_text(pymupdf.Point(x + 4, 30), f"{x // 72}\"", fontsize=14, color=(0.2, 0.2, 0.2))
            
    # Horizontal grid lines every 1 inch (72 pt)
    for y in range(0, int(P_HEIGHT), 72):
        is_major = (y % 360 == 0)
        p1.draw_line(
            pymupdf.Point(0, y),
            pymupdf.Point(P_WIDTH, y),
            color=c_bold_grid if is_major else c_grid,
            width=1.5 if is_major else 0.6
        )
        if is_major and y > 0:
            p1.insert_text(pymupdf.Point(30, y - 4), f"{y // 72}\"", fontsize=14, color=(0.2, 0.2, 0.2))
            
    # Center Crosshair & Calibration Target
    center_x = P_WIDTH / 2
    center_y = P_HEIGHT / 2
    
    # Center 4"x4" Calibration Square (288 x 288 pt)
    sq_size = 288.0
    sq_rect = pymupdf.Rect(center_x - sq_size/2, center_y - sq_size/2, center_x + sq_size/2, center_y + sq_size/2)
    p1.draw_rect(sq_rect, color=(0.1, 0.1, 0.1), fill=(1.0, 1.0, 1.0), width=3.5)
    
    # Inner 10cm x 10cm Metric Square (283.46 x 283.46 pt)
    m_size = 283.46
    m_rect = pymupdf.Rect(center_x - m_size/2, center_y - m_size/2, center_x + m_size/2, center_y + m_size/2)
    p1.draw_rect(m_rect, color=(0.8, 0.2, 0.2), width=2.0, dashes="[8 4] 0")
    
    # Center Crosshairs
    p1.draw_line(pymupdf.Point(center_x - 300, center_y), pymupdf.Point(center_x + 300, center_y), color=(0.1, 0.1, 0.1), width=2.0)
    p1.draw_line(pymupdf.Point(center_x, center_y - 300), pymupdf.Point(center_x, center_y + 300), color=(0.1, 0.1, 0.1), width=2.0)
    p1.draw_circle(pymupdf.Point(center_x, center_y), 36.0, color=(0.1, 0.1, 0.1), width=2.5)
    
    # Calibration Info Text inside Target Box
    p1.insert_text(pymupdf.Point(center_x - 120, center_y - 90), "SEWLUXE PROJECTOR CALIBRATION", fontsize=16, color=(0.1, 0.1, 0.1))
    p1.insert_text(pymupdf.Point(center_x - 100, center_y - 65), "OUTER BOX: 4 in x 4 in (101.6 mm)", fontsize=13, color=(0.1, 0.1, 0.1))
    p1.insert_text(pymupdf.Point(center_x - 100, center_y - 45), "RED DASHED: 10 cm x 10 cm (Metric)", fontsize=13, color=(0.8, 0.2, 0.2))
    p1.insert_text(pymupdf.Point(center_x - 110, center_y + 60), "1. Set Adobe Zoom to 100% (Actual Size)", fontsize=13, color=(0.2, 0.2, 0.2))
    p1.insert_text(pymupdf.Point(center_x - 110, center_y + 80), "2. Measure square with physical ruler", fontsize=13, color=(0.2, 0.2, 0.2))
    p1.insert_text(pymupdf.Point(center_x - 110, center_y + 100), "3. Toggle size layers in Left Panel", fontsize=13, color=(0.2, 0.2, 0.2))
    
    # Header Banner
    p1.insert_text(pymupdf.Point(80, 80), "SEWLUXE PATTERNS · DEDICATED PROJECTOR FILE", fontsize=28, color=(0.15, 0.22, 0.15))
    p1.insert_text(pymupdf.Point(80, 115), "Margot Elastic Wide-Leg Pants · Ultra-Thick High-Contrast Vector Lines · Full Size Range", fontsize=16, color=(0.4, 0.4, 0.4))

    # =========================================================
    # PAGE 2: MASTER UNIFIED PROJECTOR PATTERN WITH OCG LAYERS
    # =========================================================
    print("Building Page 2: Master Pattern Projection Canvas with Size Layers...")
    p2 = doc_out.new_page(width=P_WIDTH, height=P_HEIGHT)
    p2.draw_rect(p2.rect, color=None, fill=(0.99, 0.99, 0.99), overlay=False)
    
    # Add Layer 00: Projection Grid (Toggleable)
    ocg_grid = doc_out.add_ocg("00 - Projection Calibration Grid (1-inch)")
    # Draw subtle 1-inch grid under pattern
    for x in range(0, int(P_WIDTH), 72):
        p2.draw_line(pymupdf.Point(x, 0), pymupdf.Point(x, P_HEIGHT), color=(0.88, 0.88, 0.88), width=0.5, oc=ocg_grid)
    for y in range(0, int(P_HEIGHT), 72):
        p2.draw_line(pymupdf.Point(0, y), pymupdf.Point(P_WIDTH, y), color=(0.88, 0.88, 0.88), width=0.5, oc=ocg_grid)
        
    # Calibration Square on Page 2 for immediate verification
    p2.draw_rect(pymupdf.Rect(80, 80, 80 + 288, 80 + 288), color=(0.1, 0.1, 0.1), fill=(1.0, 1.0, 1.0), width=3.0, oc=ocg_grid)
    p2.insert_text(pymupdf.Point(100, 160), "4\" x 4\" TEST SQUARE", fontsize=14, color=(0.1, 0.1, 0.1), oc=ocg_grid)
    p2.insert_text(pymupdf.Point(100, 190), "10 cm x 10 cm", fontsize=14, color=(0.1, 0.1, 0.1), oc=ocg_grid)
    
    # Overlay pattern sizes as individual OCG Layers
    for s_code, s_label, s_color in ORDERED_SIZES:
        src_file = os.path.join(A0_DIR, f"SewLuxe_Wide_Leg_Pants_Size_{s_code}_A0.pdf")
        if not os.path.exists(src_file):
            continue
            
        src_doc = pymupdf.open(src_file)
        if len(src_doc) < 4:
            continue
            
        ocg_size = doc_out.add_ocg(s_label)
        p2_active = doc_out[1]
        
        # We overlay the master A0 sheet (Page 4, index 3) scaled and centered on the projector canvas
        p2_active.show_pdf_page(
            pymupdf.Rect(50, 50, P_WIDTH - 50, P_HEIGHT - 50),
            src_doc,
            pno=3,
            keep_proportion=True,
            overlay=True,
            oc=ocg_size
        )
        print(f"  Added Projector Size Layer: {s_label}")
        
    doc_out.save(OUT_PROJECTOR, deflate=True)
    print(f"[SUCCESS] Saved Projector File to: {OUT_PROJECTOR}")
    
    out_delivery_proj = os.path.join(OUT_DESKTOP_GUIDE_DIR, "Margot_Elastic_Wide_Leg_Pants_Projector_File.pdf")
    doc_out.save(out_delivery_proj, deflate=True)
    doc_out.save(os.path.join(OUT_BRAIN_DIR, "Margot_Elastic_Wide_Leg_Pants_Projector_File.pdf"), deflate=True)


if __name__ == "__main__":
    build_a0_layered()
    build_projector_file()
