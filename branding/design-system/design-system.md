# Velora Design System

Identidade visual oficial extraída do conceito **Velora — Estude. Evolua. Conquiste.**
Unifica princípios de **Material Design 3**, **Apple Human Interface Guidelines** e **Fluent UI**.

---

## 1. Logo

### Símbolo
- Letra **V** em fita com dobra 3D (duas faces sobrepostas).
- **Estrela dourada** no vértice superior direito — inteligência, insight, conquista.
- Gradiente principal: **Roxo → Azul → Teal** (135°).

### Variantes (`/branding/logo/`)
| Arquivo | Uso |
|---------|-----|
| `velora-symbol.svg` | Símbolo colorido |
| `symbol-white.svg` | Fundos escuros / overlay |
| `symbol-black.svg` | Fundos claros |
| `symbol-mono.svg` | `currentColor` — tinta única |
| `logo-horizontal-color.svg` | Header, marketing |
| `logo-horizontal-white.svg` | Hero escuro |
| `logo-horizontal-black.svg` | Impressão / fundo claro |
| `logo-vertical-color.svg` | Splash, App Store |

### Área de respiro
- Mínimo **1×** a altura do símbolo em todos os lados.
- Não distorcer, rotacionar ou alterar gradientes.

### Tagline
`ESTUDE.` (roxo) · `EVOLUA.` (azul) · `CONQUISTE.` (teal)  
Letter-spacing: `0.14em`, peso 600, caixa alta.

---

## 2. Paleta

| Token | Hex | Uso |
|-------|-----|-----|
| Purple 500 | `#9333EA` | Brand primary |
| Blue 500 | `#2563EB` | Brand secondary |
| Teal 500 | `#06B6D4` | Brand tertiary / sucesso |
| Gold 400 | `#FBBF24` | Accent / estrela / XP |
| Base | `#0B0E14` | Background dark |
| Surface | `#12182A` | Cards dark |
| Text primary | `#F8FAFC` | Títulos |
| Text secondary | `#94A3B8` | Corpo |

Gradiente marca: `linear-gradient(135deg, #9333EA, #2563EB, #06B6D4)`

**WCAG AA:** texto primário sobre `#0B0E14` ≈ 15:1 ✓

---

## 3. Tipografia

- **Primária:** Inter (fallback: system-ui)
- **Monospace:** SF Mono / Cascadia Code

| Nível | Size | Weight |
|-------|------|--------|
| Display | 2.25rem | 700 |
| H1 | 1.75rem | 650 |
| H2 | 1.375rem | 600 |
| Body | 0.9375rem | 400 |
| Caption | 0.75rem | 500 |

---

## 4. Espaçamentos

Base **4px**: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64.

Touch target mínimo: **44×44px** (Apple HIG + Material).

---

## 5. Grid

- Mobile: 4 colunas, gutter 16px
- Tablet: 8 colunas
- Desktop: 12 colunas, max-width 1280px

---

## 6. Radius & Sombras

| Token | Valor |
|-------|-------|
| `--radius-sm` | 10px |
| `--radius-md` | 14px |
| `--radius-lg` | 18px |
| `--radius-xl` | 24px |
| Squircle app icon | 22% |

Sombras suaves com blur alto; glow sutil em elementos de foco (`--shadow-glow`).

---

## 7. Componentes

Ver `design-system/components.html` + `theme/theme.css`.

### Botões
- **Primary:** gradiente brand, texto branco
- **Secondary:** borda + fundo surface
- **Ghost:** transparente
- **Danger:** vermelho semântico

### Cards
- Fundo `--bg-surface`, borda 1px, radius `--radius-lg`
- Hover: `--shadow-glow` leve

### Inputs
- Altura 44px, radius `--radius-sm`
- Focus: outline roxo 2px

### Modais
- Overlay `--bg-overlay`, card central `--radius-xl`
- Animação `velora-fade-in`

### Toast / Alert / Badge / Tag
- Cores semânticas com fundo soft (12–18% opacidade)

---

## 8. Ícones

- Estilo **line art** (stroke 1.75–2px)
- Círculo com gradiente brand opcional
- Tamanhos: 16, 20, 24, 32px

---

## 9. Dark / Light Mode

- **Default:** dark (`--bg-base: #0B0E14`)
- **Light:** `[data-theme="light"]` — superfícies brancas, texto `#0F172A`
- Preferência: `prefers-color-scheme` + toggle manual

---

## 10. Animações

| Nome | Uso |
|------|-----|
| `velora-fade-in` | Entrada de views |
| `velora-shimmer` | Loading / XP bar |
| `velora-pulse-glow` | CTA hero |
| `velora-draw` | Logo SVG (futuro) |

Respeitar `prefers-reduced-motion`.

---

## 11. Gamificação

- **XP bar:** gradiente brand + shimmer
- **Level badge:** círculo gold ou gradiente
- **Conquistas:** card compacto, ícone line + label
- **Ranking:** tabela zebra subtle

---

## 12. App Icon & PWA

- Master: `icons/app-icon.svg` (1024×1024)
- Android adaptive: foreground + background SVG
- PNGs gerados: `npm install && node branding/scripts/generate-assets.mjs`
- Manifest: `pwa/manifest.json`

---

## 13. Estrutura de arquivos

```
branding/
├── logo/           # SVG wordmarks & symbols
├── icons/          # App icon, adaptive
├── favicon/        # favicon.svg, mask-icon, PNGs
├── pwa/            # manifest, splash SVG
├── theme/          # theme.css tokens
├── design-system/  # docs + component showcase
├── assets/png/     # raster exports
└── scripts/        # generate-assets.mjs
```

---

## 14. Regras

1. Logo **sempre vetorial** (SVG).
2. Não usar raster para identidade principal.
3. Manter contraste WCAG AA mínimo.
4. Um gradiente brand por tela (CTA ou hero — não everywhere).
5. Consistência cross-platform: Android, iOS, Web, Desktop.
