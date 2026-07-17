# ExamForge

Aplicação HTML offline-first pronta para GitHub Pages.

## Como publicar corretamente

1. Extraia este ZIP no computador.
2. No repositório GitHub, apague arquivos antigos que possam conflitar, principalmente `index.html` antigo e arquivo chamado `download` se ele tiver sido enviado como arquivo.
3. Envie para a raiz do repositório estes itens extraídos:
   - `index.html`
   - `404.html`
   - `.nojekyll`
   - `README.md`
   - pasta `download`
4. Em GitHub, abra `Settings > Pages`.
5. Configure:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/root`
6. Acesse a URL do GitHub Pages do repositório.

## Observações

- O arquivo principal que carrega o aplicativo é `index.html`.
- O arquivo `404.html` é uma cópia do aplicativo para evitar tela vazia em rotas internas.
- O arquivo `.nojekyll` evita processamento Jekyll e ajuda o GitHub Pages a servir os arquivos estáticos diretamente.
- A pasta `download` contém uma cópia de segurança do HTML final.
