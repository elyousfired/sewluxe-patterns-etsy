import os
import pymupdf
from PIL import Image

BRAIN_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0"
SKETCH_DIR = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\projects\trendy_high_waist_wide_leg\02_Technical_Flat_Sketches"

# Render Design 4 (Flat Front - Side/Back Zip)
svg_d4 = os.path.join(BRAIN_DIR, "patternfast_design_4.svg")
doc4 = pymupdf.open(svg_d4)
pix4 = doc4[0].get_pixmap(dpi=300)
out_d4_png = os.path.join(BRAIN_DIR, "PatternFast_Original_Flat_Front.png")
pix4.save(out_d4_png)
doc4.close()

# Render Design 1 (Fly Front)
svg_d1 = os.path.join(BRAIN_DIR, "patternfast_design_1.svg")
doc1 = pymupdf.open(svg_d1)
pix1 = doc1[0].get_pixmap(dpi=300)
out_d1_png = os.path.join(BRAIN_DIR, "PatternFast_Original_Fly_Front.png")
pix1.save(out_d1_png)
doc1.close()

# Also create clean 1800x1800 studio presentation for both
for name, png_path in [("Flat_Front", out_d4_png), ("Fly_Front", out_d1_png)]:
    im = Image.open(png_path).convert('RGB')
    sq = Image.new('RGB', (1800, 1800), (255, 255, 255))
    
    # Crop white whitespace
    bbox = im.getbbox()
    if bbox:
        im_cropped = im.crop(bbox)
        w, h = im_cropped.size
        scale = 1500.0 / h
        new_w, new_h = int(w * scale), int(h * scale)
        im_resized = im_cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
        sq.paste(im_resized, ((1800 - new_w) // 2, (1800 - new_h) // 2))
        
    sq_path = os.path.join(BRAIN_DIR, f"PatternFast_Studio_{name}_1800.png")
    sq.save(sq_path, quality=95)
    # Copy to project sketch dir
    sq.save(os.path.join(SKETCH_DIR, f"PatternFast_Studio_{name}_1800.png"), quality=95)
    print(f"Generated studio sketch: {sq_path}")

print("Both authentic PatternFast original sketches rendered and saved!")
