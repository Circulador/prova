# Velora — Brief para assistentes de IA

> **Uso:** copie este documento (ou seções) ao pedir apoio a outra IA sobre o projeto.  
> **App ao vivo:** https://circulador.github.io/prova/  
> **Repositório:** https://github.com/Circulador/prova  
> **Workspace local:** monolito em `index.html` + `404.html` (~5600 linhas), GitHub Pages, PWA.

---

## O que é

**Velora** é um **Knowledge Operating System** para formação em **privacidade, proteção de dados e certificações DPO** — não um simples banco de questões.

O usuário-alvo principal estuda certificações nacionais e internacionais (EXIN, IAPP, LGPD, GDPR, etc.) e quer **passar na prova**, **reter conhecimento** e **aplicar no trabalho**, muitas vezes aprendendo **inglês junto** (conteúdo bilingue EN/PT).

---

## Princípio central

```
Knowledge Node (conceito canônico)
        │
        ├── Questão (view)
        ├── Flashcard (view)
        ├── Explicação / Feynman / analogia (views — roadmap)
        ├── Caso prático (view — roadmap)
        └── Tutor IA (stub: botão ✨ Explicar)
```

- Um conceito existe **uma vez** (ex.: base legal LGPD art. 7º).
- Várias certificações podem referenciar o **mesmo nó**.
- Questões são **uma visualização** do nó — não a entidade primária.

**Docs canônicas:** `docs/PRIVACY-KNOWLEDGE-OS.md`, `docs/MANIFESTO-ARQUITETURA.md`, `docs/KNOWLEDGE-MODEL.md`.

---

## Stack e deploy

| Aspecto | Detalhe |
|---------|---------|
| Frontend | HTML/CSS/JS vanilla — **um único `index.html`** (sem framework) |
| Hospedagem | GitHub Pages (`/prova/` como base path) |
| Dados | `localStorage` no navegador (offline-first) |
| PWA | `manifest.webmanifest`, `sw.js`, instalável |
| Conteúdo seed | `data/dpo-global-bank.js` (~301 questões, 19 certs, 5 trilhas) |
| Sync | `sync_dpo_global.py` copia bloco JS/CSS de `index.html` → `404.html` |

**Regra:** mobile-first, bottom nav (&lt;1024px), sidebar (≥1024px), nunca bloquear uso offline.

---

## Navegação (shell)

| Rota | Nome na UI | Função |
|------|------------|--------|
| `home` | Início | Dashboard: continuar, sessão inteligente, presets, trilhas por continente |
| `content` | Biblioteca | Certificações, questões, importação |
| `progress` | Progresso | Estatísticas, histórico |
| `builder` | — | Montagem de simulado (modal + player) |
| `settings` | Ajustes | Tema, fonte, idioma, PWA, preferências de estudo |
| `result` / `review` | — | Pós-sessão |

**Ajustes** abre via ícone ⚙ na topbar (rota `settings`). Deve incluir opção **Instalar aplicativo** (PWA).

---

## Conteúdo DPO global (v2)

- **~301 questões** autorais, alinhadas a outlines públicos — **não copia provas oficiais**.
- **19 certificações** (+ stubs): EXIN, IAPP, PECB, ISACA CDPSE, ISO 27701, CNIL, TÜV, UK GDPR, etc.
- **5 trilhas:** Global · Brasil · Europa · Américas · Ásia.
- **Bilingue EN/PT** — modo `dual`, `en` ou `pt` em Ajustes.
- **Estilo lúdico:** cenários do dia a dia (WhatsApp, academia, encomendas…).
- Seeder: `GlobalDPOSeeder` · flag: `ef_global_dpo_seeded_v2`.

Reset após deploy (console):

```javascript
localStorage.removeItem('ef_global_dpo_seeded_v2');
localStorage.removeItem('ef_cleanup_global_dpo_v2');
location.reload();
```

---

## Fluxo de estudo (SessionConfig)

1. **Home** — preset ou trilha → abre modal de configuração.
2. **Modal (`ExamConfigModal`)** — filtros, exclusões (dominadas/hoje/nunca vistas), shuffle, estratégias (sprint/maratona/CAT→smart review), export/import JSON de perfil.
3. **Player (`PlayerController`)** — treino ou simulado; pausar, explicar (IA), revisão pré-envio no simulado.
4. **Result / Review** — estatísticas e revisão de erros.

Objetivos simultâneos: **passar na prova** · **reter** · **aplicar no trabalho**.

---

## Estado da implementação (jul/2026)

### Pronto / publicado

- Banco DPO global v2 + seeder + cleanup de samples antigos
- Home com presets e trilhas por continente
- Modal com filtros metadata, estratégias, export/import
- Player com pausa, explicar, revisão simulado; **P1 UX** (footer 3 botões, menu ⋯, timer no topo)
- PWA: service worker, manifest, card **Instalar aplicativo** em Ajustes
- Spec Privacy Knowledge OS Fase 1 (`Question.nodeMeta`, taxonomy JSON)

### Em andamento / backlog

| Item | Descrição |
|------|-----------|
| Settings drawer | Manifesto pede drawer lateral, hoje é rota full-page |
| Knowledge OS Fase 2+ | Dual-write `ef_knowledge_nodes_v1`, views Feynman/analogia no player, dashboard tutor |
| Expandir stubs | AIGP, FIP, CIPP/A com mais questões |

---

## Arquivos-chave

| Arquivo | Papel |
|---------|-------|
| `index.html` / `404.html` | App monolítico (views, player, storage, PWA) |
| `data/dpo-global-bank.js` | Banco de questões |
| `sw.js` | Cache offline |
| `manifest.webmanifest` | Metadados PWA |
| `docs/PRIVACY-KNOWLEDGE-OS.md` | Roadmap Fases 1–6 |
| `docs/MANIFESTO-ARQUITETURA.md` | Requisitos obrigatórios |
| `docs/UI-REDESIGN-MODEL.md` | Shell offline-first |
| `AGENTS.md` | Guia para agentes Cursor |
| `branding/design-system/design-system.md` | Visual |

---

## Convenções para IA que for editar código

1. **Diff mínimo** — não refatorar o monolito sem pedido explícito.
2. **Seguir manifesto** — simplicidade percebida; complexidade só internamente.
3. **Mobile-first** — testar layout estreito; bottom nav intacta.
4. **Offline-first** — nunca depender de rede para fluxo core.
5. **Sincronizar** — após mudar `index.html`, rodar `python sync_dpo_global.py` para `404.html`.
6. **Não commitar** sem pedido do usuário (`sim`).
7. **Comunicação** — usuário prefere **português**.

---

## Prompt curto (copiar e colar)

```
Estou desenvolvendo o Velora (https://circulador.github.io/prova/) — Knowledge OS para certificações DPO/privacidade.

Stack: monolito index.html + localStorage + PWA no GitHub Pages.
Conteúdo: ~301 questões bilingues EN/PT, 19 certs, trilhas por continente.
Arquitetura: Knowledge Node como entidade; questões são uma view (docs/PRIVACY-KNOWLEDGE-OS.md).

Preciso de ajuda com: [DESCREVA A TAREFA]

Restrições: mobile-first, offline-first, diff mínimo, PT-BR, sync index→404 via sync_dpo_global.py.
Brief completo: docs/PLATFORM-BRIEF.md no repo.
```

---

## Contato / contexto pessoal

Plataforma criada para apoiar estudos de certificações DPO (nacionais e internacionais), com foco em retenção de longo prazo e inglês técnico em paralelo.
