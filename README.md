# Velora — Knowledge Operating System

**Acesse o app:** [https://circulador.github.io/prova/](https://circulador.github.io/prova/)

Velora é um **Sistema Operacional de Conhecimento**: questões, flashcards, simulados, importações e IA são visualizações do mesmo conhecimento conectado — não módulos isolados.

**Arquitetura (obrigatória):** [`docs/MANIFESTO-ARQUITETURA.md`](docs/MANIFESTO-ARQUITETURA.md)  
**Design visual:** [`branding/design-system/design-system.md`](branding/design-system/design-system.md)  
**Agentes Cursor:** [`AGENTS.md`](AGENTS.md)

Tudo roda em HTML estático (GitHub Pages) — sem servidor obrigatório, com PWA opcional.

---

## Missão

Criar a melhor plataforma de estudos do mundo. O usuário nunca deve sentir complexidade; toda a profundidade fica na arquitetura interna.

---

## Pilares do produto

| Pilar | Descrição |
|-------|-----------|
| **Knowledge Graph** | Conteúdo conectado em nós únicos — sem duplicação |
| **Estudo** | Simulados, treino, revisão inteligente, trilhas (ex.: EXIN DPO) |
| **Cards** | Flashcards com repetição espaçada (Again / Hard / Good / Easy) |
| **Biblioteca** | Certificações, questões, importação via adaptadores |
| **Progresso** | Estatísticas, histórico, evolução |
| **IA invisível** | ✨ Explicar, simplificar, gerar cards — contextual, sem menu "IA" |

---

## Formatos suportados (importação)

PDF · DOCX · PPTX · EPUB · HTML · Markdown · TXT · CSV · JSON · imagens · áudio · vídeo

> Importação direta no app: **JSON, CSV, TXT e HTML**. Outros formatos passam por adaptadores ou conversão prévia.

---

## Como usar

1. Abra [circulador.github.io/prova](https://circulador.github.io/prova/) no navegador (mobile first).
2. **Início** — workspace: continuar, progresso, próxima ação.
3. **Biblioteca** — certificações, questões, importar.
4. **Progresso** — estatísticas e histórico.
5. Instale como PWA pelo menu **⋯ → Instalar aplicativo** (HTTPS).

---

## Desenvolvimento

Princípios inegociáveis antes de qualquer PR:

- Mobile First (smartphone → tablet → desktop ≥ 1024px)
- Regra dos 3 cliques
- One Page First (modal/drawer antes de nova página)
- Gate de 15 perguntas — ver manifesto

Após editar o modal de simulado em `index.html`, rode:

```bash
python sync_exam_modal.py
```

---

## Estrutura do repositório

```
docs/MANIFESTO-ARQUITETURA.md   # Requisitos arquiteturais
AGENTS.md                        # Guia para agentes Cursor
.cursor/rules/velora-*.mdc       # Regras automáticas
index.html / 404.html            # App monolítico
branding/                        # Identidade Velora
*.py + *bank_data.json           # Seeders e bancos
```

---

## Licença e créditos

Ver histórico de commits e contribuições no repositório [Circulador/prova](https://github.com/Circulador/prova).
