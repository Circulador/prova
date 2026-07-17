# Velora — Knowledge Operating System

**Live app:** [https://circulador.github.io/prova/](https://circulador.github.io/prova/)

> *Bem-vindo ao Velora — pronto para evoluir hoje?*  
> O lugar onde **conhecimento, prática e certificações** se unem numa jornada contínua de aprendizado.  
> Feito com ❤️ para quem aprende todos os dias.

Velora é um **Knowledge OS** para formação em privacidade e DPO: questões, flashcards, simulados e IA são **visualizações do mesmo conhecimento conectado** — não módulos isolados.

| Doc | Link |
|-----|------|
| Arquitetura | [`docs/MANIFESTO-ARQUITETURA.md`](docs/MANIFESTO-ARQUITETURA.md) |
| Privacy Knowledge OS | [`docs/PRIVACY-KNOWLEDGE-OS.md`](docs/PRIVACY-KNOWLEDGE-OS.md) |
| Brief para IAs | [`docs/PLATFORM-BRIEF.md`](docs/PLATFORM-BRIEF.md) |
| Benchmark estratégico | [`docs/BENCHMARK-STRATEGIC.md`](docs/BENCHMARK-STRATEGIC.md) |
| Trilhas DPO global | [`docs/DPO-GLOBAL-TRACKS.md`](docs/DPO-GLOBAL-TRACKS.md) |
| Design system | [`branding/design-system/design-system.md`](branding/design-system/design-system.md) |
| Agentes Cursor | [`AGENTS.md`](AGENTS.md) |

Stack: monolito HTML/CSS/JS · GitHub Pages · **offline-first** · **PWA** · mobile-first.

---

## O que o app faz hoje

| Área | Funcionalidades |
|------|-----------------|
| **Início** | Estudar agora (~10 min) · Personalizar · Recentes · Continuar sessão · trilhas colapsadas · FAQ/Como usar |
| **Biblioteca** | Certificações · Questões · Flashcards (FSRS, olho fixo, estrela) · criar exame · importar |
| **Progresso** | Mastery · lacunas · KPIs · seções colapsáveis · histórico configurável (5–Todas) |
| **Player** | Aprendizado / Prova · Esta/Todas (revelar) · Marcar · Explicar · menu ⋯ |
| **Ajustes** | Tema · idioma UI + questões · PWA · demo · limite de histórico |

---

## Missão

Três objetivos simultâneos:

1. **Passar na prova** — sessões tipo prova, cronômetro, revisão pré-envio, refazer erradas  
2. **Reter por anos** — FSRS, mastery score, Estudar agora / lacunas  
3. **Aplicar no trabalho** — casos práticos, comparativo multi-país (roadmap)

---

## Conteúdo DPO global (v2)

Banco autoral alinhado a outlines públicos — **não copia provas oficiais**.

| Métrica | Valor |
|---------|-------|
| Questões | ~301 |
| Certificações | 19 (+ 2 stubs) |
| Trilhas | Global · Brasil · Europa · Américas · Ásia |
| Idioma das questões | Bilingue **EN/PT** (dual, en ou pt) |
| Idioma da UI | **Português (BR)** ou **English (US)** |
| Estilo | Cenários lúdicos do dia a dia |

Certificações: EXIN, IAPP, PECB, ISACA CDPSE, ISO 27701, CNIL, TÜV, UK GDPR e mais — ver [`docs/DPO-GLOBAL-TRACKS.md`](docs/DPO-GLOBAL-TRACKS.md).

Dados: [`data/dpo-global-bank.js`](data/dpo-global-bank.js)

---

## Como usar

Documentação completa in-app: **Início → FAQ** ou **Como usar** (busca por tema).

1. Abra [circulador.github.io/prova](https://circulador.github.io/prova/) (mobile first).
2. **Início → Estudar agora** — sessão ~10 min em modo Aprendizado (lacunas prioritárias).
3. **Personalizar** — prova, quantidade (10/20/Todas), Aprendizado vs Prova completa, opções avançadas.
4. **Biblioteca** — Certificações (▶) · Questões (+) · Flashcards (FSRS + olho/estrela).
5. **Progresso** — mastery, lacunas, **Estudar lacunas**; histórico com dropdown 5–Todas.
6. **Player** — botões **Esta** / **Todas** (revelar) · **Marcar** no rodapé · **Explicar** no menu ⋯.
7. **Personalizar / ▶ Biblioteca** — escolha **Aprendizado · Flashcards · Prova** (padrão: Aprendizado).
8. **Ajustes** — idioma plataforma vs questões, PWA, limite de histórico, dados demo.

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

## Importação

Formatos no app: **JSON, CSV, TXT, HTML**. Roadmap: PDF, DOCX, EPUB, APKG — ver manifesto.

---

## Desenvolvimento

Princípios: mobile-first · offline-first · regra dos 3 cliques · diff mínimo no monolito.

```bash
python generate_dpo_global_bank.py   # Regenerar banco DPO
python sync_dpo_global.py            # Sync index.html → 404.html
```

Roadmap Knowledge OS (Fases 2–6): [`docs/PRIVACY-KNOWLEDGE-OS.md`](docs/PRIVACY-KNOWLEDGE-OS.md)

---

## Estrutura

```
index.html / 404.html     # App monolítico (~6k linhas)
data/dpo-global-bank.js   # Banco DPO offline
sw.js                     # Service Worker
manifest.webmanifest      # PWA
docs/                     # Specs canônicas
branding/                 # Logo, favicon, design tokens
sync_dpo_global.py        # Sync index → 404
```

---

## Licença

Ver histórico e contribuições em [Circulador/prova](https://github.com/Circulador/prova).
