#!/usr/bin/env python3
"""Sync index.html shell (CSS + main JS + bootstrap tail) to 404.html."""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
BANK = "knowledge-os-bank.js"


def sync():
    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    html404 = (ROOT / "404.html").read_text(encoding="utf-8")

    if f"data/{BANK}" not in html404:
        html404 = re.sub(
            r"data/dpo-global-bank\.js",
            f"data/{BANK}",
            html404,
        )

    # Main inline script: from opening tag after forge scripts through GPS defer tag
    script_pat = (
        r'(<script src="forge/forge-engines\.js" defer></script>\s*'
        r'<script src="forge/knowledge-forge\.js" defer></script>\s*<script>)'
        r"(.*?)(</script>\s*\n<script src=\"\./gps/velora-gps\.js\" defer></script>)"
    )
    m_idx = re.search(script_pat, idx, re.DOTALL)
    m_404 = re.search(
        r'(<script src="forge/forge-engines\.js"(?: defer)?></script>\s*'
        r'<script src="forge/knowledge-forge\.js"(?: defer)?></script>\s*<script>)'
        r"(.*?)(</script>\s*\n<script src=\"(?:\./)?gps/velora-gps\.js\"(?: defer)?></script>)",
        html404,
        re.DOTALL,
    )
    if not m_idx:
        print("WARN: could not find main script block in index.html")
        return
    if not m_404:
        print("WARN: could not find main script block in 404.html")
        return
    new_404 = (
        html404[: m_404.start(1)]
        + m_idx.group(1)
        + m_idx.group(2)
        + m_idx.group(3)
        + html404[m_404.end(3) :]
    )

    # Remove stale trailing inline scripts after GPS (legacy bootstrap duplicate)
    new_404 = re.sub(
        r"<script>\s*Object\.assign\(window,\s*\{\s*LearningGoal[\s\S]*?</script>\s*",
        "",
        new_404,
        count=1,
    )

    # CSS
    style_pat = r"(<style>)(.*?)(</style>)"
    si = re.search(style_pat, idx, re.DOTALL)
    s4 = re.search(style_pat, new_404, re.DOTALL)
    if si and s4:
        new_404 = new_404[: s4.start(2)] + si.group(2) + new_404[s4.end(2) :]

    # Loading overlay shell
    overlay_idx = re.search(r'<div id="loading-overlay"[^>]*>', idx)
    overlay_404 = re.search(r'<div id="loading-overlay"[^>]*>', new_404)
    if overlay_idx and overlay_404:
        new_404 = (
            new_404[: overlay_404.start()]
            + overlay_idx.group(0)
            + new_404[overlay_404.end() :]
        )

    (ROOT / "404.html").write_text(new_404, encoding="utf-8")
    print("Synced CSS + JS + bootstrap tail to 404.html")


if __name__ == "__main__":
    sync()
