#!/usr/bin/env python3
"""Sync exam modal + mobile-first nav from index.html to 404.html."""
import re
from pathlib import Path

ROOT = Path(__file__).parent
idx = (ROOT / "index.html").read_text(encoding="utf-8")
html404 = (ROOT / "404.html").read_text(encoding="utf-8")

html404 = html404.replace(
    "static open({title, bodyHtml, footerHtml='', wide=false, onMount=null})",
    "static open({title, bodyHtml, footerHtml='', wide=false, modalClass='', onMount=null})",
)
html404 = html404.replace(
    '<div class="modal ${wide?\'wide\':\'\'}">',
    '<div class="modal ${wide?\'wide\':\'\'} ${modalClass||\'\'}">',
)


def replace_block(text: str, pattern: str, replacement: str, label: str) -> str:
    m_src = re.search(pattern, idx, re.S)
    m_dst = re.search(pattern, text, re.S)
    if not m_src:
        print(f"WARN: source missing {label}")
        return text
    if not m_dst:
        print(f"WARN: dest missing {label}")
        return text
    return text[: m_dst.start()] + m_src.group(0) + text[m_dst.end() :]


# Exam config CSS (.ec-layout … .player-candidate)
html404 = replace_block(
    html404,
    r"\.ec-layout\{display:grid.*?\.player-candidate\{font-size:12px",
    "",
    "exam CSS",
)

# ExamConfigModal class
html404 = replace_block(
    html404,
    r"class ExamConfigModal \{.*?\n\}\n\n/\* =+\n   PLAYER CONTROLLER",
    "",
    "ExamConfigModal",
)

# Tabbar + mobile-first hub tabs + desktop sidebar breakpoint
html404 = replace_block(
    html404,
    r"\.tabbar\{\n  position:fixed;bottom:0.*?\.topbar h1\{font-size:16px\}\n\}",
    "",
    "tabbar CSS",
)

# Velora overrides: main padding + tabbar sidebar block
html404 = replace_block(
    html404,
    r"\.main\{background:transparent;padding-bottom:calc\(60px \+ env\(safe-area-inset-bottom,0px\)\)\}\n(?:@media\(min-width:1024px\)\{\.main\{padding-bottom:0\}\}\n)?\.topbar\{padding:0 16px",
    "",
    "velora main/topbar start",
)
# Patch only the velora tabbar tail if full block match fails — use two-step
m_velora_tab = re.search(
    r"@media\(max-width:1023px\)\{\.topbar-brand \.topbar-app-name\{display:none\}\}\n@media\(min-width:1024px\)\{.*?\n  \.topbar-brand \.topbar-logo\{display:none\}\n\}",
    idx,
    re.S,
)
m_velora_tab_404 = re.search(
    r"@media\(max-width:1023px\)\{\.topbar-brand \.topbar-app-name\{display:none\}\}\n@media\(min-width:769px\)\{.*?\n  \.topbar-brand \.topbar-logo\{display:none\}\n\}|@media\(max-width:1023px\)\{\.topbar-brand \.topbar-app-name\{display:none\}\}\n@media\(min-width:1024px\)\{.*?\n  \.topbar-brand \.topbar-logo\{display:none\}\n\}",
    html404,
    re.S,
)
if m_velora_tab and m_velora_tab_404:
    html404 = (
        html404[: m_velora_tab_404.start()]
        + m_velora_tab.group(0)
        + html404[m_velora_tab_404.end() :]
    )
else:
    print("WARN: velora tabbar tail not synced")

# _buildTabbar
html404 = replace_block(
    html404,
    r"  _buildTabbar\(\)\{.*?  \}\n  _bindTopbar\(\)",
    "",
    "_buildTabbar",
)

(ROOT / "404.html").write_text(html404, encoding="utf-8")
print("Synced 404.html")
