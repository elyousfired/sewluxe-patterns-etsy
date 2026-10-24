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

    api_logs = []
    page.on("response", lambda resp: api_logs.append({
        "url": resp.url,
        "status": resp.status,
        "method": resp.request.method
    }) if "patternfast.com/api" in resp.url else None)

    page.goto("https://patternfast.com/new-design", wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2000)

    # Category selection
    page.locator("text='Pants'").first.click()
    page.wait_for_timeout(800)
    page.locator("button:has-text('Next')").first.click()
    page.wait_for_timeout(2000)

    # Size Chart & Size
    sc_dropdown = page.locator(".base-dropdown").filter(has_text="Size chart").locator("button").first
    sc_dropdown.click()
    page.wait_for_timeout(800)
    page.locator(".base-dropdown__item, [class*='item']").filter(has_text="US/CAN Standard Women").first.click()
    page.wait_for_timeout(1000)

    size_dropdown = page.locator(".base-dropdown").filter(has_text="Choose size").locator("button").first
    size_dropdown.click()
    page.wait_for_timeout(800)
    page.locator(".base-dropdown__item, [class*='item']").filter(has_text="4").first.click()
    page.wait_for_timeout(800)

    page.locator("button:has-text('Create')").first.click()
    page.wait_for_timeout(12000)

    # Select Wide Leg Floor Length
    page.locator("text='Silhouettes'").first.click()
    page.wait_for_timeout(2000)
    search_box = page.locator("input[placeholder*='Search']").first
    search_box.click()
    search_box.fill("Floor Length")
    page.keyboard.press("Enter")
    page.wait_for_timeout(2000)
    page.locator(".ElementItem[title='Wide Leg Floor Length']").first.click()
    page.wait_for_timeout(3000)

    # Select Waistband Side Button
    page.locator("text='Waist Bands'").first.click()
    page.wait_for_timeout(2000)
    page.locator(".ElementItem[title='Waistband Side Button']").first.click()
    page.wait_for_timeout(3000)

    # Clear api logs before saving
    api_logs.clear()

    # Click Save Design
    print("Clicking Save Design...")
    page.locator("button.btn.primary.small.save").first.click()
    page.wait_for_timeout(1500)

    # Fill name
    name_input = page.locator(".save-design-modal input, .modal-component-overlay input").first
    name_input.fill("SewLuxe Wide Leg Pants")
    page.wait_for_timeout(500)

    # Click Save button inside modal
    save_btn_modal = page.locator(".save-design-modal button, .modal-component-overlay button").filter(has_text="Save Design").first
    save_btn_modal.click()
    print("Clicked modal Save Design button...")
    page.wait_for_timeout(5000)

    # Print API responses
    print("API Logs during Save:")
    for l in api_logs:
        print(" ->", l['method'], l['status'], l['url'])

    ctx.close()
