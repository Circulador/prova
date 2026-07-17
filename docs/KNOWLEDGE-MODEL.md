# Velora — Modelo de Conhecimento (Knowledge Node)

> **Status:** especificação de implementação — complementa o [Manifesto de Arquitetura](MANIFESTO-ARQUITETURA.md).  
> **Versão do schema:** `1.0.0`  
> **Princípio:** migrar sem quebrar o app monolítico atual (`Question` / `Exam` / `localStorage`).

---

## 1. Objetivo

Substituir o modelo legado (listas planas de questões e exames) por um **grafo de nós de conhecimento** onde:

- cada conceito existe **uma vez**;
- questões, flashcards, explicações e mídia são **visualizações** do mesmo nó;
- exames e trilhas são **seleções** sobre o grafo, não cópias de conteúdo;
- importadores (JSON, CSV, APKG…) são **adaptadores**, nunca fonte da verdade.

A UI e os fluxos atuais **continuam iguais** durante a migração; apenas a camada de dados evolui por baixo.

---

## 2. Estado atual (legado)

| Store (`localStorage`) | Conteúdo | Problema vs Knowledge OS |
|------------------------|----------|---------------------------|
| `ef_questions` | `Question[]` | Entidade monolítica; explicação colada na questão |
| `ef_exams` | `Exam[]` com `questionIds[]` | Exame referencia IDs, ok — mas sem grafo |
| `ef_qstats` | `{ [questionId]: stats }` | Progresso desconectado do nó |
| `ef_fsrs_cards_v2` | `{ [questionId]: fsrs }` | Cards derivados da questão, não do conceito |
| `ef_history` | sessões com `detail[].questionId` | Histórico por questão, não por nó |

Hierarquia **trilha → cert → submatéria** existe só na UI (`BankHelpers`, seeders), não persistida como grafo.

---

## 3. Modelo alvo — visão geral

```
┌─────────────────────────────────────────────────────────┐
│                    Knowledge Graph                       │
│  TopicNode ──parent──▶ ConceptNode ──prerequisite──▶ …  │
│       │                      │                           │
│       │                      ├── views.question          │
│       │                      ├── views.flashcard[]       │
│       │                      ├── views.explanation       │
│       │                      └── progress + aiMetadata     │
│       └── CollectionNode (certificação / simulado)         │
└─────────────────────────────────────────────────────────┘
         ▲                              │
         │ adaptadores                  │ projeções UI
   JSON CSV APKG …              Question / Exam / Anki (facade)
```

---

## 4. Schema v1.0.0

### 4.1 `KnowledgeNode`

```typescript
/** Unidade atômica de conhecimento ou agrupamento estrutural */
interface KnowledgeNode {
  id: string;                    // ex: "kn_q_abc123" ou mantém "q_abc123" na fase 1
  schemaVersion: "1.0.0";
  kind: NodeKind;
  title: string;                 // rótulo curto para navegação / grafo
  slug?: string;

  metadata: NodeMetadata;
  views: NodeViews;
  progress?: NodeProgress;       // agregado do usuário
  ai?: NodeAIMetadata;           // cache derivado; nunca exposto como menu "IA"
  sync?: SyncMetadata;

  createdAt: string;             // ISO 8601
  updatedAt: string;
}

type NodeKind =
  | "concept"        // conceito aprendível (nó folha com views)
  | "topic"          // agrupador temático (Gramática, ISO 27001)
  | "certification"  // certificação / prova oficial (ISFS, PDPF)
  | "track"          // trilha (EXIN DPO)
  | "collection";    // simulado customizado, deck, pasta
```

### 4.2 `NodeMetadata`

```typescript
interface NodeMetadata {
  language?: string;             // "pt-BR"
  difficulty?: "facil" | "medio" | "dificil";
  tags?: string[];
  source?: SourceRef;            // origem do adaptador
  legacy?: LegacyRefs;          // pontes durante migração
}

interface SourceRef {
  adapter: "json" | "csv" | "html" | "apkg" | "seed" | "manual";
  importedAt?: string;
  externalId?: string;
}

interface LegacyRefs {
  questionId?: string;           // id em ef_questions (fase 1–3)
  examIds?: string[];
}
```

