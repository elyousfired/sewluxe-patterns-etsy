import os
import sys

sys.path.append(r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\02_pattern_engine")
from pattern_engine import PatternFastEngine

engine = PatternFastEngine()
print("Logging in...")
token = engine.login()
print("Logged in successfully! Token starts with:", token[:20])

mannequins = engine.get_standard_mannequins()
names = [m["name"] for m in mannequins]
print(f"Retrieved {len(mannequins)} standard mannequins: {names}")

# Test single size pattern generation
man_4 = next(m for m in mannequins if m["name"] == "4")
out_pdf = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\02_pattern_engine\test_output\SewLuxe_Size_US_4_A4.pdf"
print("Generating White-Labeled Pattern PDF for Size US 4 (A4)...")
res_path = engine.generate_single_size_pattern(
    elem_ids="79287,30165,28352",
    mannequin_id=man_4["mannequinId"],
    size_name="4",
    page_size="A4",
    out_pdf_path=out_pdf
)

print("Generated PDF:", res_path, "Size:", os.path.getsize(res_path), "bytes")
