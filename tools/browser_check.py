#!/usr/bin/env python3
"""Headless browser smoke test for Velora boot."""
import sys
import urllib.request

URL = 'https://circulador.github.io/prova/'


def fetch_html():
    with urllib.request.urlopen(URL, timeout=60) as r:
        return r.read().decode('utf-8', 'replace')


def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('PLAYWRIGHT_MISSING')
        html = fetch_html()
        print('live_bootstrap', 'bootstrapVelora' in html)
        print('live_hidden', 'id="loading-overlay" class="hidden"' in html)
        print('live_v14', 'velora-shell-v14' in open(__file__.replace('tools/browser_check.py', 'sw.js'), encoding='utf-8').read())
        return 2

    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on('pageerror', lambda e: errors.append(f'PAGEERROR: {e}'))
        page.on('console', lambda msg: errors.append(f'CONSOLE_{msg.type}: {msg.text}') if msg.type == 'error' else None)
        page.goto(URL, wait_until='networkidle', timeout=120000)
        page.wait_for_timeout(5000)
        overlay_hidden = page.evaluate("""() => {
          const el = document.getElementById('loading-overlay');
          if (!el) return 'missing';
          const cs = getComputedStyle(el);
          return cs.display === 'none' || el.classList.contains('hidden');
        }""")
        tabbar = page.locator('#tabbar').count()
        home = page.locator('.home-welcome, #view-home, [data-route="home"]').count()
        body_text = page.evaluate('() => document.body.innerText.slice(0, 500)')
        print('overlay_hidden', overlay_hidden)
        print('tabbar', tabbar)
        print('home_nodes', home)
        print('body_preview', body_text.replace('\n', ' ')[:200])
        if errors:
            print('ERRORS')
            for e in errors[:20]:
                print(e)
        browser.close()
    return 0 if overlay_hidden and tabbar else 1


if __name__ == '__main__':
    sys.exit(main())
