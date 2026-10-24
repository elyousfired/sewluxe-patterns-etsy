---
name: "etsy-bundle-builder"
description: "Combine 2 to 5 existing sewing patterns into high-converting Etsy Bundle listings (3-in-1 packs, Capsule Wardrobes, Mommy & Me sets) with bundle cover graphics, comparison slides, master download hub PDF, bundle SEO, and cross-sell booklet pages."
---

# Etsy Pattern Bundle & Cross-Sell Builder

Goal: Multiply shop listings, Average Order Value (AOV), and total revenue on Etsy without drafting new patterns by packaging existing single patterns into curated **Bundles** (`3-in-1 Jacket Bundle`, `Kids Loungewear Bundle`, `Capsule Wardrobe Pack`) and embedding **Cross-Sell Promo Pages** inside individual booklets.

---

## Why Bundles Crush on Etsy
1. **New Search Real Estate**: A bundle targets high-intent keywords (`sewing pattern bundle`, `jacket pattern pack`, `kids sewing bundle`, `capsule wardrobe sewing pattern`) without competing against your single listings.
2. **Higher AOV & Profit Margin**: Etsy charges a fixed `$0.20` listing fee + fixed payment processing flat fee per transaction. Selling a 3-pattern bundle at `2.2x` the single pattern price more than doubles net profit per buyer.
3. **Perceived Value**: Buyers love seeing `"3 Patterns Included · 39 Sizes · Save 35%"` on the cover thumbnail.

---

## Deliverable 1: Curated Bundle Combinations
When the user has 3+ patterns in the shop, group them by theme:
- **Silhouette / Garment Family**: e.g. *The Classic Jacket Trio* (`Florence Collarless Jacket` + `Elsie Peplum Jacket` + `Audrey Zip Jacket`).
- **Seasonal Capsule**: e.g. *Autumn Layering Bundle* (`Clara Quilted Vest` + `Nora Turtleneck Top` + `Wide-Leg Trousers`).
- **Kids Mega-Pack**: e.g. *Boys Everyday Set Bundle* (`Milo Sweatshirt & Joggers` + `Leo Zip Hoodie & Joggers` + `Oscar Shirt & Shorts`).
- **Mommy & Me Matching Bundle**: Women's pattern + matching Girls'/Kids' pattern.

---

## Deliverable 2: 10 Bundle Listing Slides (`2000 × 2000 px` via Playwright)
1. **Slide 1 (Bundle Hero Cover)**:
   - Top Banner: `3-IN-1 SEWING PATTERN BUNDLE · SAVE 35%` (`Poppins Bold`, accent `#9C4A57` bar).
   - 3 Model Photos side-by-side in arched or clean framed cards, each with its garment name (`Florence · Elsie · Audrey`) and small white Technical Flat Sketch sticker at the bottom corner.
   - Bottom Feature Bar: `SIZES US 00–22 (XXS–4XL) · A4 · US LETTER · A0 · PROJECTOR · ILLUSTRATED GUIDES + VIDEOS`.
2. **Slides 2, 3, 4 (Individual Pattern Spotlights)**:
   - One slide per included pattern showing its Front + Back model photo, technical flat sketch, skill level, and key design features.
3. **Slide 5 (Side-by-Side Comparison & Styling Matrix)**:
   - Clean comparison table showing all 3 garments: Closure type, Collar style, Skill level, Best fabrics, and Sewing time.
4. **Slide 6 (Master Size Chart)**:
   - Unified Body Measurements (`US 00–22 / XXS–4XL` or `Kids 2–16`) + Finished Garment Measurements for all 3 garments.
5. **Slide 7 (Fabric Requirements for All 3 Patterns)**:
   - Compact yardage/meterage table so buyers can shop for fabric for the whole bundle at once.
6. **Slide 8 (What You Receive in the Bundle)**:
   - Visual showcase of all 3 Instruction Booklets + Pattern Packs + Video Guides.
7. **Slide 9 (Inside the Instruction Booklets)**.
8. **Slide 10 (How Instant Download Works)**.

---

## Deliverable 3: Master Bundle Download Hub PDF
Build `<Bundle-Name>_Master-Download-Hub.pdf` (`ReportLab`, 1–2 pages):
- Organized sections for **Pattern 1**, **Pattern 2**, and **Pattern 3**.
- Each section has its own thumbnail, flat sketch, and clickable buttons for `Instruction Booklet PDF`, `A4 Pack`, `US Letter Pack`, `A0 Copyshop`, and `Projector File`.

---

## Deliverable 4: Bundle Etsy SEO (Title, 13 Tags, Description)
Follow all rules in [`seo-listing-etsy/SKILL.md`](../seo-listing-etsy/SKILL.md), adapted for bundles:
- **Title (<15 words)**: Lead with the strongest bundle noun phrase (e.g., `Jacket Sewing Pattern Bundle for Women, 3 Classic & Peplum Coat Patterns 00-22 PDF`).
- **13 Tags**: Mix high-traffic individual garment tags with bundle-specific tags (`pattern bundle`, `sewing pattern pack`, `3 in 1 pattern`, `wardrobe patterns`, `gift for sewist`).
- **Description**: Include a clear breakdown of each garment in `✨ INCLUDED PATTERNS (3 FULL PATTERNS)` before the standard sections.

---

## Deliverable 5: Cross-Sell Page for Single Booklets
Generate a reusable last-page insert or footer block for `sewluxe-booklet` and `sewluxe-kids-booklet`:
- **"Complete Your Handmade Wardrobe"**: Shows 3 related patterns from the shop (thumbnail + sketch + name) + a `VIP THANK YOU` discount code box (`Use code SEWLUXE20 for 20% off your next pattern or bundle in our Etsy shop!`).
