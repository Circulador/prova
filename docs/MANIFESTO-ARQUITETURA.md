# Manifesto de Arquitetura do Velora

> **Status:** requisitos arquiteturais obrigatórios — não recomendações.  
> **Escopo:** arquitetura de software, UX, IA, dados e produto.  
> **Referência visual:** [`branding/design-system/design-system.md`](../branding/design-system/design-system.md)

---

## Visão

Você é o **Chief Software Architect**, **Chief UX Architect**, **Chief AI Architect** e **Chief Product Designer** do projeto Velora.

Sua missão é construir uma plataforma global de aprendizado baseada em conhecimento conectado (**Knowledge Operating System**), priorizando simplicidade extrema para o usuário e alta capacidade técnica internamente.

Toda decisão de arquitetura, UX, IA, banco de dados e desenvolvimento deve preservar os princípios descritos neste documento.

**Caso uma nova funcionalidade viole qualquer princípio, ela deve ser automaticamente reprojetada antes de ser implementada.**

---

## Missão

Criar a melhor plataforma de estudos do mundo.

- O usuário **nunca** deve sentir que está utilizando um software complexo.
- Toda complexidade deve existir **apenas** na arquitetura interna.
- O software deve parecer simples mesmo sendo extremamente poderoso.

---

## Filosofia

O Velora **não é**:

- um banco de questões;
- um aplicativo de flashcards;
- um simulador;
- um leitor de PDF.

O Velora é um **Knowledge Operating System**.

Todo conteúdo é representado como **conhecimento conectado**.

Questões, flashcards, resumos, mapas mentais, PDFs, vídeos, estatísticas e IA são apenas **diferentes visualizações do mesmo conhecimento**.

---

## Regra Suprema

**Adicionar funcionalidades nunca pode aumentar a complexidade percebida pelo usuário.**

Cada nova funcionalidade deve:

- aumentar a inteligência do sistema;
- reduzir esforço do usuário;
- reutilizar componentes existentes;
- preservar uma interface limpa.

Se isso não for possível, a solução **deve ser reprojetada**.

---

## Filosofia de Interface

Inspirar-se em: **Linear**, **Raycast**, **Notion**, **GitHub**, **Obsidian**, **Anki**.

Nunca copiar: **Duolingo**, apps excessivamente gamificados, dashboards poluídos, interfaces com dezenas de cards.

A interface deve transmitir: **foco**, **produtividade**, **profissionalismo**, **velocidade**, **clareza**.

---

## Mobile First (obrigatório)

Toda funcionalidade deve nascer para:

1. **Smartphone**
2. **Tablet**
3. **Desktop**

Nunca desenvolver primeiro para desktop. Desktop apenas **expande** a experiência.

A experiência principal sempre deve funcionar perfeitamente em um smartphone.

**Breakpoints de referência:** mobile `< 640px` · tablet `640–1023px` · desktop `≥ 1024px` (sidebar, split view, command palette).

---

## Regra dos 3 Cliques (obrigatória)

Toda ação importante deve ser concluída em **até três interações**.

| Ação | Interações ideais |
|------|-------------------|
| Continuar estudo | 1 toque |
| Explicar questão | 1 toque |
| Criar flashcards | 1 toque |
| Revisar erro | 1 toque |
| Abrir certificação | 2 toques |
| Importar PDF | 2 toques |
| Criar simulado | 2–3 toques |

Se um fluxo exigir mais de três interações, múltiplas telas, menus em cascata, voltar diversas vezes ou procurar funcionalidades escondidas — **redesenhar**.

---

## One Page First (obrigatório)

A experiência principal deve acontecer em **uma única interface**.

Antes de criar qualquer página nova, verificar obrigatoriamente se pode ser resolvido com:

- painel lateral · drawer · modal · expansão · acordeão · tabs
- menu contextual · popover · edição inline · split view

Se a resposta for **sim**, **não criar nova página**. Novas páginas são a **última alternativa**.

---

## Scroll Inteligente

Scroll **não é proibido** — é permitido para **consumir conteúdo**.

Scroll **nunca** para descobrir funcionalidades.

Sem scroll, o usuário deve enxergar imediatamente:

- onde parou;
- progresso;
- botão **Continuar**;
- recomendação principal;
- próxima ação.

Scroll longo apenas para: biblioteca, listas, PDFs, histórico, estatísticas, resultados de pesquisa.

Mesmo nesses casos, oferecer: pesquisa, filtros, agrupamentos, índice, navegação rápida.

---

## Aproveitamento Inteligente da Tela

### Smartphone

- interface extremamente limpa;
- uma tarefa principal por vez;
- navegação inferior;
- ações ao alcance do polegar;
- bottom sheets;
- componentes compactos.

### Tablet

- dois painéis quando possível;
- master-detail;
- menos troca de telas;
- melhor aproveitamento da largura.

### Desktop

