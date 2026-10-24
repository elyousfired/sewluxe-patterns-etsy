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

    # 3. Open Silhouettes
    print("Opening Silhouettes...")
    page.locator("text='Silhouettes'").first.click()
    page.wait_for_timeout(2500)

    # Search for "Wide Leg Floor Length"
    search_box = page.locator("input[placeholder*='Search']").first
    search_box.click()
    search_box.fill("")
    page.keyboard.type("Floor Length", delay=80)
    page.keyboard.press("Enter")
    page.wait_for_timeout(2500)

    # Find the element with title 'Wide Leg Floor Length'
    wide_leg_card = page.locator(".ElementItem[title='Wide Leg Floor Length']").first
    print("Found 'Wide Leg Floor Length' card:", wide_leg_card.count() > 0)
    if wide_leg_card.count() > 0:
        wide_leg_card.click()
        print("Clicked 'Wide Leg Floor Length'!")
        page.wait_for_timeout(4000)

    # Screenshot after selecting Wide Leg Floor Length
    shot1 = os.path.join(SCREENSHOT_DIR, "designer_wide_leg_selected.png")
    page.screenshot(path=shot1)
    shutil.copy2(shot1, os.path.join(BRAIN_DIR, "designer_wide_leg_selected.png"))

    # 4. Inspect Waist Bands menu
    print("\nOpening Waist Bands...")
    page.locator("text='Waist Bands'").first.click()
    page.wait_for_timeout(2500)

    waistband_items = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('.ElementItem, [class*="ElementItem"]')).map(el => {
            return {
                title: el.getAttribute('title') || el.innerText || '',
                className: el.className
            };
        }).filter(it => it.title.length > 0);
    }""")
    print(f"Total Waist Bands items found: {len(waistband_items)}")
    unique_wb = sorted(list(set(it['title'] for it in waistband_items)))
    print("Unique Waist Bands:")
    for w in unique_wb:
        print("  -", w)

    shot_wb = os.path.join(SCREENSHOT_DIR, "designer_waistbands_menu.png")
    page.screenshot(path=shot_wb)
    shutil.copy2(shot_wb, os.path.join(BRAIN_DIR, "designer_waistbands_menu.png"))

    # 5. Inspect Pockets menu
    print("\nOpening Pockets...")
    page.locator("text='Pockets'").first.click()
    page.wait_for_timeout(2500)

    pocket_items = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('.ElementItem, [class*="ElementItem"]')).map(el => {
            return {
                title: el.getAttribute('title') || el.innerText || '',
                className: el.className
            };
        }).filter(it => it.title.length > 0);
    }""")
    print(f"Total Pockets items found: {len(pocket_items)}")
    unique_pk = sorted(list(set(it['title'] for it in pocket_items)))
    print("Unique Pockets:")
    for p in unique_pk:
        print("  -", p)

    # 6. Check Flat Sketch SVG
    svg_info = page.evaluate("""() => {
        const svgBoth = document.querySelector('svg#both');
        const allSvgs = Array.from(document.querySelectorAll('svg')).map(s => ({
            id: s.id,
            className: s.className ? s.className.baseVal || s.className : '',
            width: s.getAttribute('width'),
            height: s.getAttribute('height'),
            viewBox: s.getAttribute('viewBox'),
            childCount: s.children.length
        }));
        return {
            hasSvgBoth: !!svgBoth,
            svgBothHtml: svgBoth ? svgBoth.outerHTML.slice(0, 300) : null,
            svgList: allSvgs
        };
    }""")
    print("\nSVG Info:", json.dumps(svg_info, indent=2))

    ctx.close()
