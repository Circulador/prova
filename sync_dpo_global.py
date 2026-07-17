#!/usr/bin/env python3
"""Sync main JS block from index.html to 404.html (post DPO global update)."""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent

def sync():
    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    html404 = (ROOT / "404.html").read_text(encoding="utf-8")

    pattern_idx = r'(<script src="data/dpo-global-bank\.js"></script>\s*<script src="forge/knowledge-forge\.js"></script>\s*<script>)(.*?)(/\* =+\s*\n   APP BOOTSTRAP)'
    pattern_404 = r'(<script src="data/dpo-global-bank\.js"></script>\s*(?:<script src="forge/knowledge-forge\.js"></script>\s*)?<script>)(.*?)(/\* =+\s*\n   APP BOOTSTRAP)'
    m_idx = re.search(pattern_idx, idx, re.DOTALL)
    m_404 = re.search(pattern_404, html404, re.DOTALL)
    if not m_idx or not m_404:
        print("WARN: could not find script block markers")
        return
    new_404 = html404[:m_404.start(1)] + m_idx.group(1) + m_idx.group(2) + html404[m_404.end(2):]
    # Sync inline styles for home-* and player-paused from index head
    style_pat = r'(<style>)(.*?)(</style>)'
    si = re.search(style_pat, idx, re.DOTALL)
    s4 = re.search(style_pat, html404, re.DOTALL)
    if si and s4:
        new_404 = new_404[:s4.start(2)] + si.group(2) + new_404[s4.end(2):]
    (ROOT / "404.html").write_text(new_404, encoding="utf-8")
    print("Synced JS + CSS block to 404.html")

if __name__ == "__main__":
    sync()