### 4.3 `NodeViews` — visualizações do mesmo nó

```typescript
interface NodeViews {
  /** Uma questão por nó na v1; múltiplas questões = múltiplos nós linkados */
  question?: QuestionView;
  flashcards?: FlashcardView[];
  explanation?: ExplanationView;
  summary?: TextView;
  mindMap?: MindMapView;         // stub futuro
  media?: MediaRef[];            // imagem, áudio, vídeo, PDF
}

interface QuestionView {
  viewId: string;                // "qv_default"
  type: QuestionType;            // single | multi | boolean | short | …
  stem: string;                  // enunciado (ex- Question.text)
  image?: string | null;
  options?: QuestionOption[];
  correctShort?: string[];
  matchPairs?: { left: string; right: string }[];
  sequenceItems?: { text: string }[];
}

interface QuestionOption {
  id: string;
  text: string;
  correct: boolean;
}

interface FlashcardView {
  viewId: string;
  front: string;
  back: string;
  derivedFrom?: "question" | "explanation" | "manual";
}

interface ExplanationView {
  viewId: string;
  body: string;                  // ex- Question.explanation
  locale?: string;
}

interface TextView {
  viewId: string;
  format: "markdown" | "plain";
  body: string;
}

interface MediaRef {
  viewId: string;
  type: "image" | "audio" | "video" | "pdf";
  uri: string;                   // url ou data-uri
  ocr?: string;
}
```

### 4.4 `KnowledgeLink` — arestas do grafo

```typescript
interface KnowledgeLink {
  id: string;
  from: string;                  // node id
  to: string;
  type: LinkType;
  weight?: number;               // relevância para trilhas / IA
}

type LinkType =
  | "parent"           // hierarquia: submatéria → matéria → trilha
  | "prerequisite"     // deve dominar antes
  | "next"             // próximo tópico sugerido
  | "related"          // associação fraca
  | "includes"         // collection inclui nó (exame, deck)
  | "duplicate_of";    // deduplicação (alias → canônico)
```

Links armazenados em store separado `ef_knowledge_links_v1` (array) ou embutidos em nós `kind: collection` via `includes`.

### 4.5 `NodeProgress` — unificar stats + FSRS

```typescript
interface NodeProgress {
  seen: number;
  correct: number;
  streak: number;
  lastAttemptAt?: string | null;

  fsrs?: {
    due: number;
    stability: number;
    difficulty: number;
    reps: number;
    lapses: number;
    state: "new" | "learning" | "review";
    last?: number | null;
  };

  examHistory?: {
    lastCorrect?: boolean;
    lastAt?: string;
  }[];
}
```

### 4.6 `CollectionNode` — exames e trilhas

Substitui `Exam` como **visão de seleção**, não container de texto.

```typescript
/** kind: "collection" | "certification" | "track" */
interface CollectionConfig {
  collectionType: "exam" | "certification" | "track" | "deck";
  questionSelection: QuestionSelectionRef[];  // ordem + filtros
  rules?: {
    timeMinutes?: number;
    passScore?: number;
    shuffle?: boolean;
  };
}

interface QuestionSelectionRef {
  nodeId: string;
  viewId?: string;               // default "qv_default"
  /** legado: questionId === nodeId na fase 1 */
}
```

Mapeamento legado:

```javascript
// Exam legado → CollectionNode
{
  kind: "collection",
  title: exam.title,
  metadata: { legacy: { examIds: [exam.id] } },
  collection: {
    collectionType: "exam",
    questionSelection: exam.questionIds.map(id => ({ nodeId: id })),
    rules: { timeMinutes: exam.timeMinutes, passScore: exam.passScore }
  }
}
```

---

## 5. Camada de persistência

### 5.1 Novas chaves (`localStorage`)

| Chave | Conteúdo |
|-------|----------|
| `ef_knowledge_nodes_v1` | `KnowledgeNode[]` |
| `ef_knowledge_links_v1` | `KnowledgeLink[]` |
| `ef_knowledge_schema_v1` | `{ version: "1.0.0", migratedAt, flags }` |

