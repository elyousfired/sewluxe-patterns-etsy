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

    # Click Size chart dropdown
    page.locator("text='Choose...'").first.click()
    page.wait_for_timeout(800)

    # Select EU Standard Women
    print("Selecting EU Standard Women...")
    eu_opt = page.locator(":has-text('EU Standard Women')").first
    if eu_opt.is_visible():
        eu_opt.click()
        page.wait_for_timeout(1000)

    # Open size dropdown (the second Choose...)
    size_dd = page.locator("text='Choose...'").first
    if size_dd.is_visible():
        size_dd.click()
        page.wait_for_timeout(800)
        # Click e.g. size 38 or first available size
        first_size = page.locator(".base-dropdown__item, .dropdown-item, li").filter(has_text="38").first
        if not first_size.is_visible():
            first_size = page.locator(".base-dropdown__item, .dropdown-item, li").first
        if first_size.is_visible():
            print("Selecting size:", first_size.inner_text())
            first_size.click()
            page.wait_for_timeout(800)

    # Click 'Create' button
    create_btn = page.locator("button:has-text('Create')").first
    if create_btn.is_enabled():
        print("Clicking Create button...")
        create_btn.click()
        page.wait_for_timeout(12000)

    shot = os.path.join(SCREENSHOT_DIR, "pants_designer_custom_loaded.png")
    page.screenshot(path=shot)
    shutil.copy2(shot, os.path.join(BRAIN_DIR, "pants_designer_custom_loaded.png"))
    print("Screenshot saved to:", shot, "| URL:", page.url)

    # Check left sidebar categories
    categories = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('div[class*="category"], div[class*="sidebar"] div, div[class*="item"]'))
            .map(e => e.innerText ? e.innerText.trim() : '')
            .filter(t => t.length > 0 && t.length < 25);
    }""")
    print("Sidebar categories found:", set(list(categories)[:30]))

    ctx.close()
