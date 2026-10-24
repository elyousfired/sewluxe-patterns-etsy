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
    page.goto("https://patternfast.com/categories", wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(3000)

    shot = os.path.join(SCREENSHOT_DIR, "categories_page.png")
    page.screenshot(path=shot)
    shutil.copy2(shot, os.path.join(BRAIN_DIR, "categories_page.png"))
    print("Categories screenshot saved:", shot)

    # Print visible links/cards
    cards = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('a, button, div[class*="card"], div[class*="category"]'))
            .map(e => ({ text: e.innerText ? e.innerText.trim() : '', href: e.getAttribute('href') }))
            .filter(x => x.text && x.text.length < 40);
    }""")
    print("Categories cards found:", len(cards))
    for c in cards[:25]:
        print(c)

    ctx.close()
