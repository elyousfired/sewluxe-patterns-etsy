import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np
from PIL import Image
import os

def render_vector_sketch():
    # Supersampled high-res canvas: 3600 x 3600 px (downsampled to 1800 x 1800)
    fig, ax = plt.subplots(figsize=(12, 12), dpi=300)
    ax.set_xlim(0, 1200)
    ax.set_ylim(0, 1200)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    STROKE_MAIN = '#1A1817'
    STROKE_SEAM = '#2E2B29'
    FILL_FABRIC = '#FAF8F5'
    FILL_INNER = '#E8E4DD'
    DASH_TOPSTITCH = (2, 2)
    LW_OUTLINE = 2.2
    LW_SEAM = 1.3
    LW_STITCH = 0.9

    # ---------------- FRONT VIEW (Left Side: x_center = 330) ----------------
    fx = 330
    fy_waist = 1020
    fy_hem = 180
    leg_w = 115
    hip_w = 145
    waist_w = 110

    # Front Silhouette Path (Outer left, hem, inseam, crotch, inseam, hem, outer right, waist)
    # Left Leg & Right Leg
    front_outer_l = [
        (fx - waist_w, fy_waist),
        (fx - hip_w, fy_waist - 160),
        (fx - leg_w - 15, fy_waist - 450),
        (fx - leg_w - 10, fy_hem)
    ]
    front_hem_l = [(fx - leg_w - 10, fy_hem), (fx - 15, fy_hem)]
    front_inseam_l = [(fx - 15, fy_hem), (fx - 10, fy_waist - 450), (fx, fy_waist - 330)]
    
    front_inseam_r = [(fx, fy_waist - 330), (fx + 10, fy_waist - 450), (fx + 15, fy_hem)]
    front_hem_r = [(fx + 15, fy_hem), (fx + leg_w + 10, fy_hem)]
    front_outer_r = [
        (fx + leg_w + 10, fy_hem),
        (fx + leg_w + 15, fy_waist - 450),
        (fx + hip_w, fy_waist - 160),
        (fx + waist_w, fy_waist)
    ]
    
    # Waistband curve
    front_waist = [(fx + waist_w, fy_waist), (fx, fy_waist - 12), (fx - waist_w, fy_waist)]

    # Draw Front Legs Fill & Outline
    all_front_pts = front_outer_l + front_hem_l + front_inseam_l + front_inseam_r + front_hem_r + front_outer_r + front_waist
    f_codes = [Path.MOVETO] + [Path.LINETO] * (len(all_front_pts) - 1)
    f_path = Path(all_front_pts, f_codes)
    f_patch = patches.PathPatch(f_path, facecolor=FILL_FABRIC, edgecolor=STROKE_MAIN, lw=LW_OUTLINE, joinstyle='round', capstyle='round')
    ax.add_patch(f_patch)

    # Waistband Lower Seam (40 px tall waistband)
    wb_h = 36
    wb_curve_lower = [(fx - waist_w + 4, fy_waist - wb_h), (fx, fy_waist - wb_h - 12), (fx + waist_w - 4, fy_waist - wb_h)]
    ax.plot([p[0] for p in wb_curve_lower], [p[1] for p in wb_curve_lower], color=STROKE_SEAM, lw=LW_SEAM)

    # Center Front Seam & Fly Topstitching (J-Stitch)
    ax.plot([fx, fx], [fy_waist - wb_h - 12, fy_waist - 330], color=STROKE_SEAM, lw=LW_SEAM) # CF Seam
    
    # Fly J-stitch curve (Right overlap: viewer's left)
    fly_top = fy_waist - wb_h - 12
    fly_bottom = fy_waist - 170
    fly_w = 26
    fly_x = fx - fly_w
    j_pts = [(fx, fly_top), (fly_x, fly_top), (fly_x, fly_bottom), (fly_x + 8, fly_bottom - 20), (fx, fly_bottom - 28)]
    ax.plot([p[0] for p in j_pts[1:]], [p[1] for p in j_pts[1:]], color=STROKE_MAIN, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)

    # Front Button on Waistband Center
    btn = patches.Circle((fx, fy_waist - 22), radius=5.5, facecolor='#FFFFFF', edgecolor=STROKE_MAIN, lw=1.2)
    ax.add_patch(btn)
    # Button cross stitch
    ax.plot([fx - 2.5, fx + 2.5], [fy_waist - 22, fy_waist - 22], color=STROKE_MAIN, lw=0.8)
    ax.plot([fx, fx], [fy_waist - 24.5, fy_waist - 19.5], color=STROKE_MAIN, lw=0.8)

    # Slanted Pockets (Left & Right)
    # Left Pocket: from (fx - waist_w + 20, fy_waist - wb_h - 2) to (fx - hip_w + 10, fy_waist - 180)
    pock_l_start = (fx - waist_w + 24, fy_waist - wb_h - 4)
    pock_l_end = (fx - hip_w + 10, fy_waist - 175)
    ax.plot([pock_l_start[0], pock_l_end[0]], [pock_l_start[1], pock_l_end[1]], color=STROKE_MAIN, lw=LW_SEAM)
    # Topstitch along pocket opening
    ax.plot([pock_l_start[0] + 3, pock_l_end[0] + 3], [pock_l_start[1], pock_l_end[1]], color=STROKE_SEAM, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)
    # Pocket bag interior dash line (invisible on real, but dotted in technical sketch)
    pock_bag_pts_l = [pock_l_start, (fx - 45, fy_waist - 160), (fx - 55, fy_waist - 260), (fx - hip_w + 12, fy_waist - 240), pock_l_end]
    ax.plot([p[0] for p in pock_bag_pts_l], [p[1] for p in pock_bag_pts_l], color='#9E9A95', lw=0.8, linestyle=':', dashes=(1.5, 2.5))

    # Right Pocket
    pock_r_start = (fx + waist_w - 24, fy_waist - wb_h - 4)
    pock_r_end = (fx + hip_w - 10, fy_waist - 175)
    ax.plot([pock_r_start[0], pock_r_end[0]], [pock_r_start[1], pock_r_end[1]], color=STROKE_MAIN, lw=LW_SEAM)
    ax.plot([pock_r_start[0] - 3, pock_r_end[0] - 3], [pock_r_start[1], pock_r_end[1]], color=STROKE_SEAM, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)
    pock_bag_pts_r = [pock_r_start, (fx + 45, fy_waist - 160), (fx + 55, fy_waist - 260), (fx + hip_w - 12, fy_waist - 240), pock_r_end]
    ax.plot([p[0] for p in pock_bag_pts_r], [p[1] for p in pock_bag_pts_r], color='#9E9A95', lw=0.8, linestyle=':', dashes=(1.5, 2.5))

    # Front Waist Darts / Soft Pleats (Left and Right)
    # Left Pleat
    pleat_lx = fx - 52
    ax.plot([pleat_lx, pleat_lx], [fy_waist - wb_h - 6, fy_waist - wb_h - 65], color=STROKE_SEAM, lw=LW_SEAM)
    # Subtle crease line extending down
    ax.plot([pleat_lx, pleat_lx], [fy_waist - wb_h - 75, fy_hem + 80], color='#DDD8D0', lw=0.7, linestyle='--')

    # Right Pleat
    pleat_rx = fx + 52
    ax.plot([pleat_rx, pleat_rx], [fy_waist - wb_h - 6, fy_waist - wb_h - 65], color=STROKE_SEAM, lw=LW_SEAM)
    ax.plot([pleat_rx, pleat_rx], [fy_waist - wb_h - 75, fy_hem + 80], color='#DDD8D0', lw=0.7, linestyle='--')

    # Hem Topstitching (4 cm hem)
    hem_h = 32
    ax.plot([fx - leg_w - 10, fx - 15], [fy_hem + hem_h, fy_hem + hem_h], color=STROKE_SEAM, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)
    ax.plot([fx + 15, fx + leg_w + 10], [fy_hem + hem_h, fy_hem + hem_h], color=STROKE_SEAM, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)

    # Front Label
    ax.text(fx, fy_hem - 45, "F R O N T   V I E W", ha='center', va='center', fontfamily='sans-serif', fontsize=11, fontweight='bold', color='#2D3728')


    # ---------------- BACK VIEW (Right Side: bx = 870) ----------------
    bx = 870
    
    # Back Silhouette (slightly higher rise at center back)
    back_outer_l = [
        (bx - waist_w, fy_waist),
        (bx - hip_w, fy_waist - 160),
        (bx - leg_w - 15, fy_waist - 450),
        (bx - leg_w - 10, fy_hem)
    ]
    back_hem_l = [(bx - leg_w - 10, fy_hem), (bx - 15, fy_hem)]
    back_inseam_l = [(bx - 15, fy_hem), (bx - 10, fy_waist - 450), (bx, fy_waist - 340)]
    
    back_inseam_r = [(bx, fy_waist - 340), (bx + 10, fy_waist - 450), (bx + 15, fy_hem)]
    back_hem_r = [(bx + 15, fy_hem), (bx + leg_w + 10, fy_hem)]
    back_outer_r = [
        (bx + leg_w + 10, fy_hem),
        (bx + leg_w + 15, fy_waist - 450),
        (bx + hip_w, fy_waist - 160),
        (bx + waist_w, fy_waist)
    ]
    
    # Back Waistband Curve (peaks slightly higher at center back)
    back_waist = [(bx + waist_w, fy_waist), (bx, fy_waist + 12), (bx - waist_w, fy_waist)]

    all_back_pts = back_outer_l + back_hem_l + back_inseam_l + back_inseam_r + back_hem_r + back_outer_r + back_waist
    b_codes = [Path.MOVETO] + [Path.LINETO] * (len(all_back_pts) - 1)
    b_path = Path(all_back_pts, b_codes)
    b_patch = patches.PathPatch(b_path, facecolor=FILL_FABRIC, edgecolor=STROKE_MAIN, lw=LW_OUTLINE, joinstyle='round', capstyle='round')
    ax.add_patch(b_patch)

    # Back Waistband Lower Seam
    b_wb_lower = [(bx - waist_w + 4, fy_waist - wb_h), (bx, fy_waist + 12 - wb_h), (bx + waist_w - 4, fy_waist - wb_h)]
    ax.plot([p[0] for p in b_wb_lower], [p[1] for p in b_wb_lower], color=STROKE_SEAM, lw=LW_SEAM)

    # Center Back Seam (Full length through waistband down to crotch)
    ax.plot([bx, bx], [fy_waist + 12, fy_waist - 340], color=STROKE_SEAM, lw=LW_SEAM)

    # Back Waist Darts (2 on Left, 2 on Right = 4 Darts total)
    # Left inner dart
    ax.plot([bx - 38, bx - 38], [fy_waist + 4 - wb_h, fy_waist - wb_h - 85], color=STROKE_SEAM, lw=LW_SEAM)
    # Left outer dart
    ax.plot([bx - 74, bx - 74], [fy_waist - wb_h, fy_waist - wb_h - 70], color=STROKE_SEAM, lw=LW_SEAM)

    # Right inner dart
    ax.plot([bx + 38, bx + 38], [fy_waist + 4 - wb_h, fy_waist - wb_h - 85], color=STROKE_SEAM, lw=LW_SEAM)
    # Right outer dart
    ax.plot([bx + 74, bx + 74], [fy_waist - wb_h, fy_waist - wb_h - 70], color=STROKE_SEAM, lw=LW_SEAM)

    # Hem Topstitching (Back)
    ax.plot([bx - leg_w - 10, bx - 15], [fy_hem + hem_h, fy_hem + hem_h], color=STROKE_SEAM, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)
    ax.plot([bx + 15, bx + leg_w + 10], [fy_hem + hem_h, fy_hem + hem_h], color=STROKE_SEAM, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)

    # Back Label
    ax.text(bx, fy_hem - 45, "B A C K   V I E W", ha='center', va='center', fontfamily='sans-serif', fontsize=11, fontweight='bold', color='#2D3728')

    # Save high-res master
    out_master = r'C:\Users\red1e\.gemini\antigravity\scratch\etsy\colette_pants_engine\colette_sketch_master.png'
    plt.savefig(out_master, dpi=300, bbox_inches='tight', pad_inches=0.1, facecolor='#FFFFFF')
    plt.close()
    print("Master sketch rendered!")

    # Downsample with LANCZOS to 1800 x 1800 px and 1600 x 1000 px
    im = Image.open(out_master).convert('RGBA')
    # Resize to square 1800 x 1800
    im_sq = Image.new('RGB', (1800, 1800), '#FFFFFF')
    im_resized = im.resize((1740, int(1740 * im.height / im.width)), Image.Resampling.LANCZOS)
    offset_y = (1800 - im_resized.height) // 2
    offset_x = (1800 - im_resized.width) // 2
    im_sq.paste(im_resized, (offset_x, offset_y))
    
    # Save standard outputs
    f_1800 = r'C:\Users\red1e\Desktop\SewLuxe_Colette_Tailored_Pants\01_Flat_Sketches\Colette_Sketch_1800.png'
    f_brain = r'C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0\Colette_Sketch_1800.png'
    im_sq.save(f_1800)
    im_sq.save(f_brain)
    print(f"Saved 1800x1800 sketch to: {f_1800}")

    # Also crop individual Front and Back stickers
    crop_w = im.width // 2
    f_crop = im.crop((0, 0, crop_w, im.height))
    b_crop = im.crop((crop_w, 0, im.width, im.height))

    # Save Front Clean
    f_crop.save(r'C:\Users\red1e\Desktop\SewLuxe_Colette_Tailored_Pants\01_Flat_Sketches\flat_sketch_front_clean.png')
    f_crop.save(r'C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0\flat_sketch_front_clean.png')
    f_crop.save(r'C:\Users\red1e\.gemini\antigravity\scratch\etsy\colette_pants_engine\flat_sketch_front_clean.png')
    
    # Save Back Clean
    b_crop.save(r'C:\Users\red1e\Desktop\SewLuxe_Colette_Tailored_Pants\01_Flat_Sketches\flat_sketch_back_clean.png')
    b_crop.save(r'C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0\flat_sketch_back_clean.png')
    b_crop.save(r'C:\Users\red1e\.gemini\antigravity\scratch\etsy\colette_pants_engine\flat_sketch_back_clean.png')
    print("Front and Back individual sketches saved successfully!")

if __name__ == '__main__':
    render_vector_sketch()
