# Velora — Knowledge Operating System

**Acesse o app:** [https://circulador.github.io/prova/](https://circulador.github.io/prova/)

Velora é um **Sistema Operacional de Conhecimento** para formação em privacidade e DPO: questões, flashcards, simulados, importações e IA são **visualizações do mesmo conhecimento conectado** — não módulos isolados.

**Arquitetura (obrigatória):** [`docs/MANIFESTO-ARQUITETURA.md`](docs/MANIFESTO-ARQUITETURA.md)  
**Privacy Knowledge OS:** [`docs/PRIVACY-KNOWLEDGE-OS.md`](docs/PRIVACY-KNOWLEDGE-OS.md)  
**Brief para outras IAs:** [`docs/PLATFORM-BRIEF.md`](docs/PLATFORM-BRIEF.md)  
**Trilhas DPO global:** [`docs/DPO-GLOBAL-TRACKS.md`](docs/DPO-GLOBAL-TRACKS.md)  
**Design visual:** [`branding/design-system/design-system.md`](branding/design-system/design-system.md)  
**Agentes Cursor:** [`AGENTS.md`](AGENTS.md)

Tudo roda em HTML estático (GitHub Pages) — offline-first, mobile-first, com PWA.

---

## Missão

Criar a melhor plataforma de estudos do mundo. O usuário nunca deve sentir complexidade; toda a profundidade fica na arquitetura interna.

Três objetivos simultâneos:

1. **Passar na prova** — simulados, presets, revisão inteligente  
2. **Reter por anos** — repetição espaçada, analogias, storytelling  
3. **Aplicar no trabalho** — casos práticos, comparativo multi-país (roadmap)

---

## Conteúdo DPO global (v2)

Banco autoral alinhado a outlines públicos de certificações — **não copia provas oficiais**.

| Métrica | Valor |
|---------|-------|
| Questões | ~301 |
| Certificações | 19 (+ 2 stubs) |
| Trilhas | Global · Brasil · Europa · Américas · Ásia |
| Idioma | Bilingue **EN/PT** (modo dual no app) |
| Estilo | Cenários lúdicos do dia a dia (WhatsApp, academia, encomendas…) |

Certificações incluídas: EXIN (ISFS, PDPF, PDPP, CDPO, LGPD), IAPP (CIPP/E, CIPM, CIPT, CDPO/BR, CDPO/FR, CIPP/US), PECB, ISACA CDPSE, ISO 27701, CNIL, TÜV DE, UK GDPR e mais.

Dados em [`data/dpo-global-bank.js`](data/dpo-global-bank.js) · inventário completo em [`docs/DPO-GLOBAL-TRACKS.md`](docs/DPO-GLOBAL-TRACKS.md).

---

## Pilares do produto

| Pilar | Descrição |
|-------|-----------|
| **Knowledge Graph** | Conteúdo em nós únicos — schema v2 em [`docs/KNOWLEDGE-MODEL.md`](docs/KNOWLEDGE-MODEL.md) |
| **Estudo** | Simulado, treino, sessão inteligente, presets (Completo / Rápido / Só erros) |
| **Cards** | Flashcards com repetição espaçada (FSRS) |
| **Biblioteca** | Certificações por continente, importação via adaptadores |
| **Progresso** | Estatísticas, histórico, evolução |
| **IA invisível** | ✨ Explicar — contextual, sem menu "IA" |
| **PWA** | Instalável, cache offline do shell + banco (`sw.js`) |

---

## Como usar

1. Abra [circulador.github.io/prova](https://circulador.github.io/prova/) no navegador (mobile first).
2. **Início** — Continuar, Sessão inteligente, presets, certificações por trilha.
3. **Biblioteca** — certificações, questões, importar.
4. **Progresso** — estatísticas e histórico.
5. **Configurar simulado** — exclusões (já acertadas, hoje, nunca vistas), embaralhar, cronômetro.
6. **Player** — Pausar, Explicar, revisão pré-envio (simulado).
7. **Ajustes → Instalar aplicativo** — PWA offline (card dedicado com status e instruções iOS/Android).
8. Idioma das questões em **Ajustes** — `dual` (EN+PT), `en` ou `pt`.

### Atualizar conteúdo após deploy

Se ainda vir banco antigo, no console do navegador:

```javascript
localStorage.removeItem('ef_global_dpo_seeded_v2');
localStorage.removeItem('ef_cleanup_global_dpo_v2');
location.reload();
```

Reset total (histórico + stats):

```javascript
['ef_questions','ef_exams','ef_qstats','ef_history','ef_session','ef_global_dpo_seeded_v2','ef_cleanup_global_dpo_v2']
  .forEach(k => localStorage.removeItem(k));
location.reload();
```

---

## Formatos suportados (importação)

PDF · DOCX · PPTX · EPUB · HTML · Markdown · TXT · CSV · JSON · imagens · áudio · vídeo

> Importação direta no app: **JSON, CSV, TXT e HTML**. Outros formatos passam por adaptadores ou conversão prévia.

---

## Desenvolvimento

Princípios inegociáveis antes de qualquer PR:

- Mobile First (smartphone → tablet → desktop ≥ 1024px)
- Regra dos 3 cliques
- One Page First (modal/drawer antes de nova página)
- Gate de 15 perguntas — ver manifesto

### Scripts úteis

```bash
# Regenerar banco DPO global
python generate_dpo_global_bank.py

# Sincronizar index.html → 404.html (seeder + modal)
python sync_dpo_global.py
python sync_exam_modal.py
```

### Roadmap Privacy Knowledge OS (Fases 1–6)

Ver [`docs/PRIVACY-KNOWLEDGE-OS.md`](docs/PRIVACY-KNOWLEDGE-OS.md). Próximo: dual-write `ef_knowledge_nodes_v1`, learning views no player (Feynman, analogia, mnemônico).

---

## Estrutura do repositório

```
docs/
  MANIFESTO-ARQUITETURA.md      # Requisitos arquiteturais
  PRIVACY-KNOWLEDGE-OS.md       # Spec certificações privacidade
  KNOWLEDGE-MODEL.md            # Schema Knowledge Node v1 + v2
  DPO-GLOBAL-TRACKS.md          # Inventário do banco
  UI-REDESIGN-MODEL.md          # Shell offline-first
  PWA-ARCHITECTURE.md           # Service Worker, manifest
data/
  dpo-global-bank.js            # Banco DPO global (offline)
  knowledge-taxonomy.json       # Taxonomia continente → lei/cert
  node-schema.example.json      # Nó v2 de referência
AGENTS.md                       # Guia para agentes Cursor
.cursor/rules/velora-*.mdc      # Regras automáticas
index.html / 404.html           # App monolítico
branding/                       # Identidade Velora, PWA
sw.js / manifest.webmanifest    # PWA offline
generate_dpo_global_bank.py     # Gerador do banco
sync_dpo_global.py              # Sync index → 404
```

---

## Licença e créditos

Ver histórico de commits e contribuições no repositório [Circulador/prova](https://github.com/Circulador/prova).
