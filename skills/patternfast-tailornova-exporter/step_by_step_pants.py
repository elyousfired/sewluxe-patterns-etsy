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
    page.wait_for_timeout(3000)

    # Click "Woven"
    print("Clicking Woven...")
    woven = page.locator("text=Woven").first
    if woven.is_visible():
        woven.click()
        page.wait_for_timeout(1000)

    # Click "Next"
    next_btn = page.locator("button:has-text('Next')").first
    if next_btn.is_enabled():
        print("Clicking Next...")
        next_btn.click()
        page.wait_for_timeout(3000)

    shot = os.path.join(SCREENSHOT_DIR, "ai_step2.png")
    page.screenshot(path=shot)
    shutil.copy2(shot, os.path.join(BRAIN_DIR, "ai_step2.png"))
    print("Screenshot saved to:", shot)

    # Check visible texts
    texts = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('h1, h2, h3, h4, label, div[class*="title"], div[class*="option"]'))
            .map(e => e.innerText ? e.innerText.trim() : '')
            .filter(t => t.length > 0 && t.length < 60);
    }""")
    print("Options on step 2:", texts[:20])

    ctx.close()
