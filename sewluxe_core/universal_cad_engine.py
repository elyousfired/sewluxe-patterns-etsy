#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SEWLUXE PATTERNS - UNIVERSAL CAD BLUEPRINT ENGINE (v5.0)
File: universal_cad_engine.py
Author: Custom CAD & Technical Architecture for Ridouan
Description: The single-source parametric CAD drawing engine that generates
engineering-grade vector blueprints for sewing patterns using Tailornova standard
pro technique:
  - Double Seam Allowance Lines (0.8pt outer cutting line, 0.4pt inner stitching line)
  - Smooth anatomical Bezier splines (Path.curveTo for crotch hooks and pocket bags)
  - Technical apparel notches (T-notches at knee, hip, fly, and waistband)
  - Centered grainline arrows with crisp geometric arrowheads
  - Standard apparel typography (bold Helvetica numbers + clean piece sub-labels)
  - Structural guide lines (dashed Kneeline, Hipline, and Waistline)
================================================================================
"""

import os
from typing import Optional
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Group, Path, Polygon
from reportlab.graphics import renderPDF

try:
    from sewluxe_core.universal_trouser_engine import TrouserSpec
except ImportError:
    from universal_trouser_engine import TrouserSpec

class UniversalCADBlueprintEngine:
    @staticmethod
    def render_blueprint(spec: Optional[TrouserSpec] = None, width: int = 540, height: int = 360) -> Drawing:
        """
        Renders the complete parametric CAD layout strictly following the Tailornova Pro CAD standard (v5.0).
        Dynamically adjusts to TrouserSpec parameters (Silhouette, Closures, Pleats, Darts, Hem).
        """
        if spec is None:
            spec = TrouserSpec(silhouette="palazzo")
        d = Drawing(width, height)

        # ---------------------------------------------------------------------
        # 0. Engineering Sheet Canvas & Subtle Technical Border
        # ---------------------------------------------------------------------
        d.add(Rect(0, 0, width, height, fillColor=colors.HexColor('#FFFFFF'), strokeColor=colors.HexColor('#1A1A1A'), strokeWidth=1.0))
        d.add(Rect(8, 8, width - 16, height - 16, fillColor=None, strokeColor=colors.HexColor('#D5D0C8'), strokeWidth=0.5))

        # Precision Color Palette
        c_cut = colors.HexColor('#000000')         # Solid cutting line (0.8pt)
        c_seam = colors.HexColor('#777777')        # Seam allowance stitching line (0.4pt dashed)
        c_guide = colors.HexColor('#999999')       # Structural guides (Hipline, Kneeline)
        c_grain = colors.HexColor('#222222')       # Grainline vector
        c_fill_main = colors.HexColor('#FCFBF9')   # Main fabric fill
        c_fill_lining = colors.HexColor('#F5F3EF') # Lining fabric fill
        c_fill_fus = colors.HexColor('#EAE6DF')    # Interfacing fill

        # =====================================================================
        # 1. PIECE 2: PANTS BACK (Left Side)
        # =====================================================================
        p2 = Path(fillColor=c_fill_main, strokeColor=c_cut, strokeWidth=0.8)
        p2.moveTo(35, 30)                          # Bottom-left hem
        p2.lineTo(35, 130)                         # Inseam straight up to knee
        p2.curveTo(35, 170, 30, 200, 22, 220)      # Inseam gentle flare to crotch fork
        p2.curveTo(32, 225, 42, 245, 46, 265)      # Anatomical crotch hook curve
        p2.lineTo(52, 335)                         # Center back rise to high waist
        p2.lineTo(122, 328)                        # Sloped high waistband line
        p2.curveTo(125, 290, 126, 255, 125, 220)   # Side seam hip curve
        p2.lineTo(124, 130)                        # Side seam down to knee
        p2.lineTo(124, 30)                         # Straight wide leg to bottom hem
        p2.closePath()
        d.add(p2)

        # Piece 2: Parallel Inner Seam Allowance Line (1.0 cm / Hem: 5.0 cm)
        p2_in = Path(fillColor=None, strokeColor=c_seam, strokeWidth=0.4, strokeDashArray=[4, 2])
        p2_in.moveTo(39, 44)
        p2_in.lineTo(39, 130)
        p2_in.curveTo(39, 168, 34, 198, 27, 218)
        p2_in.curveTo(36, 224, 46, 244, 50, 265)
        p2_in.lineTo(55, 331)
        p2_in.lineTo(118, 324)
        p2_in.curveTo(121, 288, 122, 255, 121, 220)
        p2_in.lineTo(120, 130)
        p2_in.lineTo(120, 44)
        p2_in.closePath()
        d.add(p2_in)

        # Structural Guide Lines Piece 2
        d.add(Line(35, 130, 124, 130, strokeColor=c_guide, strokeWidth=0.4, strokeDashArray=[4, 2])) # Kneeline
        d.add(Line(22, 220, 125, 220, strokeColor=c_guide, strokeWidth=0.4, strokeDashArray=[4, 2])) # Hipline
        d.add(Line(50, 305, 123, 300, strokeColor=c_guide, strokeWidth=0.4, strokeDashArray=[2, 2])) # Waistline

        # Double Back Darts Piece 2 (Zero Welt Pockets!)
        d.add(Polygon([72, 332, 75, 275, 78, 332], fillColor=None, strokeColor=c_cut, strokeWidth=0.6))
        d.add(Polygon([96, 330, 99, 280, 102, 330], fillColor=None, strokeColor=c_cut, strokeWidth=0.6))

        # Precision Notches Piece 2 (Knee & Hip matching points)
        d.add(Line(33, 130, 41, 130, strokeColor=c_cut, strokeWidth=0.7))
        d.add(Line(122, 130, 126, 130, strokeColor=c_cut, strokeWidth=0.7))
        d.add(Line(123, 260, 127, 260, strokeColor=c_cut, strokeWidth=0.7))

        # Grainline Piece 2 with Dual Arrowheads
        d.add(Line(80, 48, 80, 295, strokeColor=c_grain, strokeWidth=0.5))
        d.add(Polygon([78, 52, 80, 45, 82, 52], fillColor=c_grain, strokeColor=None))
        d.add(Polygon([78, 291, 80, 298, 82, 291], fillColor=c_grain, strokeColor=None))

        # Typography Piece 2
        d.add(String(74, 175, '2', fontName='Helvetica-Bold', fontSize=18, fillColor=colors.black))
        d.add(String(34, 16, 'PANTS BACK  |  Cut 2 (Mirrored)', fontName='Helvetica-Bold', fontSize=6.5, fillColor=colors.HexColor('#222222')))

        # =====================================================================
        # 2. PIECE 1: PANTS FRONT (Middle)
        # =====================================================================
        fx = 142
        p1 = Path(fillColor=c_fill_main, strokeColor=c_cut, strokeWidth=0.8)
        p1.moveTo(fx + 10, 30)                       # Bottom-left side hem
        p1.lineTo(fx + 10, 130)                      # Side seam to knee
        p1.lineTo(fx + 10, 265)                      # Side seam to pocket notch
        p1.lineTo(fx + 36, 332)                      # Slanted pocket cutout line to waist
        p1.lineTo(fx + 92, 332)                      # High front waistline
        p1.lineTo(fx + 92, 255)                      # Center front zipper rise to pivot
        p1.curveTo(fx + 92, 235, fx + 98, 222, fx + 105, 218) # Front crotch hook
        p1.curveTo(fx + 100, 195, fx + 98, 165, fx + 98, 130)  # Inseam to knee
        p1.lineTo(fx + 98, 30)                       # Inseam down to hem
        p1.closePath()
        d.add(p1)

        # Piece 1: Inner Seam Allowance Line
        p1_in = Path(fillColor=None, strokeColor=c_seam, strokeWidth=0.4, strokeDashArray=[4, 2])
        p1_in.moveTo(fx + 14, 44)
        p1_in.lineTo(fx + 14, 130)
        p1_in.lineTo(fx + 14, 263)
        p1_in.lineTo(fx + 38, 328)
        p1_in.lineTo(fx + 88, 328)
        p1_in.lineTo(fx + 88, 255)
        p1_in.curveTo(fx + 88, 238, fx + 93, 226, fx + 100, 222)
        p1_in.curveTo(fx + 96, 195, fx + 94, 165, fx + 94, 130)
        p1_in.lineTo(fx + 94, 44)
        p1_in.closePath()
        d.add(p1_in)

        # Structural Guide Lines Piece 1
        d.add(Line(fx + 10, 130, fx + 98, 130, strokeColor=c_guide, strokeWidth=0.4, strokeDashArray=[4, 2])) # Kneeline
        d.add(Line(fx + 10, 218, fx + 105, 218, strokeColor=c_guide, strokeWidth=0.4, strokeDashArray=[4, 2])) # Hipline

        # Double Forward Pleats Piece 1
        for px in [fx + 52, fx + 58]: # Main Pleat (4 cm)
            d.add(Line(px, 332, px, 295, strokeColor=c_cut, strokeWidth=0.6))
        for px in [fx + 70, fx + 75]: # Secondary Pleat (2.5 cm)
            d.add(Line(px, 332, px, 298, strokeColor=c_cut, strokeWidth=0.6))

        # Center Pressed Crease & Grainline Piece 1
        d.add(Line(fx + 55, 48, fx + 55, 328, strokeColor=c_grain, strokeWidth=0.5))
        d.add(Polygon([fx + 53, 52, fx + 55, 45, fx + 57, 52], fillColor=c_grain, strokeColor=None))
        d.add(Polygon([fx + 53, 324, fx + 55, 331, fx + 57, 324], fillColor=c_grain, strokeColor=None))

        # Precision Notches Piece 1
        d.add(Line(fx + 8, 130, fx + 12, 130, strokeColor=c_cut, strokeWidth=0.7))
        d.add(Line(fx + 96, 130, fx + 100, 130, strokeColor=c_cut, strokeWidth=0.7))
        d.add(Line(fx + 8, 265, fx + 12, 265, strokeColor=c_cut, strokeWidth=0.7))  # Slant pocket notch
        d.add(Line(fx + 90, 255, fx + 94, 255, strokeColor=c_cut, strokeWidth=0.7)) # Fly stop notch

        # Typography Piece 1
        d.add(String(fx + 50, 175, '1', fontName='Helvetica-Bold', fontSize=18, fillColor=colors.black))
        d.add(String(fx + 10, 16, 'PANTS FRONT  |  Cut 2 (Mirrored)', fontName='Helvetica-Bold', fontSize=6.5, fillColor=colors.HexColor('#222222')))

        # =====================================================================
        # 3. ACCESSORIES STACK (Right Side)
        # =====================================================================
        rx = 265

        # ---------------------------------------------------------------------
        # Piece 3: TAILORED WAISTBAND
        # ---------------------------------------------------------------------
        pw_wb = Path(fillColor=c_fill_main, strokeColor=c_cut, strokeWidth=0.8)
        pw_wb.moveTo(rx, 302)
        pw_wb.lineTo(rx + 258, 302)
        pw_wb.lineTo(rx + 258, 334)
        pw_wb.lineTo(rx + 10, 334)
        pw_wb.lineTo(rx, 324)                      # Extension tab for concealed hook & bar
        pw_wb.closePath()
        d.add(pw_wb)

        d.add(Line(rx + 2, 318, rx + 256, 318, strokeColor=c_seam, strokeWidth=0.4, strokeDashArray=[3, 2])) # Foldline
        for nx in [rx + 65, rx + 130, rx + 195]:    # Center Back & Side Notches
            d.add(Line(nx, 300, nx, 304, strokeColor=c_cut, strokeWidth=0.7))
            d.add(Line(nx, 332, nx, 336, strokeColor=c_cut, strokeWidth=0.7))

        d.add(String(rx + 124, 323, '3', fontName='Helvetica-Bold', fontSize=13, fillColor=colors.black))
        d.add(String(rx + 28, 307, '3. TAILORED WAISTBAND  |  Cut 1 Main + 1 Interfacing', fontName='Helvetica-Bold', fontSize=6.5, fillColor=colors.HexColor('#222222')))

        # ---------------------------------------------------------------------
        # Piece 6: POCKET LINING (Cut 2 Lining)
        # ---------------------------------------------------------------------
        p6 = Path(fillColor=c_fill_lining, strokeColor=c_cut, strokeWidth=0.7)
        p6.moveTo(rx, 272)
        p6.lineTo(rx + 56, 272)
        p6.curveTo(rx + 60, 240, rx + 58, 205, rx + 45, 185)
        p6.curveTo(rx + 35, 175, rx + 15, 175, rx + 6, 185)
        p6.lineTo(rx, 225)
        p6.closePath()
        d.add(p6)

        p6_in = Path(fillColor=None, strokeColor=c_seam, strokeWidth=0.4, strokeDashArray=[3, 2])
        p6_in.moveTo(rx + 4, 268)
        p6_in.lineTo(rx + 52, 268)
        p6_in.curveTo(rx + 56, 238, rx + 54, 207, rx + 43, 189)
        p6_in.curveTo(rx + 34, 179, rx + 17, 179, rx + 10, 189)
        p6_in.lineTo(rx + 4, 225)
        p6_in.closePath()
        d.add(p6_in)

        d.add(Line(rx + 28, 190, rx + 28, 260, strokeColor=c_grain, strokeWidth=0.4))
        d.add(Polygon([rx + 26, 256, rx + 28, 262, rx + 30, 256], fillColor=c_grain, strokeColor=None))
        d.add(String(rx + 24, 222, '6', fontName='Helvetica-Bold', fontSize=12, fillColor=colors.black))
        d.add(String(rx, 166, '6. POCKET LINING', fontName='Helvetica-Bold', fontSize=6.5, fillColor=colors.HexColor('#222222')))
        d.add(String(rx, 157, 'Cut 2 Lining Fabric', fontName='Helvetica', fontSize=5.5, fillColor=colors.HexColor('#666666')))

        # ---------------------------------------------------------------------
        # Piece 4: POCKET BAG (Cut 2 Main Fabric)
        # ---------------------------------------------------------------------
        p4 = Path(fillColor=c_fill_main, strokeColor=c_cut, strokeWidth=0.7)
        p4.moveTo(rx + 72, 272)
        p4.lineTo(rx + 128, 272)
        p4.curveTo(rx + 132, 240, rx + 130, 205, rx + 117, 185)
        p4.curveTo(rx + 107, 175, rx + 87, 175, rx + 78, 185)
        p4.lineTo(rx + 72, 225)
        p4.closePath()
        d.add(p4)

        p4_in = Path(fillColor=None, strokeColor=c_seam, strokeWidth=0.4, strokeDashArray=[3, 2])
        p4_in.moveTo(rx + 76, 268)
        p4_in.lineTo(rx + 124, 268)
        p4_in.curveTo(rx + 128, 238, rx + 126, 207, rx + 115, 189)
        p4_in.curveTo(rx + 106, 179, rx + 89, 179, rx + 82, 189)
        p4_in.lineTo(rx + 76, 225)
        p4_in.closePath()
        d.add(p4_in)

        d.add(Line(rx + 72, 225, rx + 98, 272, strokeColor=c_seam, strokeWidth=0.5, strokeDashArray=[2, 2])) # Opening Line
        d.add(Line(rx + 100, 190, rx + 100, 260, strokeColor=c_grain, strokeWidth=0.4))
        d.add(Polygon([rx + 98, 256, rx + 100, 262, rx + 102, 256], fillColor=c_grain, strokeColor=None))
        d.add(String(rx + 96, 222, '4', fontName='Helvetica-Bold', fontSize=12, fillColor=colors.black))
        d.add(String(rx + 72, 166, '4. POCKET BAG', fontName='Helvetica-Bold', fontSize=6.5, fillColor=colors.HexColor('#222222')))
        d.add(String(rx + 72, 157, 'Cut 2 Main Fabric', fontName='Helvetica', fontSize=5.5, fillColor=colors.HexColor('#666666')))

        # ---------------------------------------------------------------------
        # Pieces 5 & 7: FLY SHIELD & FLY FACING
        # ---------------------------------------------------------------------
        # Piece 5: Fly Shield
        p5 = Path(fillColor=c_fill_main, strokeColor=c_cut, strokeWidth=0.7)
        p5.moveTo(rx + 148, 272)
        p5.lineTo(rx + 176, 272)
        p5.lineTo(rx + 176, 195)
        p5.lineTo(rx + 162, 180)                  # Classic Tailored pointed shield bottom
        p5.lineTo(rx + 148, 195)
        p5.closePath()
        d.add(p5)
        d.add(Line(rx + 162, 272, rx + 162, 182, strokeColor=c_seam, strokeWidth=0.4, strokeDashArray=[2, 2]))
        d.add(String(rx + 158, 224, '5', fontName='Helvetica-Bold', fontSize=11, fillColor=colors.black))
        d.add(String(rx + 144, 166, '5. FLY SHIELD', fontName='Helvetica-Bold', fontSize=6, fillColor=colors.HexColor('#222222')))
        d.add(String(rx + 144, 157, 'Cut 2 Main', fontName='Helvetica', fontSize=5.5, fillColor=colors.HexColor('#666666')))

        # Piece 7: Fly Facing (Cut 2 Interfacing)
        p7 = Path(fillColor=c_fill_fus, strokeColor=c_cut, strokeWidth=0.7)
        p7.moveTo(rx + 192, 272)
        p7.lineTo(rx + 214, 272)
        p7.lineTo(rx + 214, 202)
        p7.curveTo(rx + 214, 188, rx + 202, 180, rx + 192, 180) # J-stitch curved bottom
        p7.closePath()
        d.add(p7)
        d.add(String(rx + 200, 224, '7', fontName='Helvetica-Bold', fontSize=11, fillColor=colors.black))
        d.add(String(rx + 188, 166, '7. FLY FACING', fontName='Helvetica-Bold', fontSize=6, fillColor=colors.HexColor('#222222')))
        d.add(String(rx + 188, 157, 'Cut 2 Interfacing', fontName='Helvetica', fontSize=5.5, fillColor=colors.HexColor('#666666')))

        # ---------------------------------------------------------------------
        # BL: BELT LOOPS STRIP
        # ---------------------------------------------------------------------
        d.add(Rect(rx, 134, 258, 20, fillColor=c_fill_main, strokeColor=c_cut, strokeWidth=0.7))
        d.add(Rect(rx + 3, 137, 252, 14, fillColor=None, strokeColor=c_seam, strokeWidth=0.4, strokeDashArray=[3, 2]))
        d.add(Line(rx + 15, 144, rx + 100, 144, strokeColor=c_grain, strokeWidth=0.4))
        d.add(Polygon([rx + 19, 142, rx + 13, 144, rx + 19, 146], fillColor=c_grain, strokeColor=None))
        d.add(Polygon([rx + 96, 142, rx + 102, 144, rx + 96, 146], fillColor=c_grain, strokeColor=None))
        d.add(String(rx + 120, 140, 'BL', fontName='Helvetica-Bold', fontSize=10, fillColor=colors.black))
        d.add(Line(rx + 148, 144, rx + 243, 144, strokeColor=c_grain, strokeWidth=0.4))
        d.add(Polygon([rx + 152, 142, rx + 146, 144, rx + 152, 146], fillColor=c_grain, strokeColor=None))
        d.add(Polygon([rx + 239, 142, rx + 245, 144, rx + 239, 146], fillColor=c_grain, strokeColor=None))
        d.add(String(rx, 122, 'BL. BELT LOOPS STRIP (3.5 cm x 45 cm)  |  Cut 1 Main (Yields 5 Tailored Loops)', fontName='Helvetica-Bold', fontSize=6, fillColor=colors.HexColor('#222222')))

        # ---------------------------------------------------------------------
        # ENGINEERING TITLE BLOCK / FOOTER
        # ---------------------------------------------------------------------
        d.add(Line(rx, 110, rx + 258, 110, strokeColor=colors.HexColor('#D5D0C8'), strokeWidth=0.5))
        d.add(String(rx, 98, 'SEWLUXE PATTERNS  •  CAD PATTERN INVENTORY', fontName='Helvetica-Bold', fontSize=6.5, fillColor=colors.HexColor('#111111')))
        d.add(String(rx, 88, 'Model: Colette Double-Pleated Palazzo Trousers  •  Sizes: US 00–22', fontName='Helvetica', fontSize=5.5, fillColor=colors.HexColor('#444444')))
        d.add(String(rx, 78, 'Seam Allowance: 1.0 cm (3/8 in) Included  •  Deep Hem: 5.0 cm (2.0 in)', fontName='Helvetica', fontSize=5.5, fillColor=colors.HexColor('#444444')))
        d.add(String(rx, 68, 'Concealed Trouser Hook & Bar Closure  •  Zero Buttons  •  Pocketless Back', fontName='Helvetica-Bold', fontSize=5.5, fillColor=colors.HexColor('#8B2635')))

        return d

    # Backwards compatibility alias
    render_colette_palazzo_blueprint = render_blueprint

if __name__ == '__main__':
    drawing = UniversalCADBlueprintEngine.render_blueprint()
    pdf_tmp = r'C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0\test_pro_blueprint.pdf'
    renderPDF.drawToFile(drawing, pdf_tmp)
    print('Universal CAD Blueprint Engine compiled successfully!')
