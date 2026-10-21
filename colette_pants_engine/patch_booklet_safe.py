"""
Safe Patcher for generate_colette_16page_booklet.py
"""

import re

TARGET_SCRIPT = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\colette_pants_engine\generate_colette_16page_booklet.py"

with open(TARGET_SCRIPT, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update Photos to verified palazzo photos
text = text.replace(
    'PHOTO_FRONT = os.path.join(BRAIN_DIR, "colette_photo_01_front.jpg")',
    'PHOTO_FRONT = os.path.join(BRAIN_DIR, "colette_palazzo_photo_01_clean_1792601697194.jpg")'
)
text = text.replace(
    'PHOTO_SIDE = os.path.join(BRAIN_DIR, "colette_photo_02_side.jpg")',
    'PHOTO_SIDE = os.path.join(BRAIN_DIR, "colette_palazzo_photo_02_1792601621750.jpg")'
)
text = text.replace(
    'PHOTO_BACK = os.path.join(BRAIN_DIR, "colette_photo_03_back.jpg")',
    'PHOTO_BACK = os.path.join(BRAIN_DIR, "colette_palazzo_photo_03_1792601698005.jpg")'
)

# 2. Prevent step header collision
old_header = """    c.setFont("Lora", 18)
    c.setFillColor(CHARCOAL)
    c.drawString(M_L + 32, y, title)
    
    c.setFont("Poppins", 7.4)
    c.setFillColor(MUTED)
    c.drawRightString(M_R, y + 2, subtitle)"""

new_header = """    c.setFont("Lora", 15)
    c.setFillColor(CHARCOAL)
    c.drawString(M_L + 32, y + 2, title)
    
    c.setFont("Poppins", 7.2)
    c.setFillColor(MUTED)
    title_w = pdfmetrics.stringWidth(title, "Lora", 15)
    sub_w = pdfmetrics.stringWidth(subtitle, "Poppins", 7.2)
    if (M_L + 32 + title_w + 15) > (M_R - sub_w):
        y -= 12
        c.drawString(M_L + 32, y + 2, subtitle)
    else:
        c.drawRightString(M_R, y + 4, subtitle)"""

text = text.replace(old_header, new_header)

# 3. Fix Page 2 hem circumference
text = re.sub(
    r'sweeping wide-leg silhouette \([^\)]*hem circumference\),',
    'sweeping wide-leg silhouette (60.3 to 92.6 cm hem circumference across sizes),',
    text
)

# 4. Fix Page 4 finished garment table (Eliminate 0/0", fix conversions, fix palazzo inseam)
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

text = re.sub(r'fin_rows = \[\s*\("US 00".*?\n    \]', new_fin_rows, text, flags=re.DOTALL)

# 5. Fix Belt loops in Page 6 inventory
text = text.replace(
    '("BL", "Belt Loops (5x)", "Main Fabric + Interfacing", "Cut 1 strip (8 cm x 45 cm)")',
    '("BL", "Belt Loops (5x)", "Main Fabric + Interfacing", "Cut 1 strip (3.5 cm x 45 cm)")'
)

# 6. Fix QR Code vector scaling on Page 8
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

text = text.replace(old_qr, new_qr)

# 7. Update step panels to unique clean assets
text = text.replace(
    '"step5_panels.png",\n         [\n             "<b>Back Waist Darts:',
    '"step4_darts_panel.png",\n         [\n             "<b>Back Waist Darts:'
)

text = text.replace(
    '"step5_panels.png",\n         [\n             "<b>Pants Inseams:',
    '"step5_inseams_panel.png",\n         [\n             "<b>Pants Inseams:'
)

text = text.replace(
    '"step7_panels.png",',
    '"step7_hook_and_hem_panel.png",'
)

# 8. Fix Belt loops instruction text in Step 6
text = text.replace(
    '"<b>Construct 5 Belt Loops:</b> Fold belt loop strip lengthwise right sides together, stitch 6 mm from fold, turn right side out, press, and cut into 5 equal 8.5 cm loops."',
    '"<b>Construct 5 Belt Loops:</b> Fold 3.5 cm wide belt loop strip lengthwise right sides together, stitch 6 mm from fold, turn right side out, press to 1.1 cm finished width, and cut into 5 equal 8.5 cm loops."'
)

# 9. Fix Hem instruction text in Step 7
text = text.replace(
    '"<b>Turn Up 5.0 cm Hem:</b> Press leg lower edge 1 cm to wrong side, then fold up 4 cm to form deep <b>5.0 cm (2.0 in) weighted palazzo hem</b>. Blind-stitch invisibly by hand or machine."',
    '"<b>Turn Up 5.0 cm Hem:</b> Press leg lower edge 1.0 cm (3/8 in) to wrong side, then fold up 4.0 cm (1 5/8 in) to form deep <b>5.0 cm (2.0 in) weighted palazzo hem</b>. Blind-stitch invisibly by hand or machine."'
)

# 10. Fix subtitle in Step 7
text = text.replace(
    '(7, "Attach tailored waistband & hem the trousers", "Piece 3, Hook & Bar, Hem",',
    '(7, "Attach tailored waistband & hem the trousers", "Piece 3 | Hook & Bar | 5.0 cm Hem",'
)

with open(TARGET_SCRIPT, "w", encoding="utf-8") as f:
    f.write(text)

print("[SUCCESS] Applied safe patches to generate_colette_16page_booklet.py!")
