---
name: "etsy-pattern-hunter"
description: "Research high-demand, low-competition sewing pattern niches on Etsy that can be built with PatternFast/Tailornova, analyze seasonal timing and competitor gaps, and output an actionable Production Brief."
---

# Etsy Pattern Niche & Trend Hunter

Goal: Never waste hours building a pattern that has zero search demand or impossible competition, and never pick a design that `PatternFast` / `Tailornova` cannot draft cleanly. Find winning garment opportunities BEFORE production begins.

## When to Use
- When the user asks: *"What pattern should we make next?"*, *"Find me a good women's or kids' pattern niche for this month"*, or *"Is a <garment> pattern worth making on Etsy?"*

## Mandatory Anti-Block Etsy Visual & CDN Scraper (`etsy_stealth_browser.py`)
- **NEVER hit `etsy.com/search` directly with headless Playwright** (Etsy's DataDome firewall immediately serves `Access is temporarily restricted` or `Verification Required`).
- **ALWAYS use Direct AJAX or Visual Indexing**:
  1. For direct listings: Query `https://www.etsy.com/api/v3/ajax/public/listings/{id}` with standard browser headers (Zero DataDome blocks, 100% exact JSON data, and full-resolution images).
  2. For visual search: Query indexed Etsy listings via `https://www.bing.com/images/search?q=etsy+<keyword>+sewing+pattern+pdf` to extract authentic `i.etsystatic.com` CDN URLs in under 3 seconds.
  4. **MANDATORY**: Always inspect the captured PNG/JPG files with `read_file` to verify the images are real Etsy listings before showing them to the user!

---

## Step 1: Check Seasonality (6–8 Weeks Lead Time)
Sewists buy patterns and fabric **6 to 8 weeks before** the season they want to wear them:
- **Jan – Feb**: Spring transitional jackets (trench, quilted vest, boucle cropped jacket), linen blouses, Easter girls' dresses (`bishop sleeve`, `peter pan collar`, `pinafore`).
- **Mar – May**: Summer dresses (`milkmaid`, `tiered maxi`, `wrap dress`, `square neck sundress`), linen wide-leg pants, shorts sets, kids' summer rompers/sets.
- **Jun – Aug**: Back-to-school kids' sets (`sweatshirt + joggers`, `shirt + shorts`, `corduroy overalls`), early fall layering vests, button-up shirts.
- **Sep – Nov**: Peak Q4 season! Winter coats (`mandarin collar coat`, `peplum wool jacket`), fleece/sherpa zip hoodies, **Kids & Adult Holiday Pajama Sets**, sleep sacks, gifts for sewists (`sewing planners`, `project bags`).
- **Dec**: Cozy loungewear, turtleneck tops, wardrobe planners, New Year organization printables.

---

## Step 2: Filter by Generator Feasibility (PatternFast / Tailornova Compatibility)
Only recommend designs that the pattern generator handles reliably (or with simple rectangular/traced additions in `sewluxe-booklet` / `sewluxe-kids-booklet`):
- **HIGH FEASIBILITY (Green Light)**:
  - Women's tailored & boxy jackets, peplum jackets, vests, coats (collarless, mandarin stand, flat rounded collar, convertible collar; button front or exposed zip; bust/waist darts or princess seams; patch or welt pockets).
  - Women's blouses, button-up shirts, turtleneck tops, A-line / tiered dresses, skirts, wide-leg or elastic-waist trousers.
  - Kids' 2-piece sets (Top + Pants, Pajama sets, Sweatshirt + Joggers, Shirt + Shorts) and girls' dresses (trapeze, ruffle hem, square neck, bishop sleeves).
- **LOW FEASIBILITY (Avoid)**:
  - Complex origami drapery, bias-cut cowl necks with asymmetrical twists, underwire lingerie/corsetry with boning channels, multi-piece tailored men's suit jackets with pad-stitching, or complex backpack hardware patterns.

---

## Step 3: Data-Driven Keyword & Competitor Gap Analysis
1. Check the **Keyword Bank** in [`seo-listing-etsy/SKILL.md`](../seo-listing-etsy/SKILL.md) first for proven high-conversion phrases and ratios (`Ratio = Searches / Results × 1000`).
2. Run targeted web searches across Etsy, Pinterest, and sewing trend blogs for candidate garments:
   - Look for **Garment-Type Arbitrage** (e.g., when a style keyword like `mandarin collar` or `quilted` or `bishop sleeve` has strong buyer searches, few dedicated pattern listings under 5,000 results, and "typical / high / very high" conversion).
   - Check top Etsy competitors (e.g. `RusticCottageStiches`, `DearBillyPatterns`, indie pattern bestsellers): inspect their review velocity (new reviews in the last 30 days), price point (`$4.50–$9.50` after discount), and what buyers complain about in 3-star reviews (e.g. *"No A0 file"*, *"No layered PDF"*, *"Confusing collar instructions"*, *"Neckline too tight for my toddler's head"* — all things our pipeline solves!).

---

## Step 4: Output the Actionable Production Brief
Deliver a structured **Next Pattern Production Brief** containing:
1. **Recommended Garment & House Name** (e.g., *Colette Quilted Jacket* or *Oliver Pajama Set*).
2. **Why It Wins (Data & Gap)**: Search demand, competition level, seasonal timing, and specific edge over existing Etsy listings (e.g. adding `Multi-Size Layered PDF + Projector File + Video Guides`).
3. **Exact Generator Recipe (How to export it in PatternFast/Tailornova)**:
   - Category & Base Block
   - Neckline & Collar setting
   - Sleeve style & cuff setting
   - Closure type & Pocket style
   - Any extra piece our booklet script will auto-add (e.g. traced facing, bias strip, or rectangle collar).
4. **Seed Keywords to Test** in Etsy Marketplace Insights (5–8 high-priority keywords).
5. **Recommended Fabric & Editorial Color Direction** (checked against the `Previous listings` table in `prompt-photo-listing` so it stands out in the shop grid).
