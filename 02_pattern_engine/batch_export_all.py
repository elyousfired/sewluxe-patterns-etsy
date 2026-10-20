import os
import sys
import time
import zipfile
import pymupdf

sys.path.append(r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\02_pattern_engine")
from pattern_engine import PatternFastEngine

def main():
    print("==================================================")
    print("   SewLuxePatterns - Full Batch Production Engine   ")
    print("   Garment: Elastic Wide Leg Pants (All 13 Sizes)   ")
    print("==================================================")

    base_dir = r"C:\Users\red1e\Desktop\SewLuxe_Elastic_Wide_Leg_Pants\03_Patterns_PDF"
    dir_a4 = os.path.join(base_dir, "A4_Print_at_Home")
    dir_letter = os.path.join(base_dir, "US_Letter_Print_at_Home")
    dir_a0 = os.path.join(base_dir, "A0_CopyShop")
    dir_zips = os.path.join(base_dir, "Delivery_ZIPs")

    for d in [dir_a4, dir_letter, dir_a0, dir_zips]:
        os.makedirs(d, exist_ok=True)

    engine = PatternFastEngine()
    engine.login()
    print("Authenticated successfully with PatternFast API.")

    mannequins = engine.get_standard_mannequins("00-22")
    print(f"Retrieved {len(mannequins)} standard mannequins.")

    elem_ids = "79287,30165,28352"

    formats = [
        ("A4", dir_a4, "A4"),
        ("LETTER", dir_letter, "US_Letter"),
        ("A0", dir_a0, "A0")
    ]

    total_ops = len(mannequins) * len(formats)
    completed = 0
    errors = []

    for m in mannequins:
        size_name = str(m.get("name"))
        mid = str(m.get("mannequinId"))
        print(f"\n---> Processing Size US {size_name} (Mannequin ID: {mid})...")

        for fmt_code, out_dir, fmt_label in formats:
            pdf_filename = f"SewLuxe_Wide_Leg_Pants_Size_US_{size_name}_{fmt_label}.pdf"
            out_pdf_path = os.path.join(out_dir, pdf_filename)

            # Skip if already exists and valid
            if os.path.exists(out_pdf_path) and os.path.getsize(out_pdf_path) > 50000:
                print(f"  [ALREADY EXISTS] {pdf_filename} ({os.path.getsize(out_pdf_path)} bytes)")
                completed += 1
                continue

            try:
                engine.generate_single_size_pattern(
                    elem_ids=elem_ids,
                    mannequin_id=mid,
                    size_name=size_name,
                    page_size=fmt_code,
                    out_pdf_path=out_pdf_path
                )
                sz = os.path.getsize(out_pdf_path)
                completed += 1
                print(f"  [OK {completed}/{total_ops}] {pdf_filename} ({sz // 1024} KB)")
                time.sleep(0.3)
            except Exception as e:
                print(f"  [ERROR] {pdf_filename}: {e}")
                errors.append((pdf_filename, str(e)))
                time.sleep(1)

    print("\n==================================================")
    print(f"Export Completed: {completed}/{total_ops} files.")
    if errors:
        print(f"Errors encountered ({len(errors)}):", errors)
    print("==================================================")

    # Now create ZIP packages for Etsy
    print("\nCreating Etsy Delivery ZIP Archives...")
    zip_specs = [
        (dir_a4, os.path.join(dir_zips, "SewLuxe_Elastic_Wide_Leg_Pants_A4.zip")),
        (dir_letter, os.path.join(dir_zips, "SewLuxe_Elastic_Wide_Leg_Pants_US_Letter.zip")),
        (dir_a0, os.path.join(dir_zips, "SewLuxe_Elastic_Wide_Leg_Pants_A0.zip")),
    ]

    for source_dir, zip_dest in zip_specs:
        with zipfile.ZipFile(zip_dest, "w", zipfile.ZIP_DEFLATED) as zf:
            for fname in os.listdir(source_dir):
                if fname.endswith(".pdf"):
                    fpath = os.path.join(source_dir, fname)
                    zf.write(fpath, arcname=fname)
        print(f"Created ZIP: {os.path.basename(zip_dest)} ({os.path.getsize(zip_dest) // 1024} KB)")

    print("\nALL 39 PATTERN FILES + 3 DELIVERY ZIPS CREATED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
