# PNG assets

PNG files are **generated** from SVG masters. They are not hand-edited.

## Generate (requires Node + sharp OR Python + cairo)

### Node (recommended)
```bash
cd branding/scripts
npm install
node generate-assets.mjs
```

### Python
```bash
python -m pip install cairosvg
# Requires libcairo installed on the system (GTK/Cairo for Windows)
python branding/scripts/generate-assets.py
```

## Output

| File | Size |
|------|------|
| `icon-1024.png` … `icon-16.png` | App icons |
| `splash-mobile.png` | 1080×1920 |
| `splash-desktop.png` | 1920×1080 |
| `../favicon/favicon-16.png` | 16×16 |
| `../favicon/favicon-32.png` | 32×32 |
| `../favicon/apple-touch-icon.png` | 180×180 |
| `../favicon/favicon.ico` | multi-size |

Until generated, use SVG files directly in web (`favicon.svg`, `app-icon.svg`).
