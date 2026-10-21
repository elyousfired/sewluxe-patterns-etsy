"""
Generate pristine, accurate CAD vector diagram panels for SewLuxe Colette Trousers:
1. pieces_overview_colette_clean.png (8 exact pieces: 1 Front, 2 Back with 2 darts, 3 Waistband, 4 Pocket Bag, 5 Fly Shield, 6 Pocket Facing, 7 Fly Interfacing, BL Belt Loops).
2. Clean Step Panels conforming 100% to luxury tailoring rules (Concealed Hook & Bar, 5 Belt Loops, Double Pleats).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np
import os

ASSET_DIR = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\colette_pants_engine\booklet_assets"
os.makedirs(ASSET_DIR, exist_ok=True)

# Colors
BG_COLOR = "#F5F2EF"
BOX_BG = "#FFFFFF"
BORDER_COLOR = "#1E1A19"
ACCENT_BURGUNDY = "#8C3B47"
SHADING_GRAY = "#E8E5E2"
DASH_SEAM = "#666666"

def create_pieces_overview():
    """Generates 300 DPI clean diagram of exactly the 8 Colette pattern pieces."""
    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 75)
    ax.axis("off")
    
    # -------------------------------------------------------------
    # 1. Pants Front (Left, tall)
    # -------------------------------------------------------------
    # Pants Front Polygon: Waist with slant pocket cutoff, fly curve, wide leg, hem
    front_pts = np.array([
        [12, 68],   # center front waist
        [22, 68],   # waist before slant
        [27, 58],   # slant pocket opening
        [28, 12],   # side hem
        [10, 12],   # inseam hem
        [10, 48],   # inseam crotch point
        [12, 54],   # fly bottom
        [12, 68]    # center front waist
    ])
    front_poly = patches.Polygon(front_pts, closed=True, facecolor=BOX_BG, edgecolor=BORDER_COLOR, lw=1.8)
    ax.add_patch(front_poly)
    
    # Pleat lines on front waist
    ax.plot([15, 15], [68, 60], color=ACCENT_BURGUNDY, lw=1.2, ls="--")
    ax.plot([17, 17], [68, 62], color=ACCENT_BURGUNDY, lw=1.2, ls="--")
    # Center Crease line down front leg
    ax.plot([19, 19], [60, 12], color="#999999", lw=1.0, ls="-.")
    
    ax.text(19, 35, "1. PANTS FRONT\n(Cut 2 Main Fabric)\n- Double Pleats\n- Slant Pocket Cutout\n- Center Crease", 
            ha="center", va="center", fontsize=7.5, fontweight="bold", color=BORDER_COLOR)

    # -------------------------------------------------------------
    # 2. Pants Back (Next to Front)
    # -------------------------------------------------------------
    # Pants Back Polygon: higher rise at center back, 2 darts, crotch extension, wide leg
    back_pts = np.array([
        [35, 71],   # center back waist (higher)
        [49, 67],   # side waist
        [49, 12],   # side hem
        [31, 12],   # inseam hem
        [31, 46],   # back crotch point
        [35, 52],   # center back curve
        [35, 71]    # center back waist
    ])
    back_poly = patches.Polygon(back_pts, closed=True, facecolor=BOX_BG, edgecolor=BORDER_COLOR, lw=1.8)
    ax.add_patch(back_poly)
    
    # 2 Contoured Back Waist Darts (V-shapes)
    # Dart 1
    d1_pts = np.array([[39, 69.5], [40, 62], [41, 69]])
    ax.add_patch(patches.Polygon(d1_pts, closed=True, facecolor=SHADING_GRAY, edgecolor=BORDER_COLOR, lw=1.0))
    # Dart 2
    d2_pts = np.array([[44, 68.3], [45, 61], [46, 67.8]])
    ax.add_patch(patches.Polygon(d2_pts, closed=True, facecolor=SHADING_GRAY, edgecolor=BORDER_COLOR, lw=1.0))
    
    # Center Crease line down back leg
    ax.plot([40, 40], [58, 12], color="#999999", lw=1.0, ls="-.")
    
    ax.text(40, 35, "2. PANTS BACK\n(Cut 2 Main Fabric)\n- Clean Pocketless Back\n- 2 Contoured Darts\n- Center Back Seam", 
            ha="center", va="center", fontsize=7.5, fontweight="bold", color=BORDER_COLOR)

    # -------------------------------------------------------------
    # 3. Tailored Waistband (Right top, horizontal)
    # -------------------------------------------------------------
    wb_pts = np.array([[55, 66], [95, 66], [95, 59], [55, 59]])
    wb_poly = patches.Polygon(wb_pts, closed=True, facecolor=BOX_BG, edgecolor=BORDER_COLOR, lw=1.5)
    ax.add_patch(wb_poly)
    # Extension tab on left
    ax.plot([58, 58], [66, 59], color="#888888", lw=1.0, ls=":")
    ax.text(75, 62.5, "3. TAILORED WAISTBAND (Cut 1 Main + 1 Interfacing)\nWith Inside Hook & Bar Extension Tab", 
            ha="center", va="center", fontsize=7.0, fontweight="bold", color=BORDER_COLOR)

    # -------------------------------------------------------------
    # 4. Pocket Bag & 6. Pocket Facing / Lining
    # -------------------------------------------------------------
    # Pocket Bag (Piece 4)
    pbag_pts = np.array([[55, 52], [68, 52], [68, 36], [60, 34], [55, 42]])
    ax.add_patch(patches.Polygon(pbag_pts, closed=True, facecolor=BOX_BG, edgecolor=BORDER_COLOR, lw=1.4))
    ax.text(61.5, 43, "4. POCKET BAG\n(Cut 2 Main)", ha="center", va="center", fontsize=6.8, fontweight="bold", color=BORDER_COLOR)

    # Pocket Facing / Lining (Piece 6)
    pfacing_pts = np.array([[73, 52], [86, 52], [86, 36], [78, 34], [73, 42]])
    ax.add_patch(patches.Polygon(pfacing_pts, closed=True, facecolor=SHADING_GRAY, edgecolor=BORDER_COLOR, lw=1.4))
    ax.plot([73, 80], [42, 52], color=ACCENT_BURGUNDY, lw=1.2, ls="--")
    ax.text(79.5, 43, "6. POCKET LINING\n(Cut 2 Lining)", ha="center", va="center", fontsize=6.8, fontweight="bold", color=BORDER_COLOR)

    # -------------------------------------------------------------
    # 5. Fly Shield & 7. Fly Interfacing
    # -------------------------------------------------------------
    # Fly Shield (Piece 5)
    fshield_pts = np.array([[55, 28], [63, 28], [63, 16], [59, 14], [55, 16]])
    ax.add_patch(patches.Polygon(fshield_pts, closed=True, facecolor=BOX_BG, edgecolor=BORDER_COLOR, lw=1.4))
    ax.text(59, 21, "5. FLY SHIELD\n(Cut 1 Main)", ha="center", va="center", fontsize=6.5, fontweight="bold", color=BORDER_COLOR)

    # Fly Interfacing (Piece 7)
    fint_pts = np.array([[68, 28], [74, 28], [74, 16], [68, 16]])
    ax.add_patch(patches.Polygon(fint_pts, closed=True, facecolor="#D9D4CE", edgecolor=BORDER_COLOR, lw=1.2, ls="--"))
    ax.text(71, 22, "7. FLY FUSE\n(Cut 2)", ha="center", va="center", fontsize=6.5, fontweight="bold", color=BORDER_COLOR)

    # -------------------------------------------------------------
    # BL. Belt Loops (Piece BL)
    # -------------------------------------------------------------
    bl_pts = np.array([[80, 26], [95, 26], [95, 21], [80, 21]])
    ax.add_patch(patches.Polygon(bl_pts, closed=True, facecolor=BOX_BG, edgecolor=BORDER_COLOR, lw=1.4))
    ax.text(87.5, 23.5, "BL. BELT LOOPS STRIP (3.5 cm x 45 cm)\nYields 5 Tailored Loops", 
            ha="center", va="center", fontsize=6.2, fontweight="bold", color=BORDER_COLOR)

    # Legend box
    ax.text(50, 5, "AUTHENTIC SEWLUXE COLETTE PATTERN PIECES INVENTORY (8 PIECES TOTAL - ZERO WELT POCKETS)", 
            ha="center", va="center", fontsize=8.0, fontweight="bold", color=ACCENT_BURGUNDY,
            bbox=dict(boxstyle="round,pad=0.4", facecolor=BOX_BG, edgecolor=BORDER_COLOR, lw=1.0))
    
    out_path = os.path.join(ASSET_DIR, "pieces_overview_clean.png")
    plt.tight_layout()
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[+] Saved clean pieces overview to: {out_path}")

def create_step1_panel():
    """Step 1: Double Forward Pleats & Pressed Center Creases (Front legs only)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=300)
    fig.patch.set_facecolor(BG_COLOR)
    for ax in (ax1, ax2):
        ax.set_facecolor(BOX_BG)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis("off")
        # Border
        rect = patches.Rectangle((2, 2), 96, 96, fill=False, edgecolor=BORDER_COLOR, lw=1.5)
        ax.add_patch(rect)
        
    # Panel 1: Double Forward Pleats
    ax1.text(6, 90, "1.", fontsize=14, fontweight="bold", color=BORDER_COLOR)
    # Upper front pant waist
    w_pts = np.array([[20, 85], [80, 85], [80, 20], [20, 20]])
    ax1.add_patch(patches.Polygon(w_pts, closed=True, facecolor=SHADING_GRAY, edgecolor=BORDER_COLOR, lw=1.5))
    # Pleats folding
    ax1.plot([40, 40], [85, 45], color=BORDER_COLOR, lw=2.0)
    ax1.plot([46, 46], [85, 50], color=BORDER_COLOR, lw=2.0)
    # Curved direction arrow folding toward side
    ax1.annotate("", xy=(55, 80), xytext=(40, 80), arrowprops=dict(arrowstyle="->", lw=1.8, color=ACCENT_BURGUNDY))
    ax1.annotate("", xy=(61, 80), xytext=(46, 80), arrowprops=dict(arrowstyle="->", lw=1.8, color=ACCENT_BURGUNDY))
    ax1.plot([20, 80], [82, 82], color=ACCENT_BURGUNDY, lw=1.2, ls=":")
    ax1.text(50, 10, "Fold double forward pleats toward side seam\nand baste upper waist edge at 6 mm (1/4 in)", 
             ha="center", va="center", fontsize=8.0, fontweight="bold", color=BORDER_COLOR)

    # Panel 2: Razor Sharp Center Crease
    ax2.text(6, 90, "2.", fontsize=14, fontweight="bold", color=BORDER_COLOR)
    # Folded pant leg flat
    leg_pts = np.array([[30, 85], [70, 85], [70, 20], [30, 20]])
    ax2.add_patch(patches.Polygon(leg_pts, closed=True, facecolor=BOX_BG, edgecolor=BORDER_COLOR, lw=1.5))
    # Razor crease line
    ax2.plot([50, 50], [85, 20], color=ACCENT_BURGUNDY, lw=2.0, ls="-.")
    # Iron symbol
    ax2.text(50, 55, "PRESS WITH STEAM\n& CLAPPER", ha="center", va="center", fontsize=8.0, fontweight="bold", color=ACCENT_BURGUNDY,
             bbox=dict(boxstyle="round,pad=0.3", facecolor=BG_COLOR, edgecolor=ACCENT_BURGUNDY, lw=1.0))
    ax2.text(50, 10, "Press razor-sharp vertical center crease\nfrom main front pleat straight to bottom hem", 
             ha="center", va="center", fontsize=8.0, fontweight="bold", color=BORDER_COLOR)

    out_path = os.path.join(ASSET_DIR, "step1_panels.png")
    plt.tight_layout()
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[+] Saved clean step 1 panel to: {out_path}")

