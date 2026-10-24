import os
import shutil
from playwright.sync_api import sync_playwright

BASE_DIR = r"C:\Users\red1e\.gemini\config\skills\patternfast-tailornova-exporter"
PROFILE_DIR = os.path.join(BASE_DIR, "browser_profile")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
ARTIFACT_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\c675070e-91f4-406b-8086-d794cba1db24"

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        headless=True,
        viewport={"width": 1440, "height": 900},
        accept_downloads=True,
    )

    # 1. Open Tailornova Designer (no login needed)
    page_tn = context.new_page()
    page_tn.goto("https://tailornova.com/designer", wait_until="domcontentloaded", timeout=60000)
    page_tn.wait_for_timeout(6000)
    tn_shot = os.path.join(SCREENSHOT_DIR, "tailornova_designer.png")
    page_tn.screenshot(path=tn_shot)
    shutil.copy(tn_shot, os.path.join(ARTIFACT_DIR, "tailornova_designer.png"))
    print("Tailornova Designer URL:", page_tn.url)

    # 2. Open PatternFast Designer (logged in)
    page_pf = context.new_page()
    page_pf.goto("https://patternfast.com", wait_until="domcontentloaded", timeout=60000)
    page_pf.wait_for_timeout(3000)
    start_btn = page_pf.locator("text=Start Designing").first
    if start_btn.is_visible():
        start_btn.click()
        page_pf.wait_for_timeout(6000)
    pf_shot = os.path.join(SCREENSHOT_DIR, "patternfast_workspace.png")
    page_pf.screenshot(path=pf_shot)
    shutil.copy(pf_shot, os.path.join(ARTIFACT_DIR, "patternfast_workspace.png"))
    print("PatternFast Workspace URL:", page_pf.url)

    context.close()
