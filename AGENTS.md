# Velora — Guia para Agentes

Velora é um **Knowledge Operating System**, não um app de simulados.

## Documentos obrigatórios (ler antes de implementar)

1. **[Privacy Knowledge OS](docs/PRIVACY-KNOWLEDGE-OS.md)** — spec canônica certificações de privacidade, taxonomia, roadmap Fases 1–6
2. **[Manifesto de Arquitetura](docs/MANIFESTO-ARQUITETURA.md)** — requisitos arquiteturais, UX, IA e dados
3. **[Modelo de Conhecimento](docs/KNOWLEDGE-MODEL.md)** — schema Knowledge Node v1 + v2 (Privacy Certification Node)
4. **[Trilhas DPO Global](docs/DPO-GLOBAL-TRACKS.md)** — inventário do banco `dpo-global-bank.js`
5. **[Modelo de Repaginação UI](docs/UI-REDESIGN-MODEL.md)** — shell offline-first, breakpoints, componentes
6. **[Arquitetura PWA](docs/PWA-ARCHITECTURE.md)** — Service Worker, cache, installability, roadmap
7. **[Prompt IA PWA](docs/PWA-AI-PROMPT.md)** — prompt para implementação com artigo de referência
8. **[Design System](branding/design-system/design-system.md)** — tokens visuais, componentes, breakpoints
9. **Regras Cursor** — `.cursor/rules/velora-*.mdc` (aplicadas automaticamente)

## Stack atual

- App monolítico: `index.html` + `404.html` (GitHub Pages SPA fallback)
- Sync modal: `sync_exam_modal.py` (manter `404.html` alinhado após mudanças no modal)
- Branding: `branding/` (SVG, theme, PWA)
- Bancos de questões: scripts Python + JSON seeders

## Princípios inegociáveis

- **Mobile First:** smartphone → tablet → desktop (`≥ 1024px` sidebar)
- **Regra dos 3 cliques** para ações importantes
- **One Page First:** modal/drawer/painel antes de nova rota
- **Knowledge Node único:** formatos externos são adaptadores, não fonte da verdade
- **IA invisível:** ações contextuais ✨, nunca menu "IA"
- **Regra Suprema:** nova feature não pode aumentar complexidade percebida

## Gate antes de codar

Responder as 15 perguntas do manifesto. Se aumentar complexidade sem ganho proporcional → **reprojetar**.

## Publicação

- Repo: https://github.com/Circulador/prova
- Live: https://circulador.github.io/prova/
- Commit/push apenas quando o usuário solicitar explicitamente.
