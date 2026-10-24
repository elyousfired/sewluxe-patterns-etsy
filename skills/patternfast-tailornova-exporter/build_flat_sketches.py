import os
from PIL import Image, ImageOps

BRAIN_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0"

def get_bbox(img_path):
    im = Image.open(img_path).convert("RGB")
    # Invert to find non-white bounding box
    gray = im.convert("L")
    inv = ImageOps.invert(gray)
    bbox = inv.getbbox()
    return im.crop(bbox)

# 1. Side Button (Clean front, darts, no button, no fly)
front_crop = get_bbox(os.path.join(BRAIN_DIR, "test_front_only.png"))
back_crop = get_bbox(os.path.join(BRAIN_DIR, "test_back_only.png"))

print(f"Front crop: {front_crop.size}, Back crop: {back_crop.size}")

# Build 1800x1800 technical sheet
canvas = Image.new("RGB", (1800, 1800), (255, 255, 255))

# Target height: ~1350px
target_h = 1350
f_ratio = target_h / front_crop.height
f_w = int(front_crop.width * f_ratio)
front_resized = front_crop.resize((f_w, target_h), Image.Resampling.LANCZOS)

b_ratio = target_h / back_crop.height
b_w = int(back_crop.width * b_ratio)
back_resized = back_crop.resize((b_w, target_h), Image.Resampling.LANCZOS)

# Position side by side
gap = 120
total_w = f_w + b_w + gap
start_x = (1800 - total_w) // 2
y = (1800 - target_h) // 2

canvas.paste(front_resized, (start_x, y))
canvas.paste(back_resized, (start_x + f_w + gap, y))

out_path = os.path.join(BRAIN_DIR, "PatternFast_Original_Side_Zip_1800.png")
canvas.save(out_path, quality=95)
print("Saved PatternFast_Original_Side_Zip_1800.png")

# 2. Also build a comparison image with user's uploaded image:
user_img_path = os.path.join(BRAIN_DIR, ".user_uploaded", "media_1792862366828_40fcccdf.png")
if os.path.exists(user_img_path):
    user_img = Image.open(user_img_path).convert("RGB")
    comp = Image.new("RGB", (3600, 1800), (255, 255, 255))
    
    # Left: User image resized to 1800x1800 fit
    user_img.thumbnail((1700, 1700), Image.Resampling.LANCZOS)
    ux = (1800 - user_img.width) // 2
    uy = (1800 - user_img.height) // 2
    comp.paste(user_img, (ux, uy))
    
    # Right: PatternFast extracted sketch
    comp.paste(canvas, (1800, 0))
    
    comp_path = os.path.join(BRAIN_DIR, "PatternFast_vs_User_Comparison.png")
    comp.save(comp_path, quality=95)
    print("Saved PatternFast_vs_User_Comparison.png")
