# Velora — Arquitetura PWA (2026)

> **Status:** especificação técnica — complementa [UI-REDESIGN-MODEL](UI-REDESIGN-MODEL.md) e [Manifesto](MANIFESTO-ARQUITETURA.md).  
> **Baseline:** tutorials PWA clássicos (App Shell, cache-first) vs implementação atual em `index.html` → `_setupPWA()`.

---

## 1. Análise — tutorial clássico vs 2026

### Ainda válidos

| Conceito | Por quê |
|----------|---------|
| **HTTPS** | Obrigatório para SW e installability |
| **Web App Manifest** | Identidade instalável, ícones, `display: standalone` |
| **Service Worker** | Interceptação de rede, cache, offline shell |
| **Cache Storage API** | Assets estáticos versionados |
| **App Shell** | HTML/CSS/JS da UI cacheados; dados via storage local |
| **beforeinstallprompt** | Controle do CTA de instalação (Chromium) |
| **404.html SPA fallback** | GitHub Pages — já usado no repo |

### Desatualizado no Velora atual

| Prática antiga | Problema hoje | Onde está |
|----------------|---------------|-----------|
| SW inline `Blob` | Sem review, sem SRI, difícil debug, quebra CSP estrita | `index.html` `_setupPWA` |
| Cache name fixo `velora-v1` | Sem purge na `activate` → cache infinito | idem |
| `cache.put` em toda resposta GET | Cacheia HTML dinâmico, erros 404, respostas opacas | idem |
| Manifest via Blob URL | `start_url` relativo instável; sem `id` (critério 2024+) | idem |
| Um único cache para tudo | Mistura shell, API, imagens — invalidação impossível | idem |
| “Offline page” bloqueante | Viola manifesto Velora — app deve funcionar offline | screenshots comuns |
| `skipWaiting()` sem UX | Atualização silenciosa quebra sessão de simulado | idem |
| localStorage para todo conteúdo | Limite ~5MB, sync main thread | `StorageManager` |

### APIs evoluídas

- **Manifest `id`** — identidade estável da PWA entre deploys (Chrome 96+).
- **`launch_handler`** — controle de janela ao abrir atalho (desktop).
- **`file_handlers`** — abrir `.json` / `.csv` de questões no app.
- **`protocol_handlers`** — `web+velora://` (opcional).
- **Navigation Preload** — acelera SW sem penalizar TTFB.
- **Background Sync / Periodic Sync** — fila de sync quando online (enhancement).
- **Badging API** — revisões pendentes no ícone (Chromium).
- **StorageManager.persist()** — reduz eviction em mobile.

### Recomendações Google (mudanças)

- **Installability:** manifest servido com `Content-Type` correto, ícones 192+512 maskable, `start_url` absoluto, screenshots para loja.
- **Core Web Vitals** pesam mais que checklist PWA puro.
- **Workbox** recomendado vs SW hand-written para produção.
- **iOS:** Add to Home Screen ≠ PWA completa — cache SW limitado, push restrito; planear UX Safari explicitamente.

### Substitutos modernos

| Antigo | Moderno |
|--------|---------|
| SW monolítico no HTML | `sw.ts` + Workbox + build (Vite PWA plugin) |
| localStorage para banco | **IndexedDB** (Dexie/idb) + Knowledge Node |
| Cache manual | Workbox recipes (`StaleWhileRevalidate`, `NetworkFirst`) |
| Offline page estática | **App shell + dados locais** — UI sempre funcional |
| Atualização forçada | Prompt “Nova versão” + `skipWaiting` controlado |

---

## 2. Checklist moderno (Velora)

Legenda: ✅ feito · ⚠️ parcial · ❌ pendente

### Infraestrutura

| Item | Velora | Nota |
|------|--------|------|
| HTTPS | ✅ | GitHub Pages |
| Manifest estático | ⚠️ | Existe `branding/pwa/manifest.json`; app usa Blob dinâmico |
| Manifest `id` | ❌ | Adicionar |
| Ícones 192/512 maskable | ⚠️ | SVG no runtime; PNGs em branding |
| Splash / theme | ⚠️ | SVG splash; falta link apple-touch |
| Service Worker arquivo dedicado | ❌ | Migrar de Blob |
| Cache versionado + cleanup | ❌ | |
| Navigation Preload | ❌ | |
| `.nojekyll` | ✅ | |

### Capacidades PWA

