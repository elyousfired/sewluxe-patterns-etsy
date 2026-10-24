import os
import re
import json
import fitz

out_dir = r"C:\Users\red1e\.gemini\antigravity\scratch\colette_wide_leg_trousers"
sizes_order = ["00", "0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22"]

all_size_data = []

for sz in sizes_order:
    pdf_path = os.path.join(out_dir, "A4", f"SIZE {sz}.pdf")
    doc = fitz.open(pdf_path)
    p1_txt = doc[0].get_text()
    p23_txt = doc[1].get_text() + "\n" + doc[2].get_text()
    doc.close()

    # Body measurements on Page 1: Size: Height: 167.75, Bust: 80, Waist: 63.5, Hips: 87.75
    m_body = re.search(r"Height:\s*([\d.]+),\s*Bust:\s*([\d.]+),\s*Waist:\s*([\d.]+),\s*Hips:\s*([\d.]+)", p1_txt)
    body = {
        "height_cm": float(m_body.group(1)),
        "bust_cm": float(m_body.group(2)),
        "waist_cm": float(m_body.group(3)),
        "hips_cm": float(m_body.group(4)),
    }

    # Specs on Pages 2-3: e.g. 14. Waist 33.66 cm (13 1/4 in)
    specs = {}
    for line in p23_txt.splitlines():
        m_sp = re.match(r"^\s*(\d+)\.\s+(.+?)\s+([\d.]+)\s+(cm|none|pc)(?:\s+\(([^)]+)\))?", line.strip())
        if m_sp:
            specs[m_sp.group(2).strip()] = {
                "val": float(m_sp.group(3)),
                "unit": m_sp.group(4),
                "in_str": m_sp.group(5) or ""
            }
    all_size_data.append({
        "size": sz,
        "body": body,
        "specs": specs
    })

with open(os.path.join(out_dir, "booklet_size_data.json"), "w", encoding="utf-8") as f:
    json.dump(all_size_data, f, indent=2)

print("Extracted size data for all 13 sizes! Sample Size 0 and Size 12:")
for item in [all_size_data[1], all_size_data[7], all_size_data[-1]]:
    sz = item["size"]
    b = item["body"]
    sp = item["specs"]
    w_fin = round(sp["Waist"]["val"] * 2, 1)
    h_fin = round(sp["Hips"]["val"] * 2, 1)
    inseam = round(sp["Inseam length"]["val"], 1)
    sideseam = round(sp["Pants side seam length"]["val"], 1)
    hem_open = round(sp["Bottom opening"]["val"] * 2, 1)
    print(f"  US {sz}: Body W={b['waist_cm']} H={b['hips_cm']} | Fin W={w_fin} cm, Fin H={h_fin} cm, Inseam={inseam} cm, Side={sideseam} cm, Leg Opening={hem_open} cm")

# Also render Page 4 of SIZE 12.pdf (the Pattern Pieces Layout overview) cropped cleanly without header
d12 = fitz.open(os.path.join(out_dir, "A4", "SIZE 12.pdf"))
p4 = d12[3]
# Crop out the top text header (top 145 pt) and render the vector pieces overview at 300 DPI
clip_rect = fitz.Rect(140, 150, 455, 815)
pix = p4.get_pixmap(dpi=300, clip=clip_rect)
pix.save(os.path.join(out_dir, "pieces_overview_raw.png"))
d12.close()
print("Saved pieces_overview_raw.png:", pix.width, "x", pix.height)
