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
    page.goto("https://patternfast.com/designer", wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(4000)

    # Click menu-icon
    print("Clicking menu-icon...")
    menu = page.locator(".menu-icon").first
    if menu.is_visible():
        menu.click()
        page.wait_for_timeout(2000)

    shot = os.path.join(SCREENSHOT_DIR, "after_menu_click.png")
    page.screenshot(path=shot)
    shutil.copy2(shot, os.path.join(BRAIN_DIR, "after_menu_click.png"))
    print("Screenshot saved to:", shot)

    # Check visible text
    texts = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('div, a, button, span, li'))
            .map(e => e.innerText ? e.innerText.trim() : '')
            .filter(t => t.length > 0 && t.length < 50);
    }""")
    print("Sample texts found:", set(list(texts)[:50]))

    ctx.close()
