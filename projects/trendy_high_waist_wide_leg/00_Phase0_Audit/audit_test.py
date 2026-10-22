import sys
import os

sys.path.insert(0, r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\sewluxe_core")
from universal_trouser_engine import UniversalTrouserEngine, TrouserSpec

spec = TrouserSpec(
    model_name="Trendy High-Waisted Wide-Leg Pants",
    size_standard="PATTERNFAST_XXS_10XL",
    silhouette="wide_leg",
    rise_style="high_waist",
    front_shaping="front_darts",
    center_crease=True,
    back_shaping="2_darts",
    front_pockets="none",
    back_pockets="none",
    closure_type="side_invisible_zip",
    belt_loops_count=0
)

engine = UniversalTrouserEngine(spec)
passed, logs = engine.run_qa_audit()
print("QA STATUS:", "PASSED" if passed else "FAILED")
for l in logs:
    print(" ", l)

print("\nPIECE INVENTORY:")
pieces = engine.generate_piece_inventory()
for p in pieces:
    print(f"  Piece #{p['id']}: {p['name']} | Material: {p['material']} | Qty: {p['qty']}")

print("\nYARDAGE:")
yard = engine.calculate_geometric_yardage()
for k, v in yard.items():
    print(f"  {k}: {v}")

print("\nSEWING STEPS GENERATED:")
steps = engine.generate_sewing_steps()
for s in steps:
    print(f"  Step {s['step']}: {s['title']}")
    for b in s['bullets']:
        print(f"    - {b}")
