import { chromium } from '../../../node_modules/@playwright/test/index.mjs';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';

const root = path.dirname(fileURLToPath(import.meta.url));
const data = JSON.parse(await fs.readFile(path.join(root, 'palettes.json'), 'utf8'));
const browser = await chromium.launch({
  headless: true,
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
});
const page = await browser.newPage({ viewport: { width: 1600, height: 1200 }, deviceScaleFactor: 1 });
const errors = [];
page.on('pageerror', e => errors.push(e.message));
await page.goto('file://' + root + '/index.html');
await page.evaluate(() => document.fonts.ready);

// Each option is presented at the same scale and in the same layout.
const comparisonBottom = await page.locator('#comparison').evaluate(e => e.getBoundingClientRect().bottom);
await page.screenshot({
  path: root + '/comparison.png',
  clip: { x: 0, y: 0, width: 1600, height: Math.ceil(comparisonBottom + 36) },
});

const interactions = [];
for (const palette of data.palettes) {
  await page.locator(`.palette-button[data-palette="${palette.id}"]`).click();
  for (const theme of ['dark', 'light']) {
    await page.locator(`.theme-button[data-theme="${theme}"]`).click();
    for (const [stateId, state] of Object.entries(data.states)) {
      await page.locator('#state-select').selectOption(stateId);
      const result = await page.evaluate(() => {
        const e = document.getElementById('preview');
        const s = getComputedStyle(e);
        const value = k => s.getPropertyValue('--' + k).trim();
        return {
          ...e.dataset,
          bg: value('bg'), text: value('text'), stateColor: value('state'),
          a: value('particle-a'), b: value('particle-b'),
          label: document.getElementById('active-state').textContent,
          chosenPalette: document.querySelector('.palette-button[aria-pressed="true"]').dataset.palette,
          chosenTheme: document.querySelector('.theme-button[aria-pressed="true"]').dataset.theme,
          css: document.getElementById('css-download').getAttribute('href'),
          displayedPairs: [...document.querySelectorAll('#contrast-body tr')].map(r => {
            const cells = [...r.cells].map(c => c.textContent);
            return { role: cells[0], hex: cells[1], minimum: Math.min(parseFloat(cells[2]), parseFloat(cells[3])) };
          }),
        };
      });
      assert.equal(result.palette, palette.id);
      assert.equal(result.theme, theme);
      assert.equal(result.state, stateId);
      assert.equal(result.bg, palette[theme].bg);
      assert.equal(result.text, palette[theme].text);
      assert.equal(result.stateColor, palette[theme][state.role]);
      assert.equal(result.a, palette[theme][state.a]);
      assert.equal(result.b, palette[theme][state.b]);
      assert.equal(result.label, state.symbol + ' ' + state.label);
      assert.equal(result.chosenPalette, palette.id);
      assert.equal(result.chosenTheme, theme);
      assert.equal(result.css, 'assets/' + palette.id + '-tokens.css');
      assert.equal(result.displayedPairs.length, 6);
      for (const pair of result.displayedPairs) assert.ok(pair.minimum >= (pair.role === 'Control boundary' ? 3 : 4.5));
      interactions.push({ palette: palette.id, theme, state: stateId });
    }
    await page.locator('#state-select').selectOption('exploration');
    await page.locator('#preview').screenshot({ path: root + '/assets/preview-' + palette.id + '-' + theme + '.png' });
  }
}

const sizes = [];
await page.locator('.palette-button[data-palette="obsidian"]').click();
await page.locator('.theme-button[data-theme="dark"]').click();
for (const width of [1600, 1440, 1024, 768, 390]) {
  await page.setViewportSize({ width, height: 1200 });
  const result = await page.evaluate(() => ({
    width: innerWidth,
    documentWidth: document.documentElement.scrollWidth,
    brokenImages: [...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.src),
    loadedFonts: [...document.fonts].map(f => ({ family: f.family, status: f.status })),
    headings: [...document.querySelectorAll('h1,h2,h3')].map(h => ({ level: Number(h.tagName.slice(1)), text: h.textContent })),
    ordinaryTextMinimumLeading: Math.min(...[...document.querySelectorAll('body *')]
      .filter(e => !e.closest('svg') && !/^H[1-6]$/.test(e.tagName) && !e.classList.contains('sr-only'))
      .filter(e => e.getBoundingClientRect().width > 0 && e.getBoundingClientRect().height > 0)
      .filter(e => [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()))
      .map(e => { const s = getComputedStyle(e); return parseFloat(s.lineHeight) / parseFloat(s.fontSize); })),
  }));
  assert.ok(result.documentWidth <= width, 'Page overflow: ' + JSON.stringify(result));
  assert.equal(result.brokenImages.length, 0);
  assert.ok(result.loadedFonts.every(f => f.status === 'loaded'));
  assert.ok(result.ordinaryTextMinimumLeading >= 1.3);
  for (let i = 1; i < result.headings.length; i++) assert.ok(result.headings[i].level <= result.headings[i - 1].level + 1);
  sizes.push(result);
  if (width === 390) {
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.screenshot({ path: root + '/assets/mobile-opening.png', clip: { x: 0, y: 0, width: 390, height: 1200 } });
    await page.locator('#preview').screenshot({ path: root + '/assets/mobile-preview.png' });
  }
}
assert.deepEqual(errors, []);

// Original master paths are present unchanged in every neutral logo specimen.
const original = await fs.readFile(path.join(root, '../assets/logos/symbol-dark.svg'), 'utf8');
const originalPaths = [...original.matchAll(/<path d="([^"]+)"/g)].map(m => m[1]);
const logoCopies = await page.locator('svg[aria-label="Divergent Apertures, retained original logo"]').evaluateAll(es => es.map(e => [...e.querySelectorAll('path')].map(p => p.getAttribute('d'))));
assert.equal(logoCopies.length, 8);
for (const paths of logoCopies) assert.deepEqual(paths, originalPaths);

await fs.writeFile(root + '/VERIFICATION.json', JSON.stringify({
  browser: 'Installed Google Chrome / temporary headless session',
  originalLogoCopies: logoCopies.length,
  originalLogoPathsPreserved: true,
  interactionCombinations: interactions.length,
  prescribedContrastPairs: 72,
  responsiveChecks: sizes,
  scriptErrors: errors,
}, null, 2) + '\n');
await browser.close();
console.log('Rendered color comparison and 6 palette specimens. Verified 30 control combinations, 5 viewport widths, and 8 unchanged logo copies.');
