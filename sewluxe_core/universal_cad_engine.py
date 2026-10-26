#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SEWLUXE PATTERNS - UNIVERSAL CAD BLUEPRINT & DIAGRAM ENGINE (v5.0)
File: universal_cad_engine.py
Author: Custom CAD & Technical Architecture for Ridouan
Description: The single-source parametric CAD drawing engine that generates
engineering-grade vector blueprints and step-by-step sewing diagrams for ANY
trouser archetype strictly using Tailornova Pro standard technique:
  - Double Seam Allowance Lines (0.8pt outer cutting line, 0.4pt inner stitching line)
  - Smooth anatomical Bezier splines (Path.curveTo for crotch hooks, pocket curves, leg silhouettes)
  - Technical apparel notches (T-notches at knee, hip, fly, and waistband)
  - Centered grainline arrows with crisp geometric arrowheads
  - Standard apparel typography (bold Helvetica numbers + clean piece sub-labels)
  - Modular accessories stack based dynamically on TrouserSpec (Waistbands, Pockets, Fly, Belt Loops)
  - Authentic vector step diagrams (Right side white, Wrong side grey #E6E6E6, stitch lines dashed)
================================================================================
"""

import os
from typing import Optional, Dict, List, Tuple
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Group, Path, Polygon, Circle
from reportlab.graphics import renderPDF

try:
    from sewluxe_core.universal_trouser_engine import TrouserSpec, SILHOUETTE_RULES
except ImportError:
    from universal_trouser_engine import TrouserSpec, SILHOUETTE_RULES


class UniversalCADBlueprintEngine:
    """
    Parametric CAD Drawing Engine that dynamically adapts to ANY TrouserSpec.
    Zero hardcoded static layouts. Zero AI clutter.
    """

    @staticmethod
    def render_blueprint(spec: Optional[TrouserSpec] = None, width: int = 540, height: int = 360) -> Drawing:
        """
        Renders the complete parametric CAD layout sheet for the given trouser specification.
        Dynamically adjusts piece shapes, leg sweep, pleats, darts, pockets, closures, and belt loops.
        """
        if spec is None:
            spec = TrouserSpec(silhouette="palazzo")

        d = Drawing(width, height)

        # ---------------------------------------------------------------------
        # 0. Engineering Canvas & Technical Border
        # ---------------------------------------------------------------------
        d.add(Rect(0, 0, width, height, fillColor=colors.HexColor('#FFFFFF'), strokeColor=colors.HexColor('#1A1A1A'), strokeWidth=1.0))
        d.add(Rect(8, 8, width - 16, height - 16, fillColor=None, strokeColor=colors.HexColor('#D5D0C8'), strokeWidth=0.5))

        # Proportional Content Scaling Group (Base: 540x360)
        # Guarantees all CAD pattern pieces and technical blocks scale smoothly
        # and fit comfortably within ANY canvas dimensions without border collisions.
        g = Group()
        sx = width / 540.0
        sy = height / 360.0
        g.scale(sx, sy)

        # Precision Color Palette
        c_cut = colors.HexColor('#000000')         # Solid cutting line (0.8pt)
        c_seam = colors.HexColor('#777777')        # Seam allowance line (0.4pt dashed)
        c_guide = colors.HexColor('#999999')       # Structural guides (Hipline, Kneeline)
        c_grain = colors.HexColor('#222222')       # Grainline vector
        c_fill_main = colors.HexColor('#FCFBF9')   # Main fabric fill
        c_fill_lining = colors.HexColor('#F5F3EF') # Lining fabric fill
        c_fill_fus = colors.HexColor('#EAE6DF')    # Interfacing fill

        # Geometric adjustments based on silhouette
        is_palazzo = spec.silhouette == "palazzo"
        is_cigarette = spec.silhouette == "cigarette"
        is_barrel = spec.silhouette == "barrel_leg"
        is_elastic_waist = spec.closure_type == "pull_on_elastic" or spec.front_shaping == "elastic_gathered" or spec.back_shaping == "elastic_gathered"

        # Leg sweep width offsets
        hem_half_w = 45 if is_palazzo else (28 if is_cigarette else (36 if is_barrel else 38))
        knee_half_w = 44 if is_palazzo else (25 if is_cigarette else (46 if is_barrel else 34))
        hem_allowance_pt = min(spec.hem_allowance_cm * 2.8, 14.0)

        # =====================================================================
        # 1. PIECE 2: PANTS BACK (Left Side)
        # =====================================================================
        bx_center = 78
        bx_left_hem = bx_center - hem_half_w
        bx_right_hem = bx_center + hem_half_w
        bx_left_knee = bx_center - knee_half_w
        bx_right_knee = bx_center + knee_half_w

        p2 = Path(fillColor=c_fill_main, strokeColor=c_cut, strokeWidth=0.8)
        p2.moveTo(bx_left_hem, 30)                                    # Bottom-left hem
        p2.lineTo(bx_left_knee, 130)                                  # Inseam to knee
        p2.curveTo(bx_left_knee, 170, bx_center - 48, 200, bx_center - 56, 220) # Crotch fork
        p2.curveTo(bx_center - 46, 225, bx_center - 36, 245, bx_center - 32, 265) # Crotch hook
        p2.lineTo(bx_center - 26, 335)                                # Center back rise
        p2.lineTo(bx_center + 44, 328)                                # Waistline
        if is_barrel:
            p2.curveTo(bx_center + 58, 280, bx_center + 56, 220, bx_right_knee, 130) # Bowed barrel hip/side
        else:
            p2.curveTo(bx_center + 47, 290, bx_center + 48, 255, bx_right_knee, 220)
            p2.lineTo(bx_right_knee, 130)
        p2.lineTo(bx_right_hem, 30)                                   # Side to hem
        p2.closePath()
        g.add(p2)

        # Inner Seam Allowance Line Piece 2
        p2_in = Path(fillColor=None, strokeColor=c_seam, strokeWidth=0.4, strokeDashArray=[4, 2])
        p2_in.moveTo(bx_left_hem + 4, 30 + hem_allowance_pt)
        p2_in.lineTo(bx_left_knee + 4, 130)
        p2_in.curveTo(bx_left_knee + 4, 168, bx_center - 44, 198, bx_center - 51, 218)
        p2_in.curveTo(bx_center - 42, 224, bx_center - 32, 244, bx_center - 28, 265)
        p2_in.lineTo(bx_center - 23, 331)
        p2_in.lineTo(bx_center + 40, 324)
        p2_in.curveTo(bx_center + 43, 288, bx_center + 44, 255, bx_right_knee - 4, 220)
        p2_in.lineTo(bx_right_knee - 4, 130)
        p2_in.lineTo(bx_right_hem - 4, 30 + hem_allowance_pt)
        p2_in.closePath()
        g.add(p2_in)

        # Guides Piece 2
        g.add(Line(bx_left_knee, 130, bx_right_knee, 130, strokeColor=c_guide, strokeWidth=0.4, strokeDashArray=[4, 2])) # Kneeline
        g.add(Line(bx_center - 56, 220, bx_center + 47, 220, strokeColor=c_guide, strokeWidth=0.4, strokeDashArray=[4, 2])) # Hipline

        # Back Darts (If back_shaping == "4_darts")
        if spec.back_shaping == "4_darts":
            g.add(Polygon([bx_center - 6, 332, bx_center - 3, 275, bx_center, 332], fillColor=None, strokeColor=c_cut, strokeWidth=0.6))
            g.add(Polygon([bx_center + 18, 330, bx_center + 21, 280, bx_center + 24, 330], fillColor=None, strokeColor=c_cut, strokeWidth=0.6))
        elif spec.back_shaping == "2_darts":
            g.add(Polygon([bx_center + 6, 331, bx_center + 9, 275, bx_center + 12, 331], fillColor=None, strokeColor=c_cut, strokeWidth=0.6))
        elif is_elastic_waist:
            # Wavy gathered indication at waist
            for wx in range(int(bx_center - 20), int(bx_center + 40), 6):
                g.add(Line(wx, 332, wx + 3, 328, strokeColor=c_seam, strokeWidth=0.5))

        # Precision Notches Piece 2
        g.add(Line(bx_left_knee - 2, 130, bx_left_knee + 4, 130, strokeColor=c_cut, strokeWidth=0.7))
        g.add(Line(bx_right_knee - 4, 130, bx_right_knee + 2, 130, strokeColor=c_cut, strokeWidth=0.7))
        g.add(Line(bx_center + 45, 260, bx_center + 49, 260, strokeColor=c_cut, strokeWidth=0.7))

        # Grainline Piece 2
        g.add(Line(bx_center + 2, 48, bx_center + 2, 295, strokeColor=c_grain, strokeWidth=0.5))
        g.add(Polygon([bx_center, 52, bx_center + 2, 45, bx_center + 4, 52], fillColor=c_grain, strokeColor=None))
        g.add(Polygon([bx_center, 291, bx_center + 2, 298, bx_center + 4, 291], fillColor=c_grain, strokeColor=None))

        # Typography Piece 2
        g.add(String(bx_center - 4, 175, '2', fontName='Helvetica-Bold', fontSize=18, fillColor=colors.black))
        g.add(String(bx_left_hem, 16, 'PANTS BACK  |  Cut 2 (Mirrored)', fontName='Helvetica-Bold', fontSize=6.5, fillColor=colors.HexColor('#222222')))

        # =====================================================================
        # 2. PIECE 1: PANTS FRONT (Middle)
        # =====================================================================
        fx_center = 196
        fx_left_hem = fx_center - hem_half_w + 4
        fx_right_hem = fx_center + hem_half_w - 4
        fx_left_knee = fx_center - knee_half_w + 4
        fx_right_knee = fx_center + knee_half_w - 4

        p1 = Path(fillColor=c_fill_main, strokeColor=c_cut, strokeWidth=0.8)
        p1.moveTo(fx_left_hem, 30)                                    # Bottom-left side hem
        p1.lineTo(fx_left_knee, 130)                                  # Side to knee
        if spec.front_pockets == "slant_italian":
            p1.lineTo(fx_left_knee, 265)                              # Pocket notch
            p1.lineTo(fx_left_knee + 26, 332)                         # Slant pocket cut line to waist
        else:
            p1.lineTo(fx_left_knee, 265)
            p1.lineTo(fx_left_knee + 10, 332)                         # Clean continuous waist
        p1.lineTo(fx_center + 38, 332)                                # Front waist
        p1.lineTo(fx_center + 38, 255)                                # Fly rise
        p1.curveTo(fx_center + 38, 235, fx_center + 44, 222, fx_center + 51, 218) # Front crotch hook
        p1.curveTo(fx_center + 46, 195, fx_right_knee, 165, fx_right_knee, 130)  # Inseam to knee
        p1.lineTo(fx_right_hem, 30)                                   # Inseam to hem
        p1.closePath()
        g.add(p1)

        # Inner Seam Allowance Line Piece 1
        p1_in = Path(fillColor=None, strokeColor=c_seam, strokeWidth=0.4, strokeDashArray=[4, 2])
        p1_in.moveTo(fx_left_hem + 4, 30 + hem_allowance_pt)
        p1_in.lineTo(fx_left_knee + 4, 130)
        if spec.front_pockets == "slant_italian":
            p1_in.lineTo(fx_left_knee + 4, 263)
            p1_in.lineTo(fx_left_knee + 28, 328)
        else:
            p1_in.lineTo(fx_left_knee + 4, 263)
            p1_in.lineTo(fx_left_knee + 12, 328)
        p1_in.lineTo(fx_center + 34, 328)
        p1_in.lineTo(fx_center + 34, 255)
        p1_in.curveTo(fx_center + 34, 238, fx_center + 39, 226, fx_center + 46, 222)
        p1_in.curveTo(fx_center + 42, 195, fx_right_knee - 4, 165, fx_right_knee - 4, 130)
        p1_in.lineTo(fx_right_hem - 4, 30 + hem_allowance_pt)
        p1_in.closePath()
        g.add(p1_in)

        # Guides Piece 1
        g.add(Line(fx_left_knee, 130, fx_right_knee, 130, strokeColor=c_guide, strokeWidth=0.4, strokeDashArray=[4, 2])) # Kneeline
        g.add(Line(fx_left_knee, 218, fx_center + 51, 218, strokeColor=c_guide, strokeWidth=0.4, strokeDashArray=[4, 2])) # Hipline

        # Front Pleats / Shaping
        if spec.front_shaping == "double_pleats":
            for px in [fx_center - 2, fx_center + 4]: # Main Pleat (4 cm)
                g.add(Line(px, 332, px, 295, strokeColor=c_cut, strokeWidth=0.6))
            for px in [fx_center + 16, fx_center + 21]: # Secondary Pleat (2.5 cm)
                g.add(Line(px, 332, px, 298, strokeColor=c_cut, strokeWidth=0.6))
        elif spec.front_shaping == "single_pleat":
            for px in [fx_center + 2, fx_center + 8]:
                g.add(Line(px, 332, px, 295, strokeColor=c_cut, strokeWidth=0.6))
        elif spec.front_shaping == "front_darts":
            g.add(Polygon([fx_center, 332, fx_center + 3, 280, fx_center + 6, 332], fillColor=None, strokeColor=c_cut, strokeWidth=0.6))
        elif spec.front_shaping == "elastic_gathered":
            for wx in range(int(fx_left_knee + 15), int(fx_center + 35), 6):
                g.add(Line(wx, 332, wx + 3, 328, strokeColor=c_seam, strokeWidth=0.5))

        # Center Crease & Grainline Piece 1
        g.add(Line(fx_center + 1, 48, fx_center + 1, 328, strokeColor=c_grain, strokeWidth=0.5))
        g.add(Polygon([fx_center - 1, 52, fx_center + 1, 45, fx_center + 3, 52], fillColor=c_grain, strokeColor=None))
        g.add(Polygon([fx_center - 1, 324, fx_center + 1, 331, fx_center + 3, 324], fillColor=c_grain, strokeColor=None))

        # Notches Piece 1
        g.add(Line(fx_left_knee - 2, 130, fx_left_knee + 4, 130, strokeColor=c_cut, strokeWidth=0.7))
        g.add(Line(fx_right_knee - 4, 130, fx_right_knee + 2, 130, strokeColor=c_cut, strokeWidth=0.7))
        if spec.front_pockets == "slant_italian":
            g.add(Line(fx_left_knee - 2, 265, fx_left_knee + 4, 265, strokeColor=c_cut, strokeWidth=0.7))
        if not is_elastic_waist:
            g.add(Line(fx_center + 36, 255, fx_center + 40, 255, strokeColor=c_cut, strokeWidth=0.7)) # Fly stop notch

        # Typography Piece 1
        g.add(String(fx_center - 4, 175, '1', fontName='Helvetica-Bold', fontSize=18, fillColor=colors.black))
        g.add(String(fx_left_hem, 16, 'PANTS FRONT  |  Cut 2 (Mirrored)', fontName='Helvetica-Bold', fontSize=6.5, fillColor=colors.HexColor('#222222')))

        # =====================================================================
        # 3. ACCESSORIES STACK (Right Side) - DYNAMIC TO SPEC
        # =====================================================================
        rx = 265

        # ---------------------------------------------------------------------
        # Piece 3: WAISTBAND (Tailored or Elastic Casing)
        # ---------------------------------------------------------------------
        pw_wb = Path(fillColor=c_fill_main, strokeColor=c_cut, strokeWidth=0.8)
        pw_wb.moveTo(rx, 302)
        pw_wb.lineTo(rx + 258, 302)
        pw_wb.lineTo(rx + 258, 334)
        if spec.closure_type == "concealed_hook_bar":
            pw_wb.lineTo(rx + 10, 334)
            pw_wb.lineTo(rx, 324)  # Angled extension tab
        else:
            pw_wb.lineTo(rx, 334)  # Straight rectangular waistband
        pw_wb.closePath()
        g.add(pw_wb)

        g.add(Line(rx + 2, 318, rx + 256, 318, strokeColor=c_seam, strokeWidth=0.4, strokeDashArray=[3, 2]))
        for nx in [rx + 65, rx + 130, rx + 195]:
            g.add(Line(nx, 300, nx, 304, strokeColor=c_cut, strokeWidth=0.7))
            g.add(Line(nx, 332, nx, 336, strokeColor=c_cut, strokeWidth=0.7))

        wb_label = "3. TAILORED WAISTBAND  |  Cut 1 Main + 1 Interfacing" if not is_elastic_waist else "3. ELASTIC CASING WAISTBAND  |  Cut 1 Main"
        g.add(String(rx + 124, 323, '3', fontName='Helvetica-Bold', fontSize=13, fillColor=colors.black))
        g.add(String(rx + 28, 307, wb_label, fontName='Helvetica-Bold', fontSize=6.5, fillColor=colors.HexColor('#222222')))

        # ---------------------------------------------------------------------
        # POCKETS (Pieces 6 & 4 or In-seam or None)
        # ---------------------------------------------------------------------
        if spec.front_pockets == "slant_italian":
            # Piece 6: Pocket Lining
            p6 = Path(fillColor=c_fill_lining, strokeColor=c_cut, strokeWidth=0.7)
            p6.moveTo(rx, 272)
            p6.lineTo(rx + 56, 272)
            p6.curveTo(rx + 60, 240, rx + 58, 205, rx + 45, 185)
            p6.curveTo(rx + 35, 175, rx + 15, 175, rx + 6, 185)
            p6.lineTo(rx, 225)
            p6.closePath()
            g.add(p6)

            p6_in = Path(fillColor=None, strokeColor=c_seam, strokeWidth=0.4, strokeDashArray=[3, 2])
            p6_in.moveTo(rx + 4, 268)
            p6_in.lineTo(rx + 52, 268)
            p6_in.curveTo(rx + 56, 238, rx + 54, 207, rx + 43, 189)
            p6_in.curveTo(rx + 34, 179, rx + 17, 179, rx + 10, 189)
            p6_in.lineTo(rx + 4, 225)
            p6_in.closePath()
            g.add(p6_in)

            g.add(String(rx + 24, 222, '6', fontName='Helvetica-Bold', fontSize=12, fillColor=colors.black))
            g.add(String(rx, 166, '6. POCKET LINING', fontName='Helvetica-Bold', fontSize=6.5, fillColor=colors.HexColor('#222222')))
            g.add(String(rx, 157, 'Cut 2 Lining Fabric', fontName='Helvetica', fontSize=5.5, fillColor=colors.HexColor('#666666')))

            # Piece 4: Pocket Bag
            p4 = Path(fillColor=c_fill_main, strokeColor=c_cut, strokeWidth=0.7)
            p4.moveTo(rx + 72, 272)
            p4.lineTo(rx + 128, 272)
            p4.curveTo(rx + 132, 240, rx + 130, 205, rx + 117, 185)
            p4.curveTo(rx + 107, 175, rx + 87, 175, rx + 78, 185)
            p4.lineTo(rx + 72, 225)
            p4.closePath()
            g.add(p4)

            p4_in = Path(fillColor=None, strokeColor=c_seam, strokeWidth=0.4, strokeDashArray=[3, 2])
            p4_in.moveTo(rx + 76, 268)
            p4_in.lineTo(rx + 124, 268)
            p4_in.curveTo(rx + 128, 238, rx + 126, 207, rx + 115, 189)
            p4_in.curveTo(rx + 106, 179, rx + 89, 179, rx + 82, 189)
            p4_in.lineTo(rx + 76, 225)
            p4_in.closePath()
            g.add(p4_in)

            g.add(String(rx + 96, 222, '4', fontName='Helvetica-Bold', fontSize=12, fillColor=colors.black))
            g.add(String(rx + 72, 166, '4. POCKET BAG', fontName='Helvetica-Bold', fontSize=6.5, fillColor=colors.HexColor('#222222')))
            g.add(String(rx + 72, 157, 'Cut 2 Main Fabric', fontName='Helvetica', fontSize=5.5, fillColor=colors.HexColor('#666666')))
        elif spec.front_pockets == "in_seam":
            # In-Seam Pocket Bag
            p_in = Path(fillColor=c_fill_main, strokeColor=c_cut, strokeWidth=0.7)
            p_in.moveTo(rx + 30, 272)
            p_in.lineTo(rx + 90, 272)
            p_in.curveTo(rx + 105, 235, rx + 95, 195, rx + 75, 185)
            p_in.curveTo(rx + 60, 178, rx + 38, 182, rx + 30, 200)
            p_in.closePath()
            g.add(p_in)
            g.add(String(rx + 56, 222, '4', fontName='Helvetica-Bold', fontSize=12, fillColor=colors.black))
            g.add(String(rx + 30, 166, '4. IN-SEAM POCKET BAG', fontName='Helvetica-Bold', fontSize=6.5, fillColor=colors.HexColor('#222222')))
            g.add(String(rx + 30, 157, 'Cut 4 Main Fabric', fontName='Helvetica', fontSize=5.5, fillColor=colors.HexColor('#666666')))

        # ---------------------------------------------------------------------
        # FLY PIECES (5 & 7) - Only if front fly closure!
        # ---------------------------------------------------------------------
        has_fly = spec.closure_type in ("exterior_button", "jeans_tack_button", "concealed_hook_bar")
        if has_fly and not is_elastic_waist:
            # Piece 5: Fly Shield
            p5 = Path(fillColor=c_fill_main, strokeColor=c_cut, strokeWidth=0.7)
            p5.moveTo(rx + 148, 272)
            p5.lineTo(rx + 176, 272)
            p5.lineTo(rx + 176, 195)
            p5.lineTo(rx + 162, 180)
            p5.lineTo(rx + 148, 195)
            p5.closePath()
            g.add(p5)
            g.add(Line(rx + 162, 272, rx + 162, 182, strokeColor=c_seam, strokeWidth=0.4, strokeDashArray=[2, 2]))
            g.add(String(rx + 158, 224, '5', fontName='Helvetica-Bold', fontSize=11, fillColor=colors.black))
            g.add(String(rx + 144, 166, '5. FLY SHIELD', fontName='Helvetica-Bold', fontSize=6, fillColor=colors.HexColor('#222222')))
            g.add(String(rx + 144, 157, 'Cut 2 Main', fontName='Helvetica', fontSize=5.5, fillColor=colors.HexColor('#666666')))

            # Piece 7: Fly Facing
            p7 = Path(fillColor=c_fill_fus, strokeColor=c_cut, strokeWidth=0.7)
            p7.moveTo(rx + 192, 272)
            p7.lineTo(rx + 214, 272)
            p7.lineTo(rx + 214, 202)
            p7.curveTo(rx + 214, 188, rx + 202, 180, rx + 192, 180)
            p7.closePath()
            g.add(p7)
            g.add(String(rx + 200, 224, '7', fontName='Helvetica-Bold', fontSize=11, fillColor=colors.black))
            g.add(String(rx + 188, 166, '7. FLY FACING', fontName='Helvetica-Bold', fontSize=6, fillColor=colors.HexColor('#222222')))
            g.add(String(rx + 188, 157, 'Cut 2 Interfacing', fontName='Helvetica', fontSize=5.5, fillColor=colors.HexColor('#666666')))
        elif (spec.closure_type in ("side_invisible_zip", "pull_on_elastic")) and spec.front_pockets == "none":
            # Clean Pocketless & Side-Zip Blueprint Legend Block
            box_x = rx + 6
            box_y = 138
            box_w = 246
            box_h = 146
            g.add(Rect(box_x, box_y, box_w, box_h, fillColor=colors.HexColor('#F8F7F4'), strokeColor=colors.HexColor('#D5D0C8'), strokeWidth=0.8, rx=4, ry=4))
            g.add(Rect(box_x, box_y + box_h - 18, box_w, 18, fillColor=colors.HexColor('#1A4D54'), strokeColor=None, rx=4, ry=4))
            g.add(Rect(box_x, box_y + box_h - 18, box_w, 4, fillColor=colors.HexColor('#1A4D54'), strokeColor=None))
            g.add(String(box_x + 8, box_y + box_h - 12.5, "TECHNICAL BLUEPRINT SPECIFICATIONS", fontName='Helvetica-Bold', fontSize=6.8, fillColor=colors.white))

            f1_note = "Continuous Elastic Waist" if spec.front_shaping == "elastic_gathered" else ("Seamless Flat Front (Zero Darts)" if spec.front_shaping == "flat_front" else "1 Contoured Waist Dart per Leg")
            b2_note = "Elastic Gathered Back Waist" if spec.back_shaping == "elastic_gathered" else ("4 Contoured Waist Darts" if spec.back_shaping == "4_darts" else "1 Contoured Waist Dart per Side")
            
            if spec.closure_type == "pull_on_elastic":
                closure_spec = ("Waistband Closure:", "Continuous Pull-On Elastic Casing (Zero Zippers)")
                p3_spec = ("Piece 3 (Waistband):", "Cut 1 on Fold (Self-Fabric Elastic Casing)")
            else:
                closure_spec = ("Left Side Seam:", "18.00 cm (7 1/8 in) Concealed Invisible Zipper Opening")
                p3_spec = ("Piece 3 (Waistband):", "Cut 1 Main Fabric + Cut 1 Fusible Interfacing")

            specs_lines = [
                ("Pattern Piece Count:", "3 Essential Garment Pieces (Clean Minimalist Silhouette)"),
                ("Piece 1 (Pants Front):", f"Cut 2 Mirrored Pair  •  {f1_note}"),
                ("Piece 2 (Pants Back):", f"Cut 2 Mirrored Pair  •  {b2_note}"),
                p3_spec,
                closure_spec,
                ("Front Rise Shaping:", "Continuous Flat Front  •  Zero Bulk  •  No Fly Shield"),
                ("Seam Allowances:", f"Standard {spec.seam_allowance_cm:.1f} cm (3/8 in) included on all edges"),
                ("Bottom Weighted Hem:", f"Deep {spec.hem_allowance_cm:.1f} cm ({spec.hem_allowance_cm/2.54:.1f} in) weighted hem built-in"),
            ]
            cur_sy = box_y + box_h - 32
            for s_label, s_val in specs_lines:
                g.add(Circle(box_x + 10, cur_sy + 2, 1.5, fillColor=colors.HexColor('#1A4D54'), strokeColor=None))
                g.add(String(box_x + 16, cur_sy, s_label, fontName='Helvetica-Bold', fontSize=5.6, fillColor=colors.HexColor('#1E1A19')))
                g.add(String(box_x + 90, cur_sy, s_val, fontName='Helvetica', fontSize=5.4, fillColor=colors.HexColor('#444444')))
                cur_sy -= 13.5

        # ---------------------------------------------------------------------
        # BL: BELT LOOPS STRIP (Only if belt_loops_count > 0)
        # ---------------------------------------------------------------------
        if spec.belt_loops_count > 0:
            bw, bl = spec.cut_belt_loop_strip_cm
            g.add(Rect(rx, 134, 258, 20, fillColor=c_fill_main, strokeColor=c_cut, strokeWidth=0.7))
            g.add(Rect(rx + 3, 137, 252, 14, fillColor=None, strokeColor=c_seam, strokeWidth=0.4, strokeDashArray=[3, 2]))
            g.add(Line(rx + 15, 144, rx + 100, 144, strokeColor=c_grain, strokeWidth=0.4))
            g.add(Polygon([rx + 19, 142, rx + 13, 144, rx + 19, 146], fillColor=c_grain, strokeColor=None))
            g.add(Polygon([rx + 96, 142, rx + 102, 144, rx + 96, 146], fillColor=c_grain, strokeColor=None))
            g.add(String(rx + 120, 140, 'BL', fontName='Helvetica-Bold', fontSize=10, fillColor=colors.black))
            g.add(Line(rx + 148, 144, rx + 243, 144, strokeColor=c_grain, strokeWidth=0.4))
            g.add(Polygon([rx + 152, 142, rx + 146, 144, rx + 152, 146], fillColor=c_grain, strokeColor=None))
            g.add(Polygon([rx + 239, 142, rx + 245, 144, rx + 239, 146], fillColor=c_grain, strokeColor=None))
            g.add(String(rx, 122, f'BL. BELT LOOPS STRIP ({bw:.1f} cm x {bl:.0f} cm)  |  Cut 1 Main (Yields {spec.belt_loops_count} Loops)', fontName='Helvetica-Bold', fontSize=6, fillColor=colors.HexColor('#222222')))

        # ---------------------------------------------------------------------
        # ENGINEERING TITLE BLOCK / FOOTER
        # ---------------------------------------------------------------------
        g.add(Line(rx, 110, rx + 258, 110, strokeColor=colors.HexColor('#D5D0C8'), strokeWidth=0.5))
        g.add(String(rx, 98, f'SEWLUXE PATTERNS  •  CAD PATTERN INVENTORY', fontName='Helvetica-Bold', fontSize=6.5, fillColor=colors.HexColor('#111111')))
        sizes_str = "Sizes: XXS-10XL (15 Sizes)" if spec.size_standard == "PATTERNFAST_XXS_10XL" else "Sizes: US 00-22"
        g.add(String(rx, 88, f'Model: {spec.model_name}  ·  {sizes_str}', fontName='Helvetica-Bold', fontSize=6.5, fillColor=colors.HexColor('#222222')))
        g.add(String(rx, 78, f'Seam Allowance: {spec.seam_allowance_cm:.1f} cm Included  ·  Hem: {spec.hem_allowance_cm:.1f} cm', fontName='Helvetica-Bold', fontSize=6.5, fillColor=colors.HexColor('#222222')))
        closure_label = "Concealed Trouser Hook & Bar" if spec.closure_type == "concealed_hook_bar" else ("Side Invisible Zipper" if spec.closure_type == "side_invisible_zip" else ("Pull-On Continuous Elastic" if is_elastic_waist else "Tailored Button Closure"))
        back_label = "Pocketless Back" if spec.back_pockets == "none" else f"{spec.back_pockets.replace('_', ' ').title()}"
        accent_hex = spec.color_hex if hasattr(spec, 'color_hex') and spec.color_hex else '#1A4D54'
        g.add(String(rx, 68, f'{closure_label}  •  {back_label}  •  Zero AI Clutter', fontName='Helvetica-Bold', fontSize=5.5, fillColor=colors.HexColor(accent_hex)))

        # 5 cm CAD Calibration Reference Bar
        cal_x = rx
        cal_y = 44
        g.add(Rect(cal_x, cal_y, 70.87, 8, fillColor=colors.HexColor('#FFFFFF'), strokeColor=colors.HexColor('#222222'), strokeWidth=0.5))
        g.add(Rect(cal_x, cal_y, 35.43, 8, fillColor=colors.HexColor('#222222'), strokeColor=None))
        g.add(String(cal_x + 76, cal_y + 1.5, "5 cm / 2 in CAD Reference Scale", fontName='Helvetica', fontSize=5.5, fillColor=colors.HexColor('#555555')))

        d.add(g)
        return d

    # Backwards compatibility alias
    render_colette_palazzo_blueprint = render_blueprint

    # -------------------------------------------------------------------------
    # 4. PROCEDURAL SEWING STEP DIAGRAM RENDERER (TAILORNOVA PRO v5.0)
    # -------------------------------------------------------------------------
    @staticmethod
    def render_step_panel(step_num: int, spec: TrouserSpec, width: int = 500, height: int = 220) -> Drawing:
        """
        Renders pristine vector sewing step diagram panels matching Tailornova Pro standard:
        - Right side of fabric: White (#FFFFFF)
        - Wrong side of fabric: Neutral Grey (#E6E6E6)
        - Seam stitching: Crisp dashed lines (4, 2)
        - Step Callout Numbers: 1. and 2. in bold
        """
        d = Drawing(width, height)
        c_cut = colors.HexColor('#000000')
        c_wrong = colors.HexColor('#E6E6E6')
        c_stitch = colors.HexColor('#000000')
        c_accent = colors.HexColor('#8B2635')

        # Outer Container (#F5F2EF with subtle border)
        d.add(Rect(0, 0, width, height, rx=12, ry=12, fillColor=colors.HexColor('#F5F2EF'), strokeColor=colors.HexColor('#E2DDD8'), strokeWidth=1.0))

        # Two distinct white inner boxes
        box_w = (width - 36) / 2
        box_h = height - 24
        d.add(Rect(12, 12, box_w, box_h, fillColor=colors.white, strokeColor=colors.black, strokeWidth=1.2))
        d.add(Rect(width / 2 + 6, 12, box_w, box_h, fillColor=colors.white, strokeColor=colors.black, strokeWidth=1.2))

        # Bold Callout numbers in Poppins/Helvetica-Bold
        d.add(String(24, height - 32, "1.", fontName="Helvetica-Bold", fontSize=16, fillColor=colors.black))
        d.add(String(width / 2 + 18, height - 32, "2.", fontName="Helvetica-Bold", fontSize=16, fillColor=colors.black))

        # Dynamically render step graphics based on step_num & spec
        if step_num == 1:
            if spec.front_shaping in ("flat_front", "front_darts"):
                # Panel 1: Flat Front Shaping & Staystitching
                d.add(String(50, height - 28, "Staystitch Waist & Front Darts", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))
                d.add(Polygon([40, 40, 40, 160, 200, 160, 200, 40], fillColor=colors.white, strokeColor=c_cut, strokeWidth=1.0))
                # Front waist dart
                d.add(Polygon([115, 160, 120, 95, 125, 160], fillColor=c_wrong, strokeColor=c_cut, strokeWidth=0.8))
                d.add(Line(120, 160, 120, 95, strokeColor=c_stitch, strokeWidth=1.0, strokeDashArray=[3, 2]))
                # Staystitch line
                d.add(Line(40, 154, 200, 154, strokeColor=c_accent, strokeWidth=0.8, strokeDashArray=[3, 2]))
                d.add(String(50, 22, "Staystitch waist curve at 6 mm; stitch front darts (zero pleats)", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor('#555555')))

                # Panel 2: Razor-Sharp Pressed Center Crease
                d.add(String(width / 2 + 44, height - 28, "Press Center Leg Crease", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))
                d.add(Polygon([290, 40, 290, 160, 450, 160, 450, 40], fillColor=colors.white, strokeColor=c_cut, strokeWidth=1.0))
                d.add(Line(370, 40, 370, 160, strokeColor=c_accent, strokeWidth=1.4, strokeDashArray=[6, 3]))
                d.add(Rect(325, 95, 90, 22, rx=4, ry=4, fillColor=colors.white, strokeColor=c_accent, strokeWidth=0.8))
                d.add(String(332, 102, "STEAM & CLAPPER", fontName="Helvetica-Bold", fontSize=6.5, fillColor=c_accent))
                d.add(String(290, 22, "Press crease from waistline straight down to hem", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor('#555555')))
            else:
                # Panel 1: Double Forward Pleats
                pw1 = 12 + box_w / 2
                d.add(String(50, height - 28, "Fold & Baste Front Pleats", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))
                d.add(Polygon([40, 40, 40, 160, 200, 160, 200, 40], fillColor=colors.white, strokeColor=c_cut, strokeWidth=1.0))
                # Main Pleat
                d.add(Line(90, 160, 90, 80, strokeColor=c_cut, strokeWidth=1.0))
                d.add(Line(105, 160, 105, 80, strokeColor=c_cut, strokeWidth=1.0))
                d.add(Line(105, 140, 80, 140, strokeColor=c_accent, strokeWidth=1.2))
                d.add(Polygon([83, 137, 77, 140, 83, 143], fillColor=c_accent, strokeColor=None))
                # Secondary Pleat
                d.add(Line(140, 160, 140, 90, strokeColor=c_cut, strokeWidth=1.0))
                d.add(Line(152, 160, 152, 90, strokeColor=c_cut, strokeWidth=1.0))
                d.add(Line(152, 140, 132, 140, strokeColor=c_accent, strokeWidth=1.2))
                d.add(Polygon([135, 137, 129, 140, 135, 143], fillColor=c_accent, strokeColor=None))
                # Basting line across waist
                d.add(Line(40, 152, 200, 152, strokeColor=c_stitch, strokeWidth=0.8, strokeDashArray=[3, 2]))
                d.add(String(50, 22, "Machine-baste waist edge at 6 mm (1/4 in)", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor('#555555')))

                # Panel 2: Razor-Sharp Pressed Center Crease
                d.add(String(width / 2 + 44, height - 28, "Press Center Leg Crease", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))
                d.add(Polygon([290, 40, 290, 160, 450, 160, 450, 40], fillColor=colors.white, strokeColor=c_cut, strokeWidth=1.0))
                d.add(Line(370, 40, 370, 160, strokeColor=c_accent, strokeWidth=1.4, strokeDashArray=[6, 3]))
                d.add(Rect(325, 95, 90, 22, rx=4, ry=4, fillColor=colors.white, strokeColor=c_accent, strokeWidth=0.8))
                d.add(String(332, 102, "STEAM & CLAPPER", fontName="Helvetica-Bold", fontSize=6.5, fillColor=c_accent))
                d.add(String(290, 22, "Press crease from main pleat straight to hem", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor('#555555')))

        elif step_num == 4:
            # Step 4: Back Darts & Center Back Rise
            d.add(String(50, height - 28, "Stitch Back Waist Darts", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))
            # Wrong side fabric panel
            d.add(Polygon([40, 40, 40, 160, 200, 160, 200, 40], fillColor=c_wrong, strokeColor=c_cut, strokeWidth=1.0))
            # 2 Darts stitched on wrong side
            d.add(Polygon([75, 160, 80, 75, 85, 160], fillColor=colors.white, strokeColor=c_cut, strokeWidth=0.8))
            d.add(Line(80, 160, 80, 75, strokeColor=c_stitch, strokeWidth=1.0, strokeDashArray=[3, 2]))
            d.add(Polygon([135, 160, 140, 85, 145, 160], fillColor=colors.white, strokeColor=c_cut, strokeWidth=0.8))
            d.add(Line(140, 160, 140, 85, strokeColor=c_stitch, strokeWidth=1.0, strokeDashArray=[3, 2]))
            d.add(String(50, 22, "Stitch darts on wrong side; press toward center back", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor('#555555')))

            # Panel 2: Stitch Center Back Rise
            d.add(String(width / 2 + 44, height - 28, "Stitch Center Back Rise", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))
            d.add(Polygon([310, 40, 310, 160, 430, 160, 445, 90, 430, 40], fillColor=c_wrong, strokeColor=c_cut, strokeWidth=1.0))
            d.add(Line(430, 160, 445, 90, strokeColor=c_stitch, strokeWidth=1.2, strokeDashArray=[4, 2]))
            d.add(Line(445, 90, 430, 40, strokeColor=c_stitch, strokeWidth=1.2, strokeDashArray=[4, 2]))
            d.add(String(310, 22, "Stitch center back rise at 1.0 cm (3/8 in); serge and press open", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor('#555555')))

        elif step_num == 7:
            if spec.closure_type in ("exterior_button", "jeans_tack_button"):
                d.add(String(50, height - 28, "Attach Waistband & Buttonhole", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))
                d.add(Rect(45, 75, 150, 50, rx=4, ry=4, fillColor=colors.white, strokeColor=c_cut, strokeWidth=1.0))
                # Buttonhole & Button
                d.add(Line(70, 100, 95, 100, strokeColor=c_accent, strokeWidth=2.0))
                d.add(Circle(150, 100, 10, fillColor=colors.HexColor('#F8F6F2'), strokeColor=c_cut, strokeWidth=1.2))
                d.add(Circle(150, 100, 2, fillColor=c_cut, strokeColor=None))
                d.add(String(65, 122, "BUTTONHOLE", fontName="Helvetica-Bold", fontSize=6.5, fillColor=c_accent))
                d.add(String(138, 122, "BUTTON", fontName="Helvetica-Bold", fontSize=6.5, fillColor=colors.black))
                d.add(String(45, 22, "Waistband attached over fly zipper with buttonhole & horn button", fontName="Helvetica", fontSize=6.2, fillColor=colors.HexColor('#555555')))

                # Panel 2: Deep Weighted Hem
                d.add(String(width / 2 + 44, height - 28, f"Deep {spec.hem_allowance_cm:.1f} cm Weighted Hem", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))
                d.add(Polygon([290, 40, 290, 160, 450, 160, 450, 40], fillColor=colors.white, strokeColor=c_cut, strokeWidth=1.0))
                # Hem fold line
                d.add(Line(290, 80, 450, 80, strokeColor=c_accent, strokeWidth=1.2))
                d.add(Line(290, 60, 450, 60, strokeColor=c_stitch, strokeWidth=0.8, strokeDashArray=[3, 2]))
                d.add(String(330, 84, f"{spec.hem_allowance_cm:.1f} cm ({spec.hem_allowance_cm/2.54:.1f} in) Hem Fold", fontName="Helvetica-Bold", fontSize=6.5, fillColor=c_accent))
                d.add(String(340, 64, "Blind-stitch along inner edge", fontName="Helvetica", fontSize=6.0, fillColor=colors.HexColor('#444444')))
                d.add(String(290, 22, "Provides waterfall drape and gravity over footwear", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor('#555555')))
            else:
                # Step 7: Concealed Hook & Bar & Deep Hem
                d.add(String(50, height - 28, "Install Concealed Hook & Bar", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))
                d.add(Rect(45, 75, 150, 50, rx=4, ry=4, fillColor=colors.white, strokeColor=c_cut, strokeWidth=1.0))
                # Left Inside Bar
                d.add(Line(80, 85, 80, 115, strokeColor=colors.black, strokeWidth=4.0))
                d.add(String(74, 122, "BAR", fontName="Helvetica-Bold", fontSize=7, fillColor=c_accent))
                # Right Extension Hook
                d.add(Line(150, 85, 150, 115, strokeColor=colors.black, strokeWidth=4.0))
                d.add(Line(150, 100, 160, 100, strokeColor=colors.black, strokeWidth=3.0))
                d.add(String(142, 122, "HOOK", fontName="Helvetica-Bold", fontSize=7, fillColor=c_accent))
                d.add(String(45, 22, "Concealed inside extension tab; ZERO exterior buttons!", fontName="Helvetica-Bold", fontSize=6.5, fillColor=c_accent))

                # Panel 2: Deep 5.0 cm Weighted Hem
                d.add(String(width / 2 + 44, height - 28, "Deep 5.0 cm Weighted Hem", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))
                d.add(Polygon([290, 40, 290, 160, 450, 160, 450, 40], fillColor=colors.white, strokeColor=c_cut, strokeWidth=1.0))
                # Hem fold line
                d.add(Line(290, 80, 450, 80, strokeColor=c_accent, strokeWidth=1.2))
                d.add(Line(290, 60, 450, 60, strokeColor=c_stitch, strokeWidth=0.8, strokeDashArray=[3, 2]))
                d.add(String(340, 84, "5.0 cm (2.0 in) Hem Fold", fontName="Helvetica-Bold", fontSize=6.5, fillColor=c_accent))
                d.add(String(340, 64, "Blind-stitch along inner edge", fontName="Helvetica", fontSize=6.0, fillColor=colors.HexColor('#444444')))
                d.add(String(290, 22, "Provides waterfall drape and gravity over footwear", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor('#555555')))

        elif step_num == 2:
            # Step 2: Slanted Hip Pockets
            d.add(String(50, height - 28, "Attach Pocket Lining & Understitch", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))
            d.add(Polygon([40, 40, 40, 160, 200, 160, 200, 40], fillColor=colors.white, strokeColor=c_cut, strokeWidth=1.0))
            # Slanted pocket opening line
            d.add(Line(150, 160, 200, 110, strokeColor=c_cut, strokeWidth=1.2))
            # Lining fold & understitch line
            d.add(Line(152, 158, 198, 112, strokeColor=c_accent, strokeWidth=1.0, strokeDashArray=[3, 2]))
            d.add(Rect(55, 95, 80, 20, rx=3, ry=3, fillColor=colors.HexColor('#F8F6F2'), strokeColor=c_accent, strokeWidth=0.8))
            d.add(String(62, 101, "UNDERSTITCH 2mm", fontName="Helvetica-Bold", fontSize=6.5, fillColor=c_accent))
            d.add(String(50, 22, "Understitch lining to keep hip flat and smooth", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor('#555555')))

            # Panel 2: Stitch Pocket Bag Lower Curve
            d.add(String(width / 2 + 44, height - 28, "Stitch & Finish Pocket Bag", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))
            d.add(Polygon([290, 40, 290, 160, 450, 160, 450, 40], fillColor=c_wrong, strokeColor=c_cut, strokeWidth=1.0))
            # Curved pocket bag outline
            pb = Path(fillColor=colors.white, strokeColor=c_cut, strokeWidth=1.0)
            pb.moveTo(370, 160)
            pb.lineTo(440, 160)
            pb.lineTo(440, 90)
            pb.curveTo(440, 50, 390, 50, 370, 90)
            pb.closePath()
            d.add(pb)
            # Seam around curved edge
            pb_seam = Path(fillColor=None, strokeColor=c_stitch, strokeWidth=1.0, strokeDashArray=[3, 2])
            pb_seam.moveTo(434, 154)
            pb_seam.lineTo(434, 90)
            pb_seam.curveTo(434, 56, 396, 56, 376, 92)
            d.add(pb_seam)
            d.add(String(290, 22, "Stitch pocket bag curve at 1.0 cm; serge raw edge", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor('#555555')))

        elif step_num == 3:
            # Step 3: Front Zipper Fly & Shield
            d.add(String(50, height - 28, "Stitch Zipper to Left Fly Extension", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))
            d.add(Polygon([40, 40, 40, 160, 150, 160, 150, 40], fillColor=c_wrong, strokeColor=c_cut, strokeWidth=1.0))
            # Center rise fold and zipper teeth
            d.add(Line(125, 160, 125, 65, strokeColor=c_cut, strokeWidth=1.2))
            d.add(Line(132, 155, 132, 75, strokeColor=colors.black, strokeWidth=2.2))
            d.add(Line(135, 155, 135, 75, strokeColor=c_accent, strokeWidth=0.8, strokeDashArray=[2, 2]))
            d.add(Circle(125, 65, 3, fillColor=c_accent, strokeColor=None))
            d.add(String(50, 22, "Align zipper tape 3 mm inside fold; stitch with zipper foot", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor('#555555')))

            # Panel 2: Topstitch Curved J-Stitch
            d.add(String(width / 2 + 44, height - 28, "Topstitch Curved J-Seam", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))
            d.add(Polygon([290, 40, 290, 160, 410, 160, 410, 40], fillColor=colors.white, strokeColor=c_cut, strokeWidth=1.0))
            d.add(Line(375, 160, 375, 65, strokeColor=c_cut, strokeWidth=1.0))
            # J-stitch topstitching curve
            j_curve = Path(fillColor=None, strokeColor=c_accent, strokeWidth=1.3, strokeDashArray=[4, 2])
            j_curve.moveTo(350, 160)
            j_curve.lineTo(350, 85)
            j_curve.curveTo(350, 68, 365, 65, 375, 65)
            d.add(j_curve)
            d.add(Rect(310, 105, 32, 16, rx=2, ry=2, fillColor=colors.HexColor('#F8F6F2'), strokeColor=c_accent, strokeWidth=0.6))
            d.add(String(314, 110, "3.5 cm", fontName="Helvetica-Bold", fontSize=6, fillColor=c_accent))
            d.add(String(290, 22, "Stitch J-curve at 3.5 cm (1 3/8 in); bartack at base", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor('#555555')))

        elif step_num == 5:
            # Step 5: Inseams & Crotch Curve
            d.add(String(50, height - 28, "Join Front & Back Inseams", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))
            d.add(Polygon([60, 40, 60, 160, 180, 160, 180, 40], fillColor=c_wrong, strokeColor=c_cut, strokeWidth=1.0))
            # Inseam line
            d.add(Line(60, 40, 60, 160, strokeColor=c_stitch, strokeWidth=1.2, strokeDashArray=[4, 2]))
            d.add(String(50, 22, "Pin at knee notches; stitch at 1.0 cm (3/8 in); press open", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor('#555555')))

            # Panel 2: Continuous U-Shaped Crotch Curve
            d.add(String(width / 2 + 44, height - 28, "Reinforce Continuous Crotch Curve", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))
            d.add(Polygon([310, 40, 310, 160, 430, 160, 430, 40], fillColor=c_wrong, strokeColor=c_cut, strokeWidth=1.0))
            # Crotch U-curve
            u_curve = Path(fillColor=None, strokeColor=c_accent, strokeWidth=1.4, strokeDashArray=[4, 2])
            u_curve.moveTo(330, 160)
            u_curve.curveTo(330, 70, 410, 70, 410, 160)
            d.add(u_curve)
            d.add(String(345, 80, "DOUBLE STITCH", fontName="Helvetica-Bold", fontSize=6.5, fillColor=c_accent))
            d.add(String(290, 22, "Stitch one leg inside the other; reinforce curve with second row", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor('#555555')))

        elif step_num == 6:
            # Step 6: Outer Side Seams & Belt Loops
            d.add(String(50, height - 28, "Stitch Outer Side Seams", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))
            d.add(Polygon([60, 40, 60, 160, 180, 160, 180, 40], fillColor=c_wrong, strokeColor=c_cut, strokeWidth=1.0))
            # Side seam line
            d.add(Line(180, 40, 180, 160, strokeColor=c_stitch, strokeWidth=1.2, strokeDashArray=[4, 2]))
            d.add(String(50, 22, "Match hip and pocket edges; stitch side seam at 1.0 cm", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor('#555555')))

            # Panel 2: Construct & Position Belt Loops
            d.add(String(width / 2 + 44, height - 28, f"Construct {spec.belt_loops_count} Belt Loops (1.1 cm finished)", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))
            d.add(Rect(310, 110, 120, 18, fillColor=colors.white, strokeColor=c_cut, strokeWidth=0.8))
            d.add(Line(310, 119, 430, 119, strokeColor=c_stitch, strokeWidth=0.8, strokeDashArray=[3, 2]))
            d.add(Line(310, 113, 430, 113, strokeColor=c_stitch, strokeWidth=0.8, strokeDashArray=[3, 2]))
            d.add(String(340, 122, "1.1 cm Finished Loop", fontName="Helvetica-Bold", fontSize=6.5, fillColor=colors.black))
            # Vertical loops basted to waist edge
            d.add(Line(300, 70, 440, 70, strokeColor=c_cut, strokeWidth=1.0))
            for lx in [315, 345, 370, 395, 425]:
                d.add(Rect(lx, 60, 10, 22, fillColor=colors.HexColor('#F5F2EF'), strokeColor=c_cut, strokeWidth=0.7))
            d.add(String(290, 22, f"Position {spec.belt_loops_count} loops at waistband notches; baste upside down", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor('#555555')))

        else:
            d.add(String(50, height - 28, f"Step {step_num} Preparation", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))
            d.add(String(width / 2 + 44, height - 28, f"Step {step_num} Assembly", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#222222')))

        return d


if __name__ == '__main__':
    for s in ["palazzo", "cigarette", "barrel_leg", "jogger_pullon"]:
        spec = TrouserSpec(silhouette=s)
        d = UniversalCADBlueprintEngine.render_blueprint(spec)
        print(f"Generated blueprint for {s} successfully!")
    
    # Test step diagram generator
    p1 = UniversalCADBlueprintEngine.render_step_panel(1, spec)
    p4 = UniversalCADBlueprintEngine.render_step_panel(4, spec)
    p7 = UniversalCADBlueprintEngine.render_step_panel(7, spec)
    print("All step diagram panels compiled successfully!")
