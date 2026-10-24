import re
import fitz

def whitelabel_pattern_pdf(in_pdf_path, out_pdf_path, size_label="SIZE 0"):
    doc = fitz.open(in_pdf_path)
    hex_size = size_label.encode("ascii").hex()
    replacement_tj = f"[<{hex_size}> 0] TJ".encode("latin1")

    # Pages 0, 1, 3 (1-indexed: Pages 1, 2, 4) have the PatternFast logo and header
    for pno in [0, 1, 3]:
        if pno >= len(doc):
            continue
        page = doc[pno]
        xrefs = page.get_contents()
        if not xrefs:
            continue
        raw = doc.xref_stream(xrefs[0])
        # 1. Remove PatternFast vector logo block at top of page:
        # Starts at `q\n1 0 0 1 0 28.3465 cm\n0.75 0 0 0.75 0 0 cm\nq\n0 0 m\n793.706667`
        # Ends right before `/DeviceRGB cs\n0.4666666666666667` (on P1/P2) or `/DeviceRGB CS\n0.8` (on P4)
        raw_new = re.sub(
            rb"q\n1 0 0 1 0 28\.3465 cm\n0\.75 0 0 0\.75 0 0 cm\nq\n0 0 m\n793\.706667 0 l\n793\.706667 48 l\n0 48 l\nh\nW n\n2 0 0 2 275\.853333 0 cm\nq.*?Q\nQ\nQ\n",
            rb"",
            raw,
            count=1,
            flags=re.S
        )
        # 2. Replace "Pattern Name: -" with "SIZE <X>" on Page 1 & Page 2
        if pno in (0, 1):
            raw_new = re.sub(
                rb"\[<50>\s*\d+\s*<6174746572[^>]*>\s*50\s*<202d>\s*0\]\s*TJ",
                replacement_tj,
                raw_new
            )
        doc.update_stream(xrefs[0], raw_new)

        # 3. Stamp SewLuxePatterns / SEWING PATTERNS at exact reference coordinates
        # In PyMuPDF (top-left origin, page height 841.89):
        # Baseline y in PDF bottom-up is 791.54 -> from top: 841.89 - 791.54 = 50.35
        # Baseline y for subtitle is 779.54 -> from top: 841.89 - 779.54 = 62.35
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

if __name__ == "__main__":
    in_p = r"C:\Users\red1e\.gemini\antigravity\scratch\colette_wide_leg_trousers\test_SIZE_0_A4.pdf"
    out_p = r"C:\Users\red1e\.gemini\antigravity\scratch\colette_wide_leg_trousers\test_SIZE_0_A4_clean.pdf"
    whitelabel_pattern_pdf(in_p, out_p, "SIZE 0")
    d = fitz.open(out_p)
    for pno in [0, 1, 3]:
        pix = d[pno].get_pixmap(dpi=150)
        pix.save(rf"C:\Users\red1e\.gemini\antigravity\scratch\colette_wide_leg_trousers\clean_p{pno+1}.png")
    print("Saved clean_p1.png, clean_p2.png, clean_p4.png")
