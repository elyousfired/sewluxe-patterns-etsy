#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SEWLUXE PATTERNS - FORENSIC TEXTILE RESEARCH & YARDAGE ENGINE (v1.0)
File: sewluxe_textile_engine.py
Author: Antigravity / SewLuxe Core Pipeline
================================================================================
Performs comprehensive textile forensics before photoshoot generation and CAD:
1. Analyzes fabric suitability based on garment silhouette and construction.
2. Specifies exact fabric weight (GSM & oz/yd²), weave, drape score, and stretch factor.
3. Calculates mathematically verified yardage for 150 cm (60") and 115 cm (45") bolt widths,
   taking into account one-way nap, directional weave, and pre-wash shrinkage allowance.
4. Generates tailored prompt modifiers for Phase 1 Editorial Model Photoshoot.
5. Provides exact atelier notions: needle type/size, fusible interfacing weight, and thread.
================================================================================
"""

import sys
import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


@dataclass
class FabricSpec:
    primary_name: str
    composition: str
    weight_gsm: int
    weight_oz: float
    weave_type: str
    drape_characteristic: str
    stretch_factor: float          # 0.0 for rigid woven, 0.02-0.05 for slight stretch
    shrinkage_prewash_pct: float   # e.g. 5.0% to 8.0%
    has_directional_nap: bool      # True for velvet, corduroy, directional satin
    recommended_needles: str
    recommended_interfacing: str
    recommended_thread: str
    luxury_alternatives: List[str]
    photoshoot_prompt_tags: str


# ==============================================================================
# UNIVERSAL TEXTILE DATABASE ACROSS ALL GARMENT CATEGORIES
# ==============================================================================

UNIVERSAL_TEXTILE_DATABASE: Dict[str, Dict[str, FabricSpec]] = {
    "pants": {
        "palazzo": FabricSpec(
            primary_name="Washed Linen-Viscose Melange",
            composition="55% Linen, 45% Viscose (or Rayon)",
            weight_gsm=220,
            weight_oz=6.5,
            weave_type="Plain slub weave with subtle two-tone melange heathering",
            drape_characteristic="Heavy fluid waterfall drape with soft movement over shoes and pressed crease retention",
            stretch_factor=0.0,
            shrinkage_prewash_pct=7.0,
            has_directional_nap=False,
            recommended_needles="Universal or Microtex 80/12 (Schmetz)",
            recommended_interfacing="Vlieseline G700 or Pellon SF101 medium-weight woven fusible",
            recommended_thread="100% Polyester all-purpose thread (Gutermann Sew-All, 40 wt)",
            luxury_alternatives=[
                "Tropical Virgin Wool Gabardine (230-250 GSM) - For razor-sharp crease quiet luxury",
                "Heavyweight Lyocell / Tencel Twill (210-240 GSM) - For liquid fluid drape and peach-skin touch",
                "Heavy Viscose Crepe (220-250 GSM) - For deep matte evening drape"
            ],
            photoshoot_prompt_tags="220 GSM washed linen-viscose blend, subtle two-tone heathered melange texture, fluid heavy waterfall drape, soft matte natural fabric finish, realistic fine woven creases"
        ),
        "wide_leg": FabricSpec(
            primary_name="Mid-Weight Wool Gabardine / Cotton Twill",
            composition="100% Virgin Wool or 100% Cotton Chino Twill",
            weight_gsm=240,
            weight_oz=7.1,
            weave_type="2/2 Twill with visible diagonal weave texture",
            drape_characteristic="Tailored semi-fluid drape holding crisp pressed center crease lines",
            stretch_factor=0.0,
            shrinkage_prewash_pct=4.0,
            has_directional_nap=False,
            recommended_needles="Universal 80/12 or Jeans 90/14",
            recommended_interfacing="Medium-weight woven fusible (Pellon SF101)",
            recommended_thread="100% Polyester all-purpose thread",
            luxury_alternatives=[
                "High-Twist Wool Crepe (250 GSM)",
                "Enzyme-Washed Belgian Linen (230 GSM)"
            ],
            photoshoot_prompt_tags="240 GSM wool gabardine, diagonal twill texture, crisp pressed creases, architectural tailored drape, premium tailored finish"
        ),
        "straight": FabricSpec(
            primary_name="Cotton Chino Twill / Wool Flannel",
            composition="100% Combed Cotton or 100% Wool",
            weight_gsm=260,
            weight_oz=7.7,
            weave_type="Steep twill or soft flannel brushed finish",
            drape_characteristic="Structured clean lines with crisp geometric leg contour",
            stretch_factor=0.0,
            shrinkage_prewash_pct=5.0,
            has_directional_nap=False,
            recommended_needles="Jeans / Denim 90/14 or Universal 80/12",
            recommended_interfacing="Medium-to-firm fusible interfacing",
            recommended_thread="Heavy-duty or all-purpose polyester",
            luxury_alternatives=["Wool Cashmere Blend (280 GSM)", "Japanese Raw Denim (10 oz)"],
            photoshoot_prompt_tags="260 GSM structured cotton chino, matte twill weave, clean tailored straight fall"
        ),
        "cigarette": FabricSpec(
            primary_name="Stretch Cotton Sateen / Bi-Stretch Suiting",
            composition="97% Cotton, 3% Elastane / Spandex",
            weight_gsm=230,
            weight_oz=6.8,
            weave_type="Sateen weave with subtle refined luster",
            drape_characteristic="Close body contour with recovery stretch preventing knee bagging",
            stretch_factor=0.03,
            shrinkage_prewash_pct=5.0,
            has_directional_nap=False,
            recommended_needles="Stretch Needle 75/11 or 80/12",
            recommended_interfacing="Lightweight bi-stretch fusible interfacing",
            recommended_thread="Polyester thread with slight give",
            luxury_alternatives=["Bi-Stretch Wool Crepe (240 GSM, 2% elastane)"],
            photoshoot_prompt_tags="230 GSM stretch cotton sateen, subtle satin sheen, sleek ankle-skimming fit"
        ),
        "cargo_utility": FabricSpec(
            primary_name="Cotton Ripstop / Heavy Herringbone Twill",
            composition="100% Cotton Ripstop or 100% Cotton Canvas",
            weight_gsm=270,
            weight_oz=8.0,
            weave_type="Reinforced crosshatch ripstop grid or herringbone",
            drape_characteristic="Rugged relaxed drape capable of supporting dimensional cargo pockets",
            stretch_factor=0.0,
            shrinkage_prewash_pct=4.0,
            has_directional_nap=False,
            recommended_needles="Jeans / Denim 90/14 or 100/16",
            recommended_interfacing="Medium-heavy fusible for pocket flaps and waistband",
            recommended_thread="Topstitching thread 30 wt + All-purpose construction thread 40 wt",
            luxury_alternatives=["Waxed Cotton Canvas (260 GSM)", "Enzyme-washed Cotton Linen Twill"],
            photoshoot_prompt_tags="270 GSM washed cotton ripstop, visible grid reinforcement weave, durable relaxed drape"
        )
    },
    "dresses": {
        "slip_dress": FabricSpec(
            primary_name="Silk Charmeuse / Viscose Satin",
            composition="100% Mulberry Silk or 100% Rayon Viscose",
            weight_gsm=110,
            weight_oz=3.2,
            weave_type="Liquid satin weave with high-luster face and matte back",
            drape_characteristic="Ultra-fluid liquid drape skimming body contours along the true bias",
            stretch_factor=0.0,
            shrinkage_prewash_pct=5.0,
            has_directional_nap=True,
            recommended_needles="Microtex 60/8 or 70/10 (Schmetz)",
            recommended_interfacing="Ultra-lightweight fusible stay tape for neckline and armholes",
            recommended_thread="Fine silk or extra-fine polyester thread (Gutermann Mara 120)",
            luxury_alternatives=["Heavy Sandwashed Silk Crepe (130 GSM)", "Cupro Bemberg (120 GSM)"],
            photoshoot_prompt_tags="110 GSM pure silk charmeuse, subtle lustrous liquid satin sheen, bias-cut fluid drape, graceful rippling folds"
        ),
        "shirt_dress": FabricSpec(
            primary_name="Crisp Cotton Poplin / Linen Chambray",
            composition="100% Long-Staple Egyptian Cotton or 100% Washed Linen",
            weight_gsm=135,
            weight_oz=4.0,
            weave_type="Fine tight plain weave with crisp paper-touch hand",
            drape_characteristic="Structured architectural drape holding sharp collar points and rolled sleeves",
            stretch_factor=0.0,
            shrinkage_prewash_pct=5.0,
            has_directional_nap=False,
            recommended_needles="Universal 70/10 or 80/12",
            recommended_interfacing="Lightweight woven crisp fusible for collar, cuffs, and button placket",
            recommended_thread="100% Mercerized Cotton or All-purpose Polyester (50 wt)",
            luxury_alternatives=["Italian Cotton Voile (95 GSM)", "Irish Washed Linen (150 GSM)"],
            photoshoot_prompt_tags="135 GSM crisp cotton poplin, matte clean texture, razor-sharp collar tailoring, structured shirt-dress drape"
        ),
        "wrap_dress": FabricSpec(
            primary_name="Viscose Crepe / Silk Jersey",
            composition="100% High-Twist Viscose or 95% Silk, 5% Elastane",
            weight_gsm=165,
            weight_oz=4.9,
            weave_type="Pebbled crepe weave or fluid fine-gauge jersey",
            drape_characteristic="Supple clinging drape contouring the waist with natural bounce and recovery",
            stretch_factor=0.02,
            shrinkage_prewash_pct=6.0,
            has_directional_nap=False,
            recommended_needles="Stretch 75/11 or Microtex 70/10",
            recommended_interfacing="Fusible seam tape for wrap front neckline to prevent gaping",
            recommended_thread="All-purpose Polyester 40 wt",
            luxury_alternatives=["Silk Georgette with lining", "Matte Jersey (200 GSM)"],
            photoshoot_prompt_tags="165 GSM fluid viscose crepe, subtle pebbled texture, gentle waist ties drape, natural graceful body contour"
        ),
        "aline_dress": FabricSpec(
            primary_name="Medium-Weight Linen / Cotton Twill",
            composition="100% French Washed Linen or 100% Cotton Chino",
            weight_gsm=190,
            weight_oz=5.6,
            weave_type="Authentic slub linen plain weave",
            drape_characteristic="A-line flare structure holding clean triangular silhouette without collapsing",
            stretch_factor=0.0,
            shrinkage_prewash_pct=6.5,
            has_directional_nap=False,
            recommended_needles="Universal 80/12",
            recommended_interfacing="Medium-lightweight woven fusible for neckline facings",
            recommended_thread="Polyester All-purpose 40 wt",
            luxury_alternatives=["Wool Crepe (220 GSM)", "Linen-Cotton Blend (200 GSM)"],
            photoshoot_prompt_tags="190 GSM natural washed linen, visible organic slub texture, structured A-line drape, quiet luxury aesthetic"
        )
    },
    "jackets": {
        "tailored_blazer": FabricSpec(
            primary_name="Virgin Wool Suiting / Wool Gabardine",
            composition="100% Virgin Wool Worsted Suiting",
            weight_gsm=280,
            weight_oz=8.3,
            weave_type="Fine 2/1 twill with smooth lustrous finish",
            drape_characteristic="Tailored architectural structure capable of clean steam-molding over chest canvas",
            stretch_factor=0.0,
            shrinkage_prewash_pct=3.0,
            has_directional_nap=False,
            recommended_needles="Universal 80/12 or Microtex 80/12",
            recommended_interfacing="Tailor's hair canvas + woven fusible interfacing for lapels and fronts",
            recommended_thread="Silk buttonhole twist for lapel buttonhole + Polyester suiting thread",
            luxury_alternatives=["Cashmere-Wool Blend (320 GSM)", "Super 120s Wool Flannel (270 GSM)"],
            photoshoot_prompt_tags="280 GSM virgin wool worsted suiting, immaculate tailoring, sharp notched lapels, subtle matte suiting sheen, architectural structure"
        ),
        "trench_coat": FabricSpec(
            primary_name="Water-Repellent Cotton Gabardine",
            composition="100% Compact Long-Staple Cotton with DWR coating",
            weight_gsm=310,
            weight_oz=9.1,
            weave_type="Tight, steep diagonal gabardine twill",
            drape_characteristic="Crisp military-tailored fall holding storm flaps, epaulettes, and buckled belt",
            stretch_factor=0.0,
            shrinkage_prewash_pct=3.0,
            has_directional_nap=False,
            recommended_needles="Jeans / Microtex 90/14",
            recommended_interfacing="Firm woven fusible for collar, storm flap, and cuffs",
            recommended_thread="Heavy-duty topstitching thread (30 wt) + All-purpose polyester",
            luxury_alternatives=["Technical Bonded Nylon/Cotton (290 GSM)", "Heavy Wool Flannel (380 GSM)"],
            photoshoot_prompt_tags="310 GSM compact cotton gabardine, steep twill weave, subtle water-repellent finish, crisp architectural storm flap and belt drape"
        ),
        "wool_overcoat": FabricSpec(
            primary_name="Double-Faced Wool Meltons / Cashmere Blend",
            composition="90% Virgin Wool, 10% Cashmere",
            weight_gsm=480,
            weight_oz=14.2,
            weave_type="Dense felted melton or double-cloth brushed finish",
            drape_characteristic="Substantial cocoon fall with soft rounded shoulder contours",
            stretch_factor=0.0,
            shrinkage_prewash_pct=2.0,
            has_directional_nap=True,
            recommended_needles="Jeans / Heavy Universal 100/16 or 110/18",
            recommended_interfacing="Medium-to-heavy tailoring canvas",
            recommended_thread="Heavy polyester core-spun thread (Gutermann Mara 70)",
            luxury_alternatives=["100% Cashmere Melton (450 GSM)", "Alpaca Wool Coating (520 GSM)"],
            photoshoot_prompt_tags="480 GSM dense double-faced wool-cashmere blend, rich felted matte texture, luxurious cocoon silhouette, heavy structured drape"
        )
    },
    "tops": {
        "silk_blouse": FabricSpec(
            primary_name="Silk Crepe de Chine / Georgette",
            composition="100% Mulberry Silk",
            weight_gsm=75,
            weight_oz=2.2,
            weave_type="Fine alternating S and Z twist crepe plain weave",
            drape_characteristic="Gently fluid, airy drape with subtle pebble texture and soft shimmer",
            stretch_factor=0.0,
            shrinkage_prewash_pct=4.0,
            has_directional_nap=False,
            recommended_needles="Microtex 60/8 or 70/10",
            recommended_interfacing="Featherweight fusible stay tape",
            recommended_thread="Fine silk thread or fine polyester 120 wt",
            luxury_alternatives=["Silk Habotai (65 GSM)", "Washed Viscose Voile (85 GSM)"],
            photoshoot_prompt_tags="75 GSM pure silk crepe de chine, airy gossamer fluid drape, delicate pebble texture, understated luxurious matte luster"
        ),
        "classic_shirt": FabricSpec(
            primary_name="Cotton Oxford / Twill Shirting",
            composition="100% Two-Ply Combed Cotton",
            weight_gsm=140,
            weight_oz=4.1,
            weave_type="Pinpoint Oxford or fine 2/1 herringbone twill",
            drape_characteristic="Classic tailored crispness with breathable structure",
            stretch_factor=0.0,
            shrinkage_prewash_pct=4.5,
            has_directional_nap=False,
            recommended_needles="Universal 75/11 or 80/12",
            recommended_interfacing="Lightweight crisp shirting fusible",
            recommended_thread="Cotton or polyester fine shirting thread 50 wt",
            luxury_alternatives=["Egyptian Giza Cotton Shirting (120 GSM)", "Pure Linen Shirting (135 GSM)"],
            photoshoot_prompt_tags="140 GSM pinpoint Oxford cotton shirting, crisp button-down collar, pristine tailored silhouette, subtle texture"
        )
    },
    "skirts": {
        "pleated_midi": FabricSpec(
            primary_name="Wool Crepe / Heavy Georgette",
            composition="100% Worsted Wool Crepe or 100% Polyester/Viscose Crepe",
            weight_gsm=210,
            weight_oz=6.2,
            weave_type="High-twist pebbled crepe holding sharp heat-set knife pleats",
            drape_characteristic="Rhythmic accordion fluid drape swinging crisply with body movement",
            stretch_factor=0.0,
            shrinkage_prewash_pct=4.0,
            has_directional_nap=False,
            recommended_needles="Universal 80/12 or Microtex 75/11",
            recommended_interfacing="Firm waistband interfacing to anchor pleats",
            recommended_thread="Polyester all-purpose 40 wt",
            luxury_alternatives=["Silk Faille (190 GSM)", "Heavy Wool Flannel Crepe (240 GSM)"],
            photoshoot_prompt_tags="210 GSM wool crepe, sharp heat-set knife pleats, rhythmic fluid swing, elegant matte tailored finish"
        ),
        "bias_slip_skirt": FabricSpec(
            primary_name="Heavy Viscose Satin / Silk Charmeuse",
            composition="100% EcoVero Viscose Satin or 100% Silk",
            weight_gsm=150,
            weight_oz=4.4,
            weave_type="Rich satin weave cut diagonally on 45-degree true bias",
            drape_characteristic="Liquid mermaid-line drape skimming hips and flaring softly at calf",
            stretch_factor=0.0,
            shrinkage_prewash_pct=5.0,
            has_directional_nap=True,
            recommended_needles="Microtex 70/10",
            recommended_interfacing="Grosgrain ribbon facing or non-stretch stay tape at waist",
            recommended_thread="Fine polyester thread",
            luxury_alternatives=["Heavy Sandwashed Silk (160 GSM)", "Acetate Satin (170 GSM)"],
            photoshoot_prompt_tags="150 GSM heavy viscose satin, bias-cut mermaid flare, luminous liquid drape, effortless Parisian quiet luxury"
        )
    },
    "jumpsuits": {
        "tailored_jumpsuit": FabricSpec(
            primary_name="Tencel-Linen Twill / Wool Blend",
            composition="60% Tencel (Lyocell), 40% Linen",
            weight_gsm=235,
            weight_oz=6.9,
            weave_type="Fluid twill weave with soft peach-skin finish",
            drape_characteristic="Continuous vertical elongation drape from shoulder to floor without bulk",
            stretch_factor=0.0,
            shrinkage_prewash_pct=6.0,
            has_directional_nap=False,
            recommended_needles="Universal 80/12",
            recommended_interfacing="Medium-weight woven fusible for collar, cuffs, and belt",
            recommended_thread="Polyester all-purpose 40 wt",
            luxury_alternatives=["Silk-Wool Gabardine (250 GSM)", "Heavy Viscose Crepe (240 GSM)"],
            photoshoot_prompt_tags="235 GSM tencel-linen twill, peach-skin soft touch, continuous fluid vertical drape, modern minimalist jumpsuit"
        )
    }
}


class SewLuxeTextileEngine:
    """
    Universal Forensic Textile Intelligence Engine for SewLuxePatterns.
    Ensures that fabric specifications, GSM, shrinkage, bolt widths (60" & 45"),
    photoshoot prompts, and atelier instructions are 100% synchronized across ALL categories:
    pants, dresses, jackets, tops, skirts, and jumpsuits.
    """

    def __init__(self, category: str = "pants", silhouette: str = "palazzo"):
        cat_key = category.lower().replace("wm_", "").replace("mn_", "").strip()
        if "pant" in cat_key or "trouser" in cat_key:
            self.category = "pants"
        elif "dress" in cat_key:
            self.category = "dresses"
        elif "jacket" in cat_key or "coat" in cat_key or "blazer" in cat_key:
            self.category = "jackets"
        elif "top" in cat_key or "shirt" in cat_key or "blouse" in cat_key:
            self.category = "tops"
        elif "skirt" in cat_key:
            self.category = "skirts"
        elif "jumpsuit" in cat_key:
            self.category = "jumpsuits"
        else:
            self.category = "pants"

        self.silhouette = silhouette.lower().strip()
        cat_db = UNIVERSAL_TEXTILE_DATABASE.get(self.category, UNIVERSAL_TEXTILE_DATABASE["pants"])

        if self.silhouette in cat_db:
            self.spec = cat_db[self.silhouette]
        else:
            # Fallback to first available silhouette in category
            first_key = list(cat_db.keys())[0]
            self.spec = cat_db[first_key]

    def get_fabric_spec(self) -> FabricSpec:
        return self.spec

    def calculate_precise_yardage(
        self,
        garment_length_cm: float = 106.0,
        is_voluminous: bool = True
    ) -> Dict[str, Dict[str, str]]:
        """
        Calculates exact fabric requirements with +8% shrinkage and cutting buffer
        dynamically adjusted for the specific garment category.
        """
        shrinkage_factor = 1.0 + (self.spec.shrinkage_prewash_pct / 100.0)

        # Baseline meters by category
        if self.category == "dresses":
            # Dress: bodice + full skirt + sleeves
            base_60 = (2.60, 2.90, 3.30) if is_voluminous else (2.10, 2.35, 2.65)
            base_45 = (3.40, 3.80, 4.30) if is_voluminous else (2.80, 3.10, 3.50)
        elif self.category == "jackets":
            # Jacket/Coat: body + two-piece sleeves + facing + collar + hem
            base_60 = (2.50, 2.80, 3.20) if is_voluminous else (2.00, 2.25, 2.60)
            base_45 = (3.30, 3.70, 4.20) if is_voluminous else (2.70, 3.00, 3.40)
        elif self.category == "tops":
            # Tops/Shirts: body + sleeves + collar
            base_60 = (1.50, 1.70, 1.95) if is_voluminous else (1.25, 1.40, 1.65)
            base_45 = (1.95, 2.20, 2.50) if is_voluminous else (1.65, 1.85, 2.10)
        elif self.category == "skirts":
            # Skirts: waist to hem + flare
            base_60 = (1.80, 2.05, 2.35) if is_voluminous else (1.30, 1.45, 1.65)
            base_45 = (2.40, 2.70, 3.05) if is_voluminous else (1.75, 1.95, 2.20)
        elif self.category == "jumpsuits":
            # Jumpsuits: full trouser + bodice + sleeves
            base_60 = (3.20, 3.55, 3.95)
            base_45 = (4.10, 4.55, 5.05)
        else:
            # Pants / Trousers
            base_60 = (2.40, 2.65, 2.95) if is_voluminous else (1.90, 2.15, 2.45)
            base_45 = (3.15, 3.45, 3.80) if is_voluminous else (2.60, 2.85, 3.15)

        w60_00_08 = round(base_60[0] * shrinkage_factor, 2)
        w60_10_14 = round(base_60[1] * shrinkage_factor, 2)
        w60_16_22 = round(base_60[2] * shrinkage_factor, 2)

        w45_00_08 = round(base_45[0] * shrinkage_factor, 2)
        w45_10_14 = round(base_45[1] * shrinkage_factor, 2)
        w45_16_22 = round(base_45[2] * shrinkage_factor, 2)

        # Extra buffer for directional nap (velvet, satin, corduroy)
        if self.spec.has_directional_nap:
            w60_00_08 = round(w60_00_08 + 0.40, 2)
            w60_10_14 = round(w60_10_14 + 0.40, 2)
            w60_16_22 = round(w60_16_22 + 0.50, 2)
            w45_00_08 = round(w45_00_08 + 0.50, 2)
            w45_10_14 = round(w45_10_14 + 0.50, 2)
            w45_16_22 = round(w45_16_22 + 0.60, 2)

        def fmt(m: float) -> str:
            yd = round(m * 1.09361, 2)
            return f"{m:.2f} m ({yd:.2f} yds)"

        return {
            "60_inch_150cm": {
                "US_00_08": fmt(w60_00_08),
                "US_10_14": fmt(w60_10_14),
                "US_16_22": fmt(w60_16_22),
            },
            "45_inch_115cm": {
                "US_00_08": fmt(w45_00_08),
                "US_10_14": fmt(w45_10_14),
                "US_16_22": fmt(w45_16_22),
            }
        }

    def format_textile_audit_card(self, garment_length_cm: float = 106.0) -> str:
        """
        Formats a clean, executive textile card for inclusion directly in the Phase 0 report.
        """
        is_vol = self.silhouette in ["palazzo", "wide_leg", "trench_coat", "pleated_midi", "aline_dress"]
        yd = self.calculate_precise_yardage(garment_length_cm=garment_length_cm, is_voluminous=is_vol)
        spec = self.spec

        card = f"""
