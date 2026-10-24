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

    shot = os.path.join(SCREENSHOT_DIR, "user_collections.png")
    page.screenshot(path=shot)
    shutil.copy2(shot, os.path.join(BRAIN_DIR, "user_collections.png"))
    print("Saved user_collections.png | URL:", page.url)

    # Click on the collection "h" or check buttons
    buttons = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('button, a, div[class*="card"]'))
            .map(e => ({ text: e.innerText ? e.innerText.trim() : '', class: e.className, href: e.getAttribute('href') }))
            .filter(x => x.text && x.text.length < 50);
    }""")
    print("Collection page elements:")
    for b in buttons[:20]:
        print(b)

    ctx.close()
