#!/usr/bin/env python3
"""Generate Velora PNG assets from SVG masters (svglib + reportlab)."""
from pathlib import Path
import sys

try:
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM
except ImportError:
    print("Install: python -m pip install svglib reportlab")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
PNG_DIR = ROOT / "assets" / "png"
FAV_DIR = ROOT / "favicon"
SIZES = [1024, 512, 256, 192, 180, 167, 152, 144, 96, 72, 64, 48, 32, 16]

def render(svg_path: Path, out_path: Path, w: int, h: int | None = None):
    h = h or w
    out_path.parent.mkdir(parents=True, exist_ok=True)
    drawing = svg2rlg(str(svg_path))
    if drawing is None:
        raise RuntimeError(f"Failed to parse {svg_path}")
    sx = w / drawing.width
    sy = h / drawing.height
    drawing.width = w
    drawing.height = h
    drawing.scale(sx, sy)
    renderPM.drawToFile(drawing, str(out_path), fmt="PNG")
    print(f"OK {out_path.relative_to(ROOT)}")

def main():
    app_icon = ROOT / "icons" / "app-icon.svg"
    favicon = FAV_DIR / "favicon.svg"
    splash_m = ROOT / "pwa" / "splash-mobile.svg"
    splash_d = ROOT / "pwa" / "splash-desktop.svg"

    for size in SIZES:
        render(app_icon, PNG_DIR / f"icon-{size}.png", size)

    render(favicon, FAV_DIR / "favicon-32.png", 32)
    render(favicon, FAV_DIR / "favicon-16.png", 16)
    render(favicon, FAV_DIR / "apple-touch-icon.png", 180)

    import shutil
    shutil.copy(FAV_DIR / "favicon-32.png", FAV_DIR / "favicon.ico")

    render(splash_m, PNG_DIR / "splash-mobile.png", 1080, 1920)
    render(splash_d, PNG_DIR / "splash-desktop.png", 1920, 1080)
    print("Done.")

if __name__ == "__main__":
    main()
