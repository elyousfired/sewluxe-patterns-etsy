import os
import re
import json
import pymupdf

def extract_specs():
    a4_dir = r"C:\Users\red1e\Desktop\SewLuxe_Elastic_Wide_Leg_Pants\03_Patterns_PDF\A4_Print_at_Home"
    out_json = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\03_booklet_engine\booklet_size_data.json"
    manifest_json = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\03_booklet_engine\design_manifest.json"
    
    files = sorted(os.listdir(a4_dir))
    size_order = ['00', '0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22']
    
    all_sizes = {}
    master_pieces = []
    seam_allowance_val = "1 cm (3/8 in)"
    hem_val = "3 cm (1 1/8 in)"
    
    for sz in size_order:
        fname = f"SewLuxe_Wide_Leg_Pants_Size_US_{sz}_A4.pdf"
        fpath = os.path.join(a4_dir, fname)
        if not os.path.exists(fpath):
            continue
            
        doc = pymupdf.open(fpath)
        p1_text = doc[0].get_text()
        p2_text = doc[1].get_text()
        doc.close()
        
        # Parse Page 1: Size: Height: 167.75, Bust: 82.5, Waist: 66, Hips: 90.25
        body_m = {}
        m_match = re.search(r"Size:\s*Height:\s*([\d\.]+),\s*Bust:\s*([\d\.]+),\s*Waist:\s*([\d\.]+),\s*Hips:\s*([\d\.]+)", p1_text)
        if m_match:
            body_m = {
                "height_cm": float(m_match.group(1)),
                "bust_cm": float(m_match.group(2)),
                "waist_cm": float(m_match.group(3)),
                "hips_cm": float(m_match.group(4)),
                "waist_in": round(float(m_match.group(3)) / 2.54, 1),
                "hips_in": round(float(m_match.group(4)) / 2.54, 1),
            }
            
        # Parse Page 2: Specs
        finished = {}
        for line in p2_text.split("\n"):
            line = line.strip()
            if "Low hips" in line:
                val = float(re.search(r"Low hips\s+([\d\.]+)", line).group(1)) * 2
                finished["hips_cm"] = round(val, 1)
                finished["hips_in"] = round(val / 2.54, 1)
            elif "Bottom opening" in line:
                val = float(re.search(r"Bottom opening\s+([\d\.]+)", line).group(1)) * 2
                finished["leg_opening_cm"] = round(val, 1)
                finished["leg_opening_in"] = round(val / 2.54, 1)
            elif "Inseam length" in line:
                val = float(re.search(r"Inseam length\s+([\d\.]+)", line).group(1))
                finished["inseam_cm"] = round(val, 1)
                finished["inseam_in"] = round(val / 2.54, 1)
            elif "Pants side seam length" in line:
                val = float(re.search(r"Pants side seam length\s+([\d\.]+)", line).group(1))
                finished["side_seam_cm"] = round(val, 1)
                finished["side_seam_in"] = round(val / 2.54, 1)
            elif "Waistband elastic length" in line:
                val = float(re.search(r"Waistband elastic length\s+([\d\.]+)", line).group(1))
                finished["elastic_length_cm"] = round(val, 1)
                finished["elastic_length_in"] = round(val / 2.54, 1)
                
        # Parse pieces from p2_text once
        if not master_pieces and "Pattern pieces:" in p2_text:
            p_section = p2_text[p2_text.find("Pattern pieces:"):p2_text.find("Pattern Specs")]
            for pline in p_section.split("\n"):
                pline = pline.strip()
                pmatch = re.search(r'(\d+)\.\s*"([^"]+)",\s*([^:]+):\s*(.*)', pline)
                if pmatch:
                    master_pieces.append({
                        "index": int(pmatch.group(1)),
                        "name": pmatch.group(2).title(),
                        "material": pmatch.group(3).strip().title(),
                        "cut": pmatch.group(4).strip()
                    })

        all_sizes[sz] = {
            "size": sz,
            "body": body_m,
            "finished": finished
        }

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(all_sizes, f, indent=2)
    print(f"Extracted specs for {len(all_sizes)} sizes saved to {out_json}")

    # Generate design_manifest.json
    manifest = {
        "garment_name": "Margot",
        "garment_type": "Wide-Leg Pants",
        "full_title": "Margot Elastic Wide-Leg Pants",
        "subtitle": "High-rise relaxed wide-leg pull-on trousers with elasticated casing waistband and concealed in-seam pockets.",
        "category_code": "wm_pants",
        "division": "womenswear",
        "silhouette": "High-rise relaxed wide straight leg with fluid drape",
        "closure": "Pull-on continuous elasticated waistband casing (No zipper, no fly)",
        "pockets": {
            "front": "Concealed in-seam side pockets anchored cleanly into side seams",
            "back": "Clean unadorned back with continuous drape"
        },
        "hem": "Deep 3 cm (1 1/8 in) clean topstitched hem",
        "seam_allowance": seam_allowance_val,
        "suggested_fabrics": "Lightweight to medium-weight woven fabrics with fluid drape: washed linen, linen blends, cotton twill, tencel modal, chambray, or viscose rayon.",
        "lining_fabric": "Self-fabric or lightweight cotton batiste for pocket bags.",
        "palette_theme": "Olive Linen & Cream",
        "colors": {
            "primary": "#2D3728",
            "secondary": "#58694B",
            "page_bg": "#FAF8F5",
            "table_head": "#2D3728",
            "table_alt": "#F2F4F0",
            "rule_line": "#E2DDD5",
            "text_body": "#1A1918",
            "muted": "#6E6862"
        },
        "features": [
            "High-rise wide-leg silhouette with relaxed fluid fall",
            "Continuous pull-on elasticated waistband casing",
            "Concealed in-seam pockets nested cleanly into side seams",
            "Zero zippers, zero buttons, and zero darts for accessible sewing",
            "Deep 3 cm (1 1/8 in) hem for weighted drape and stability"
        ],
        "pieces": master_pieces
    }

    with open(manifest_json, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Design manifest created: {manifest_json}")

if __name__ == "__main__":
    extract_specs()
