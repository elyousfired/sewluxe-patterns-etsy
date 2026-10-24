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

    # 1. Category selection
    print("Selecting Pants...")
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

    # Launch Designer
    page.locator("button:has-text('Create')").first.click()
    print("Waiting for Designer to load...")
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

    # 4. Select Waistband Side Button
    print("Selecting Waistband Side Button...")
    page.locator("text='Waist Bands'").first.click()
    page.wait_for_timeout(2000)

    side_wb = page.locator(".ElementItem[title='Waistband Side Button']").first
    if side_wb.count() > 0:
        side_wb.click()
        print("Clicked 'Waistband Side Button'!")
        page.wait_for_timeout(3500)

    # 5. Inspect Pattern Pieces (Flat Pattern on the right)
    print("\nInspecting Flat Pattern pieces...")
    pattern_info = page.evaluate("""() => {
        const patternArea = document.querySelector('.Flat_pattern, [class*="Flat_pattern"], [class*="pattern-layout"]');
        const pieces = Array.from(document.querySelectorAll('.Flat_pattern svg text, .Flat_pattern [class*="piece"], [class*="piece-name"], svg.pattern-svg text'))
            .map(t => t.textContent.trim())
            .filter(t => t.length > 0);
        
        const pieceSvgs = Array.from(document.querySelectorAll('.Flat_pattern svg, [class*="Flat_pattern"] svg')).map(s => ({
            width: s.getAttribute('width'),
            height: s.getAttribute('height'),
            viewBox: s.getAttribute('viewBox'),
            childCount: s.children.length
        }));

        return {
            hasPatternArea: !!patternArea,
            piecesText: pieces,
            pieceSvgs: pieceSvgs,
            patternAreaHtml: patternArea ? patternArea.outerHTML.slice(0, 500) : null
        };
    }""")
    print("Pattern pieces info:", json.dumps(pattern_info, indent=2))

    # Take screenshot of the complete designer workspace
    shot_designer = os.path.join(SCREENSHOT_DIR, "designer_full_workspace.png")
    page.screenshot(path=shot_designer)
    shutil.copy2(shot_designer, os.path.join(BRAIN_DIR, "designer_full_workspace.png"))
    print("Saved designer_full_workspace.png")

    # 6. Save Design to Collection
    print("\nSaving Design to Collection...")
    save_btn = page.locator("button.btn.primary.small.save").first
    if save_btn.count() > 0:
        save_btn.click()
        page.wait_for_timeout(2500)
        
        # Check if a naming modal appeared
        naming_input = page.locator("input[placeholder*='name'], input[type='text']:visible").first
        if naming_input.count() > 0:
            print("Naming modal detected. Setting design name...")
            naming_input.fill("SewLuxe Wide Leg Pants")
            page.wait_for_timeout(500)
            confirm_save = page.locator("button:has-text('Save'), button:has-text('Confirm')").first
            if confirm_save.count() > 0:
                confirm_save.click()
                page.wait_for_timeout(2500)
        
        shot_saved = os.path.join(SCREENSHOT_DIR, "designer_save_confirmed.png")
        page.screenshot(path=shot_saved)
        shutil.copy2(shot_saved, os.path.join(BRAIN_DIR, "designer_save_confirmed.png"))
        print("Saved designer_save_confirmed.png")

    # 7. Check Download Options
    print("\nInspecting Download options...")
    download_btn = page.locator("button.btn.secondary.small:has-text('Download')").first
    if download_btn.count() > 0:
        download_btn.click()
        page.wait_for_timeout(2000)

        shot_dl_modal = os.path.join(SCREENSHOT_DIR, "download_modal_options.png")
        page.screenshot(path=shot_dl_modal)
        shutil.copy2(shot_dl_modal, os.path.join(BRAIN_DIR, "download_modal_options.png"))
        print("Saved download_modal_options.png")

        # Let's inspect options inside download modal
        formats = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('.modal-component-overlay button, .modal-component-overlay label, .modal-component-overlay div[class*="item"]'))
                .map(el => el.innerText ? el.innerText.trim() : '')
                .filter(t => t.length > 0);
        }""")
        print("Available download formats:", formats)

    ctx.close()
