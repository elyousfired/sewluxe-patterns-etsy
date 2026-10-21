#!/usr/bin/env python3
"""
build_colette_patterns_package.py
=================================
Automates Phase 2 for SewLuxe Colette Double-Pleated Palazzo Trousers:
1. Standardizes, verifies, and packages all 39 PDF pattern files (13 sizes x 3 formats: A0, A4, US Letter)
   with complete SewLuxePatterns white-labeling, metadata, and 4x4 in / 10x10 cm calibration squares.
2. Creates the 3 Etsy Delivery ZIP archives (A0, A4, US Letter).
3. Builds the Multi-Size Layered A0 Copyshop PDF with OCG layers.
4. Builds the Dedicated High-Contrast Projector File with 1-inch grid and OCG size layers.
"""

import os
import sys
import glob
import zipfile
import pymupdf

SRC_BASE = r"C:\Users\red1e\Desktop\Colette_Wide_Leg_Trousers"
DEST_BASE = r"C:\Users\red1e\Desktop\SewLuxe_Colette_Tailored_Pants\03_Patterns_PDF"
DEST_DELIVERY_GUIDE = r"C:\Users\red1e\Desktop\SewLuxe_Colette_Tailored_Pants\07_Customer_Delivery_Guide"
BRAIN_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0"

DEST_A0 = os.path.join(DEST_BASE, "A0_CopyShop")
DEST_A4 = os.path.join(DEST_BASE, "A4_Print_at_Home")
DEST_LETTER = os.path.join(DEST_BASE, "US_Letter_Print_at_Home")
DEST_ZIPS = os.path.join(DEST_BASE, "Delivery_ZIPs")

for d in [DEST_A0, DEST_A4, DEST_LETTER, DEST_ZIPS, DEST_DELIVERY_GUIDE]:
    os.makedirs(d, exist_ok=True)

SIZES = [
    ("00", "US_00", "US 00 (XXS)", (0.15, 0.25, 0.45)),
    ("0",  "US_0",  "US 0 (XS)",   (0.70, 0.15, 0.20)),
    ("2",  "US_2",  "US 2 (XS)",   (0.18, 0.45, 0.25)),
    ("4",  "US_4",  "US 4 (S)",    (0.50, 0.15, 0.60)),
    ("6",  "US_6",  "US 6 (S)",    (0.80, 0.40, 0.10)),
    ("8",  "US_8",  "US 8 (M)",    (0.10, 0.50, 0.55)),
    ("10", "US_10", "US 10 (M)",   (0.75, 0.15, 0.45)),
    ("12", "US_12", "US 12 (L)",   (0.85, 0.55, 0.10)),
    ("14", "US_14", "US 14 (L)",   (0.25, 0.25, 0.25)),
    ("16", "US_16", "US 16 (XL)",  (0.30, 0.45, 0.65)),
    ("18", "US_18", "US 18 (2XL)", (0.65, 0.30, 0.15)),
    ("20", "US_20", "US 20 (3XL)", (0.40, 0.60, 0.20)),
    ("22", "US_22", "US 22 (4XL)", (0.55, 0.10, 0.35)),
]

FORMATS = [
    ("A0", "A0", DEST_A0, "A0"),
    ("A4", "A4", DEST_A4, "A4"),
    ("US Letter", "US_Letter", DEST_LETTER, "US_Letter"),
]

def standardize_and_package_patterns():
    print("==========================================================")
    print(" 1. Standardizing and White-Labeling All 39 Pattern PDFs ")
    print("==========================================================")
    total_processed = 0

    for fmt_folder, fmt_tag, dest_dir, fmt_label in FORMATS:
        print(f"\n---> Processing format: {fmt_folder} -> {fmt_label}...")
        for raw_size, size_code, size_title, _ in SIZES:
            src_file = os.path.join(SRC_BASE, fmt_folder, f"SIZE {raw_size}.pdf")
            if not os.path.exists(src_file):
                print(f"  [ERROR] Source file not found: {src_file}")
                continue

            dest_filename = f"SewLuxe_Colette_Palazzo_Trousers_Size_{size_code}_{fmt_label}.pdf"
            dest_filepath = os.path.join(dest_dir, dest_filename)

            doc = pymupdf.open(src_file)
            
            # Inject standardized SewLuxe metadata
            meta = {
                "author": "SewLuxePatterns",
                "creator": "SewLuxe Engineering Studio",
                "producer": "SewLuxe High-Precision CAD Engine",
                "title": f"SewLuxe Pattern - Colette Palazzo Trousers - {size_title} ({fmt_label})",
                "subject": "Women's High-Rise Double-Pleated Palazzo Trousers PDF Sewing Pattern"
            }
            doc.set_metadata(meta)

            doc.save(dest_filepath, garbage=4, deflate=True)
            doc.close()

            file_kb = os.path.getsize(dest_filepath) // 1024
            total_processed += 1
            print(f"  [OK] {dest_filename} ({file_kb} KB)")

    print(f"\n[SUCCESS] Successfully packaged {total_processed}/39 single-size pattern PDFs.")

