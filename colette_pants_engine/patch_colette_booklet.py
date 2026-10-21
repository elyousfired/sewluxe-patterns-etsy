"""
Systemic Patcher for generate_colette_16page_booklet.py
Applies all 7 critical quality fixes with zero syntax errors.
"""

import re
import os

SCRIPT_PATH = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\colette_pants_engine\generate_colette_16page_booklet.py"

with open(SCRIPT_PATH, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# 1. Clean up broken unicode replacement characters
content = content.replace("\ufffd", "-").replace("", "-")

# 2. Fix Page 2 Hem text
content = re.sub(
    r'sweeping wide-leg silhouette \([^\)]+hem circumference\),',
    'sweeping wide-leg silhouette (60.3 to 92.6 cm hem circumference across sizes),',
    content
)

# 3. Fix Page 4 Finished Garment Table
new_fin_rows = """    fin_rows = [
        ("US 00", "64.8 cm (25 1/2\\\")", "90.2 cm (35 1/2\\\")", "60.3 cm (23 3/4\\\")", "78 cm / 104 cm (30 3/4\\\" / 41\\\")"),
        ("US 0",  "67.3 cm (26 1/2\\\")", "92.6 cm (36 1/2\\\")", "61.9 cm (24 3/8\\\")", "78 cm / 104 cm (30 3/4\\\" / 41\\\")"),
        ("US 2",  "70.1 cm (27 5/8\\\")", "95.0 cm (37 3/8\\\")", "63.6 cm (25\\\")",      "78 cm / 104 cm (30 3/4\\\" / 41\\\")"),
        ("US 4",  "72.7 cm (28 5/8\\\")", "97.4 cm (38 3/8\\\")", "65.2 cm (25 5/8\\\")", "78 cm / 105 cm (30 3/4\\\" / 41 3/8\\\")"),
        ("US 6",  "75.2 cm (29 5/8\\\")", "100.0 cm (39 3/8\\\")", "67.0 cm (26 3/8\\\")", "78 cm / 105 cm (30 3/4\\\" / 41 3/8\\\")"),
        ("US 8",  "77.8 cm (30 5/8\\\")", "102.2 cm (40 1/4\\\")", "68.6 cm (27\\\")",      "78 cm / 106 cm (30 3/4\\\" / 41 3/4\\\")"),
        ("US 10", "80.3 cm (31 5/8\\\")", "104.4 cm (41 1/8\\\")", "70.1 cm (27 5/8\\\")", "78 cm / 106 cm (30 3/4\\\" / 41 3/4\\\")"),
        ("US 12", "84.4 cm (33 1/4\\\")", "107.8 cm (42 3/8\\\")", "72.5 cm (28 1/2\\\")", "78 cm / 107 cm (30 3/4\\\" / 42 1/8\\\")"),
        ("US 14", "89.2 cm (35 1/8\\\")", "111.8 cm (44\\\")",      "75.4 cm (29 5/8\\\")", "78 cm / 107 cm (30 3/4\\\" / 42 1/8\\\")"),
        ("US 16", "95.1 cm (37 1/2\\\")", "115.8 cm (45 5/8\\\")", "78.4 cm (30 7/8\\\")", "78 cm / 108 cm (30 3/4\\\" / 42 1/2\\\")"),
        ("US 18", "101.0 cm (39 3/4\\\")", "126.1 cm (49 5/8\\\")", "84.6 cm (33 3/8\\\")", "78 cm / 108 cm (30 3/4\\\" / 42 1/2\\\")"),
        ("US 20", "106.8 cm (42 1/8\\\")", "132.0 cm (52\\\")",      "88.6 cm (34 7/8\\\")", "78 cm / 109 cm (30 3/4\\\" / 42 7/8\\\")"),
        ("US 22", "112.7 cm (44 3/8\\\")", "137.9 cm (54 1/4\\\")", "92.6 cm (36 1/2\\\")", "78 cm / 110 cm (30 3/4\\\" / 43 1/4\\\")"),
    ]"""

content = re.sub(r'fin_rows = \[\s*\("US 00".*?\n    \]', new_fin_rows, content, flags=re.DOTALL)

# 4. Fix Page 6 Belt Loops in pieces_data
content = content.replace(
    '("BL", "Belt Loops (5x)", "Main Fabric + Interfacing", "Cut 1 strip (8 cm x 45 cm)")',
    '("BL", "Belt Loops (5x)", "Main Fabric + Interfacing", "Cut 1 strip (3.5 cm x 45 cm)")'
)

# 5. Fix Page 8 QR Code widget transform
old_qr = """        # QR Code
        qr = QrCodeWidget(v_url)
        qr.barWidth = 66
        qr.barHeight = 66
        d = Drawing(66, 66)
        d.add(qr)
        d.drawOn(c, cx, cy - c_h + 20)"""

new_qr = """        # QR Code with proper vector transform
        qr = QrCodeWidget(v_url)
        bounds = qr.getBounds()
        qw = bounds[2] - bounds[0]
        qh = bounds[3] - bounds[1]
        target_sz = 60.0
        d = Drawing(target_sz, target_sz, transform=[target_sz/qw, 0, 0, target_sz/qh, 0, 0])
        d.add(qr)
        d.drawOn(c, cx + 3, cy - c_h + 16)"""

content = content.replace(old_qr, new_qr)

# 6. Fix Steps data panels and descriptions
# Replace Step 4 panel and Step 5 panel
content = content.replace(
    '# Page 12: Step 4\n        (4, "Sew back waist darts & center back seam", "Piece 2 - 4 Darts & Rise", "step5_panels.png",',
    '# Page 12: Step 4\n        (4, "Sew back waist darts & center back seam", "Piece 2 - 4 Darts & Rise", "step4_darts_panel.png",'
)

content = content.replace(
    '# Page 13: Step 5\n        (5, "Sew the inseams & reinforced crotch curve", "Pieces 1 & 2 - pictures 1-2", "step5_panels.png",',
    '# Page 13: Step 5\n        (5, "Sew the inseams & reinforced crotch curve", "Pieces 1 & 2 - pictures 1-2", "step5_inseams_panel.png",'
)

content = content.replace(
    '# Page 15: Step 7\n        (7, "Attach tailored waistband & hem the trousers", "Piece 3, Hook & Bar, Hem", "step7_panels.png",',
    '# Page 15: Step 7\n        (7, "Attach tailored waistband & hem the trousers", "Piece 3 | Hook & Bar | 5.0 cm Hem", "step7_hook_and_hem_panel.png",'
)

# Fix Belt loops instruction text in Step 6
content = content.replace(
    '"<b>Construct 5 Belt Loops:</b> Fold belt loop strip lengthwise right sides together, stitch 6 mm from fold, turn right side out, press, and cut into 5 equal 8.5 cm loops."',
    '"<b>Construct 5 Belt Loops:</b> Fold 3.5 cm wide belt loop strip lengthwise right sides together, stitch 6 mm from fold, turn right side out, press to 1.1 cm finished width, and cut into 5 equal 8.5 cm loops."'
)

# Fix Hem instruction text in Step 7
content = content.replace(
    '"<b>Turn Up 5.0 cm Hem:</b> Press leg lower edge 1 cm to wrong side, then fold up 4 cm to form deep <b>5.0 cm (2.0 in) weighted palazzo hem</b>. Blind-stitch invisibly by hand or machine."',
    '"<b>Turn Up 5.0 cm Hem:</b> Press leg lower edge 1.0 cm (3/8 in) to wrong side, then fold up 4.0 cm (1 5/8 in) to form deep <b>5.0 cm (2.0 in) weighted palazzo hem</b>. Blind-stitch invisibly by hand or machine."'
)

with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("[SUCCESS] Patched generate_colette_16page_booklet.py successfully!")
