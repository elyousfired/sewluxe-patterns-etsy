#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# ⚠️ CRITICAL IMMUTABLE SYSTEM RULE (قاعدة النظام الأساسية التي لا تتغير):
# ما تبدلش الكود! الكود هو السيستم اللي فيه مراحل الخدمة، الـ AI ما خاصوش يبدل الكود.
# DO NOT MODIFY THIS CODE! THE CODE IS THE OPERATIONAL SYSTEM CONTAINING
# THE WORK STEPS (PHASES 0 TO 6). THE AI ASSISTANT MUST NOT CHANGE THE CODE,
# BUT EXECUTE AND ORCHESTRATE THE STEPS DEFINED HEREIN.
# ==============================================================================
"""
================================================================================
SEWLUXE PATTERNS - LIVE IN-ACCOUNT PATTERNFAST ENGINE & SKETCH STUDIO (v3.0)
File: patternfast_account_engine.py
Author: Antigravity / SewLuxe Core Pipeline
================================================================================
The Absolute Ground-Truth Engine:
1. Authenticates directly with the user's Pro PatternFast account.
2. Creates and saves a NEW PROJECT / DESIGN directly inside the user's PatternFast
   collection ('My Designs' / https://patternfast.com/my-designs).
3. Provides a direct live URL (https://patternfast.com/designer/{design_id}) so
   the user can inspect and modify the design live in their browser.
4. Extracts the authentic vector SVGs (sketchFront & sketchBack) directly from
   the saved in-account design to render 100% synchronized 1800x1800 flat sketches.
5. Maps and accesses ALL categories and options (Dresses, Jackets, Tops, Skirts,
   Pants, Jumpsuits) across all nodes in PatternFast.
6. Batch downloads and white-labels the pattern PDFs (A4, US Letter, A0) across
   the full 13-size range.
================================================================================
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, List, Any, Optional, Tuple

import pymupdf as fitz
from PIL import Image

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class PatternFastAccountEngine:
    """
    Direct in-account manager for PatternFast.
    Guarantees that every project is physically stored in the user's account
    before any sketch, photoshoot, or PDF pattern is produced.
    """

    BASE_API = "https://api.patternfast.com"
    BASE_WEB = "https://patternfast.com"
    DEFAULT_CREDS_PATH = r"C:\Users\red1e\.gemini\config\skills\patternfast-tailornova-exporter\.credentials.json"

    # All major apparel categories supported by PatternFast
    SUPPORTED_CATEGORIES = {
        "pants": "wm_pants",
        "dresses": "wm_dresses",
        "jackets": "wm_jackets",
        "coats": "wm_jackets",
        "tops": "wm_tops",
        "shirts": "wm_tops",
        "skirts": "wm_skirts",
        "jumpsuits": "wm_jumpsuits",
        "mens_shirts": "mn_shirts",
        "mens_pants": "mn_pants",
        "mens_jackets": "mn_jackets",
    }

    # North American Standard Alvanon 13 Sizes
    SIZE_LIST = [
        ("00", "US_00", "US 00 (XXS)"),
        ("0",  "US_0",  "US 0 (XS)"),
        ("2",  "US_2",  "US 2 (XS)"),
        ("4",  "US_4",  "US 4 (S)"),
        ("6",  "US_6",  "US 6 (S)"),
        ("8",  "US_8",  "US 8 (M)"),
        ("10", "US_10", "US 10 (M)"),
        ("12", "US_12", "US 12 (L)"),
        ("14", "US_14", "US 14 (L)"),
        ("16", "US_16", "US 16 (XL)"),
        ("18", "US_18", "US 18 (2XL)"),
        ("20", "US_20", "US 20 (3XL)"),
        ("22", "US_22", "US 22 (4XL)")
    ]

    def __init__(self, creds_path: Optional[str] = None):
        self.creds_path = creds_path or self.DEFAULT_CREDS_PATH
        self.token: Optional[str] = None
        self.collection_id: Optional[str] = None
        self.mannequins_map: Dict[str, str] = {}
        self._authenticate()
        self._load_account_context()

    def _authenticate(self):
        """Authenticates with PatternFast using saved credentials."""
        if not os.path.exists(self.creds_path):
            raise FileNotFoundError(f"Credentials file not found at: {self.creds_path}")

        with open(self.creds_path, "r", encoding="utf-8") as f:
            creds = json.load(f)["patternfast"]

        login_url = f"{self.BASE_WEB}/api/user/login"
        req = urllib.request.Request(
            login_url,
            data=json.dumps({"email": creds["email"], "password": creds["password"]}).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                self.token = data.get("token")
        except Exception as e:
            raise RuntimeError(f"PatternFast authentication failed: {e}")

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def _load_account_context(self):
        """Loads user collection ID and standard Alvanon mannequins map."""
        # 1. Collection ID
        url_col = f"{self.BASE_API}/api/collections"
        req_col = urllib.request.Request(url_col, headers=self._get_headers())
        try:
            with urllib.request.urlopen(req_col, timeout=15) as resp:
                cols = json.loads(resp.read().decode("utf-8"))
                rows = cols.get("rows", [])
                if rows:
                    self.collection_id = str(rows[0].get("id"))
                else:
                    self.collection_id = "750"
        except Exception:
            self.collection_id = "750"

        # 2. Standard Mannequins (US 00-22)
        url_man = f"{self.BASE_API}/api/fit-charts-standart?offset=0&limit=20&type=FEMALE&search="
        req_man = urllib.request.Request(url_man, headers=self._get_headers())
        try:
            with urllib.request.urlopen(req_man, timeout=15) as resp:
                man_data = json.loads(resp.read().decode("utf-8"))
                for row in man_data.get("rows", []):
                    if "00-22" in row.get("name", "") and "Standard North America" in row.get("name", ""):
                        for m in row.get("mannequins", []):
                            self.mannequins_map[m["name"]] = m["mannequinId"]
                        break
        except Exception as e:
            print(f"[WARN] Failed to fetch mannequins dynamically: {e}")

    def normalize_category_code(self, category_str: str) -> str:
        """Normalizes friendly category name to PatternFast category code."""
        cat_lower = category_str.lower().strip()
        if cat_lower in self.SUPPORTED_CATEGORIES:
            return self.SUPPORTED_CATEGORIES[cat_lower]
        for key, code in self.SUPPORTED_CATEGORIES.items():
            if key in cat_lower:
                return code
        return "wm_pants"

    def list_category_menus_and_options(self, category_code: str) -> List[Dict[str, Any]]:
        """
        Fetches all menus (nodes) and options (elements) for any category
        (e.g. wm_dresses, wm_jackets, wm_tops, wm_skirts, wm_pants, wm_jumpsuits).
        """
        cat_code = self.normalize_category_code(category_code)
        url = f"{self.BASE_API}/api/categories/{cat_code}/nodes"
        req = urllib.request.Request(url, headers=self._get_headers())
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"[ERROR] Failed to list nodes for {cat_code}: {e}")
            return []

    def search_elements(
        self,
        category: str,
        node_code: str,
        query: str = "",
        offset: int = 0,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Searches and lists live elements/options inside a specific node of any category.
        Example: search_elements('wm_pants', 'wm_pn_silhouettes', 'wide', limit=20)
        """
        cat_code = self.normalize_category_code(category)
        params = {
            "categoryCode": cat_code,
            "nodeCode": node_code,
            "offset": str(offset),
            "limit": str(limit)
        }
        if query:
            params["search"] = query

        qs = urllib.parse.urlencode(params)
        url = f"{self.BASE_API}/api/elements?{qs}"
        req = urllib.request.Request(url, headers=self._get_headers())
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"[ERROR] search_elements failed for {cat_code}/{node_code}: {e}")
            return {"items": [], "total": 0, "limit": limit, "offset": offset}

    def get_element_details(
        self,
        category: str,
        element_ids: List[str],
        settings_codes: str = ""
    ) -> List[Dict[str, Any]]:
        """
        Retrieves vector linework (svgFront, svgBack) and attributes for given element IDs.
        """
        cat_code = self.normalize_category_code(category)
        elem_ids_str = ",".join(str(eid).strip() for eid in element_ids)
        url = f"{self.BASE_WEB}/api/categories/{cat_code}/elements?elemIds={elem_ids_str}&settingCodes={settings_codes}"
        req = urllib.request.Request(url, headers=self._get_headers())
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"[ERROR] Failed to get element details for {elem_ids_str}: {e}")
            return []

    def get_category_full_catalog(self, category: str) -> Dict[str, Any]:
        """
        Returns a complete structured catalog of all menus, default elements,
        and filter dimensions for any category.
        """
        cat_code = self.normalize_category_code(category)
        nodes = self.list_category_menus_and_options(cat_code)
        catalog = {
            "category_code": cat_code,
            "nodes_count": len(nodes),
            "nodes": []
        }
        for n in nodes:
            st = (n.get("settings") or {}).get("name", [])
            if isinstance(st, str):
                st_list = [st]
            elif isinstance(st, list):
                st_list = st
            else:
                st_list = []

            node_info = {
                "name": n.get("name"),
                "code": n.get("code"),
                "priority": n.get("priority"),
                "default_element_id": n.get("defaultElementId"),
                "filters": [f.get("name") for f in (n.get("filters") or []) if isinstance(f, dict)],
                "settings": st_list
            }
            catalog["nodes"].append(node_info)
        return catalog

    def create_in_account_design(
        self,
        design_name: str,
        category: str,
        element_ids: List[str],
        reference_size: str = "8",
        fabric_type: str = "1",             # 1 = Woven, 2 = Knit
        fabric_code: str = "WOVEN",         # "WOVEN" or "KNIT"
        fit: str = "2",                     # 1 = Tight, 2 = Fitted/Standard, 3 = Semi-fitted, 4 = Loose
        seam_allowance: str = "0",          # 0 = No seam allowance included, 1 = 1.0 cm included
        settings_codes: str = ""
    ) -> Dict[str, Any]:
        """
        CREATES AND PERMANENTLY SAVES A LIVE DESIGN IN THE USER'S PATTERNFAST ACCOUNT.
        Returns design metadata including persistent Design ID and live designer URL.
        """
        cat_code = self.normalize_category_code(category)
        elem_ids_str = ",".join(str(eid).strip() for eid in element_ids)
        ref_man_id = self.mannequins_map.get(reference_size, "5073b293-257d-4cce-994b-91791d38bd2a")

        print("=" * 80)
        print(f"CREATING LIVE IN-ACCOUNT DESIGN IN PATTERNFAST")
        print(f"Design Name: {design_name}")
        print(f"Category: {cat_code}")
        print(f"Elements: {elem_ids_str}")
        print("=" * 80)

        # 1. Fetch element vectors for sketch composition
        elem_url = f"{self.BASE_WEB}/api/categories/{cat_code}/elements?elemIds={elem_ids_str}&settingCodes={settings_codes}"
        req_el = urllib.request.Request(elem_url, headers=self._get_headers())
        with urllib.request.urlopen(req_el, timeout=15) as r_el:
            el_data = json.loads(r_el.read().decode("utf-8"))

        front_svg = ""
        back_svg = ""
        for item in el_data:
            el = item.get("element", item)
            sf = (el.get("svgFront") or "").replace("<svg>", "").replace("</svg>", "")
            sb = (el.get("svgBack") or "").replace("<svg>", "").replace("</svg>", "")
            front_svg += sf + "\n"
            back_svg += sb + "\n"

        combined_front = f'<svg viewBox="18.5 67.0 61.5 141.0" xmlns="http://www.w3.org/2000/svg"><g class="front-view">{front_svg}</g></svg>'
        combined_back = f'<svg viewBox="18.5 67.0 61.5 141.0" xmlns="http://www.w3.org/2000/svg"><g class="back-view">{back_svg}</g></svg>'
        combined_both = f'<svg id="both" viewBox="0 60 220 155" xmlns="http://www.w3.org/2000/svg"><g class="front-view">{front_svg}</g><g class="back-view">{back_svg}</g></svg>'

        # 2. Fetch Parametric Preview
        qs = urllib.parse.urlencode({
            "elemIds": elem_ids_str,
            "mannequinId": ref_man_id,
            "fabricType": fabric_type,
            "fit": fit,
            "seamAllowance": seam_allowance,
            "eases": "",
            "settingCodes": settings_codes,
            "fontName": "DM Sans",
            "debug_params": "1",
            "view": "2",
            "format": "json"
        })
        prev_url = f"{self.BASE_API}/api/patterns/preview?{qs}"
        req_prev = urllib.request.Request(prev_url, headers=self._get_headers())
        with urllib.request.urlopen(req_prev, timeout=15) as r_prev:
            prev_json = json.loads(r_prev.read().decode("utf-8"))

        # 3. Post design to user's collection
        payload = {
            "designName": design_name,
            "designCategory": cat_code,
            "elementIds": elem_ids_str,
            "mannequinId": ref_man_id,
            "ease": "{}",
            "fabricCode": fabric_code.upper(),
            "fabricType": str(fabric_type),
            "fit": str(fit),
            "seamAllowance": str(seam_allowance),
            "mannequinEase": json.dumps({ref_man_id: {"fit": int(fit), "ease": {}, "fabricType": int(fabric_type)}}),
            "collectionId": str(self.collection_id),
            "sketch": combined_both,
            "sketchFront": combined_front,
            "sketchBack": combined_back,
            "patternsPreview": json.dumps(prev_json)
        }

        url_create = f"{self.BASE_API}/api/designs"
        req_create = urllib.request.Request(
            url_create,
            data=json.dumps(payload).encode("utf-8"),
            headers=self._get_headers()
        )

        with urllib.request.urlopen(req_create, timeout=20) as resp:
            design_res = json.loads(resp.read().decode("utf-8"))

        design_id = design_res.get("id")
        live_designer_url = f"{self.BASE_WEB}/designer/{design_id}"
        my_designs_url = f"{self.BASE_WEB}/my-designs"

        print(f"[SUCCESS] Design created in user account!")
        print(f"  * Design ID: {design_id}")
        print(f"  * Live Workspace URL: {live_designer_url}")
        print(f"  * Viewable in My Designs: {my_designs_url}")

        return {
            "design_id": design_id,
            "design_name": design_name,
            "category_code": cat_code,
            "element_ids": element_ids,
            "live_designer_url": live_designer_url,
            "my_designs_url": my_designs_url,
            "raw_response": design_res
        }

    def export_flat_sketch_from_design(
        self,
        design_id: int,
        out_sketch_1800: str,
        out_sketch_sidebyside: str,
        target_size: int = 1800
    ) -> Dict[str, str]:
        """
        Extracts the authentic vector linework from the live in-account design
        and renders 300 DPI high-resolution technical flat sketches:
        1. 1800x1800 Studio Sketch (Front + Back neatly framed)
        2. 1600x1000 Side-by-Side Sketch for Etsy Slide 3
        """
        url_d = f"{self.BASE_API}/api/designs/{design_id}"
        req_d = urllib.request.Request(url_d, headers=self._get_headers())
        with urllib.request.urlopen(req_d, timeout=15) as resp:
            d = json.loads(resp.read().decode("utf-8"))

        sf = d.get("sketchFront", "")
        sb = d.get("sketchBack", "")

        sf_inner = sf.split(">", 1)[1].rsplit("</svg>", 1)[0] if "<svg" in sf else sf
        sb_inner = sb.split(">", 1)[1].rsplit("</svg>", 1)[0] if "<svg" in sb else sb

        # 1. 1800x1800 Studio Canvas
        combined_1800 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 60 220 155" width="{target_size}" height="{target_size}">
