import os
import shutil

src_root = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\projects\wide_leg_trousers_welt_pockets"
desktop_dest = r"C:\Users\red1e\Desktop\SewLuxe_Vivienne_Wide_Leg_Trousers"

os.makedirs(desktop_dest, exist_ok=True)

deliverables = [
    # 1. Booklet
    ("03_Sewing_Instruction_Booklet", os.path.join(src_root, "04_Booklet", "Vivienne_Wide_Leg_Trousers_Sewing_Instructions.pdf")),
    # 2. Photos
    ("01_Model_Photos", os.path.join(src_root, "01_Model_Photos", "vivienne_photo_01_front.jpg")),
    ("01_Model_Photos", os.path.join(src_root, "01_Model_Photos", "vivienne_photo_02_side.jpg")),
    ("01_Model_Photos", os.path.join(src_root, "01_Model_Photos", "vivienne_photo_03_back.jpg")),
    # 3. Flat Sketches
    ("02_Technical_Flat_Sketches", os.path.join(src_root, "02_Technical_Flat_Sketches", "Vivienne_Pants_Sketch_SideBySide.png")),
    ("02_Technical_Flat_Sketches", os.path.join(src_root, "02_Technical_Flat_Sketches", "Vivienne_Pants_Sketch_1800.png")),
    # 4. Customer Guides
    ("04_Customer_Delivery_Guides", os.path.join(src_root, "05_Customer_Delivery_Guides", "Vivienne_Wide_Leg_Trousers_Download_Hub.pdf")),
    ("04_Customer_Delivery_Guides", os.path.join(src_root, "05_Customer_Delivery_Guides", "SewLuxe_Printing_And_Assembling_Guide.pdf")),
    ("04_Customer_Delivery_Guides", os.path.join(src_root, "05_Customer_Delivery_Guides", "SewLuxe_Complete_Sewing_Tips_Guide.pdf")),
    # 5. Advanced Digital Formats
    ("05_Advanced_Digital_Formats", os.path.join(src_root, "06_Advanced_Digital_Formats", "Vivienne_Wide_Leg_Trousers_Projector_Layered.pdf")),
    ("05_Advanced_Digital_Formats", os.path.join(src_root, "06_Advanced_Digital_Formats", "Vivienne_Wide_Leg_Trousers_A0_ALL_SIZES_LAYERED.pdf")),
]

for subfolder, src_path in deliverables:
    target_dir = os.path.join(desktop_dest, subfolder)
    os.makedirs(target_dir, exist_ok=True)
    if os.path.exists(src_path):
        target_file = os.path.join(target_dir, os.path.basename(src_path))
        shutil.copy2(src_path, target_file)
        print(f"[OK] {subfolder} -> {os.path.basename(src_path)}")
    else:
        print(f"[MISSING] {src_path}")

print("\nDesktop Package successfully deployed to:", desktop_dest)
