import os

html_template = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SPAFIT — Master Spa Catalog & Gazebo Sizer Suite (1,339 Spas)</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            spafit: {
              blue: '#0072CE',
              cyan: '#0099D8',
              navy: '#0B2545',
              dark: '#080E1A',
              card: '#0F1A2E',
              cardhover: '#162540',
              border: '#1E3250',
              accent: '#38BDF8',
              emerald: '#10B981',
              amber: '#F59E0B',
              rose: '#F43F5E'
            }
          },
          fontFamily: {
            sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace']
          }
        }
      }
    }
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #080E1A; }
    ::-webkit-scrollbar-thumb { background: #1E3250; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #0072CE; }
    
    .grid-blueprint {
      background-size: 24px 24px;
      background-image: 
        linear-gradient(to right, rgba(30, 50, 80, 0.25) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(30, 50, 80, 0.25) 1px, transparent 1px);
    }
    .grid-blueprint-dense {
      background-size: 14px 14px;
      background-image: 
        linear-gradient(to right, rgba(0, 153, 216, 0.12) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0, 153, 216, 0.12) 1px, transparent 1px);
    }
    .glass-panel {
      background: rgba(15, 26, 46, 0.78);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(30, 50, 80, 0.65);
    }
    .img-zoom-hover:hover {
      transform: scale(1.03);
    }
  </style>
  <!-- Load Embedded Catalog Dataset (Zero-CORS guaranteed offline) -->
  <script src="data/spas_catalog_data.js"></script>
