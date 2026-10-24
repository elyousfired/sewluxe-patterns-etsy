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
    page.wait_for_timeout(3000)

    # 1. Click Silhouettes
    print("Clicking Silhouettes...")
    sil = page.locator("text='Silhouettes'").first
    sil.click()
    page.wait_for_timeout(2000)

    shot1 = os.path.join(SCREENSHOT_DIR, "menu_silhouettes.png")
    page.screenshot(path=shot1)
    shutil.copy2(shot1, os.path.join(BRAIN_DIR, "menu_silhouettes.png"))

    # Print silhouette options
    sil_opts = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('.elements-list div, div[class*="item"], div[class*="element"]'))
            .map(e => e.innerText.trim())
            .filter(t => t.length > 0 && t.length < 30);
    }""")
    print("Silhouette options:", set(list(sil_opts)[:25]))

    # 2. Click Waist Bands
    print("Clicking Waist Bands...")
    wb = page.locator("text='Waist Bands'").first
    wb.click()
    page.wait_for_timeout(2000)

    shot2 = os.path.join(SCREENSHOT_DIR, "menu_waistbands.png")
    page.screenshot(path=shot2)
    shutil.copy2(shot2, os.path.join(BRAIN_DIR, "menu_waistbands.png"))

    # Print waistband options
    wb_opts = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('.elements-list div, div[class*="item"], div[class*="element"]'))
            .map(e => e.innerText.trim())
            .filter(t => t.length > 0 && t.length < 30);
    }""")
    print("Waistband options:", set(list(wb_opts)[:25]))

    ctx.close()
