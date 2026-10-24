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

    # Open size dropdown
    print("Opening Choose size dropdown...")
    page.locator("text='Choose...'").first.click()
    page.wait_for_timeout(800)

    # Click size 4
    print("Clicking size 4...")
    size_4 = page.locator("li, div").filter(has_text="^4$").first
    if not size_4.is_visible():
        size_4 = page.locator("text='4'").last
    size_4.click()
    page.wait_for_timeout(800)

    # Click Create
    print("Clicking Create button...")
    create_btn = page.locator("button:has-text('Create')").first
    create_btn.click()
    print("Waiting 15 seconds for Designer to initialize with Pants...")
    page.wait_for_timeout(15000)

    shot = os.path.join(SCREENSHOT_DIR, "pants_designer_active.png")
    page.screenshot(path=shot)
    shutil.copy2(shot, os.path.join(BRAIN_DIR, "pants_designer_active.png"))
    print("Saved pants_designer_active.png | URL:", page.url)

    # List left menu items
    menu_items = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('div[class*="sidebar"] div, div[class*="menu"] div, div[class*="tab"], div[class*="item"]'))
            .map(e => e.innerText ? e.innerText.trim() : '')
            .filter(t => t.length > 0 && t.length < 30);
    }""")
    print("Pants Designer menu items:", set(list(menu_items)[:40]))

    ctx.close()
