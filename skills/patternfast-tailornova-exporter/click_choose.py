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

    # Click locator
    choose_el = page.locator("text='Choose...'").first
    print("Found Choose... locator, clicking it...")
    choose_el.click()
    page.wait_for_timeout(1500)

    shot = os.path.join(SCREENSHOT_DIR, "choose_clicked.png")
    page.screenshot(path=shot)
    shutil.copy2(shot, os.path.join(BRAIN_DIR, "choose_clicked.png"))
    print("Saved choose_clicked.png")

    # List options
    opts = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('.base-dropdown__item, .dropdown-item, li, [role="option"], div[class*="item"]'))
            .map(e => e.innerText.trim())
            .filter(t => t.length > 0 && t.length < 80);
    }""")
    print("Dropdown options found:", opts)

    ctx.close()