**Chaves legadas mantidas** até fase 5 (leitura dual / escrita dual).

### 5.2 `KnowledgeRepository` (facade)

Única API interna para o resto do app:

```javascript
class KnowledgeRepository {
  // Compatibilidade — retorna Question para Player, Editor, FSRS
  static getQuestions(filters?) { /* projeta node.views.question */ }
  static upsertQuestion(q) { /* dual-write Question + Node */ }

  static getExams() { /* projeta CollectionNode → Exam */ }
  static upsertExam(exam) { /* dual-write */ }

  // API nova (uso gradual)
  static getNode(id) { }
  static upsertNode(node) { }
  static getLinks(from?, type?) { }
  static getChildren(parentId) { }
  static resolveExamQuestions(examId) { }
}
```

**Regra:** controllers (`PlayerController`, `ExamConfigModal`, `FSRS`) **não** acessam `StorageManager.getQuestions()` diretamente após fase 2 — só via `KnowledgeRepository`.

---

## 6. Adaptadores → modelo interno

Fluxo obrigatório:

```
Arquivo externo → Adapter.parse() → Normalizer → KnowledgeNode[] + KnowledgeLink[]
                                              → (opcional) Legacy projection Question[]
```

| Adaptador atual | Entrada | Saída normalizada |
|-----------------|---------|-------------------|
| `JSONImporter` | `{ questions, exam }` | 1 nó `concept` por questão + 1 `collection` se exam |
| `CSVImporter` | linhas CSV | nós `concept` |
| `ExinDPOSeeder` | JS inline / JSON | nós `track` → `certification` → `topic` → `concept` + links `parent` / `includes` |

**Normalizer** (novo módulo):

```javascript
class KnowledgeNormalizer {
  static fromLegacyQuestion(q) {
    return {
      id: q.id,
      schemaVersion: "1.0.0",
      kind: "concept",
      title: truncate(q.text, 80),
      metadata: {
        difficulty: q.level,
        tags: q.tags,
        legacy: { questionId: q.id }
      },
      views: {
        question: {
          viewId: "qv_default",
          type: q.type,
          stem: q.text,
          image: q.image,
          options: q.options,
          correctShort: q.correctShort,
          matchPairs: q.matchPairs,
          sequenceItems: q.sequenceItems
        },
        explanation: q.explanation
          ? { viewId: "ev_default", body: q.explanation }
          : undefined,
        flashcards: KnowledgeNormalizer.autoFlashcard(q)
      },
      progress: StorageManager.getStat(q.id) // migrar inline
    };
  }

  static autoFlashcard(q) {
    // mesma lógica de FSRS.backText — derivado, não duplicado semanticamente
    return [{ viewId: "fc_auto", front: q.text, back: "...", derivedFrom: "question" }];
  }
}
```

---

## 7. Mapeamento campo a campo (Question → Node)

| Legado `Question` | Knowledge Node |
|-------------------|----------------|
| `id` | `id` (mesmo valor na fase 1) |
| `text` | `views.question.stem` |
| `type` | `views.question.type` |
| `options` | `views.question.options` |
| `explanation` | `views.explanation.body` |
| `level` | `metadata.difficulty` |
| `tags` | `metadata.tags` |
| `materia` | link `parent` → nó `topic` ou metadata |
| `submateria` | link `parent` → nó `topic` |
| `category` | tag ou link |
| `comments` | `views.explanation` extensão ou `ai.notes` |

| Legado `Exam` | Collection Node |
|---------------|-----------------|
| `questionIds` | `collection.questionSelection[].nodeId` |
| `timeMinutes`, `passScore` | `collection.rules` |
| `trilha`, `materia`, `code` | nó `certification` pai + metadata |

---

## 8. Plano de migração incremental

### Fase 0 — Especificação (✅ este documento)

- Schema congelado v1.0.0
- Gate: novas features usam `KnowledgeRepository` quando tocando dados

### Fase 1 — Projeção read-only (sem risco)

**Entrega:** `KnowledgeNormalizer` + testes manuais no console.

- Ao carregar app, gerar nós em memória a partir de `ef_questions`
- Nenhuma escrita nova; validar contagem e round-trip
- Seeder EXIN: gerar grafo trilha → cert → tópico em memória para preview

