import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np
from PIL import Image
import os

def render_palazzo_vector_sketch():
    fig, ax = plt.subplots(figsize=(12, 12), dpi=300)
    ax.set_xlim(0, 1200)
    ax.set_ylim(0, 1200)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    STROKE_MAIN = '#11100F'
    STROKE_SEAM = '#22201E'
    FILL_FABRIC = '#FAF8F5'
    DASH_TOPSTITCH = (2.2, 2.2)
    LW_OUTLINE = 2.4
    LW_SEAM = 1.4
    LW_STITCH = 0.95

    # ==================== FRONT VIEW (fx = 330) ====================
    fx = 330
    fy_waist = 1010
    fy_hem = 170
    leg_w = 168      # Ultra-wide Palazzo sweep
    hip_w = 155
    waist_w = 108
    wb_h = 36        # 4 cm contoured waistband height

    # Front Silhouette
    front_outer_l = [
        (fx - waist_w, fy_waist),
        (fx - hip_w, fy_waist - 160),
        (fx - leg_w - 20, fy_waist - 460),
        (fx - leg_w - 32, fy_hem)
    ]
    front_hem_l = [(fx - leg_w - 32, fy_hem), (fx - 15, fy_hem)]
    front_inseam_l = [(fx - 15, fy_hem), (fx - 10, fy_waist - 460), (fx, fy_waist - 340)]
    
    front_inseam_r = [(fx, fy_waist - 340), (fx + 10, fy_waist - 460), (fx + 15, fy_hem)]
    front_hem_r = [(fx + 15, fy_hem), (fx + leg_w + 32, fy_hem)]
    front_outer_r = [
        (fx + leg_w + 32, fy_hem),
        (fx + leg_w + 20, fy_waist - 460),
        (fx + hip_w, fy_waist - 160),
        (fx + waist_w, fy_waist)
    ]
    front_waist = [(fx + waist_w, fy_waist), (fx, fy_waist - 10), (fx - waist_w, fy_waist)]

    all_front_pts = front_outer_l + front_hem_l + front_inseam_l + front_inseam_r + front_hem_r + front_outer_r + front_waist
    f_codes = [Path.MOVETO] + [Path.LINETO] * (len(all_front_pts) - 1)
    f_path = Path(all_front_pts, f_codes)
    f_patch = patches.PathPatch(f_path, facecolor=FILL_FABRIC, edgecolor=STROKE_MAIN, lw=LW_OUTLINE, joinstyle='round', capstyle='round')
    ax.add_patch(f_patch)

    # Waistband Lower Seam
    wb_curve_lower = [(fx - waist_w + 3, fy_waist - wb_h), (fx, fy_waist - wb_h - 10), (fx + waist_w - 3, fy_waist - wb_h)]
    ax.plot([p[0] for p in wb_curve_lower], [p[1] for p in wb_curve_lower], color=STROKE_SEAM, lw=LW_SEAM)

    # Center Front Seam
    ax.plot([fx, fx], [fy_waist - wb_h - 10, fy_waist - 340], color=STROKE_SEAM, lw=LW_SEAM)
    
    # Fly J-Stitch (Right overlap / viewer's left)
    fly_top = fy_waist - wb_h - 10
    fly_bottom = fy_waist - 175
    fly_w = 28
    fly_x = fx - fly_w
    j_pts = [(fx, fly_top), (fly_x, fly_top), (fly_x, fly_bottom), (fly_x + 9, fly_bottom - 22), (fx, fly_bottom - 30)]
    ax.plot([p[0] for p in j_pts[1:]], [p[1] for p in j_pts[1:]], color=STROKE_MAIN, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)

    # Clean Concealed Waistband Closure (Seamless Quiet-Luxury Front with Inside Hook & Bar)
    # Clean center overlap line on waistband
    ax.plot([fx, fx], [fy_waist - 10, fy_waist - wb_h - 10], color=STROKE_SEAM, lw=LW_SEAM)

    # Pleat X Coordinates (Front)
    # Inner Main Pleat: at fx - 42 and fx + 42
    # Outer Secondary Pleat: at fx - 74 and fx + 74
    # Pocket Corner / Side Loop: at fx - 104 and fx + 104
    p1_lx = fx - 42
    p2_lx = fx - 74
    p_corner_lx = fx - 104

    p1_rx = fx + 42
    p2_rx = fx + 74
    p_corner_rx = fx + 104

    # 4 FRONT BELT LOOPS (Exact matching placement):
    # 2 Inner Loops: placed DIRECTLY OVER the Main Pleats (p1_lx and p1_rx)
    # 2 Outer Loops: placed DIRECTLY AT the Pocket / Side Seam (p_corner_lx and p_corner_rx)
    loop_w = 7.0
    front_loop_xs = [p1_lx, p1_rx, p_corner_lx, p_corner_rx]
    for lx in front_loop_xs:
        ratio = abs(lx - fx) / waist_w
        local_top = (fy_waist - 10) + ratio * 10
        local_bot = local_top - wb_h
        loop = patches.Rectangle((lx - loop_w/2, local_bot - 4), loop_w, wb_h + 8, facecolor=FILL_FABRIC, edgecolor=STROKE_MAIN, lw=1.1, zorder=5)
        ax.add_patch(loop)
        ax.plot([lx - loop_w/2, lx + loop_w/2], [local_top + 4, local_top + 4], color=STROKE_MAIN, lw=1.2, zorder=6)
        ax.plot([lx - loop_w/2, lx + loop_w/2], [local_bot - 4, local_bot - 4], color=STROKE_MAIN, lw=1.2, zorder=6)

    # DOUBLE FRONT PLEATS (Left Leg)
    # 1. Main Pleat: Starts directly under loop p1_lx
    ax.plot([p1_lx, p1_lx], [fy_waist - wb_h - 7, fy_waist - wb_h - 75], color=STROKE_MAIN, lw=1.6)
    # Sharp Center Crease Line
    ax.plot([p1_lx, p1_lx - 42], [fy_waist - wb_h - 75, fy_hem + 42], color='#2B2826', lw=1.15, linestyle='-')

    # 2. Secondary Pleat
    ax.plot([p2_lx, p2_lx], [fy_waist - wb_h - 4, fy_waist - wb_h - 52], color=STROKE_MAIN, lw=1.4)

    # DOUBLE FRONT PLEATS (Right Leg)
    # 1. Main Pleat: Starts directly under loop p1_rx
    ax.plot([p1_rx, p1_rx], [fy_waist - wb_h - 7, fy_waist - wb_h - 75], color=STROKE_MAIN, lw=1.6)
    # Sharp Center Crease Line
    ax.plot([p1_rx, p1_rx + 42], [fy_waist - wb_h - 75, fy_hem + 42], color='#2B2826', lw=1.15, linestyle='-')

    # 2. Secondary Pleat
    ax.plot([p2_rx, p2_rx], [fy_waist - wb_h - 4, fy_waist - wb_h - 52], color=STROKE_MAIN, lw=1.4)

    # Slanted Pockets (Italian Slant Pockets)
    # Left Pocket: starts at the side belt loop p_corner_lx, angles down to side seam
    pock_l_start = (p_corner_lx - 2, fy_waist - wb_h - 1)
    pock_l_end = (fx - hip_w + 10, fy_waist - 190)
    ax.plot([pock_l_start[0], pock_l_end[0]], [pock_l_start[1], pock_l_end[1]], color=STROKE_MAIN, lw=LW_SEAM)
    ax.plot([pock_l_start[0] + 3, pock_l_end[0] + 3], [pock_l_start[1], pock_l_end[1]], color=STROKE_SEAM, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)

    # Right Pocket
    pock_r_start = (p_corner_rx + 2, fy_waist - wb_h - 1)
    pock_r_end = (fx + hip_w - 10, fy_waist - 190)
    ax.plot([pock_r_start[0], pock_r_end[0]], [pock_r_start[1], pock_r_end[1]], color=STROKE_MAIN, lw=LW_SEAM)
    ax.plot([pock_r_start[0] - 3, pock_r_end[0] - 3], [pock_r_start[1], pock_r_end[1]], color=STROKE_SEAM, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)

    # Deep 5 cm Hem foldline
    hem_h = 42
    ax.plot([fx - leg_w - 32, fx - 15], [fy_hem + hem_h, fy_hem + hem_h], color=STROKE_SEAM, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)
    ax.plot([fx + 15, fx + leg_w + 32], [fy_hem + hem_h, fy_hem + hem_h], color=STROKE_SEAM, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)

    # Front Label
    ax.text(fx, fy_hem - 45, "F R O N T   V I E W", ha='center', va='center', fontfamily='sans-serif', fontsize=11, fontweight='bold', color='#2D3728')


    # ==================== BACK VIEW (bx = 870) ====================
    bx = 870

    back_outer_l = [
        (bx - waist_w, fy_waist),
        (bx - hip_w, fy_waist - 160),
        (bx - leg_w - 20, fy_waist - 460),
        (bx - leg_w - 32, fy_hem)
    ]
    back_hem_l = [(bx - leg_w - 32, fy_hem), (bx - 15, fy_hem)]
    back_inseam_l = [(bx - 15, fy_hem), (bx - 10, fy_waist - 460), (bx, fy_waist - 350)]
    
    back_inseam_r = [(bx, fy_waist - 350), (bx + 10, fy_waist - 460), (bx + 15, fy_hem)]
    back_hem_r = [(bx + 15, fy_hem), (bx + leg_w + 32, fy_hem)]
    back_outer_r = [
        (bx + leg_w + 32, fy_hem),
        (bx + leg_w + 20, fy_waist - 460),
        (bx + hip_w, fy_waist - 160),
        (bx + waist_w, fy_waist)
    ]
    back_waist = [(bx + waist_w, fy_waist), (bx, fy_waist + 12), (bx - waist_w, fy_waist)]

    all_back_pts = back_outer_l + back_hem_l + back_inseam_l + back_inseam_r + back_hem_r + back_outer_r + back_waist
    b_codes = [Path.MOVETO] + [Path.LINETO] * (len(all_back_pts) - 1)
    b_path = Path(all_back_pts, b_codes)
    b_patch = patches.PathPatch(b_path, facecolor=FILL_FABRIC, edgecolor=STROKE_MAIN, lw=LW_OUTLINE, joinstyle='round', capstyle='round')
    ax.add_patch(b_patch)

    # Back Waistband Lower Seam
    b_wb_lower = [(bx - waist_w + 3, fy_waist - wb_h), (bx, fy_waist + 12 - wb_h), (bx + waist_w - 3, fy_waist - wb_h)]
    ax.plot([p[0] for p in b_wb_lower], [p[1] for p in b_wb_lower], color=STROKE_SEAM, lw=LW_SEAM)

    # Center Back Seam
    ax.plot([bx, bx], [fy_waist + 12, fy_waist - 350], color=STROKE_SEAM, lw=LW_SEAM)

    # 3 BACK BELT LOOPS (Exact matching placement):
    # 1 Center Back Loop: placed DIRECTLY OVER the Center Back Seam (bx)
    # 2 Side Loops: at side seams (bx - 104 and bx + 104)
    back_loop_xs = [bx, bx - 104, bx + 104]
    for lx in back_loop_xs:
        if lx == bx:
            local_top = fy_waist + 12
            local_bot = local_top - wb_h
        else:
            local_top = fy_waist
            local_bot = local_top - wb_h
        loop = patches.Rectangle((lx - loop_w/2, local_bot - 4), loop_w, wb_h + 8, facecolor=FILL_FABRIC, edgecolor=STROKE_MAIN, lw=1.1, zorder=5)
        ax.add_patch(loop)
        ax.plot([lx - loop_w/2, lx + loop_w/2], [local_top + 4, local_top + 4], color=STROKE_MAIN, lw=1.2, zorder=6)
        ax.plot([lx - loop_w/2, lx + loop_w/2], [local_bot - 4, local_bot - 4], color=STROKE_MAIN, lw=1.2, zorder=6)

    # Back Waist Darts (2 on Left, 2 on Right = 4 Darts total)
    # Left inner dart (longer)
    ax.plot([bx - 42, bx - 42], [fy_waist + 4 - wb_h, fy_waist - wb_h - 90], color=STROKE_SEAM, lw=LW_SEAM)
    # Left outer dart (shorter)
    ax.plot([bx - 74, bx - 74], [fy_waist - wb_h, fy_waist - wb_h - 72], color=STROKE_SEAM, lw=LW_SEAM)

    # Right inner dart (longer)
    ax.plot([bx + 42, bx + 42], [fy_waist + 4 - wb_h, fy_waist - wb_h - 90], color=STROKE_SEAM, lw=LW_SEAM)
    # Right outer dart (shorter)
    ax.plot([bx + 74, bx + 74], [fy_waist - wb_h, fy_waist - wb_h - 72], color=STROKE_SEAM, lw=LW_SEAM)

    # Center Crease on Back Legs
    ax.plot([bx - 42, bx - 74], [fy_waist - wb_h - 90, fy_hem + 42], color='#2B2826', lw=1.05, linestyle='-')
    ax.plot([bx + 42, bx + 74], [fy_waist - wb_h - 90, fy_hem + 42], color='#2B2826', lw=1.05, linestyle='-')

    # Hem Topstitching (Back)
    ax.plot([bx - leg_w - 32, bx - 15], [fy_hem + hem_h, fy_hem + hem_h], color=STROKE_SEAM, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)
    ax.plot([bx + 15, bx + leg_w + 32], [fy_hem + hem_h, fy_hem + hem_h], color=STROKE_SEAM, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)

    # Back Label
    ax.text(bx, fy_hem - 45, "B A C K   V I E W", ha='center', va='center', fontfamily='sans-serif', fontsize=11, fontweight='bold', color='#2D3728')

    # Save high-res master
    out_master = r'C:\Users\red1e\.gemini\antigravity\scratch\etsy\colette_pants_engine\colette_sketch_master.png'
    plt.savefig(out_master, dpi=300, bbox_inches='tight', pad_inches=0.1, facecolor='#FFFFFF')
    plt.close()
    print("Master vector flat sketch rendered!")

    # Downsample to 1800 x 1800
    im = Image.open(out_master).convert('RGBA')
    im_sq = Image.new('RGB', (1800, 1800), '#FFFFFF')
    scale = 1720 / max(im.width, im.height)
    new_w = int(im.width * scale)
    new_h = int(im.height * scale)
    im_resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    offset_y = (1800 - new_h) // 2
    offset_x = (1800 - new_w) // 2
    im_sq.paste(im_resized, (offset_x, offset_y))
    
    f_1800 = r'C:\Users\red1e\Desktop\SewLuxe_Colette_Tailored_Pants\01_Flat_Sketches\Colette_Sketch_1800.png'
    f_brain = r'C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0\Colette_Sketch_1800.png'
    im_sq.save(f_1800)
    im_sq.save(f_brain)
    print(f"Saved pristine 1800x1800 sketch to: {f_1800}")

    # Crop individual Front and Back
    crop_w = im.width // 2
    f_crop = im.crop((0, 0, crop_w, im.height))
    b_crop = im.crop((crop_w, 0, im.width, im.height))

    f_crop.save(r'C:\Users\red1e\Desktop\SewLuxe_Colette_Tailored_Pants\01_Flat_Sketches\flat_sketch_front_clean.png')
    f_crop.save(r'C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0\flat_sketch_front_clean.png')
    f_crop.save(r'C:\Users\red1e\.gemini\antigravity\scratch\etsy\colette_pants_engine\flat_sketch_front_clean.png')
    
    b_crop.save(r'C:\Users\red1e\Desktop\SewLuxe_Colette_Tailored_Pants\01_Flat_Sketches\flat_sketch_back_clean.png')
    b_crop.save(r'C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0\flat_sketch_back_clean.png')
    b_crop.save(r'C:\Users\red1e\.gemini\antigravity\scratch\etsy\colette_pants_engine\flat_sketch_back_clean.png')

    # Side-by-side 1600x1000
    sbs = Image.new('RGB', (1600, 1000), '#FFFFFF')
    target_h = 860
    scale_f = target_h / f_crop.height
    wf = int(f_crop.width * scale_f)
    f_res = f_crop.resize((wf, target_h), Image.Resampling.LANCZOS)
    wb = int(b_crop.width * scale_f)
    b_res = b_crop.resize((wb, target_h), Image.Resampling.LANCZOS)
    gap = 60
    start_x = (1600 - (wf + wb + gap)) // 2
    sbs.paste(f_res, (start_x, 70), f_res)
    sbs.paste(b_res, (start_x + wf + gap, 70), b_res)
    sbs_path = r'C:\Users\red1e\Desktop\SewLuxe_Colette_Tailored_Pants\01_Flat_Sketches\Colette_Sketch_SideBySide.png'
    sbs.save(sbs_path)
    sbs.save(r'C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0\Colette_Sketch_SideBySide.png')

    # Transparent Stickers
    def make_transparent_sticker(img_rgba, path1, path2):
        arr = np.array(img_rgba)
        mask = (arr[:, :, 0] > 250) & (arr[:, :, 1] > 250) & (arr[:, :, 2] > 250)
        arr[mask, 3] = 0
        res = Image.fromarray(arr)
        res.save(path1)
        res.save(path2)

    make_transparent_sticker(
        f_crop,
        r'C:\Users\red1e\Desktop\SewLuxe_Colette_Tailored_Pants\01_Flat_Sketches\Colette_Sticker_Front.png',
        r'C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0\Colette_Sticker_Front.png'
    )
    make_transparent_sticker(
        b_crop,
        r'C:\Users\red1e\Desktop\SewLuxe_Colette_Tailored_Pants\01_Flat_Sketches\Colette_Sticker_Back.png',
        r'C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0\Colette_Sticker_Back.png'
    )
    print("All flat sketch deliverables exported successfully!")

if __name__ == '__main__':
    render_palazzo_vector_sketch()
