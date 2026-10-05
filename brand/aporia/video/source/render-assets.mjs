import { chromium } from '../../../../node_modules/@playwright/test/index.mjs';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const browser = await chromium.launch({headless:true, executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const page = await browser.newPage({viewport:{width:1000,height:1000}, deviceScaleFactor:1});
for (const [name,width,height] of [['symbol-light',640,640],['symbol-dark',640,640],['wordmark-light',1260,460],['wordmark-dark',1260,460]]) {
  const svg = await fs.readFile(path.resolve(root,'../assets/logos',name+'.svg'),'utf8');
  await page.setViewportSize({width,height});
  await page.setContent(`<html><head><style>html,body{margin:0;background:transparent}svg{display:block;width:${width}px;height:${height}px}</style></head><body>${svg}</body></html>`);
  await page.screenshot({path:path.join(root,'assets',name+'.png'), omitBackground:true});
}
await browser.close();
console.log('Rasterized the retained, unmodified SVG symbol and outlined wordmark.');