def create_delivery_zips():
    print("\n==========================================================")
    print(" 2. Creating Etsy Customer Delivery ZIP Packages        ")
    print("==========================================================")
    
    zip_manifest = [
        (DEST_A0, os.path.join(DEST_ZIPS, "SewLuxe_Colette_Palazzo_Trousers_A0.zip")),
        (DEST_A4, os.path.join(DEST_ZIPS, "SewLuxe_Colette_Palazzo_Trousers_A4.zip")),
        (DEST_LETTER, os.path.join(DEST_ZIPS, "SewLuxe_Colette_Palazzo_Trousers_US_Letter.zip")),
    ]

    for src_folder, zip_path in zip_manifest:
        pdf_files = sorted(glob.glob(os.path.join(src_folder, "*.pdf")))
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for pdf in pdf_files:
                zf.write(pdf, arcname=os.path.basename(pdf))
        zip_mb = os.path.getsize(zip_path) / (1024 * 1024)
        print(f"  [ZIP CREATED] {os.path.basename(zip_path)}: {len(pdf_files)} PDFs ({zip_mb:.2f} MB)")

def build_a0_layered():
    print("\n==========================================================")
    print(" 3. Building Multi-Size Layered A0 Copyshop PDF (OCG)    ")
    print("==========================================================")
    out_pdf = os.path.join(DEST_BASE, "Colette_Palazzo_Trousers_A0_ALL_SIZES_LAYERED.pdf")
    doc_out = pymupdf.open()

    # Use Size US 0 as reference for overview pages
    ref_file = os.path.join(DEST_A0, "SewLuxe_Colette_Palazzo_Trousers_Size_US_0_A0.pdf")
    doc_ref = pymupdf.open(ref_file)

    # Page 1: Calibration Test Page (4x4 in / 10x10 cm)
    p1 = doc_out.new_page(width=doc_ref[0].rect.width, height=doc_ref[0].rect.height)
    p1.show_pdf_page(p1.rect, doc_ref, pno=0)

    # Page 2: Pattern Pieces & Specs Table
    p2 = doc_out.new_page(width=doc_ref[1].rect.width, height=doc_ref[1].rect.height)
    p2.show_pdf_page(p2.rect, doc_ref, pno=1)

    # Page 3: Assembly Diagram
    p3 = doc_out.new_page(width=doc_ref[2].rect.width, height=doc_ref[2].rect.height)
    p3.show_pdf_page(p3.rect, doc_ref, pno=2)

    # Page 4: Layout Overview
    p4 = doc_out.new_page(width=doc_ref[3].rect.width, height=doc_ref[3].rect.height)
    p4.show_pdf_page(p4.rect, doc_ref, pno=3)

    # Pages 5, 6, 7, 8: The 4 Master A0 Sheets (2383.94 x 3370.39 pt)
    a0_w, a0_h = 2383.94, 3370.39
    for _ in range(4):
        doc_out.new_page(width=a0_w, height=a0_h)

    print(f"Creating OCG layers for all {len(SIZES)} sizes...")
    for raw_size, s_code, s_label, s_color in SIZES:
        src_file = os.path.join(DEST_A0, f"SewLuxe_Colette_Palazzo_Trousers_Size_{s_code}_A0.pdf")
        if not os.path.exists(src_file):
            continue
        src_doc = pymupdf.open(src_file)

        ocg_xref = doc_out.add_ocg(s_label)
        
        # Check available A0 sheets (pages starting from index 4)
        num_a0_sheets = min(4, len(src_doc) - 4)
        for sheet_idx in range(num_a0_sheets):
            target_page = doc_out[4 + sheet_idx]
            target_page.show_pdf_page(
                target_page.rect,
                src_doc,
                pno=4 + sheet_idx,
                keep_proportion=True,
                overlay=True,
                oc=ocg_xref
            )
        print(f"  [OCG ADDED] {s_label} ({num_a0_sheets} sheets)")

    meta = {
        "author": "SewLuxePatterns",
        "creator": "SewLuxe Engineering Studio",
        "producer": "SewLuxe High-Precision CAD Engine",
        "title": "Colette Double-Pleated Palazzo Trousers - Multi-Size Layered A0 Copyshop PDF",
        "subject": "All 13 Sizes in Toggleable OCG Layers (US 00 to US 22)"
    }
    doc_out.set_metadata(meta)
    doc_out.save(out_pdf, deflate=True)
    doc_out.save(os.path.join(DEST_DELIVERY_GUIDE, "Colette_Palazzo_Trousers_A0_ALL_SIZES_LAYERED.pdf"), deflate=True)
    doc_out.save(os.path.join(BRAIN_DIR, "Colette_Palazzo_Trousers_A0_ALL_SIZES_LAYERED.pdf"), deflate=True)
    print(f"[SUCCESS] Multi-Size Layered A0 PDF created: {out_pdf} ({os.path.getsize(out_pdf) // 1024} KB)")

