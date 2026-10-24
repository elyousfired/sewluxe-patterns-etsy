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
    page.goto("https://patternfast.com/new-design", wait_until="networkidle", timeout=45000)
    page.wait_for_timeout(2000)

    # Click Pants
    page.locator("text='Pants'").first.click()
    page.wait_for_timeout(500)
    page.locator("button:has-text('Next')").first.click()
    page.wait_for_timeout(2500)

    # Click 'Size chart' dropdown
    print("Clicking Size chart dropdown...")
    dropdowns = page.locator(".base-dropdown__button, select, div:has-text('Choose...')").all()
    print("Dropdowns found:", len(dropdowns))
    if dropdowns:
        dropdowns[0].click()
        page.wait_for_timeout(1000)

    shot = os.path.join(SCREENSHOT_DIR, "size_charts_dropdown.png")
    page.screenshot(path=shot)
    shutil.copy2(shot, os.path.join(BRAIN_DIR, "size_charts_dropdown.png"))
    print("Saved size_charts_dropdown.png")

    # List items in dropdown
    items = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('.base-dropdown__item, .dropdown-item, li, [role="option"]'))
            .map(e => e.innerText.trim())
            .filter(t => t.length > 0 && t.length < 80);
    }""")
    print("Size chart options:", items)

    ctx.close()
