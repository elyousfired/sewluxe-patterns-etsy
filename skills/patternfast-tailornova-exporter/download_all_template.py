import os
import re
import json
import zipfile
import subprocess
import urllib.parse
import fitz

out_dir = r"C:\Users\red1e\.gemini\antigravity\scratch\colette_wide_leg_trousers"
login_file = r"C:\Users\red1e\.gemini\antigravity\brain\c675070e-91f4-406b-8086-d794cba1db24\scratch\login_active.json"

os.makedirs(os.path.join(out_dir, "A4"), exist_ok=True)
os.makedirs(os.path.join(out_dir, "US Letter"), exist_ok=True)
os.makedirs(os.path.join(out_dir, "A0"), exist_ok=True)
os.makedirs(os.path.join(out_dir, "raw_pdfs"), exist_ok=True)
os.makedirs(os.path.join(out_dir, "source_instructions", "svgs"), exist_ok=True)

def get_token():
    res = subprocess.run([
        "curl.exe", "-s", "-X", "POST", "https://patternfast.com/api/user/login",
        "-H", "Content-Type: application/json",
        "--data-binary", f"@{login_file}"
    ], capture_output=True, text=True, encoding="utf-8")
    return json.loads(res.stdout)["token"]

def whitelabel_pattern_pdf(in_pdf_path, out_pdf_path, size_label):
    doc = fitz.open(in_pdf_path)
    hex_size = size_label.encode("ascii").hex()
    replacement_tj = f"[<{hex_size}> 0] TJ".encode("latin1")

    for pno in [0, 1, 3]:
        if pno >= len(doc):
            continue
        page = doc[pno]
        xrefs = page.get_contents()
        if not xrefs:
            continue
        raw = doc.xref_stream(xrefs[0])
        raw_new = re.sub(
            rb"q\n1 0 0 1 0 28\.3465 cm\n0\.75 0 0 0\.75 0 0 cm\nq\n0 0 m\n793\.706667 0 l\n793\.706667 48 l\n0 48 l\nh\nW n\n2 0 0 2 275\.853333 0 cm\nq.*?Q\nQ\nQ\n",
            rb"",
            raw,
            count=1,
            flags=re.S
        )
        if pno in (0, 1):
            raw_new = re.sub(
                rb"\[<50>[^\]]*<202d>\s*0\]\s*TJ",
                replacement_tj,
                raw_new
            )
        doc.update_stream(xrefs[0], raw_new)

        page.insert_text(
            fitz.Point(214.83, 841.89 - 791.54),
            "SewLuxePatterns",
            fontname="hebo",
            fontsize=20,
            color=(0.1215686, 0.1215686, 0.1215686)
        )
        page.insert_text(
            fitz.Point(262.285, 841.89 - 779.54),
            "SEWING PATTERNS",
            fontname="helv",
            fontsize=7.5,
            color=(0.4, 0.4, 0.4)
        )

    doc.set_metadata({})
    doc.save(out_pdf_path, garbage=4, deflate=True)
    doc.close()

# 1. Download all 10 Tailornova SVG diagrams and render to 300 DPI PNG
svg_urls = {
    "01_pleats_and_back_darts": "https://admin.patternfast.ai/instructions_images/20df3d4a4106961e5bf00e7a65d861c0.svg",
    "02_back_darts_alt": "https://admin.patternfast.ai/instructions_images/8e6b919835d368cd76344b51fdb99373.svg",
    "03_side_pockets": "https://admin.patternfast.ai/instructions_images/c863fc28cc2feff5ddf6715dc2a25cca.svg",
    "04_back_welt_pockets": "https://admin.patternfast.ai/instructions_images/970e78452c416aabdb675e4d8f1348f8.svg",
    "05_zipper_fly": "https://admin.patternfast.ai/instructions_images/3b1a35074fda547b69d02f31bc4e94b3.svg",
    "06_inseams": "https://admin.patternfast.ai/instructions_images/ae908af490717bf723c424ed4a63b9d2.svg",
    "07_crotch_seam": "https://admin.patternfast.ai/instructions_images/664a91b278f313a553722ed65cf0a659.svg",
    "08_side_seams": "https://admin.patternfast.ai/instructions_images/037502f7e4ad2ed97b2d22f6f5a562fc.svg",
    "09_waistband": "https://admin.patternfast.ai/instructions_images/4f75d77cccb0f4893595e153b4538e70.svg",
    "10_hem": "https://admin.patternfast.ai/instructions_images/cd094cf0cd9ef4db96bba0f02c224d3a.svg"
}

for name, url in svg_urls.items():
    svg_path = os.path.join(out_dir, "source_instructions", "svgs", f"{name}.svg")
    png_path = os.path.join(out_dir, "source_instructions", "svgs", f"{name}.png")
    subprocess.run(["curl.exe", "-s", url, "-o", svg_path], check=True)
    doc = fitz.open(svg_path)
    pix = doc[0].get_pixmap(dpi=300)
    pix.save(png_path)
    doc.close()
    print(f"Downloaded & rendered {name}.png ({pix.width}x{pix.height})")

