import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
const {Window}=await import(process.env.HAPPY_DOM_MODULE||'happy-dom');
const root=new URL('../',import.meta.url);
const urls=[...fs.readFileSync(new URL('sitemap.xml',root),'utf8').matchAll(/<loc>(.*?)<\/loc>/g)].map(m=>m[1]);
const header=fs.readFileSync(new URL('partials/header.html',root),'utf8').trim(),footer=fs.readFileSync(new URL('partials/footer.html',root),'utf8').trim();
test('All 29 public pages have unique SEO metadata, shared navigation and working local links',async()=>{
 assert.equal(urls.length,29);const titles=new Set(),descriptions=new Set();
 for(const url of urls){const pathname=new URL(url).pathname;const html=fs.readFileSync(new URL('.'+pathname+'index.html',root),'utf8');assert.ok(html.includes(header),url);assert.ok(html.includes(footer),url);const w=new Window({url});w.document.write(html);const d=w.document;
 assert.equal(d.querySelectorAll('h1').length,1,url);assert.equal(d.querySelector('link[rel=canonical]').href,url);assert.ok(!d.querySelector('meta[name=robots]').content.includes('noindex'));assert.ok(!titles.has(d.title));titles.add(d.title);const desc=d.querySelector('meta[name=description]').content;assert.ok(desc.length>60);assert.ok(!descriptions.has(desc));descriptions.add(desc);
 for(const a of d.querySelectorAll('a[href]')){const link=new URL(a.getAttribute('href'),url);if(link.origin!==new URL(url).origin)continue;let file='.'+link.pathname;if(file.endsWith('/'))file+='index.html';assert.ok(fs.existsSync(new URL(file,root)),`${url}: ${link}`);if(link.hash){const linked=fs.readFileSync(new URL(file,root),'utf8');assert.ok(linked.includes('id="'+decodeURIComponent(link.hash.slice(1))+'"'),`${url}: missing ${link.hash}`);}}
 await w.happyDOM.close();
 }
});
test('Sector pages start with their own service and reach the matching confirmation',async()=>{
 for(const [slug,service] of [['sector/dakwerkers','Opmeting dak'],['sector/beauty-wellness','Laserontharing'],['sector/installateurs','Advies & opmeting airco'],['sector/tuinaannemers','Tuinbezoek & opmeting']]){
 const w=new Window();w.document.body.innerHTML=fs.readFileSync(new URL(slug+'/index.html',root),'utf8');w.matchMedia=()=>({matches:true,addEventListener(){}});vm.runInNewContext(fs.readFileSync(new URL('sector-demo.js',root),'utf8'),{window:w,document:w.document,IntersectionObserver:class{observe(){}}});assert.equal(w.document.querySelector('.walk-service strong').textContent,service);for(let i=0;i<6;i++)w.document.getElementById('walkthrough-next').click();assert.ok(w.document.querySelector('.walk-thanks').textContent.includes(service));await w.happyDOM.close();
 }
});
test('Legacy sector URLs immediately redirect to canonical sector pages and stay out of the sitemap',async()=>{
 for(const suffix of ['', '/dakwerkers','/beauty-wellness','/installateurs','/tuinaannemers']){
 const w=new Window();w.document.write(fs.readFileSync(new URL('voor'+suffix+'/index.html',root),'utf8'));const target='https://afspraakboeken.be/sector'+suffix+'/';assert.equal(w.document.querySelector('meta[http-equiv=refresh]').content,'0; url='+target);assert.equal(w.document.querySelector('link[rel=canonical]').href,target);assert.ok(urls.includes(target));assert.ok(!urls.some(u=>u.includes('/voor/')));await w.happyDOM.close();
 }
});

test('Every registration category has a guide with practical examples, benefits and internal links',async()=>{
 const categories=JSON.parse(fs.readFileSync(new URL('scripts/sector-categories.json',root),'utf8'));
 assert.equal(categories.length,13);
 const w=new Window({url:'https://afspraakboeken.be/sector/'});w.document.write(fs.readFileSync(new URL('sector/index.html',root),'utf8'));
 for(const category of categories){
  const pathname='/sector/'+category.slug+'/';assert.ok(urls.includes('https://afspraakboeken.be'+pathname));
  assert.ok([...w.document.querySelectorAll('.sector-catalogue a')].some(a=>a.getAttribute('href')===pathname&&a.querySelector('h3')?.textContent===category.label));
  const page=new Window();page.document.write(fs.readFileSync(new URL('.'+pathname+'index.html',root),'utf8'));
  assert.equal(page.document.querySelectorAll('.sector-usecases tbody tr').length,3);
  assert.equal(page.document.querySelectorAll('.sector-advantages li').length,3);
  assert.ok(page.document.querySelector('a[href="/prijzen/"]'));
  assert.ok(page.document.querySelector('a[href="/crm-voor-zelfstandigen/"]'));
  await page.happyDOM.close();
 }
 await w.happyDOM.close();
});