**Critério de aceite:** 100% das questões → 1 nó `concept`; exames → `collection`.

### Fase 2 — Dual-write transparente

**Entrega:** `KnowledgeRepository` substitui writes.

- `upsertQuestion` / `upsertExam` escrevem **legado +** `ef_knowledge_nodes_v1`
- Reads ainda do legado (fallback se nó ausente)
- Flag migração: `ef_knowledge_schema_v1.migrationPhase = 2`

**Critério:** app idêntico para usuário; diff de stores após import/seed.

### Fase 3 — Dual-read com fallback

**Entrega:** reads preferem nós; legado só fallback.

- `getQuestions()` projeta de nós
- `PlayerController.isCorrect` usa `Question` projetado (API inalterada)
- Histórico continua gravando `questionId` (= `nodeId`)

### Fase 4 — Progresso unificado

**Entrega:** `ef_qstats` + `ef_fsrs_cards_v2` → `node.progress`.

- Migration one-shot no boot: mesclar stats por id
- `FSRS.schedule(q)` → `KnowledgeRepository.updateProgress(nodeId, …)`
- Manter espelho legado 1 versão (rollback)

### Fase 5 — Grafo estrutural EXIN

**Entrega:** trilha DPO como nós + links persistidos.

```
track: EXIN-DPO
  └─ parent ─ certification: ISFS | PDPF | PDPP
       └─ parent ─ topic: "Conceitos de SI" | "ISO/IEC 27001" | …
            └─ includes ─ concept: (50 questões cada)
```

- Biblioteca UI navega grafo (mesma UI, dados reais)
- Eliminar duplicação seeder JS vs JSON (JSON = fonte; seeder só importa)

### Fase 6 — Deprecar legado (opcional, longo prazo)

- Remover `ef_questions` / writes duplicados
- `Exam` vira DTO de projeção apenas
- Exportadores emitem schema Knowledge Node nativo

---

## 9. Compatibilidade e rollback

| Risco | Mitigação |
|-------|-----------|
| Usuário com dados antigos | Migration no boot por fase; flag `migrationPhase` |
| GitHub Pages offline | Tudo em localStorage; sem backend |
| Regressão no player | `Question` projetado mantém `isCorrect()` |
| Rollback | Manter legado até fase 6; flag downgrade phase |

Script de migração (futuro):

```javascript
class KnowledgeMigration {
  static FLAG = 'ef_knowledge_schema_v1';
  static run() {
    const state = StorageManager._get(this.FLAG, { version: '0', migrationPhase: 0 });
    if (state.migrationPhase < 2) this.migratePhase2DualWrite();
    if (state.migrationPhase < 4) this.migratePhase4Progress();
    // …
  }
}
```

---

## 10. Impacto no código (touchpoints)

| Arquivo / classe | Mudança |
|------------------|---------|
| `StorageManager` | Novas keys; delegar a `KnowledgeRepository` |
| `Question` / `Exam` | Mantidos como **DTOs de projeção** |
| `JSONImporter`, `CSVImporter` | Output → `Normalizer` → dual-write |
| `ExinDPOSeeder` | Importar de JSON; criar grafo |
| `PlayerController` | Sem mudança de API ( consome `Question` ) |
| `FSRS` | `schedule` → progress no nó |
| `ExamConfigModal` | `resolveExamQuestions` via repository |
| `BankHelpers` / Biblioteca | Navegar links `parent` / `includes` |

Ordem sugerida de PRs: **1 → 2 → 3 → 4 → 5** (cada um publicável isoladamente).

---

## 11. Formato de exportação nativo (futuro)

```json
{
  "schemaVersion": "1.0.0",
  "nodes": [ { "id": "…", "kind": "concept", "views": { … } } ],
  "links": [ { "from": "track-exin", "to": "cert-isfs", "type": "parent" } ],
  "collections": [ { "id": "exam-…", "questionSelection": [ … ] } ]
}
```

Importadores legados continuam suportados via adaptadores.

---

## 12. Checklist antes de cada PR de migração

