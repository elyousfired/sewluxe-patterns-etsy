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
    page.goto("https://patternfast.com/designer", wait_until="networkidle", timeout=45000)
    print("Page URL:", page.url)

    shot = os.path.join(SCREENSHOT_DIR, "designer_current.png")
    page.screenshot(path=shot)
    shutil.copy2(shot, os.path.join(BRAIN_DIR, "designer_current.png"))
    print("Screenshot saved to:", shot)

    # Let's inspect the entire DOM structure of the header / toolbar
    header_info = page.evaluate("""() => {
        const header = document.querySelector('header') || document.querySelector('.header') || document.querySelector('[class*="header"]');
        return header ? header.outerHTML : 'NO HEADER';
    }""")
    print("Header outerHTML:", header_info[:600])

    ctx.close()
