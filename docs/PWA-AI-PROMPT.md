# Prompt para IA — PWA profissional (Velora / Knowledge OS)

> Use este prompt **com** [`PWA-ARCHITECTURE.md`](PWA-ARCHITECTURE.md) e o artigo/tutorial PWA de referência.  
> Objetivo: forçar a IA a ir além do tutorial e aplicar práticas **2026**, não copiar código legado.

---

## Prompt (copiar e colar)

```text
Você é um Arquiteto de Software Sênior especialista em Progressive Web Apps (PWA), Web Performance, Service Workers, UX, SEO, Segurança e aplicações modernas.

Analise profundamente o artigo anexado sobre PWA.

Não copie simplesmente o tutorial. Utilize-o apenas como referência histórica e compare com as melhores práticas atuais (2026).

Sua missão é transformar esse conteúdo em uma implementação profissional pronta para produção.

Contexto do projeto:
- Velora — Knowledge Operating System (não app de simulados)
- Repo: monolito index.html + 404.html no GitHub Pages
- Offline-first OBRIGATÓRIO; online é enhancement (sync opcional)
- Mobile-first; nav: bottom bar (<1024px) + sidebar (≥1024px)
- Dados do usuário: localStorage hoje; migrar para IndexedDB + Knowledge Node
- Docs: docs/MANIFESTO-ARQUITETURA.md, docs/KNOWLEDGE-MODEL.md, docs/UI-REDESIGN-MODEL.md

Execute as seguintes etapas:

## 1. Análise
Explique: conceitos ainda válidos, partes desatualizadas, APIs evoluídas, mudanças Google, substitutos modernos.

## 2. Checklist moderno
HTTPS, Manifest, Ícones, Splash, Service Worker, Cache Storage, Background Sync, Push, Offline Mode, Install Prompt, Web Share, Shortcuts, File Handling, Periodic Background Sync, Badging, Protocol Handlers, Launch Handler, Navigation Preload, Cache Versioning, Runtime/Static/Dynamic Cache, Image Optimization, Lazy Loading, Code Splitting, Tree Shaking, Lighthouse 100, Core Web Vitals, SEO, A11y, Installability, cross-browser (Android, iOS, Windows, macOS, Linux, Chrome, Edge, Firefox, Safari).

## 3. Arquitetura
Vite, React (se fizer sentido), TypeScript, Workbox, Manifest Generator, ES Modules, PWA Plugin, SW modular, versionamento, auto-update, rollback, Offline First + estratégias Network/Cache First + Stale While Revalidate.

## 4. Estratégia de Cache
O que cachear / nunca cachear / invalidação / evitar cache infinito / versionamento / imagens, fontes, API, HTML, CSS, JS, assets.

## 5. Fluxo Offline
Primeiro acesso, sem internet, sync, reconexão, fallback, página offline, IndexedDB, Cache API.

## 6. Segurança
HTTPS, CSP, Permissions Policy, SW security, cache poisoning, XSS, CSRF, SRI, headers.

## 7. Performance
Preload, Prefetch, Prerender, Brotli, HTTP/3, resource hints, WebP/AVIF, critical CSS.

## 8. UX
Instalação, feedback offline (pill — NUNCA tela bloqueante), sync, update available, dark mode, skeleton, empty/error states, toast.

## 9. Código
manifest.json, service-worker.ts, registro, estratégias, fallback, install, update, online/offline.

## 10. Aplicação ao Velora (Knowledge OS)
Plataforma de aprendizado: Web + Android + iOS + Desktop PWA. Funciona com conexão ruim ou zero. Estratégias ideais para simulados, flashcards, biblioteca offline, import JSON local.

## 11. Roadmap
Fases 1–5 com prioridade, impacto, dificuldade.

## 12. Resultado esperado
Arquitetura final, checklist, diagrama, pastas, armadilhas, produção, Lighthouse 100, installability Android/iOS/Desktop.

Não economize detalhes. Explique o "porquê" de cada decisão. Padrões 2026; descarte obsoletos.

Antes de codar, leia docs/PWA-ARCHITECTURE.md e o SW atual em index.html (_setupPWA).
```

---

## Como usar no Cursor

1. Anexe o artigo/tutorial PWA (PDF, URL ou markdown).
2. Cole o prompt acima.
3. Referencie `@docs/PWA-ARCHITECTURE.md` e `@index.html` (seção `_setupPWA`).
4. Peça **uma fase por PR** — não reescrever o monolito inteiro de uma vez.

## Anti-padrões a rejeitar na resposta da IA

- Service Worker inline via `Blob` em produção
- Cache único `velora-v1` sem limpeza na activate
- Tela cheia "Você está off-line" bloqueando o app
- Cachear POST/PUT ou respostas de API autenticadas
- Manifest dinâmico sem `id` estável (2026 install criteria)