</head>
<body class="bg-spafit-dark text-slate-100 font-sans min-h-screen flex flex-col antialiased selection:bg-spafit-cyan selection:text-white">

  <!-- ==================== TOP NAVIGATION BAR ==================== -->
  <header class="sticky top-0 z-40 bg-spafit-dark/95 backdrop-blur-md border-b border-spafit-border px-4 lg:px-6 py-2.5">
    <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-3">
      
      <!-- Brand & Title -->
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-lg bg-gradient-to-br from-spafit-cyan to-spafit-blue flex items-center justify-center font-bold text-white shadow-lg shadow-spafit-blue/30 text-lg tracking-wider">
          C
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-base lg:text-lg font-bold tracking-tight text-white">SPAFIT</h1>
            <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-spafit-blue/20 text-spafit-accent border border-spafit-blue/30">Master Spa Catalog</span>
            <span id="navSpaCountBadge" class="text-xs font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">1,339 Spas</span>
          </div>
          <p class="text-xs text-slate-400 hidden sm:block">Top Views, Blueprints, Physical Radii & SpaFit Sizer Simulation</p>
        </div>
      </div>

      <!-- Quick Global Search Bar -->
      <div class="flex-1 max-w-md relative min-w-[220px]">
        <div class="relative">
          <input 
            type="text" 
            id="globalSearchInput" 
            placeholder="Search by model, brand, series (e.g. Grandee, Cameo, J-385, A8)... [/]" 
            class="w-full bg-spafit-card/90 border border-spafit-border text-sm rounded-lg pl-9 pr-9 py-1.5 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-spafit-cyan focus:border-transparent transition-all font-sans"
          />
          <svg class="w-4 h-4 text-slate-400 absolute left-3 top-2 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
          <button id="clearSearchBtn" class="hidden absolute right-2.5 top-2 text-slate-400 hover:text-white transition-colors" title="Clear search">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
      </div>

      <!-- Controls: Media Toggle, Units, View Mode, Export, 3D Configurator Link -->
      <div class="flex items-center gap-2">
        
        <!-- Global Card Media Toggle (Top View Photo vs CAD Blueprint) -->
        <div class="flex rounded-lg bg-spafit-card border border-spafit-border p-0.5 text-xs font-medium">
          <button id="mediaTogglePhoto" class="px-2.5 py-1 rounded bg-spafit-blue text-white shadow transition-all flex items-center gap-1" title="Show Real Overhead Photos on Cards">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
            <span>Photos</span>
          </button>
          <button id="mediaToggleBp" class="px-2.5 py-1 rounded text-slate-400 hover:text-white transition-all flex items-center gap-1" title="Show 2D Blueprints on Cards">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"></path></svg>
            <span>Blueprints</span>
          </button>
        </div>

        <!-- Unit Toggle (IN / CM) -->
        <div class="flex rounded-lg bg-spafit-card border border-spafit-border p-0.5 text-xs font-mono font-medium">
          <button id="unitToggleIn" class="px-2 py-1 rounded bg-spafit-blue text-white shadow transition-all">IN</button>
          <button id="unitToggleCm" class="px-2 py-1 rounded text-slate-400 hover:text-white transition-all">CM</button>
        </div>

        <!-- View Switcher -->
        <div class="flex rounded-lg bg-spafit-card border border-spafit-border p-0.5 text-xs">
          <button id="viewGridBtn" class="p-1.5 rounded bg-spafit-blue text-white shadow" title="Grid Card View">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
          </button>
          <button id="viewTableBtn" class="p-1.5 rounded text-slate-400 hover:text-white" title="Detailed Specification Table">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"></path></svg>
          </button>
          <button id="viewCompareBtn" class="p-1.5 rounded text-slate-400 hover:text-white relative" title="Compare Pinned Spas">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
            <span id="pinnedBadge" class="hidden absolute -top-1 -right-1 w-4 h-4 bg-spafit-cyan text-white text-[10px] font-bold rounded-full flex items-center justify-center">0</span>
          </button>
        </div>

        <!-- Export CSV Button -->
        <button id="exportCsvBtn" class="hidden xl:flex items-center gap-1 px-2.5 py-1 rounded-lg bg-spafit-card border border-spafit-border text-xs text-slate-300 hover:text-white transition-colors" title="Export current filtered view to CSV">
          <svg class="w-3.5 h-3.5 text-spafit-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
          CSV
        </button>

        <!-- Switch to 3D Configurator -->
        <a href="index.html" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gradient-to-r from-spafit-blue to-spafit-cyan text-xs font-semibold text-white shadow-md hover:brightness-110 transition-all" title="Open SpaFit 3D Gazebo Configurator">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path></svg>
          <span class="hidden md:inline">3D Configurator</span>
        </a>

      </div>
    </div>
  </header>

  <!-- ==================== MAIN WORKSPACE CONTAINER ==================== -->
  <div class="flex-1 max-w-7xl w-full mx-auto px-4 lg:px-6 py-4 flex flex-col md:flex-row gap-5">

    <!-- ==================== LEFT FILTER SIDEBAR ==================== -->
    <aside class="w-full md:w-72 lg:w-80 shrink-0 space-y-4">
      
      <!-- Quick Filter Cards / Stats -->
      <div class="glass-panel p-4 rounded-xl space-y-3">
        <div class="flex items-center justify-between">
          <h2 class="text-xs font-bold uppercase tracking-wider text-spafit-accent flex items-center gap-1.5">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path></svg>
            Filter & Facets
          </h2>
          <button id="resetFiltersBtn" class="text-[11px] text-slate-400 hover:text-spafit-accent hover:underline transition-colors">Reset All</button>
        </div>

        <!-- Top View Photos Filter Button (Special Quick Filter) -->
        <button id="onlyWithPhotosBtn" class="w-full py-2 px-3 rounded-lg border border-spafit-border bg-spafit-card hover:border-spafit-cyan text-xs font-semibold text-slate-200 flex items-center justify-between transition-all group">
          <span class="flex items-center gap-1.5 group-hover:text-spafit-cyan">
            <svg class="w-4 h-4 text-spafit-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
            Has Top View Photo
          </span>
          <span id="badgePhotoCount" class="text-[11px] font-mono px-2 py-0.5 rounded bg-spafit-blue/30 text-spafit-accent font-bold">413</span>
        </button>

        <!-- Segment Filter Pills -->
        <div>
          <label class="text-[11px] font-medium text-slate-400 block mb-1">Spa Category</label>
          <div class="grid grid-cols-3 gap-1">
            <button data-segment="all" id="segBtnAll" class="segment-btn active text-xs py-1.5 px-1.5 rounded bg-spafit-blue text-white font-medium text-center transition-all">All (1,339)</button>
            <button data-segment="hot_tub" id="segBtnHotTub" class="segment-btn text-xs py-1.5 px-1.5 rounded bg-spafit-card border border-spafit-border text-slate-300 hover:text-white text-center transition-all">Hot Tub (687)</button>
            <button data-segment="swim_spa" id="segBtnSwimSpa" class="segment-btn text-xs py-1.5 px-1.5 rounded bg-spafit-card border border-spafit-border text-slate-300 hover:text-white text-center transition-all">Swim Spa (385)</button>
          </div>
        </div>

        <!-- SpaFit Fit Quick Filter -->
        <div>
          <label class="text-[11px] font-medium text-slate-400 block mb-1">SpaFit Sizer Compatibility</label>
          <div class="grid grid-cols-3 gap-1.5 text-xs">
            <button data-spafit-filter="oasis" class="spafit-quick-btn py-1.5 px-2 rounded bg-spafit-card border border-spafit-border text-slate-300 hover:border-spafit-cyan hover:text-white flex items-center justify-between transition-all">
              <span>Oasis</span>
              <span id="badgeOasisCount" class="text-[10px] font-mono px-1.5 py-0.2 rounded bg-spafit-blue/30 text-spafit-accent font-bold">468</span>
            </button>
            <button data-spafit-filter="horizon" class="spafit-quick-btn py-1.5 px-2 rounded bg-spafit-card border border-spafit-border text-slate-300 hover:border-spafit-cyan hover:text-white flex items-center justify-between transition-all">
              <span>Horizon</span>
              <span id="badgeHorizonCount" class="text-[10px] font-mono px-1.5 py-0.2 rounded bg-amber-500/20 text-amber-400 font-bold">425</span>
            </button>
            <button data-spafit-filter="evolution" class="spafit-quick-btn py-1.5 px-2 rounded bg-spafit-card border border-spafit-border text-slate-300 hover:border-spafit-cyan hover:text-white flex items-center justify-between transition-all">
              <span>Evolution</span>
              <span id="badgeEvoCount" class="text-[10px] font-mono px-1.5 py-0.2 rounded bg-emerald-500/20 text-emerald-400 font-bold">436</span>
            </button>
            <button data-spafit-filter="legend" class="spafit-quick-btn py-1.5 px-2 rounded bg-spafit-card border border-spafit-border text-slate-300 hover:border-spafit-cyan hover:text-white flex items-center justify-between transition-all">
              <span>Legend</span>
              <span id="badgeLegendCount" class="text-[10px] font-mono px-1.5 py-0.2 rounded bg-purple-500/20 text-purple-400 font-bold">274</span>
            </button>
            <button data-spafit-filter="cad" class="spafit-quick-btn py-1.5 px-2 rounded bg-spafit-card border border-spafit-border text-slate-300 hover:border-spafit-cyan hover:text-white flex items-center justify-between transition-all">
              <span>CAD SVG</span>
              <span id="badgeCadCount" class="text-[10px] font-mono px-1.5 py-0.2 rounded bg-cyan-500/20 text-cyan-400 font-bold">48</span>
            </button>
            <button data-spafit-filter="any" class="spafit-quick-btn py-1.5 px-2 rounded bg-spafit-card border border-spafit-border text-slate-300 hover:border-spafit-cyan hover:text-white flex items-center justify-between transition-all">
              <span>Any Fit</span>
              <span id="badgeAnyCovCount" class="text-[10px] font-mono px-1.5 py-0.2 rounded bg-emerald-500/30 text-emerald-300 font-bold">782</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Manufacturer / Brand Selector -->
      <div class="glass-panel p-4 rounded-xl space-y-3">
        <div class="flex items-center justify-between">
          <label class="text-xs font-bold uppercase tracking-wider text-slate-300">Manufacturer (Marque)</label>
          <span id="activeBrandCount" class="text-[11px] font-mono text-slate-400">91 Brands</span>
        </div>
        
        <select id="brandSelect" class="w-full bg-spafit-card border border-spafit-border text-xs rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-1 focus:ring-spafit-cyan">
          <option value="all">All Manufacturers (1,339 Spas)</option>
          <!-- Dynamically populated -->
        </select>

        <!-- Series / Collection Selector -->
        <div>
          <label class="text-[11px] font-medium text-slate-400 block mb-1">Collection / Series</label>
          <select id="seriesSelect" class="w-full bg-spafit-card border border-spafit-border text-xs rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-1 focus:ring-spafit-cyan">
            <option value="all">All Collections / Series</option>
            <!-- Dynamically populated -->
          </select>
        </div>

        <!-- Generation Filter -->
        <div>
          <label class="text-[11px] font-medium text-slate-400 block mb-1">Vintage / Generation</label>
          <select id="genSelect" class="w-full bg-spafit-card border border-spafit-border text-xs rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-1 focus:ring-spafit-cyan">
            <option value="all">All Generations</option>
            <option value="Gen 1">Gen 1</option>
            <option value="Gen 2">Gen 2</option>
            <option value="Gen 3">Gen 3</option>
            <option value="Gen 4">Gen 4 (Modern 2019-2026)</option>
            <option value="NXT">NXT Architectural</option>
          </select>
        </div>
      </div>

      <!-- Physical Geometry Filters (Radius, Dimensions) -->
      <div class="glass-panel p-4 rounded-xl space-y-3.5">
        <h3 class="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center justify-between">
          <span>Corner Radius & Sizing</span>
          <span id="radiusFilterLabel" class="text-[11px] font-mono text-spafit-accent">All Radii</span>
        </h3>

        <!-- Corner Radius Presets -->
        <div class="grid grid-cols-2 gap-1.5 text-[11px]">
          <button data-radius-preset="all" class="radius-preset-btn active py-1 px-2 rounded bg-spafit-blue text-white text-center font-medium">All Radii</button>
          <button data-radius-preset="square" class="radius-preset-btn py-1 px-2 rounded bg-spafit-card border border-spafit-border text-slate-300 hover:text-white text-center">Square (0")</button>
          <button data-radius-preset="crisp" class="radius-preset-btn py-1 px-2 rounded bg-spafit-card border border-spafit-border text-slate-300 hover:text-white text-center">Crisp (2"–4")</button>
          <button data-radius-preset="classic" class="radius-preset-btn py-1 px-2 rounded bg-spafit-card border border-spafit-border text-slate-300 hover:text-white text-center">Classic (5"–8")</button>
          <button data-radius-preset="wide" class="radius-preset-btn py-1 px-2 rounded bg-spafit-card border border-spafit-border text-slate-300 hover:text-white text-center">Wide (9"–16")</button>
          <button data-radius-preset="round" class="radius-preset-btn py-1 px-2 rounded bg-spafit-card border border-spafit-border text-slate-300 hover:text-white text-center">Round / Circular</button>
        </div>

        <!-- Length Slider -->
        <div class="space-y-1">
          <div class="flex justify-between text-[11px]">
            <span class="text-slate-400">Max Length:</span>
            <span id="lengthValLabel" class="font-mono text-white font-semibold">300 in (762 cm)</span>
          </div>
          <input type="range" id="lengthSlider" min="60" max="300" value="300" step="5" class="w-full accent-spafit-cyan cursor-pointer">
        </div>

        <!-- Width Slider -->
        <div class="space-y-1">
          <div class="flex justify-between text-[11px]">
            <span class="text-slate-400">Max Width:</span>
            <span id="widthValLabel" class="font-mono text-white font-semibold">120 in (305 cm)</span>
          </div>
          <input type="range" id="widthSlider" min="45" max="120" value="120" step="1" class="w-full accent-spafit-cyan cursor-pointer">
        </div>
      </div>

    </aside>

    <!-- ==================== MAIN RESULTS PANEL ==================== -->
    <main class="flex-1 flex flex-col min-w-0 space-y-4">
      
      <!-- Sub-header bar: Counts, Active Pills, Sort -->
      <div class="glass-panel p-3.5 rounded-xl flex flex-wrap items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <span class="text-sm font-semibold text-white">
            <span id="resultsCount" class="font-mono text-spafit-accent font-bold text-base">1,339</span> spas found
          </span>
          <span class="text-xs text-slate-400 hidden sm:inline">|</span>
          <div id="activeFilterTags" class="flex flex-wrap items-center gap-1.5">
            <!-- Dynamically populated filter tags -->
          </div>
        </div>

        <!-- Sort by -->
        <div class="flex items-center gap-2 text-xs">
          <span class="text-slate-400 hidden sm:inline">Sort:</span>
          <select id="sortSelect" class="bg-spafit-card border border-spafit-border text-xs rounded-lg px-2.5 py-1.5 text-slate-200 focus:outline-none focus:ring-1 focus:ring-spafit-cyan">
            <option value="brand_asc">Manufacturer (A → Z)</option>
            <option value="model_asc">Model Name (A → Z)</option>
            <option value="length_desc">Length: Longest First</option>
            <option value="length_asc">Length: Shortest First</option>
            <option value="radius_asc">Corner Radius: Smallest First</option>
            <option value="radius_desc">Corner Radius: Largest First</option>
            <option value="year_desc">Vintage: Newest First</option>
          </select>
        </div>
      </div>

      <!-- ==================== VIEW MODE 1: GRID VIEW ==================== -->
      <div id="catalogGridContainer" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-4">
        <!-- Spa cards injected here -->
      </div>

      <!-- ==================== VIEW MODE 2: TABLE VIEW ==================== -->
      <div id="catalogTableContainer" class="hidden glass-panel rounded-xl overflow-hidden border border-spafit-border">
        <div class="overflow-x-auto max-h-[750px] overflow-y-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead class="sticky top-0 bg-spafit-card text-slate-300 font-semibold border-b border-spafit-border z-10">
              <tr>
                <th class="p-3">#</th>
                <th class="p-3">Photo / Thumb</th>
                <th class="p-3">Manufacturer</th>
                <th class="p-3">Series & Model</th>
                <th class="p-3">Gen / Vintage</th>
                <th class="p-3">Dimensions (L × W × H)</th>
                <th class="p-3">Corner Radius</th>
                <th class="p-3">SpaFit Fit</th>
                <th class="p-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody id="catalogTableBody" class="divide-y divide-spafit-border font-sans">
              <!-- Table rows injected here -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- ==================== VIEW MODE 3: PINNED COMPARISON VIEW ==================== -->
      <div id="catalogCompareContainer" class="hidden glass-panel rounded-xl p-5 space-y-6">
        <div class="flex items-center justify-between border-b border-spafit-border pb-3">
          <div>
            <h2 class="text-base font-bold text-white flex items-center gap-2">
              <svg class="w-5 h-5 text-spafit-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
              Multi-Spa Comparative Blueprint & Fitting Matrix
            </h2>
            <p class="text-xs text-slate-400">Side-by-side photographic, dimensional, blueprint, and SpaFit Gazebo fit comparison for pinned models</p>
          </div>
          <button id="clearPinnedBtn" class="text-xs text-rose-400 hover:text-rose-300 px-3 py-1.5 rounded bg-rose-500/10 border border-rose-500/20">Clear All Pinned</button>
        </div>

        <div id="compareCardsGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <!-- Pinned comparison cards injected here -->
        </div>
      </div>

      <!-- Empty State -->
      <div id="emptyState" class="hidden glass-panel p-12 text-center rounded-xl space-y-3">
        <div class="w-12 h-12 mx-auto rounded-full bg-spafit-blue/20 text-spafit-accent flex items-center justify-center">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        </div>
        <h3 class="text-base font-bold text-white">No spas match your criteria</h3>
        <p class="text-xs text-slate-400 max-w-sm mx-auto">Try widening your dimensional sliders, selecting "All Radii", or clearing your search term.</p>
        <button id="emptyResetBtn" class="px-4 py-2 rounded-lg bg-spafit-blue text-xs font-semibold text-white shadow hover:brightness-110 transition-all">Clear All Filters</button>
      </div>

    </main>
  </div>

  <!-- ==================== DETAILED TECHNICAL MODAL & SIMULATOR ==================== -->
  <div id="spaModal" class="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-3 lg:p-6 hidden">
    <div class="bg-spafit-dark border border-spafit-border rounded-2xl w-full max-w-5xl max-h-[92vh] flex flex-col shadow-2xl overflow-hidden">
      
      <!-- Modal Header -->
      <div class="px-5 py-3.5 border-b border-spafit-border bg-spafit-card/90 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <span id="modalBrandBadge" class="text-xs font-bold px-2.5 py-1 rounded bg-spafit-blue/30 text-spafit-accent border border-spafit-blue/40">Hot Spring Spas</span>
          <div>
            <div class="flex items-center gap-2">
              <h2 id="modalModelTitle" class="text-lg font-bold text-white tracking-tight">Grandee</h2>
              <span id="modalGenBadge" class="text-xs px-2 py-0.5 rounded-full bg-slate-700 text-slate-300 font-mono">Gen 4 (2019-2026)</span>
            </div>
            <p id="modalSubtitle" class="text-xs text-slate-400">Highlife Collection | Chassis GGN | Watkins Wellness</p>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <!-- Pin button inside modal -->
          <!-- Open in Seal Tracer button -->
          <a id="modalOpenTracerLink" href="index.html" target="_blank" class="px-2.5 py-1.5 rounded-lg bg-emerald-600/30 hover:bg-emerald-600 border border-emerald-500/50 text-xs text-emerald-200 hover:text-white flex items-center gap-1.5 transition-colors font-semibold" title="Ouvrir dans l'Analyseur de Joint 2D">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
            <span>Ouvrir dans l'Analyseur de Joint</span>
          </a>

          <button id="modalPinBtn" class="px-2.5 py-1.5 rounded-lg bg-spafit-card border border-spafit-border text-xs text-slate-300 hover:text-white flex items-center gap-1.5 transition-colors">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path></svg>
            <span id="modalPinText">Pin for Compare</span>
          </button>
          
          <!-- Close button -->
          <button id="modalCloseBtn" class="w-8 h-8 rounded-lg bg-spafit-card border border-spafit-border flex items-center justify-center text-slate-400 hover:text-white transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>
      </div>

      <!-- Modal Tabs Navigation -->
      <div class="px-5 border-b border-spafit-border bg-spafit-card/50 flex items-center gap-1 text-xs font-medium overflow-x-auto">
        <button data-tab="visual" class="modal-tab-btn active px-4 py-2.5 border-b-2 border-spafit-cyan text-white font-semibold flex items-center gap-1.5 transition-all">
          <svg class="w-3.5 h-3.5 text-spafit-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
          Top View & Blueprint
        </button>
        <button data-tab="spafit" class="modal-tab-btn px-4 py-2.5 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-1.5 transition-all">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
          SpaFit Sizer Simulator
        </button>
        <button data-tab="specs" class="modal-tab-btn px-4 py-2.5 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-1.5 transition-all">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
          Full Spec Sheet
        </button>
        <button data-tab="timeline" class="modal-tab-btn px-4 py-2.5 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-1.5 transition-all">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          Generational Radius Evolution
        </button>
        <button data-tab="assets" class="modal-tab-btn px-4 py-2.5 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-1.5 transition-all">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
          CAD, 3D & Gallery
        </button>
      </div>

      <!-- Modal Body Content -->
      <div class="flex-1 overflow-y-auto p-5 lg:p-6 space-y-6">

        <!-- ==================== TAB 1: TOP VIEW PHOTO & BLUEPRINT ==================== -->
        <div id="tabContentVisual" class="modal-tab-content space-y-5">
          
          <!-- View Sub-Toggle (Photo | Blueprint | Split Side-by-Side) -->
          <div class="flex items-center justify-between bg-spafit-card/80 p-2 rounded-xl border border-spafit-border">
            <span class="text-xs font-semibold text-slate-300 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-spafit-cyan"></span>
              Visualization Mode:
            </span>
            <div class="flex rounded-lg bg-spafit-dark border border-spafit-border p-0.5 text-xs font-medium">
              <button id="modalSubTogglePhoto" class="px-3 py-1.5 rounded bg-spafit-blue text-white shadow transition-all flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                <span>Top View Photo</span>
              </button>
              <button id="modalSubToggleBp" class="px-3 py-1.5 rounded text-slate-400 hover:text-white transition-all flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"></path></svg>
                <span>CAD Blueprint</span>
              </button>
              <button id="modalSubToggleSplit" class="px-3 py-1.5 rounded text-slate-400 hover:text-white transition-all flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2"></path></svg>
                <span>Split View</span>
              </button>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <!-- Main Display Area (Photo or Blueprint or Split) -->
            <div id="modalVisualDisplayArea" class="lg:col-span-2 glass-panel p-4 rounded-xl flex flex-col items-center justify-center relative min-h-[440px] overflow-hidden">
              
              <!-- Container for Top View Photo -->
              <div id="modalPhotoContainer" class="w-full h-full flex items-center justify-center relative group">
                <img id="modalTopImg" src="" alt="Top View Photo" class="max-h-[380px] max-w-full object-contain rounded-lg shadow-xl drop-shadow-[0_10px_20px_rgba(0,0,0,0.6)] transition-transform duration-300">
                <div id="modalPhotoFallback" class="hidden text-center p-8 space-y-2">
                  <div class="w-12 h-12 mx-auto rounded-full bg-slate-800 text-slate-400 flex items-center justify-center">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                  </div>
                  <h4 class="text-sm font-bold text-slate-200">Top View Photo Not Published for this Vintage</h4>
                  <p class="text-xs text-slate-400 max-w-xs mx-auto">Displaying precision CAD blueprint calculated from official manufacturer PDI and factory templates.</p>
                </div>
                <!-- Floating Expand / Fullscreen Link -->
                <a id="modalImgExternalLink" href="#" target="_blank" class="absolute bottom-3 right-3 px-3 py-1.5 rounded-lg bg-spafit-dark/90 border border-spafit-border text-xs text-spafit-cyan hover:text-white flex items-center gap-1.5 shadow-lg backdrop-blur">
                  <span>Open Full-Res Photo</span>
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                </a>
              </div>

              <!-- Container for SVG Blueprint -->
              <div id="modalBpContainer" class="hidden w-full h-full flex items-center justify-center grid-blueprint-dense relative p-2">
                <div id="modalSvgHolder" class="w-full h-full flex items-center justify-center"></div>
                <!-- Blueprint Layer Overlay Toggles -->
                <div class="absolute bottom-3 left-3 bg-spafit-dark/90 backdrop-blur-md border border-spafit-border rounded-lg px-3 py-1.5 flex items-center gap-3 text-[11px] font-mono text-slate-300">
                  <span class="text-slate-400 uppercase tracking-wider text-[10px]">Overlays:</span>
                  <label class="flex items-center gap-1 cursor-pointer">
                    <input type="checkbox" id="toggleLayerSpaFit" checked class="accent-spafit-cyan">
                    <span>SpaFit Posts</span>
                  </label>
                  <label class="flex items-center gap-1 cursor-pointer">
                    <input type="checkbox" id="toggleLayerSeal" checked class="accent-spafit-cyan">
                    <span>Seal Landing</span>
                  </label>
                </div>
              </div>

              <!-- Container for Split Side-by-Side View -->
              <div id="modalSplitContainer" class="hidden w-full h-full grid grid-cols-1 md:grid-cols-2 gap-4 items-center">
                <div class="w-full h-64 md:h-80 rounded-lg bg-spafit-dark/90 border border-spafit-border flex items-center justify-center p-2 relative overflow-hidden">
                  <img id="modalSplitImg" src="" alt="Top View" class="max-h-full max-w-full object-contain">
                  <span class="absolute top-2 left-2 text-[10px] font-mono bg-spafit-dark/90 px-2 py-0.5 rounded text-spafit-cyan border border-spafit-border">Photo</span>
                </div>
                <div class="w-full h-64 md:h-80 rounded-lg bg-spafit-dark/90 border border-spafit-border grid-blueprint p-2 flex items-center justify-center relative overflow-hidden">
                  <div id="modalSplitSvgHolder" class="w-full h-full flex items-center justify-center"></div>
                  <span class="absolute top-2 left-2 text-[10px] font-mono bg-spafit-dark/90 px-2 py-0.5 rounded text-spafit-accent border border-spafit-border">CAD Blueprint</span>
                </div>
              </div>

            </div>

            <!-- Blueprint Dimension & Geometric Summary -->
            <div class="space-y-4">
              <div class="glass-panel p-4 rounded-xl space-y-3">
                <h4 class="text-xs font-bold uppercase tracking-wider text-spafit-accent">Verified Physical Geometry</h4>
                
                <div class="space-y-2 text-xs">
                  <div class="flex justify-between items-center py-1.5 border-b border-spafit-border">
                    <span class="text-slate-400">Length (Longueur):</span>
                    <span id="bpLength" class="font-mono font-bold text-white">100.0" (254.0 cm)</span>
                  </div>
                  <div class="flex justify-between items-center py-1.5 border-b border-spafit-border">
                    <span class="text-slate-400">Width (Largeur):</span>
                    <span id="bpWidth" class="font-mono font-bold text-white">91.0" (231.1 cm)</span>
                  </div>
                  <div class="flex justify-between items-center py-1.5 border-b border-spafit-border">
                    <span class="text-slate-400">Height (Hauteur):</span>
                    <span id="bpHeight" class="font-mono font-bold text-white">38.0" (96.5 cm)</span>
                  </div>
                  <div class="flex justify-between items-center py-1.5 border-b border-spafit-border">
                    <span class="text-slate-400 font-semibold text-spafit-cyan">Corner Radius (R):</span>
                    <span id="bpRadius" class="font-mono font-bold text-spafit-cyan bg-spafit-cyan/10 px-2 py-0.5 rounded border border-spafit-cyan/30">3.0" (7.6 cm)</span>
                  </div>
                  <div class="flex justify-between items-center py-1.5 border-b border-spafit-border">
                    <span class="text-slate-400">Diagonal Dimension:</span>
                    <span id="bpDiag" class="font-mono text-slate-200">135.2" (343.4 cm)</span>
                  </div>
                  <div class="flex justify-between items-center py-1.5">
                    <span class="text-slate-400">Perimeter / Rim Surface:</span>
                    <span id="bpPerimeter" class="font-mono text-slate-200">376.9" (957.3 cm)</span>
                  </div>
                </div>
              </div>

              <!-- Quick Fit Card -->
              <div class="glass-panel p-4 rounded-xl space-y-2">
                <h4 class="text-xs font-bold uppercase tracking-wider text-slate-300">SpaFit Sizer Summary</h4>
                <div id="bpSpaFitQuickPills" class="flex flex-wrap gap-1.5">
                  <!-- Badges injected -->
                </div>
                <button id="bpSimulateNowBtn" class="w-full mt-2 py-2 rounded-lg bg-spafit-blue hover:bg-spafit-cyan text-xs font-semibold text-white transition-all shadow flex items-center justify-center gap-1.5">
                  <span>Open Detailed SpaFit Simulation</span>
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                </button>
              </div>

            </div>
          </div>
        </div>

        <!-- ==================== TAB 2: SPAFIT COMPATIBILITY SIMULATOR ==================== -->
        <div id="tabContentSpaFit" class="modal-tab-content space-y-6 hidden">
          <div class="glass-panel p-5 rounded-xl space-y-4">
            
            <div class="flex flex-wrap items-center justify-between gap-3 border-b border-spafit-border pb-4">
              <div>
                <h3 class="text-sm font-bold text-white flex items-center gap-2">
                  <span class="w-2.5 h-2.5 rounded-full bg-spafit-cyan animate-pulse"></span>
                  SpaFit Gazebo Fit & Mechanical Simulation
                </h3>
                <p class="text-xs text-slate-400">Simulate physical clearances against all 29 official SpaFit models</p>
              </div>

              <div class="flex items-center gap-2">
                <button id="autoSelectBestSpaFitBtn" class="px-3 py-1.5 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-semibold hover:bg-emerald-500/30 transition-all flex items-center gap-1.5">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                  Auto-Select Optimal Model
                </button>
              </div>
            </div>

            <!-- SpaFit Model Dropdown & Orientation -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div class="sm:col-span-2 space-y-1">
                <label class="text-[11px] font-medium text-slate-400">Select SpaFit Gazebo Model to Test:</label>
                <select id="spafitModelSelect" class="w-full bg-spafit-card border border-spafit-border text-xs rounded-lg px-3 py-2 text-white font-medium focus:outline-none focus:ring-1 focus:ring-spafit-cyan">
                  <!-- Populated from SPAFIT_MODELS -->
                </select>
              </div>

              <div class="space-y-1">
                <label class="text-[11px] font-medium text-slate-400">Installation Orientation:</label>
                <select id="spafitOrientationSelect" class="w-full bg-spafit-card border border-spafit-border text-xs rounded-lg px-3 py-2 text-white font-medium focus:outline-none focus:ring-1 focus:ring-spafit-cyan">
                  <option value="standard">Standard (Spa Length || Cover Length)</option>
                  <option value="rotated">Rotated 90° (Spa Length || Cover Width)</option>
                </select>
              </div>
            </div>

            <!-- Live Diagnostic Results Card -->
            <div id="spafitDiagnosticBanner" class="p-4 rounded-xl border flex items-start gap-3">
              <!-- Injected dynamically -->
            </div>

            <!-- Clearances Breakdown Grid -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
              
              <!-- Column Clearance X -->
              <div class="glass-panel p-3.5 rounded-xl space-y-1.5">
                <span class="text-slate-400 block text-[11px]">Column Margin X (Length)</span>
                <div class="flex items-baseline justify-between">
                  <span id="simMarginX" class="text-base font-mono font-bold text-white">+2.50"</span>
                  <span id="simStatusX" class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400">OPTIMAL</span>
                </div>
                <div class="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                  <div id="simBarX" class="bg-emerald-500 h-1.5 rounded-full" style="width: 80%"></div>
                </div>
                <span id="simDescX" class="text-[10px] text-slate-400 block">Min recommended: 1.25"</span>
              </div>

              <!-- Column Clearance Y -->
              <div class="glass-panel p-3.5 rounded-xl space-y-1.5">
                <span class="text-slate-400 block text-[11px]">Column Margin Y (Width)</span>
                <div class="flex items-baseline justify-between">
                  <span id="simMarginY" class="text-base font-mono font-bold text-white">+1.00"</span>
                  <span id="simStatusY" class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400">MARGINAL</span>
                </div>
                <div class="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                  <div id="simBarY" class="bg-amber-500 h-1.5 rounded-full" style="width: 50%"></div>
                </div>
                <span id="simDescY" class="text-[10px] text-slate-400 block">Min safe: 0.50"</span>
              </div>

              <!-- Seal Landing Contact -->
              <div class="glass-panel p-3.5 rounded-xl space-y-1.5">
                <span class="text-slate-400 block text-[11px]">Seal Contact Band (3.5")</span>
                <div class="flex items-baseline justify-between">
                  <span id="simSealCoverage" class="text-base font-mono font-bold text-white">100%</span>
                  <span id="simStatusSeal" class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400">COMPLIANT</span>
                </div>
                <div class="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                  <div id="simBarSeal" class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div>
                </div>
                <span id="simDescSeal" class="text-[10px] text-slate-400 block">Shell within seal range</span>
              </div>

              <!-- Height Clearance -->
              <div class="glass-panel p-3.5 rounded-xl space-y-1.5">
                <span class="text-slate-400 block text-[11px]">Height Stroke & Operating Range</span>
                <div class="flex items-baseline justify-between">
                  <span id="simHeightVal" class="text-base font-mono font-bold text-white">38.0"</span>
                  <span id="simStatusHeight" class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400">PASSED</span>
                </div>
                <div class="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                  <div id="simBarHeight" class="bg-emerald-500 h-1.5 rounded-full" style="width: 65%"></div>
                </div>
                <span id="simDescHeight" class="text-[10px] text-slate-400 block">Cover range: [34.0" - 48.0"]</span>
              </div>

            </div>

            <!-- Mini Overlay Diagram for Current Simulation -->
            <div class="glass-panel p-4 rounded-xl space-y-2">
              <h4 class="text-xs font-bold uppercase tracking-wider text-slate-300">Live Clearance Footprint Overlay</h4>
              <div id="simSvgContainer" class="w-full h-64 flex items-center justify-center grid-blueprint rounded-lg overflow-hidden border border-spafit-border">
                <!-- Live SVG fit preview -->
              </div>
            </div>

          </div>
        </div>

        <!-- ==================== TAB 3: ENGINEERING SPEC SHEET ==================== -->
        <div id="tabContentSpecs" class="modal-tab-content space-y-4 hidden">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            
            <!-- Manufacturer & Identifiers -->
            <div class="glass-panel p-4 rounded-xl space-y-2">
              <h4 class="font-bold uppercase tracking-wider text-spafit-accent text-[11px]">Manufacturer & Model Identity</h4>
              <div class="space-y-1.5 text-slate-300">
                <div class="flex justify-between py-1 border-b border-spafit-border"><span class="text-slate-400">Manufacturer Group:</span><span id="specGroupe" class="font-semibold text-white"></span></div>
                <div class="flex justify-between py-1 border-b border-spafit-border"><span class="text-slate-400">Brand / Marque:</span><span id="specMarque" class="font-semibold text-white"></span></div>
                <div class="flex justify-between py-1 border-b border-spafit-border"><span class="text-slate-400">Segment:</span><span id="specSegment" class="font-semibold text-white"></span></div>
                <div class="flex justify-between py-1 border-b border-spafit-border"><span class="text-slate-400">Collection / Series:</span><span id="specSerie" class="font-semibold text-white"></span></div>
                <div class="flex justify-between py-1 border-b border-spafit-border"><span class="text-slate-400">Model Name:</span><span id="specModele" class="font-semibold text-white"></span></div>
                <div class="flex justify-between py-1 border-b border-spafit-border"><span class="text-slate-400">Sub-Model / Version:</span><span id="specSousModele" class="font-semibold text-white"></span></div>
                <div class="flex justify-between py-1 border-b border-spafit-border"><span class="text-slate-400">Factory Chassis Code:</span><span id="specChassis" class="font-mono text-spafit-cyan"></span></div>
                <div class="flex justify-between py-1"><span class="text-slate-400">Production Years:</span><span id="specAnnees" class="font-semibold text-white"></span></div>
              </div>
            </div>

            <!-- Physical & Engineering Metrics -->
            <div class="glass-panel p-4 rounded-xl space-y-2">
              <h4 class="font-bold uppercase tracking-wider text-spafit-accent text-[11px]">Physical Dimensions & Metric Conversions</h4>
              <div class="space-y-1.5 text-slate-300">
                <div class="flex justify-between py-1 border-b border-spafit-border"><span class="text-slate-400">Length (Imperial):</span><span id="specLIn" class="font-mono text-white"></span></div>
                <div class="flex justify-between py-1 border-b border-spafit-border"><span class="text-slate-400">Length (Metric):</span><span id="specLCm" class="font-mono text-white"></span></div>
                <div class="flex justify-between py-1 border-b border-spafit-border"><span class="text-slate-400">Width (Imperial):</span><span id="specWIn" class="font-mono text-white"></span></div>
                <div class="flex justify-between py-1 border-b border-spafit-border"><span class="text-slate-400">Width (Metric):</span><span id="specWCm" class="font-mono text-white"></span></div>
                <div class="flex justify-between py-1 border-b border-spafit-border"><span class="text-slate-400">Height (Imperial):</span><span id="specHIn" class="font-mono text-white"></span></div>
                <div class="flex justify-between py-1 border-b border-spafit-border"><span class="text-slate-400">Height (Metric):</span><span id="specHCm" class="font-mono text-white"></span></div>
                <div class="flex justify-between py-1 border-b border-spafit-border"><span class="text-slate-400 font-bold text-spafit-cyan">Corner Radius (Imperial):</span><span id="specRIn" class="font-mono font-bold text-spafit-cyan"></span></div>
                <div class="flex justify-between py-1"><span class="text-slate-400">Corner Radius (Metric):</span><span id="specRCm" class="font-mono font-bold text-spafit-cyan"></span></div>
              </div>
            </div>

            <!-- Verification & Audit Compliance -->
            <div class="md:col-span-2 glass-panel p-4 rounded-xl space-y-2">
              <div class="flex items-center justify-between">
                <h4 class="font-bold uppercase tracking-wider text-spafit-accent text-[11px]">Verification Audit & Negative Assertions</h4>
                <span id="specStatusBadge" class="text-xs px-2.5 py-0.5 rounded-full font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">VERIFIED_DUAL_SOURCE</span>
              </div>
              <p id="specAuditNotes" class="text-xs text-slate-300 leading-relaxed font-mono bg-spafit-card/60 p-3 rounded-lg border border-spafit-border"></p>
            </div>

          </div>
        </div>

        <!-- ==================== TAB 4: GENERATIONAL RADIUS EVOLUTION ==================== -->
        <div id="tabContentTimeline" class="modal-tab-content space-y-4 hidden">
          <div class="glass-panel p-5 rounded-xl space-y-4">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center gap-2">
                <svg class="w-4 h-4 text-spafit-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                Generational Mold & Radius Progression
              </h3>
              <p class="text-xs text-slate-400">Comparison of all production vintages for this specific model line</p>
            </div>

            <div id="timelineContainer" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <!-- Sibling generations injected dynamically -->
            </div>
          </div>

          <!-- Wayback Machine 3-Year Generational Tracking Archive -->
          <div class="glass-panel p-5 rounded-xl space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-sm font-bold text-white flex items-center gap-2">
                  <span class="text-base">🏛️</span>
                  Wayback Machine 3-Year Generational Archive
                </h3>
                <p class="text-xs text-slate-400">Official CAD blueprints, overhead photography, and spec sheets tracked across milestone vintages</p>
              </div>
              <span id="waybackTrackingBadge" class="text-[10px] font-mono px-2 py-0.5 rounded bg-spafit-blue/30 text-spafit-accent border border-spafit-blue/40">CDX API Tracked</span>
            </div>

            <div id="waybackVintageContainer" class="space-y-3">
              <!-- Dynamic milestone cards injected dynamically -->
            </div>
          </div>
        </div>

        <!-- ==================== TAB 5: VISUAL GALLERY & CAD ASSETS ==================== -->
        <div id="tabContentAssets" class="modal-tab-content space-y-5 hidden">
          
          <!-- Visual Photo Gallery in Assets Tab -->
          <div class="glass-panel p-5 rounded-xl space-y-4">
            <h3 class="text-sm font-bold text-white flex items-center gap-2">
              <svg class="w-4 h-4 text-spafit-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
              Physical Spa Photography Gallery
            </h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Overhead Top View Photo -->
              <div class="p-3.5 rounded-xl bg-spafit-card/80 border border-spafit-border space-y-2.5">
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-spafit-accent uppercase tracking-wider text-[11px]">Top View (Overhead Shell)</span>
                  <span id="galleryTopBadge" class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300">Verified Photo</span>
                </div>
                <div class="w-full h-56 rounded-lg bg-spafit-dark/90 border border-spafit-border flex items-center justify-center p-2 overflow-hidden relative group">
                  <img id="galleryTopImg" src="" alt="Top View Shell" class="max-h-full max-w-full object-contain rounded drop-shadow-md transition-transform duration-300 group-hover:scale-105">
                  <div id="galleryTopFallback" class="hidden text-xs text-slate-500 text-center">No photo on disk for this vintage</div>
                  <a id="galleryTopLink" href="#" target="_blank" class="absolute bottom-2 right-2 text-[10px] font-mono bg-spafit-dark/90 px-2 py-1 rounded text-spafit-cyan border border-spafit-border hover:text-white transition-colors">Open Full-Res ↗</a>
                </div>
              </div>

              <!-- Side View Elevation Photo -->
              <div class="p-3.5 rounded-xl bg-spafit-card/80 border border-spafit-border space-y-2.5">
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-slate-300 uppercase tracking-wider text-[11px]">Side View (Elevation / Skirt)</span>
                  <span id="gallerySideBadge" class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">Elevation</span>
                </div>
                <div class="w-full h-56 rounded-lg bg-spafit-dark/90 border border-spafit-border flex items-center justify-center p-2 overflow-hidden relative group">
                  <img id="gallerySideImg" src="" alt="Side Elevation" class="max-h-full max-w-full object-contain rounded drop-shadow-md transition-transform duration-300 group-hover:scale-105">
                  <div id="gallerySideFallback" class="hidden text-xs text-slate-500 text-center">No side-view photo available</div>
                  <a id="gallerySideLink" href="#" target="_blank" class="absolute bottom-2 right-2 text-[10px] font-mono bg-spafit-dark/90 px-2 py-1 rounded text-spafit-cyan border border-spafit-border hover:text-white transition-colors">Open Full-Res ↗</a>
                </div>
              </div>
            </div>
          </div>

          <!-- 2D / 3D CAD Downloads & Verified Source URLs -->
          <div class="glass-panel p-5 rounded-xl space-y-4">
            <h3 class="text-sm font-bold text-white">Harvested Engineering Drawings & Factory Links</h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- 2D / 3D CAD Downloads -->
              <div class="space-y-2 text-xs">
                <h4 class="font-bold text-slate-300 uppercase tracking-wider text-[11px]">Engineering CAD / BIM Assets</h4>
                <div class="space-y-1.5" id="assetLinksContainer"></div>
              </div>

              <!-- Official Source URLs -->
              <div class="space-y-2 text-xs">
                <h4 class="font-bold text-slate-300 uppercase tracking-wider text-[11px]">Verified Source Documentation Links</h4>
                <div class="space-y-1.5" id="sourceUrlsContainer"></div>
              </div>
            </div>
          </div>

        </div>

      </div>

      <!-- Modal Footer -->
      <div class="px-5 py-3 border-t border-spafit-border bg-spafit-card/90 flex items-center justify-between text-xs text-slate-400">
        <div class="flex items-center gap-2">
          <span>Row ID: <span id="modalRowId" class="font-mono text-white font-semibold">1</span></span>
          <span>•</span>
          <span id="modalProcessTime" class="font-mono">Verified Dual Source</span>
        </div>
        <button id="modalCloseFooterBtn" class="px-4 py-1.5 rounded-lg bg-spafit-card border border-spafit-border text-slate-200 hover:text-white hover:bg-spafit-cardhover transition-colors">Close</button>
      </div>

    </div>
  </div>

  <!-- ==================== APPLICATION JAVASCRIPT ==================== -->
  <script>
    /**
     * SPAFIT Master Spa Catalog & Fit Simulator Application
     */
    (function() {
      // Application State
      const state = {
        spas: [],
        spafitModels: [],
        filteredSpas: [],
        searchTerm: '',
        selectedBrand: 'all',
        selectedSeries: 'all',
        selectedGen: 'all',
        selectedSegment: 'all',
        selectedSpaFitFilter: 'all',
        radiusPreset: 'all',
        onlyWithPhotos: false,
        cardMediaMode: 'photo', // 'photo' or 'bp'
        maxLength: 300,
        maxWidth: 120,
        unit: 'in', // 'in' or 'cm'
        viewMode: 'grid', // 'grid', 'table', 'compare'
        sortBy: 'brand_asc',
        pinnedIds: new Set(),
        activeSpa: null,
        activeSpaFitModelId: 'oasis-std-8x8',
        simOrientation: 'standard',
        showLayerSpaFit: true,
        showLayerSeal: true,
        modalVisualMode: 'photo', // 'photo', 'bp', 'split'
        cardFlipMap: {} // spa.id -> 'photo' or 'bp'
      };

      // DOM Elements
      const els = {
        globalSearchInput: document.getElementById('globalSearchInput'),
        clearSearchBtn: document.getElementById('clearSearchBtn'),
        mediaTogglePhoto: document.getElementById('mediaTogglePhoto'),
        mediaToggleBp: document.getElementById('mediaToggleBp'),
        unitToggleIn: document.getElementById('unitToggleIn'),
        unitToggleCm: document.getElementById('unitToggleCm'),
        viewGridBtn: document.getElementById('viewGridBtn'),
        viewTableBtn: document.getElementById('viewTableBtn'),
        viewCompareBtn: document.getElementById('viewCompareBtn'),
        pinnedBadge: document.getElementById('pinnedBadge'),
        exportCsvBtn: document.getElementById('exportCsvBtn'),
        resetFiltersBtn: document.getElementById('resetFiltersBtn'),
        emptyResetBtn: document.getElementById('emptyResetBtn'),
        onlyWithPhotosBtn: document.getElementById('onlyWithPhotosBtn'),
        badgePhotoCount: document.getElementById('badgePhotoCount'),
        brandSelect: document.getElementById('brandSelect'),
        seriesSelect: document.getElementById('seriesSelect'),
        genSelect: document.getElementById('genSelect'),
        lengthSlider: document.getElementById('lengthSlider'),
        widthSlider: document.getElementById('widthSlider'),
        lengthValLabel: document.getElementById('lengthValLabel'),
        widthValLabel: document.getElementById('widthValLabel'),
        radiusFilterLabel: document.getElementById('radiusFilterLabel'),
        resultsCount: document.getElementById('resultsCount'),
        activeFilterTags: document.getElementById('activeFilterTags'),
        sortSelect: document.getElementById('sortSelect'),
        catalogGridContainer: document.getElementById('catalogGridContainer'),
        catalogTableContainer: document.getElementById('catalogTableContainer'),
        catalogTableBody: document.getElementById('catalogTableBody'),
        catalogCompareContainer: document.getElementById('catalogCompareContainer'),
        compareCardsGrid: document.getElementById('compareCardsGrid'),
        clearPinnedBtn: document.getElementById('clearPinnedBtn'),
        emptyState: document.getElementById('emptyState'),
        // Modal
        spaModal: document.getElementById('spaModal'),
        modalCloseBtn: document.getElementById('modalCloseBtn'),
        modalCloseFooterBtn: document.getElementById('modalCloseFooterBtn'),
        modalBrandBadge: document.getElementById('modalBrandBadge'),
        modalModelTitle: document.getElementById('modalModelTitle'),
        modalGenBadge: document.getElementById('modalGenBadge'),
        modalSubtitle: document.getElementById('modalSubtitle'),
        modalOpenTracerLink: document.getElementById('modalOpenTracerLink'),
        modalPinBtn: document.getElementById('modalPinBtn'),
        modalPinText: document.getElementById('modalPinText'),
        modalRowId: document.getElementById('modalRowId'),
        modalProcessTime: document.getElementById('modalProcessTime'),
        // Modal Visual Tab
        modalSubTogglePhoto: document.getElementById('modalSubTogglePhoto'),
        modalSubToggleBp: document.getElementById('modalSubToggleBp'),
        modalSubToggleSplit: document.getElementById('modalSubToggleSplit'),
        modalPhotoContainer: document.getElementById('modalPhotoContainer'),
        modalTopImg: document.getElementById('modalTopImg'),
        modalPhotoFallback: document.getElementById('modalPhotoFallback'),
        modalImgExternalLink: document.getElementById('modalImgExternalLink'),
        modalBpContainer: document.getElementById('modalBpContainer'),
        modalSvgHolder: document.getElementById('modalSvgHolder'),
        modalSplitContainer: document.getElementById('modalSplitContainer'),
        modalSplitImg: document.getElementById('modalSplitImg'),
        modalSplitSvgHolder: document.getElementById('modalSplitSvgHolder'),
        toggleLayerSpaFit: document.getElementById('toggleLayerSpaFit'),
        toggleLayerSeal: document.getElementById('toggleLayerSeal'),
        bpLength: document.getElementById('bpLength'),
        bpWidth: document.getElementById('bpWidth'),
        bpHeight: document.getElementById('bpHeight'),
        bpRadius: document.getElementById('bpRadius'),
        bpDiag: document.getElementById('bpDiag'),
        bpPerimeter: document.getElementById('bpPerimeter'),
        bpSpaFitQuickPills: document.getElementById('bpSpaFitQuickPills'),
        bpSimulateNowBtn: document.getElementById('bpSimulateNowBtn'),
        // Simulator Tab
        spafitModelSelect: document.getElementById('spafitModelSelect'),
        spafitOrientationSelect: document.getElementById('spafitOrientationSelect'),
        autoSelectBestSpaFitBtn: document.getElementById('autoSelectBestSpaFitBtn'),
        spafitDiagnosticBanner: document.getElementById('spafitDiagnosticBanner'),
        simMarginX: document.getElementById('simMarginX'),
        simStatusX: document.getElementById('simStatusX'),
        simBarX: document.getElementById('simBarX'),
        simDescX: document.getElementById('simDescX'),
        simMarginY: document.getElementById('simMarginY'),
        simStatusY: document.getElementById('simStatusY'),
        simBarY: document.getElementById('simBarY'),
        simDescY: document.getElementById('simDescY'),
        simSealCoverage: document.getElementById('simSealCoverage'),
        simStatusSeal: document.getElementById('simStatusSeal'),
        simBarSeal: document.getElementById('simBarSeal'),
        simDescSeal: document.getElementById('simDescSeal'),
        simHeightVal: document.getElementById('simHeightVal'),
        simStatusHeight: document.getElementById('simStatusHeight'),
        simBarHeight: document.getElementById('simBarHeight'),
        simDescHeight: document.getElementById('simDescHeight'),
        simSvgContainer: document.getElementById('simSvgContainer'),
        // Specs Tab
        specGroupe: document.getElementById('specGroupe'),
        specMarque: document.getElementById('specMarque'),
        specSegment: document.getElementById('specSegment'),
        specSerie: document.getElementById('specSerie'),
        specModele: document.getElementById('specModele'),
        specSousModele: document.getElementById('specSousModele'),
        specChassis: document.getElementById('specChassis'),
        specAnnees: document.getElementById('specAnnees'),
        specLIn: document.getElementById('specLIn'),
        specLCm: document.getElementById('specLCm'),
        specWIn: document.getElementById('specWIn'),
        specWCm: document.getElementById('specWCm'),
        specHIn: document.getElementById('specHIn'),
        specHCm: document.getElementById('specHCm'),
        specRIn: document.getElementById('specRIn'),
        specRCm: document.getElementById('specRCm'),
        specStatusBadge: document.getElementById('specStatusBadge'),
        specAuditNotes: document.getElementById('specAuditNotes'),
        // Timeline Tab
        timelineContainer: document.getElementById('timelineContainer'),
        waybackVintageContainer: document.getElementById('waybackVintageContainer'),
        waybackTrackingBadge: document.getElementById('waybackTrackingBadge'),
        // Assets Tab
        galleryTopImg: document.getElementById('galleryTopImg'),
        galleryTopFallback: document.getElementById('galleryTopFallback'),
        galleryTopBadge: document.getElementById('galleryTopBadge'),
        galleryTopLink: document.getElementById('galleryTopLink'),
        gallerySideImg: document.getElementById('gallerySideImg'),
        gallerySideFallback: document.getElementById('gallerySideFallback'),
        gallerySideBadge: document.getElementById('gallerySideBadge'),
        gallerySideLink: document.getElementById('gallerySideLink'),
        assetLinksContainer: document.getElementById('assetLinksContainer'),
        sourceUrlsContainer: document.getElementById('sourceUrlsContainer')
      };

      // Initialization
      async function init() {
        if (window.SPAFIT_CATALOG_DATA && window.SPAFIT_CATALOG_DATA.spas) {
          state.spas = window.SPAFIT_CATALOG_DATA.spas;
          state.spafitModels = window.SPAFIT_CATALOG_DATA.cover_models || [];
          finishInit();
        } else {
          try {
            const resp = await fetch('data/spas_catalog_data.json');
            const data = await resp.json();
            state.spas = data.spas;
            state.spafitModels = data.cover_models || [];
            finishInit();
          } catch (e) {
            console.error('Failed to load catalog data:', e);
            document.body.innerHTML = '<div class="p-8 text-center text-rose-400">Error loading data/spas_catalog_data.js. Ensure file exists.</div>';
          }
        }
      }

      function finishInit() {
        const total = state.spas.length;
        const withPhotos = state.spas.filter(s => hasTopImage(s)).length;
        const hotTubs = state.spas.filter(s => !s.Segment || !s.Segment.toLowerCase().includes('nage')).length;
        const swimSpas = total - hotTubs;

        const oasisCount = state.spas.filter(s => (s.cover_compatible || []).some(m => m.includes('oasis'))).length;
        const horizonCount = state.spas.filter(s => (s.cover_compatible || []).some(m => m.includes('horizon'))).length;
        const evoCount = state.spas.filter(s => (s.cover_compatible || []).some(m => m.includes('evolution'))).length;
        const legCount = state.spas.filter(s => (s.cover_compatible || []).some(m => m.includes('legend') || m.includes('endless'))).length;
        const cadCount = state.spas.filter(s => s.cad_svg_contour || (s.cad_dwg_file && s.cad_dwg_file !== 'N/A')).length;
        const anyCount = state.spas.filter(s => (s.cover_compatible || []).length > 0).length;

        if (els.badgePhotoCount) els.badgePhotoCount.textContent = withPhotos.toLocaleString();
        const navBadge = document.getElementById('navSpaCountBadge');
        if (navBadge) navBadge.textContent = `${total.toLocaleString()} Spas`;

        const btnAll = document.getElementById('segBtnAll');
        if (btnAll) btnAll.textContent = `All (${total.toLocaleString()})`;
        const btnHt = document.getElementById('segBtnHotTub');
        if (btnHt) btnHt.textContent = `Hot Tub (${hotTubs.toLocaleString()})`;
        const btnSs = document.getElementById('segBtnSwimSpa');
        if (btnSs) btnSs.textContent = `Swim Spa (${swimSpas.toLocaleString()})`;

        const bOasis = document.getElementById('badgeOasisCount');
        if (bOasis) bOasis.textContent = oasisCount;
        const bHoriz = document.getElementById('badgeHorizonCount');
        if (bHoriz) bHoriz.textContent = horizonCount;
        const bEvo = document.getElementById('badgeEvoCount');
        if (bEvo) bEvo.textContent = evoCount;
        const bLeg = document.getElementById('badgeLegendCount');
        if (bLeg) bLeg.textContent = legCount;
        const bCad = document.getElementById('badgeCadCount');
        if (bCad) bCad.textContent = cadCount;
        const bAny = document.getElementById('badgeAnyCovCount');
        if (bAny) bAny.textContent = anyCount;

        populateFilters();
        populateSpaFitSimulatorDropdown();
        bindEvents();
        applyFilters();
      }

      function hasTopImage(spa) {
        return (spa.image_top_file && spa.image_top_file !== 'N/A' && spa.image_top_file !== '') ||
               (spa.image_top_source_url && spa.image_top_source_url !== 'N/A' && spa.image_top_source_url.startsWith('http'));
      }

      function getTopImageSrc(spa) {
        if (spa.image_top_file && spa.image_top_file !== 'N/A' && spa.image_top_file !== '') {
          return spa.image_top_file;
        }
        if (spa.image_top_source_url && spa.image_top_source_url !== 'N/A' && spa.image_top_source_url.startsWith('http')) {
          return spa.image_top_source_url;
        }
        return null;
      }

      // Populate Brand & Series Filters
      function populateFilters() {
        const brands = {};
        state.spas.forEach(s => {
          const b = s.Marque || 'Unknown';
          brands[b] = (brands[b] || 0) + 1;
        });

        const sortedBrands = Object.keys(brands).sort((a,b) => a.localeCompare(b));
        const activeBrandEl = document.getElementById('activeBrandCount');
        if (activeBrandEl) activeBrandEl.textContent = `${sortedBrands.length} Brands`;
        els.brandSelect.innerHTML = '<option value="all">All Manufacturers (' + state.spas.length + ' Spas)</option>';
        sortedBrands.forEach(b => {
          const opt = document.createElement('option');
          opt.value = b;
          opt.textContent = `${b} (${brands[b]})`;
          els.brandSelect.appendChild(opt);
        });

        updateSeriesOptions('all');
      }

      function updateSeriesOptions(brand) {
        const seriesSet = new Set();
        state.spas.forEach(s => {
          if (brand === 'all' || s.Marque === brand) {
            if (s.Serie_Collection && s.Serie_Collection !== 'N/A') {
              seriesSet.add(s.Serie_Collection);
            }
          }
        });

        const sortedSeries = Array.from(seriesSet).sort();
        els.seriesSelect.innerHTML = '<option value="all">All Collections / Series (' + sortedSeries.length + ')</option>';
        sortedSeries.forEach(ser => {
          const opt = document.createElement('option');
          opt.value = ser;
          opt.textContent = ser;
          els.seriesSelect.appendChild(opt);
        });
      }

      function populateSpaFitSimulatorDropdown() {
        els.spafitModelSelect.innerHTML = '';
        const byGamme = {};
        state.spafitModels.forEach(m => {
          const g = m.gamme || 'Other';
          if (!byGamme[g]) byGamme[g] = [];
          byGamme[g].push(m);
        });

        Object.keys(byGamme).forEach(g => {
          const grp = document.createElement('optgroup');
          grp.label = `Gamme ${g}`;
          byGamme[g].forEach(m => {
            const opt = document.createElement('option');
            opt.value = m.id;
            opt.textContent = `${m.nom} (${m.degagement_colonnes.longueur}" × ${m.degagement_colonnes.largeur}")`;
            grp.appendChild(opt);
          });
          els.spafitModelSelect.appendChild(grp);
        });

        if (state.spafitModels.length > 0) {
          state.activeSpaFitModelId = state.spafitModels[0].id;
        }
      }

      // Filtering Logic
      function applyFilters() {
        const query = state.searchTerm.toLowerCase().trim();
        const brand = state.selectedBrand;
        const series = state.selectedSeries;
        const gen = state.selectedGen;
        const seg = state.selectedSegment;
        const cov = state.selectedSpaFitFilter;
        const rPreset = state.radiusPreset;
        const maxL = state.maxLength;
        const maxW = state.maxWidth;
        const photosOnly = state.onlyWithPhotos;

        state.filteredSpas = state.spas.filter(s => {
          // Photo filter
          if (photosOnly && !hasTopImage(s)) return false;

          // Search term across brand, model, series, chassis, notes
          if (query) {
            const text = `${s.Marque} ${s.Modele} ${s.Serie_Collection} ${s.Sous_Modele_ou_Version} ${s.Code_Usine_Chassis} ${s.Annees_Production}`.toLowerCase();
            if (!text.includes(query)) return false;
          }

          // Brand
          if (brand !== 'all' && s.Marque !== brand) return false;

          // Series
          if (series !== 'all' && s.Serie_Collection !== series) return false;

          // Generation
          if (gen !== 'all') {
            if (!s.Generation || !s.Generation.toLowerCase().includes(gen.toLowerCase())) return false;
          }

          // Segment (Hot tub vs Swim spa)
          if (seg === 'hot_tub' && s.Segment && s.Segment.toLowerCase().includes('nage')) return false;
          if (seg === 'swim_spa' && s.Segment && !s.Segment.toLowerCase().includes('nage')) return false;

          // SpaFit filter
          if (cov === 'oasis') {
            if (!s.cover_compatible || !s.cover_compatible.some(m => m.includes('oasis'))) return false;
          } else if (cov === 'horizon') {
            if (!s.cover_compatible || !s.cover_compatible.some(m => m.includes('horizon'))) return false;
          } else if (cov === 'evolution') {
            if (!s.cover_compatible || !s.cover_compatible.some(m => m.includes('evolution'))) return false;
          } else if (cov === 'legend') {
            if (!s.cover_compatible || !s.cover_compatible.some(m => m.includes('legend') || m.includes('endless'))) return false;
          } else if (cov === 'cad') {
            if (!s.cad_svg_contour && (!s.cad_dwg_file || s.cad_dwg_file === 'N/A')) return false;
          } else if (cov === 'any') {
            if (!s.cover_compatible || s.cover_compatible.length === 0) return false;
          }

          // Corner radius preset
          const r = parseFloat(s.corner_radius_in) || 0;
          if (rPreset === 'square' && r !== 0) return false;
          if (rPreset === 'crisp' && (r < 2.0 || r > 4.0)) return false;
          if (rPreset === 'classic' && (r < 4.5 || r > 8.5)) return false;
          if (rPreset === 'wide' && (r < 9.0 || r > 16.0)) return false;
          if (rPreset === 'round' && r < 20.0) return false;

          // Dimensions slider
          const l = parseFloat(s.length_in) || 0;
          const w = parseFloat(s.width_in) || 0;
          if (l > 0 && l > maxL) return false;
          if (w > 0 && w > maxW) return false;

          return true;
        });

        // Apply Sorting
        sortResults();

        // Render Active View
        renderResults();
        renderActiveFilterTags();
      }

      function sortResults() {
        const sort = state.sortBy;
        state.filteredSpas.sort((a, b) => {
          if (sort === 'brand_asc') {
            const cmp = (a.Marque || '').localeCompare(b.Marque || '');
            return cmp !== 0 ? cmp : (a.Modele || '').localeCompare(b.Modele || '');
          }
          if (sort === 'model_asc') {
            return (a.Modele || '').localeCompare(b.Modele || '');
          }
          if (sort === 'length_desc') {
            return (parseFloat(b.length_in) || 0) - (parseFloat(a.length_in) || 0);
          }
          if (sort === 'length_asc') {
            return (parseFloat(a.length_in) || 0) - (parseFloat(b.length_in) || 0);
          }
          if (sort === 'radius_asc') {
            return (parseFloat(a.corner_radius_in) || 0) - (parseFloat(b.corner_radius_in) || 0);
          }
          if (sort === 'radius_desc') {
            return (parseFloat(b.corner_radius_in) || 0) - (parseFloat(a.corner_radius_in) || 0);
          }
          if (sort === 'year_desc') {
            return (b.Annees_Production || '').localeCompare(a.Annees_Production || '');
          }
          return 0;
        });
      }

      function renderResults() {
        els.resultsCount.textContent = state.filteredSpas.length;

        if (state.filteredSpas.length === 0) {
          els.catalogGridContainer.classList.add('hidden');
          els.catalogTableContainer.classList.add('hidden');
          els.catalogCompareContainer.classList.add('hidden');
          els.emptyState.classList.remove('hidden');
          return;
        }

        els.emptyState.classList.add('hidden');

        if (state.viewMode === 'grid') {
          els.catalogGridContainer.classList.remove('hidden');
          els.catalogTableContainer.classList.add('hidden');
          els.catalogCompareContainer.classList.add('hidden');
          renderGridView();
        } else if (state.viewMode === 'table') {
          els.catalogGridContainer.classList.add('hidden');
          els.catalogTableContainer.classList.remove('hidden');
          els.catalogCompareContainer.classList.add('hidden');
          renderTableView();
        } else if (state.viewMode === 'compare') {
          els.catalogGridContainer.classList.add('hidden');
          els.catalogTableContainer.classList.add('hidden');
          els.catalogCompareContainer.classList.remove('hidden');
          renderCompareView();
        }
      }

      // Generate accurate 2D SVG Blueprint
      function createSpaBlueprintSvg(spa, widthPx = 280, heightPx = 180, showOverlays = true) {
        const lIn = parseFloat(spa.length_in) || 84;
        const wIn = parseFloat(spa.width_in) || 84;
        const rIn = parseFloat(spa.corner_radius_in) || 0;

        // ViewBox sizing with padding for dimension leaders
        const pad = 24;
        const maxDim = Math.max(lIn, wIn);
        const scale = (Math.min(widthPx, heightPx) - pad * 2) / (maxDim || 1);

        const svgL = lIn * scale;
        const svgW = wIn * scale;
        const svgR = Math.min(rIn * scale, Math.min(svgL, svgW) / 2);

        const startX = (widthPx - svgL) / 2;
        const startY = (heightPx - svgW) / 2;

        // SVG Path for Rounded Corner Rectangle
        let pathD = '';
        if (svgR <= 0.5) {
          pathD = `M ${startX} ${startY} h ${svgL} v ${svgW} h ${-svgL} Z`;
        } else if (svgR >= Math.min(svgL, svgW) / 2 - 0.5 && Math.abs(svgL - svgW) < 2) {
          // Pure Circle
          const cx = startX + svgL / 2;
          const cy = startY + svgW / 2;
          const rad = svgL / 2;
          pathD = `M ${cx - rad} ${cy} a ${rad} ${rad} 0 1 0 ${rad * 2} 0 a ${rad} ${rad} 0 1 0 ${-rad * 2} 0 Z`;
        } else {
          pathD = `
            M ${startX + svgR} ${startY}
            L ${startX + svgL - svgR} ${startY}
            A ${svgR} ${svgR} 0 0 1 ${startX + svgL} ${startY + svgR}
            L ${startX + svgL} ${startY + svgW - svgR}
            A ${svgR} ${svgR} 0 0 1 ${startX + svgL - svgR} ${startY + svgW}
            L ${startX + svgR} ${startY + svgW}
            A ${svgR} ${svgR} 0 0 1 ${startX} ${startY + svgW - svgR}
            L ${startX} ${startY + svgR}
            A ${svgR} ${svgR} 0 0 1 ${startX + svgR} ${startY}
            Z
          `;
        }

        // SpaFit Columns & Seal Overlay (if Oasis is selected/fits)
        let overlaySvg = '';
        if (showOverlays && state.showLayerSpaFit) {
          const colL = 98.0 * scale;
          const colW = 93.0 * scale;
          const colX = (widthPx - colL) / 2;
          const colY = (heightPx - colW) / 2;
          const postSize = 6 * scale;

          overlaySvg = `
            <!-- SpaFit Column Posts Footprint -->
            <rect x="${colX}" y="${colY}" width="${colL}" height="${colW}" fill="none" stroke="#0099D8" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.6"/>
            <!-- 4 Posts -->
            <rect x="${colX - postSize/2}" y="${colY - postSize/2}" width="${postSize}" height="${postSize}" fill="#0099D8" opacity="0.8" rx="1"/>
            <rect x="${colX + colL - postSize/2}" y="${colY - postSize/2}" width="${postSize}" height="${postSize}" fill="#0099D8" opacity="0.8" rx="1"/>
            <rect x="${colX - postSize/2}" y="${colY + colW - postSize/2}" width="${postSize}" height="${postSize}" fill="#0099D8" opacity="0.8" rx="1"/>
            <rect x="${colX + colL - postSize/2}" y="${colY + colW - postSize/2}" width="${postSize}" height="${postSize}" fill="#0099D8" opacity="0.8" rx="1"/>
          `;
        }

        return `
          <svg viewBox="0 0 ${widthPx} ${heightPx}" class="w-full h-full select-none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="spaGrad_${spa.id}" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#1E3250" stop-opacity="0.85"/>
                <stop offset="100%" stop-color="#0F1A2E" stop-opacity="0.95"/>
              </linearGradient>
            </defs>
            
            ${overlaySvg}

            <!-- Spa Shell Outer Rim -->
            <path d="${pathD}" fill="url(#spaGrad_${spa.id})" stroke="#38BDF8" stroke-width="2" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.5))"/>
            
            <!-- Acrylic Inner Basin Recess -->
            <path d="${pathD}" fill="none" stroke="#1E3250" stroke-width="6" transform="scale(0.92) translate(${widthPx * 0.04}, ${heightPx * 0.04})" opacity="0.6"/>

            <!-- Center Center Mark -->
            <circle cx="${widthPx/2}" cy="${heightPx/2}" r="3" fill="#38BDF8" opacity="0.5"/>
            <line x1="${widthPx/2 - 8}" y1="${heightPx/2}" x2="${widthPx/2 + 8}" y2="${heightPx/2}" stroke="#38BDF8" stroke-width="0.75" opacity="0.5"/>
            <line x1="${widthPx/2}" y1="${heightPx/2 - 8}" x2="${widthPx/2}" y2="${heightPx/2 + 8}" stroke="#38BDF8" stroke-width="0.75" opacity="0.5"/>
          </svg>
        `;
      }

      window.createSpaBlueprintSvgFallback = function(id) {
        const spa = (state.spas || []).find(s => s.id === id);
        if (!spa) return '<div class="text-xs text-slate-500 flex items-center justify-center h-full">Image unavailable</div>';
        return createSpaBlueprintSvg(spa, 230, 140, true);
      };

      // Render Grid Cards
      function renderGridView() {
        els.catalogGridContainer.innerHTML = '';
        
        state.filteredSpas.forEach(spa => {
          const isPinned = state.pinnedIds.has(spa.id);
          const card = document.createElement('div');
          card.className = 'glass-panel rounded-xl p-4 flex flex-col justify-between hover:border-spafit-cyan/60 hover:shadow-lg hover:shadow-spafit-blue/10 transition-all duration-200 group relative';

          // Dimensions labels based on unit
          const lStr = state.unit === 'in' ? `${spa.length_in}"` : `${spa.length_cm} cm`;
          const wStr = state.unit === 'in' ? `${spa.width_in}"` : `${spa.width_cm} cm`;
          const hStr = state.unit === 'in' ? `${spa.height_in}"` : `${spa.height_cm} cm`;
          const rStr = state.unit === 'in' ? `${spa.corner_radius_in}"` : `${spa.corner_radius_cm} cm`;

          // Determine card media mode: photo vs blueprint
          const imgSrc = getTopImageSrc(spa);
          const spaCardMode = state.cardFlipMap[spa.id] || (imgSrc && state.cardMediaMode === 'photo' ? 'photo' : 'bp');

          let mediaContentHtml = '';
          if (spaCardMode === 'photo' && imgSrc) {
            mediaContentHtml = `
              <div class="w-full h-44 rounded-lg bg-spafit-dark/90 border border-spafit-border p-2 flex items-center justify-center relative overflow-hidden group-hover:border-spafit-cyan/40 transition-colors">
                <img src="${imgSrc}" alt="${spa.Modele} Top View" class="max-h-full max-w-full object-contain rounded drop-shadow-md transition-transform duration-300 group-hover:scale-105" loading="lazy" onerror="this.parentElement.innerHTML = createSpaBlueprintSvgFallback(${spa.id});">
                <span class="absolute top-2 left-2 text-[10px] font-mono font-bold text-emerald-300 bg-spafit-dark/90 px-2 py-0.5 rounded border border-spafit-border flex items-center gap-1 shadow">
                  <svg class="w-3 h-3 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path></svg>
                  Top View Photo
                </span>
                <span class="absolute top-2 right-2 text-[10px] font-mono font-bold text-spafit-cyan bg-spafit-dark/90 px-1.5 py-0.5 rounded border border-spafit-border shadow">R: ${rStr}</span>
                
                <!-- Flip to Blueprint Button -->
                <button data-flip-card="${spa.id}" class="absolute bottom-2 right-2 px-2 py-1 rounded bg-spafit-dark/95 border border-spafit-border text-[10px] font-mono text-slate-300 hover:text-white hover:border-spafit-cyan transition-colors flex items-center gap-1 shadow" title="Flip to 2D CAD Blueprint">
                  <svg class="w-3 h-3 text-spafit-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                  <span>Blueprint</span>
                </button>
              </div>
            `;
          } else {
            mediaContentHtml = `
              <div class="w-full h-44 rounded-lg bg-spafit-dark/80 border border-spafit-border grid-blueprint p-2 flex items-center justify-center relative overflow-hidden group-hover:border-spafit-cyan/40 transition-colors">
                ${createSpaBlueprintSvg(spa, 230, 140, true)}
                <span class="absolute top-2 left-2 text-[10px] font-mono font-bold text-spafit-cyan bg-spafit-dark/90 px-1.5 py-0.5 rounded border border-spafit-border">R: ${rStr}</span>
                <span class="absolute bottom-2 left-2 text-[10px] font-mono text-slate-300 bg-spafit-dark/90 px-1.5 py-0.5 rounded border border-spafit-border">${lStr} × ${wStr}</span>
                
                ${imgSrc ? `
                <!-- Flip to Photo Button -->
                <button data-flip-card="${spa.id}" class="absolute bottom-2 right-2 px-2 py-1 rounded bg-spafit-dark/95 border border-spafit-border text-[10px] font-mono text-emerald-300 hover:text-white hover:border-emerald-400 transition-colors flex items-center gap-1 shadow" title="Flip to Real Overhead Photo">
                  <svg class="w-3 h-3 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path></svg>
                  <span>Photo</span>
                </button>
                ` : `
                <span class="absolute bottom-2 right-2 text-[9px] font-mono text-slate-500 bg-spafit-dark/80 px-1.5 py-0.5 rounded">Photo N/A</span>
                `}
              </div>
            `;
          }

          // SpaFit fit badges
          let spafitBadges = '';
          if (spa.cover_compatible && spa.cover_compatible.length > 0) {
            const hasOasis = spa.cover_compatible.some(m => m.includes('oasis'));
            const hasHorizon = spa.cover_compatible.some(m => m.includes('horizon'));
            const hasEvo = spa.cover_compatible.some(m => m.includes('evolution'));
            const hasLegend = spa.cover_compatible.some(m => m.includes('legend') || m.includes('endless'));
            
            if (hasOasis) spafitBadges += `<span class="px-2 py-0.5 rounded bg-spafit-blue/30 text-spafit-accent border border-spafit-blue/40 text-[10px] font-bold">Oasis</span>`;
            if (hasHorizon) spafitBadges += `<span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 text-[10px] font-bold">Horizon</span>`;
            if (hasEvo) spafitBadges += `<span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[10px] font-bold">Evolution</span>`;
            if (hasLegend) spafitBadges += `<span class="px-2 py-0.5 rounded bg-purple-500/20 text-purple-400 border border-purple-500/30 text-[10px] font-bold">Legend</span>`;
            if (spa.cad_svg_contour) {
              spafitBadges += `<span class="px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 text-[10px] font-bold">CAD 2D SVG</span>`;
            }
          } else {
            spafitBadges = `<span class="px-2 py-0.5 rounded bg-slate-800 text-slate-400 text-[10px]">No Direct Fit</span>`;
          }

          card.innerHTML = `
            <div>
              <!-- Card Header -->
              <div class="flex items-start justify-between gap-2 mb-2">
                <div>
                  <span class="text-[11px] font-bold tracking-wider uppercase text-spafit-accent">${spa.Marque}</span>
                  <h3 class="text-base font-bold text-white group-hover:text-spafit-cyan transition-colors leading-tight">${spa.Modele}</h3>
                  <p class="text-[11px] text-slate-400 font-medium">${spa.Serie_Collection || ''}</p>
                </div>
                
                <!-- Pin for Compare Button -->
                <button data-spa-id="${spa.id}" class="pin-btn p-1.5 rounded-lg border text-xs transition-all ${isPinned ? 'bg-spafit-cyan text-white border-spafit-cyan' : 'bg-spafit-card border-spafit-border text-slate-400 hover:text-white'}" title="${isPinned ? 'Remove from compare' : 'Pin to compare'}">
                  <svg class="w-3.5 h-3.5" fill="${isPinned ? 'currentColor' : 'none'}" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path></svg>
                </button>
              </div>

              <!-- Generation / Vintage Pill -->
              <div class="flex items-center gap-2 mb-2.5">
                <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 font-semibold">${spa.Generation || 'Standard'}</span>
                <span class="text-[10px] font-mono text-slate-400">${spa.Annees_Production || ''}</span>
              </div>

              <!-- Media Content Container (Photo or Blueprint) -->
              ${mediaContentHtml}

              <!-- Dimensions & Height Strip -->
              <div class="mt-3 grid grid-cols-2 gap-2 text-[11px] font-mono bg-spafit-dark/70 p-2 rounded-lg border border-spafit-border">
                <div>
                  <span class="text-slate-400 text-[10px] block">Dimensions:</span>
                  <span class="text-slate-100 font-semibold">${lStr} × ${wStr}</span>
                </div>
                <div>
                  <span class="text-slate-400 text-[10px] block">Height | Radius:</span>
                  <span class="text-slate-100 font-semibold">${hStr} | <span class="text-spafit-cyan font-bold">${rStr}</span></span>
                </div>
              </div>

              <!-- SpaFit Fit Badges -->
              <div class="mt-2.5 flex flex-wrap gap-1">
                ${spafitBadges}
              </div>
            </div>

            <!-- Card Action Footer -->
            <div class="mt-4 pt-3 border-t border-spafit-border/80 flex items-center justify-between gap-2">
              <button data-open-modal="${spa.id}" data-target-tab="visual" class="flex-1 py-1.5 px-3 rounded-lg bg-spafit-card border border-spafit-border hover:bg-spafit-cardhover hover:border-slate-400 text-xs text-slate-200 font-medium transition-all flex items-center justify-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-spafit-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
                <span>View Photos & Plan</span>
              </button>
              <button data-open-modal="${spa.id}" data-target-tab="spafit" class="py-1.5 px-3 rounded-lg bg-spafit-blue hover:bg-spafit-cyan text-xs text-white font-semibold shadow transition-all flex items-center gap-1" title="Simulate SpaFit Sizer Compatibility">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
                <span>Simulate</span>
              </button>
            </div>
          `;

          els.catalogGridContainer.appendChild(card);
        });

        bindCardEvents();
      }

      // Render Detailed Table View
      function renderTableView() {
        els.catalogTableBody.innerHTML = '';
        state.filteredSpas.forEach((spa) => {
          const tr = document.createElement('tr');
          tr.className = 'hover:bg-spafit-card/60 transition-colors cursor-pointer group';
          tr.setAttribute('data-open-modal', spa.id);

          const lStr = state.unit === 'in' ? `${spa.length_in}"` : `${spa.length_cm} cm`;
          const wStr = state.unit === 'in' ? `${spa.width_in}"` : `${spa.width_cm} cm`;
          const hStr = state.unit === 'in' ? `${spa.height_in}"` : `${spa.height_cm} cm`;
          const rStr = state.unit === 'in' ? `${spa.corner_radius_in}"` : `${spa.corner_radius_cm} cm`;

          // Top Image Thumb
          const imgSrc = getTopImageSrc(spa);
          const thumbHtml = imgSrc ? `
            <div class="w-12 h-10 rounded bg-spafit-dark/80 border border-spafit-border flex items-center justify-center p-0.5 overflow-hidden">
              <img src="${imgSrc}" alt="${spa.Modele}" class="max-h-full max-w-full object-contain">
            </div>
          ` : `
            <div class="w-12 h-10 rounded bg-spafit-dark/80 border border-spafit-border flex items-center justify-center text-[10px] text-slate-500 font-mono">
              Plan
            </div>
          `;

          // SpaFit fit pill
          let covPill = '<span class="text-slate-500">—</span>';
          if (spa.cover_compatible && spa.cover_compatible.length > 0) {
            const topModel = spa.cover_compatible[0].replace('oasis-', 'Oasis ').replace('evolution-', 'Evo ').replace('legend-', 'Legend ');
            covPill = `<span class="px-2 py-0.5 rounded bg-spafit-blue/20 text-spafit-accent border border-spafit-blue/30 font-bold font-mono text-[10px]">${topModel} (+${spa.cover_compatible.length - 1})</span>`;
          }

          tr.innerHTML = `
            <td class="p-3 font-mono text-slate-400">${spa.id}</td>
            <td class="p-2">${thumbHtml}</td>
            <td class="p-3 font-semibold text-white">${spa.Marque}</td>
            <td class="p-3">
              <div class="font-bold text-slate-100 group-hover:text-spafit-cyan">${spa.Modele}</div>
              <div class="text-[11px] text-slate-400">${spa.Serie_Collection || ''}</div>
            </td>
            <td class="p-3 font-mono text-slate-300">
              <div>${spa.Generation || 'Standard'}</div>
              <div class="text-[10px] text-slate-400">${spa.Annees_Production || ''}</div>
            </td>
            <td class="p-3 font-mono text-slate-200">
              <span class="font-semibold">${lStr} × ${wStr}</span> × ${hStr}
            </td>
            <td class="p-3 font-mono font-bold text-spafit-cyan">
              ${rStr}
            </td>
            <td class="p-3">
              ${covPill}
            </td>
            <td class="p-3 text-right">
              <button class="px-2.5 py-1 rounded bg-spafit-card border border-spafit-border group-hover:border-spafit-cyan text-xs font-semibold text-spafit-accent hover:bg-spafit-blue hover:text-white transition-all">Inspect</button>
            </td>
          `;

          els.catalogTableBody.appendChild(tr);
        });

        // Click row to open modal
        els.catalogTableBody.querySelectorAll('tr').forEach(tr => {
          tr.addEventListener('click', () => {
            const spaId = parseInt(tr.getAttribute('data-open-modal'));
            openModal(spaId, 'visual');
          });
        });
      }

      // Render Pinned Comparison View
      function renderCompareView() {
        els.compareCardsGrid.innerHTML = '';
        const pinnedList = state.spas.filter(s => state.pinnedIds.has(s.id));

        if (pinnedList.length === 0) {
          els.compareCardsGrid.innerHTML = `
            <div class="col-span-full py-12 text-center space-y-3">
              <div class="w-12 h-12 mx-auto rounded-full bg-spafit-card border border-spafit-border text-slate-400 flex items-center justify-center">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path></svg>
              </div>
              <h3 class="text-base font-bold text-white">No Spas Pinned for Comparison</h3>
              <p class="text-xs text-slate-400 max-w-sm mx-auto">Click the bookmark pin icon on any spa card to pin up to 6 models for comparative photographic and SpaFit sizing analysis.</p>
            </div>
          `;
          return;
        }

        pinnedList.forEach(spa => {
          const card = document.createElement('div');
          card.className = 'glass-panel rounded-xl p-5 space-y-4 border border-spafit-border relative';

          const lStr = state.unit === 'in' ? `${spa.length_in}"` : `${spa.length_cm} cm`;
          const wStr = state.unit === 'in' ? `${spa.width_in}"` : `${spa.width_cm} cm`;
          const hStr = state.unit === 'in' ? `${spa.height_in}"` : `${spa.height_cm} cm`;
          const rStr = state.unit === 'in' ? `${spa.corner_radius_in}"` : `${spa.corner_radius_cm} cm`;
          const imgSrc = getTopImageSrc(spa);

          card.innerHTML = `
            <div class="flex items-start justify-between">
              <div>
                <span class="text-[10px] font-bold text-spafit-accent uppercase">${spa.Marque}</span>
                <h3 class="text-lg font-bold text-white">${spa.Modele}</h3>
                <span class="text-xs font-mono text-slate-400">${spa.Generation || ''} (${spa.Annees_Production || ''})</span>
              </div>
              <button data-unpin="${spa.id}" class="text-slate-400 hover:text-rose-400 p-1 transition-colors" title="Unpin">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
              </button>
            </div>

            <!-- Image or Blueprint -->
            <div class="w-full h-48 rounded-lg bg-spafit-dark/90 border border-spafit-border p-3 flex items-center justify-center relative overflow-hidden">
              ${imgSrc ? `
                <img src="${imgSrc}" alt="${spa.Modele}" class="max-h-full max-w-full object-contain rounded">
              ` : `
                ${createSpaBlueprintSvg(spa, 260, 160, true)}
              `}
            </div>

            <!-- Sizing specs list -->
            <div class="space-y-1.5 text-xs font-mono bg-spafit-card/60 p-3 rounded-lg border border-spafit-border">
              <div class="flex justify-between py-1 border-b border-spafit-border"><span class="text-slate-400">Dimensions:</span><span class="font-bold text-white">${lStr} × ${wStr}</span></div>
              <div class="flex justify-between py-1 border-b border-spafit-border"><span class="text-slate-400">Height:</span><span class="font-bold text-white">${hStr}</span></div>
              <div class="flex justify-between py-1 border-b border-spafit-border"><span class="text-slate-400 text-spafit-cyan">Corner Radius:</span><span class="font-bold text-spafit-cyan">${rStr}</span></div>
              <div class="flex justify-between py-1"><span class="text-slate-400">Chassis:</span><span class="text-slate-200">${spa.Code_Usine_Chassis || 'N/A'}</span></div>
            </div>

            <!-- SpaFit Fit List -->
            <div class="space-y-1">
              <span class="text-[11px] font-bold text-slate-300 block">Compatible SpaFit Models:</span>
              <div class="flex flex-wrap gap-1">
                ${(spa.cover_compatible || []).slice(0, 4).map(m => `<span class="px-2 py-0.5 rounded bg-spafit-blue/20 text-spafit-accent text-[10px] font-mono font-bold">${m.replace('oasis-', 'Oasis ').replace('evolution-', 'Evo ').replace('legend-', 'Legend ')}</span>`).join('')}
              </div>
            </div>

            <button data-open-modal="${spa.id}" data-target-tab="visual" class="w-full py-2 rounded-lg bg-spafit-blue hover:bg-spafit-cyan text-xs font-semibold text-white shadow transition-all">Inspect Photos & Simulation</button>
          `;

          els.compareCardsGrid.appendChild(card);
        });

        els.compareCardsGrid.querySelectorAll('[data-unpin]').forEach(btn => {
          btn.addEventListener('click', () => {
            const id = parseInt(btn.getAttribute('data-unpin'));
            togglePinSpa(id);
          });
        });

        els.compareCardsGrid.querySelectorAll('[data-open-modal]').forEach(btn => {
          btn.addEventListener('click', () => {
            const id = parseInt(btn.getAttribute('data-open-modal'));
            const tab = btn.getAttribute('data-target-tab') || 'visual';
            openModal(id, tab);
          });
        });
      }

      function renderActiveFilterTags() {
        els.activeFilterTags.innerHTML = '';
        const tags = [];

        if (state.onlyWithPhotos) tags.push({ label: '📷 Only With Photos', type: 'photo' });
        if (state.searchTerm) tags.push({ label: `"${state.searchTerm}"`, type: 'search' });
        if (state.selectedBrand !== 'all') tags.push({ label: state.selectedBrand, type: 'brand' });
        if (state.selectedSeries !== 'all') tags.push({ label: state.selectedSeries, type: 'series' });
        if (state.selectedGen !== 'all') tags.push({ label: state.selectedGen, type: 'gen' });
        if (state.selectedSegment !== 'all') tags.push({ label: state.selectedSegment === 'hot_tub' ? 'Hot Tubs' : 'Swim Spas', type: 'segment' });
        if (state.selectedSpaFitFilter !== 'all') tags.push({ label: `Fits ${state.selectedSpaFitFilter.toUpperCase()}`, type: 'spafit' });
        if (state.radiusPreset !== 'all') tags.push({ label: `R: ${state.radiusPreset}`, type: 'radius' });

        tags.forEach(t => {
          const pill = document.createElement('span');
          pill.className = 'inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-spafit-card border border-spafit-border text-xs text-spafit-accent';
          pill.innerHTML = `<span>${t.label}</span><button class="hover:text-rose-400 font-bold">&times;</button>`;
          pill.querySelector('button').addEventListener('click', () => removeFilter(t.type));
          els.activeFilterTags.appendChild(pill);
        });
      }

      function removeFilter(type) {
        if (type === 'photo') {
          state.onlyWithPhotos = false;
          els.onlyWithPhotosBtn.classList.remove('border-spafit-cyan', 'bg-spafit-cyan/15');
        } else if (type === 'search') {
          state.searchTerm = '';
          els.globalSearchInput.value = '';
          els.clearSearchBtn.classList.add('hidden');
        } else if (type === 'brand') {
          state.selectedBrand = 'all';
          els.brandSelect.value = 'all';
          updateSeriesOptions('all');
        } else if (type === 'series') {
          state.selectedSeries = 'all';
          els.seriesSelect.value = 'all';
        } else if (type === 'gen') {
          state.selectedGen = 'all';
          els.genSelect.value = 'all';
        } else if (type === 'segment') {
          state.selectedSegment = 'all';
          document.querySelectorAll('.segment-btn').forEach(b => {
            b.classList.toggle('active', b.getAttribute('data-segment') === 'all');
            b.classList.toggle('bg-spafit-blue', b.getAttribute('data-segment') === 'all');
            b.classList.toggle('text-white', b.getAttribute('data-segment') === 'all');
          });
        } else if (type === 'spafit') {
          state.selectedSpaFitFilter = 'all';
          document.querySelectorAll('.spafit-quick-btn').forEach(b => b.classList.remove('border-spafit-cyan', 'text-white'));
        } else if (type === 'radius') {
          state.radiusPreset = 'all';
          document.querySelectorAll('.radius-preset-btn').forEach(b => {
            const isAll = b.getAttribute('data-radius-preset') === 'all';
            b.classList.toggle('active', isAll);
            b.classList.toggle('bg-spafit-blue', isAll);
            b.classList.toggle('text-white', isAll);
          });
          els.radiusFilterLabel.textContent = 'All Radii';
        }
        applyFilters();
      }

      function togglePinSpa(id) {
        if (state.pinnedIds.has(id)) {
          state.pinnedIds.delete(id);
        } else {
          if (state.pinnedIds.size >= 6) {
            alert('You can pin up to 6 spas for comparison.');
            return;
          }
          state.pinnedIds.add(id);
        }
        updatePinnedBadge();
        renderResults();
      }

      function updatePinnedBadge() {
        const count = state.pinnedIds.size;
        if (count > 0) {
          els.pinnedBadge.textContent = count;
          els.pinnedBadge.classList.remove('hidden');
        } else {
          els.pinnedBadge.classList.add('hidden');
        }
      }

      // Detailed Modal Logic
      function openModal(spaId, targetTab = 'visual') {
        const spa = state.spas.find(s => s.id === spaId);
        if (!spa) return;
        state.activeSpa = spa;

        // Header info
        els.modalBrandBadge.textContent = spa.Marque;
        els.modalModelTitle.textContent = spa.Modele;
        els.modalGenBadge.textContent = `${spa.Generation || 'Gen'} (${spa.Annees_Production || ''})`;
        els.modalSubtitle.textContent = `${spa.Serie_Collection || ''} | Chassis Code: ${spa.Code_Usine_Chassis || 'N/A'} | ${spa.Groupe_Fabricant || ''}`;
        els.modalRowId.textContent = spa.id;
        els.modalProcessTime.textContent = spa.process_timestamp || 'Verified';
        if (els.modalOpenTracerLink) {
          els.modalOpenTracerLink.href = `index.html?spa_id=${spa.id}`;
        }

        // Pin button state
        updateModalPinButton();

        // 1. Populate Tab 1: Top View Photo & Blueprint
        renderModalVisualTab(spa);

        // 2. Populate Tab 2: SpaFit Simulator
        renderModalSpaFitTab(spa);

        // 3. Populate Tab 3: Specs
        renderModalSpecsTab(spa);

        // 4. Populate Tab 4: Timeline
        renderModalTimelineTab(spa);

        // 5. Populate Tab 5: Assets Gallery
        renderModalAssetsTab(spa);

        // Activate Tab
        switchModalTab(targetTab);

        // Show Modal
        els.spaModal.classList.remove('hidden');
      }

      function closeModal() {
        els.spaModal.classList.add('hidden');
        state.activeSpa = null;
      }

      function updateModalPinButton() {
        if (!state.activeSpa) return;
        const isPinned = state.pinnedIds.has(state.activeSpa.id);
        els.modalPinText.textContent = isPinned ? 'Pinned in Compare' : 'Pin for Compare';
        els.modalPinBtn.classList.toggle('bg-spafit-cyan', isPinned);
        els.modalPinBtn.classList.toggle('text-white', isPinned);
      }

      function switchModalTab(tabId) {
        document.querySelectorAll('.modal-tab-btn').forEach(btn => {
          const match = btn.getAttribute('data-tab') === tabId;
          btn.classList.toggle('active', match);
          btn.classList.toggle('border-spafit-cyan', match);
          btn.classList.toggle('text-white', match);
          btn.classList.toggle('border-transparent', !match);
          btn.classList.toggle('text-slate-400', !match);
        });

        document.querySelectorAll('.modal-tab-content').forEach(content => {
          content.classList.add('hidden');
        });

        const activeContent = document.getElementById(`tabContent${tabId.charAt(0).toUpperCase() + tabId.slice(1)}`);
        if (activeContent) activeContent.classList.remove('hidden');
      }

      function renderModalVisualTab(spa) {
        const lIn = parseFloat(spa.length_in) || 84;
        const wIn = parseFloat(spa.width_in) || 84;
        const hIn = parseFloat(spa.height_in) || 36;
        const rIn = parseFloat(spa.corner_radius_in) || 0;

        const diagIn = Math.sqrt(lIn * lIn + wIn * wIn);
        const perimIn = 2 * (lIn + wIn) - (8 - 2 * Math.PI) * rIn;

        els.bpLength.textContent = `${lIn.toFixed(1)}" (${(lIn * 2.54).toFixed(1)} cm)`;
        els.bpWidth.textContent = `${wIn.toFixed(1)}" (${(wIn * 2.54).toFixed(1)} cm)`;
        els.bpHeight.textContent = `${hIn.toFixed(1)}" (${(hIn * 2.54).toFixed(1)} cm)`;
        els.bpRadius.textContent = `${rIn.toFixed(1)}" (${(rIn * 2.54).toFixed(1)} cm)`;
        els.bpDiag.textContent = `${diagIn.toFixed(1)}" (${(diagIn * 2.54).toFixed(1)} cm)`;
        els.bpPerimeter.textContent = `${perimIn.toFixed(1)}" (${(perimIn * 2.54).toFixed(1)} cm)`;

        // Image Handling
        const imgSrc = getTopImageSrc(spa);
        if (imgSrc) {
          els.modalTopImg.src = imgSrc;
          els.modalTopImg.classList.remove('hidden');
          els.modalPhotoFallback.classList.add('hidden');
          els.modalImgExternalLink.href = imgSrc;
          els.modalImgExternalLink.classList.remove('hidden');
          els.modalSplitImg.src = imgSrc;
        } else {
          els.modalTopImg.classList.add('hidden');
          els.modalPhotoFallback.classList.remove('hidden');
          els.modalImgExternalLink.classList.add('hidden');
          els.modalSplitImg.src = '';
        }

        // SVG Blueprints
        els.modalSvgHolder.innerHTML = createSpaBlueprintSvg(spa, 460, 320, true);
        els.modalSplitSvgHolder.innerHTML = createSpaBlueprintSvg(spa, 230, 160, true);

        // SpaFit quick badges
        els.bpSpaFitQuickPills.innerHTML = (spa.cover_compatible || []).map(m => {
          return `<span class="px-2.5 py-1 rounded-full bg-spafit-blue/20 text-spafit-accent border border-spafit-blue/30 font-mono text-xs font-semibold">${m}</span>`;
        }).join('') || '<span class="text-xs text-slate-400">No standard SpaFit model fits this profile</span>';

        // Set visual mode based on availability
        if (imgSrc && state.modalVisualMode === 'photo') {
          setModalVisualMode('photo');
        } else if (state.modalVisualMode === 'split' && imgSrc) {
          setModalVisualMode('split');
        } else {
          setModalVisualMode('bp');
        }
      }

      function setModalVisualMode(mode) {
        state.modalVisualMode = mode;
        
        // Update sub toggle buttons
        els.modalSubTogglePhoto.className = mode === 'photo' ? 'px-3 py-1.5 rounded bg-spafit-blue text-white shadow transition-all flex items-center gap-1' : 'px-3 py-1.5 rounded text-slate-400 hover:text-white transition-all flex items-center gap-1';
        els.modalSubToggleBp.className = mode === 'bp' ? 'px-3 py-1.5 rounded bg-spafit-blue text-white shadow transition-all flex items-center gap-1' : 'px-3 py-1.5 rounded text-slate-400 hover:text-white transition-all flex items-center gap-1';
        els.modalSubToggleSplit.className = mode === 'split' ? 'px-3 py-1.5 rounded bg-spafit-blue text-white shadow transition-all flex items-center gap-1' : 'px-3 py-1.5 rounded text-slate-400 hover:text-white transition-all flex items-center gap-1';

        els.modalPhotoContainer.classList.toggle('hidden', mode !== 'photo');
        els.modalBpContainer.classList.toggle('hidden', mode !== 'bp');
        els.modalSplitContainer.classList.toggle('hidden', mode !== 'split');
      }

      function renderModalSpaFitTab(spa) {
        if (spa.cover_optimal && spa.cover_optimal.length > 0) {
          state.activeSpaFitModelId = spa.cover_optimal[0];
        } else if (spa.cover_compatible && spa.cover_compatible.length > 0) {
          state.activeSpaFitModelId = spa.cover_compatible[0];
        }
        els.spafitModelSelect.value = state.activeSpaFitModelId;
        executeSpaFitSimulation();
      }

      function executeSpaFitSimulation() {
        const spa = state.activeSpa;
        if (!spa) return;

        const modelId = els.spafitModelSelect.value;
        const covModel = state.spafitModels.find(m => m.id === modelId) || state.spafitModels[0];
        const orientation = els.spafitOrientationSelect.value;

        const lIn = parseFloat(spa.length_in) || 0;
        const wIn = parseFloat(spa.width_in) || 0;
        const hIn = parseFloat(spa.height_in) || 0;
        const rIn = parseFloat(spa.corner_radius_in) || 0;

        const testL = orientation === 'standard' ? Math.max(lIn, wIn) : Math.min(lIn, wIn);
        const testW = orientation === 'standard' ? Math.min(lIn, wIn) : Math.max(lIn, wIn);

        const cols = covModel.degagement_colonnes || {};
        const colL = cols.longueur || 98.0;
        const colW = cols.largeur || 93.0;

        const seal = covModel.joint_etancheite || {};
        const sLMin = seal.longueur_min || 0;
        const sLMax = seal.longueur_max || 999;
        const sWMin = seal.largeur_min || 0;
        const sWMax = seal.largeur_max || 999;
        const sRMin = seal.rayon_min || 4.0;
        const sRMax = seal.rayon_max || 16.0;

        const hSpec = covModel.hauteur || {};
        const hMin = hSpec.spa_min || 34.0;
        const hMax = hSpec.spa_max || 48.0;

        // Margin Calculations
        const marginX = (colL - testL) / 2.0;
        const marginY = (colW - testW) / 2.0;

        const colOk = marginX >= 0.5 && marginY >= 0.5;
        const sealOk = (testL >= sLMin && testL <= sLMax) && (testW >= sWMin && testW <= sWMax);
        const rOk = rIn >= sRMin && rIn <= sRMax;
        const hOk = hIn >= hMin && hIn <= hMax;

        const isOptimal = marginX >= 1.25 && marginY >= 1.25 && sealOk && rOk && hOk;
        const isCompatible = colOk && sealOk && hOk;

        // UI Diagnostics Banner
        if (isOptimal) {
          els.spafitDiagnosticBanner.className = 'p-4 rounded-xl border bg-emerald-500/10 border-emerald-500/30 text-emerald-300 flex items-start gap-3';
          els.spafitDiagnosticBanner.innerHTML = `
            <div class="w-8 h-8 rounded-lg bg-emerald-500/20 flex items-center justify-center shrink-0">
              <svg class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
            </div>
            <div>
              <div class="text-sm font-bold text-white">SPAFIT CERTIFIED — PERFECT FIT</div>
              <p class="text-xs text-emerald-200/90 mt-0.5">The ${spa.Marque} ${spa.Modele} provides optimal post clearance (&gt;1.25") and falls exactly within the primary perimeter seal contact band of the ${covModel.nom}.</p>
            </div>
          `;
        } else if (isCompatible) {
          els.spafitDiagnosticBanner.className = 'p-4 rounded-xl border bg-amber-500/10 border-amber-500/30 text-amber-300 flex items-start gap-3';
          els.spafitDiagnosticBanner.innerHTML = `
            <div class="w-8 h-8 rounded-lg bg-amber-500/20 flex items-center justify-center shrink-0">
              <svg class="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            </div>
            <div>
              <div class="text-sm font-bold text-white">ACCEPTABLE FIT WITH INSTALLATION ATTENTION</div>
              <p class="text-xs text-amber-200/90 mt-0.5">Clearance is tight (&lt;1.25" on post clearance or seal margin). Careful ground leveling and post alignment during installation is required.</p>
            </div>
          `;
        } else {
          els.spafitDiagnosticBanner.className = 'p-4 rounded-xl border bg-rose-500/10 border-rose-500/30 text-rose-300 flex items-start gap-3';
          els.spafitDiagnosticBanner.innerHTML = `
            <div class="w-8 h-8 rounded-lg bg-rose-500/20 flex items-center justify-center shrink-0">
              <svg class="w-5 h-5 text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </div>
            <div>
              <div class="text-sm font-bold text-white">INCOMPATIBLE WITH THIS SPAFIT MODEL</div>
              <p class="text-xs text-rose-200/90 mt-0.5">${marginX < 0.5 ? 'Post collision on Length axis. ' : ''}${marginY < 0.5 ? 'Post collision on Width axis. ' : ''}${!sealOk ? 'Spa rim falls outside the perimeter rubber seal landing strip. ' : ''}${!hOk ? 'Spa height is outside the operating stroke range. ' : ''}Try another SpaFit model or rotation.</p>
            </div>
          `;
        }

        // Margin X values
        els.simMarginX.textContent = `${marginX >= 0 ? '+' : ''}${marginX.toFixed(2)}"`;
        els.simStatusX.textContent = marginX >= 1.25 ? 'OPTIMAL' : (marginX >= 0.5 ? 'MARGINAL' : 'COLLISION');
        els.simStatusX.className = `text-[10px] font-bold px-1.5 py-0.5 rounded ${marginX >= 1.25 ? 'bg-emerald-500/20 text-emerald-400' : (marginX >= 0.5 ? 'bg-amber-500/20 text-amber-400' : 'bg-rose-500/20 text-rose-400')}`;
        els.simBarX.style.width = `${Math.max(10, Math.min(100, (marginX / 2.5) * 100))}%`;
        els.simBarX.className = `h-1.5 rounded-full ${marginX >= 1.25 ? 'bg-emerald-500' : (marginX >= 0.5 ? 'bg-amber-500' : 'bg-rose-500')}`;
        els.simDescX.textContent = `Clearance col: ${colL}" vs spa ${testL}"`;

        // Margin Y values
        els.simMarginY.textContent = `${marginY >= 0 ? '+' : ''}${marginY.toFixed(2)}"`;
        els.simStatusY.textContent = marginY >= 1.25 ? 'OPTIMAL' : (marginY >= 0.5 ? 'MARGINAL' : 'COLLISION');
        els.simStatusY.className = `text-[10px] font-bold px-1.5 py-0.5 rounded ${marginY >= 1.25 ? 'bg-emerald-500/20 text-emerald-400' : (marginY >= 0.5 ? 'bg-amber-500/20 text-amber-400' : 'bg-rose-500/20 text-rose-400')}`;
        els.simBarY.style.width = `${Math.max(10, Math.min(100, (marginY / 2.5) * 100))}%`;
        els.simBarY.className = `h-1.5 rounded-full ${marginY >= 1.25 ? 'bg-emerald-500' : (marginY >= 0.5 ? 'bg-amber-500' : 'bg-rose-500')}`;
        els.simDescY.textContent = `Clearance col: ${colW}" vs spa ${testW}"`;

        // Seal Landing values
        els.simSealCoverage.textContent = sealOk ? '100%' : 'Misaligned';
        els.simStatusSeal.textContent = sealOk ? 'COMPLIANT' : 'OUT OF SEAL';
        els.simStatusSeal.className = `text-[10px] font-bold px-1.5 py-0.5 rounded ${sealOk ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'}`;
        els.simBarSeal.style.width = sealOk ? '100%' : '30%';
        els.simBarSeal.className = `h-1.5 rounded-full ${sealOk ? 'bg-emerald-500' : 'bg-rose-500'}`;
        els.simDescSeal.textContent = `Range: [${sLMin}"-${sLMax}"] × [${sWMin}"-${sWMax}"]`;

        // Height values
        els.simHeightVal.textContent = `${hIn.toFixed(1)}"`;
        els.simStatusHeight.textContent = hOk ? 'PASSED' : 'OUT OF RANGE';
        els.simStatusHeight.className = `text-[10px] font-bold px-1.5 py-0.5 rounded ${hOk ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'}`;
        els.simBarHeight.style.width = hOk ? '75%' : '20%';
        els.simBarHeight.className = `h-1.5 rounded-full ${hOk ? 'bg-emerald-500' : 'bg-rose-500'}`;
        els.simDescHeight.textContent = `Operating Range: [${hMin}" - ${hMax}"]`;

        // Live Simulation SVG Footprint
        renderSimulationSvg(testL, testW, rIn, colL, colW, sLMin, sLMax, sWMin, sWMax);
      }

      function renderSimulationSvg(lIn, wIn, rIn, colL, colW, sLMin, sLMax, sWMin, sWMax) {
        const svgW = 420;
        const svgH = 240;
        const pad = 30;

        const maxDim = Math.max(lIn, wIn, colL, colW);
        const scale = (Math.min(svgW, svgH) - pad * 2) / (maxDim || 1);

        const spaL = lIn * scale;
        const spaW = wIn * scale;
        const spaR = Math.min(rIn * scale, Math.min(spaL, spaW) / 2);

        const spaX = (svgW - spaL) / 2;
        const spaY = (svgH - spaW) / 2;

        const cL = colL * scale;
        const cW = colW * scale;
        const cX = (svgW - cL) / 2;
        const cY = (svgH - cW) / 2;
        const post = 7 * scale;

        // Path for spa
        let spaPath = '';
        if (spaR <= 0.5) {
          spaPath = `M ${spaX} ${spaY} h ${spaL} v ${spaW} h ${-spaL} Z`;
        } else {
          spaPath = `
            M ${spaX + spaR} ${spaY}
            L ${spaX + spaL - spaR} ${spaY}
            A ${spaR} ${spaR} 0 0 1 ${spaX + spaL} ${spaY + spaR}
            L ${spaX + spaL} ${spaY + spaW - spaR}
            A ${spaR} ${spaR} 0 0 1 ${spaX + spaL - spaR} ${spaY + spaW}
            L ${spaX + spaR} ${spaY + spaW}
            A ${spaR} ${spaR} 0 0 1 ${spaX} ${spaY + spaW - spaR}
            L ${spaX} ${spaY + spaR}
            A ${spaR} ${spaR} 0 0 1 ${spaX + spaR} ${spaY}
            Z
          `;
        }

        els.simSvgContainer.innerHTML = `
          <svg viewBox="0 0 ${svgW} ${svgH}" class="w-full h-full select-none" xmlns="http://www.w3.org/2000/svg">
            <!-- SpaFit Column Frame Clearance -->
            <rect x="${cX}" y="${cY}" width="${cL}" height="${cW}" fill="none" stroke="#0099D8" stroke-width="1.5" stroke-dasharray="5,5" opacity="0.6"/>
            <!-- 4 Posts -->
            <rect x="${cX - post/2}" y="${cY - post/2}" width="${post}" height="${post}" fill="#0099D8" opacity="0.9" rx="1.5"/>
            <rect x="${cX + cL - post/2}" y="${cY - post/2}" width="${post}" height="${post}" fill="#0099D8" opacity="0.9" rx="1.5"/>
            <rect x="${cX - post/2}" y="${cY + cW - post/2}" width="${post}" height="${post}" fill="#0099D8" opacity="0.9" rx="1.5"/>
            <rect x="${cX + cL - post/2}" y="${cY + cW - post/2}" width="${post}" height="${post}" fill="#0099D8" opacity="0.9" rx="1.5"/>

            <!-- Spa Footprint -->
            <path d="${spaPath}" fill="#1E3250" stroke="#38BDF8" stroke-width="2" opacity="0.85"/>

            <!-- Dimension callouts -->
            <text x="${svgW/2}" y="${cY - 8}" fill="#0099D8" font-size="10" font-family="monospace" text-anchor="middle">SpaFit Col: ${colL.toFixed(1)}"</text>
            <text x="${svgW/2}" y="${spaY + spaW/2 + 3}" fill="#FFFFFF" font-size="11" font-family="monospace" font-weight="bold" text-anchor="middle">Spa: ${lIn.toFixed(1)}" × ${wIn.toFixed(1)}"</text>
          </svg>
        `;
      }

      function renderModalSpecsTab(spa) {
        els.specGroupe.textContent = spa.Groupe_Fabricant || 'N/A';
        els.specMarque.textContent = spa.Marque || 'N/A';
        els.specSegment.textContent = spa.Segment || 'N/A';
        els.specSerie.textContent = spa.Serie_Collection || 'N/A';
        els.specModele.textContent = spa.Modele || 'N/A';
        els.specSousModele.textContent = spa.Sous_Modele_ou_Version || 'N/A';
        els.specChassis.textContent = spa.Code_Usine_Chassis || 'N/A';
        els.specAnnees.textContent = spa.Annees_Production || 'N/A';

        els.specLIn.textContent = `${spa.length_in} in`;
        els.specLCm.textContent = `${spa.length_cm} cm`;
        els.specWIn.textContent = `${spa.width_in} in`;
        els.specWCm.textContent = `${spa.width_cm} cm`;
        els.specHIn.textContent = `${spa.height_in} in`;
        els.specHCm.textContent = `${spa.height_cm} cm`;
        els.specRIn.textContent = `${spa.corner_radius_in} in`;
        els.specRCm.textContent = `${spa.corner_radius_cm} cm`;

        els.specStatusBadge.textContent = spa.verification_status || 'VERIFIED_DUAL_SOURCE';
        els.specAuditNotes.textContent = spa.audit_notes || 'No audit notes registered.';
      }

      function renderModalTimelineTab(spa) {
        els.timelineContainer.innerHTML = '';
        
        // Find sibling generations of the same brand and model
        const siblings = state.spas.filter(s => s.Marque === spa.Marque && s.Modele === spa.Modele);

        if (siblings.length <= 1) {
          els.timelineContainer.innerHTML = `
            <div class="col-span-full py-6 text-center text-slate-400 text-xs">
              This model is documented as a single distinct generation in the master engineering database.
            </div>
          `;
        } else {
          siblings.sort((a,b) => (a.Generation || '').localeCompare(b.Generation || ''));

          siblings.forEach(sib => {
            const isCurrent = sib.id === spa.id;
            const card = document.createElement('div');
            card.className = `p-4 rounded-xl border transition-all ${isCurrent ? 'bg-spafit-blue/20 border-spafit-cyan shadow-lg shadow-spafit-blue/20' : 'bg-spafit-card/60 border-spafit-border'}`;

            const rIn = parseFloat(sib.corner_radius_in) || 0;
            const sibImg = getTopImageSrc(sib);

            card.innerHTML = `
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-bold font-mono ${isCurrent ? 'text-spafit-accent' : 'text-slate-200'}">${sib.Generation || 'Gen'}</span>
                ${isCurrent ? '<span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-spafit-cyan text-white">Active</span>' : ''}
              </div>
              <div class="text-[11px] font-mono text-slate-400 mb-2">${sib.Annees_Production || ''}</div>
              
              ${sibImg ? `
                <div class="w-full h-24 rounded bg-spafit-dark/80 border border-spafit-border mb-2 flex items-center justify-center p-1 overflow-hidden">
                  <img src="${sibImg}" alt="${sib.Modele}" class="max-h-full max-w-full object-contain">
                </div>
              ` : ''}

              <div class="space-y-1 text-xs font-mono">
                <div class="flex justify-between"><span class="text-slate-400">Dimensions:</span><span class="text-slate-100 font-semibold">${sib.length_in}" × ${sib.width_in}"</span></div>
                <div class="flex justify-between"><span class="text-slate-400">Height:</span><span class="text-slate-100">${sib.height_in}"</span></div>
                <div class="flex justify-between py-1 bg-spafit-dark/60 px-1.5 rounded border border-spafit-border">
                  <span class="text-spafit-cyan font-semibold">Corner Radius:</span>
                  <span class="font-bold text-spafit-cyan font-mono text-sm">R = ${rIn.toFixed(1)}"</span>
                </div>
              </div>

              <div class="mt-3 pt-2 border-t border-spafit-border text-[10px] text-slate-400 line-clamp-3">
                ${sib.audit_notes || 'Verified against OEM template'}
              </div>

              ${!isCurrent ? `<button class="w-full mt-3 py-1 px-2 rounded bg-spafit-card border border-spafit-border hover:bg-spafit-cardhover text-xs text-spafit-accent transition-colors" onclick="window.SPAFIT_APP.openModal(${sib.id}, 'timeline')">Switch to this Vintage</button>` : ''}
            `;

            els.timelineContainer.appendChild(card);
          });
        }

        // Render Wayback Machine 3-Year Generational Archive
        if (els.waybackVintageContainer) {
          els.waybackVintageContainer.innerHTML = '';
          let wbData = null;
          if (spa.wayback_vintage_links) {
            try {
              wbData = typeof spa.wayback_vintage_links === 'string' ? JSON.parse(spa.wayback_vintage_links) : spa.wayback_vintage_links;
            } catch(e) {
              wbData = null;
            }
          }

          if (wbData && wbData.snapshots && wbData.snapshots.length > 0) {
            const milestoneYears = wbData.milestone_years || wbData.vintage_years || [];
            const grid = document.createElement('div');
            grid.className = 'grid grid-cols-1 md:grid-cols-3 gap-3';

            milestoneYears.forEach(yr => {
              const yearSnaps = wbData.snapshots.filter(s => (s.target_year === yr || s.year === yr));
              const card = document.createElement('div');
              card.className = 'p-3.5 rounded-xl bg-spafit-card/80 border border-spafit-border space-y-2';

              let snapsHtml = '';
              if (yearSnaps.length > 0) {
                snapsHtml = yearSnaps.map(s => {
                  const isBp = (s.type || '').includes('blueprint') || (s.category || '').includes('Blueprint');
                  const badgeStyle = isBp ? 'bg-spafit-cyan/20 text-spafit-cyan border-spafit-cyan/30' : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30';
                  const typeLabel = isBp ? '📐 Blueprint (CAD/PDF)' : '📷 Overhead Shell';
                  return `
                    <div class="p-2.5 rounded-lg bg-spafit-dark/70 border border-spafit-border space-y-1.5 text-xs">
                      <div class="flex items-center justify-between">
                        <span class="text-[10px] font-mono px-1.5 py-0.5 rounded border ${badgeStyle}">${typeLabel}</span>
                        <span class="text-[10px] font-mono text-slate-400">Snapshot: ${s.archived_year || s.year}</span>
                      </div>
                      <div class="font-mono text-white text-[11px] font-semibold truncate">${s.code || ''}</div>
                      <div class="flex items-center gap-2 pt-1 border-t border-spafit-border/50">
                        <a href="${s.snapshot_url}" target="_blank" class="text-[10px] text-spafit-accent hover:underline flex items-center gap-1 font-mono">Archive Snapshot ↗</a>
                        ${s.raw_url ? `<a href="${s.raw_url}" target="_blank" class="text-[10px] text-slate-300 hover:text-white flex items-center gap-1 font-mono ml-auto">Raw Binary 📥</a>` : ''}
                      </div>
                    </div>
                  `;
                }).join('');
              } else {
                snapsHtml = '<div class="text-[11px] text-slate-500 italic py-2 text-center">No archived snapshot captured for this milestone vintage.</div>';
              }

              card.innerHTML = `
                <div class="flex items-center justify-between border-b border-spafit-border pb-1.5">
                  <span class="text-xs font-bold text-spafit-cyan font-mono flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-spafit-cyan"></span>
                    Vintage Milestone ${yr}
                  </span>
                  <span class="text-[10px] font-mono text-slate-400">${yearSnaps.length} verified item(s)</span>
                </div>
                <div class="space-y-2 pt-1">
                  ${snapsHtml}
                </div>
              `;
              grid.appendChild(card);
            });

            els.waybackVintageContainer.appendChild(grid);
            if (els.waybackTrackingBadge) {
              els.waybackTrackingBadge.textContent = `${wbData.snapshots.length} Verified Snapshots`;
              els.waybackTrackingBadge.className = 'text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';
            }
          } else {
            els.waybackVintageContainer.innerHTML = `
              <div class="p-6 rounded-xl bg-spafit-card/40 border border-spafit-border text-center space-y-1.5">
                <div class="text-sm font-semibold text-slate-300">Wayback Machine Generational Tracking Pending</div>
                <div class="text-xs text-slate-500">Automated multi-year archival tracking will ingest launch, mid-cycle, and mature vintages for this brand in the next scheduled batch.</div>
              </div>
            `;
            if (els.waybackTrackingBadge) {
              els.waybackTrackingBadge.textContent = 'Pending Ingestion';
              els.waybackTrackingBadge.className = 'text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700';
            }
          }
        }
      }

      function renderModalAssetsTab(spa) {
        els.assetLinksContainer.innerHTML = '';
        els.sourceUrlsContainer.innerHTML = '';

        // Photos in Gallery
        const topImg = getTopImageSrc(spa);
        if (topImg) {
          els.galleryTopImg.src = topImg;
          els.galleryTopImg.classList.remove('hidden');
          els.galleryTopFallback.classList.add('hidden');
          els.galleryTopLink.href = topImg;
          els.galleryTopLink.classList.remove('hidden');
          els.galleryTopBadge.textContent = 'Verified Image';
          els.galleryTopBadge.className = 'text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300';
        } else {
          els.galleryTopImg.classList.add('hidden');
          els.galleryTopFallback.classList.remove('hidden');
          els.galleryTopLink.classList.add('hidden');
          els.galleryTopBadge.textContent = 'Not Published';
          els.galleryTopBadge.className = 'text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-500';
        }

        const sideImg = (spa.image_side_file && spa.image_side_file !== 'N/A') ? spa.image_side_file : (spa.image_side_source_url && spa.image_side_source_url.startsWith('http') ? spa.image_side_source_url : null);
        if (sideImg) {
          els.gallerySideImg.src = sideImg;
          els.gallerySideImg.classList.remove('hidden');
          els.gallerySideFallback.classList.add('hidden');
          els.gallerySideLink.href = sideImg;
          els.gallerySideLink.classList.remove('hidden');
          els.gallerySideBadge.textContent = 'Elevation Skirt';
          els.gallerySideBadge.className = 'text-[10px] font-mono px-2 py-0.5 rounded bg-spafit-blue/30 text-spafit-accent';
        } else {
          els.gallerySideImg.classList.add('hidden');
          els.gallerySideFallback.classList.remove('hidden');
          els.gallerySideLink.classList.add('hidden');
          els.gallerySideBadge.textContent = 'Not Available';
          els.gallerySideBadge.className = 'text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-500';
        }

        // CAD Assets
        const cadItems = [
          { name: '2D CAD Drawing (DWG)', file: spa.cad_dwg_file, icon: 'DWG' },
          { name: '2D CAD Vector (DXF)', file: spa.cad_dxf_file, icon: 'DXF' },
          { name: '2D CAD Vector Contour (SVG)', file: spa.cad_svg_contour, icon: 'SVG' },
          { name: '3D Solid Model (STEP)', file: spa.model_step_file, icon: 'STEP' },
          { name: '3D Mesh Model (STL)', file: spa.model_stl_file, icon: 'STL' },
          { name: 'Architectural Footprint (PDF)', file: spa.footprint_file, icon: 'PDF' }
        ];

        cadItems.forEach(item => {
          const div = document.createElement('div');
          div.className = 'flex items-center justify-between p-2.5 rounded-lg bg-spafit-card/60 border border-spafit-border';
          const hasFile = item.file && item.file !== 'N/A';
          div.innerHTML = `
            <div class="flex items-center gap-2">
              <span class="w-10 text-center font-mono font-bold text-[10px] px-1.5 py-0.5 rounded ${hasFile ? 'bg-spafit-blue/30 text-spafit-accent border border-spafit-blue/40' : 'bg-slate-800 text-slate-500'}">${item.icon}</span>
              <span class="${hasFile ? 'text-slate-200' : 'text-slate-500'} font-medium">${item.name}</span>
            </div>
            ${hasFile ? `<a href="${item.file}" target="_blank" class="px-2.5 py-1 rounded bg-spafit-blue text-[11px] font-semibold text-white hover:bg-spafit-cyan transition-colors flex items-center gap-1">Download</a>` : '<span class="text-[11px] text-slate-500 italic">Not Published</span>'}
          `;
          els.assetLinksContainer.appendChild(div);
        });

        // Source URLs
        const srcItems = [
          { name: 'Dimensions Source 1', url: spa.dimensions_source_url_1 },
          { name: 'Dimensions Source 2', url: spa.dimensions_source_url_2 },
          { name: 'Corner Radius Source (OEM Template)', url: spa.corner_radius_source_url }
        ];

        srcItems.forEach(src => {
          const div = document.createElement('div');
          div.className = 'p-2.5 rounded-lg bg-spafit-card/60 border border-spafit-border space-y-1';
          const hasUrl = src.url && src.url !== 'N/A' && src.url.startsWith('http');
          div.innerHTML = `
            <span class="text-[11px] text-slate-400 font-medium block">${src.name}</span>
            ${hasUrl ? `<a href="${src.url}" target="_blank" class="text-xs text-spafit-cyan hover:underline break-all flex items-center gap-1 font-mono">${src.url} <svg class="w-3 h-3 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg></a>` : '<span class="text-xs text-slate-500 italic">N/A</span>'}
          `;
          els.sourceUrlsContainer.appendChild(div);
        });
      }

      // Event Listeners Binding
      function bindEvents() {
        // Global search
        els.globalSearchInput.addEventListener('input', (e) => {
          state.searchTerm = e.target.value;
          els.clearSearchBtn.classList.toggle('hidden', !state.searchTerm);
          applyFilters();
        });

        els.clearSearchBtn.addEventListener('click', () => {
          state.searchTerm = '';
          els.globalSearchInput.value = '';
          els.clearSearchBtn.classList.add('hidden');
          applyFilters();
        });

        // Global Media Toggle (Photos vs Blueprints on cards)
        els.mediaTogglePhoto.addEventListener('click', () => {
          state.cardMediaMode = 'photo';
          els.mediaTogglePhoto.className = 'px-2.5 py-1 rounded bg-spafit-blue text-white shadow transition-all flex items-center gap-1';
          els.mediaToggleBp.className = 'px-2.5 py-1 rounded text-slate-400 hover:text-white transition-all flex items-center gap-1';
          state.cardFlipMap = {}; // reset card manual flips
          renderResults();
        });

        els.mediaToggleBp.addEventListener('click', () => {
          state.cardMediaMode = 'bp';
          els.mediaToggleBp.className = 'px-2.5 py-1 rounded bg-spafit-blue text-white shadow transition-all flex items-center gap-1';
          els.mediaTogglePhoto.className = 'px-2.5 py-1 rounded text-slate-400 hover:text-white transition-all flex items-center gap-1';
          state.cardFlipMap = {}; // reset card manual flips
          renderResults();
        });

        // Photos Quick Filter Button
        els.onlyWithPhotosBtn.addEventListener('click', () => {
          state.onlyWithPhotos = !state.onlyWithPhotos;
          els.onlyWithPhotosBtn.classList.toggle('border-spafit-cyan', state.onlyWithPhotos);
          els.onlyWithPhotosBtn.classList.toggle('bg-spafit-cyan/15', state.onlyWithPhotos);
          applyFilters();
        });

        // Modal Visual Sub-Toggles (Photo | Blueprint | Split)
        els.modalSubTogglePhoto.addEventListener('click', () => setModalVisualMode('photo'));
        els.modalSubToggleBp.addEventListener('click', () => setModalVisualMode('bp'));
        els.modalSubToggleSplit.addEventListener('click', () => setModalVisualMode('split'));

        // Keyboard shortcut: slash '/' focuses search
        window.addEventListener('keydown', (e) => {
          if (e.key === '/' && document.activeElement !== els.globalSearchInput) {
            e.preventDefault();
            els.globalSearchInput.focus();
          }
          if (e.key === 'Escape' && !els.spaModal.classList.contains('hidden')) {
            closeModal();
          }
        });

        // Unit Toggle
        els.unitToggleIn.addEventListener('click', () => {
          state.unit = 'in';
          els.unitToggleIn.classList.add('bg-spafit-blue', 'text-white', 'shadow');
          els.unitToggleIn.classList.remove('text-slate-400');
          els.unitToggleCm.classList.remove('bg-spafit-blue', 'text-white', 'shadow');
          els.unitToggleCm.classList.add('text-slate-400');
          renderResults();
        });

        els.unitToggleCm.addEventListener('click', () => {
          state.unit = 'cm';
          els.unitToggleCm.classList.add('bg-spafit-blue', 'text-white', 'shadow');
          els.unitToggleCm.classList.remove('text-slate-400');
          els.unitToggleIn.classList.remove('bg-spafit-blue', 'text-white', 'shadow');
          els.unitToggleIn.classList.add('text-slate-400');
          renderResults();
        });

        // View Mode Switcher
        els.viewGridBtn.addEventListener('click', () => {
          state.viewMode = 'grid';
          updateViewButtons();
          renderResults();
        });
        els.viewTableBtn.addEventListener('click', () => {
          state.viewMode = 'table';
          updateViewButtons();
          renderResults();
        });
        els.viewCompareBtn.addEventListener('click', () => {
          state.viewMode = 'compare';
          updateViewButtons();
          renderResults();
        });

        // Segment Buttons
        document.querySelectorAll('.segment-btn').forEach(btn => {
          btn.addEventListener('click', () => {
            document.querySelectorAll('.segment-btn').forEach(b => {
              b.classList.remove('active', 'bg-spafit-blue', 'text-white');
              b.classList.add('bg-spafit-card', 'border', 'border-spafit-border', 'text-slate-300');
            });
            btn.classList.add('active', 'bg-spafit-blue', 'text-white');
            btn.classList.remove('bg-spafit-card', 'text-slate-300');
            state.selectedSegment = btn.getAttribute('data-segment');
            applyFilters();
          });
        });

        // SpaFit Quick Buttons
        document.querySelectorAll('.spafit-quick-btn').forEach(btn => {
          btn.addEventListener('click', () => {
            const filter = btn.getAttribute('data-spafit-filter');
            if (state.selectedSpaFitFilter === filter) {
              state.selectedSpaFitFilter = 'all';
              btn.classList.remove('border-spafit-cyan', 'text-white');
            } else {
              state.selectedSpaFitFilter = filter;
              document.querySelectorAll('.spafit-quick-btn').forEach(b => b.classList.remove('border-spafit-cyan', 'text-white'));
              btn.classList.add('border-spafit-cyan', 'text-white');
            }
            applyFilters();
          });
        });

        // Manufacturer select
        els.brandSelect.addEventListener('change', (e) => {
          state.selectedBrand = e.target.value;
          state.selectedSeries = 'all';
          updateSeriesOptions(state.selectedBrand);
          applyFilters();
        });

        // Series select
        els.seriesSelect.addEventListener('change', (e) => {
          state.selectedSeries = e.target.value;
          applyFilters();
        });

        // Generation select
        els.genSelect.addEventListener('change', (e) => {
          state.selectedGen = e.target.value;
          applyFilters();
        });

        // Radius presets
        document.querySelectorAll('.radius-preset-btn').forEach(btn => {
          btn.addEventListener('click', () => {
            document.querySelectorAll('.radius-preset-btn').forEach(b => {
              b.classList.remove('active', 'bg-spafit-blue', 'text-white');
              b.classList.add('bg-spafit-card', 'border', 'border-spafit-border', 'text-slate-300');
            });
            btn.classList.add('active', 'bg-spafit-blue', 'text-white');
            btn.classList.remove('bg-spafit-card', 'text-slate-300');
            state.radiusPreset = btn.getAttribute('data-radius-preset');
            els.radiusFilterLabel.textContent = btn.textContent;
            applyFilters();
          });
        });

        // Sliders
        els.lengthSlider.addEventListener('input', (e) => {
          state.maxLength = parseInt(e.target.value);
          els.lengthValLabel.textContent = `${state.maxLength} in (${Math.round(state.maxLength * 2.54)} cm)`;
          applyFilters();
        });

        els.widthSlider.addEventListener('input', (e) => {
          state.maxWidth = parseInt(e.target.value);
          els.widthValLabel.textContent = `${state.maxWidth} in (${Math.round(state.maxWidth * 2.54)} cm)`;
          applyFilters();
        });

        // Sort
        els.sortSelect.addEventListener('change', (e) => {
          state.sortBy = e.target.value;
          sortResults();
          renderResults();
        });

        // Reset
        els.resetFiltersBtn.addEventListener('click', resetAllFilters);
        els.emptyResetBtn.addEventListener('click', resetAllFilters);
        els.clearPinnedBtn.addEventListener('click', () => {
          state.pinnedIds.clear();
          updatePinnedBadge();
          renderCompareView();
        });

        // Export CSV
        els.exportCsvBtn.addEventListener('click', exportFilteredCsv);

        // Modal Controls
        els.modalCloseBtn.addEventListener('click', closeModal);
        els.modalCloseFooterBtn.addEventListener('click', closeModal);
        els.spaModal.addEventListener('click', (e) => {
          if (e.target === els.spaModal) closeModal();
        });

        // Modal Tabs
        document.querySelectorAll('.modal-tab-btn').forEach(btn => {
          btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            switchModalTab(tabId);
          });
        });

        // Modal Pin Button
        els.modalPinBtn.addEventListener('click', () => {
          if (state.activeSpa) {
            togglePinSpa(state.activeSpa.id);
            updateModalPinButton();
          }
        });

        // Modal Blueprint layer toggles
        els.toggleLayerSpaFit.addEventListener('change', (e) => {
          state.showLayerSpaFit = e.target.checked;
          if (state.activeSpa) renderModalVisualTab(state.activeSpa);
        });
        els.toggleLayerSeal.addEventListener('change', (e) => {
          state.showLayerSeal = e.target.checked;
          if (state.activeSpa) renderModalVisualTab(state.activeSpa);
        });

        // Modal Simulator inputs
        els.spafitModelSelect.addEventListener('change', executeSpaFitSimulation);
        els.spafitOrientationSelect.addEventListener('change', executeSpaFitSimulation);
        els.autoSelectBestSpaFitBtn.addEventListener('click', () => {
          if (state.activeSpa) renderModalSpaFitTab(state.activeSpa);
        });

        els.bpSimulateNowBtn.addEventListener('click', () => {
          switchModalTab('spafit');
        });
      }

      function updateViewButtons() {
        els.viewGridBtn.className = state.viewMode === 'grid' ? 'p-1.5 rounded bg-spafit-blue text-white shadow' : 'p-1.5 rounded text-slate-400 hover:text-white';
        els.viewTableBtn.className = state.viewMode === 'table' ? 'p-1.5 rounded bg-spafit-blue text-white shadow' : 'p-1.5 rounded text-slate-400 hover:text-white';
        els.viewCompareBtn.className = state.viewMode === 'compare' ? 'p-1.5 rounded bg-spafit-blue text-white shadow relative' : 'p-1.5 rounded text-slate-400 hover:text-white relative';
      }

      function bindCardEvents() {
        document.querySelectorAll('[data-open-modal]').forEach(btn => {
          btn.addEventListener('click', () => {
            const id = parseInt(btn.getAttribute('data-open-modal'));
            const tab = btn.getAttribute('data-target-tab') || 'visual';
            openModal(id, tab);
          });
        });

        document.querySelectorAll('.pin-btn').forEach(btn => {
          btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const id = parseInt(btn.getAttribute('data-spa-id'));
            togglePinSpa(id);
          });
        });

        // Card flip button between Photo and Blueprint
        document.querySelectorAll('[data-flip-card]').forEach(btn => {
          btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const id = parseInt(btn.getAttribute('data-flip-card'));
            const current = state.cardFlipMap[id] || (getTopImageSrc(state.spas.find(s => s.id === id)) && state.cardMediaMode === 'photo' ? 'photo' : 'bp');
            state.cardFlipMap[id] = current === 'photo' ? 'bp' : 'photo';
            renderGridView();
          });
        });
      }

      function resetAllFilters() {
        state.searchTerm = '';
        els.globalSearchInput.value = '';
        els.clearSearchBtn.classList.add('hidden');

        state.onlyWithPhotos = false;
        els.onlyWithPhotosBtn.classList.remove('border-spafit-cyan', 'bg-spafit-cyan/15');

        state.selectedBrand = 'all';
        els.brandSelect.value = 'all';
        updateSeriesOptions('all');

        state.selectedSeries = 'all';
        els.seriesSelect.value = 'all';

        state.selectedGen = 'all';
        els.genSelect.value = 'all';

        state.selectedSegment = 'all';
        document.querySelectorAll('.segment-btn').forEach(b => {
          const isAll = b.getAttribute('data-segment') === 'all';
          b.classList.toggle('active', isAll);
          b.classList.toggle('bg-spafit-blue', isAll);
          b.classList.toggle('text-white', isAll);
        });

        state.selectedSpaFitFilter = 'all';
        document.querySelectorAll('.spafit-quick-btn').forEach(b => b.classList.remove('border-spafit-cyan', 'text-white'));

        state.radiusPreset = 'all';
        document.querySelectorAll('.radius-preset-btn').forEach(b => {
          const isAll = b.getAttribute('data-radius-preset') === 'all';
          b.classList.toggle('active', isAll);
          b.classList.toggle('bg-spafit-blue', isAll);
          b.classList.toggle('text-white', isAll);
        });
        els.radiusFilterLabel.textContent = 'All Radii';

        state.maxLength = 300;
        els.lengthSlider.value = 300;
        els.lengthValLabel.textContent = '300 in (762 cm)';

        state.maxWidth = 120;
        els.widthSlider.value = 120;
        els.widthValLabel.textContent = '120 in (305 cm)';

        applyFilters();
      }

      function exportFilteredCsv() {
        if (state.filteredSpas.length === 0) {
          alert('No spas to export.');
          return;
        }

        const headers = ['ID', 'Marque', 'Modele', 'Serie_Collection', 'Generation', 'Annees_Production', 'length_in', 'length_cm', 'width_in', 'width_cm', 'height_in', 'height_cm', 'corner_radius_in', 'corner_radius_cm', 'cover_compatible'];
        let csvContent = 'data:text/csv;charset=utf-8,' + headers.join(';') + '\\n';

        state.filteredSpas.forEach(s => {
          const row = [
            s.id,
            `"${s.Marque || ''}"`,
            `"${s.Modele || ''}"`,
            `"${s.Serie_Collection || ''}"`,
            `"${s.Generation || ''}"`,
            `"${s.Annees_Production || ''}"`,
            s.length_in || '',
            s.length_cm || '',
            s.width_in || '',
            s.width_cm || '',
            s.height_in || '',
            s.height_cm || '',
            s.corner_radius_in || '',
            s.corner_radius_cm || '',
            `"${(s.cover_compatible || []).join(', ')}"`
          ];
          csvContent += row.join(';') + '\\n';
        });

        const encodedUri = encodeURI(csvContent);
        const link = document.createElement('a');
        link.setAttribute('href', encodedUri);
        link.setAttribute('download', `spafit_spas_export_${new Date().toISOString().slice(0,10)}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }

      // Expose globally for inline event handlers
      window.SPAFIT_APP = {
        openModal: openModal
      };

      // Launch
      init();
    })();
  </script>
</body>
</html>
"""

with open('spa_catalog_viewer.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Regenerated spa_catalog_viewer.html with Top View Photos successfully!")
