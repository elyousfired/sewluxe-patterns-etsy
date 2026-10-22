import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np
from PIL import Image
import os

def render_vivienne_sketches():
    out_dir = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\projects\wide_leg_trousers_welt_pockets\02_Technical_Flat_Sketches"
    os.makedirs(out_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(16, 10), dpi=300)
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 1000)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    STROKE_MAIN = '#111111'
    STROKE_SEAM = '#222222'
    FILL_FABRIC = '#FAF9F6'  # Elegant light ecru/white fill
    DASH_TOPSTITCH = (2.5, 2.5)
    LW_OUTLINE = 2.4
    LW_SEAM = 1.4
    LW_STITCH = 0.9

    # ---------------- FRONT VIEW (Left Side: fx = 440) ----------------
    fx = 440
    fy_waist = 860
    fy_hem = 120
    leg_w = 110
    hip_w = 138
    waist_w = 104
    wb_h = 34

    front_outer_l = [
        (fx - waist_w, fy_waist),
        (fx - hip_w, fy_waist - 140),
        (fx - leg_w - 12, fy_waist - 400),
        (fx - leg_w - 6, fy_hem)
    ]
    front_hem_l = [(fx - leg_w - 6, fy_hem), (fx - 14, fy_hem)]
    front_inseam_l = [(fx - 14, fy_hem), (fx - 10, fy_waist - 400), (fx, fy_waist - 290)]
    
    front_inseam_r = [(fx, fy_waist - 290), (fx + 10, fy_waist - 400), (fx + 14, fy_hem)]
    front_hem_r = [(fx + 14, fy_hem), (fx + leg_w + 6, fy_hem)]
    front_outer_r = [
        (fx + leg_w + 6, fy_hem),
        (fx + leg_w + 12, fy_waist - 400),
        (fx + hip_w, fy_waist - 140),
        (fx + waist_w, fy_waist)
    ]
    front_waist = [(fx + waist_w, fy_waist), (fx, fy_waist - 10), (fx - waist_w, fy_waist)]

    all_front_pts = front_outer_l + front_hem_l + front_inseam_l + front_inseam_r + front_hem_r + front_outer_r + front_waist
    f_codes = [Path.MOVETO] + [Path.LINETO] * (len(all_front_pts) - 1)
    f_path = Path(all_front_pts, f_codes)
    f_patch = patches.PathPatch(f_path, facecolor=FILL_FABRIC, edgecolor=STROKE_MAIN, lw=LW_OUTLINE, joinstyle='round', capstyle='round')
    ax.add_patch(f_patch)

    # Waistband lower seam
    wb_curve_lower = [(fx - waist_w + 3, fy_waist - wb_h), (fx, fy_waist - wb_h - 10), (fx + waist_w - 3, fy_waist - wb_h)]
    ax.plot([p[0] for p in wb_curve_lower], [p[1] for p in wb_curve_lower], color=STROKE_SEAM, lw=LW_SEAM)

    # Center Front Seam & Fly
    ax.plot([fx, fx], [fy_waist - wb_h - 10, fy_waist - 290], color=STROKE_SEAM, lw=LW_SEAM)

    # J-Stitch Fly (viewer's left side)
    fly_top = fy_waist - wb_h - 10
    fly_bottom = fy_waist - 150
    fly_w = 24
    fly_x = fx - fly_w
    j_pts = [(fx, fly_top), (fly_x, fly_top), (fly_x, fly_bottom), (fly_x + 8, fly_bottom - 18), (fx, fly_bottom - 24)]
    ax.plot([p[0] for p in j_pts[1:]], [p[1] for p in j_pts[1:]], color=STROKE_MAIN, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)

    # Center front horn button on waistband
    btn = patches.Circle((fx, fy_waist - 18), radius=5.0, facecolor='#FFFFFF', edgecolor=STROKE_MAIN, lw=1.2)
    ax.add_patch(btn)
    ax.plot([fx - 2, fx + 2], [fy_waist - 18, fy_waist - 18], color=STROKE_MAIN, lw=0.8)
    ax.plot([fx, fx], [fy_waist - 20, fy_waist - 16], color=STROKE_MAIN, lw=0.8)

    # 4 Belt loops on front (2 front, 2 side)
    # Front left belt loop
    bl_fl = patches.Rectangle((fx - 46, fy_waist - wb_h - 8), 7, wb_h + 6, facecolor=FILL_FABRIC, edgecolor=STROKE_MAIN, lw=1.0)
    ax.add_patch(bl_fl)
    # Front right belt loop
    bl_fr = patches.Rectangle((fx + 39, fy_waist - wb_h - 8), 7, wb_h + 6, facecolor=FILL_FABRIC, edgecolor=STROKE_MAIN, lw=1.0)
    ax.add_patch(bl_fr)
    # Side left belt loop
    bl_sl = patches.Rectangle((fx - waist_w + 8, fy_waist - wb_h + 2), 6, wb_h - 4, facecolor=FILL_FABRIC, edgecolor=STROKE_MAIN, lw=1.0)
    ax.add_patch(bl_sl)
    # Side right belt loop
    bl_sr = patches.Rectangle((fx + waist_w - 14, fy_waist - wb_h + 2), 6, wb_h - 4, facecolor=FILL_FABRIC, edgecolor=STROKE_MAIN, lw=1.0)
    ax.add_patch(bl_sr)

    # Slanted front hip pockets (Italian slant pockets)
    pock_l_start = (fx - waist_w + 20, fy_waist - wb_h - 4)
    pock_l_end = (fx - hip_w + 8, fy_waist - 160)
    ax.plot([pock_l_start[0], pock_l_end[0]], [pock_l_start[1], pock_l_end[1]], color=STROKE_MAIN, lw=LW_SEAM)
    ax.plot([pock_l_start[0] + 3, pock_l_end[0] + 3], [pock_l_start[1], pock_l_end[1]], color=STROKE_SEAM, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)

    pock_r_start = (fx + waist_w - 20, fy_waist - wb_h - 4)
    pock_r_end = (fx + hip_w - 8, fy_waist - 160)
    ax.plot([pock_r_start[0], pock_r_end[0]], [pock_r_start[1], pock_r_end[1]], color=STROKE_MAIN, lw=LW_SEAM)
    ax.plot([pock_r_start[0] - 3, pock_r_end[0] - 3], [pock_r_start[1], pock_r_end[1]], color=STROKE_SEAM, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)

    # Sharp vertical center crease line on both legs (From below fly down to hem)
    crease_lx = fx - 54
    crease_rx = fx + 54
    ax.plot([crease_lx, crease_lx], [fy_waist - wb_h - 30, fy_hem + 36], color='#B0AAA0', lw=0.8, linestyle='--')
    ax.plot([crease_rx, crease_rx], [fy_waist - wb_h - 30, fy_hem + 36], color='#B0AAA0', lw=0.8, linestyle='--')

    # Hem topstitching (4.0 cm clean hem)
    hem_h = 30
    ax.plot([fx - leg_w - 6, fx - 14], [fy_hem + hem_h, fy_hem + hem_h], color=STROKE_SEAM, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)
    ax.plot([fx + 14, fx + leg_w + 6], [fy_hem + hem_h, fy_hem + hem_h], color=STROKE_SEAM, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)

    # Front Label
    ax.text(fx, fy_hem - 45, "F R O N T   V I E W", ha='center', va='center', fontfamily='sans-serif', fontsize=12, fontweight='bold', color='#1A1817')


    # ---------------- BACK VIEW (Right Side: bx = 1160) ----------------
    bx = 1160

    back_outer_l = [
        (bx - waist_w, fy_waist),
        (bx - hip_w, fy_waist - 140),
        (bx - leg_w - 12, fy_waist - 400),
        (bx - leg_w - 6, fy_hem)
    ]
    back_hem_l = [(bx - leg_w - 6, fy_hem), (bx - 14, fy_hem)]
    back_inseam_l = [(bx - 14, fy_hem), (bx - 10, fy_waist - 400), (bx, fy_waist - 300)]
    
    back_inseam_r = [(bx, fy_waist - 300), (bx + 10, fy_waist - 400), (bx + 14, fy_hem)]
    back_hem_r = [(bx + 14, fy_hem), (bx + leg_w + 6, fy_hem)]
    back_outer_r = [
        (bx + leg_w + 6, fy_hem),
        (bx + leg_w + 12, fy_waist - 400),
        (bx + hip_w, fy_waist - 140),
        (bx + waist_w, fy_waist)
    ]
    # Back waist curve peaks slightly higher at center back
    back_waist = [(bx + waist_w, fy_waist), (bx, fy_waist + 12), (bx - waist_w, fy_waist)]

    all_back_pts = back_outer_l + back_hem_l + back_inseam_l + back_inseam_r + back_hem_r + back_outer_r + back_waist
    b_codes = [Path.MOVETO] + [Path.LINETO] * (len(all_back_pts) - 1)
    b_path = Path(all_back_pts, b_codes)
    b_patch = patches.PathPatch(b_path, facecolor=FILL_FABRIC, edgecolor=STROKE_MAIN, lw=LW_OUTLINE, joinstyle='round', capstyle='round')
    ax.add_patch(b_patch)

    # Back waistband lower seam
    b_wb_lower = [(bx - waist_w + 3, fy_waist - wb_h), (bx, fy_waist + 12 - wb_h), (bx + waist_w - 3, fy_waist - wb_h)]
    ax.plot([p[0] for p in b_wb_lower], [p[1] for p in b_wb_lower], color=STROKE_SEAM, lw=LW_SEAM)

    # Center Back Seam (through waistband down to crotch)
    ax.plot([bx, bx], [fy_waist + 12, fy_waist - 300], color=STROKE_SEAM, lw=LW_SEAM)

    # Center back belt loop (placed over CB seam)
    bl_cb = patches.Rectangle((bx - 3.5, fy_waist + 12 - wb_h - 2), 7, wb_h + 4, facecolor=FILL_FABRIC, edgecolor=STROKE_MAIN, lw=1.0)
    ax.add_patch(bl_cb)

    # Side belt loops (back view)
    bl_bsl = patches.Rectangle((bx - waist_w + 8, fy_waist - wb_h + 2), 6, wb_h - 4, facecolor=FILL_FABRIC, edgecolor=STROKE_MAIN, lw=1.0)
    ax.add_patch(bl_bsl)
    bl_bsr = patches.Rectangle((bx + waist_w - 14, fy_waist - wb_h + 2), 6, wb_h - 4, facecolor=FILL_FABRIC, edgecolor=STROKE_MAIN, lw=1.0)
    ax.add_patch(bl_bsr)

    # TWO BACK WAIST DARTS (1 Left, 1 Right)
    dart_lx = bx - 48
    ax.plot([dart_lx, dart_lx], [fy_waist + 5 - wb_h, fy_waist - wb_h - 75], color=STROKE_SEAM, lw=LW_SEAM)

    dart_rx = bx + 48
    ax.plot([dart_rx, dart_rx], [fy_waist + 5 - wb_h, fy_waist - wb_h - 75], color=STROKE_SEAM, lw=LW_SEAM)

    # Back center crease lines
    ax.plot([dart_lx - 6, dart_lx - 6], [fy_waist - wb_h - 85, fy_hem + 36], color='#B0AAA0', lw=0.8, linestyle='--')
    ax.plot([dart_rx + 6, dart_rx + 6], [fy_waist - wb_h - 85, fy_hem + 36], color='#B0AAA0', lw=0.8, linestyle='--')

    # Hem topstitching (Back)
    ax.plot([bx - leg_w - 6, bx - 14], [fy_hem + hem_h, fy_hem + hem_h], color=STROKE_SEAM, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)
    ax.plot([bx + 14, bx + leg_w + 6], [fy_hem + hem_h, fy_hem + hem_h], color=STROKE_SEAM, lw=LW_STITCH, linestyle='--', dashes=DASH_TOPSTITCH)

    # Back Label
    ax.text(bx, fy_hem - 45, "B A C K   V I E W", ha='center', va='center', fontfamily='sans-serif', fontsize=12, fontweight='bold', color='#1A1817')

    # Title at the top center
    ax.text(800, 950, "V I V I E N N E   W I D E - L E G   T R O U S E R S", ha='center', va='center', fontfamily='sans-serif', fontsize=14, fontweight='bold', color='#1A1817')
    ax.text(800, 920, "TECHNICAL FLAT SPECIFICATION · SEWLUXE PATTERNS", ha='center', va='center', fontfamily='sans-serif', fontsize=8.5, color='#777777')

    sidebyside_path = os.path.join(out_dir, "Vivienne_Pants_Sketch_SideBySide.png")
    plt.savefig(sidebyside_path, dpi=300, bbox_inches='tight', pad_inches=0.1, facecolor='#FFFFFF')
    plt.close()
    print("Saved SideBySide sketch:", sidebyside_path)

    # Also render square 1800x1800 px sketch
    im = Image.open(sidebyside_path)
    sq_size = max(im.width, im.height) + 120
    sq_bg = Image.new('RGB', (sq_size, sq_size), (255, 255, 255))
    offset = ((sq_size - im.width) // 2, (sq_size - im.height) // 2)
    sq_bg.paste(im, offset)
    sq_final = sq_bg.resize((1800, 1800), Image.Resampling.LANCZOS)
    sq_path = os.path.join(out_dir, "Vivienne_Pants_Sketch_1800.png")
    sq_final.save(sq_path, quality=95)
    print("Saved 1800x1800 sketch:", sq_path)

if __name__ == "__main__":
    render_vivienne_sketches()
