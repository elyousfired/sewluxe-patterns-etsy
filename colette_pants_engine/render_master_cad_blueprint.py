"""
Render the Master CAD Blueprint for Colette Palazzo Trousers (Page 7 Blueprint)
Combines the user's architectural framework with smooth Bezier curves and authentic CAD markings:
- Waistline, Hipline, Kneeline, Grainlines
- Smooth Bezier Crotch Curves (Back & Front)
- Smooth Teardrop Pocket Bags (Pieces 4 & 6)
- Chevron Fly Shield (Piece 5)
- Interfacing & Belt Loops (3.5 cm x 45 cm)
- Bold Burgundy Piece Numbers (1, 2, 3, 4, 5, 6, 7, BL)
"""

import os
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Polygon, Path, Group
import pymupdf as fitz
from reportlab.pdfgen import canvas

BRAIN_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0"
ASSET_DIR = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\colette_pants_engine\booklet_assets"
os.makedirs(ASSET_DIR, exist_ok=True)

OUT_PNG = os.path.join(BRAIN_DIR, "colette_cad_blueprint_preview.png")
OUT_ASSET = os.path.join(ASSET_DIR, "pieces_overview_clean.png")

def create_cad_blueprint_drawing(width: int = 540, height: int = 380) -> Drawing:
    d = Drawing(width, height)
    # Background Canvas
    d.add(Rect(0, 0, width, height, fillColor=colors.HexColor("#FAF8F5"), strokeColor=colors.HexColor("#D8D3CC"), strokeWidth=1.0))

    # Outer Margins
    c_burgundy = colors.HexColor("#8C3B47")
    c_charcoal = colors.HexColor("#1E1A19")
    c_grey_line = colors.HexColor("#9E9891")
    c_light_fill = colors.white
    c_fuse_fill = colors.HexColor("#EFEBE6")

    # =========================================================================
    # 1. PANTS BACK (#2) - LEFT PANEL
    # =========================================================================
    bx = 20
    by = 22
    bw = 100
    bh = 330
    
    # Smooth Bezier Path for Pants Back with realistic Crotch Curve
    p_back = Path(fillColor=c_light_fill, strokeColor=c_charcoal, strokeWidth=1.3)
    p_back.moveTo(bx, by)                            # Hem inner corner
    p_back.lineTo(bx + bw, by)                       # Hem outer corner
    p_back.lineTo(bx + bw - 4, by + bh - 40)         # Side hip curve up
    p_back.lineTo(bx + bw - 8, by + bh)              # Side waist
    p_back.lineTo(bx + 18, by + bh + 8)              # Center back waist (higher rise)
    p_back.lineTo(bx + 15, by + 225)                 # Upper center back rise
    # Smooth crotch curve (Bezier cubic curve!)
    p_back.curveTo(bx + 15, by + 195, bx + 6, by + 180, bx, by + 175)
    p_back.lineTo(bx, by)                            # Inseam straight down to hem
    p_back.closePath()
    d.add(p_back)

    # Reference Guideline: Waistline
    d.add(Line(bx + 16, by + bh - 8, bx + bw - 7, by + bh - 10, strokeColor=c_grey_line, strokeWidth=0.5, strokeDashArray=[2, 2]))
    d.add(String(bx + 20, by + bh - 6, "WAISTLINE", fontName="Helvetica", fontSize=4.2, fillColor=c_grey_line))

    # Reference Guideline: Hipline
    d.add(Line(bx + 8, by + 215, bx + bw - 5, by + 215, strokeColor=c_grey_line, strokeWidth=0.5, strokeDashArray=[4, 2]))
    d.add(String(bx + 12, by + 217, "HIPLINE", fontName="Helvetica", fontSize=4.2, fillColor=c_grey_line))

    # Reference Guideline: Kneeline
    d.add(Line(bx + 1, by + 115, bx + bw - 2, by + 115, strokeColor=c_grey_line, strokeWidth=0.5, strokeDashArray=[4, 2]))
    d.add(String(bx + 6, by + 117, "KNEELINE", fontName="Helvetica", fontSize=4.2, fillColor=c_grey_line))

    # Reference Guideline: Hem Allowance
    d.add(Line(bx, by + 18, bx + bw, by + 18, strokeColor=c_grey_line, strokeWidth=0.5, strokeDashArray=[2, 2]))
    d.add(String(bx + 18, by + 6, "HEM 2.0\" (5.0 cm)", fontName="Helvetica", fontSize=4.5, fillColor=c_grey_line))

    # 2 Contoured Back Waist Darts (Burgundy V-shapes)
    d.add(Polygon([bx + 38, by + bh + 4, bx + 42, by + bh - 48, bx + 46, by + bh + 3], fillColor=None, strokeColor=c_burgundy, strokeWidth=0.9))
    d.add(Polygon([bx + 62, by + bh + 1, bx + 66, by + bh - 44, bx + 70, by + bh], fillColor=None, strokeColor=c_burgundy, strokeWidth=0.9))

    # Grainline with Arrowhead
    gx = bx + 52
    d.add(Line(gx, by + 25, gx, by + 270, strokeColor=c_grey_line, strokeWidth=0.6, strokeDashArray=[6, 3]))
    d.add(Polygon([gx - 2, by + 265, gx, by + 272, gx + 2, by + 265], fillColor=c_grey_line, strokeColor=None))
    d.add(Polygon([gx - 2, by + 32, gx, by + 25, gx + 2, by + 32], fillColor=c_grey_line, strokeColor=None))
    d.add(String(gx + 3, by + 155, "GRAINLINE", fontName="Helvetica", fontSize=4.5, fillColor=c_grey_line))

    # Piece Label
    d.add(String(bx + 46, by + 180, "2", fontName="Helvetica-Bold", fontSize=18, fillColor=c_burgundy))
    d.add(String(bx + 12, by + 140, "PANTS BACK", fontName="Helvetica-Bold", fontSize=7.0, fillColor=c_charcoal))
    d.add(String(bx + 12, by + 131, "- Cut 2 (Mirrored Pair)", fontName="Helvetica", fontSize=5.5, fillColor=c_charcoal))
    d.add(String(bx + 12, by + 123, "- 2 Contoured Waist Darts", fontName="Helvetica", fontSize=5.5, fillColor=c_charcoal))
    d.add(String(bx + 12, by + 115, "- Clean Pocketless Back", fontName="Helvetica", fontSize=5.5, fillColor=c_charcoal))

    # =========================================================================
    # 2. PANTS FRONT (#1) - MIDDLE PANEL
    # =========================================================================
    fx = 145
    fy = 22
    fw = 96
    fh = 330

    p_front = Path(fillColor=c_light_fill, strokeColor=c_charcoal, strokeWidth=1.3)
    p_front.moveTo(fx, fy)                           # Hem inner corner
    p_front.lineTo(fx + fw, fy)                      # Hem outer corner
    p_front.lineTo(fx + fw - 2, fy + 230)            # Side hip up to slant pocket notch
    p_front.lineTo(fx + fw - 16, fy + fh - 2)        # Slant pocket opening cutout
    p_front.lineTo(fx + 18, fy + fh)                 # Waist edge with pleats
    p_front.lineTo(fx + 18, fy + 245)                # Center front fly extension
    # Smooth front crotch curve (Bezier cubic curve!)
    p_front.curveTo(fx + 18, fy + 215, fx + 6, by + 185, fx, fy + 180)
    p_front.lineTo(fx, fy)                           # Inseam straight down to hem
    p_front.closePath()
    d.add(p_front)

    # Reference Guideline: Waistline
    d.add(Line(fx + 18, fy + fh - 8, fx + fw - 15, fy + fh - 9, strokeColor=c_grey_line, strokeWidth=0.5, strokeDashArray=[2, 2]))
    d.add(String(fx + 22, fy + fh - 6, "WAISTLINE", fontName="Helvetica", fontSize=4.2, fillColor=c_grey_line))

    # Reference Guideline: Hipline
    d.add(Line(fx + 8, fy + 215, fx + fw - 3, fy + 215, strokeColor=c_grey_line, strokeWidth=0.5, strokeDashArray=[4, 2]))
    d.add(String(fx + 12, fy + 217, "HIPLINE", fontName="Helvetica", fontSize=4.2, fillColor=c_grey_line))

    # Reference Guideline: Kneeline
    d.add(Line(fx + 1, fy + 115, fx + fw - 1, fy + 115, strokeColor=c_grey_line, strokeWidth=0.5, strokeDashArray=[4, 2]))
    d.add(String(fx + 6, fy + 117, "KNEELINE", fontName="Helvetica", fontSize=4.2, fillColor=c_grey_line))

    # Reference Guideline: Hem Allowance
    d.add(Line(fx, fy + 18, fx + fw, fy + 18, strokeColor=c_grey_line, strokeWidth=0.5, strokeDashArray=[2, 2]))
    d.add(String(fx + 18, fy + 6, "HEM 2.0\" (5.0 cm)", fontName="Helvetica", fontSize=4.5, fillColor=c_grey_line))

    # Double Forward Pleats Marks (Burgundy with arrows toward side)
    for px in [fx + 34, fx + 42]:
        d.add(Line(px, fy + fh, px, fy + fh - 32, strokeColor=c_burgundy, strokeWidth=1.0))
        d.add(Line(px + 4, fy + fh, px + 4, fy + fh - 32, strokeColor=c_burgundy, strokeWidth=0.6, strokeDashArray=[2, 2]))
    d.add(String(fx + 30, fy + fh - 38, "DOUBLE PLEATS", fontName="Helvetica-Bold", fontSize=4.8, fillColor=c_burgundy))

    # Slant Pocket Opening line
    d.add(Line(fx + fw - 16, fy + fh - 2, fx + fw - 2, fy + 230, strokeColor=c_burgundy, strokeWidth=1.1, strokeDashArray=[3, 2]))
    d.add(String(fx + fw - 34, fy + 255, "POCKET LINE", fontName="Helvetica", fontSize=4.5, fillColor=c_burgundy))

    # Center Pressed Crease Line (Dashed)
    cx = fx + 46
    d.add(Line(cx, fy + 20, cx, fy + fh - 35, strokeColor=colors.HexColor("#777777"), strokeWidth=0.7, strokeDashArray=[5, 3]))
    d.add(String(cx + 3, fy + 155, "CENTER CREASE", fontName="Helvetica", fontSize=4.5, fillColor=c_grey_line))

    # Piece Label
    d.add(String(fx + 42, fy + 180, "1", fontName="Helvetica-Bold", fontSize=18, fillColor=c_burgundy))
    d.add(String(fx + 12, by + 140, "PANTS FRONT", fontName="Helvetica-Bold", fontSize=7.0, fillColor=c_charcoal))
    d.add(String(fx + 12, by + 131, "- Cut 2 (Mirrored Pair)", fontName="Helvetica", fontSize=5.5, fillColor=c_charcoal))
    d.add(String(fx + 12, by + 123, "- Double Forward Pleats", fontName="Helvetica", fontSize=5.5, fillColor=c_charcoal))
    d.add(String(fx + 12, by + 115, "- Slant Italian Pocket Cutout", fontName="Helvetica", fontSize=5.5, fillColor=c_charcoal))

    # =========================================================================
    # 3. ACCESSORIES & TAILORING DETAILS - RIGHT SIDE
    # =========================================================================
    rx = 265

    # Piece 3: Tailored Waistband (Horizontal strip with extension tab)
    wb_y = 315
    wb_w = 255
    wb_h = 32
    d.add(Rect(rx, wb_y, wb_w, wb_h, fillColor=c_light_fill, strokeColor=c_charcoal, strokeWidth=1.2))
    # Fold line in middle
    d.add(Line(rx, wb_y + wb_h/2, rx + wb_w, wb_y + wb_h/2, strokeColor=c_grey_line, strokeWidth=0.6, strokeDashArray=[4, 2]))
    # Extension tab line
    d.add(Line(rx + 18, wb_y, rx + 18, wb_y + wb_h, strokeColor=c_burgundy, strokeWidth=0.8, strokeDashArray=[2, 2]))
    d.add(String(rx + 5, wb_y + 12, "TAB", fontName="Helvetica-Bold", fontSize=5.0, fillColor=c_burgundy))
    d.add(String(rx + 85, wb_y + 19, "3. TAILORED WAISTBAND", fontName="Helvetica-Bold", fontSize=8.0, fillColor=c_burgundy))
    d.add(String(rx + 65, wb_y + 8, "Cut 1 Main Fabric + 1 Fusible Interfacing | With Inside Hook & Bar Tab", fontName="Helvetica", fontSize=5.2, fillColor=c_charcoal))

    # Piece 6: Pocket Lining (Smooth Teardrop Curve)
    p6_x = rx
    p6_y = 195
    p6 = Path(fillColor=c_light_fill, strokeColor=c_charcoal, strokeWidth=1.2)
    p6.moveTo(p6_x, p6_y + 90)
    p6.lineTo(p6_x + 55, p6_y + 90)
    p6.lineTo(p6_x + 55, p6_y + 40)
    p6.curveTo(p6_x + 55, p6_y + 10, p6_x + 35, p6_y, p6_x + 15, p6_y)
    p6.curveTo(p6_x + 5, p6_y, p6_x, p6_y + 10, p6_x, p6_y + 25)
    p6.closePath()
    d.add(p6)
    # Slant opening cut
    d.add(Line(p6_x + 55, p6_y + 90, p6_x + 10, p6_y + 50, strokeColor=c_burgundy, strokeWidth=0.9, strokeDashArray=[2, 2]))
    d.add(String(p6_x + 24, p6_y + 35, "6", fontName="Helvetica-Bold", fontSize=13, fillColor=c_burgundy))
    d.add(String(p6_x + 4, p6_y + 12, "POCKET LINING", fontName="Helvetica-Bold", fontSize=5.6, fillColor=c_charcoal))
    d.add(String(p6_x + 4, p6_y + 5, "Cut 2 Lining Fabric", fontName="Helvetica", fontSize=4.8, fillColor=c_charcoal))

    # Piece 4: Pocket Bag Facing (Smooth Teardrop Curve)
    p4_x = rx + 75
    p4_y = 195
    p4 = Path(fillColor=c_light_fill, strokeColor=c_charcoal, strokeWidth=1.2)
    p4.moveTo(p4_x, p4_y + 90)
    p4.lineTo(p4_x + 55, p4_y + 90)
    p4.lineTo(p4_x + 55, p4_y + 40)
    p4.curveTo(p4_x + 55, p4_y + 10, p4_x + 35, p4_y, p4_x + 15, p4_y)
    p4.curveTo(p4_x + 5, p4_y, p4_x, p4_y + 10, p4_x, p4_y + 25)
    p4.closePath()
    d.add(p4)
    d.add(String(p4_x + 24, p4_y + 45, "4", fontName="Helvetica-Bold", fontSize=13, fillColor=c_burgundy))
    d.add(String(p4_x + 4, p4_y + 12, "POCKET BAG", fontName="Helvetica-Bold", fontSize=5.6, fillColor=c_charcoal))
    d.add(String(p4_x + 4, p4_y + 5, "Cut 2 Main Fabric", fontName="Helvetica", fontSize=4.8, fillColor=c_charcoal))

    # Piece 5: Fly Facing Shield (With authentic folded chevron end!)
    f5_x = rx + 150
    f5_y = 195
    f5 = Path(fillColor=c_light_fill, strokeColor=c_charcoal, strokeWidth=1.2)
    f5.moveTo(f5_x, f5_y + 90)
    f5.lineTo(f5_x + 30, f5_y + 90)
    f5.lineTo(f5_x + 30, f5_y + 15)
    f5.lineTo(f5_x + 15, f5_y)                       # Chevron point
    f5.lineTo(f5_x, f5_y + 15)
    f5.closePath()
    d.add(f5)
    d.add(Line(f5_x + 15, f5_y + 15, f5_x + 15, f5_y + 90, strokeColor=c_grey_line, strokeWidth=0.5, strokeDashArray=[3, 2]))
    d.add(String(f5_x + 11, f5_y + 45, "5", fontName="Helvetica-Bold", fontSize=12, fillColor=c_burgundy))
    d.add(String(f5_x + 2, f5_y + 15, "FLY SHIELD", fontName="Helvetica-Bold", fontSize=5.0, fillColor=c_charcoal))
    d.add(String(f5_x + 2, f5_y + 8, "Cut 1 Main", fontName="Helvetica", fontSize=4.5, fillColor=c_charcoal))

    # Piece 7: Fly Extension Interfacing
    f7_x = rx + 195
    f7_y = 195
    d.add(Rect(f7_x, f7_y + 15, 24, 75, fillColor=c_fuse_fill, strokeColor=c_charcoal, strokeWidth=1.0))
    d.add(String(f7_x + 8, f7_y + 50, "7", fontName="Helvetica-Bold", fontSize=11, fillColor=c_burgundy))
    d.add(String(f7_x + 2, f7_y + 28, "FLY FUSE", fontName="Helvetica-Bold", fontSize=4.8, fillColor=c_charcoal))
    d.add(String(f7_x + 2, f7_y + 20, "Cut 2 Fuse", fontName="Helvetica", fontSize=4.2, fillColor=c_charcoal))

    # Piece BL: Belt Loops Strip (3.5 cm x 45 cm)
    bl_y = 145
    d.add(Rect(rx, bl_y, 255, 20, fillColor=c_light_fill, strokeColor=c_charcoal, strokeWidth=1.1))
    # 5 loop cut tick marks
    for lx in range(1, 5):
        d.add(Line(rx + lx * 51, bl_y, rx + lx * 51, bl_y + 20, strokeColor=c_grey_line, strokeWidth=0.6, strokeDashArray=[2, 2]))
    d.add(String(rx + 45, bl_y + 7, "BL. BELT LOOPS STRIP (3.5 cm x 45 cm) - Yields 5 Tailored Loops", fontName="Helvetica-Bold", fontSize=6.5, fillColor=c_burgundy))

    # Bottom Technical Metadata Banner
    banner_y = 22
    d.add(Rect(rx, banner_y, 255, 95, fillColor=colors.HexColor("#F2EFEA"), strokeColor=c_grey_line, strokeWidth=0.8))
    d.add(String(rx + 12, banner_y + 78, "SEWLUXE COLETTE PATTERN INVENTORY", fontName="Helvetica-Bold", fontSize=7.2, fillColor=c_burgundy))
    d.add(String(rx + 12, banner_y + 64, "* Total Garment Pieces: 8 Pieces (All Seam Allowances Included)", fontName="Helvetica", fontSize=5.6, fillColor=c_charcoal))
    d.add(String(rx + 12, banner_y + 52, "* Standard Seam Allowance: 1.0 cm (3/8 in) on all joining edges", fontName="Helvetica", fontSize=5.6, fillColor=c_charcoal))
    d.add(String(rx + 12, banner_y + 40, "* Weighted Palazzo Hem Allowance: Deep 5.0 cm (2.0 in)", fontName="Helvetica", fontSize=5.6, fillColor=c_charcoal))
    d.add(String(rx + 12, banner_y + 28, "* Waistband Closure: Concealed Trouser Hook & Bar on Tab", fontName="Helvetica", fontSize=5.6, fillColor=c_charcoal))
    d.add(String(rx + 12, banner_y + 16, "* Tailoring Specification: Clean Pocketless Back + 4 Waist Darts", fontName="Helvetica", fontSize=5.6, fillColor=c_charcoal))

    return d

def render_drawing_to_png(drawing: Drawing, out_png_path: str, dpi: int = 300):
    """Renders a ReportLab Drawing to a pristine high-resolution 300 DPI PNG via PyMuPDF."""
    temp_pdf = out_png_path.replace(".png", "_temp.pdf")
    c = canvas.Canvas(temp_pdf, pagesize=(drawing.width, drawing.height))
    drawing.drawOn(c, 0, 0)
    c.showPage()
    c.save()

    doc = fitz.open(temp_pdf)
    page = doc[0]
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    pix.save(out_png_path)
    doc.close()
    if os.path.exists(temp_pdf):
        os.remove(temp_pdf)
    print(f"[SUCCESS] Rendered 300 DPI CAD Blueprint to: {out_png_path}")

if __name__ == "__main__":
    d = create_cad_blueprint_drawing(540, 380)
    render_drawing_to_png(d, OUT_PNG, dpi=300)
    render_drawing_to_png(d, OUT_ASSET, dpi=300)
    print("FINISHED RENDERING CAD BLUEPRINT!")
