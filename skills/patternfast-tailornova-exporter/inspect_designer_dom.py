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

    # Print all button texts / aria-labels / titles in top bar
    buttons = page.locator("header button, div[class*='toolbar'] button, div[class*='top'] button, nav button, svg").all()
    print(f"Total buttons/svgs found: {len(buttons)}")

    # Let's inspect page HTML or top bar elements
    top_bar_html = page.evaluate("""() => {
        const topEl = document.querySelector('header') || document.querySelector('[class*="header"]') || document.querySelector('[class*="top"]');
        return topEl ? topEl.outerHTML.slice(0, 1500) : 'No top element';
    }""")
    print("Top bar HTML:", top_bar_html[:500])

    # Check categories / new design modal
    # In Tailornova/PatternFast, clicking "Design > New" or Category icon opens the selection modal
    # Let's look for icons on the top toolbar:
    tool_icons = page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('button, [role="button"], a'));
        return els.map(e => ({
            tag: e.tagName,
            text: e.innerText.trim(),
            title: e.getAttribute('title') || '',
            aria: e.getAttribute('aria-label') || '',
            class: e.className
        })).filter(x => x.text || x.title || x.aria);
    }""")
    print("\nActionable elements:")
    for item in tool_icons[:35]:
        print(item)

    ctx.close()
