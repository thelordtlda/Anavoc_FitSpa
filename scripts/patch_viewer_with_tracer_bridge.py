#!/usr/bin/env python3
"""
patch_viewer_with_tracer_bridge.py
Injects the 'Ouvrir dans l'Analyseur de Joint' bridge into scripts/build_spa_catalog_viewer.py
and regenerates spa_catalog_viewer.html.
"""

import os
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BUILDER_PATH = os.path.join(ROOT_DIR, 'scripts', 'build_spa_catalog_viewer.py')

def patch():
    with open(BUILDER_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Title and Badges from 1,030 to 1,339
    content = content.replace("1,030 Spas", "1,339 Spas")
    content = content.replace("1,030", "1,339")

    # 2. Add Tracer button to Modal Header
    modal_pin_str = '<button id="modalPinBtn"'
    tracer_modal_btn = '''<!-- Open in Seal Tracer button -->
          <a id="modalOpenTracerLink" href="index.html" target="_blank" class="px-2.5 py-1.5 rounded-lg bg-emerald-600/30 hover:bg-emerald-600 border border-emerald-500/50 text-xs text-emerald-200 hover:text-white flex items-center gap-1.5 transition-colors font-semibold" title="Ouvrir dans l'Analyseur de Joint 2D">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
            <span>Ouvrir dans l'Analyseur de Joint</span>
          </a>

          <button id="modalPinBtn"'''
    if 'id="modalOpenTracerLink"' not in content:
        content = content.replace(modal_pin_str, tracer_modal_btn, 1)

    # 3. Add to els object
    els_str = "modalPinBtn: document.getElementById('modalPinBtn'),"
    els_tracer = "modalOpenTracerLink: document.getElementById('modalOpenTracerLink'),\n        modalPinBtn: document.getElementById('modalPinBtn'),"
    if 'modalOpenTracerLink:' not in content:
        content = content.replace(els_str, els_tracer, 1)

    # 4. Add to openModal function
    open_modal_anchor = "els.modalProcessTime.textContent = spa.process_timestamp || 'Verified';"
    tracer_link_update = '''els.modalProcessTime.textContent = spa.process_timestamp || 'Verified';
        if (els.modalOpenTracerLink) {
          els.modalOpenTracerLink.href = `index.html?spa_id=${spa.id}`;
        }'''
    if 'els.modalOpenTracerLink.href' not in content:
        content = content.replace(open_modal_anchor, tracer_link_update, 1)

    # 5. Add Tracer button to Card Footer
    card_footer_target = '''              <button data-open-modal="${spa.id}" data-target-tab="spafit" class="py-1.5 px-3 rounded-lg bg-spafit-blue hover:bg-spafit-cyan text-xs text-white font-semibold shadow transition-all flex items-center gap-1" title="Simulate SpaFit Sizer Compatibility">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
                <span>Simulate</span>
              </button>'''

    card_footer_replacement = '''              <button data-open-modal="${spa.id}" data-target-tab="spafit" class="py-1.5 px-2.5 rounded-lg bg-spafit-blue hover:bg-spafit-cyan text-xs text-white font-semibold shadow transition-all flex items-center gap-1" title="Simulate SpaFit Sizer Compatibility">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
                <span>Simuler</span>
              </button>
              <a href="index.html?spa_id=${spa.id}" target="_blank" class="py-1.5 px-2 rounded-lg bg-emerald-600/20 hover:bg-emerald-600 border border-emerald-500/40 text-emerald-300 hover:text-white text-xs font-semibold shadow transition-all flex items-center gap-1" title="Ouvrir dans l'Analyseur de Joint 2D">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                <span>Tracer</span>
              </a>'''

    if 'title="Ouvrir dans l\'Analyseur de Joint 2D"' not in content:
        # Normalize CRLF for matching
        content_norm = content.replace('\r\n', '\n')
        target_norm = card_footer_target.replace('\r\n', '\n')
        replacement_norm = card_footer_replacement.replace('\r\n', '\n')
        content_norm = content_norm.replace(target_norm, replacement_norm, 1)
        content = content_norm

    with open(BUILDER_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Patched {BUILDER_PATH}")

if __name__ == '__main__':
    patch()
