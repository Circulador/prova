#!/usr/bin/env python3
"""Sync main JS block from index.html to 404.html."""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
BANK = "knowledge-os-bank.js"


def sync():
    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    html404 = (ROOT / "404.html").read_text(encoding="utf-8")

    if f"data/{BANK}" not in html404:
        html404 = re.sub(
            r'data/dpo-global-bank\.js',
            f"data/{BANK}",
            html404,
        )

    pattern_idx = (
        r'(<script src="forge/forge-engines\.js" defer></script>\s*'
        r'<script src="forge/knowledge-forge\.js" defer></script>\s*<script>)'
        r'(.*?)(/\* =+\s*\n   APP BOOTSTRAP)'
    )
    pattern_404 = (
        r'(<script src="forge/forge-engines\.js"(?: defer)?></script>\s*'
        r'<script src="forge/knowledge-forge\.js"(?: defer)?></script>\s*<script>)'
        r'(.*?)(/\* =+\s*\n   APP BOOTSTRAP)'
    )
    m_idx = re.search(pattern_idx, idx, re.DOTALL)
    m_404 = re.search(pattern_404, html404, re.DOTALL)
    if not m_idx:
        print("WARN: could not find script block in index.html")
        return
    if not m_404:
        print("WARN: could not find script block in 404.html")
        return
    new_404 = html404[: m_404.start(1)] + m_idx.group(1) + m_idx.group(2) + html404[m_404.end(2) :]
    style_pat = r"(<style>)(.*?)(</style>)"
    si = re.search(style_pat, idx, re.DOTALL)
    s4 = re.search(style_pat, html404, re.DOTALL)
    if si and s4:
        new_404 = new_404[: s4.start(2)] + si.group(2) + new_404[s4.end(2) :]
    (ROOT / "404.html").write_text(new_404, encoding="utf-8")
    print("Synced JS + CSS block to 404.html")


if __name__ == "__main__":
    sync()
