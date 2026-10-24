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
    page.goto("https://patternfast.com/new-design", wait_until="networkidle", timeout=45000)
    page.wait_for_timeout(2000)

    # Click Pants
    page.locator("text='Pants'").first.click()
    page.wait_for_timeout(500)
    page.locator("button:has-text('Next')").first.click()
    page.wait_for_timeout(2500)

    # Inspect the 'Choose size' dropdown HTML structure
    dd_info = page.evaluate("""() => {
        const dds = Array.from(document.querySelectorAll('.base-dropdown, [class*="dropdown"]'));
        return dds.map(d => ({
            class: d.className,
            html: d.outerHTML.slice(0, 300)
        }));
    }""")
    print("Dropdown structures found:", len(dd_info))
    for d in dd_info:
        print(d)

    ctx.close()
