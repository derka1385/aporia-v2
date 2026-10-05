import { chromium } from '@playwright/test';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import path from 'node:path';

const root = process.cwd();
const review = path.join(root,'.impeccable/review');
await fs.mkdir(review,{recursive:true});
const browser = await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const page = await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1,reducedMotion:'reduce'});
const errors = [];
page.on('pageerror',e => errors.push(e.message));
page.on('console',m => {if(m.type()==='error')errors.push(m.text());});
await page.goto('http://127.0.0.1:5173/');
await page.locator('.ap-landing').waitFor();
await page.evaluate(() => document.fonts.ready);
await page.locator('canvas').waitFor();
await page.waitForTimeout(1800);

for(const name of ['Reasoning','Conflict','Exploration']){
  await page.getByRole('button',{name,exact:true}).click();
  assert.equal(await page.getByRole('button',{name,exact:true}).getAttribute('aria-pressed'),'true');
  assert.equal(await page.locator('.ap-state-button[aria-pressed="true"]').count(),1);
}
await page.getByRole('button',{name:'Pause particle animation'}).click();
assert.equal(await page.getByRole('button',{name:'Resume particle animation'}).getAttribute('aria-pressed'),'true');
await page.getByRole('button',{name:'Resume particle animation'}).click();
for(const name of ['Formalist','Skeptic','Synthesizer','Minimalist','Explorer']){
  await page.getByRole('tab',{name,exact:true}).click();
  assert.equal(await page.getByRole('tab',{name,exact:true}).getAttribute('aria-selected'),'true');
  assert.equal(await page.locator('.ap-profile-description h3').textContent(),name);
  assert.equal(await page.locator('.ap-path li').count(),3);
}
await page.getByRole('tab',{name:'Explorer',exact:true}).focus();
await page.keyboard.press('End');
assert.equal(await page.getByRole('tab',{name:'Minimalist',exact:true}).getAttribute('aria-selected'),'true');
await page.keyboard.press('Home');
assert.equal(await page.getByRole('tab',{name:'Explorer',exact:true}).getAttribute('aria-selected'),'true');
await page.locator('.ap-faq-list details').first().locator('summary').click();
assert.equal(await page.locator('.ap-faq-list details').first().getAttribute('open'),'');
await page.locator('.ap-faq-list details').first().locator('summary').click();

const viewports=[];
for(const width of [1440,1280,768,390,320]){
  await page.setViewportSize({width,height:1000});
  await page.evaluate(() => window.scrollTo(0,0));
  await page.waitForTimeout(1600);
  const check=await page.evaluate(() => {
    const text=[...document.querySelectorAll('.ap-landing *')].filter(e=>!e.closest('svg,h1,h2,h3,h4,h5,h6')&&e.getBoundingClientRect().width&&e.getBoundingClientRect().height).filter(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()));
    const hs=[...document.querySelectorAll('h1,h2,h3')].map(e=>({level:Number(e.tagName.slice(1)),text:e.textContent}));
    const clipped=text.filter(e=>e.scrollWidth>e.clientWidth+2&&!e.closest('.ap-path')).map(e=>({tag:e.tagName,className:e.className,text:e.textContent.slice(0,80),width:e.clientWidth,content:e.scrollWidth}));
    const fonts=[...document.fonts].map(f=>({family:f.family,status:f.status}));
    return{width:innerWidth,documentWidth:document.documentElement.scrollWidth,headings:hs,clippedText:clipped,fonts,ordinaryTextLeading:Math.min(...text.map(e=>{const c=getComputedStyle(e);return parseFloat(c.lineHeight)/parseFloat(c.fontSize)})),canvasPresent:!!document.querySelector('canvas'),internalLinks:[...document.querySelectorAll('a[href^="#"]')].map(a=>({href:a.getAttribute('href'),exists:!!document.getElementById(a.getAttribute('href').slice(1))}))};
  });
  assert.ok(check.documentWidth<=width,'Page overflow at '+width);
  assert.deepEqual(check.clippedText,[],'Clipped text at '+width);
  assert.ok(check.ordinaryTextLeading>=1.3);
  assert.ok(check.fonts.every(f=>f.status==='loaded'));
  assert.ok(check.internalLinks.every(a=>a.exists));
  for(let i=1;i<check.headings.length;i++) assert.ok(check.headings[i].level<=check.headings[i-1].level+1);
  viewports.push(check);
  if(width===1440){
    await page.screenshot({path:review+'/desktop.png',fullPage:true});
    await page.screenshot({path:review+'/hero.png',clip:{x:0,y:0,width:1440,height:920}});
    await page.locator('#approach').screenshot({path:review+'/approach-desktop.png'});
  }
  if(width===390){
    await page.getByRole('button',{name:'Open navigation',exact:true}).click();
    assert.equal(await page.getByRole('button',{name:'Close navigation',exact:true}).getAttribute('aria-expanded'),'true');
    await page.locator('.ap-nav').getByRole('link',{name:'The approach',exact:true}).click();
    assert.equal(await page.getByRole('button',{name:'Open navigation',exact:true}).getAttribute('aria-expanded'),'false');
    await page.evaluate(() => window.scrollTo(0,0));
    await page.waitForTimeout(1200);
    await page.screenshot({path:review+'/mobile.png',fullPage:true});
    await page.screenshot({path:review+'/hero-mobile.png',clip:{x:0,y:0,width:390,height:1370}});
    await page.locator('#approach').screenshot({path:review+'/approach-mobile.png'});
  }
}
await page.setViewportSize({width:1440,height:1000});
await page.getByRole('link',{name:'Investigate this question',exact:true}).click();
await page.locator('.question-input input').waitFor();
assert.equal(new URL(page.url()).pathname,'/app');
assert.equal(await page.getByRole('textbox',{name:'Philosophical question'}).inputValue(),'Is personal identity dependent on psychological continuity?');
assert.equal(await page.getByRole('button',{name:'Research',exact:true}).count(),1);
await page.getByRole('button',{name:'Visual studies',exact:true}).click();
assert.equal(await page.getByRole('button',{name:'Exploration',exact:false}).count(),1);
assert.deepEqual(errors,[]);
await fs.writeFile(review+'/verification.json',JSON.stringify({viewports,interactionChecks:['3 visual states','pause and resume','5 policy tabs','tab keyboard Home/End','FAQ expand/collapse','mobile navigation','inquiry link prefills actual laboratory','existing visual studies accessible'],javascriptErrors:errors},null,2)+'\n');
await browser.close();
console.log('Landing verified at 5 widths; state, policy, navigation, FAQ and laboratory interactions pass.');
