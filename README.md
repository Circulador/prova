# ExamForge — Plataforma de Aprendizagem com IA

**Acesse o app:** [https://circulador.github.io/prova/](https://circulador.github.io/prova/)

ExamForge transforma qualquer conteúdo em conhecimento duradouro utilizando inteligência artificial offline, repetição espaçada, gamificação e aprendizado ativo. Tudo em um único arquivo HTML — sem servidor, sem instalação obrigatória.

---

## Missão

O objetivo não é apenas "resolver questões", mas fazer com que o usuário **realmente aprenda e retenha** o conteúdo por muito tempo.

---

## Módulos

| Módulo | Descrição |
|--------|-----------|
| **Simulados** | Criação de provas, banco de questões, correção automática, feedback e estatísticas |
| **Cards (Anki Pro)** | Flashcards com Again / Hard / Good / Easy, repetição espaçada FSRS-like e geração offline |
| **Resolver** | Provas dinâmicas por categoria, tema, matéria ou histórico de erros |
| **Biblioteca** | Organização em decks, categorias, tags, favoritos e histórico |
| **IA offline** | Explica respostas, identifica lacunas, sugere revisões e gera conteúdo localmente |
| **Dashboard** | Desempenho, evolução, XP, streak, metas e curva de retenção |
| **Gamificação** | XP, níveis, missões, conquistas, streak e ranking |
| **Perfil** | Gráficos por categoria, acelerômetro de preparação e centro de performance |

---

## Formatos suportados (importação)

PDF · DOCX · PPTX · EPUB · HTML · Markdown · TXT · CSV · JSON · imagens · áudio · vídeo

> A importação direta no app suporta **JSON, CSV, TXT e HTML**. Outros formatos podem ser convertidos antes ou colados no gerador de cards offline.

---

## Público-alvo

Estudantes de concursos, ENEM, certificações (Microsoft, AWS, Cisco, Palo Alto), medicina, direito, idiomas (TOEFL, IELTS), treinamento corporativo (compliance, LGPD, ISO, phishing) e escolas.

---

## Como usar

1. Abra [circulador.github.io/prova](https://circulador.github.io/prova/) no navegador.
2. Use o **Dashboard** para continuar simulados, revisar erros ou criar exames.
3. Acesse **Cards** para revisão espaçada estilo Anki.
4. Use **Resolver** para montar provas filtradas por categoria ou tema.
5. Importe questões pelo menu **⋯ → Importar questões** (JSON, CSV, TXT, HTML).
6. Instale como PWA pelo menu **⋯ → Instalar aplicativo** (requer HTTPS).

**Atalhos úteis**

- `Ctrl+K` — busca global (command palette)
- `Ctrl+B` — alternar menu lateral expandido/compacto
- `←` / `→` — nos Cards: Again / Good (após revelar a resposta)

---

## Offline first

Toda a aplicação funciona **sem internet**. Os dados ficam no navegador (localStorage / IndexedDB). Ideal para viagens, ambientes sem conexão ou uso em campo. Quando houver internet, basta abrir a URL normalmente.

---

## Estrutura do repositório

```
├── index.html      # Aplicação principal (single-file)
├── 404.html        # Fallback para rotas internas no GitHub Pages
├── .nojekyll       # Desativa Jekyll — necessário no GitHub Pages
├── README.md
└── download/       # Cópia de segurança do HTML final
```

---

## Publicação (GitHub Pages)

Este repositório já está configurado:

- **Source:** Deploy from a branch
- **Branch:** `main`
- **Folder:** `/ (root)`

Para republicar após alterações, envie os arquivos acima para a raiz do repositório. O deploy é automático em alguns minutos.

---

## Tecnologias

HTML5 · CSS3 · JavaScript (ES2023) · PWA · Service Worker · localStorage · IndexedDB

Sem dependências externas. Um único `index.html` contém toda a aplicação.

---

## Visão

ExamForge evolui para uma **plataforma unificada de aprendizagem**, combinando:

- Repetição espaçada do **Anki**
- Organização de conhecimento do **RemNote**
- Facilidade de criação do **Quizlet**
- Gamificação do **Duolingo**
- Treinamento corporativo inspirado em **Hoxhunt**
- Suporte de IA para geração de conteúdo e explicações

Tudo com filosofia **offline-first** e publicação simples via GitHub Pages.

---

## Licença

Uso livre para estudo pessoal, treinamentos e projetos educacionais.
