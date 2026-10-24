import os
import pymupdf
from playwright.sync_api import sync_playwright

BASE_DIR = r"C:\Users\red1e\.gemini\config\skills\patternfast-tailornova-exporter"
PROFILE_DIR = os.path.join(BASE_DIR, "browser_profile_berop")
BRAIN_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0"

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(user_data_dir=PROFILE_DIR, headless=True)
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://patternfast.com/ai-designer/wm_pants", wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2000)
    page.locator("text=Woven").first.click()
    page.wait_for_timeout(500)
    page.locator("button:has-text('Next')").first.click()
    page.wait_for_timeout(1000)
    page.locator("text=Wide Leg").first.click()
    page.wait_for_timeout(500)
    page.locator("button:has-text('Next')").first.click()
    page.wait_for_timeout(1000)
    page.locator("text=Floor Length").first.click()
    page.wait_for_timeout(500)
    page.locator("button:has-text('Next')").first.click()
    page.wait_for_timeout(12000)

    # Inspect all svgs on page
    svg_data = page.evaluate("""() => {
        const svgs = Array.from(document.querySelectorAll('svg#both'));
        return svgs.map((s, idx) => ({
            idx: idx + 1,
            html: s.outerHTML
        }));
    }""")
    print(f"Total svgs found: {len(svg_data)}")

    for item in svg_data:
        idx = item["idx"]
        html = item["html"]
        has_fly = "M46.22 73.58C46.22 73.58 45.92 89.91" in html
        has_button = "circle" in html or "48.63 72.87" in html
        print(f"Design {idx}: has_fly={has_fly}, has_button={has_button}, len={len(html)}")

        # Save each SVG and render PNG
        svg_file = os.path.join(BRAIN_DIR, f"patternfast_design_{idx}.svg")
        png_file = os.path.join(BRAIN_DIR, f"patternfast_design_{idx}.png")
        with open(svg_file, "w", encoding="utf-8") as f:
            f.write(html)
        doc = pymupdf.open(svg_file)
        pix = doc[0].get_pixmap(dpi=250)
        pix.save(png_file)
        doc.close()

    ctx.close()
