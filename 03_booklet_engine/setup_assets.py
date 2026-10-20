import os
import shutil

src_studio = r"C:\Users\red1e\Desktop\SewLuxe_Production_System\01_Pants_System\projects\Lila_Lounge_Pants\instruction_panels_studio"
dst_studio = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\03_booklet_engine\instruction_panels_studio"
os.makedirs(dst_studio, exist_ok=True)

for f in os.listdir(src_studio):
    if f.endswith(".png"):
        shutil.copy2(os.path.join(src_studio, f), os.path.join(dst_studio, f))
print(f"Copied {len(os.listdir(dst_studio))} panels to {dst_studio}")

# Copy pieces_overview.png
shutil.copy2(
    r"C:\Users\red1e\Desktop\SewLuxe_Production_System\01_Pants_System\projects\Lila_Lounge_Pants\pieces_overview.png",
    r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\03_booklet_engine\pieces_overview.png"
)
print("Copied pieces_overview.png")

# Copy flat sketch
shutil.copy2(
    r"C:\Users\red1e\Desktop\SewLuxe_Elastic_Wide_Leg_Pants\01_Flat_Sketches\Elastic_Wide_Leg_Pants_Technical_Sketch.png",
    r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\03_booklet_engine\flat_sketch.png"
)
print("Copied flat_sketch.png")

# Copy cover model photo
shutil.copy2(
    r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\03_booklet_engine\model_photos\model_photo_1.jpg",
    r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\03_booklet_engine\margot_cover_model.jpg"
)
shutil.copy2(
    r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\03_booklet_engine\model_photos\model_photo_2.jpg",
    r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\03_booklet_engine\margot_model_back.jpg"
)
print("Copied cover & back model photos.")
