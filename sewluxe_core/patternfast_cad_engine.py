"""
SewLuxe PatternFast Native CAD Engine
====================================
Automated, parametric browser engine for PatternFast Garment Designer.
Bypasses the random AI Designer (/ai-designer) and directly controls the
professional parametric CAD Garment Designer (/designer via /new-design).

Features:
- Parametric component selection: Silhouettes, Waist Bands, Pockets.
- Native Vector Extraction: Extracts authentic 1:1 SVG linework directly from DOM.
- Vector Normalization: Separates Front and Back views at 1.0 scale and renders 300 DPI PNGs.
- Zero credential leakage: Loads auth from secure local config.
"""

import os
import json
import time
import copy
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, Dict, Any, List

try:
    import pymupdf as fitz
except ImportError:
    import fitz

from PIL import Image, ImageOps
from playwright.sync_api import sync_playwright, Page, BrowserContext


class PatternFastCADEngine:
    def __init__(
        self,
        credentials_path: Optional[str] = None,
        profile_dir: Optional[str] = None,
        headless: bool = True
    ):
        self.headless = headless
        
        # Resolve credentials path safely
        if credentials_path and os.path.exists(credentials_path):
            self.creds_path = credentials_path
        else:
            default_creds = Path(r"C:\Users\red1e\.gemini\config\skills\patternfast-tailornova-exporter\.credentials.json")
            self.creds_path = str(default_creds) if default_creds.exists() else None

        # Resolve profile dir
        if profile_dir:
            self.profile_dir = profile_dir
        else:
            self.profile_dir = r"C:\Users\red1e\.gemini\config\skills\patternfast-tailornova-exporter\browser_profile_berop"

        self.playwright = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    def start(self):
        """Launches the persistent Playwright browser context."""
        self.playwright = sync_playwright().start()
        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.profile_dir,
            headless=self.headless,
            viewport={"width": 1440, "height": 900}
        )
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()

    def close(self):
        """Closes browser session."""
        if self.context:
            self.context.close()
        if self.playwright:
            self.playwright.stop()

    def create_new_design(
        self,
        category: str = "Pants",
        size_chart: str = "US/CAN Standard Women",
        size: str = "4"
    ) -> bool:
        """
        Navigates to /new-design, selects garment category, size chart, and size,
        then launches the standard Parametric Designer.
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")

        print(f"[PatternFast] Navigating to /new-design...")
        self.page.goto("https://patternfast.com/new-design", wait_until="domcontentloaded", timeout=45000)
        self.page.wait_for_timeout(2000)

        # Step 1: Category selection
        print(f"[PatternFast] Selecting category: {category}...")
        self.page.locator(f"text='{category}'").first.click()
        self.page.wait_for_timeout(800)
        self.page.locator("button:has-text('Next')").first.click()
        self.page.wait_for_timeout(2000)

        # Step 2: Size Chart & Size selection
        print(f"[PatternFast] Selecting Size Chart: {size_chart}...")
        sc_dropdown = self.page.locator(".base-dropdown").filter(has_text="Size chart").locator("button").first
        sc_dropdown.click()
        self.page.wait_for_timeout(800)
        self.page.locator(".base-dropdown__item, [class*='item']").filter(has_text=size_chart).first.click()
        self.page.wait_for_timeout(1000)

        print(f"[PatternFast] Selecting Size: {size}...")
        size_dropdown = self.page.locator(".base-dropdown").filter(has_text="Choose size").locator("button").first
        size_dropdown.click()
        self.page.wait_for_timeout(800)
        self.page.locator(".base-dropdown__item, [class*='item']").filter(has_text=size).first.click()
        self.page.wait_for_timeout(800)

        # Step 3: Launch Designer
        print("[PatternFast] Launching Designer...")
        self.page.locator("button:has-text('Create')").first.click()
        self.page.wait_for_timeout(12000)
        return True

    def select_silhouette(self, keyword: str = "Wide Leg Floor Length") -> bool:
        """
        Searches and selects a silhouette element from the 480+ silhouettes list.
        """
        print(f"[PatternFast] Opening Silhouettes menu...")
        self.page.locator("text='Silhouettes'").first.click()
        self.page.wait_for_timeout(2000)

        # Type in the internal search input
        search_box = self.page.locator("input[placeholder*='Search']").first
        search_box.click()
        search_box.fill("")
        self.page.keyboard.type(keyword, delay=60)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(2500)

        card = self.page.locator(f".ElementItem[title*='{keyword}']").first
        if card.count() > 0:
            card.click()
            print(f"[PatternFast] Selected silhouette: '{keyword}'")
            self.page.wait_for_timeout(3500)
            return True
        else:
            print(f"[PatternFast] Warning: Silhouette card '{keyword}' not found directly.")
            return False

    def select_waistband(self, waistband_title: str = "Waistband Side Button") -> bool:
        """
        Selects waistband type (e.g. Waistband Side Button, Waistband Front Button).
        """
        print(f"[PatternFast] Opening Waist Bands menu...")
        self.page.locator("text='Waist Bands'").first.click()
        self.page.wait_for_timeout(2000)

        wb_card = self.page.locator(f".ElementItem[title*='{waistband_title}']").first
        if wb_card.count() > 0:
            wb_card.click()
            print(f"[PatternFast] Selected waistband: '{waistband_title}'")
            self.page.wait_for_timeout(3500)
            return True
        else:
            print(f"[PatternFast] Warning: Waistband '{waistband_title}' not found.")
            return False

    def select_pockets(self, pocket_title: str = "No Front Pockets") -> bool:
        """
        Selects pocket configuration (e.g. No Front Pockets, In-Seam Pockets).
        """
        print(f"[PatternFast] Opening Pockets menu...")
        self.page.locator("text='Pockets'").first.click()
        self.page.wait_for_timeout(2000)

        if "no" in pocket_title.lower():
            # Deselect any selected pocket or click No Front Pockets
            no_pk = self.page.locator(".ElementItem[title*='No Front Pockets'], .ElementItem[title*='NO FRONT POCKETS']").first
            if no_pk.count() > 0:
                no_pk.click()
                print("[PatternFast] Ensured 'No Front Pockets' selected.")
                self.page.wait_for_timeout(2000)
                return True
        else:
            pk_card = self.page.locator(f".ElementItem[title*='{pocket_title}']").first
            if pk_card.count() > 0:
                pk_card.click()
                print(f"[PatternFast] Selected pocket: '{pocket_title}'")
                self.page.wait_for_timeout(3000)
                return True
        return True

    def extract_flat_sketch_svg(self) -> Optional[str]:
        """
        Extracts the authentic SVG outerHTML directly from the Flat Sketch canvas (svg#both).
        """
        svg_html = self.page.evaluate("""() => {
            const svg = document.querySelector('svg#both');
            return svg ? svg.outerHTML : null;
        }""")
        return svg_html

    def save_design(self) -> bool:
        """
        Saves the configured design into the user's PatternFast collection.
        """
        save_btn = self.page.locator("button.btn.primary.small.save").first
        if save_btn.count() > 0:
            save_btn.click()
            self.page.wait_for_timeout(2500)
            print("[PatternFast] Design saved successfully to collection.")
            return True
        return False

    @staticmethod
    def process_and_render_sketch(
        svg_str: str,
        output_svg_path: str,
        output_png_path: str,
        target_size: int = 1800
    ) -> bool:
        """
        Parses PatternFast vector SVG, separates Front and Back views,
        normalizes the Back view scale from 0.7 to 1.0, and renders a clean
        side-by-side technical flat sketch at 300 DPI on a square canvas.
        """
        root = ET.fromstring(svg_str)

        # 1. Front View only
        root_front = copy.deepcopy(root)
        for g in list(root_front):
            if '{http://www.w3.org/2000/svg}g' in g.tag or g.tag == 'g':
                for child in list(g):
                    if child.attrib.get('class') == 'back-view':
                        g.remove(child)

        doc_front = fitz.open(stream=ET.tostring(root_front, encoding='utf-8'), filetype='svg')
        pix_f = doc_front[0].get_pixmap(dpi=300)
        im_front = Image.frombytes("RGB", [pix_f.width, pix_f.height], pix_f.samples)

        # 2. Back View only (remove scale(0.7) and transform)
        root_back = copy.deepcopy(root)
        for g in list(root_back):
            if '{http://www.w3.org/2000/svg}g' in g.tag or g.tag == 'g':
                for child in list(g):
                    if child.attrib.get('class') == 'front-view':
                        g.remove(child)
                    elif child.attrib.get('class') == 'back-view':
                        child.attrib.pop('transform', None)

        doc_back = fitz.open(stream=ET.tostring(root_back, encoding='utf-8'), filetype='svg')
        pix_b = doc_back[0].get_pixmap(dpi=300)
        im_back = Image.frombytes("RGB", [pix_b.width, pix_b.height], pix_b.samples)

        # Helper to crop white borders
        def get_bbox(im):
            gray = im.convert("L")
            inv = ImageOps.invert(gray)
            bbox = inv.getbbox()
            return im.crop(bbox)

        crop_f = get_bbox(im_front)
        crop_b = get_bbox(im_back)

        # 3. Compose on square studio canvas
        canvas = Image.new("RGB", (target_size, target_size), (255, 255, 255))
        target_h = int(target_size * 0.75)

        f_ratio = target_h / crop_f.height
        f_w = int(crop_f.width * f_ratio)
        front_resized = crop_f.resize((f_w, target_h), Image.Resampling.LANCZOS)

        b_ratio = target_h / crop_b.height
        b_w = int(crop_b.width * b_ratio)
        back_resized = crop_b.resize((b_w, target_h), Image.Resampling.LANCZOS)

        gap = int(target_size * 0.07)
        total_w = f_w + b_w + gap
        start_x = (target_size - total_w) // 2
        y = (target_size - target_h) // 2

        canvas.paste(front_resized, (start_x, y))
        canvas.paste(back_resized, (start_x + f_w + gap, y))

        os.makedirs(os.path.dirname(output_png_path), exist_ok=True)
        canvas.save(output_png_path, quality=95)

        with open(output_svg_path, "w", encoding="utf-8") as f:
            f.write(svg_str)

        print(f"[PatternFast] Saved clean technical flat sketch: {output_png_path}")
        return True
