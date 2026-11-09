# SpaFit — Master Spa Catalog & Automated Cover Sizer Suite

[![Architecture: Zero-CORS Offline](https://img.shields.io/badge/Architecture-Zero--CORS%20Offline-emerald.svg)](#architecture)
[![Catalog: 1,339 Spas](https://img.shields.io/badge/Spas%20Indexed-1%2C339-sky.svg)](#catalog-database)
[![Photos Top-View: 470](https://img.shields.io/badge/Top--View%20Photos-470%20(100%25%201%3A1)-blue.svg)](#assets--cad-coverage)
[![Factory CAD: 63 DXF/SVG](https://img.shields.io/badge/Factory%20CAD-63%20Models-amber.svg)](#cad-seal-tracer)

An engineering-grade spa catalog, automated gazebo/cover compatibility matrix, and interactive 2D seal trajectory simulator. Evaluates physical spa envelope dimensions, 4-corner radii, flat rim landing surfaces, and perimeter obstacles against 30 automated cover models across 6 design collections.

---

## Key Features

1. **Comprehensive Master Catalog (1,339 Spas)**
   - 38 international spa manufacturers across 14 manufacturing groups.
   - 100% 1:1 generational unicity: each spa entry is strictly bound to its verified production vintage and chassis code.
   - Comprehensive dimensional specs: Length, Width, Height, Corner Radius, Flat Rim Lip, and Footprint blueprints.

2. **Interactive 2D Seal Landing & Clearance Tracer (`index.html`)**
   - High-precision orthographic 2D top-down view rendered via HTML5 Canvas.
   - **Radial Gradient Transition Rim Detection**: Accurately measures flat landing lip width on both light and dark acrylic shells (Midnight Canyon, Slate, Black) without false threshold errors.
   - **4-Side Obstacle Detection**: Scans all 4 sides (`top`, `bottom`, `left`, `right`) for topside control keypads, raised pillows, waterfalls, and grab handles, converting normalized coordinates to precise Cartesian $(X, Y)$ callout pins.
   - **Round Spa Geometry**: Native support for circular spas ($R \approx L/2$) with point-to-curve distance clearance checks.
   - **Authentic Factory CAD Integration**: Directly renders genuine LibreDWG DXF/SVG factory contours at 1:1 scale with laser-aligned weather seal pathing.

3. **Master Catalog Explorer & Visual Comparator (`spa_catalog_viewer.html`)**
   - Instant search and filtering by Brand, Model, Generation, Collection, and Cover compatibility.
   - Toggle between authentic factory overhead photos and high-contrast SVG blueprints.
   - Modal deep-dive with physical spec sheets, multi-vintage timeline comparison, and one-click bridge to the 2D Seal Tracer (`index.html?spa_id=X`).

4. **Zero-CORS Offline Architecture**
   - Standalone offline runtime: runs directly under `file:///` without requiring Node.js, Webpack, or a local HTTP server.
   - Embedded database payloads via JavaScript global objects (`data/spas_catalog_data.js`).

---

## Quick Start

### Option 1: Direct In-Browser (No Install Required)
Simply open the HTML interfaces directly in any modern web browser:
- **`index.html`** : Interactive 2D Seal Tracer & Fit Configurator.
- **`spa_catalog_viewer.html`** : Master Catalog Browser with photo and blueprint views.

### Option 2: Python Environment (For Data Tools & Scraping Scripts)
To run or modify the catalog generation and extraction scripts:
```bash
# 1. Clone repository
git clone https://github.com/<your-username>/spafit-cover-sizer.git
cd spafit-cover-sizer

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Project Structure

```
├── index.html                 # 2D Interactive Seal Tracer & Fit Configurator
├── app.js                     # Core geometry, computer vision & seal simulation engine
├── spa_catalog_viewer.html    # Master Catalog Browser with 1,339 spas & comparator
├── style.css                  # UI styling & Tailwind dark mode configurations
├── requirements.txt           # Python dependencies for extraction/audit tools
├── .gitignore                 # GitHub ignore rules (excludes large binaries & caches)
│
├── data/
│   ├── spas_master_database.csv  # Single Source of Truth (SSOT) catalog CSV
│   ├── spas_catalog_data.js      # Zero-CORS embedded dataset for web frontends
│   ├── spas_catalog_data.json    # JSON compilation of catalog & cover models
│   └── models.json               # 30 automated cover specs (Oasis, Horizon, etc.)
│
├── assets/                    # Production assets organized by Manufacturer / Model
│   ├── <Brand>/<Model_Gen>/
│   │   ├── cad/               # Authentic factory DWG, DXF, and rendered vector SVGs
│   │   ├── top/               # Verified orthographic top-view photos
│   │   └── footprint/         # Manufacturer architectural blueprints (PDF/SVG)
│
└── scripts/                   # Pipeline scripts (JSON compilation, viewer builder, etc.)
    ├── generate_catalog_json.py        # Compiles master database to JSON/JS
    ├── build_spa_catalog_viewer.py     # Generates the standalone viewer HTML
    └── verify_confidentiality.py       # Integrity and confidentiality verification
```

---

## Specifications & Data Governance

- **Master Database Integrity**: 100% 1:1 generational unicity (1 row = 1 model vintage).
- **Perceptual Image Unicity**: Verified via dHash (difference hash, hash size 16) with 0 hash collisions across all 470 photos.
- **CAD Vector Certification**: All 63 genuine factory DWGs converted using LibreDWG and rendered via ezdxf to SVG vectors.

---

## License

Proprietary / Internal Engineering Tool. All rights reserved.
