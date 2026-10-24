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
    page.goto("https://patternfast.com/user/collections", wait_until="networkidle", timeout=45000)
    page.wait_for_timeout(2000)

    # Click on folder 'h'
    print("Clicking folder h...")
    folder = page.locator("text='h'").first
    if folder.is_visible():
        folder.click()
        page.wait_for_timeout(3000)

    shot = os.path.join(SCREENSHOT_DIR, "inside_collection_h.png")
    page.screenshot(path=shot)
    shutil.copy2(shot, os.path.join(BRAIN_DIR, "inside_collection_h.png"))
    print("Saved inside_collection_h.png | URL:", page.url)

    elements = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('button, a, div'))
            .map(e => e.innerText ? e.innerText.trim() : '')
            .filter(t => t.length > 0 && t.length < 50);
    }""")
    print("Elements inside collection h:", set(list(elements)[:30]))

    ctx.close()