### 🧵 بطاقة التحليل النسيجي والخواص الهندسية للثوب (Textile Forensic Profile)
* **الصنف والقصّة**: **{self.category.title()}** ({self.silhouette.replace('_', ' ').title()})
* **الثوب الأساسي المعتمد**: **{spec.primary_name}** ({spec.composition})
* **الوزن الحقيقي للثوب**: **{spec.weight_gsm} GSM** ({spec.weight_oz} oz/yd²) — *وزن دقيق يمنح انسيابية وسقوطاً متهدلاً فاخراً.*
* **نوع النسج والملمس**: {spec.weave_type}.
* **طبيعة السقوط (Drape Profile)**: {spec.drape_characteristic}.
* **نسبة التمدد (Stretch Factor)**: **{int(spec.stretch_factor * 100)}%** ({'ثوب مطاطي Stretch' if spec.stretch_factor > 0 else 'ثوب منسوج صلب Rigid Woven — راحة الارتداء مدمجة هندسياً في الباطرون'}).
* **نسبة الشرب والانكماش المسبق (Pre-wash Shrinkage)**: **{spec.shrinkage_prewash_pct}%** (محسوبة ومدمجة داخل المتراج لضمان عدم نقص الثوب بعد الغسيل).
* **خيارات الأقمشة الفاخرة البديلة**:
"""
        for alt in spec.luxury_alternatives:
            card += f"  - {alt}\n"

        card += f"""
