'use strict';

/** Velora PWA — shell v2 (2026). Bump SHELL_CACHE ao alterar precache. */
const SHELL_CACHE = 'velora-shell-v12';
const RUNTIME_CACHE = 'velora-runtime-v8';

const PRECACHE = [
  './',
  './index.html',
  './404.html',
  './data/knowledge-os-bank.js',
  './forge/forge-engines.js',
  './forge/knowledge-forge.js',
  './gps/velora-gps.js',
  './manifest.webmanifest',
  './branding/favicon/favicon.svg',
  './branding/icons/app-icon.svg',
  './branding/logo/symbol-white.svg',
  './branding/logo/symbol-color.svg',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(SHELL_CACHE)
      .then((cache) => cache.addAll(PRECACHE))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.filter((k) => k !== SHELL_CACHE && k !== RUNTIME_CACHE).map((k) => caches.delete(k))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((resp) => {
          if (resp.ok) {
            caches.open(SHELL_CACHE).then((c) => c.put('./index.html', resp.clone()));
          }
          return resp;
        })
        .catch(() =>
          caches.match('./index.html').then((r) => r || caches.match('./404.html'))
        )
    );
    return;
  }

  event.respondWith(
    caches.match(request).then((cached) => {
      const network = fetch(request)
        .then((resp) => {
          if (resp.ok && resp.type === 'basic') {
            caches.open(RUNTIME_CACHE).then((c) => c.put(request, resp.clone()));
          }
          return resp;
        })
        .catch(() => cached);
      return cached || network;
    })
  );
});
