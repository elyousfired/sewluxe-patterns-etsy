#!/usr/bin/env python3
"""
Universal PatternFast Batch Exporter Template
=============================================
Uses the robust SewLuxe REST API engine to export and white-label all 13 sizes
(US 00 to US 22) across 3 formats (A4, US Letter, A0) in ~60 seconds total.
"""

import os
import sys
import json
from playwright.sync_api import sync_playwright

# Add repo root to sys.path for sewluxe_core access
REPO_ROOT = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy"
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from sewluxe_core.batch_patternfast_exporter import run_batch_export
from sewluxe_core.sewluxe_pipeline_guard import SewLuxePipelineGuard

def extract_session_and_export(
    design_id: int,
    project_dir: str,
    garment_title: str,
    garment_file_slug: str,
    desktop_dir: str = None
):
    profile_dir = r"C:\Users\red1e\.gemini\config\skills\patternfast-tailornova-exporter\browser_profile_berop"
    
    print(f"[PatternFast] Initializing fast session for Design ID {design_id}...")
    auth_token = None
    mannequins = []
    design_elements = []
    setting_codes = []

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=True,
            viewport={"width": 1440, "height": 900}
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        def handle_response(resp):
            nonlocal auth_token, mannequins, design_elements, setting_codes
            url = resp.url
            if "api" in url:
                try:
                    auth = resp.request.headers.get("authorization")
                    if auth and not auth_token:
                        auth_token = auth
                    
                    if "fit-charts" in url:
                        j = resp.json()
                        mannequins = j.get("mannequins", [])
                    elif f"designs/{design_id}" in url:
                        j = resp.json()
                        design_elements = j.get("elements", [])
                        setting_codes = j.get("elementsSettings", [])
                except Exception:
                    pass

        page.on("response", handle_response)
        page.goto(f"https://patternfast.com/designer/{design_id}", wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(6000)
        ctx.close()

    if not auth_token:
        raise RuntimeError("Failed to capture active auth Bearer token from PatternFast session.")
    if not mannequins:
        raise RuntimeError("Failed to capture mannequins fit-chart from PatternFast session.")

    elem_ids = ",".join(str(e) for e in design_elements) if design_elements else "3833,4355"
    settings = ",".join(setting_codes) if setting_codes else "pants_slits:no_slits"

    print(f"[PatternFast] Active Session Confirmed:")
    print(f"  Token: {auth_token[:30]}...")
    print(f"  Elements: {elem_ids}")
    print(f"  Settings: {settings}")
    print(f"  Total Mannequins: {len(mannequins)}")

    # Verify pipeline gate
    guard = SewLuxePipelineGuard(project_dir)
    guard.verify_gate("PHASE_2_BATCH_PATTERN_EXPORT")

    # Run batch export
    count = run_batch_export(
        project_dir=project_dir,
        garment_title=garment_title,
        garment_file_slug=garment_file_slug,
        elem_ids=elem_ids,
        setting_codes=settings,
        token=auth_token,
        mannequins=mannequins,
        desktop_dir=desktop_dir
    )

    if count == 39:
        guard.complete_phase("PHASE_2_BATCH_PATTERN_EXPORT", "All 39 PDFs exported, white-labeled, and packaged into 3 ZIPs.")
        guard.print_status_dashboard()

if __name__ == "__main__":
    # Example execution for active project
    extract_session_and_export(
        design_id=10593,
        project_dir=r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\projects\trendy_high_waist_wide_leg",
        garment_title="Aria Trendy Wide-Leg Pants",
        garment_file_slug="SewLuxe_Aria_Wide_Leg_Pants",
        desktop_dir=r"C:\Users\red1e\Desktop\SewLuxe_Aria_Trendy_Wide_Leg_Pants"
    )