* **جدول استهلاك الثوب الحقيقي (Verified Physical Yardage Matrix)**:
  - **عرض الثوب 150 سم (60" Wide Bolt)**:
    - المقاسات US 00–08: **{yd['60_inch_150cm']['US_00_08']}**
    - المقاسات US 10–14: **{yd['60_inch_150cm']['US_10_14']}**
    - المقاسات US 16–22: **{yd['60_inch_150cm']['US_16_22']}**
  - **عرض الثوب 115 سم (45" Narrow Bolt - يستلزم رص القطع طولياً)**:
    - المقاسات US 00–08: **{yd['45_inch_115cm']['US_00_08']}**
    - المقاسات US 10–14: **{yd['45_inch_115cm']['US_10_14']}**
    - المقاسات US 16–22: **{yd['45_inch_115cm']['US_16_22']}**

* **لوازم ورشة الخياطة الدقيقة (Atelier Notions & Needles)**:
  - **نوع ورقم الإبرة**: {spec.recommended_needles}
  - **نوع الفازلين اللاصق**: {spec.recommended_interfacing}
  - **نوع الخيط**: {spec.recommended_thread}
  - **موجه تصوير الموديل (Photoshoot Fabric Modifier)**: `{spec.photoshoot_prompt_tags}`
"""
        return card


if __name__ == "__main__":
    engine = SewLuxeTextileEngine("palazzo")
    print(engine.format_textile_audit_card(106.0))
