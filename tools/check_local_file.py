#!/usr/bin/env python3
from pathlib import Path
from playwright.sync_api import sync_playwright

INDEX = Path(__file__).resolve().parents[1] / 'index.html'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(INDEX.as_uri(), wait_until='load', timeout=120000)
    page.wait_for_timeout(3000)
    info = page.evaluate('''() => ({
      app: typeof App !== 'undefined',
      bootstrap: typeof bootstrapVelora !== 'undefined',
      overlay: document.getElementById('loading-overlay')?.className,
      tabbar: !!document.getElementById('tabbar'),
      home: !!document.querySelector('.home-welcome, #view-home')
    })''')
    print('local', info)
    print('errors', errors)
    browser.close()
