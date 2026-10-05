import { chromium } from '../../../../node_modules/@playwright/test/index.mjs';
import path from 'node:path';
import fs from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const url=process.env.APORIA_PREVIEW_URL || 'http://127.0.0.1:8767/';
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const page=await browser.newPage();
const errors=[];page.on('pageerror',e=>errors.push(e.message));
const checks=[];
for(const width of [1440,390]){
  await page.setViewportSize({width,height:1000});
  await page.goto(url);
  await page.evaluate(()=>document.fonts.ready);
  await page.waitForFunction(()=>document.querySelector('video').readyState>=1);
  const state=await page.evaluate(()=>{
    const v=document.querySelector('video');
    return {viewport:innerWidth,documentWidth:document.documentElement.scrollWidth,duration:v.duration,width:v.videoWidth,height:v.videoHeight,controls:v.controls,autoplay:v.autoplay,brokenImages:[...document.images].filter(x=>!x.complete||!x.naturalWidth).map(x=>x.src),captions:v.querySelector('track')?.getAttribute('src')};
  });
  if(state.documentWidth>width||state.duration!==60||state.width!==1920||state.height!==1080||state.brokenImages.length)throw Error(JSON.stringify(state));
  checks.push(state);
  await page.screenshot({path:path.join(root,'exports',`player-${width}.png`),fullPage:true});
}
await page.setViewportSize({width:1440,height:1000});
const seeks=[];
for(const t of [4,11,17,25,29.7,31.7,33,41,51,58]){
  await page.evaluate(async t=>{const v=document.querySelector('video');const p=new Promise(r=>v.addEventListener('seeked',r,{once:true}));v.currentTime=t;await p;},t);
  const s=await page.evaluate(()=>{const v=document.querySelector('video');return {time:v.currentTime,readyState:v.readyState,error:v.error?.message||null};});
  if(s.error||s.readyState<2||Math.abs(s.time-t)>.05)throw Error(JSON.stringify({requested:t,...s}));
  seeks.push(s);
}
await page.evaluate(async()=>{
  const v=document.querySelector('video');v.textTracks[0].mode='showing';
  await new Promise(r=>setTimeout(r,200));v.currentTime=22;
});
await page.waitForFunction(()=>document.querySelector('video').textTracks[0].cues?.length>0);
const subtitles=await page.evaluate(()=>{const v=document.querySelector('video');return {cues:v.textTracks[0].cues.length,language:v.textTracks[0].language};});
await page.evaluate(async()=>{const v=document.querySelector('video');v.muted=true;v.currentTime=0;await v.play();});
await page.waitForFunction(()=>document.querySelector('video').currentTime>.6);
await page.evaluate(()=>document.querySelector('video').pause());
if(errors.length)throw Error(errors.join('\n'));
await fs.writeFile(path.join(root,'exports','player-verification.json'),JSON.stringify({checks,seeks,subtitles,playback:true,scriptErrors:errors},null,2)+'\n');
await browser.close();
console.log('Player verified at 1440px and 390px: 60 seconds, 1080p, seeking, playback and English captions.');