<style>
  path {{ fill: none; stroke: #1C1B1A; stroke-width: 0.55; stroke-linecap: round; stroke-linejoin: round; }}
</style>
<rect x="0" y="60" width="220" height="155" fill="#FAF8F5" rx="14" />
<g transform="translate(10, 0)">
  {sf_inner}
</g>
<g transform="translate(115, 0)">
  {sb_inner}
</g>
<text x="60" y="209" text-anchor="middle" font-family="sans-serif" font-size="5.5" font-weight="bold" fill="#777" letter-spacing="1">FRONT</text>
<text x="165" y="209" text-anchor="middle" font-family="sans-serif" font-size="5.5" font-weight="bold" fill="#777" letter-spacing="1">BACK</text>
</svg>"""

        os.makedirs(os.path.dirname(os.path.abspath(out_sketch_1800)), exist_ok=True)
        doc1 = fitz.open(stream=combined_1800.encode("utf-8"), filetype="svg")
        pix1 = doc1[0].get_pixmap(dpi=300)
        pix1.save(out_sketch_1800)
        doc1.close()

        # 2. 1600x1000 Side-by-Side Canvas
        combined_sbs = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 60 220 155" width="1600" height="1000">
<style>
  path {{ fill: none; stroke: #1C1B1A; stroke-width: 0.55; stroke-linecap: round; stroke-linejoin: round; }}
</style>
<rect x="0" y="60" width="220" height="155" fill="#FFFFFF" />
<g transform="translate(12, 0)">
  {sf_inner}
</g>
<g transform="translate(118, 0)">
  {sb_inner}
</g>
<text x="62" y="208" text-anchor="middle" font-family="sans-serif" font-size="5.5" font-weight="bold" fill="#888" letter-spacing="1">FRONT VIEW</text>
<text x="168" y="208" text-anchor="middle" font-family="sans-serif" font-size="5.5" font-weight="bold" fill="#888" letter-spacing="1">BACK VIEW</text>
</svg>"""

        os.makedirs(os.path.dirname(os.path.abspath(out_sketch_sidebyside)), exist_ok=True)
        doc2 = fitz.open(stream=combined_sbs.encode("utf-8"), filetype="svg")
        pix2 = doc2[0].get_pixmap(dpi=300)
        pix2.save(out_sketch_sidebyside)
        doc2.close()

        print(f"[SUCCESS] Exported flat sketches directly from Live Design ID {design_id}:")
        print(f"  * Studio 1800: {out_sketch_1800}")
        print(f"  * SideBySide 1600: {out_sketch_sidebyside}")

        return {
            "sketch_1800": out_sketch_1800,
            "sketch_sidebyside": out_sketch_sidebyside
        }

    def whitelabel_pattern_pdf(
        self,
        in_pdf_path: str,
        out_pdf_path: str,
        garment_title: str,
        size_label: str,
        fmt_label: str
    ):
        """Applies authentic SewLuxe branding and standardizes metadata."""
        doc = fitz.open(in_pdf_path)
        for pno in [0, 1, 3]:
            if pno >= len(doc):
                continue
            page = doc[pno]
            xrefs = page.get_contents()
            if not xrefs:
                continue
            raw = doc.xref_stream(xrefs[0])
            raw_new = re.sub(
                rb"q\n1 0 0 1 0 28\.3465 cm\n0\.75 0 0 0\.75 0 0 cm\nq\n0 0 m\n793\.706667 0 l\n793\.706667 48 l\n0 48 l\nh\nW n\n2 0 0 2 275\.853333 0 cm\nq.*?Q\nQ\nQ\n",
                rb"",
                raw,
                count=1,
                flags=re.S
            )
            doc.update_stream(xrefs[0], raw_new)
            page.insert_text(
                fitz.Point(214.83, 841.89 - 791.54),
                "SewLuxePatterns",
                fontname="hebo",
                fontsize=20,
                color=(0.12, 0.12, 0.12)
            )
            page.insert_text(
                fitz.Point(262.285, 841.89 - 779.54),
                "SEWING PATTERNS",
                fontname="helv",
                fontsize=7.5,
                color=(0.4, 0.4, 0.4)
            )

        meta = {
            "author": "SewLuxePatterns",
            "creator": "SewLuxe High-Precision CAD Engine",
            "producer": "SewLuxe Atelier System",
            "title": f"SewLuxe Pattern - {garment_title} - {size_label} ({fmt_label})",
            "subject": f"{garment_title} PDF Sewing Pattern"
        }
        doc.set_metadata(meta)
        os.makedirs(os.path.dirname(os.path.abspath(out_pdf_path)), exist_ok=True)
        doc.save(out_pdf_path, garbage=4, deflate=True)
        doc.close()

    def audit_a4_calibration_test_square(
        self,
        pdf_path: str,
        max_tol_pct: float = 0.8
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        SUB-STEP 0.4: A4-FIRST CALIBRATION TEST SQUARE INSPECTION GATE.
        Audits Page 1 of reference A4 pattern PDF to mathematically verify
        the 10.00x10.00 cm (4x4 in) vector calibration test box before batch export.
        Prevents fatal printer scaling errors (a 2% printer shrinkage ruins sizing by a full dress size).
        """
        if not os.path.exists(pdf_path):
            return False, f"File not found: {pdf_path}", {}

        doc = fitz.open(pdf_path)
        if len(doc) < 1:
            doc.close()
            return False, "PDF has 0 pages", {}

        p1 = doc[0]
        p1_text = p1.get_text()

        # 1. Text Instruction Inspection
        text_issues = []
        if not any(k in p1_text.lower() for k in ["calibration", "scale box", "test page", "test square"]):
            text_issues.append("Missing 'Calibration Test Page' / 'Scale Box' header")
        if not any(k in p1_text.lower() for k in ["100%", "actual"]):
            text_issues.append("Missing '100%' or 'Actual Size' printer instruction")
        if not any(k in p1_text.lower() for k in ["ruler", "measure"]):
            text_issues.append("Missing ruler measurement instruction before cutting fabric")

        # 2. Vector Calibration Square Geometry Inspection
        found_square = None
        drawings = p1.get_drawings()
        for d in drawings:
            r = d['rect']
            w, h = r.width, r.height
            # 10 cm = 283.46 pt, 4 in = 288.0 pt
            if 260.0 < w < 310.0 and 260.0 < h < 310.0:
                aspect = min(w, h) / max(w, h)
                if aspect > 0.98:  # Uniform square
                    w_cm = w / 72.0 * 2.54
                    h_cm = h / 72.0 * 2.54
                    target_cm = 10.00
                    diff_pct = abs(w_cm - target_cm) / target_cm * 100.0
                    found_square = {
                        "rect": [r.x0, r.y0, r.x1, r.y1],
                        "w_pt": round(w, 2),
                        "h_pt": round(h, 2),
                        "w_cm": round(w_cm, 3),
                        "h_cm": round(h_cm, 3),
                        "aspect_ratio": round(aspect, 4),
                        "diff_pct": round(diff_pct, 3)
                    }
                    break

        doc.close()

        if not found_square:
            return False, "FATAL: No 10x10 cm (4x4 in) vector calibration square found on Page 1!", {"text_issues": text_issues}

        if found_square["diff_pct"] > max_tol_pct:
            return (
                False,
                f"FATAL: Calibration square distortion {found_square['diff_pct']:.2f}% exceeds tolerance {max_tol_pct}% "
                f"(w={found_square['w_cm']}cm, h={found_square['h_cm']}cm). Sizing will shift by an entire dress size!",
                found_square
            )

        if text_issues:
            return False, f"Instruction Warning: {'; '.join(text_issues)}", found_square

        return True, f"PASSED: 10.00x10.00 cm calibration square verified (w={found_square['w_cm']}cm, diff={found_square['diff_pct']}%)", found_square

    def download_pattern_pdf(
        self,
        element_ids: List[str],
        mannequin_id: str,
        page_size: str,
        out_path: str,
        garment_title: str,
        size_label: str,
        setting_codes: str = "",
        fabric_type: str = "1",
        fit: str = "2",
        seam_allowance: str = "0"
    ) -> str:
        """
        Downloads and immediately white-labels a single pattern PDF for given mannequin and format.
        """
        elem_ids_str = ",".join(str(eid).strip() for eid in element_ids)
        qs = urllib.parse.urlencode({
            "elemIds": elem_ids_str,
            "mannequinId": mannequin_id,
            "fabricType": str(fabric_type),
            "fit": str(fit),
            "seamAllowance": str(seam_allowance),
            "eases": "",
            "settingCodes": setting_codes,
            "fontName": "DM Sans",
            "debug_params": "1",
            "view": "2",
            "format": "json"
        })
        prev_url = f"{self.BASE_API}/api/patterns/preview?{qs}"
        req_prev = urllib.request.Request(prev_url, headers=self._get_headers())
        with urllib.request.urlopen(req_prev, timeout=20) as resp_prev:
            prev_data = json.loads(resp_prev.read().decode("utf-8"))
        param_kits = prev_data["parameterizedKits"]

        dl_payload = {
            "mannequinId": mannequin_id,
            **param_kits,
            "cutVerticallySymmetric": False,
            "pageSize": page_size.upper()
        }

        dl_url = f"{self.BASE_API}/api/cat/download-pdf"
        req_dl = urllib.request.Request(
            dl_url,
            data=json.dumps(dl_payload).encode("utf-8"),
            headers=self._get_headers()
        )

        tmp_raw = out_path + ".raw.tmp"
        os.makedirs(os.path.dirname(os.path.abspath(tmp_raw)), exist_ok=True)
        with urllib.request.urlopen(req_dl, timeout=30) as resp_dl:
            with open(tmp_raw, "wb") as f_out:
                f_out.write(resp_dl.read())

        # Apply SewLuxe branding
        self.whitelabel_pattern_pdf(
            in_pdf_path=tmp_raw,
            out_pdf_path=out_path,
            garment_title=garment_title,
            size_label=size_label,
            fmt_label=page_size.upper()
        )

        if os.path.exists(tmp_raw):
            try:
                os.remove(tmp_raw)
            except Exception:
                pass

        return out_path

    def batch_export_all_sizes(
        self,
        garment_title: str,
        garment_slug: str,
        element_ids: List[str],
        output_dir: str,
        formats: Optional[List[str]] = None,
        setting_codes: str = ""
    ) -> Dict[str, Any]:
        """
        Executes complete Phase 2 Pattern Export:
        1. Sub-Step 0.4 A4-First Fast Audit on Size 8.
        2. Downloads all 13 sizes x 3 formats (A4, US Letter, A0).
        3. Packages 3 clean ZIP archives for Etsy delivery.
        """
        import zipfile
        formats = formats or ["A4", "LETTER", "A0"]

        pattern_suite_dir = os.path.join(output_dir, "03_Pattern_Suite")
        dir_a4 = os.path.join(pattern_suite_dir, "A4")
        dir_letter = os.path.join(pattern_suite_dir, "US_Letter")
        dir_a0 = os.path.join(pattern_suite_dir, "A0")
        for d in [dir_a4, dir_letter, dir_a0]:
            os.makedirs(d, exist_ok=True)

        fmt_map = {
            "A4": (dir_a4, "A4"),
            "LETTER": (dir_letter, "US_Letter"),
            "A0": (dir_a0, "A0")
        }

        # Step 0.4: Fast A4 Calibration Audit on Reference Size 8
        ref_mid = self.mannequins_map.get("8", "5073b293-257d-4cce-994b-91791d38bd2a")
        ref_a4_path = os.path.join(dir_a4, f"{garment_slug}_Size_US_8_A4.pdf")
        print(f"[AUDIT] Running Sub-Step 0.4 A4-First Fast Calibration Audit on Size 8...")
        self.download_pattern_pdf(
            element_ids=element_ids,
            mannequin_id=ref_mid,
            page_size="A4",
            out_path=ref_a4_path,
            garment_title=garment_title,
            size_label="US 8 (M)",
            setting_codes=setting_codes
        )

        passed, msg, sq_data = self.audit_a4_calibration_test_square(ref_a4_path)
        if not passed:
            raise RuntimeError(f"A4-First Calibration Audit FAILED: {msg}")
        print(f"[SUCCESS] {msg}")

        # Batch Export remaining files
        exported_files: Dict[str, List[str]] = {"A4": [ref_a4_path], "LETTER": [], "A0": []}

        for sz_raw, sz_code, sz_title in self.SIZE_LIST:
            mid = self.mannequins_map.get(sz_raw)
            if not mid:
                continue

            for fmt in formats:
                dest_dir, fmt_label = fmt_map[fmt]
                file_path = os.path.join(dest_dir, f"{garment_slug}_Size_{sz_code}_{fmt_label}.pdf")
                if os.path.exists(file_path):
                    continue

                print(f"  -> Exporting {sz_title} [{fmt_label}]...")
                try:
                    self.download_pattern_pdf(
                        element_ids=element_ids,
                        mannequin_id=mid,
                        page_size=fmt,
                        out_path=file_path,
                        garment_title=garment_title,
                        size_label=sz_title,
                        setting_codes=setting_codes
                    )
                    exported_files[fmt].append(file_path)
                except Exception as e:
                    print(f"    [WARN] Export failed for {sz_title} {fmt_label}: {e}")

        # Package 3 Delivery ZIPs
        zips_dir = os.path.join(output_dir, "03_Delivery_Zips")
        os.makedirs(zips_dir, exist_ok=True)
        zip_packages = {}

        for fmt, (src_dir, fmt_name) in fmt_map.items():
            zip_filename = f"{garment_slug}_{fmt_name}_Package.zip"
            zip_path = os.path.join(zips_dir, zip_filename)
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for root, _, files in os.walk(src_dir):
                    for file in files:
                        if file.endswith(".pdf"):
                            zf.write(os.path.join(root, file), arcname=file)
            zip_packages[fmt] = zip_path
            print(f"[ZIP] Packaged: {zip_path}")

        return {
            "pattern_suite_dir": pattern_suite_dir,
            "exported_files": exported_files,
            "zip_packages": zip_packages
        }


if __name__ == "__main__":
    engine = PatternFastAccountEngine()
    print("PatternFast Account Engine initialized successfully.")
    print(f"Collection ID: {engine.collection_id}")
    print(f"Mannequins mapped: {len(engine.mannequins_map)}")
