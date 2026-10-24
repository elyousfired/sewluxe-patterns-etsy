import json
import os
import shutil
from playwright.sync_api import sync_playwright

BASE_DIR = r"C:\Users\red1e\.gemini\config\skills\patternfast-tailornova-exporter"
CRED_PATH = os.path.join(BASE_DIR, ".credentials.json")
PROFILE_DIR = os.path.join(BASE_DIR, "browser_profile_berop")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
BRAIN_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0"

os.makedirs(PROFILE_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

with open(CRED_PATH, "r", encoding="utf-8") as f:
    creds = json.load(f)
pf = creds["patternfast"]

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        headless=True,
        viewport={"width": 1440, "height": 900}
    )
    page = ctx.new_page()
    print("Navigating to https://patternfast.com/login ...")
    page.goto("https://patternfast.com/login", wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(3000)

    email_in = page.locator("input[type='email'], input[placeholder*='name@example.com'], input[type='text']").first
    pass_in = page.locator("input[type='password'], input[placeholder*='Password']").first
    
    if email_in.is_visible() and pass_in.is_visible():
        print(f"Logging in with {pf['email']} ...")
        email_in.fill(pf["email"])
        pass_in.fill(pf["password"])
        pass_in.press("Enter")
        page.wait_for_timeout(5000)

    print("Current URL after login:", page.url)
    
    page.goto("https://patternfast.com/designer", wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(6000)
    print("Current URL at designer:", page.url)

    shot = os.path.join(SCREENSHOT_DIR, "berop_designer.png")
    page.screenshot(path=shot)
    shutil.copy2(shot, os.path.join(BRAIN_DIR, "berop_designer.png"))
    print("Screenshot saved to:", shot)
    ctx.close()
