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
    page.wait_for_timeout(3500)

    # Let's inspect all tabs in toolbar__tabs
    tabs = page.locator(".toolbar__tabs__tab").all()
    print("Total toolbar tabs:", len(tabs))

    for idx, tab in enumerate(tabs):
        tooltip = tab.get_attribute("title") or tab.get_attribute("aria-label") or ""
        # Let's also see what text or hover gives
        tab.hover()
        page.wait_for_timeout(300)
        # Check tooltip element
        tt = page.evaluate("""() => {
            const el = document.querySelector('.tooltip, [role="tooltip"], div[class*="tooltip"]');
            return el ? el.innerText.trim() : '';
        }""")
        print(f"Tab {idx}: attr='{tooltip}', hover_tt='{tt}'")

    # Let's check document icon (tab 6)
    if len(tabs) > 6:
        print("Clicking Tab 6 (Document icon)...")
        tabs[6].click()
        page.wait_for_timeout(2000)
        shot = os.path.join(SCREENSHOT_DIR, "tab6_click.png")
        page.screenshot(path=shot)
        shutil.copy2(shot, os.path.join(BRAIN_DIR, "tab6_click.png"))
        print("Saved tab6 screenshot")

    # Let's check what modals or popups exist
    modal_text = page.evaluate("""() => {
        const modals = Array.from(document.querySelectorAll('.v--modal, .modal, [class*="modal"], [class*="popup"], [class*="dropdown"]'));
        return modals.map(m => m.innerText.trim()).filter(t => t.length > 0);
    }""")
    print("Modal texts:", modal_text)

    ctx.close()