# 2. Download all 13 sizes x 3 formats (A4, US Letter, A0) = 39 PDFs
with open(os.path.join(out_dir, "mannequins.json"), "r", encoding="utf-8") as f:
    mannequins = json.load(f)

token = get_token()

# Also download the Tailornova Sewing Instructions PDF for Size 0
si_post = {
    "sketchFront": open("pants_pleated_svgFront.svg", encoding="utf-8").read(),
    "sketchBack": open("pants_pleated_svgBack.svg", encoding="utf-8").read(),
    "name": "Colette Wide-Leg Trousers"
}
si_post_path = os.path.join(out_dir, "source_instructions", "si_post.json")
with open(si_post_path, "w", encoding="utf-8") as f:
    json.dump(si_post, f)

si_qs = urllib.parse.urlencode({
    "elementIds": "30145,85721,79534",
    "mannequinId": mannequins[1]["mannequinId"],
    "categoryCode": "wm_pants",
    "format": "pdf",
    "orientation": "portrait",
    "eases": "",
    "settingCodes": "",
    "seamAllowance": "1",
    "fabricType": "1",
    "fit": "2"
})
si_pdf_path = os.path.join(out_dir, "source_instructions", "Tailornova_Colette_Instructions.pdf")
subprocess.run([
    "curl.exe", "-s", "-X", "POST", f"https://api.patternfast.com/api/sewing-instructions?{si_qs}",
    "-H", f"Authorization: Bearer {token}",
    "-H", "Content-Type: application/json; charset=UTF-8",
    "--data-binary", f"@{si_post_path}",
    "-o", si_pdf_path
], check=True)
print("Downloaded Tailornova_Colette_Instructions.pdf:", os.path.getsize(si_pdf_path), "bytes")

for idx, man in enumerate(mannequins):
    if idx % 4 == 0:
        token = get_token()
    sz_name = man["name"]
    size_label = f"SIZE {sz_name}"
    man_id = man["mannequinId"]

    preview_qs = urllib.parse.urlencode({
        "elemIds": "30145,85721,79534",
        "mannequinId": man_id,
        "fabricType": "1",
        "fit": "2",
        "seamAllowance": "1",
        "eases": "",
        "settingCodes": "",
        "fontName": "AvenirNext LT Pro",
        "debug_params": "1",
        "view": "2"
    })
    res = subprocess.run([
        "curl.exe", "-s", "-X", "GET", f"https://api.patternfast.com/api/patterns/preview?{preview_qs}",
        "-H", f"Authorization: Bearer {token}",
        "-H", "Accept: application/json"
    ], capture_output=True, text=True, encoding="utf-8")
    preview_data = json.loads(res.stdout)
    param_kits = preview_data["parameterizedKits"]

    for fmt_folder, api_page_size in [("A4", "A4"), ("US Letter", "LETTER"), ("A0", "A0")]:
        raw_pdf = os.path.join(out_dir, "raw_pdfs", f"{size_label}_{api_page_size}.pdf")
        clean_pdf = os.path.join(out_dir, fmt_folder, f"{size_label}.pdf")
        if os.path.exists(clean_pdf) and os.path.getsize(clean_pdf) > 10000:
            continue
        dl_payload = {
            "mannequinId": man_id,
            **param_kits,
            "cutVerticallySymmetric": False,
            "pageSize": api_page_size
        }
        payload_file = os.path.join(out_dir, "raw_pdfs", "tmp_payload.json")
        with open(payload_file, "w", encoding="utf-8") as pf:
            json.dump(dl_payload, pf)
        subprocess.run([
            "curl.exe", "-s", "-X", "POST", "https://api.patternfast.com/api/cat/download-pdf",
            "-H", f"Authorization: Bearer {token}",
            "-H", "Content-Type: application/json; charset=UTF-8",
            "--data-binary", f"@{payload_file}",
            "-o", raw_pdf
        ], check=True)
        whitelabel_pattern_pdf(raw_pdf, clean_pdf, size_label)
    print(f"Completed {size_label} (A4, US Letter, A0)")

# 3. Package A4.zip, US Letter.zip, A0.zip matching the exact folder structure of the reference ZIPs
for fmt_folder in ["A4", "US Letter", "A0"]:
    zip_path = os.path.join(out_dir, f"{fmt_folder}.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        folder_full = os.path.join(out_dir, fmt_folder)
        for fn in sorted(os.listdir(folder_full)):
            if fn.endswith(".pdf"):
                zf.write(os.path.join(folder_full, fn), f"{fmt_folder}/{fn}")
    print(f"Created {zip_path} ({os.path.getsize(zip_path)} bytes)")
