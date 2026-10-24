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
    page.locator("text='Silhouettes'").first.click()
    page.wait_for_timeout(2500)

    # Search for "Floor Length"
    search_box = page.locator("input[placeholder*='Search']").first
    search_box.click()
    search_box.fill("")
    page.keyboard.type("Floor Length", delay=80)
    page.keyboard.press("Enter")
    page.wait_for_timeout(2000)

    # Inspect all items for "Floor Length"
    floor_items = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('.ElementItem, [class*="ElementItem"]')).map(el => {
            return {
                title: el.getAttribute('title') || el.innerText || '',
                className: el.className
            };
        }).filter(it => it.title.length > 0);
    }""")
    print("Floor Length items count:", len(floor_items))
    unique_titles = sorted(list(set(it['title'] for it in floor_items)))
    print("Unique Floor Length titles:")
    for t in unique_titles:
        print("  *", t)

    # Now let's search "Wide" AND "Floor"
    search_box.click()
    search_box.fill("")
    page.keyboard.type("Wide Leg", delay=80)
    page.keyboard.press("Enter")
    page.wait_for_timeout(2000)

    wide_items = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('.ElementItem, [class*="ElementItem"]')).map(el => {
            return {
                title: el.getAttribute('title') || el.innerText || '',
                className: el.className
            };
        }).filter(it => it.title.length > 0);
    }""")
    unique_wide = sorted(list(set(it['title'] for it in wide_items)))
    print("\nUnique Wide Leg titles:")
    for t in unique_wide:
        print("  *", t)

    ctx.close()
