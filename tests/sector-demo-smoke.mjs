import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const {Window}=await import(process.env.HAPPY_DOM_MODULE||'happy-dom');
const html=fs.readFileSync(new URL('../index.html',import.meta.url),'utf8');
const code=fs.readFileSync(new URL('../sector-demo.js',import.meta.url),'utf8');
function setup(reduced=true){
 const w=new Window();w.document.body.innerHTML=html;w.matchMedia=()=>({matches:reduced,addEventListener(){}});
 let scheduled=null;w.setTimeout=fn=>{scheduled=fn;return 1};w.clearTimeout=()=>{scheduled=null};
 vm.runInNewContext(code,{window:w,document:w.document,IntersectionObserver:class{constructor(fn){this.fn=fn}observe(){this.fn([{isIntersecting:true}])}}});
 return {w,d:w.document,tick:()=>{const fn=scheduled;scheduled=null;fn?.()},pending:()=>!!scheduled};
}
test('Every sector shows its booking, confirmation and automatic intake, then manual follow-up',async()=>{
 const {w,d,pending}=setup();const root=d.getElementById('sector-walkthrough');const buttons=[...d.querySelectorAll('button[data-sector]')];assert.equal(buttons.length,10);assert.equal(pending(),false);
 for(const button of buttons){button.click();assert.equal(root.dataset.step,'0');assert.equal(button.getAttribute('aria-pressed'),'true');assert.equal(d.querySelectorAll('button[data-sector][aria-pressed=true]').length,1);const service=d.querySelector('.walk-service strong').textContent;
 for(let n=0;n<6;n++)d.getElementById('walkthrough-next').click();assert.match(d.querySelector('.walk-thanks').textContent,/Bedankt voor je boeking/);assert.ok(d.querySelector('.walk-thanks').textContent.includes(service));
 d.getElementById('walkthrough-next').click();assert.match(d.getElementById('walkthrough-caption').textContent,/Automatisch/);assert.equal(d.querySelector('.walk-board>div:first-child .walk-lead strong').textContent,'Emma Janssens');
 d.getElementById('walkthrough-next').click();assert.ok(d.querySelector('.walk-board>div:nth-child(2) .walk-lead'));assert.match(d.querySelector('.walk-hint').textContent,/doe jij/);assert.equal(d.getElementById('walkthrough-next').disabled,true);
 }assert.equal(root.querySelector('form'),null);await w.happyDOM.close();
});
test('Playback can pause and restart, and automatically stops after the final scene',async()=>{
 const {w,d,tick,pending}=setup(false);const root=d.getElementById('sector-walkthrough');assert.equal(pending(),true);tick();assert.equal(root.dataset.step,'1');d.getElementById('walkthrough-play').click();assert.equal(pending(),false);d.getElementById('walkthrough-replay').click();assert.equal(root.dataset.step,'0');for(let i=0;i<8;i++)tick();assert.equal(root.dataset.step,'8');assert.equal(pending(),false);d.querySelector('[data-sector=beauty]').click();assert.equal(root.dataset.step,'0');assert.match(d.getElementById('walkthrough-screen').textContent,/Laserontharing/);await w.happyDOM.close();
});
