#!/usr/bin/env python3
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML = Path(__file__).resolve().parents[1] / 'index.html'

def extract_inline_js(html: str) -> str:
    parts = []
    for m in re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>', html, re.I):
        parts.append(m.group(1))
    return '\n'.join(parts)

def line_at(js: str, pos: int) -> int:
    return js.count('\n', 0, pos) + 1

def snippet(js: str, pos: int, radius=120):
    start = max(0, pos - radius)
    end = min(len(js), pos + radius)
    chunk = js[start:end]
    mark = pos - start
    return chunk, mark

with sync_playwright() as p:
    page = p.chromium.launch(headless=True).new_page()
    page.goto('about:blank')
    js = extract_inline_js(HTML.read_text(encoding='utf-8'))

    def ok(n):
        try:
            page.evaluate('(code) => new Function(code)', js[:n])
            return True
        except Exception:
            return False

    if ok(len(js)):
        print('FULL_OK')
        raise SystemExit(0)

    lo, hi = 1, len(js)
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            lo = mid + 1
        else:
            hi = mid
    fail = lo
    ln = line_at(js, fail)
    lines = js.splitlines()
    print('fail_char', fail, 'line', ln)
    for i in range(max(1, ln-4), min(len(lines), ln+4)+1):
        mark = '>>' if i == ln else '  '
        print(f'{mark}{i:5d}|{lines[i-1][:200]}')
    chunk, mark = snippet(js, fail)
    print('--- context ---')
    print(chunk[:mark] + '<<HERE>>' + chunk[mark:])
