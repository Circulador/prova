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
| **Início** | Estudar agora (~10 min) · Personalizar · Recentes · Continuar sessão · trilhas colapsadas · FAQ/Como usar |
| **Biblioteca** | Trilhas · Questões · Flashcards (FSRS, olho, estrela) · criar sessão · importar |
| **Progresso** | Mastery · lacunas · KPIs · seções colapsáveis · histórico configurável (5–Todas) |
| **Player** | Aprendizado / Prova · Esta/Todas (revelar) · Marcar · Explicar · menu ⋯ |
| **Ajustes** | Tema · idioma UI + questões · PWA · demo · limite de histórico |

### Modos de estudo (mesma trilha, views do mesmo conhecimento)

| Modo | Uso |
|------|-----|
| **Aprendizado** | Feedback imediato, lacunas, ~10 min (padrão) |
| **Flashcards** | FSRS do conteúdo selecionado |
| **Prova completa** | Cronômetro, revisão pré-envio, simulado |

---

## Missão

Três objetivos simultâneos:

1. **Avaliar domínio** — simulados, cronômetro, revisão, refazer erradas  
2. **Reter por anos** — FSRS, mastery score, Estudar agora / lacunas  
3. **Aplicar na prática** — cenários, casos, explicações (roadmap: grafo, Feynman)

---

## Conteúdo

O Velora aceita **qualquer matéria**: crie questões, importe CSV/JSON ou use conteúdo pré-carregado no deploy. Cada questão alimenta automaticamente flashcards, estatísticas, mastery e sessões inteligentes.

Formatos in-app: **JSON, CSV, TXT, HTML**. Roadmap: PDF, DOCX, EPUB, APKG.

---

## Como usar

Documentação completa in-app: **Início → FAQ** ou **Como usar**.

1. Abra [circulador.github.io/prova](https://circulador.github.io/prova/) (mobile first).
2. **Início → Estudar agora** — ~10 min, lacunas prioritárias (1 toque).
3. **Personalizar** — trilha + **Aprendizado · Flashcards · Prova** + quantidade.
4. **Biblioteca** — Trilhas (▶) · Questões (+) · Flashcards.
5. **Progresso** — mastery, **Estudar lacunas**, histórico 5–Todas.
6. **Ajustes** — idiomas, PWA, demo, limite de histórico.

### Reset após deploy

```javascript
localStorage.removeItem('ef_global_dpo_seeded_v2');
localStorage.removeItem('ef_cleanup_global_dpo_v2');
location.reload();
```

Reset total:

```javascript
['ef_questions','ef_exams','ef_qstats','ef_history','ef_session','ef_global_dpo_seeded_v2','ef_cleanup_global_dpo_v2']
  .forEach(k => localStorage.removeItem(k));
location.reload();
```

---

## Desenvolvimento

Princípios: mobile-first · offline-first · regra dos 3 cliques · diff mínimo no monolito.

```bash
python sync_dpo_global.py            # Sync index.html → 404.html
```

Roadmap Knowledge OS: [`docs/PRIVACY-KNOWLEDGE-OS.md`](docs/PRIVACY-KNOWLEDGE-OS.md)

---

## Estrutura

```
index.html / 404.html     # App monolítico (~7k linhas)
data/dpo-global-bank.js   # Conteúdo seed de exemplo (deploy)
sw.js                     # Service Worker
manifest.webmanifest      # PWA
docs/                     # Specs canônicas
branding/                 # Logo, favicon, design tokens
sync_dpo_global.py        # Sync index → 404
```

---

## Licença

Ver histórico e contribuições em [Circulador/prova](https://github.com/Circulador/prova).
