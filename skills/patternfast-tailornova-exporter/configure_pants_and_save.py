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
    page.wait_for_timeout(2500)

    # 1. Click Pants
    print("1. Selecting Pants...")
    page.locator("text='Pants'").first.click()
    page.wait_for_timeout(800)
    page.locator("button:has-text('Next')").first.click()
    page.wait_for_timeout(2500)

    # 2. Select Size chart
    print("2. Selecting Size chart...")
    sc_dropdown = page.locator(".base-dropdown").filter(has_text="Size chart").locator("button").first
    sc_dropdown.click()
    page.wait_for_timeout(1000)
    page.locator(".base-dropdown__item, [class*='item']").filter(has_text="US/CAN Standard Women").first.click()
    page.wait_for_timeout(1500)

    # 3. Select Size 4
    print("3. Selecting Size 4...")
    size_dropdown = page.locator(".base-dropdown").filter(has_text="Choose size").locator("button").first
    size_dropdown.click()
    page.wait_for_timeout(1000)
    page.locator(".base-dropdown__item, [class*='item']").filter(has_text="4").first.click()
    page.wait_for_timeout(1000)

    # 4. Click Create
    print("4. Clicking Create...")
    page.locator("button:has-text('Create')").first.click()
    print("Waiting for Designer to load with Pants...")
    page.wait_for_timeout(15000)

    # Take screenshot of default pants
    shot1 = os.path.join(SCREENSHOT_DIR, "session_pants_loaded.png")
    page.screenshot(path=shot1)
    shutil.copy2(shot1, os.path.join(BRAIN_DIR, "session_pants_loaded.png"))
    print("Saved session_pants_loaded.png")

    # 5. Click Silhouettes
    print("5. Clicking Silhouettes...")
    page.locator("text='Silhouettes'").first.click()
    page.wait_for_timeout(3000)

    shot2 = os.path.join(SCREENSHOT_DIR, "session_pants_silhouettes.png")
    page.screenshot(path=shot2)
    shutil.copy2(shot2, os.path.join(BRAIN_DIR, "session_pants_silhouettes.png"))
    print("Saved session_pants_silhouettes.png")

    # Print elements found in silhouettes list
    sil_items = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('.elements-list div, div[class*="item"]'))
            .map(e => e.innerText ? e.innerText.trim() : '')
            .filter(t => t.length > 0 && t.length < 35);
    }""")
    print("Pants silhouette items:", sil_items[:20])

    ctx.close()
