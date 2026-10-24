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
    page.goto("https://patternfast.com/ai-designer/wm_pants", wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2500)

    # Step 1: Woven
    page.locator("text=Woven").first.click()
    page.wait_for_timeout(500)
    page.locator("button:has-text('Next')").first.click()
    page.wait_for_timeout(1500)

    # Step 2: Wide Leg
    page.locator("text=Wide Leg").first.click()
    page.wait_for_timeout(500)
    page.locator("button:has-text('Next')").first.click()
    page.wait_for_timeout(1500)

    # Step 3: Floor Length
    page.locator("text=Floor Length").first.click()
    page.wait_for_timeout(500)
    page.locator("button:has-text('Next')").first.click()
    
    print("Waiting for Designer to load generated pants (12 seconds)...")
    page.wait_for_timeout(12000)

    shot = os.path.join(SCREENSHOT_DIR, "pants_designer_loaded.png")
    page.screenshot(path=shot)
    shutil.copy2(shot, os.path.join(BRAIN_DIR, "pants_designer_loaded.png"))
    print("Screenshot saved to:", shot, "| URL:", page.url)

    # Extract Flat Sketch element / SVG
    sketch_el = page.locator(".FlatSketch, [class*='FlatSketch'], [class*='sketch'], div:has(> svg)").first
    # Also extract raw SVGs
    svgs = page.evaluate("""() => {
        const svgEls = Array.from(document.querySelectorAll('svg'));
        return svgEls.map((s, i) => ({
            idx: i,
            w: s.clientWidth,
            h: s.clientHeight,
            viewBox: s.getAttribute('viewBox'),
            id: s.id,
            class: s.className.baseVal || s.className,
            parentClass: s.parentElement ? s.parentElement.className : ''
        })).filter(x => x.w > 100 || x.h > 100);
    }""")
    print("Large SVGs found:", len(svgs))
    for s in svgs:
        print(s)

    ctx.close()