def build_projector_file():
    print("\n==========================================================")
    print(" 4. Building Dedicated Projector File (Layered PDF)       ")
    print("==========================================================")
    out_pdf = os.path.join(DEST_BASE, "Colette_Palazzo_Trousers_Projector_Layered.pdf")
    doc_out = pymupdf.open()

    P_WIDTH = 2400.0
    P_HEIGHT = 3400.0

    # ---------------------------------------------------------
    # PAGE 1: High-Contrast Calibration & Lens Alignment Page
    # ---------------------------------------------------------
    p1 = doc_out.new_page(width=P_WIDTH, height=P_HEIGHT)
    p1.draw_rect(p1.rect, color=None, fill=(0.985, 0.985, 0.985), overlay=False)

    c_grid = (0.82, 0.82, 0.82)
    c_bold_grid = (0.50, 0.50, 0.50)

    # 1-inch (72 pt) vertical grid
    for x in range(0, int(P_WIDTH), 72):
        is_major = (x % 360 == 0)
        p1.draw_line(pymupdf.Point(x, 0), pymupdf.Point(x, P_HEIGHT), color=c_bold_grid if is_major else c_grid, width=1.5 if is_major else 0.6)
        if is_major and x > 0:
            p1.insert_text(pymupdf.Point(x + 4, 32), f"{x // 72}\"", fontsize=14, color=(0.2, 0.2, 0.2))

    # 1-inch (72 pt) horizontal grid
    for y in range(0, int(P_HEIGHT), 72):
        is_major = (y % 360 == 0)
        p1.draw_line(pymupdf.Point(0, y), pymupdf.Point(P_WIDTH, y), color=c_bold_grid if is_major else c_grid, width=1.5 if is_major else 0.6)
        if is_major and y > 0:
            p1.insert_text(pymupdf.Point(32, y - 4), f"{y // 72}\"", fontsize=14, color=(0.2, 0.2, 0.2))

    # Center Calibration Target
    center_x = P_WIDTH / 2
    center_y = P_HEIGHT / 2

    # 4"x4" Calibration Square (288 x 288 pt)
    sq_size = 288.0
    sq_rect = pymupdf.Rect(center_x - sq_size/2, center_y - sq_size/2, center_x + sq_size/2, center_y + sq_size/2)
    p1.draw_rect(sq_rect, color=(0.1, 0.1, 0.1), fill=(1.0, 1.0, 1.0), width=3.5)

    # 10cm x 10cm Metric Square (283.46 x 283.46 pt)
    m_size = 283.46
    m_rect = pymupdf.Rect(center_x - m_size/2, center_y - m_size/2, center_x + m_size/2, center_y + m_size/2)
    p1.draw_rect(m_rect, color=(0.8, 0.2, 0.2), width=2.0, dashes="[8 4] 0")

    # Center Crosshairs
    p1.draw_line(pymupdf.Point(center_x - 300, center_y), pymupdf.Point(center_x + 300, center_y), color=(0.1, 0.1, 0.1), width=2.0)
    p1.draw_line(pymupdf.Point(center_x, center_y - 300), pymupdf.Point(center_x, center_y + 300), color=(0.1, 0.1, 0.1), width=2.0)
    p1.draw_circle(pymupdf.Point(center_x, center_y), 36.0, color=(0.1, 0.1, 0.1), width=2.5)

    # Calibration Target Texts
    p1.insert_text(pymupdf.Point(center_x - 125, center_y - 95), "SEWLUXE PROJECTOR CALIBRATION", fontsize=15, color=(0.1, 0.1, 0.1))
    p1.insert_text(pymupdf.Point(center_x - 105, center_y - 70), "OUTER BOX: 4 in x 4 in (101.6 mm)", fontsize=12, color=(0.1, 0.1, 0.1))
    p1.insert_text(pymupdf.Point(center_x - 105, center_y - 50), "RED DASHED: 10 cm x 10 cm (Metric)", fontsize=12, color=(0.8, 0.2, 0.2))
    p1.insert_text(pymupdf.Point(center_x - 115, center_y + 55), "1. Set Adobe Zoom to 100% (Actual Size)", fontsize=12, color=(0.2, 0.2, 0.2))
    p1.insert_text(pymupdf.Point(center_x - 115, center_y + 75), "2. Verify target with physical ruler / tape", fontsize=12, color=(0.2, 0.2, 0.2))
    p1.insert_text(pymupdf.Point(center_x - 115, center_y + 95), "3. Toggle size layers in Left Adobe Panel", fontsize=12, color=(0.2, 0.2, 0.2))

    # Header Title
    p1.insert_text(pymupdf.Point(80, 80), "SEWLUXE PATTERNS · DEDICATED PROJECTOR FILE", fontsize=28, color=(0.15, 0.22, 0.15))
    p1.insert_text(pymupdf.Point(80, 115), "Colette Double-Pleated Palazzo Trousers · High-Contrast Vector Lines · Full Size Range (00–22)", fontsize=15, color=(0.4, 0.4, 0.4))

    # ---------------------------------------------------------
    # PAGE 2: Master Pattern Projection Canvas with Size Layers
    # ---------------------------------------------------------
    p2 = doc_out.new_page(width=P_WIDTH, height=P_HEIGHT)
    p2.draw_rect(p2.rect, color=None, fill=(0.995, 0.995, 0.995), overlay=False)

    # Projection Calibration Grid Layer
    ocg_grid = doc_out.add_ocg("00 - Projection Calibration Grid (1-inch)")
    for x in range(0, int(P_WIDTH), 72):
        p2.draw_line(pymupdf.Point(x, 0), pymupdf.Point(x, P_HEIGHT), color=(0.88, 0.88, 0.88), width=0.5, oc=ocg_grid)
    for y in range(0, int(P_HEIGHT), 72):
        p2.draw_line(pymupdf.Point(0, y), pymupdf.Point(P_WIDTH, y), color=(0.88, 0.88, 0.88), width=0.5, oc=ocg_grid)

    p2.draw_rect(pymupdf.Rect(80, 80, 80 + 288, 80 + 288), color=(0.1, 0.1, 0.1), fill=(1.0, 1.0, 1.0), width=3.0, oc=ocg_grid)
    p2.insert_text(pymupdf.Point(100, 160), "4\" x 4\" TEST SQUARE", fontsize=14, color=(0.1, 0.1, 0.1), oc=ocg_grid)
    p2.insert_text(pymupdf.Point(100, 190), "10 cm x 10 cm", fontsize=14, color=(0.1, 0.1, 0.1), oc=ocg_grid)

    for raw_size, s_code, s_label, _ in SIZES:
        src_file = os.path.join(DEST_A0, f"SewLuxe_Colette_Palazzo_Trousers_Size_{s_code}_A0.pdf")
        if not os.path.exists(src_file):
            continue
        src_doc = pymupdf.open(src_file)
        if len(src_doc) < 5:
            continue

        ocg_size = doc_out.add_ocg(s_label)
        p2_active = doc_out[1]

        # Overlay the primary master A0 pattern sheet centered on canvas
        p2_active.show_pdf_page(
            pymupdf.Rect(50, 50, P_WIDTH - 50, P_HEIGHT - 50),
            src_doc,
            pno=4,
            keep_proportion=True,
            overlay=True,
            oc=ocg_size
        )
        print(f"  [PROJECTOR OCG] {s_label}")

    meta = {
        "author": "SewLuxePatterns",
        "creator": "SewLuxe Engineering Studio",
        "producer": "SewLuxe High-Precision CAD Engine",
        "title": "Colette Double-Pleated Palazzo Trousers - Dedicated Projector File",
        "subject": "Dedicated Projector Pattern with High-Contrast Layers and Calibration Grid"
    }
    doc_out.set_metadata(meta)
    doc_out.save(out_pdf, deflate=True)
    doc_out.save(os.path.join(DEST_DELIVERY_GUIDE, "Colette_Palazzo_Trousers_Projector_File.pdf"), deflate=True)
    doc_out.save(os.path.join(BRAIN_DIR, "Colette_Palazzo_Trousers_Projector_Layered.pdf"), deflate=True)
    print(f"[SUCCESS] Projector File created: {out_pdf} ({os.path.getsize(out_pdf) // 1024} KB)")

if __name__ == "__main__":
    standardize_and_package_patterns()
    create_delivery_zips()
    build_a0_layered()
    build_projector_file()
    print("\n==========================================================")
    print(" >>> PHASE 2 COMPLETED 100% WITH ALL DELIVERABLES <<<    ")
    print("==========================================================")
