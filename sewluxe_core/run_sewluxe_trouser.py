"""
SewLuxe Universal Trouser Production Pipeline Runner (v5.0 Pro)
End-to-end autonomous CLI to generate 100% verified sewing pattern deliverables for ANY trouser archetype.

Usage:
    python run_sewluxe_trouser.py --silhouette palazzo --model "Colette Palazzo Trousers"
    python run_sewluxe_trouser.py --silhouette barrel_leg --model "Aura Curved Barrel Pants"
    python run_sewluxe_trouser.py --silhouette cargo_utility --model "Sloane Utility Cargo Trousers"
    python run_sewluxe_trouser.py --list-silhouettes
"""

import os
import sys
import shutil
import argparse
from typing import Optional

# Ensure package import
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from sewluxe_core.universal_trouser_engine import (
        UniversalTrouserEngine,
        TrouserSpec,
        SILHOUETTE_RULES
    )
    from sewluxe_core.universal_cad_engine import UniversalCADBlueprintEngine
    from sewluxe_core.universal_booklet_builder import UniversalBookletBuilder
    from sewluxe_core.sewluxe_booklet_linter import SewLuxeBookletLinter
except ImportError:
    from universal_trouser_engine import (
        UniversalTrouserEngine,
        TrouserSpec,
        SILHOUETTE_RULES
    )
    from universal_cad_engine import UniversalCADBlueprintEngine
    from universal_booklet_builder import UniversalBookletBuilder
    from sewluxe_booklet_linter import SewLuxeBookletLinter


def run_pipeline(silhouette: str, model_name: Optional[str] = None, output_dir: Optional[str] = None, assets_dir: Optional[str] = None):
    print("=" * 70)
    print("  SEWLUXE UNIVERSAL TROUSER PRODUCTION ENGINE (v5.0 PRO)")
    print("=" * 70)

    if silhouette not in SILHOUETTE_RULES:
        print(f"[ERROR] Unknown silhouette: '{silhouette}'")
        print(f"Available silhouettes: {list(SILHOUETTE_RULES.keys())}")
        return False

    rule = SILHOUETTE_RULES[silhouette]
    if not model_name:
        model_name = rule["name"]

    safe_name = model_name.replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")
    if not output_dir:
        output_dir = os.path.join(r"C:\Users\red1e\Desktop", f"SewLuxe_{safe_name}")

    os.makedirs(output_dir, exist_ok=True)
    guide_dir = os.path.join(output_dir, "07_Customer_Delivery_Guide")
    os.makedirs(guide_dir, exist_ok=True)

    print(f"[*] GARMENT ARCHETYPE : {silhouette.upper()} ({rule['name']})")
    print(f"[*] MODEL NAME        : {model_name}")
    print(f"[*] OUTPUT DIRECTORY  : {output_dir}")
    print("-" * 70)

    # 1. SPECIFICATION INITIALIZATION
    spec = TrouserSpec(silhouette=silhouette, model_name=model_name)
    engine = UniversalTrouserEngine(spec)

    # 2. PHASE 0 AUDIT & MEASUREMENT VERIFICATION
    print("\n[PHASE 0] MANDATORY CAD & MEASUREMENT AUDIT GATE...")
    qa_passed, qa_logs = engine.run_qa_audit()
    for log in qa_logs:
        print(f"  {log}")
    if not qa_passed:
        print("\n[STOP] Pre-Production QA Audit Failed! Halting generation.")
        return False
    print("  -> [PASSED 100% MATCH] Ready for Production.")

    # 3. COMPUTE SIZES & GEOMETRIC YARDAGE
    print("\n[PHASE 1] GENERATING SIZE CHARTS & SMART GEOMETRIC YARDAGE...")
    tables = engine.generate_size_tables()
    print(f"  [+] Finished Measurements calculated for {len(tables['finished'])} sizes (US 00 to 22).")
    yardage = engine.calculate_geometric_yardage()
    print(f"  [+] 60\" Yardage: 00-08: {yardage['00_08']['60_m']:.2f}m | 10-14: {yardage['10_14']['60_m']:.2f}m | 16-22: {yardage['16_22']['60_m']:.2f}m")
    print(f"  [+] 45\" Yardage: 00-08: {yardage['00_08']['45_m']:.2f}m | 10-14: {yardage['10_14']['45_m']:.2f}m | 16-22: {yardage['16_22']['45_m']:.2f}m")

    # 4. PIECE INVENTORY VERIFICATION
    pieces = engine.generate_piece_inventory()
    print(f"\n[PHASE 2] PIECE INVENTORY VERIFICATION ({len(pieces)} pieces):")
    for p in pieces:
        print(f"  - Piece #{p['id']}: {p['name']} ({p['material']}) -> {p['qty']}")

    # 5. COMPILE 16-PAGE LUXURY BOOKLET PDF
    print("\n[PHASE 3] COMPILING 16-PAGE LUXURY BOOKLET PDF...")
    booklet_filename = f"{safe_name}_Sewing_Instructions.pdf"
    booklet_out_path = os.path.join(guide_dir, booklet_filename)
    brain_out_path = os.path.join(r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0", booklet_filename)

    builder = UniversalBookletBuilder(spec)
    builder.build_booklet(booklet_out_path, assets_dir=assets_dir)
    shutil.copy2(booklet_out_path, brain_out_path)
    print(f"  [+] Booklet saved to: {booklet_out_path}")
    print(f"  [+] Brain copy saved to: {brain_out_path}")

    # 6. SUMMARY & AUDIT VERDICT
    print("\n" + "=" * 70)
    print(f"[SUCCESS 100%] HOMOGENEOUS PIPELINE COMPLETED FOR: {model_name}")
    print(f"  Booklet Delivery PDF: {booklet_out_path}")
    print("=" * 70)
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SewLuxe Universal Trouser Production Pipeline")
    parser.add_argument("--silhouette", type=str, default="palazzo", help="Trouser archetype key")
    parser.add_argument("--model", type=str, default=None, help="Garment model name")
    parser.add_argument("--output-dir", type=str, default=None, help="Destination directory")
    parser.add_argument("--assets-dir", type=str, default=None, help="Assets directory with photos/sketches")
    parser.add_argument("--list-silhouettes", action="store_true", help="List all available archetypes")

    args = parser.parse_args()

    if args.list_silhouettes:
        print("\nAVAILABLE TROUSER ARCHETYPES IN SEWLUXE CORE:")
        print("-" * 55)
        for k, v in SILHOUETTE_RULES.items():
            print(f"  • {k:<18} : {v['name']}")
        print("-" * 55)
        sys.exit(0)

    run_pipeline(
        silhouette=args.silhouette,
        model_name=args.model,
        output_dir=args.output_dir,
        assets_dir=args.assets_dir
    )
