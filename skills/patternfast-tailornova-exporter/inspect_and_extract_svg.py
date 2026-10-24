import json
import os
import shutil
from playwright.sync_api import sync_playwright

BASE_DIR = r"C:\Users\red1e\.gemini\config\skills\patternfast-tailornova-exporter"
PROFILE_DIR = os.path.join(BASE_DIR, "browser_profile_berop")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
BRAIN_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0"

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        headless=True,
        viewport={"width": 1440, "height": 900}
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://patternfast.com/new-design", wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2000)

    # 1. Click Pants
    page.locator("text='Pants'").first.click()
    page.wait_for_timeout(800)
    page.locator("button:has-text('Next')").first.click()
    page.wait_for_timeout(2000)

    # 2. Size Chart & Size
    sc_dropdown = page.locator(".base-dropdown").filter(has_text="Size chart").locator("button").first
    sc_dropdown.click()
    page.wait_for_timeout(800)
    page.locator(".base-dropdown__item, [class*='item']").filter(has_text="US/CAN Standard Women").first.click()
    page.wait_for_timeout(1000)

    size_dropdown = page.locator(".base-dropdown").filter(has_text="Choose size").locator("button").first
    size_dropdown.click()
    page.wait_for_timeout(800)
    page.locator(".base-dropdown__item, [class*='item']").filter(has_text="4").first.click()
    page.wait_for_timeout(800)

    page.locator("button:has-text('Create')").first.click()
    page.wait_for_timeout(12000)

    # 3. Select Wide Leg Floor Length
    print("Selecting Wide Leg Floor Length...")
    page.locator("text='Silhouettes'").first.click()
    page.wait_for_timeout(2000)

    search_box = page.locator("input[placeholder*='Search']").first
    search_box.click()
    search_box.fill("")
    page.keyboard.type("Floor Length", delay=60)
    page.keyboard.press("Enter")
    page.wait_for_timeout(2000)

    page.locator(".ElementItem[title='Wide Leg Floor Length']").first.click()
    page.wait_for_timeout(3000)

    # 4. Check Waist Bands
    print("Inspecting Waist Bands...")
    page.locator("text='Waist Bands'").first.click()
    page.wait_for_timeout(2000)

    selected_wb = page.evaluate("""() => {
        const sel = document.querySelector('.ElementItem__selected');
        return sel ? (sel.getAttribute('title') || sel.innerText) : 'None';
    }""")
    print("Default selected Waistband:", selected_wb)

    # Let's see what happens if we select "Waistband Side Button"
    side_wb = page.locator(".ElementItem[title*='Side Button']").first
    print("Side Button WB found:", side_wb.count() > 0)
    # Let's inspect all waistband items titles exactly
    wb_list = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('.ElementItem')).map(el => ({
            title: el.getAttribute('title') || el.innerText,
            selected: el.className.includes('selected')
        }));
    }""")
    print("Waistband options:", json.dumps(wb_list, indent=2))

    # 5. Check Pockets
    print("Inspecting Pockets...")
    page.locator("text='Pockets'").first.click()
    page.wait_for_timeout(2000)
    pk_list = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('.ElementItem')).map(el => ({
            title: el.getAttribute('title') || el.innerText,
            selected: el.className.includes('selected')
        }));
    }""")
    print("Pockets options:", json.dumps(pk_list, indent=2))

    # Let's make sure "NO FRONT POCKETS" or "No Front Pockets" is selected
    no_pockets = page.locator(".ElementItem[title*='NO FRONT POCKETS'], .ElementItem[title*='No Front Pockets']").first
    if no_pockets.count() > 0:
        no_pockets.click()
        print("Clicked No Front Pockets!")
        page.wait_for_timeout(2000)

    # 6. Extract SVG of the Flat Sketch
    svg_html = page.evaluate("""() => {
        const svg = document.querySelector('svg#both');
        return svg ? svg.outerHTML : null;
    }""")

    if svg_html:
        svg_path = os.path.join(SCREENSHOT_DIR, "PatternFast_Original_Authentic_Sketch.svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_html)
        shutil.copy2(svg_path, os.path.join(BRAIN_DIR, "PatternFast_Original_Authentic_Sketch.svg"))
        print(f"Extracted SVG successfully! Size: {len(svg_html)} bytes")

    shot_final = os.path.join(SCREENSHOT_DIR, "patternfast_designer_configured.png")
    page.screenshot(path=shot_final)
    shutil.copy2(shot_final, os.path.join(BRAIN_DIR, "patternfast_designer_configured.png"))
    print("Saved patternfast_designer_configured.png")

    ctx.close()
