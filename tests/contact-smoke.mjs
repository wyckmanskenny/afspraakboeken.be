import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const {Window}=await import(process.env.HAPPY_DOM_MODULE||'happy-dom');
const home=fs.readFileSync(new URL('../index.html',import.meta.url),'utf8');
const prices=fs.readFileSync(new URL('../prijzen/index.html',import.meta.url),'utf8');
const code=fs.readFileSync(new URL('../site.js',import.meta.url),'utf8');
for(const [title,html,url] of [['home',home,'https://afspraakboeken.be/'],['pricing',prices,'https://afspraakboeken.be/prijzen/']])test(`${title}: demo, information, trial and login remain distinct`,async()=>{
 const w=new Window({url});w.document.body.innerHTML=html.match(/<body[^>]*>([\s\S]*)<\/body>/)[1].replace(/<script[\s\S]*?<\/script>/g,'');
 vm.runInNewContext(code,{document:w.document,location:w.location,URL,console});
 assert.equal(w.document.querySelector('[data-app-link=trial]').href,'https://app.afspraakboeken.be/registreren/?mode=trial');
 assert.equal(w.document.querySelector('[data-app-link=register]').href,'https://app.afspraakboeken.be/registreren/');
 assert.ok(w.document.querySelector('.preview-bar a').href.includes('/demo/'));
 assert.equal(w.document.querySelector('[data-app-link=app]').textContent,'Inloggen');
 assert.equal(w.document.querySelector('#contact-form'),null);assert.ok(!w.document.body.textContent.includes('door Wycked'));
 await w.happyDOM.close();
});
test('Pricing states the annual total, tax basis and absence of automatic charges',()=>{
 assert.match(prices,/€180 per gebruiker per jaar/);assert.match(prices,/exclusief btw/);assert.match(prices,/Geen automatische betaling/);assert.match(prices,/14 dagen/);
});
