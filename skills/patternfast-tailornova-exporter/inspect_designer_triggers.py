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

    # Let's inspect buttons, links, download triggers
    triggers = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('button, a, .q-btn, [class*="download"], [class*="save"]')).map(el => ({
            text: el.innerText ? el.innerText.trim() : '',
            title: el.getAttribute('title') || '',
            ariaLabel: el.getAttribute('aria-label') || '',
            className: el.className,
            tag: el.tagName
        })).filter(b => b.text.length > 0 || b.title.length > 0 || b.ariaLabel.length > 0);
    }""")
    print("Found triggers count:", len(triggers))
    for t in triggers:
        if any(w in (t['text'] + t['title'] + t['ariaLabel']).lower() for w in ['save', 'down', 'export', 'print', 'sketch', 'pattern']):
            print(" -", t)

    ctx.close()
