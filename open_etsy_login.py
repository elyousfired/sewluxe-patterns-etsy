import os
from playwright.sync_api import sync_playwright

PROFILE_DIR = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\etsy_browser_profile"
os.makedirs(PROFILE_DIR, exist_ok=True)
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

print("Opening Etsy persistent profile window...")
with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        executable_path=CHROME_PATH,
        headless=False,
        viewport={"width": 1280, "height": 850},
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.goto("https://www.etsy.com", wait_until="domcontentloaded")
    print("Etsy is now open in your visible Chrome browser.")
    print("Please log in or solve any initial check, then close the browser window when done.")
    try:
        page.wait_for_timeout(60000) # wait up to 60s for user or until closed
    except Exception:
        pass
    context.close()
print("Profile session saved successfully!")
