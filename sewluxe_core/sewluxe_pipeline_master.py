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
SEWLUXE PATTERNS - MASTER PIPELINE COMMAND CENTER & ORCHESTRATOR (v3.0)
File: sewluxe_pipeline_master.py
Author: Antigravity / SewLuxe Core Pipeline
================================================================================
The End-to-End Autonomous Orchestrator:
1. Authenticates directly with the user's Pro PatternFast account.
2. Explores, searches, and discovers elements across ALL categories:
   - Dresses (wm_dresses)
   - Jackets & Coats (wm_jackets)
   - Tops & Blouses (wm_tops)
   - Skirts (wm_skirts)
   - Pants & Trousers (wm_pants)
   - Jumpsuits (wm_jumpsuits)
3. Creates and saves live designs inside the user's collection (collection 750,
   viewable at https://patternfast.com/my-designs and live at https://patternfast.com/designer/{id}).
4. Extracts authentic server vector SVGs to render 300 DPI technical flat sketches
   (1800x1800 Studio + 1600x1000 Side-by-Side).
5. Conducts full textile forensics (GSM, stretch factor, yardage matrix for 60" and 45",
   pre-wash shrinkage, needles, interfacing, thread).
6. Executes Sub-Step 0.4 A4-First Fast Calibration Test Square Inspection (10x10 cm).
7. Automates batch PDF pattern exports and SewLuxe white-labeling across 13 sizes x 3 formats.
8. Enforces the Phase 0 Pre-Production STOP & REPORT Gate before touching downstream production.
================================================================================
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Any, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure sewluxe_core is on sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
for p in [SCRIPT_DIR, PARENT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from sewluxe_core.patternfast_account_engine import PatternFastAccountEngine
from sewluxe_core.sewluxe_textile_engine import SewLuxeTextileEngine, UNIVERSAL_TEXTILE_DATABASE


class SewLuxeMasterPipeline:
    """
    Central Orchestrator for SewLuxe Pattern Production.
    Connects PatternFast account management, textile forensics, CAD auditing,
    and turnkey deliverable packaging.
    """

    def __init__(self, creds_path: Optional[str] = None):
        self.account_engine = PatternFastAccountEngine(creds_path=creds_path)
        print(f"[INIT] SewLuxe Master Pipeline initialized.")
        print(f"  * User Collection ID: {self.account_engine.collection_id}")
        print(f"  * Standard Mannequins Mapped: {len(self.account_engine.mannequins_map)}")

    def run_catalog_discovery(self, category: str) -> Dict[str, Any]:
        """Lists all menus and options for any category."""
        catalog = self.account_engine.get_category_full_catalog(category)
        print("=" * 80)
        print(f"CATALOG DISCOVERY FOR: {catalog['category_code'].upper()} ({catalog['nodes_count']} MENUS)")
        print("=" * 80)
        for i, node in enumerate(catalog["nodes"], 1):
            print(f"{i:02d}. Menu: {node['name']} (code: {node['code']})")
            if node["default_element_id"]:
                print(f"    * Default Element ID: {node['default_element_id']}")
            if node["filters"]:
                print(f"    * Filters: {', '.join(node['filters'])}")
            if node["settings"]:
                print(f"    * Settings: {', '.join(node['settings'])}")
        return catalog

    def run_element_search(
        self,
        category: str,
        node_code: str,
        query: str = "",
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Searches live elements inside a specific category node."""
        res = self.account_engine.search_elements(
            category=category,
            node_code=node_code,
            query=query,
            limit=limit
        )
        items = res.get("items", [])
        total = res.get("total", 0)
        print("=" * 80)
        print(f"SEARCH RESULTS: Category: {category} | Node: {node_code} | Query: '{query}'")
        print(f"Total matching elements in PatternFast: {total} (showing up to {len(items)})")
        print("=" * 80)
        for it in items:
            print(f"  - ID: {it.get('id'):<7} | Name: {it.get('name')}")
        return items

    def run_phase0_workflow(
        self,
        garment_title: str,
        category: str,
        silhouette: str,
        element_ids: List[str],
        output_dir: str,
        garment_slug: Optional[str] = None,
        reference_size: str = "8",
        fabric_type: str = "1",
        fit: str = "2",
        seam_allowance: str = "0",
        settings_codes: str = ""
    ) -> Dict[str, Any]:
        """
        Executes the Mandatory Phase 0 Pre-Production Gate:
        1. Creates live project inside user's PatternFast account (collection 750).
        2. Exports authentic 300 DPI flat sketches (Studio 1800 + Side-by-Side 1600).
        3. Conducts full textile forensics (GSM, stretch factor, yardage matrix, atelier notions).
        4. Formats executive report with DNA table + Textile Card + Live URLs.
        5. HARD STOP: Returns complete report ready for user approval before touching Phase 1.
        """
        slug = garment_slug or garment_title.lower().replace(" ", "_").replace("-", "_")
        sketch_dir = os.path.join(output_dir, "02_Sketches")
        os.makedirs(sketch_dir, exist_ok=True)

        sketch_1800_path = os.path.join(sketch_dir, f"{slug}_flat_sketch_1800.png")
        sketch_sbs_path = os.path.join(sketch_dir, f"{slug}_flat_sketch_sidebyside.png")

        # 1. Create live project in PatternFast account
        design_meta = self.account_engine.create_in_account_design(
            design_name=garment_title,
            category=category,
            element_ids=element_ids,
            reference_size=reference_size,
            fabric_type=fabric_type,
            fabric_code="WOVEN" if fabric_type == "1" else "KNIT",
            fit=fit,
            seam_allowance=seam_allowance,
            settings_codes=settings_codes
        )
        design_id = design_meta["design_id"]

        # 2. Extract authentic SVGs and render 300 DPI flat sketches
        sketches = self.account_engine.export_flat_sketch_from_design(
            design_id=design_id,
            out_sketch_1800=sketch_1800_path,
            out_sketch_sidebyside=sketch_sbs_path
        )

        # 3. Conduct Textile Forensics
        textile_engine = SewLuxeTextileEngine(category=category, silhouette=silhouette)
        textile_card = textile_engine.format_textile_audit_card()
        fabric_spec = textile_engine.get_fabric_spec()

        # 4. Compile Executive Phase 0 Report
        report = {
            "status": "AWAITING_USER_APPROVAL",
            "garment_title": garment_title,
            "category": design_meta["category_code"],
            "design_id": design_id,
            "live_designer_url": design_meta["live_designer_url"],
            "my_designs_url": design_meta["my_designs_url"],
            "element_ids": element_ids,
            "sketch_1800": sketches["sketch_1800"],
            "sketch_sidebyside": sketches["sketch_sidebyside"],
            "fabric_spec": {
                "name": fabric_spec.primary_name,
                "composition": fabric_spec.composition,
                "weight_gsm": fabric_spec.weight_gsm,
                "drape": fabric_spec.drape_characteristic,
                "stretch_factor": fabric_spec.stretch_factor,
                "shrinkage_pct": fabric_spec.shrinkage_prewash_pct,
                "photoshoot_prompt_tags": fabric_spec.photoshoot_prompt_tags
            },
            "textile_card": textile_card
        }

        print("=" * 80)
        print(f"PHASE 0 COMPLETED: LIVE IN-ACCOUNT DESIGN CREATED & READY FOR AUDIT")
        print(f"  * Design ID: {design_id}")
        print(f"  * Live URL: {design_meta['live_designer_url']}")
        print(f"  * Flat Sketch (1800x1800): {sketches['sketch_1800']}")
        print(f"  * Flat Sketch (Side-by-Side): {sketches['sketch_sidebyside']}")
        print("=" * 80)

        return report

    def run_phase2_pattern_export(
        self,
        garment_title: str,
        element_ids: List[str],
        output_dir: str,
        garment_slug: Optional[str] = None,
        setting_codes: str = ""
    ) -> Dict[str, Any]:
        """Executes Phase 2 Batch Pattern Export across 13 sizes x 3 formats."""
        slug = garment_slug or garment_title.lower().replace(" ", "_").replace("-", "_")
        return self.account_engine.batch_export_all_sizes(
            garment_title=garment_title,
            garment_slug=slug,
            element_ids=element_ids,
            output_dir=output_dir,
            setting_codes=setting_codes
        )


def main():
    parser = argparse.ArgumentParser(description="SewLuxe Master Pipeline CLI")
    parser.add_argument("--action", choices=["phase0", "catalog", "search", "export_patterns", "textile_card"], default="catalog")
    parser.add_argument("--category", default="wm_pants", help="Apparel category (wm_pants, wm_dresses, wm_jackets, etc.)")
    parser.add_argument("--silhouette", default="palazzo", help="Silhouette name for textile analysis")
    parser.add_argument("--node", default="wm_pn_silhouettes", help="Category node code for searching elements")
    parser.add_argument("--query", default="", help="Search query string")
    parser.add_argument("--title", default="SewLuxe Custom Garment", help="Product title")
    parser.add_argument("--slug", default="sewluxe_garment", help="File slug")
    parser.add_argument("--elements", default="4367,85721", help="Comma-separated element IDs")
    parser.add_argument("--output", default=r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\projects\custom_garment", help="Output directory")

    args = parser.parse_args()
    pipeline = SewLuxeMasterPipeline()

    if args.action == "catalog":
        pipeline.run_catalog_discovery(args.category)
    elif args.action == "search":
        pipeline.run_element_search(category=args.category, node_code=args.node, query=args.query)
    elif args.action == "textile_card":
        eng = SewLuxeTextileEngine(category=args.category, silhouette=args.silhouette)
        print(eng.format_textile_audit_card())
    elif args.action == "phase0":
        elem_list = [e.strip() for e in args.elements.split(",") if e.strip()]
        pipeline.run_phase0_workflow(
            garment_title=args.title,
            category=args.category,
            silhouette=args.silhouette,
            element_ids=elem_list,
            output_dir=args.output,
            garment_slug=args.slug
        )
    elif args.action == "export_patterns":
        elem_list = [e.strip() for e in args.elements.split(",") if e.strip()]
        pipeline.run_phase2_pattern_export(
            garment_title=args.title,
            element_ids=elem_list,
            output_dir=args.output,
            garment_slug=args.slug
        )


if __name__ == "__main__":
    main()