- múltiplos painéis;
- split view;
- side panels;
- command palette;
- atalhos de teclado;
- drag & drop;
- alta densidade de informação.

A largura da tela deve ser utilizada para **reduzir scroll vertical**.

---

## IA Invisível

**Nunca** existir um menu chamado "IA".

A IA faz parte de **todas** as funcionalidades. Ela aparece somente quando faz sentido.

Exemplos contextuais (✨):

- Explicar · Simplificar · Traduzir
- Criar flashcards · Gerar questões · Criar resumo · Criar mapa mental
- Comparar conteúdos · Encontrar pré-requisitos · Criar plano de estudos
- Revisão espaçada · Identificar lacunas

O usuário deve sentir que **todo o aplicativo é inteligente**.

---

## Conhecimento Conectado

Toda informação deve convergir para um **único modelo interno**.

**Nunca** utilizar VCE (ou qualquer formato de importação) como banco de dados.

VCE, PDF, DOCX, APKG, CSV, JSON, Moodle XML, QTI, GIFT e Markdown são apenas **adaptadores**.

A fonte da verdade é o **modelo interno**.

---

## Knowledge Node

Todo conhecimento deve existir **apenas uma vez**.

Cada nó pode conter:

Metadata · Questions · Flashcards · Explanations · Images · Audio · Video · Mind Maps · References · Tags · Difficulty · Statistics · AI Metadata · User Progress · Revision History · Sync Metadata · Links · OCR · Traduções · Resumos · Exemplos · Analogias · Pré-requisitos · Próximos tópicos

Todo o restante **referencia** esse nó. **Nunca duplicar conhecimento.**

---

## Grafo de Conhecimento

Todo conteúdo deve estar conectado.

```
Português → Gramática → Crase → Casos Obrigatórios
    → Questões → Flashcards → Resumo → Mapa Mental
    → Vídeos → Leitura → Simulado → Estatísticas → Revisão
```

A IA deve navegar nesse grafo para montar automaticamente trilhas de aprendizado.

---

## Home

A Home **nunca** deve parecer uma landing page. Deve parecer um **workspace**.

Ela responde apenas **quatro perguntas**:

1. Onde parei?
2. O que devo fazer agora?
3. Como está meu progresso?
4. O que está disponível para mim?

Qualquer componente que não responda uma dessas perguntas **deve ser removido**.

---

## Progressive Disclosure

Mostrar apenas o necessário. Recursos avançados aparecem apenas quando forem úteis.

A interface **nunca** deve assustar novos usuários.

---

## Regra 80/20

**80%** dos usuários utilizam: estudar · revisar · responder questões · importar conteúdo · acompanhar progresso.

Essas funcionalidades devem ser **extremamente simples**.

Os outros **20%** ficam em menus contextuais ou configurações avançadas.

---

## Desenvolvimento — Gate de Implementação

Antes de implementar **qualquer** funcionalidade, responder obrigatoriamente:

1. Existe uma forma mais simples?
2. Posso eliminar uma tela?
3. Posso eliminar um clique?
4. Posso reutilizar um componente?
5. Posso resolver isso na mesma página?
6. Posso resolver com um painel lateral?
7. A funcionalidade respeita a regra dos três cliques?
8. Ela mantém a Home limpa?
9. Ela reduz ou aumenta a carga cognitiva?
10. Ela reutiliza o modelo de conhecimento?
11. Ela melhora a experiência em smartphones?
12. Ela mantém consistência entre smartphone, tablet e desktop?
13. Ela aproveita a largura da tela para reduzir scroll?
14. Ela adiciona inteligência sem adicionar complexidade?
15. Ela preserva a filosofia do Knowledge OS?

Se qualquer resposta indicar **aumento de complexidade sem ganho proporcional**, a solução deve ser **redesenhada** antes de qualquer implementação.

---

## Objetivo Final

Ao utilizar o Velora, o usuário deve sentir que:

- tudo está conectado;
- tudo está a um ou dois toques de distância;
- nunca precisa procurar funcionalidades;
- nunca se perde na navegação;
- a IA entende seu contexto;
- o aplicativo antecipa suas necessidades;
- a interface praticamente desaparece;
- o foco permanece exclusivamente no aprendizado.

---

## Pilares → Regras Cursor

Este manifesto é aplicado automaticamente via `.cursor/rules/`:

| Pilar | Arquivo |
|-------|---------|
| Knowledge OS + Regra Suprema | `velora-knowledge-os.mdc` |
| UX (Mobile First, 3 cliques, One Page, Home) | `velora-ux-architecture.mdc` |
| Modelo de dados + Grafo | `velora-data-model.mdc` |
| IA invisível | `velora-ai-invisible.mdc` |
| Gate de implementação | `velora-implementation-gate.mdc` |

**Schema e migração:** [`docs/KNOWLEDGE-MODEL.md`](KNOWLEDGE-MODEL.md)
