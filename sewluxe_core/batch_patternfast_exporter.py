"""
Batch PatternFast Exporter & Packager (محرك التصدير الجماعي للباترونات)
====================================================================
Phase 2 Automated Engine:
- Downloads all 13 sizes (US 00 to US 22) across 3 formats (A4, US Letter, A0) = 39 PDFs.
- Applies authentic SewLuxePatterns white-labeling and PDF metadata.
- Packages 3 clean Etsy Customer Delivery ZIP archives.
- Updates SewLuxePipelineGuard state.
"""

import os
import sys
import json
import re
import zipfile
import shutil
import urllib.request
import urllib.parse
import pymupdf as fitz
from typing import Dict, List, Any

# Windows terminal UTF-8 encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SIZE_META = [
    ("00", "US_00", "US 00 (XXS)"),
    ("0",  "US_0",  "US 0 (XS)"),
    ("2",  "US_2",  "US 2 (XS)"),
    ("4",  "US_4",  "US 4 (S)"),
    ("6",  "US_6",  "US 6 (S)"),
    ("8",  "US_8",  "US 8 (M)"),
    ("10", "US_10", "US 10 (M)"),
    ("12", "US_12", "US 12 (L)"),
    ("14", "US_14", "US 14 (L)"),
    ("16", "US_16", "US 16 (XL)"),
    ("18", "US_18", "US 18 (2XL)"),
    ("20", "US_20", "US 20 (3XL)"),
    ("22", "US_22", "US 22 (4XL)")
]

def whitelabel_pattern_pdf(in_pdf_path: str, out_pdf_path: str, garment_title: str, size_label: str, fmt_label: str):
    doc = fitz.open(in_pdf_path)
    
    # Strip PatternFast top banner and replace with SewLuxe luxury branding on pages 0, 1, 3
    for pno in [0, 1, 3]:
        if pno >= len(doc):
            continue
        page = doc[pno]
        xrefs = page.get_contents()
        if not xrefs:
            continue
        raw = doc.xref_stream(xrefs[0])
        raw_new = re.sub(
            rb"q\n1 0 0 1 0 28\.3465 cm\n0\.75 0 0 0\.75 0 0 cm\nq\n0 0 m\n793\.706667 0 l\n793\.706667 48 l\n0 48 l\nh\nW n\n2 0 0 2 275\.853333 0 cm\nq.*?Q\nQ\nQ\n",
            rb"",
            raw,
            count=1,
            flags=re.S
        )
        doc.update_stream(xrefs[0], raw_new)

        page.insert_text(
            fitz.Point(214.83, 841.89 - 791.54),
            "SewLuxePatterns",
            fontname="hebo",
            fontsize=20,
            color=(0.12, 0.12, 0.12)
        )
        page.insert_text(
            fitz.Point(262.285, 841.89 - 779.54),
            "SEWING PATTERNS",
            fontname="helv",
            fontsize=7.5,
            color=(0.4, 0.4, 0.4)
        )

    # Standardized metadata
    meta = {
        "author": "SewLuxePatterns",
        "creator": "SewLuxe Engineering Studio",
        "producer": "SewLuxe High-Precision CAD Engine",
        "title": f"SewLuxe Pattern - {garment_title} - {size_label} ({fmt_label})",
        "subject": "Women's High-Rise Minimalist Wide-Leg Pants PDF Sewing Pattern"
    }
    doc.set_metadata(meta)
    os.makedirs(os.path.dirname(os.path.abspath(out_pdf_path)), exist_ok=True)
    doc.save(out_pdf_path, garbage=4, deflate=True)
    doc.close()

