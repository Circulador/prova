#!/usr/bin/env python3
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

pat = r"\.ec-layout\{display:grid.*?\.player-candidate\{font-size:12px"
m_idx = re.search(pat, idx, re.S)
m_404 = re.search(pat, html404, re.S)
if m_idx and m_404:
    html404 = html404[: m_404.start()] + m_idx.group(0) + html404[m_404.end() :]

pat2 = r"class ExamConfigModal \{.*?\n\}\n\n/\* =+\n   PLAYER CONTROLLER"
m_idx = re.search(pat2, idx, re.S)
m_404 = re.search(pat2, html404, re.S)
if m_idx and m_404:
    html404 = html404[: m_404.start()] + m_idx.group(0) + html404[m_404.end() :]

(ROOT / "404.html").write_text(html404, encoding="utf-8")
print("Synced 404.html")
