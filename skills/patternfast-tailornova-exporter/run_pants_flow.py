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
    page.goto("https://patternfast.com/new-design", wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(3000)

    # 1. Click Pants
    print("1. Selecting Pants...")
    pants_card = page.locator("text='Pants'").first
    pants_card.click()
    page.wait_for_timeout(1000)
    page.locator("button:has-text('Next')").first.click()
    page.wait_for_timeout(2500)

    # 2. Click Size chart button
    print("2. Opening Size chart dropdown...")
    sc_dropdown = page.locator(".base-dropdown").filter(has_text="Size chart").locator("button").first
    sc_dropdown.click()
    page.wait_for_timeout(1000)

    # 3. Select US/CAN Standard Women
    print("3. Selecting size chart option...")
    page.locator(".base-dropdown__item, [class*='item']").filter(has_text="US/CAN Standard Women").first.click()
    page.wait_for_timeout(1500)

    # 4. Open Choose size dropdown
    print("4. Opening Choose size dropdown...")
    size_dropdown = page.locator(".base-dropdown").filter(has_text="Choose size").locator("button").first
    size_dropdown.click()
    page.wait_for_timeout(1000)

    # 5. Select Size 4
    print("5. Selecting size 4...")
    page.locator(".base-dropdown__item, [class*='item']").filter(has_text="4").first.click()
    page.wait_for_timeout(1000)

    # 6. Click Create
    print("6. Clicking Create...")
    create_btn = page.locator("button:has-text('Create')").first
    create_btn.click()

    print("7. Waiting for Designer to load...")
    page.wait_for_timeout(15000)

    shot = os.path.join(SCREENSHOT_DIR, "pants_designer_loaded_success.png")
    page.screenshot(path=shot)
    shutil.copy2(shot, os.path.join(BRAIN_DIR, "pants_designer_loaded_success.png"))
    print("SUCCESS! Saved pants_designer_loaded_success.png | URL:", page.url)

    ctx.close()
