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

    # Click the Choose size dropdown
    print("Clicking size dropdown...")
    size_btn = page.locator(".base-dropdown__button").last
    size_btn.click()
    page.wait_for_timeout(1000)

    # Click the first size item
    print("Clicking first size item...")
    first_item = page.locator(".base-dropdown__item").first
    print("First item text:", first_item.inner_text())
    first_item.click()
    page.wait_for_timeout(1000)

    # Click Create
    print("Clicking Create button...")
    create_btn = page.locator("button:has-text('Create')").first
    create_btn.click()
    print("Waiting for Designer URL...")
    page.wait_for_url("**/designer**", timeout=30000)
    page.wait_for_timeout(8000)

    shot = os.path.join(SCREENSHOT_DIR, "pants_designer_loaded_final.png")
    page.screenshot(path=shot)
    shutil.copy2(shot, os.path.join(BRAIN_DIR, "pants_designer_loaded_final.png"))
    print("SUCCESS! Screenshot saved to:", shot, "| URL:", page.url)

    ctx.close()
