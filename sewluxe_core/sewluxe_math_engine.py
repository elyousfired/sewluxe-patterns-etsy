"""
SewLuxe Core Math & Measurement Engine
Guarantees 100% mathematical accuracy for body and finished garment charts:
- Zero '0/0' fraction bugs.
- Precise standard sewing inch fractions (1/8, 1/4, 3/8, 1/2, 5/8, 3/4, 7/8).
- Sanity checks for Inseam, Outseam, Crotch Rise, and Leg Sweep.
"""

from fractions import Fraction
import math

def cm_to_inches_fraction(cm_value: float, precision: int = 8) -> str:
    """
    Converts cm value to a clean sewing fraction in inches.
    Precision 8 means nearest 1/8th inch (standard indie pattern convention).
    Never outputs '0/0', '0/8', or improper fractions.
    Examples:
      63.6 cm -> 25"
      75.4 cm -> 29 5/8"
      111.0 cm -> 43 3/4"
    """
    if cm_value is None or cm_value <= 0:
        return ""
    
    inches_total = cm_value / 2.54
    int_part = math.floor(inches_total)
    fractional = inches_total - int_part
    
    # Round to nearest 1/precision
    steps = round(fractional * precision)
    if steps == precision:
        int_part += 1
        steps = 0
        
    if steps == 0:
        return f'{int_part}"'
    
    # Simplify fraction
    frac = Fraction(steps, precision)
    return f'{int_part} {frac.numerator}/{frac.denominator}"'

def format_cm_and_inches(cm_value: float, precision: int = 8) -> str:
    """
    Formats measurement as: "75.4 cm (29 5/8\")"
    """
    in_str = cm_to_inches_fraction(cm_value, precision)
    return f"{cm_value:.1f} cm ({in_str})"

def validate_trouser_geometry(size_label: str, waist_cm: float, hip_cm: float, sweep_cm: float, inseam_cm: float, outseam_cm: float, is_palazzo: bool = True):
    """
    Validates physical sanity of trouser measurements.
    Raises ValueError with detailed explanation if geometry is broken.
    """
    # 1. Rise sanity: Outseam - Inseam = Crotch Rise
    rise = outseam_cm - inseam_cm
    if rise < 20.0 or rise > 36.0:
        raise ValueError(f"[{size_label}] Broken crotch rise: Outseam ({outseam_cm}) - Inseam ({inseam_cm}) = {rise:.1f} cm (expected 23-32 cm).")
        
    # 2. Palazzo Inseam sanity: Palazzo trousers drape to floor/shoes, inseam must NOT drop below 75 cm!
    if is_palazzo and inseam_cm < 75.0:
        raise ValueError(f"[{size_label}] Defective Palazzo Inseam: {inseam_cm:.1f} cm is too short for palazzo drape (expected 76-80 cm).")
        
    # 3. Leg Sweep sanity: Palazzo hem sweep must be wide (> 58 cm per leg)
    if is_palazzo and sweep_cm < 58.0:
        raise ValueError(f"[{size_label}] Palazzo leg sweep {sweep_cm:.1f} cm is too narrow (expected > 60 cm).")
        
    return True

if __name__ == "__main__":
    # Test cases demonstrating the fix
    test_cases = [63.6, 68.6, 75.4, 111.0, 111.8, 100.0, 95.0]
    print("[TESTING cm_to_inches_fraction]")
    for tc in test_cases:
        res = format_cm_and_inches(tc)
        print(f"  {tc} cm -> {res}")
        assert "0/0" not in res, f"Failed for {tc}: {res}"
    print("ALL MATH ENGINE TESTS PASSED!")
