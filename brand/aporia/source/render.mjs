import { chromium } from '../../../node_modules/@playwright/test/index.mjs';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const browser = await chromium.launch({ headless: true, executablePath: process.env.APORIA_BROWSER_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
const page = await browser.newPage({ viewport: { width: 1600, height: 1100 }, deviceScaleFactor: 1 });
const errors = [];
page.on('pageerror', error => errors.push(error.message));

await page.goto('file://' + root + '/overview.html');
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: root + '/assets/visuals/brand-overview.png', fullPage: true });

await page.goto('file://' + root + '/applications.html');
await page.evaluate(() => document.fonts.ready);
const applicationReview = await page.evaluate(() => {
  const textElements = [...document.querySelectorAll('body *')].filter(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()));
  const bodyRatios = textElements.filter(e=>!/^H[1-6]$/.test(e.tagName)).map(e=>{const s=getComputedStyle(e);return parseFloat(s.lineHeight)/parseFloat(s.fontSize)});
  const dashboardHeadings = [...document.querySelectorAll('#dashboard h1,#dashboard h2,#dashboard h3')].map(h=>({level:h.tagName,text:h.textContent}));
  return {minimumOrdinaryTextLeading:Math.min(...bodyRatios),dashboardHeadings};
});
if(applicationReview.minimumOrdinaryTextLeading<1.3) throw new Error('Application body text leading is too tight');
if(applicationReview.dashboardHeadings.some(h=>h.level==='H3')) throw new Error('Dashboard heading level skipped');
for (const [selector, name] of [['#website','website-study'],['#dashboard','dashboard-study'],['#deck','presentation-study']]) {
  await page.locator(selector).screenshot({ path: root + '/assets/visuals/' + name + '.png' });
}

// Browser rasterization preserves all vector geometry and outlined letterforms.
const iconPage = await browser.newPage();
for (const size of [16, 32, 48]) {
  await iconPage.setViewportSize({ width: size, height: size });
  await iconPage.goto('file://' + root + `/assets/logos/favicon-${size}.svg`);
  await iconPage.screenshot({ path: root + `/assets/logos/favicon-${size}.png`, omitBackground: true });
}
for (const size of [192,512,1024]) {
  await iconPage.setViewportSize({ width: size, height: size });
  await iconPage.goto('file://' + root + '/assets/logos/app-icon.svg');
  await iconPage.evaluate((n) => {const s=document.querySelector('svg');s.setAttribute('width',n);s.setAttribute('height',n)},size);
  await iconPage.screenshot({ path: root + `/assets/logos/app-icon-${size}.png`, omitBackground: true });
}
await iconPage.setViewportSize({ width: 1600, height: 850 });
await iconPage.goto('file://' + root + '/assets/visuals/logo-contact-sheet.svg');
await iconPage.screenshot({ path: root + '/assets/visuals/logo-contact-sheet.png' });

// Inspect the delivered HTML at three sizes. Check layout and review controls,
// rather than running unrelated application tests for a proposal-only change.
const checks = [];
for (const width of [1440,768,390]) {
  await page.setViewportSize({width,height:1000});
  await page.goto('file://' + root + '/index.html');
  await page.evaluate(() => document.fonts.ready);
  const state = await page.evaluate(() => ({
    width: innerWidth,
    documentWidth: document.documentElement.scrollWidth,
    chapters: document.querySelectorAll('.chapter').length,
    concepts: document.querySelectorAll('.concept').length,
    brokenImages: [...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src),
    headings: [...document.querySelectorAll('.chapter h2')].map(h=>h.textContent),
  }));
  if (state.documentWidth > width) throw new Error(`Page overflow at ${width}: ${state.documentWidth}`);
  if (state.chapters !== 18 || state.concepts !== 10 || state.brokenImages.length) throw new Error(JSON.stringify(state));
  checks.push(state);
  if(width===1440) {
    await page.screenshot({path:root+'/assets/visuals/book-opening.png'});
    await page.locator('#s06').screenshot({path:root+'/assets/visuals/logo-chapter.png'});
  }
  if(width===390) await page.screenshot({path:root+'/assets/visuals/book-mobile.png'});
}
await page.locator('#theme-toggle').click();
await page.locator('#preview-size').selectOption('24');
const interaction = await page.evaluate(() => ({theme:document.getElementById('concepts').dataset.mode,size:getComputedStyle(document.querySelector('.concept .symbol svg')).width}));
if(interaction.theme!=='dark'||interaction.size!=='24px') throw new Error(JSON.stringify(interaction));
if(errors.length) throw new Error(errors.join('\n'));

// ICO with individually rendered 16, 32 and 48 px PNG entries.
const pngs = await Promise.all([16,32,48].map(n=>fs.readFile(root+`/assets/logos/favicon-${n}.png`)));
const header = Buffer.alloc(6+pngs.length*16);
header.writeUInt16LE(1,2); header.writeUInt16LE(pngs.length,4);
let offset = header.length;
for(let i=0;i<pngs.length;i++) {
  const size=[16,32,48][i],base=6+i*16;
  header[base]=size;header[base+1]=size;
  header.writeUInt16LE(1,base+4);header.writeUInt16LE(32,base+6);
  header.writeUInt32LE(pngs[i].length,base+8);header.writeUInt32LE(offset,base+12);
  offset+=pngs[i].length;
}
await fs.writeFile(root+'/assets/logos/favicon.ico',Buffer.concat([header,...pngs]));
await fs.writeFile(root+'/VERIFICATION.json',JSON.stringify({date:'2026-10-04',checks,interaction,applicationReview,scriptErrors:errors},null,2)+'\n');
await browser.close();
console.log('Rendered all studies, raster icons and ICO; verified 18 chapters, 10 concepts, image loading, responsive layout and review controls.');
