import json
import os
from playwright.sync_api import sync_playwright

BASE_DIR = r"C:\Users\red1e\.gemini\config\skills\patternfast-tailornova-exporter"
PROFILE_DIR = os.path.join(BASE_DIR, "browser_profile_berop")

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        headless=True,
        viewport={"width": 1440, "height": 900}
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://patternfast.com/designer", wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(3000)

    # Check Exit button or red P logo
    logo = page.locator(".LayoutBase__logoContainer, .menu-icon, a[href*='patternfast.com']").all()
    print("Logos / links found:", len(logo))
    
    # Check what URLs exist on patternfast: e.g. /designs, /categories, /dashboard, /workspace
    # Let's test navigating to https://patternfast.com/designs or https://patternfast.com/workspace
    for test_url in [
        "https://patternfast.com/workspace",
        "https://patternfast.com/designs",
        "https://patternfast.com/categories",
        "https://patternfast.com/my-designs"
    ]:
        resp = page.goto(test_url, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(2000)
        print(f"URL: {test_url} -> final: {page.url} (status: {resp.status if resp else 'none'})")

    ctx.close()
