# Velora — Privacy Knowledge OS

> **Status:** especificação canônica · **Versão:** 1.0.0  
> **Escopo:** transformar o Velora de banco de questões em **Knowledge OS para Certificações de Privacidade**  
> **Princípio central:** questões são **uma visualização** de um Nó de Conhecimento — não a entidade primária.

---

## 1. Visão

O Velora evolui de simulador de provas para um **sistema operacional de conhecimento em privacidade, proteção de dados e governança**, capaz de:

1. **Passar na certificação** (objetivo de curto prazo)
2. **Reter conhecimento por anos** (ciência da aprendizagem)
3. **Aplicar no trabalho** (casos, incidentes, decisões regulatórias)

Tudo **offline-first**, **mobile-first** e dentro da **regra dos 3 cliques**.

---

## 2. Princípio arquitetural

```
                    ┌─────────────────────────┐
                    │   Knowledge Node (nó)    │
                    │   — conceito canônico    │
                    └───────────┬─────────────┘
                                │
        ┌───────────┬───────────┼───────────┬───────────┐
        ▼           ▼           ▼           ▼           ▼
   Questão    Flashcard   Explicação   Caso prático   Tutor IA
   (view)      (view)       (views)      (view)        (stub)
```

- Um conceito existe **uma vez** (ex.: *base legal LGPD art. 7º*)
- Múltiplas certificações podem **referenciar o mesmo nó**
- Múltiplos idiomas compartilham o **mesmo `nodeId`**
- Importadores (CSV, JSON, XML, APKG) são **adaptadores**, nunca fonte da verdade

**Referências técnicas:** [KNOWLEDGE-MODEL.md](KNOWLEDGE-MODEL.md) · [MANIFESTO-ARQUITETURA.md](MANIFESTO-ARQUITETURA.md)

---

## 3. Taxonomia de conteúdo

### 3.1 Global (transversal)

| Área | Exemplos |
|------|----------|
| GDPR | Regulamento UE, adequação, DPO |
| ISO 27701 | PIMS, extensão ISO 27001 |
| ISO 27001 (privacidade) | Controles, SoA, risco |
| NIST Privacy Framework | Identify, Govern, Control |
| OECD | Princípios transfronteiriços |
| APEC / CBPR | Cross-border, accountability |
| Cross-border | Transferências, SCCs, BCRs |
| AI Governance | NIST AI RMF, ISO 42001 |
| AI Act (UE) | Risco, GPAI, DPO-like roles |
| Data Governance | Qualidade, linhagem, stewardship |
| Data Ethics | Fairness, bias, transparência |

### 3.2 Por região

| Região | Certificações / leis |
|--------|----------------------|
| **UE** | CIPP/E, CIPM, CIPT, GDPR Specialist, DPO, ePrivacy, AI Act |
| **EUA** | CIPP/US, HIPAA, GLBA, COPPA, FERPA, CCPA, CPRA, leis estaduais |
| **Canadá** | CIPP/C, PIPEDA, Quebec Law 25 |
| **Brasil** | LGPD, ENAP DPO, ANPD, certificações nacionais |
| **Reino Unido** | UK GDPR, DPA 2018 |
| **Ásia** | APPI (JP), PDPA (SG), India DPDP, PIPL (CN), PIPA (KR) |
| **Oceania** | Privacy Act AU, NZ Privacy Act |
| **África** | POPIA (ZA) |
| **LatAm** | Chile, Argentina, Uruguay, México, Colômbia, Peru… |

Estrutura hierárquica formal: [`data/knowledge-taxonomy.json`](../data/knowledge-taxonomy.json)

---

## 4. Metadados de questão (completos)

Cada visualização `question` herda metadados do nó pai:

| Campo | Descrição |
|-------|-----------|
| `certification` | Certificação alvo (ex.: IAPP-CIPP-E) |
| `country` | País de aplicação |
| `region` | Região (UE, LatAm, global…) |
| `continent` | Continente |
| `knowledgeArea` | Domínio temático |
| `difficulty` | fácil / médio / difícil |
| `estimatedMinutes` | Tempo estimado de resposta |
| `bloomLevel` | Taxonomia de Bloom (L1–L6) |
| `primaryLaw` | Lei principal (ex.: GDPR art. 6) |
| `secondaryLaw` | Lei secundária / norma correlata |
| `tags` | Etiquetas livres |
| `examObjective` | Objetivo oficial do syllabus |
| `officialReference` | Referência normativa / guia |
| `revisionHistory` | Histórico de revisões do nó |
| `language` | Idioma(s) da visualização |