1. Respondeu as [15 perguntas do manifesto](MANIFESTO-ARQUITETURA.md)?
2. Usuário percebe diferença? (deve ser **não** até fase 5+)
3. Dual-write/read testado com banco EXIN 150 questões?
4. `sync_exam_modal.py` / `404.html` se tocaram UI?
5. Nó duplicado? → usar `duplicate_of` link, não copy-paste

---

## 13. Próximo passo recomendado

Implementar **Fase 1** em `index.html`:

1. Adicionar `KnowledgeNormalizer` + `KnowledgeRepository` (read-only)
2. Log de validação no boot (`console.debug` contagem nós/links)
3. PR pequeno; zero mudança de UX

Depois **Fase 2** (dual-write) em PR separado.

---

---

## 14. Schema v2.0 — Privacy Certification Node

> **Status:** especificação · complementa v1.0.0 para certificações de privacidade  
> **Spec canônica:** [PRIVACY-KNOWLEDGE-OS.md](PRIVACY-KNOWLEDGE-OS.md)  
> **Exemplo JSON:** [`data/node-schema.example.json`](../data/node-schema.example.json)  
> **Taxonomia:** [`data/knowledge-taxonomy.json`](../data/knowledge-taxonomy.json)

### 14.1 Evolução v1 → v2

| v1.0.0 | v2.0.0 |
|--------|--------|
| `views.explanation` única | `learningViews.*` (7 camadas) |
| `metadata.tags` simples | `QuestionMetadata` completo |
| Idioma opcional | `LocaleBundle[]` multilíngue |
| Certificação via tags | `CertificationRef` + `LawRef` |
| Questão = entidade | Questão = `views.question` do nó |

`schemaVersion` do nó passa a `"2.0.0"` para conteúdo de privacidade; nós legados permanecem `"1.0.0"` até migração.

### 14.2 `LearningViews`

Camadas pedagógicas do mesmo conceito — **não duplicar** em `Question.explanation`.

```typescript
/** Camadas de aprendizagem — Privacy Knowledge OS */
interface LearningViews {
  technical?: LearningViewText;
  simple?: LearningViewText;
  feynman?: LearningViewText;
  analogy?: LearningViewText;
  story?: LearningViewText;
  mnemonic?: LearningViewText;
  visual?: LearningViewVisual;
}

interface LearningViewText {
  viewId: string;
  locale: string;              // "pt-BR", "en", …
  body: string;
}

interface LearningViewVisual {
  viewId: string;
  locale: string;
  suggestions: string[];       // descrições de associação visual / diagrama
}
```

Mapeamento legado (pass-through no seeder):

| Campo legado em `raw` (bank) | Destino v2 |
|------------------------------|------------|
| `explanation` / `explanationPt` | `learningViews.technical` ou `views.explanation` |
| `story` | `learningViews.story` |
| `analogy` | `learningViews.analogy` |
| `feynman` | `learningViews.feynman` |
| `mnemonic` | `learningViews.mnemonic` |
| `visualAssociation` | `learningViews.visual.suggestions` |

### 14.3 `QuestionMetadata`

Metadados completos por nó/visualização — armazenados em `KnowledgeNode.metadata` (v2) ou `Question.nodeMeta` (pass-through legado).

```typescript
interface QuestionMetadata {
  certification?: CertificationRef;
  country?: string;            // ISO 3166-1 alpha-2
  region?: string;             // ex.: "brazil", "europe"
  continent?: string;          // ex.: "americas", "asia"
  knowledgeArea?: string;      // id da taxonomia
  difficulty?: "facil" | "medio" | "dificil";
  estimatedMinutes?: number;
  bloomLevel?: BloomLevel;
  primaryLaw?: LawRef;
  secondaryLaw?: LawRef;
  tags?: string[];
  examObjective?: string;
  officialReference?: string;
  revisionHistory?: RevisionEntry[];
  language?: string;           // locale principal da view
}

type BloomLevel =
  | "remember"    // L1
  | "understand"  // L2
  | "apply"       // L3
  | "analyze"     // L4
  | "evaluate"    // L5
  | "create";     // L6

interface RevisionEntry {
  version: string;
  date: string;                // ISO 8601
  author?: string;
  note?: string;
}
```

