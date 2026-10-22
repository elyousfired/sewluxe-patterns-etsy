import sys
import os

repo_root = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy"
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from sewluxe_core.universal_trouser_engine import TrouserSpec, UniversalTrouserEngine

def run_test():
    spec = TrouserSpec(
        model_name="Vivienne Tailored Wide-Leg Trousers",
        size_standard="PATTERNFAST_XXS_10XL",
        silhouette="wide_leg",
        rise_style="high_waist",
        front_shaping="flat_front",
        center_crease=True,
        back_shaping="2_darts",
        front_pockets="slant_italian",
        back_pockets="none",
        closure_type="exterior_button",
        belt_loops_count=5
    )

    engine = UniversalTrouserEngine(spec)
    passed, logs = engine.run_qa_audit()
    print("Audit Passed:", passed)
    for log in logs:
        print(" ", log)

    pieces = engine.generate_piece_inventory()
    print(f"\nPiece Inventory ({len(pieces)} pieces):")
    for p in pieces:
        print(f"  {p['id']}. {p['name']} ({p['material']}) - {p['qty']}")

    tables = engine.generate_size_tables()
    print(f"\nSizes generated: {len(tables['finished'])} sizes")
    print("Smallest (XXS):", tables['finished'][0])
    print("Largest (10XL):", tables['finished'][-1])

    yardage = engine.calculate_geometric_yardage()
    print("\nIntelligent Fabric Yardage:")
    for grp, y in yardage.items():
        print(f"  Group {grp}: 60in={y['60_m']}m ({y['60_yd']} yd) | 45in={y['45_m']}m ({y['45_yd']} yd)")

if __name__ == "__main__":
    run_test()
