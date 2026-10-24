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
    page.wait_for_timeout(2000)

    # 1. Click Pants
    print("Selecting Pants...")
    page.locator("text='Pants'").first.click()
    page.wait_for_timeout(800)
    page.locator("button:has-text('Next')").first.click()
    page.wait_for_timeout(2000)

    # 2. Select Size chart
    sc_dropdown = page.locator(".base-dropdown").filter(has_text="Size chart").locator("button").first
    sc_dropdown.click()
    page.wait_for_timeout(800)
    page.locator(".base-dropdown__item, [class*='item']").filter(has_text="US/CAN Standard Women").first.click()
    page.wait_for_timeout(1000)

    # 3. Select Size 4
    size_dropdown = page.locator(".base-dropdown").filter(has_text="Choose size").locator("button").first
    size_dropdown.click()
    page.wait_for_timeout(800)
    page.locator(".base-dropdown__item, [class*='item']").filter(has_text="4").first.click()
    page.wait_for_timeout(800)

    # 4. Click Create
    page.locator("button:has-text('Create')").first.click()
    print("Waiting for Designer to load...")
    page.wait_for_timeout(12000)

    # 5. Click Silhouettes
    print("Opening Silhouettes...")
    page.locator("text='Silhouettes'").first.click()
    page.wait_for_timeout(2500)

    # Inspect the sidebar DOM structure
    dom_info = page.evaluate("""() => {
        const searchInput = document.querySelector('input[placeholder*="Search"]');
        const cards = Array.from(document.querySelectorAll('.elements-list .card, .elements-list > div, div[class*="element"]')).map(el => {
            return {
                text: el.innerText ? el.innerText.trim() : '',
                html: el.outerHTML.slice(0, 150),
                img: el.querySelector('img') ? el.querySelector('img').src : null
            };
        });
        const filters = Array.from(document.querySelectorAll('.filters, [class*="filter"]')).map(f => f.innerText);
        return {
            hasSearch: !!searchInput,
            searchPlaceholder: searchInput ? searchInput.placeholder : null,
            cardCount: cards.length,
            cardsSample: cards.slice(0, 10),
            filters: filters
        };
    }""")
    print("DOM Info:", json.dumps(dom_info, indent=2))

    # Now let's try typing "wide" or "Wide Leg" into the search input
    search_input = page.locator("input[placeholder*='Search']").first
    if search_input.count() > 0:
        print("Typing 'wide' in search input...")
        search_input.fill("wide")
        page.wait_for_timeout(2000)
        
        shot_search = os.path.join(SCREENSHOT_DIR, "silhouettes_search_wide.png")
        page.screenshot(path=shot_search)
        shutil.copy2(shot_search, os.path.join(BRAIN_DIR, "silhouettes_search_wide.png"))
        print("Saved silhouettes_search_wide.png")
        
        # Check filtered cards
        filtered_cards = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('.elements-list .card, .elements-list > div, div[class*="element"]')).map(el => {
                return {
                    text: el.innerText ? el.innerText.trim() : '',
                    img: el.querySelector('img') ? el.querySelector('img').src : null
                };
            }).filter(c => c.text.length > 0 || c.img);
        }""")
        print("Filtered cards:", json.dumps(filtered_cards[:10], indent=2))

    ctx.close()
