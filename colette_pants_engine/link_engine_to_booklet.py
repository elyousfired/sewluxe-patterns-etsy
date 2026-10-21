"""
Link universal_trouser_engine directly into generate_colette_16page_booklet.py
"""

import re

path = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\colette_pants_engine\generate_colette_16page_booklet.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Add import at top
if "universal_trouser_engine" not in text:
    import_stmt = (
        "import sys\n"
        "sys.path.append(r'C:\\Users\\red1e\\.gemini\\antigravity\\scratch\\etsy\\sewluxe_core')\n"
        "from universal_trouser_engine import TrouserSpec, UniversalTrouserEngine, cm_to_tailor_inches\n"
    )
    text = text.replace("import pymupdf as fitz\n", "import pymupdf as fitz\n" + import_stmt)

engine_init = """    colette_spec = TrouserSpec(
        model_name="Colette Palazzo Trousers",
        size_standard="US_00_22",
        silhouette="palazzo",
        front_shaping="double_pleats",
        back_shaping="4_darts",
        front_pockets="slant_italian",
        back_pockets="none",
        closure_type="concealed_hook_bar",
        belt_loops_count=5
    )
    ute_engine = UniversalTrouserEngine(colette_spec)
    qa_ok, qa_logs = ute_engine.run_qa_audit()
    if not qa_ok:
        raise ValueError(f"Pre-Flight Trouser QA Audit Failed: {qa_logs}")
    ute_tables = ute_engine.generate_size_tables()
    fin_rows = [
        (r["size"], r["fin_waist"], r["fin_hips"], r["leg_sweep"], f"{r['inseam_outseam']} ({cm_to_tailor_inches(r['_raw'][3])} / {cm_to_tailor_inches(r['_raw'][4])})")
        for r in ute_tables["finished"]
    ]"""

text = re.sub(r'    fin_rows = \[\s*\("US 00".*?\n    \]', engine_init, text, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("[SUCCESS] Fully linked universal_trouser_engine dynamically into booklet script!")
