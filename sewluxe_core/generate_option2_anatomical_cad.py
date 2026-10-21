#!/usr/bin/env python3
"""
generate_option2_anatomical_cad.py
Generates Option 2: Pure Procedural Anatomical Apparel CAD for Step 4:
- Anatomical trouser back silhouette with real Bezier curves (waist pitch, hip contour, curved crotch rise).
- Panel 1: Stitching and pressing 4 contoured back waist darts on the wrong side.
- Panel 2: Stitching the center back rise seam (two panels right sides together with pins and serged edge).
- Gold Standard #F5F2EF container with crisp #000000 borders and bold Poppins-Bold '1.' and '2.'.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import pymupdf as fitz

FONTS_DIR = r"C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\fonts"
FONT_BOLD = os.path.join(FONTS_DIR, "Poppins-Bold.ttf")
FONT_MED = os.path.join(FONTS_DIR, "Poppins-Medium.ttf")
FONT_REG = os.path.join(FONTS_DIR, "Poppins-Regular.ttf")

OUT_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0"

def build_option2_svg():
    # 2000 x 950 px high-res SVG canvas
    W, H = 2000, 950
    box_w = 930
    box_h = 830
    pad_x = 45
    pad_y = 60

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <!-- Arrowhead markers -->
    <marker id="arr-burgundy" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M1,1 L8,4.5 L1,8 Z" fill="#8C3B47" />
    </marker>
    <marker id="arr-black" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M1,1 L8,4.5 L1,8 Z" fill="#222222" />
    </marker>
    <!-- Serge/Overlock stitch pattern -->
    <pattern id="serge-stitch" width="12" height="6" patternUnits="userSpaceOnUse">
      <path d="M0,0 L6,6 L12,0" fill="none" stroke="#666666" stroke-width="1.0" />
    </pattern>
  </defs>

  <!-- Outer Luxury Container #F5F2EF -->
  <rect x="15" y="15" width="{W - 30}" height="{H - 30}" rx="32" ry="32" fill="#F5F2EF" stroke="#E2DDD8" stroke-width="4" />

  <!-- ========================================================================= -->
  <!-- PANEL 1: STITCH BACK WAIST DARTS -->
  <!-- ========================================================================= -->
  <g id="panel_1" transform="translate({pad_x}, {pad_y})">
    <!-- Inner White Box -->
    <rect x="0" y="0" width="{box_w}" height="{box_h}" fill="#FFFFFF" stroke="#000000" stroke-width="4" />
    
    <!-- Bold Callout Number -->
    <text x="45" y="75" font-family="Poppins, Arial" font-size="52" font-weight="bold" fill="#000000">1.</text>
    <text x="110" y="72" font-family="Poppins, Arial" font-size="28" font-weight="bold" fill="#1E1A19">Stitch Back Waist Darts</text>
    <text x="110" y="104" font-family="Poppins, Arial" font-size="19" fill="#6E655F">Wrong Side of Fabric (Inside)  ·  4 Contoured Darts</text>

    <!-- Anatomical Pants Back Upper Panel (Wrong Side - #E8E5E0) -->
    <!-- Waistline: (200, 220) to (760, 185) - inclined 35px toward Center Back -->
    <!-- Hip curve: (200, 220) curveTo (165, 380) (175, 520) (220, 680) -->
    <!-- Inseam/Crotch: (760, 185) down to (740, 420) curveTo (780, 560) (840, 610) to (730, 680) -->
    <path d="M 195,220 
             Q 480,205 750,175 
             L 745,430 
             Q 750,560 830,600 
             L 760,670 
             L 260,670 
             Q 180,480 195,220 Z" 
          fill="#E8E5E0" stroke="#000000" stroke-width="3.5" stroke-linejoin="round" />

    <!-- Center Back (CB) label line -->
    <line x1="750" y1="175" x2="745" y2="430" stroke="#8C3B47" stroke-width="1.8" stroke-dasharray="6,4" />
    <text x="758" y="270" font-family="Poppins, Arial" font-size="15" font-weight="bold" fill="#8C3B47">CENTER BACK</text>

    <!-- Side Seam (SS) label line -->
    <text x="100" y="380" font-family="Poppins, Arial" font-size="15" font-weight="bold" fill="#6E655F">SIDE SEAM</text>
    <path d="M 175,375 L 188,375" stroke="#6E655F" stroke-width="1.5" marker-end="url(#arr-black)" />

    <!-- DART 1: Outer Waist Dart (Wider, slightly shorter) -->
    <!-- Dart intake at waist: 340 to 380 (width 40), depth down to 360, 470 -->
    <polygon points="340,212 380,209 360,470" fill="#FFFFFF" stroke="#000000" stroke-width="2.5" />
    <line x1="360" y1="210" x2="360" y2="470" stroke="#000000" stroke-width="3.2" stroke-dasharray="10,6" />
    <!-- Dart Apex Circle -->
    <circle cx="360" cy="470" r="4.5" fill="#8C3B47" />
    <!-- Thread tails extending -->
    <path d="M 360,470 Q 365,510 380,530" fill="none" stroke="#555555" stroke-width="1.6" />
    <path d="M 360,470 Q 355,515 350,535" fill="none" stroke="#555555" stroke-width="1.6" />

    <!-- DART 2: Inner Waist Dart (Near Center Back, longer) -->
    <!-- Dart intake at waist: 520 to 560 (width 40), depth down to 540, 510 -->
    <polygon points="520,198 560,195 540,510" fill="#FFFFFF" stroke="#000000" stroke-width="2.5" />
    <line x1="540" y1="196" x2="540" y2="510" stroke="#000000" stroke-width="3.2" stroke-dasharray="10,6" />
    <!-- Dart Apex Circle -->
    <circle cx="540" cy="510" r="4.5" fill="#8C3B47" />
    <!-- Thread tails extending -->
    <path d="M 540,510 Q 545,550 560,575" fill="none" stroke="#555555" stroke-width="1.6" />
    <path d="M 540,510 Q 532,555 530,580" fill="none" stroke="#555555" stroke-width="1.6" />

    <!-- Directional Pressing Arrows (Press toward Center Back) -->
    <path d="M 390,320 Q 420,310 450,320" fill="none" stroke="#8C3B47" stroke-width="3.0" marker-end="url(#arr-burgundy)" />
    <path d="M 570,300 Q 600,290 630,300" fill="none" stroke="#8C3B47" stroke-width="3.0" marker-end="url(#arr-burgundy)" />
    <text x="440" y="290" font-family="Poppins, Arial" font-size="16" font-weight="bold" fill="#8C3B47">PRESS TOWARD CENTER BACK</text>

    <!-- Bottom Instruction Banner -->
    <rect x="40" y="730" width="{box_w - 80}" height="70" rx="10" ry="10" fill="#F8F6F2" stroke="#E2DDD8" stroke-width="1.5" />
    <text x="{box_w // 2}" y="760" font-family="Poppins, Arial" font-size="17" font-weight="bold" fill="#1E1A19" text-anchor="middle">
      Fold darts right sides together matching waist notches.
    </text>
    <text x="{box_w // 2}" y="785" font-family="Poppins, Arial" font-size="15" fill="#6E655F" text-anchor="middle">
      Stitch from waist edge tapering to apex point. Tie thread tails by hand (do NOT backstitch).
    </text>
  </g>

  <!-- ========================================================================= -->
  <!-- PANEL 2: STITCH CENTER BACK RISE SEAM -->
  <!-- ========================================================================= -->
  <g id="panel_2" transform="translate({W // 2 + pad_x // 2}, {pad_y})">
    <!-- Inner White Box -->
    <rect x="0" y="0" width="{box_w}" height="{box_h}" fill="#FFFFFF" stroke="#000000" stroke-width="4" />
    
    <!-- Bold Callout Number -->
    <text x="45" y="75" font-family="Poppins, Arial" font-size="52" font-weight="bold" fill="#000000">2.</text>
    <text x="110" y="72" font-family="Poppins, Arial" font-size="28" font-weight="bold" fill="#1E1A19">Stitch Center Back Rise</text>
    <text x="110" y="104" font-family="Poppins, Arial" font-size="19" fill="#6E655F">Right Sides Together (Face to Face)  ·  1.0 cm (3/8 in) Seam</text>

    <!-- Two Pants Backs placed Right Sides Together (Offset slightly to show 2 layers) -->
    <!-- Under layer (Layer 2 - slightly darker offset #DDD9D2) -->
    <path d="M 235,185 
             Q 370,195 530,225 
             Q 550,470 500,675 
             L 285,675 
             Q 215,570 170,520 
             L 175,380 
             Z" 
          fill="#DDD9D2" stroke="#888888" stroke-width="2" />

    <!-- Top layer (Layer 1 - #FFFFFF / #FAF8F5) -->
    <path d="M 225,175 
             Q 360,185 520,215 
             Q 540,460 490,665 
             L 275,665 
             Q 205,560 160,510 
             L 165,370 
             Z" 
          fill="#FFFFFF" stroke="#000000" stroke-width="3.5" stroke-linejoin="round" />

    <!-- Center Back Curved Seam Line (Stitching at 1.0 cm) -->
    <!-- Starts at waist (225, 175) along left edge to crotch hook (160, 510) -->
    <path d="M 245,177 
             L 185,375 
             Q 180,480 230,510" 
          fill="none" stroke="#000000" stroke-width="4.0" stroke-dasharray="14,8" />

    <!-- 1.0 cm (3/8 in) Seam Callout Dimension -->
    <line x1="225" y1="165" x2="245" y2="167" stroke="#8C3B47" stroke-width="2" />
    <line x1="225" y1="160" x2="225" y2="170" stroke="#8C3B47" stroke-width="1.5" />
    <line x1="245" y1="162" x2="245" y2="172" stroke="#8C3B47" stroke-width="1.5" />
    <text x="235" y="152" font-family="Poppins, Arial" font-size="15" font-weight="bold" fill="#8C3B47" text-anchor="middle">1.0 cm (3/8")</text>

    <!-- Realistic Tailoring Pins along Seam Line -->
    <!-- Pin 1 -->
    <g transform="translate(230, 240) rotate(-15)">
      <line x1="-35" y1="0" x2="35" y2="0" stroke="#777777" stroke-width="2.5" />
      <circle cx="-35" cy="0" r="6.5" fill="#E53935" stroke="#B71C1C" stroke-width="1" />
    </g>
    <!-- Pin 2 -->
    <g transform="translate(205, 330) rotate(-8)">
      <line x1="-35" y1="0" x2="35" y2="0" stroke="#777777" stroke-width="2.5" />
      <circle cx="-35" cy="0" r="6.5" fill="#E53935" stroke="#B71C1C" stroke-width="1" />
    </g>
    <!-- Pin 3 -->
    <g transform="translate(190, 420) rotate(5)">
      <line x1="-35" y1="0" x2="35" y2="0" stroke="#777777" stroke-width="2.5" />
      <circle cx="-35" cy="0" r="6.5" fill="#E53935" stroke="#B71C1C" stroke-width="1" />
    </g>
    <!-- Pin 4 near crotch curve -->
    <g transform="translate(185, 485) rotate(35)">
      <line x1="-35" y1="0" x2="35" y2="0" stroke="#777777" stroke-width="2.5" />
      <circle cx="-35" cy="0" r="6.5" fill="#E53935" stroke="#B71C1C" stroke-width="1" />
    </g>

    <!-- Serge / Overlock Stitch along Raw Edge -->
    <path d="M 220,180 L 163,372 Q 158,510 205,520" fill="none" stroke="#777777" stroke-width="2.0" stroke-dasharray="3,3" />
    <text x="75" y="310" font-family="Poppins, Arial" font-size="15" font-weight="bold" fill="#6E655F">SERGE OR PINK EDGES</text>
    <path d="M 135,315 L 185,340" fill="none" stroke="#6E655F" stroke-width="1.5" marker-end="url(#arr-black)" />

    <!-- Crotch Intersection Point Marker -->
    <circle cx="215" cy="515" r="5" fill="#8C3B47" />
    <text x="235" y="525" font-family="Poppins, Arial" font-size="14" font-weight="bold" fill="#8C3B47">CROTCH INTERSECTION</text>

    <!-- Seam Open Pressing Callout -->
    <text x="360" y="360" font-family="Poppins, Arial" font-size="18" font-weight="bold" fill="#8C3B47">PRESS SEAM OPEN FLAT</text>
    <path d="M 350,365 Q 260,375 220,380" fill="none" stroke="#8C3B47" stroke-width="2.5" marker-end="url(#arr-burgundy)" />

    <!-- Bottom Instruction Banner -->
    <rect x="40" y="730" width="{box_w - 80}" height="70" rx="10" ry="10" fill="#F8F6F2" stroke="#E2DDD8" stroke-width="1.5" />
    <text x="{box_w // 2}" y="760" font-family="Poppins, Arial" font-size="17" font-weight="bold" fill="#1E1A19" text-anchor="middle">
      Place Pants Backs right sides together matching center rise notches.
    </text>
    <text x="{box_w // 2}" y="785" font-family="Poppins, Arial" font-size="15" fill="#6E655F" text-anchor="middle">
      Stitch at 1.0 cm (3/8 in) from waist down to crotch intersection. Serge and press seam open.
    </text>
  </g>
</svg>'''
    return svg

def main():
    svg_code = build_option2_svg()
    svg_path = os.path.join(OUT_DIR, "option2_anatomical_cad.svg")
    png_path = os.path.join(OUT_DIR, "option2_anatomical_cad.png")

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_code)
    print(f"[+] Saved Option 2 SVG: {svg_path}")

    # Render at crisp 300 DPI via PyMuPDF
    doc = fitz.open(stream=svg_code.encode("utf-8"), filetype="svg")
    page = doc[0]
    pix = page.get_pixmap(dpi=300)
    pix.save(png_path)
    print(f"[+] Rendered Option 2 PNG at 300 DPI: {png_path} ({pix.width}x{pix.height})")

if __name__ == "__main__":
    main()
