# Velora — Knowledge Operating System

**Live app:** [https://circulador.github.io/prova/](https://circulador.github.io/prova/)

> *Bem-vindo ao Velora — pronto para evoluir hoje?*  
> Uma plataforma para **absorver, reter e aplicar conhecimento** — de múltiplas formas, no mesmo fluxo.  
> Feito com ❤️ para quem aprende todos os dias.

Velora é um **Knowledge OS**: questões, flashcards, simulados, sessões inteligentes e explicações são **visualizações do mesmo conhecimento conectado** — não módulos isolados.

| Doc | Link |
|-----|------|
| Arquitetura | [`docs/MANIFESTO-ARQUITETURA.md`](docs/MANIFESTO-ARQUITETURA.md) |
| Privacy Knowledge OS | [`docs/PRIVACY-KNOWLEDGE-OS.md`](docs/PRIVACY-KNOWLEDGE-OS.md) |
| Brief para IAs | [`docs/PLATFORM-BRIEF.md`](docs/PLATFORM-BRIEF.md) |
| Benchmark estratégico | [`docs/BENCHMARK-STRATEGIC.md`](docs/BENCHMARK-STRATEGIC.md) |
| Modelo de conhecimento | [`docs/KNOWLEDGE-MODEL.md`](docs/KNOWLEDGE-MODEL.md) |
| Design system | [`branding/design-system/design-system.md`](branding/design-system/design-system.md) |
| Agentes Cursor | [`AGENTS.md`](AGENTS.md) |

Stack: monolito HTML/CSS/JS · GitHub Pages · **offline-first** · **PWA** · mobile-first.

---

## O que o app faz hoje

| Área | Funcionalidades |
|------|-----------------|
| **Início** | Continuar (GPS ou sessão pausada) · Personalizar · Recentes · ▶ trilhas instantâneo · FAQ/Como usar |
| **Biblioteca** | Trilhas (▶ 1 toque · Layers progressivo) · Questões · Flashcards (FSRS) · importar · Forja |
| **Evolução** | Domínio · retenção 90d · lacunas · competências · histórico configurável (5–Todas) |
| **Player** | Aprendizado / Prova · Esta/Todas (revelar) · Marcar · Explicar · menu ⋯ |
| **Ajustes** | Tema · idioma UI + questões · PWA · demo · limite de histórico · meta GPS |

### Fluxo de sessão (sem fricção)

| Ação | Comportamento |
|------|----------------|
| **Continuar** | Retoma sessão pausada ou rota GPS (~10 min) |
| **▶ trilha** | Aprendizado · 10 questões · embaralhar (sem modal) |
| **Personalizar** | Modal enxuto: Aprendizado ou Prova · quantidade · filtros |
| **Layers** | Modo progressivo (Biblioteca) |
| **Flashcards** | Aba Flashcards na Biblioteca |

---

## Missão

Três objetivos simultâneos:

1. **Avaliar domínio** — simulados, cronômetro, revisão, refazer erradas  
2. **Reter por anos** — FSRS, mastery score, GPS / lacunas  
3. **Aplicar na prática** — cenários, casos, explicações (roadmap: grafo, Feynman)

---

## Conteúdo

O Velora aceita **qualquer matéria**: crie questões, importe CSV/JSON ou use conteúdo pré-carregado no deploy. Cada questão alimenta automaticamente flashcards, estatísticas, mastery e sessões inteligentes.

Formatos in-app: **JSON, CSV, TXT, HTML**. Roadmap: PDF, DOCX, EPUB, APKG.

---

## Como usar

Documentação completa in-app: **Início → FAQ** ou **Como usar**.

1. Abra [circulador.github.io/prova](https://circulador.github.io/prova/) (mobile first).
2. **Início → Continuar** — retoma sessão ou rota GPS personalizada.
3. **▶ em uma trilha** — Aprendizado · 10 questões (1 toque).
4. **Personalizar** — trilha + **Aprendizado · Prova** + quantidade + filtros.
5. **Biblioteca** — Trilhas (▶ · Layers) · Questões · Flashcards.
6. **Evolução** — domínio, retenção, **Estudar lacunas**, histórico 5–Todas.
7. **Ajustes** — idiomas, PWA, demo, meta GPS.

### Reset após deploy

```javascript
localStorage.removeItem('ef_knowledge_os_seeded_v3');
localStorage.removeItem('ef_cleanup_knowledge_os_v3');
location.reload();
```

Reset total:

```javascript
[
  'ef_questions','ef_exams','ef_qstats','ef_history','ef_session',
  'ef_knowledge_os_seeded_v3','ef_cleanup_knowledge_os_v3','ef_session_preset_v1'
].forEach(k => localStorage.removeItem(k));
location.reload();
```

---

## Desenvolvimento

Princípios: mobile-first · offline-first · regra dos 3 cliques · diff mínimo no monolito.

```bash
python sync_dpo_global.py            # Sync index.html → 404.html
python tools/browser_check.py        # Smoke test (headless)
python tools/cdp_compile.py          # Verifica parse JS
```

Roadmap Knowledge OS: [`docs/PRIVACY-KNOWLEDGE-OS.md`](docs/PRIVACY-KNOWLEDGE-OS.md)

---

## Estrutura

```
index.html / 404.html     # App monolítico (~8.7k linhas)
data/dpo-global-bank.js   # Conteúdo seed de exemplo (deploy)
gps/velora-gps.js         # Knowledge GPS v2
sw.js                     # Service Worker
manifest.webmanifest      # PWA
docs/                     # Specs canônicas
branding/                 # Logo, favicon, design tokens
sync_dpo_global.py        # Sync index → 404
tools/                    # browser_check, cdp_compile
```

---

## Licença

Ver histórico e contribuições em [Circulador/prova](https://github.com/Circulador/prova).
