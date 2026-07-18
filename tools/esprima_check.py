#!/usr/bin/env python3
import re
from pathlib import Path

try:
    import esprima
except ImportError:
    raise SystemExit('pip install esprima')

HTML = Path(__file__).resolve().parents[1] / 'index.html'

def extract_js(html):
    m = re.search(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", html, re.I)
    return m.group(1)

js = extract_js(HTML.read_text(encoding='utf-8'))
lines = js.splitlines()
try:
    esprima.parseScript(js)
    print('LOCAL_OK')
except esprima.Error as e:
    ln = e.lineNumber or 0
    col = e.column or 0
    print('LOCAL_FAIL', e.message, 'line', ln, 'col', col)
    for i in range(max(1, ln - 5), min(len(lines), ln + 5) + 1):
        mark = '>>' if i == ln else '  '
        print(f'{mark}{i:5d}|{lines[i-1][:240]}')