def run_batch_export(
    project_dir: str,
    garment_title: str,
    garment_file_slug: str,
    elem_ids: str = "3833,4355",
    setting_codes: str = "pants_slits:no_slits",
    token: str = None,
    mannequins: List[Dict[str, Any]] = None,
    desktop_dir: str = None
):
    print("=" * 80)
    print(f"SEWLUXE PHASE 2: BATCH PATTERN EXPORT & PACKAGING")
    print(f"Garment: {garment_title}")
    print("=" * 80)

    pattern_suite_dir = os.path.join(project_dir, "03_Pattern_Suite")
    dir_a4 = os.path.join(pattern_suite_dir, "A4")
    dir_letter = os.path.join(pattern_suite_dir, "US_Letter")
    dir_a0 = os.path.join(pattern_suite_dir, "A0")
    dir_raw = os.path.join(pattern_suite_dir, "raw_downloads")

    for d in [dir_a4, dir_letter, dir_a0, dir_raw]:
        os.makedirs(d, exist_ok=True)

    # Map mannequins by size name
    man_map = {m["name"]: m["mannequinId"] for m in mannequins}

    formats = [
        ("A4", dir_a4, "A4"),
        ("LETTER", dir_letter, "US_Letter"),
        ("A0", dir_a0, "A0")
    ]

    total_downloaded = 0

    for raw_sz, sz_code, sz_title in SIZE_META:
        if raw_sz not in man_map:
            print(f"[WARN] Size {raw_sz} not found in mannequins map! Skipping.")
            continue
        
        mid = man_map[raw_sz]
        print(f"\n---> Processing Size: {raw_sz} ({sz_title}) [ID: {mid[:8]}...] ...")

        # 1. Fetch parameterized kits
        qs = urllib.parse.urlencode({
            "elemIds": elem_ids,
            "mannequinId": mid,
            "fabricType": "1",
            "fit": "2",
            "seamAllowance": "0",
            "eases": "",
            "settingCodes": setting_codes,
            "fontName": "DM Sans",
            "debug_params": "1",
            "view": "2",
            "format": "json"
        })
        prev_url = f"https://api.patternfast.com/api/patterns/preview?{qs}"
        req_prev = urllib.request.Request(prev_url, headers={
            "Authorization": token,
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0"
        })

        try:
            with urllib.request.urlopen(req_prev) as resp:
                prev_data = json.loads(resp.read().decode())
            param_kits = prev_data["parameterizedKits"]
        except Exception as e:
            print(f"  [ERROR] Failed to fetch preview for size {raw_sz}: {e}")
            continue

        # 2. Download all 3 formats
        for api_fmt, dest_dir, fmt_label in formats:
            clean_filename = f"{garment_file_slug}_Size_{sz_code}_{fmt_label}.pdf"
            clean_filepath = os.path.join(dest_dir, clean_filename)
            raw_filepath = os.path.join(dir_raw, f"raw_{sz_code}_{api_fmt}.pdf")

            dl_payload = {
                "mannequinId": mid,
                **param_kits,
                "cutVerticallySymmetric": False,
                "pageSize": api_fmt
            }
            req_dl = urllib.request.Request(
                "https://api.patternfast.com/api/cat/download-pdf",
                data=json.dumps(dl_payload).encode("utf-8"),
                headers={
                    "Authorization": token,
                    "Content-Type": "application/json; charset=UTF-8",
                    "User-Agent": "Mozilla/5.0"
                }
            )

            try:
                with urllib.request.urlopen(req_dl) as resp:
                    pdf_bytes = resp.read()
                with open(raw_filepath, "wb") as rf:
                    rf.write(pdf_bytes)

                # White-label
                whitelabel_pattern_pdf(raw_filepath, clean_filepath, garment_title, sz_title, fmt_label)
                size_kb = os.path.getsize(clean_filepath) // 1024
                print(f"  [OK] {clean_filename} ({size_kb} KB)")
                total_downloaded += 1
            except Exception as e:
                print(f"  [ERROR] Failed to download {api_fmt} for size {raw_sz}: {e}")

    print("\n" + "=" * 80)
    print(f" Successfully exported and white-labeled {total_downloaded}/39 pattern PDFs! ")
    print("=" * 80)

    # 3. Build the 3 Customer Delivery ZIP archives
    print("\nPackaging Etsy Customer Delivery ZIP Archives...")
    zip_a4 = os.path.join(pattern_suite_dir, f"{garment_file_slug}_A4_Print_at_Home_All_Sizes.zip")
    zip_letter = os.path.join(pattern_suite_dir, f"{garment_file_slug}_US_Letter_Print_at_Home_All_Sizes.zip")
    zip_a0 = os.path.join(pattern_suite_dir, f"{garment_file_slug}_A0_Copyshop_All_Sizes.zip")

    zips_to_build = [
        (dir_a4, zip_a4, "A4"),
        (dir_letter, zip_letter, "US_Letter"),
        (dir_a0, zip_a0, "A0")
    ]

    for source_dir, zip_dest, label in zips_to_build:
        with zipfile.ZipFile(zip_dest, "w", zipfile.ZIP_DEFLATED) as zf:
            for fn in sorted(os.listdir(source_dir)):
                if fn.endswith(".pdf"):
                    zf.write(os.path.join(source_dir, fn), f"{label}/{fn}")
        zip_mb = os.path.getsize(zip_dest) / (1024 * 1024)
        print(f"  [ZIP CREATED] {os.path.basename(zip_dest)} ({zip_mb:.2f} MB)")

    # 4. Sync to Desktop if specified
    if desktop_dir:
        desktop_suite = os.path.join(desktop_dir, "03_Pattern_Suite")
        print(f"\nSyncing pattern suite to Desktop: {desktop_suite}...")
        os.makedirs(desktop_suite, exist_ok=True)
        for z in [zip_a4, zip_letter, zip_a0]:
            shutil.copy2(z, os.path.join(desktop_suite, os.path.basename(z)))
            print(f"  [DESKTOP SYNC] {os.path.basename(z)}")

    print("\n[PHASE 2 COMPLETED 100%]")
    return total_downloaded

if __name__ == "__main__":
    BRAIN_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0"
    with open(os.path.join(BRAIN_DIR, "auth_token.txt"), "r", encoding="utf-8") as f:
        auth_tok = f.read().strip()

    with open(os.path.join(BRAIN_DIR, "scratch", "mannequins.json"), "r", encoding="utf-8") as f:
        mans = json.load(f)

    proj_dir = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\projects\trendy_high_waist_wide_leg"
    desk_dir = r"C:\Users\red1e\Desktop\SewLuxe_Aria_Trendy_Wide_Leg_Pants"

    # Verify pipeline gate first
    from sewluxe_core.sewluxe_pipeline_guard import SewLuxePipelineGuard
    guard = SewLuxePipelineGuard(proj_dir)
    guard.verify_gate("PHASE_2_BATCH_PATTERN_EXPORT")

    count = run_batch_export(
        project_dir=proj_dir,
        garment_title="Aria Trendy Wide-Leg Pants",
        garment_file_slug="SewLuxe_Aria_Wide_Leg_Pants",
        elem_ids="3833,4355",
        setting_codes="pants_slits:no_slits",
        token=auth_tok,
        mannequins=mans,
        desktop_dir=desk_dir
    )

    if count == 39:
        guard.complete_phase("PHASE_2_BATCH_PATTERN_EXPORT", "All 39 PDFs exported, white-labeled, and packaged into 3 ZIPs.")
        print("\nPipeline status updated successfully:")
        guard.print_status_dashboard()