| Item | Velora | Prioridade Knowledge OS |
|------|--------|-------------------------|
| Offline Mode (app funcional) | ✅ | Dados localStorage |
| Install Prompt | ⚠️ | Menu ⋯; falta UI redesign pill |
| Shortcuts | ⚠️ | manifest.json tem; Blob não |
| Web Share | ❌ | Compartilhar resultado |
| File Handling | ❌ | Import JSON arrastar |
| Background Sync | ❌ | Fase online |
| Push Notifications | ❌ | Baixa — opt-in futuro |
| Periodic Background Sync | ❌ | Revisão espaçada reminder |
| Badging | ❌ | Cards due count |
| Launch Handler | ❌ | Desktop |

### Performance / qualidade

| Item | Velora |
|------|--------|
| Lighthouse PWA | ⚠️ ~70–85 estimado |
| Core Web Vitals | ⚠️ HTML monolítico grande |
| Code splitting | ❌ |
| Lazy loading imagens | ⚠️ |
| SEO | ⚠️ meta básica |
| A11y | ⚠️ touch 44px ok |

### Cross-browser

| Plataforma | Expectativa |
|------------|-------------|
| Android Chrome | Install full, SW robusto |
| iOS Safari | Install A2HS, SW cache limitado, sem push |
| Desktop Chrome/Edge | Install + shortcuts |
| Firefox | Install limitado, SW ok |
| Linux/macOS | PWA desktop Chromium |

---

## 3. Arquitetura proposta

### Fase A — Evoluir monolito (curto prazo, GitHub Pages)

```
prova-publish/
├── index.html              # app (mantém)
├── 404.html
├── sw.js                   # NOVO — SW estático versionado
├── manifest.webmanifest    # NOVO — estático na raiz (link rel=manifest)
├── branding/               # assets cacheados
└── docs/
```

**Por quê:** GitHub Pages serve arquivos estáticos; SW em arquivo separado é cacheável e auditável.

### Fase B — Build moderno (médio prazo)

```
velora-app/
├── vite.config.ts          # vite-plugin-pwa
├── src/
│   ├── main.tsx
│   ├── sw/                 # Workbox injectManifest
│   │   └── sw.ts
│   ├── data/               # KnowledgeRepository
│   └── ui/
├── public/
│   └── manifest.webmanifest
└── dist/                   # deploy → gh-pages
```

**Stack:** Vite + TypeScript + Workbox (`injectManifest` ou `generateSW`). React **somente** quando extrair views do monolito — não obrigatório dia 1.

**Next.js:** só se precisar SSR/SEO marketing; **Knowledge OS offline-first → Vite SPA** é melhor fit.

### Princípios

- **Offline First** para shell + dados do usuário (IndexedDB).
- **Network First** para sync/API futura.
- **Stale While Revalidate** para assets estáticos (branding, fonts).
- **Cache First** só para fonts/icons imutáveis com hash.

---

## 4. Estratégia de cache

### O que cachear

| Recurso | Estratégia | TTL / versão |
|---------|------------|--------------|
| `index.html`, `404.html` | Network First ou SWR | Revalidar sempre; hash no precache |
| `sw.js` | Network Only | Nunca cache longo |
| `branding/**` | SWR | `velora-static-{buildId}` |
| `exin_dpo_bank_data.json` | Cache First após 1ª carga | Versionado com build |
| Fonts (se CDN) | Cache First | Longo, com hash |

### Nunca cachear

- Respostas `POST`/`PUT`/`DELETE`
- URLs com auth tokens
- Respostas `opaque` não intencionais
- HTML de erro (4xx/5xx)
- Blob URLs temporários

### Invalidação

```javascript
// Padrão Workbox na activate
const CURRENT = 'velora-shell-v3';
const KEEP = [CURRENT, 'velora-runtime-v3'];
caches.keys().then(keys =>
  Promise.all(keys.filter(k => !KEEP.includes(k)).map(k => caches.delete(k)))
);
```

### Evitar cache infinito

- Prefixos separados: `shell`, `runtime`, `images`
- Limite runtime: Workbox `ExpirationPlugin` (maxEntries, maxAgeSeconds)
- **Nunca** `cache.put` cego em todo GET (bug atual)

### Dados do usuário

**Não** vão para Cache API — vão para **IndexedDB** (`ef_knowledge_*`). Cache API = assets de rede; IDB = conhecimento e progresso.

---

## 5. Fluxo offline (Velora)

```
┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│ 1º acesso    │────▶│ SW install  │────▶│ Precache     │
│ online       │     │ + manifest  │     │ shell+brand  │
└──────────────┘     └─────────────┘     └──────────────┘
        │                                        │
        ▼                                        ▼
┌──────────────┐                          ┌──────────────┐
│ Seed EXIN /  │                          │ IndexedDB    │
│ import JSON  │─────────────────────────▶│ Knowledge    │
└──────────────┘                          └──────────────┘

Offline depois:
  UI lê IDB/localStorage → simulado/cards 100% local
  Topbar pill "Offline" → NUNCA bloqueia

Reconexão:
  Background sync (futuro) → fila export/backup
  Toast "Sincronizado" (UI-REDESIGN-MODEL)
```

