import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np
from PIL import Image
import os

PANELS_DIR = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\sewluxe_core\assets\master_panels"
os.makedirs(PANELS_DIR, exist_ok=True)

# Colors
C_CONTAINER = '#F5F2EF'
C_BORDER = '#E2DDD8'
C_BOX_BG = '#FFFFFF'
C_STROKE_BOX = '#000000'
C_STROKE_MAIN = '#111111'
C_STROKE_SEAM = '#333333'
C_FABRIC_RIGHT = '#FAF8F5'
C_FABRIC_WRONG = '#E6E6E6'
C_STITCH = '#D9534F' # Red/dark dashed for clear sewing indication or dark dashed
C_CREASE = '#337AB7'

def build_step1_flat_front():
    # Width: 2200, Height: 1050 (Aspect ratio ~ 2.1:1)
    fig, ax = plt.subplots(figsize=(11, 5.25), dpi=300)
    ax.set_xlim(0, 2200)
    ax.set_ylim(0, 1050)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(C_CONTAINER)
    ax.set_facecolor(C_CONTAINER)

    # Rounded outer border
    outer = patches.FancyBboxPatch((15, 15), 2170, 1020, boxstyle="round,pad=10,rounding_size=24",
                                  facecolor=C_CONTAINER, edgecolor=C_BORDER, lw=1.5)
    ax.add_patch(outer)

    # Box 1: Left Box (x: 45 to 1080, y: 45 to 1005)
    box1 = patches.Rectangle((45, 45), 1035, 960, facecolor=C_BOX_BG, edgecolor=C_STROKE_BOX, lw=3.0)
    ax.add_patch(box1)

    # Box 2: Right Box (x: 1120 to 2155, y: 45 to 1005)
    box2 = patches.Rectangle((1120, 45), 1035, 960, facecolor=C_BOX_BG, edgecolor=C_STROKE_BOX, lw=3.0)
    ax.add_patch(box2)

    # Numbers 1. and 2.
    ax.text(80, 940, "1.", fontfamily='sans-serif', fontsize=26, fontweight='bold', color='#000000')
    ax.text(1155, 940, "2.", fontfamily='sans-serif', fontsize=26, fontweight='bold', color='#000000')

    # ---------------- PANEL 1: Staystitch Front Waist & Stitch Darts (Wrong Side) ----------------
    # Upper front of trouser (wrong side: grey fill #E6E6E6)
    cx1 = 562
    cy1 = 530
    
    # Front waist curve points (wrong side shown)
    pts_f1 = [
        (cx1 - 320, cy1 + 220), # left hip waist
        (cx1, cy1 + 195),       # center front waist
        (cx1 + 320, cy1 + 220), # right hip waist
        (cx1 + 350, cy1 - 40),  # right side hip curve
        (cx1 + 240, cy1 - 300), # right thigh
        (cx1 + 50, cy1 - 250),  # crotch curve
        (cx1, cy1 - 180),       # center crotch
        (cx1 - 50, cy1 - 250),
        (cx1 - 240, cy1 - 300), # left thigh
        (cx1 - 350, cy1 - 40),  # left hip curve
    ]
    poly1 = patches.Polygon(pts_f1, closed=True, facecolor=C_FABRIC_WRONG, edgecolor=C_STROKE_MAIN, lw=2.2)
    ax.add_patch(poly1)

    # Staystitching along waist curve (6 mm / dashed line)
    stay_pts = [
        (cx1 - 310, cy1 + 205),
        (cx1 - 150, cy1 + 190),
        (cx1, cy1 + 182),
        (cx1 + 150, cy1 + 190),
        (cx1 + 310, cy1 + 205),
    ]
    ax.plot([p[0] for p in stay_pts], [p[1] for p in stay_pts], color='#222222', lw=1.6, linestyle='--', dashes=(3, 3))

    # Front waist darts (one on left, one on right)
    # Left front dart
    d1_x = cx1 - 140
    d1_top_y = cy1 + 198
    d1_bot_y = cy1 + 40
    ax.plot([d1_x, d1_x], [d1_top_y, d1_bot_y], color='#111111', lw=2.0)
    # Dart stitch lines forming a slim V
    ax.plot([d1_x - 12, d1_x, d1_x + 12], [d1_top_y, d1_bot_y, d1_top_y], color='#444444', lw=1.2, linestyle=':')
    
    # Right front dart
    d2_x = cx1 + 140
    d2_top_y = cy1 + 198
    d2_bot_y = cy1 + 40
    ax.plot([d2_x, d2_x], [d2_top_y, d2_bot_y], color='#111111', lw=2.0)
    ax.plot([d2_x - 12, d2_x, d2_x + 12], [d2_top_y, d2_bot_y, d2_top_y], color='#444444', lw=1.2, linestyle=':')

    # Directional pressing arrows for darts (curving toward side seams)
    ax.annotate("", xy=(d1_x - 45, cy1 + 110), xytext=(d1_x - 10, cy1 + 110),
                arrowprops=dict(arrowstyle="->", lw=1.5, color='#333333', connectionstyle="arc3,rad=-0.2"))
    ax.annotate("", xy=(d2_x + 45, cy1 + 110), xytext=(d2_x + 10, cy1 + 110),
                arrowprops=dict(arrowstyle="->", lw=1.5, color='#333333', connectionstyle="arc3,rad=0.2"))

    # Labels for Panel 1
    ax.text(cx1, cy1 + 235, "Staystitch waistline (6 mm)", ha='center', fontfamily='sans-serif', fontsize=10.5, fontweight='bold', color='#111111')
    ax.text(d1_x - 55, cy1 + 80, "Press dart to side", ha='right', fontfamily='sans-serif', fontsize=9, color='#555555')
    ax.text(cx1, 100, "1. Staystitch front waist (6 mm) & stitch front waist darts on wrong side", ha='center', fontfamily='sans-serif', fontsize=12, fontweight='bold', color='#111111')
    ax.text(cx1, 70, "NO PLEATS: Keep front waistline completely flat and smooth", ha='center', fontfamily='sans-serif', fontsize=10, color='#8C3B47', fontweight='bold')

    # ---------------- PANEL 2: Steam-Press Center Crease (Folded Leg) ----------------
    cx2 = 1637
    cy2 = 530

    # Draw full trouser leg folded in half along center
    leg_pts = [
        (cx2 - 130, cy2 + 350), # top waist
        (cx2 + 130, cy2 + 350),
        (cx2 + 150, cy2 + 180), # hip
        (cx2 + 120, cy2 - 100), # knee
        (cx2 + 110, cy2 - 340), # hem right
        (cx2 - 110, cy2 - 340), # hem left
        (cx2 - 120, cy2 - 100), # knee
        (cx2 - 150, cy2 + 180), # crotch
    ]
    poly2 = patches.Polygon(leg_pts, closed=True, facecolor=C_FABRIC_RIGHT, edgecolor=C_STROKE_MAIN, lw=2.2)
    ax.add_patch(poly2)

    # Sharp vertical center crease line running straight down
    ax.plot([cx2, cx2], [cy2 + 340, cy2 - 340], color='#1E1A19', lw=2.0, linestyle='--', dashes=(6, 3))

    # Steam iron icon / illustration on crease
    iron_x = cx2 + 50
    iron_y = cy2 + 30
    iron_pts = [(iron_x, iron_y), (iron_x + 90, iron_y), (iron_x + 130, iron_y + 40), (iron_x, iron_y + 40)]
    iron = patches.Polygon(iron_pts, closed=True, facecolor='#D5D0C8', edgecolor='#111111', lw=1.8)
    ax.add_patch(iron)
    # Steam waves
    ax.plot([iron_x - 10, iron_x - 25], [iron_y + 10, iron_y + 10], color='#337AB7', lw=1.8, linestyle=':')
    ax.plot([iron_x - 10, iron_x - 25], [iron_y + 20, iron_y + 20], color='#337AB7', lw=1.8, linestyle=':')
    ax.plot([iron_x - 10, iron_x - 25], [iron_y + 30, iron_y + 30], color='#337AB7', lw=1.8, linestyle=':')

    # Labels for Panel 2
    ax.text(cx2 - 140, cy2 + 10, "Steam-press\nsharp crease", ha='right', va='center', fontfamily='sans-serif', fontsize=10, fontweight='bold', color='#111111')
    ax.text(cx2, 100, "2. Fold legs lengthwise matching seams; steam-press crisp center crease", ha='center', fontfamily='sans-serif', fontsize=12, fontweight='bold', color='#111111')
    ax.text(cx2, 70, "Fold matching inseam and side seam at knee and hemline", ha='center', fontfamily='sans-serif', fontsize=10, color='#555555')

    out_path = os.path.join(PANELS_DIR, "step1_flat_front_and_crease.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print("Saved step1_flat_front_and_crease.png at:", out_path)

def build_step7_fly_button_and_hem():
    fig, ax = plt.subplots(figsize=(11, 5.25), dpi=300)
    ax.set_xlim(0, 2200)
    ax.set_ylim(0, 1050)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(C_CONTAINER)
    ax.set_facecolor(C_CONTAINER)

    # Rounded outer border
    outer = patches.FancyBboxPatch((15, 15), 2170, 1020, boxstyle="round,pad=10,rounding_size=24",
                                  facecolor=C_CONTAINER, edgecolor=C_BORDER, lw=1.5)
    ax.add_patch(outer)

    # Box 1: Left Box (Waistband & Zipper Fly Button Closure)
    box1 = patches.Rectangle((45, 45), 1035, 960, facecolor=C_BOX_BG, edgecolor=C_STROKE_BOX, lw=3.0)
    ax.add_patch(box1)

    # Box 2: Right Box (Clean Weighted 4.0 cm Hem)
    box2 = patches.Rectangle((1120, 45), 1035, 960, facecolor=C_BOX_BG, edgecolor=C_STROKE_BOX, lw=3.0)
    ax.add_patch(box2)

    # Numbers 1. and 2.
    ax.text(80, 940, "1.", fontfamily='sans-serif', fontsize=26, fontweight='bold', color='#000000')
    ax.text(1155, 940, "2.", fontfamily='sans-serif', fontsize=26, fontweight='bold', color='#000000')

    # ---------------- PANEL 1: Attached Waistband over Zipper Fly & Buttonhole ----------------
    cx1 = 562
    cy1 = 530

    # Upper front of trouser (right side: fabric fill)
    f_body = [
        (cx1 - 280, cy1 + 120),
        (cx1 + 280, cy1 + 120),
        (cx1 + 310, cy1 - 70),
        (cx1 + 220, cy1 - 330),
        (cx1, cy1 - 250), # crotch
        (cx1 - 220, cy1 - 330),
        (cx1 - 310, cy1 - 70),
    ]
    ax.add_patch(patches.Polygon(f_body, closed=True, facecolor=C_FABRIC_RIGHT, edgecolor=C_STROKE_MAIN, lw=2.2))

    # Waistband strip attached on top (40 px tall in diagram)
    wb_pts = [
        (cx1 - 280, cy1 + 120),
        (cx1 - 280, cy1 + 240),
        (cx1 + 330, cy1 + 240), # Extension overlap tab on right
        (cx1 + 330, cy1 + 120),
    ]
    ax.add_patch(patches.Polygon(wb_pts, closed=True, facecolor='#F0ECE1', edgecolor=C_STROKE_MAIN, lw=2.2))
    # Waistband lower seam
    ax.plot([cx1 - 280, cx1 + 330], [cy1 + 120, cy1 + 120], color=C_STROKE_SEAM, lw=1.8)
    # Edge-stitching / stitch-in-the-ditch
    ax.plot([cx1 - 275, cx1 + 325], [cy1 + 125, cy1 + 125], color='#777777', lw=1.0, linestyle='--', dashes=(3, 2))

    # Center Front Seam
    ax.plot([cx1, cx1], [cy1 + 120, cy1 - 250], color=C_STROKE_SEAM, lw=1.8)

    # J-Stitch Fly Topstitching (Left overlap)
    fly_j = [
        (cx1, cy1 + 120),
        (cx1 - 65, cy1 + 120),
        (cx1 - 65, cy1 - 50),
        (cx1 - 40, cy1 - 100),
        (cx1, cy1 - 120),
    ]
    ax.plot([p[0] for p in fly_j[1:]], [p[1] for p in fly_j[1:]], color='#222222', lw=1.6, linestyle='--', dashes=(3, 3))
    ax.text(cx1 - 75, cy1 - 40, "Zipper Fly\nJ-Stitch", ha='right', va='center', fontfamily='sans-serif', fontsize=9.5, fontweight='bold', color='#111111')

    # Waistband Button & Buttonhole
    # Left tab buttonhole
    ax.plot([cx1 - 35, cx1 - 5], [cy1 + 180, cy1 + 180], color='#111111', lw=3.0)
    ax.plot([cx1 - 35, cx1 - 35], [cy1 + 173, cy1 + 187], color='#111111', lw=2.0)
    ax.plot([cx1 - 5, cx1 - 5], [cy1 + 173, cy1 + 187], color='#111111', lw=2.0)
    ax.text(cx1 - 20, cy1 + 205, "Buttonhole", ha='center', fontfamily='sans-serif', fontsize=9, color='#111111')

    # Right underlap horn button
    btn_x = cx1 + 55
    btn_y = cy1 + 180
    ax.add_patch(patches.Circle((btn_x, btn_y), radius=14, facecolor='#FFFFFF', edgecolor='#111111', lw=1.6))
    ax.plot([btn_x - 5, btn_x + 5], [btn_y, btn_y], color='#111111', lw=1.2)
    ax.plot([btn_x, btn_x], [btn_y - 5, btn_y + 5], color='#111111', lw=1.2)
    ax.text(btn_x, cy1 + 205, "Horn Button", ha='center', fontfamily='sans-serif', fontsize=9, color='#111111')

    # Belt loops caught in waistband
    ax.add_patch(patches.Rectangle((cx1 - 130, cy1 + 105), 18, 145, facecolor='#FAF8F5', edgecolor='#111111', lw=1.4))
    ax.add_patch(patches.Rectangle((cx1 + 160, cy1 + 105), 18, 145, facecolor='#FAF8F5', edgecolor='#111111', lw=1.4))

    # Labels for Panel 1
    ax.text(cx1, 100, "1. Attach waistband over zipper fly; finish ends & sew button closure", ha='center', fontfamily='sans-serif', fontsize=12, fontweight='bold', color='#111111')
    ax.text(cx1, 70, "Left end flush with fly shield; buttonhole centered above zipper line", ha='center', fontfamily='sans-serif', fontsize=10, color='#555555')

    # ---------------- PANEL 2: Clean 4.0 cm Weighted Hem Fold-up ----------------
    cx2 = 1637
    cy2 = 530

    # Lower trouser leg (hem)
    leg_w = 260
    leg_pts = [
        (cx2 - leg_w, cy2 + 300),
        (cx2 + leg_w, cy2 + 300),
        (cx2 + leg_w, cy2 - 180),
        (cx2 - leg_w, cy2 - 180),
    ]
    ax.add_patch(patches.Polygon(leg_pts, closed=True, facecolor=C_FABRIC_RIGHT, edgecolor=C_STROKE_MAIN, lw=2.2))

    # Folded-up hem section (wrong side turned up on inside, or transparent cutaway)
    hem_h = 130 # Represents 4.0 cm hem
    ax.add_patch(patches.Rectangle((cx2 - leg_w + 3, cy2 - 180), 2*leg_w - 6, hem_h, facecolor=C_FABRIC_WRONG, edgecolor=C_STROKE_SEAM, lw=1.8))
    
    # 1.0 cm turned-under raw edge
    ax.plot([cx2 - leg_w + 5, cx2 + leg_w - 5], [cy2 - 180 + hem_h - 30, cy2 - 180 + hem_h - 30], color='#666666', lw=1.2, linestyle=':')

    # Blind-hem stitch / topstitch line along upper hem edge
    ax.plot([cx2 - leg_w + 5, cx2 + leg_w - 5], [cy2 - 180 + hem_h, cy2 - 180 + hem_h], color='#222222', lw=1.8, linestyle='--', dashes=(4, 3))

    # Double-headed measurement arrow showing 4.0 cm
    arr_x = cx2 + leg_w + 40
    ax.annotate("", xy=(arr_x, cy2 - 180), xytext=(arr_x, cy2 - 180 + hem_h),
                arrowprops=dict(arrowstyle="<->", lw=1.8, color='#8C3B47'))
    ax.text(arr_x + 15, cy2 - 180 + hem_h/2, "4.0 cm\n(1 5/8 in)", va='center', fontfamily='sans-serif', fontsize=10, fontweight='bold', color='#8C3B47')

    # Upward pressing arrow
    ax.annotate("", xy=(cx2, cy2 - 180 + hem_h + 40), xytext=(cx2, cy2 - 150),
                arrowprops=dict(arrowstyle="->", lw=2.0, color='#111111'))
    ax.text(cx2 + 20, cy2 - 100, "Fold & press up 4 cm", fontfamily='sans-serif', fontsize=10, fontweight='bold', color='#111111')

    # Labels for Panel 2
    ax.text(cx2, 100, "2. Turn up 4.0 cm (1 5/8 in) hem; press and blind-stitch securely", ha='center', fontfamily='sans-serif', fontsize=12, fontweight='bold', color='#111111')
    ax.text(cx2, 70, "Fold 1.0 cm under, then 3.0 cm up for clean, weighted waterfall drape", ha='center', fontfamily='sans-serif', fontsize=10, color='#555555')

    out_path = os.path.join(PANELS_DIR, "step7_trouser_fly_and_waistband.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print("Saved step7_trouser_fly_and_waistband.png at:", out_path)

if __name__ == "__main__":
    build_step1_flat_front()
    build_step7_fly_button_and_hem()
