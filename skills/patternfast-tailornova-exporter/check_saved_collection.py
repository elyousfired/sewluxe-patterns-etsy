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
    page.goto("https://patternfast.com/user/collections", wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(3000)

    # Check collections and items
    coll_info = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('.card, [class*="collection"], [class*="design"]')).map(el => ({
            text: el.innerText ? el.innerText.trim() : '',
            className: el.className
        })).filter(c => c.text.length > 0 && c.text.length < 150);
    }""")
    print("Collections list:", json.dumps(coll_info[:10], indent=2))

    shot_coll = os.path.join(SCREENSHOT_DIR, "user_collections_with_saved_pants.png")
    page.screenshot(path=shot_coll)
    shutil.copy2(shot_coll, os.path.join(BRAIN_DIR, "user_collections_with_saved_pants.png"))
    print("Saved user_collections_with_saved_pants.png")

    # Let's click into collection 'h' or the first collection
    col_card = page.locator("text='h'").first
    if col_card.count() > 0:
        col_card.click()
        page.wait_for_timeout(3000)
        
        designs_in_col = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('.card, [class*="design-card"], [class*="item"]')).map(el => ({
                text: el.innerText ? el.innerText.trim() : '',
                className: el.className
            })).filter(c => c.text.length > 0 && c.text.length < 150);
        }""")
        print("Designs in Collection:", json.dumps(designs_in_col, indent=2))
        
        shot_inside = os.path.join(SCREENSHOT_DIR, "collection_h_with_sewluxe_pants.png")
        page.screenshot(path=shot_inside)
        shutil.copy2(shot_inside, os.path.join(BRAIN_DIR, "collection_h_with_sewluxe_pants.png"))
        print("Saved collection_h_with_sewluxe_pants.png")

    ctx.close()
