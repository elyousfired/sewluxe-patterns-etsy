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

    # Click on 'Pants' card
    print("Selecting Pants...")
    pants_card = page.locator("text='Pants'").first
    if pants_card.is_visible():
        pants_card.click()
        page.wait_for_timeout(1000)

    # Click Next
    next_btn = page.locator("button:has-text('Next')").first
    if next_btn.is_enabled():
        print("Clicking Next...")
        next_btn.click()
        page.wait_for_timeout(3000)

    shot = os.path.join(SCREENSHOT_DIR, "step2_after_pants.png")
    page.screenshot(path=shot)
    shutil.copy2(shot, os.path.join(BRAIN_DIR, "step2_after_pants.png"))
    print("Saved step2_after_pants.png | URL:", page.url)

    texts = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('h1, h2, h3, h4, div[class*="title"], div[class*="card"], div[class*="category"], a, button, label'))
            .map(e => e.innerText ? e.innerText.trim() : '')
            .filter(t => t.length > 0 && t.length < 50);
    }""")
    print("Visible elements on Step 2/2:", texts[:25])

    ctx.close()