def create_step4_and_5_panels():
    """Generates distinct, accurate panels for Step 4 (Back Darts) and Step 5 (Inseams)."""
    # Step 4: Back Darts & Center Back Rise
    fig4, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=300)
    fig4.patch.set_facecolor(BG_COLOR)
    for ax in (ax1, ax2):
        ax.set_facecolor(BOX_BG)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis("off")
        ax.add_patch(patches.Rectangle((2, 2), 96, 96, fill=False, edgecolor=BORDER_COLOR, lw=1.5))
        
    ax1.text(6, 90, "1.", fontsize=14, fontweight="bold", color=BORDER_COLOR)
    # 2 darts stitching on back panel
    ax1.add_patch(patches.Polygon([[20, 85], [80, 85], [80, 25], [20, 25]], closed=True, facecolor=SHADING_GRAY, edgecolor=BORDER_COLOR, lw=1.5))
    ax1.plot([38, 40], [85, 50], color=ACCENT_BURGUNDY, lw=1.8)
    ax1.plot([42, 40], [85, 50], color=ACCENT_BURGUNDY, lw=1.8)
    ax1.plot([58, 60], [85, 50], color=ACCENT_BURGUNDY, lw=1.8)
    ax1.plot([62, 60], [85, 50], color=ACCENT_BURGUNDY, lw=1.8)
    ax1.text(50, 10, "Stitch 4 contoured waist darts (2 per leg)\nTie thread tails by hand at dart points", 
             ha="center", va="center", fontsize=8.0, fontweight="bold", color=BORDER_COLOR)
    
    ax2.text(6, 90, "2.", fontsize=14, fontweight="bold", color=BORDER_COLOR)
    # Center back seam
    ax2.add_patch(patches.Polygon([[30, 85], [70, 85], [70, 25], [30, 25]], closed=True, facecolor=BOX_BG, edgecolor=BORDER_COLOR, lw=1.5))
    ax2.plot([50, 50], [85, 35], color=ACCENT_BURGUNDY, lw=2.2, ls="--")
    ax2.text(50, 10, "Pin Pants Backs right sides together\nStitch center back rise at 1.0 cm and press open", 
             ha="center", va="center", fontsize=8.0, fontweight="bold", color=BORDER_COLOR)
             
    out4 = os.path.join(ASSET_DIR, "step4_darts_panel.png")
    fig4.tight_layout()
    fig4.savefig(out4, facecolor=fig4.get_facecolor(), edgecolor="none")
    plt.close(fig4)
    print(f"[+] Saved clean step 4 darts panel to: {out4}")

    # Step 5: Inseams & Crotch Curve
    fig5, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=300)
    fig5.patch.set_facecolor(BG_COLOR)
    for ax in (ax1, ax2):
        ax.set_facecolor(BOX_BG)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis("off")
        ax.add_patch(patches.Rectangle((2, 2), 96, 96, fill=False, edgecolor=BORDER_COLOR, lw=1.5))
        
    ax1.text(6, 90, "1.", fontsize=14, fontweight="bold", color=BORDER_COLOR)
    # Inner leg seam
    ax1.add_patch(patches.Polygon([[30, 85], [70, 85], [70, 20], [30, 20]], closed=True, facecolor=BOX_BG, edgecolor=BORDER_COLOR, lw=1.5))
    ax1.plot([30, 30], [85, 20], color=ACCENT_BURGUNDY, lw=2.2, ls="--")
    ax1.text(50, 10, "Pin Front to Back right sides together\nStitch inseams continuously from crotch to hem", 
             ha="center", va="center", fontsize=8.0, fontweight="bold", color=BORDER_COLOR)
             
    ax2.text(6, 90, "2.", fontsize=14, fontweight="bold", color=BORDER_COLOR)
    # U-shaped crotch curve
    ax2.add_patch(patches.Polygon([[25, 85], [75, 85], [75, 25], [25, 25]], closed=True, facecolor=SHADING_GRAY, edgecolor=BORDER_COLOR, lw=1.5))
    u_curve = patches.Arc((50, 60), 30, 40, theta1=180, theta2=360, color=ACCENT_BURGUNDY, lw=2.2, ls="--")
    ax2.add_patch(u_curve)
    ax2.text(50, 10, "Slide one leg inside the other\nStitch U-shaped crotch curve with double row", 
             ha="center", va="center", fontsize=8.0, fontweight="bold", color=BORDER_COLOR)
             
    out5 = os.path.join(ASSET_DIR, "step5_inseams_panel.png")
    fig5.tight_layout()
    fig5.savefig(out5, facecolor=fig5.get_facecolor(), edgecolor="none")
    plt.close(fig5)
    print(f"[+] Saved clean step 5 inseams panel to: {out5}")