| Cenário | Comportamento |
|---------|---------------|
| Primeiro acesso online | SW + seed; dados gravados local |
| Offline total | App abre; estuda; histórico local |
| Reconexão | Pill → Online; sync opcional background |
| SW update | Banner “Nova versão — Atualizar” antes de `skipWaiting` |
| Fallback rede | Só para assets não precached — nunca tela morta |

---

## 6. Segurança

| Controle | Recomendação Velora |
|----------|---------------------|
| HTTPS | GitHub Pages ✅ |
| CSP | `default-src 'self'; script-src 'self'; worker-src 'self';` — elimina SW Blob |
| Permissions-Policy | Restringir camera/mic se não usar |
| SW scope | `/` na raiz do deploy |
| Cache poisoning | Só cachear same-origin; validar `response.ok` |
| XSS | `Util.escapeHtml` já usado — manter; CSP strict |
| SRI | Scripts externos com integrity (hoje sem deps ✅) |
| Headers | `_headers` no Netlify ou meta CSP no HTML |

---

## 7. Performance

| Técnica | Aplicação |
|---------|-----------|
| Monolito ~5000 linhas | Fase B: split por route lazy |
| Brotli | GitHub Pages gzip automático |
| Preload | `app-icon.svg`, font Inter |
| AVIF/WebP | Ícones PNG já; imagens questões lazy |
| Critical CSS | Inline `#ef-onepage-css` top — ok para Fase A |
| `requestIdleCallback` | Knowledge Phase 1 validation |

**Lighthouse 100:** exige SW arquivo dedicado, manifest estático, contrast a11y, tap targets, meta description, valid apple-touch-icon.

---

## 8. UX (alinhado UI-REDESIGN-MODEL)

| Estado | Padrão Velora |
|--------|---------------|
| Offline | Pill topbar — app utilizável |
| Sync | Toast discreto ao reconectar |
| Update SW | Bottom sheet / banner — não reload mid-exam |
| Install | Menu ⋯ + `beforeinstallprompt` |
| Loading | Skeleton na biblioteca |
| Empty | Biblioteca vazia → CTA importar |
| Error | Toast + retry — nunca modal bloqueante |

---

## 9. Código de referência (produção)

### `manifest.webmanifest` (raiz)

```json
{
  "id": "/prova/",
  "name": "Velora — Knowledge OS",
  "short_name": "Velora",
  "description": "Plataforma de estudos offline-first.",
  "start_url": "/prova/",
  "scope": "/prova/",
  "display": "standalone",
  "orientation": "any",
  "background_color": "#0B0E14",
  "theme_color": "#0B0E14",
  "lang": "pt-BR",
  "icons": [
    { "src": "/prova/branding/assets/png/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any" },
    { "src": "/prova/branding/assets/png/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ],
  "shortcuts": [
    { "name": "Continuar", "url": "/prova/#home", "icons": [{ "src": "/prova/branding/favicon/favicon.svg", "sizes": "96x96" }] },
    { "name": "Biblioteca", "url": "/prova/#content" }
  ],
  "file_handlers": [
    {
      "action": "/prova/#import",
      "accept": { "application/json": [".json"], "text/csv": [".csv"] }
    }
  ]
}
```

Ajuste paths ao base URL real (`/prova/` no GitHub Pages).

### `sw.js` (Workbox CDN ou bundle — exemplo manual enxuto)

```javascript
const SHELL_CACHE = 'velora-shell-v2';
const RUNTIME_CACHE = 'velora-runtime-v2';
const PRECACHE = [
  './',
  './index.html',
  './404.html',
  './branding/theme/theme.css',
  './branding/icons/app-icon.svg',
  './branding/logo/symbol-white.svg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(SHELL_CACHE).then((c) => c.addAll(PRECACHE)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== SHELL_CACHE && k !== RUNTIME_CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  if (PRECACHE.some((p) => url.pathname.endsWith(p.replace('./', '')))) {
    event.respondWith(caches.match(request).then((r) => r || fetch(request)));
    return;
  }

  event.respondWith(
    caches.open(RUNTIME_CACHE).then(async (cache) => {
      const cached = await cache.match(request);
      const fetchPromise = fetch(request).then((resp) => {
        if (resp.ok && resp.type === 'basic') cache.put(request, resp.clone());
        return resp;
      });
      return cached || fetchPromise.catch(() => cached);
    })
  );
});
```