### 14.4 `CertificationRef`

```typescript
interface CertificationRef {
  code: string;                // ex.: "IAPP-CIPP-E", "EXIN-LGPD"
  org?: string;                // "IAPP", "EXIN", "ANPD"…
  name?: string;
  examObjective?: string;
  stub?: boolean;              // certificação em desenvolvimento
}
```

### 14.5 `LawRef`

```typescript
interface LawRef {
  id: string;                  // ex.: "lgpd", "gdpr"
  name: string;                // nome completo
  article?: string;            // ex.: "Art. 7º, I"
  jurisdiction?: string;       // "BR", "EU", "US-CA"…
}
```

### 14.6 `LocaleBundle`

Idiomas linkados pelo **mesmo `nodeId`** — conteúdo não duplicado semanticamente.

```typescript
interface LocaleBundle {
  nodeId: string;              // id canônico compartilhado
  language: string;            // "pt-BR" | "en" | "es" | "fr" | "it" | "de" | "ja"
  linked: boolean;
  stub?: boolean;

  /** Integração EN (e outros) */
  glossary?: GlossaryEntry[];
  flashcards?: { front: string; back: string }[];
  examExpressions?: string[];
}

interface GlossaryEntry {
  term: string;
  translation: string;
  pronunciation?: string;
}
```

### 14.7 `KnowledgeNode` v2 (extensão)

```typescript
interface KnowledgeNodeV2 extends KnowledgeNode {
  schemaVersion: "2.0.0";
  metadata: NodeMetadata & QuestionMetadata;
  learningViews?: LearningViews;
  localeBundles?: Record<string, LocaleBundle>;
  /** views.question permanece compatível com Player */
  views: NodeViews;
}
```

### 14.8 Migração Question/Exam → nó v2

| Fase | Ação | Store |
|------|------|-------|
| **2a** | `Question.nodeMeta` pass-through no seeder | `ef_questions` |
| **2b** | `KnowledgeNormalizer` mapeia `nodeMeta` → `metadata` + `learningViews` | `ef_knowledge_nodes_v1` |
| **3** | Player exibe abas `learningViews` | UI |
| **4** | Filtros simulador usam `primaryLaw`, `bloomLevel` | `SessionConfig` |
| **5** | Taxonomia JSON → links `parent` persistidos | `ef_knowledge_links_v1` |
| **6** | Export nativo v2; deprecar campos legados | — |

Pontes legado durante migração:

```javascript
// Question legado (fase 2a)
{
  id: "q_…",
  text: "…",
  nodeMeta: {
    primaryLaw: { id: "lgpd", name: "LGPD", article: "Art. 7º" },
    bloomLevel: "apply",
    learningViews: { story: { body: "João…" } }  // opcional no bank
  }
}

// KnowledgeNormalizer (fase 2b)
static fromLegacyQuestion(q) {
  const node = KnowledgeNormalizer.fromLegacyQuestion_v1(q);
  if (q.nodeMeta) {
    Object.assign(node.metadata, pickMeta(q.nodeMeta));
    node.learningViews = q.nodeMeta.learningViews || buildLearningViews(q.nodeMeta);
    node.schemaVersion = "2.0.0";
  }
  return node;
}
```

### 14.9 Checklist v2

1. Novo conteúdo de privacidade segue [`node-schema.example.json`](../data/node-schema.example.json)?
2. Certificação mapeada em [`knowledge-taxonomy.json`](../data/knowledge-taxonomy.json)?
3. Mesmo conceito em 2 certs → **um nó**, múltiplos `CertificationRef`?
4. Mesmo conceito em 2 idiomas → **um `nodeId`**, `LocaleBundle`?
5. Pass-through no seeder antes de UI?

---

## Referências

- [Privacy Knowledge OS](PRIVACY-KNOWLEDGE-OS.md)
- [Manifesto de Arquitetura](MANIFESTO-ARQUITETURA.md)
- [DPO Global Tracks](DPO-GLOBAL-TRACKS.md)
- [AGENTS.md](../AGENTS.md)
- Código legado: `Question`, `Exam`, `StorageManager` em `index.html`
