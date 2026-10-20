# SewLuxe Patterns — Etsy Sewing Intelligence & Automation Engine 🧵✨

An automated intelligence system and end-to-end production pipeline for digital sewing patterns on Etsy, following the Argon Benchmark standards.

---

## 🚀 Key Features

### 1. Market Research & 1:1 Bestseller Intelligence
- **Exact Category Matching**: Pre-configured with the 8 core Tailornova & PatternFast categories (`Jackets`, `Dresses`, `Tops`, `Jumpsuits`, `Pants`, `Skirts`, `Sweatshirts`, `T-Shirts`).
- **Direct Etsy URL Analyzer (1:1 Exact Match)**: Paste any Etsy listing URL to pull authentic product data directly from Etsy's official servers:
  - Exact listing title, tags, and shop name
  - High-resolution hero image (cached locally for offline stability)
  - Full photo gallery thumbnails
  - Accurate pricing and description snippets
- **One-Click Model Selection**: Select any bestseller or direct listing to lock it for production (`selected_pattern.json`).

### 2. Live Interactive Dashboard
- Modern, clean luxury interface (`#FAF8F5`, `#1C1B1A`, Poppins & Serif typography).
- Instant AJAX scanning and cached responses for ultra-fast browsing.

---

## 🛠️ Quick Start

```bash
# Clone the repository
git clone https://github.com/elyousfired/sewluxe-patterns-etsy.git
cd sewluxe-patterns-etsy

# Install dependencies
pip install fastapi uvicorn playwright

# Launch the Dashboard
python -m uvicorn 01_market_research.dashboard.server:app --host 127.0.0.1 --port 8000
```

Open your browser at: `http://127.0.0.1:8000/`

---

## 📋 Production Pipeline Roadmap

- [x] **Phase 1: Market Intelligence & Bestseller Selection Dashboard**
- [ ] **Phase 2: PatternFast & Tailornova 1:1 Drafting & Multi-Size Export**
- [ ] **Phase 3: 16-Page Luxury Instruction Booklet (ReportLab Vector Panels)**
- [ ] **Phase 4: High-Converting Etsy Listing Slides (2000x2000 px)**