def create_step7_panel():
    """Step 7: Concealed Trouser Hook & Bar Closure + Deep 5.0 cm Hem (ZERO BUTTONS)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=300)
    fig.patch.set_facecolor(BG_COLOR)
    for ax in (ax1, ax2):
        ax.set_facecolor(BOX_BG)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis("off")
        ax.add_patch(patches.Rectangle((2, 2), 96, 96, fill=False, edgecolor=BORDER_COLOR, lw=1.5))
        
    ax1.text(6, 90, "1.", fontsize=14, fontweight="bold", color=BORDER_COLOR)
    # Waistband extension with concealed Hook & Bar
    ax1.add_patch(patches.Polygon([[20, 75], [80, 75], [80, 40], [20, 40]], closed=True, facecolor=SHADING_GRAY, edgecolor=BORDER_COLOR, lw=1.5))
    # Inside metal hook & bar symbols
    ax1.plot([32, 32], [62, 53], color="#333333", lw=4.0)  # Metal Bar
    ax1.plot([68, 68], [62, 53], color="#333333", lw=4.0)  # Metal Hook base
    ax1.plot([68, 63], [57, 57], color="#333333", lw=3.0)  # Hook latch
    ax1.text(32, 70, "BAR", ha="center", fontsize=7.0, fontweight="bold", color=ACCENT_BURGUNDY)
    ax1.text(68, 70, "HOOK", ha="center", fontsize=7.0, fontweight="bold", color=ACCENT_BURGUNDY)
    ax1.text(50, 10, "CONCEALED TROUSER HOOK & BAR\nInstall metal bar on inside left, hook on right extension\nZERO BUTTONS VISIBLE ON EXTERIOR!", 
             ha="center", va="center", fontsize=7.8, fontweight="bold", color=BORDER_COLOR)

    ax2.text(6, 90, "2.", fontsize=14, fontweight="bold", color=BORDER_COLOR)
    # 5.0 cm weighted palazzo hem
    ax2.add_patch(patches.Polygon([[25, 85], [75, 85], [75, 25], [25, 25]], closed=True, facecolor=BOX_BG, edgecolor=BORDER_COLOR, lw=1.5))
    # Hem fold lines
    ax2.plot([25, 75], [45, 45], color=ACCENT_BURGUNDY, lw=2.0)
    ax2.plot([25, 75], [37, 37], color="#888888", lw=1.2, ls=":")
    ax2.annotate("5.0 cm (2.0 in) Fold", xy=(77, 45), xytext=(82, 35),
                 arrowprops=dict(arrowstyle="->", lw=1.2, color=ACCENT_BURGUNDY), fontsize=6.8, fontweight="bold", color=ACCENT_BURGUNDY)
    ax2.text(50, 10, "DEEP 5.0 CM (2.0 IN) WEIGHTED PALAZZO HEM\nPress edge 1 cm under, fold up 4 cm, blind-stitch\nProvides graceful waterfall drape over shoes", 
             ha="center", va="center", fontsize=7.8, fontweight="bold", color=BORDER_COLOR)

    out_path = os.path.join(ASSET_DIR, "step7_hook_and_hem_panel.png")
    plt.tight_layout()
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[+] Saved clean step 7 hook and hem panel to: {out_path}")

if __name__ == "__main__":
    create_pieces_overview()
    create_step1_panel()
    create_step4_and_5_panels()
    create_step7_panel()
    print("ALL CLEAN PANELS GENERATED SUCCESSFULLY!")
