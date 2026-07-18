#!/usr/bin/env python3
from pathlib import Path
from playwright.sync_api import sync_playwright

INDEX = Path(__file__).resolve().parents[1] / 'index.html'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    cdp = page.context.new_cdp_session(page)
    cdp.send('Runtime.enable')
    page.goto(INDEX.as_uri(), wait_until='domcontentloaded', timeout=120000)

    # compile inline script to get exception details
    js = page.evaluate('''() => {
      const el = [...document.scripts].find(s => !s.src);
      return el ? el.textContent : '';
    }''')

    result = cdp.send('Runtime.compileScript', {
        'expression': js,
        'persistScript': False,
        'sourceURL': 'index-inline.js'
    })
    print('compile', result)
    browser.close()
