#!/usr/bin/env python3
import re
from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / 'index.html'
js = re.search(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", HTML.read_text(encoding='utf-8'), re.I).group(1)
lines = js.splitlines()
ln = 5392
for i in range(ln - 8, ln + 8):
    if 1 <= i <= len(lines):
        mark = '>>' if i == ln else '  '
        line = lines[i-1]
        print(f'{mark}{i:5d}|{line}')
        if i == ln:
            print(' ' * 9 + ' ' * 10 + '^')
