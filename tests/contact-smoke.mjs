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
 assert.ok(w.document.querySelector('a[href="/contact/"]'));
 assert.ok(w.document.querySelector('.preview-bar a').href.includes('/demo/'));
 assert.equal(w.document.querySelector('[data-app-link=app]').textContent,'Inloggen');
 assert.equal(w.document.querySelector('#contact-form'),null);assert.ok(!w.document.body.textContent.includes('door Wycked'));
 await w.happyDOM.close();
});
test('Pricing states the annual total, tax basis and absence of automatic charges',()=>{
 assert.match(prices,/€180 per gebruiker per jaar/);assert.match(prices,/exclusief btw/);assert.match(prices,/Geen automatische betaling/);assert.match(prices,/14 dagen/);
});

const solutions=fs.readFileSync(new URL('../alles-in-1/index.html',import.meta.url),'utf8'),contact=fs.readFileSync(new URL('../contact/index.html',import.meta.url),'utf8');
test('All marketing pages share the same header and link to existing feature sections',()=>{
 const headers=[home,prices,solutions,contact].map(s=>s.match(/<header class="header">[\s\S]*?<\/header>/)[0]);assert.ok(headers.every(x=>x===headers[0]));for(const id of ['contactformulier','afspraken','aanvragen','crm'])assert.ok(solutions.includes('id="'+id+'"'));assert.match(solutions,/extra, betalende module/);
});
test('Solutions menu supports opening, Escape and outside click',async()=>{
 const w=new Window({url:'https://afspraakboeken.be/'});w.document.body.innerHTML=home;vm.runInNewContext(code,{document:w.document,location:w.location,URL,console});const details=w.document.querySelector('.solutions-menu');details.open=true;w.document.dispatchEvent(new w.KeyboardEvent('keydown',{key:'Escape',bubbles:true}));assert.equal(details.open,false);details.open=true;w.document.body.click();assert.equal(details.open,false);await w.happyDOM.close();
});
test('Information form preserves data after failure and only confirms a successful submission',async()=>{
 const w=new Window({url:'https://afspraakboeken.be/contact/?interesse=crm'});w.document.body.innerHTML=contact;let sent=[],succeed=false;
 const fetch=async(url,options)=>{sent.push({url,data:JSON.parse(options.body)});return {ok:succeed,json:async()=>succeed?{message:'Bedankt'}:{error:'Probeer opnieuw'}};};
 vm.runInNewContext(fs.readFileSync(new URL('../contact/contact.js',import.meta.url),'utf8'),{document:w.document,location:w.location,URLSearchParams,FormData:w.FormData,fetch,console});const form=w.document.getElementById('contact-form');form.elements.name.value='Test';form.elements.company.value='Testbedrijf';form.elements.email.value='test@example.test';assert.match(form.elements.message.value,/CRM/);
 form.dispatchEvent(new w.Event('submit',{bubbles:true,cancelable:true}));await new Promise(r=>setTimeout(r,10));assert.equal(form.hidden,false);assert.equal(form.elements.name.value,'Test');assert.equal(w.document.getElementById('contact-success').hidden,true);assert.match(w.document.getElementById('contact-status').textContent,/opnieuw/);
 succeed=true;form.dispatchEvent(new w.Event('submit',{bubbles:true,cancelable:true}));await new Promise(r=>setTimeout(r,10));assert.equal(form.hidden,true);assert.equal(w.document.getElementById('contact-success').hidden,false);assert.equal(sent[1].url,'https://app.afspraakboeken.be/api/index.php?route=contact');assert.equal(sent[1].data.company,'Testbedrijf');await w.happyDOM.close();
});