Schema TypeScript completo: [KNOWLEDGE-MODEL.md § Schema v2.0](KNOWLEDGE-MODEL.md#14-schema-v20--privacy-certification-node)

---

## 5. Camadas de aprendizagem por nó

Além de Q&A, cada nó suporta **Learning Views**:

| View | Propósito | Exemplo |
|------|-----------|---------|
| `technical` | Explicação precisa para profissional | Artigos, requisitos legais |
| `simple` | Linguagem de 12 anos | Analogias curtas |
| `analogy` | Cotidiano (WhatsApp, iFood, Netflix, PIX) | "É como compartilhar a chave do apartamento…" |
| `story` | Narrativa (João, Maria, Carlos…) | Caso fictício completo |
| `feynman` | "Explique como se eu tivesse 10 anos" | Simplificação máxima |
| `mnemonic` | Mnemônicos | "LGPD = Lei Garante Privacidade Direito" |
| `visual` | Sugestões de associação visual | Ícones, diagramas sugeridos |

### Multilinguismo

- Idiomas alvo: **PT, EN, ES, FR, IT, DE, JA**
- Mesmo `nodeId` → bundles por locale (`LocaleBundle`)
- Integração EN: glossário, pronúncia, flashcards PT↔EN, expressões de exame

Exemplo completo: [`data/node-schema.example.json`](../data/node-schema.example.json)

---

## 6. Ciência da aprendizagem

| Técnica | Implementação Velora |
|---------|---------------------|
| Spaced repetition | FSRS (`ef_fsrs_cards_v2` → `node.progress.fsrs`) |
| Active recall | Player sem dicas; flashcards |
| Leitner | Caixas por domínio (futuro) |
| Interleaving | Sessão inteligente mistura domínios |
| Retrieval practice | Modo "só erros", revisão pré-envio |
| Forgetting curve | `due review`, predição IA (stub) |
| Bloom taxonomy | `bloomLevel` no metadata; filtros futuros |

---

## 7. Simuladores inteligentes

Filtros combináveis (arquitetura; UI incremental):

- Certificação, país, continente, idioma
- Lei, tema, capítulo, nível, objetivo
- Tempo, quantidade
- Mix de certs/países
- Modos: só erradas, só novas, favoritas, due review, predição de esquecimento (IA stub)

**Estado atual:** `SessionConfig` + Home presets + modal de exclusões (`index.html`)

---

## 8. Tutor IA (stub offline-first)

Arquitetura planejada — **sem backend obrigatório** na v1:

```
User prompt → TutorFacade (local)
              ├─ ContextBuilder (nó + progresso + cert)
              ├─ OfflineLLM / on-device (futuro)
              └─ Fallback: views pré-escritas (technical, feynman…)
```

Capacidades alvo: ensinar, explicar, adaptar dificuldade, gap analysis, plano de estudo, probabilidade de aprovação.

**Regra:** IA invisível — ações contextuais ✨, nunca menu "IA" ([MANIFESTO](MANIFESTO-ARQUITETURA.md)).

---

## 9. Dashboard

Métricas alvo (fase posterior):

- Probabilidade de aprovação
- Tempo restante até prova
- Conhecimento por domínio / lei / cert
- Heatmap, radar, curva de aprendizado
- Retenção e confiança IA

**Estado atual:** resumo de progresso na Home (`DashboardView`)

---

## 10. Arquitetura de escala

| Desafio | Estratégia |
|---------|------------|
| Milhões de questões | Nós canônicos + views; dedup via `duplicate_of` |
| Multi-cert por nó | `CertificationRef[]` no metadata |
| Multi-idioma | `LocaleBundle` linkado por `nodeId` |
| Versionamento | `revisionHistory`, `schemaVersion` |
| Bulk import | Adaptadores CSV/JSON/XML → `KnowledgeNormalizer` |
| Geração IA | Pipeline com **gate de QA humano** antes de publicar |

---

## 11. Três objetivos simultâneos

| Objetivo | Horizonte | Entregáveis |
|----------|-----------|-------------|
| Passar na prova | Dias/semanas | Simulador, revisão, FSRS due |
| Reter por anos | Meses/anos | Spaced rep, interleaving, mnemonics |
| Aplicar no trabalho | Contínuo | Casos, stories, decisões regulatórias |

---

## 12. Roadmap de implementação (Fases 1–6)

### Fase 1 — Fundação documental e schema ✅ (esta sessão)

| Entrega | Arquivo |
|---------|---------|
| Spec canônica | `docs/PRIVACY-KNOWLEDGE-OS.md` |
| Schema v2.0 | `docs/KNOWLEDGE-MODEL.md` §14 |
| Taxonomia | `data/knowledge-taxonomy.json` |
| Exemplo de nó | `data/node-schema.example.json` |
| Regras Cursor | `.cursor/rules/velora-privacy-knowledge-os.mdc` |
| Pass-through metadata | `GlobalDPOSeeder._normalizeQuestion` |
| Inventário DPO | `docs/DPO-GLOBAL-TRACKS.md` |

### Fase 2 — Migração Knowledge Node (dual-write)

| Entrega | Arquivo / classe |
|---------|------------------|
| Dual-write transparente | `KnowledgeRepository.upsertQuestion` |
| Metadata v2 no normalizer | `KnowledgeNormalizer.fromLegacyQuestion` |
| Flag de migração | `ef_knowledge_schema_v1.migrationPhase = 2` |
| Pass-through bank → node | `GlobalDPOSeeder` + `nodeMeta` em `Question` |

**Critério:** app idêntico para usuário; nós persistidos em `ef_knowledge_nodes_v1`.

### Fase 3 — Learning Views na UI

| Entrega | Descrição |
|---------|-----------|
| Abas no player | Técnico · Simples · Feynman · Analogia · História |
| Bilingue EN/PT | `QuestionDisplay` estendido |
| Glossário EN | Store `ef_glossary_v1` (stub) |

**Critério:** 3 cliques para alternar view; offline.

### Fase 4 — Simulador inteligente completo

| Entrega | Descrição |
|---------|-----------|
| Filtros avançados | Cert, lei, Bloom, due, favoritas |
| Mix multi-cert | `SessionConfig.filters` |
| Interleaving | Algoritmo de seleção por domínio |

**Critério:** presets Home + modal cobrem 80% dos casos.

### Fase 5 — Grafo e taxonomia navegável

| Entrega | Descrição |
|---------|-----------|
| Grafo persistido | Trilha → cert → domínio → nó |
| Biblioteca | Navega `knowledge-taxonomy.json` + links |
| Multi-cert dedup | Links `duplicate_of` |

**Critério:** biblioteca reflete taxonomia real, não só tags.

### Fase 6 — Tutor IA + Dashboard avançado

| Entrega | Descrição |
|---------|-----------|
| `TutorFacade` | Stub com views pré-escritas |
| Pass probability | Heurística local + progresso |
| Bulk import | CSV/JSON com QA gate |
| Deprecar legado | `ef_questions` opcional |

---

## 13. Mapa de arquivos existentes

```
prova-publish/
├── index.html              # App monolítico: Player, SessionConfig, GlobalDPOSeeder
├── 404.html                # SPA fallback (sync via sync_dpo_global.py)
├── data/
│   ├── dpo-global-bank.js  # Banco DPO v2 (~301 questões, 19 certs)
│   ├── knowledge-taxonomy.json
│   └── node-schema.example.json
├── docs/
│   ├── PRIVACY-KNOWLEDGE-OS.md   ← este documento
│   ├── KNOWLEDGE-MODEL.md        # Schema v1 + v2
│   ├── DPO-GLOBAL-TRACKS.md      # Inventário atual
│   └── MANIFESTO-ARQUITETURA.md
├── generate_dpo_global_bank.py
├── sync_dpo_global.py
└── .cursor/rules/
    └── velora-privacy-knowledge-os.mdc
```

### Classes-chave em `index.html`

| Classe | Papel |
|--------|-------|
| `Question` | DTO legado + `nodeMeta` (pass-through v2) |
| `GlobalDPOSeeder` | Seed banco DPO global |
| `KnowledgeNormalizer` | Question → KnowledgeNode (fase 1 read-only) |
| `KnowledgeRepository` | Facade de dados |
| `SessionConfig` | Configuração de sessão inteligente |
| `QuestionDisplay` | Render bilingue EN/PT |
| `PlayerController` | Player com pause e revisão pré-envio |
| `FSRS` | Spaced repetition |

---

## 14. Conteúdo e compliance

- **Conteúdo original:** cenários lúdicos do cotidiano — não reproduz itens oficiais IAPP/EXIN
- **Alinhamento:** domínios públicos de syllabi e leis
- **Offline-first:** zero dependência de API para estudar
- **Mobile-first:** smartphone → tablet → desktop

---

## 15. Próximo sprint recomendado

Ver [AGENTS.md](../AGENTS.md) e resumo ao final da sessão de implementação.

1. **Fase 2:** implementar dual-write em `KnowledgeRepository`
2. Enriquecer 5–10 questões piloto em `dpo-global-bank.js` com `learningViews` completas
3. Protótipo de abas Learning Views no player (1 cert, 1 domínio)
4. Conectar filtros `SessionConfig` a `nodeMeta.primaryLaw` e `bloomLevel`

---

## Referências

- [KNOWLEDGE-MODEL.md](KNOWLEDGE-MODEL.md)
- [DPO-GLOBAL-TRACKS.md](DPO-GLOBAL-TRACKS.md)
- [MANIFESTO-ARQUITETURA.md](MANIFESTO-ARQUITETURA.md)
- [AGENTS.md](../AGENTS.md)