### Registro + online/offline + update

```javascript
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/prova/sw.js').then((reg) => {
    reg.addEventListener('updatefound', () => {
      const nw = reg.installing;
      nw?.addEventListener('statechange', () => {
        if (nw.state === 'installed' && navigator.serviceWorker.controller) {
          Toast.show('Nova versão disponível. Atualize quando terminar o simulado.', 'warn');
        }
      });
    });
  });
}

window.addEventListener('online', () => document.body.dataset.network = 'online');
window.addEventListener('offline', () => document.body.dataset.network = 'offline');
```

---

## 10. Estratégias ideais para Knowledge OS

| Feature | Estratégia PWA |
|---------|----------------|
| Simulados | Dados 100% IDB; zero rede durante prova |
| Flashcards FSRS | IDB + Badging (cards due) |
| Biblioteca / grafo | Precache shell; conteúdo IDB |
| Import JSON | File Handling + leitura local |
| IA offline | Modelo/assets em IDB cache opcional |
| Sync nuvem (futuro) | Background Sync fila; Network First API |
| EXIN seed | Precache `exin_dpo_bank_data.json` ou embed IDB no seed |

**Por quê offline-first encaixa:** aprendizado não pode depender de rede — alinhado ao manifesto e screenshot “off-line” que **não deve bloquear**.

---

## 11. Roadmap PWA Velora

| Fase | Entrega | Impacto | Dificuldade | Prioridade |
|------|---------|---------|-------------|------------|
| **P1** | `sw.js` + `manifest.webmanifest` estáticos; remover Blob SW | Alto | Baixa | 🔴 |
| **P2** | Pill offline/online + remover tela bloqueante | Alto | Baixa | 🔴 |
| **P3** | Cache versionado + cleanup activate; precache list | Alto | Média | 🔴 |
| **P4** | IndexedDB para questões (Knowledge Fase 2–4) | Muito alto | Alta | 🟠 |
| **P5** | Workbox + Vite build; code split | Alto | Alta | 🟠 |
| **P6** | File handlers, shortcuts, screenshots install | Médio | Média | 🟡 |
| **P7** | Background sync, push, badging | Médio | Alta | 🟢 |

---

## 12. Resultado esperado

### Arquitetura final (diagrama)

```
                    ┌─────────────────┐
                    │   Manifest      │
                    │   (estático)    │
                    └────────┬────────┘
                             │
┌──────────┐    ┌────────────▼────────────┐    ┌─────────────┐
│ Browser  │───▶│ Service Worker (Workbox)│───▶│ Cache API   │
│ UI Shell │    │ precache + runtime      │    │ shell/runtime│
└────┬─────┘    └────────────┬────────────┘    └─────────────┘
     │                       │
     │              ┌────────▼────────┐
     └─────────────▶│ IndexedDB       │
                    │ Knowledge Graph │
                    │ progress, exams │
                    └────────┬────────┘
                             │ (online only)
                    ┌────────▼────────┐
                    │ Sync Queue      │
                    │ (enhancement)   │
                    └─────────────────┘
```

### Armadilhas comuns

1. SW Blob — impossível auditar/CSP  
2. Cache sem expiração — disco cheio mobile  
3. `skipWaiting` durante simulado — perda de sessão  
4. Assumir iOS = Android — testar Safari A2HS  
5. Cachear API — dados stale perigosos em sync  
6. Manifest `start_url` errado no subpath `/prova/`  

### Lighthouse 100 (checklist)

- [ ] SW registrado em arquivo dedicado  
- [ ] Manifest com ícones maskable + `id`  
- [ ] HTTPS  
- [ ] `<meta name="viewport">`  
- [ ] Contraste WCAG  
- [ ] Tap targets ≥ 44px  
- [ ] `theme-color`  
- [ ] Apple touch icon  
- [ ] Não registrar SW em `file://` (ok — guard já existe)  

### Installability

- **Android:** manifest + SW + ícones → prompt nativo  
- **iOS:** meta apple-mobile-web-app-capable + touch icon + orientação  
- **Desktop:** shortcuts + janela standalone  

---

## Referências cruzadas

- [PWA-AI-PROMPT.md](PWA-AI-PROMPT.md) — prompt para IA com artigo anexo  
- [UI-REDESIGN-MODEL.md](UI-REDESIGN-MODEL.md) — UX offline  
- [KNOWLEDGE-MODEL.md](KNOWLEDGE-MODEL.md) — IndexedDB / nós  
- Implementação atual: `index.html` → `App._setupPWA()`
