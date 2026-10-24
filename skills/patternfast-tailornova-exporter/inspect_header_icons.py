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
    page.wait_for_timeout(4000)

    # Inspect the icons in the top bar (header)
    header_icons = page.evaluate("""() => {
        const topBar = document.querySelector('header') || document.querySelector('.top-bar') || document.querySelector('[class*="header"]');
        const svgs = Array.from(document.querySelectorAll('header svg, .top-bar svg, div[class*="header"] svg, div[class*="nav"] svg, div[class*="tool"] svg'));
        return svgs.map((s, idx) => {
            const parent = s.closest('button') || s.closest('a') || s.parentElement;
            return {
                idx,
                tag: parent ? parent.tagName : '',
                class: parent ? parent.className : '',
                onclick: parent ? parent.getAttribute('onclick') : '',
                outer: parent ? parent.outerHTML.slice(0, 150) : s.outerHTML.slice(0, 100)
            };
        });
    }""")
    print("Header icons:")
    for h in header_icons[:25]:
        print(h)

    ctx.close()
