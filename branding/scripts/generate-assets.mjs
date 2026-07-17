#!/usr/bin/env node
/**
 * Velora asset generator — SVG → PNG + favicon.ico
 * Usage: node branding/scripts/generate-assets.mjs
 */
import { readFile, mkdir, writeFile } from 'fs/promises';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dir = dirname(fileURLToPath(import.meta.url));
const root = join(__dir, '..');
const pngDir = join(root, 'assets', 'png');
const faviconDir = join(root, 'favicon');

const ICON_SIZES = [1024, 512, 256, 192, 180, 167, 152, 144, 96, 72, 64, 48, 32, 16];

async function main() {
  let sharp;
  try {
    sharp = (await import('sharp')).default;
  } catch {
    console.error('Install sharp: npm install --prefix branding/scripts sharp');
    process.exit(1);
  }

  await mkdir(pngDir, { recursive: true });
  await mkdir(faviconDir, { recursive: true });

  const appIconSvg = await readFile(join(root, 'icons', 'app-icon.svg'));
  const faviconSvg = await readFile(join(faviconDir, 'favicon.svg'));

  for (const size of ICON_SIZES) {
    const out = join(pngDir, `icon-${size}.png`);
    await sharp(appIconSvg).resize(size, size).png().toFile(out);
    console.log('✓', out);
  }

  await sharp(faviconSvg).resize(32, 32).png().toFile(join(faviconDir, 'favicon-32.png'));
  await sharp(faviconSvg).resize(16, 16).png().toFile(join(faviconDir, 'favicon-16.png'));
  await sharp(faviconSvg).resize(180, 180).png().toFile(join(faviconDir, 'apple-touch-icon.png'));
  console.log('✓ favicons PNG');

  // Multi-size ICO (16 + 32)
  const buf16 = await sharp(faviconSvg).resize(16, 16).png().toBuffer();
  const buf32 = await sharp(faviconSvg).resize(32, 32).png().toBuffer();
  // sharp doesn't write ICO natively — embed 32px as primary favicon.ico substitute
  await writeFile(join(faviconDir, 'favicon.ico'), buf32);
  console.log('✓ favicon.ico (32px PNG embedded)');

  const splashes = [
    ['pwa/splash-mobile.svg', 1080, 1920, 'splash-mobile.png'],
    ['pwa/splash-desktop.svg', 1920, 1080, 'splash-desktop.png'],
  ];
  for (const [rel, w, h, name] of splashes) {
    const svg = await readFile(join(root, rel));
    await sharp(svg).resize(w, h).png().toFile(join(pngDir, name));
    console.log('✓ splash', name);
  }

  console.log('\nDone. All PNG assets generated.');
}

main().catch(e => { console.error(e); process.exit(1); });
