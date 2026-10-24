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

    # Let's inspect the entire DOM of Flat Pattern on the right
    pattern_dom = page.evaluate("""() => {
        const flatPattern = document.querySelector('.Flat_pattern');
        if (!flatPattern) return null;
        
        // Find all text elements in SVGs or divs
        const texts = Array.from(flatPattern.querySelectorAll('text, span, p, div')).map(e => e.textContent.trim()).filter(t => t.length > 0 && t.length < 50);
        
        // Find all svg paths or pieces
        const paths = Array.from(flatPattern.querySelectorAll('path')).length;
        const svgs = Array.from(flatPattern.querySelectorAll('svg')).map(s => ({
            id: s.id,
            className: s.className ? (s.className.baseVal || s.className) : '',
            viewBox: s.getAttribute('viewBox'),
            width: s.getAttribute('width'),
            height: s.getAttribute('height'),
            pathCount: s.querySelectorAll('path').length
        }));

        return {
            texts: Array.from(new Set(texts)),
            totalPaths: paths,
            svgs: svgs
        };
    }""")
    print("Pattern DOM details:", json.dumps(pattern_dom, indent=2))

    ctx.close()
