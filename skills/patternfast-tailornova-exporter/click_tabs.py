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

    tabs = page.locator(".toolbar__tabs__tab").all()
    print("Found tabs:", len(tabs))

    # Let's inspect the 9-dots icon, which is usually tab index 4 or 5
    # Let's hover and click each tab and see what appears
    for i, tab in enumerate(tabs):
        # get inner HTML of tab svg
        svg_html = tab.inner_html()
        print(f"Tab {i}: {svg_html[:80]}")

    # Let's click tab 4 or 5 (the 9 dots icon)
    # Looking at berop_designer.png:
    # 0: undo, 1: redo, 2: tape measure, 3: sliders, 4: grid, 5: 9-dots, 6: document, 7: fabric roll
    if len(tabs) > 5:
        print("Clicking tab 5 (9-dots icon)...")
        tabs[5].click()
        page.wait_for_timeout(2000)
        shot = os.path.join(SCREENSHOT_DIR, "tab5_click.png")
        page.screenshot(path=shot)
        shutil.copy2(shot, os.path.join(BRAIN_DIR, "tab5_click.png"))
        print("Saved tab5 screenshot")

    ctx.close()
