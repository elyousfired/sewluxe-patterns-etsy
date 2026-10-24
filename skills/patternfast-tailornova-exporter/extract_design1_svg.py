import json
import os
import shutil
from playwright.sync_api import sync_playwright

BASE_DIR = r"C:\Users\red1e\.gemini\config\skills\patternfast-tailornova-exporter"
PROFILE_DIR = os.path.join(BASE_DIR, "browser_profile_berop")
BRAIN_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0"
PROJECT_SKETCH_DIR = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\projects\trendy_high_waist_wide_leg\02_Technical_Flat_Sketches"

os.makedirs(PROJECT_SKETCH_DIR, exist_ok=True)

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        headless=True,
        viewport={"width": 1440, "height": 900}
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://patternfast.com/ai-designer/wm_pants", wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2500)

    # Step 1: Woven
    page.locator("text=Woven").first.click()
    page.wait_for_timeout(500)
    page.locator("button:has-text('Next')").first.click()
    page.wait_for_timeout(1500)

    # Step 2: Wide Leg
    page.locator("text=Wide Leg").first.click()
    page.wait_for_timeout(500)
    page.locator("button:has-text('Next')").first.click()
    page.wait_for_timeout(1500)

    # Step 3: Floor Length
    page.locator("text=Floor Length").first.click()
    page.wait_for_timeout(500)
    page.locator("button:has-text('Next')").first.click()
    
    print("Waiting for designs to generate...")
    page.wait_for_timeout(12000)

    # Extract Design 1 SVG
    design1_svg = page.evaluate("""() => {
        // Find card with 'Design 1'
        const cards = Array.from(document.querySelectorAll('div')).filter(d => d.innerText && d.innerText.includes('Design 1'));
        for (const card of cards) {
            const svg = card.querySelector('svg#both') || card.querySelector('svg');
            if (svg && svg.clientWidth > 50) {
                return {
                    outerHTML: svg.outerHTML,
                    viewBox: svg.getAttribute('viewBox'),
                    innerHTML: svg.innerHTML
                };
            }
        }
        // Fallback: query all svg#both
        const svgs = Array.from(document.querySelectorAll('svg#both, svg[id="both"]'));
        if (svgs.length > 0) {
            return {
                outerHTML: svgs[0].outerHTML,
                viewBox: svgs[0].getAttribute('viewBox'),
                innerHTML: svgs[0].innerHTML
            };
        }
        return null;
    }""")

    if design1_svg:
        svg_content = design1_svg["outerHTML"]
        print(f"Design 1 SVG found! Length: {len(svg_content)} chars")
        
        # Save SVG directly
        svg_out1 = os.path.join(BRAIN_DIR, "PatternFast_Original_Sketch_Design1.svg")
        svg_out2 = os.path.join(PROJECT_SKETCH_DIR, "PatternFast_Original_Sketch_Design1.svg")
        with open(svg_out1, "w", encoding="utf-8") as f:
            f.write(svg_content)
        with open(svg_out2, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print("Saved raw SVG to:", svg_out1)

        # Also take a crisp snapshot of Design 1 card
        card1 = page.locator("div:has-text('Design 1')").filter(has=page.locator("svg")).last
        if card1:
            png_out1 = os.path.join(BRAIN_DIR, "PatternFast_Original_Sketch_Design1.png")
            png_out2 = os.path.join(PROJECT_SKETCH_DIR, "PatternFast_Original_Sketch_Design1.png")
            card1.screenshot(path=png_out1)
            shutil.copy2(png_out1, png_out2)
            print("Saved card screenshot to:", png_out1)

    ctx.close()
