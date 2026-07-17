# Velora Branding

Identidade visual oficial do projeto **Velora**.

## Estrutura

```
branding/
├── logo/              SVG — símbolo e wordmarks (color, white, black, mono)
├── icons/             App icon 1024 + Android adaptive layers
├── favicon/           favicon.svg, mask-icon, PNGs
├── pwa/               manifest.json, splash screens, browserconfig
├── theme/             theme.css — design tokens
├── design-system/     design-system.md, components.html, components.css
├── assets/png/        PNGs gerados (não editar manualmente)
└── scripts/           generate-assets.mjs
```

## Gerar PNGs e favicons

```bash
cd branding/scripts
npm install
node generate-assets.mjs
```

Gera todos os tamanhos de ícone (16–1024), favicons, apple-touch-icon e splash screens.

## Visualizar componentes

Abra `design-system/components.html` no navegador.

## Paleta principal

| Cor | Hex |
|-----|-----|
| Purple | `#9333EA` |
| Blue | `#2563EB` |
| Teal | `#06B6D4` |
| Gold | `#FBBF24` |
| Base | `#0B0E14` |

## Tagline

**ESTUDE. EVOLUA. CONQUISTE.**

## Licença

Uso exclusivo do projeto Velora.
