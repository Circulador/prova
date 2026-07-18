#!/usr/bin/env python3
import re
import urllib.request
from playwright.sync_api import sync_playwright

URL = 'https://circulador.github.io/prova/'

def fetch_js():
    html = urllib.request.urlopen(URL, timeout=60).read().decode('utf-8', 'replace')
    m = re.search(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", html, re.I)
    return m.group(1)

js = fetch_js()
lines = js.splitlines()
print('lines', len(lines))

with sync_playwright() as p:
    page = p.chromium.launch(headless=True).new_page()
    page.goto('about:blank')

    def err(code):
        return page.evaluate('''(code) => {
          try { new Function(code); return null; }
          catch(e){ return String(e.message); }
        }''', code)

    full = err(js)
    print('full_err', full)

    lo, hi = 1, len(lines)
    while lo < hi:
        mid = (lo + hi) // 2
        chunk = '\n'.join(lines[:mid])
        e = err(chunk)
        if e is None:
            lo = mid + 1
        else:
            hi = mid
    fail_line = lo
    print('fail_line', fail_line, 'msg', err('\n'.join(lines[:fail_line])))
    for i in range(max(1, fail_line - 8), min(len(lines), fail_line + 8) + 1):
        mark = '>>' if i == fail_line else '  '
        print(f'{mark}{i:5d}|{lines[i-1][:240]}')
