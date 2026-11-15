'use strict';
// The packaged homepage points to the separate app. The private review copy
// lives under /website/ alongside the app and keeps its navigation local.
const appBase=location.hostname.endsWith('.chatgpt.site')&&location.pathname.startsWith('/website/')?new URL('../',location.href):new URL('https://app.afspraakboeken.be/');
const targets={app:new URL('./',appBase),register:new URL('https://afspraakboeken.be/#contact'),booking:new URL('demo/?mode=book&tenant=lune',appBase)};
for(const [key,value] of Object.entries({primary:'#264653',secondary:'#2a9d8f',background:'#f8fafb'}))targets.booking.searchParams.set('theme_'+key,value);
for(const link of document.querySelectorAll('[data-app-link]'))link.href=targets[link.dataset.appLink].href;
const menu=document.querySelector('.menu-toggle'),navigation=document.getElementById('navigation');
function closeMenu(){menu.setAttribute('aria-expanded','false');navigation.classList.remove('open')}
menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));navigation.classList.toggle('open',open)});
navigation.addEventListener('click',event=>{if(event.target.closest('a'))closeMenu()});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&menu.getAttribute('aria-expanded')==='true'){closeMenu();menu.focus()}});
const examples={
 dak:{symbol:'↗',title:'Een eerste kijk op je dak.',description:'Laat een bezoek inplannen om het dak te bekijken en de werken te bespreken.',service:'Dakinspectie ter plaatse',duration:'45 min',question:'Op welk adres mogen we langskomen?',tip:'Eerst de situatie bekijken. Daarna een gerichte offerte.'},
 airco:{symbol:'❋',title:'Een frisse start voor elk project.',description:'Plan een adviesgesprek om de ruimtes, wensen en mogelijkheden te bekijken.',service:'Advies over airconditioning',duration:'45 min',question:'Voor hoeveel ruimtes zoek je een oplossing?',tip:'De juiste informatie vóór je op bezoek gaat.'},
 solar:{symbol:'☀',title:'Een helder plan voor hun dak.',description:'Laat geïnteresseerde klanten een eerste adviesgesprek vastleggen.',service:'Advies over zonnepanelen',duration:'30 min',question:'Wat is het adres van de woning?',tip:'Een duidelijk startpunt voor een voorstel op maat.'},
 beauty:{symbol:'✦',title:'Een moment helemaal voor hen.',description:'Geef elke behandeling een heldere uitleg en de tijd die ze nodig heeft.',service:'Intake voor laserontharing',duration:'30 min',question:'Is dit je eerste bezoek aan onze zaak?',tip:'Een persoonlijke start, nog voor de klant binnenstapt.'},
 hair:{symbol:'✂',title:'Een frisse look begint hier.',description:'Laat klanten zelf de juiste behandeling en een passend moment kiezen.',service:'Knippen & brushing',duration:'60 min',question:'Wil je vooraf nog iets meegeven?',tip:'Genoeg tijd voor elke klant en elke behandeling.'},
 catering:{symbol:'◒',title:'Van feestidee naar eerste gesprek.',description:'Plan een kennismaking om de gelegenheid, gasten en wensen te bespreken.',service:'Kennismaking voor jouw evenement',duration:'45 min',question:'Voor hoeveel gasten organiseer je het evenement?',tip:'Het gesprek boeken, daarna het menu en de offerte afstemmen.'}
};
for(const button of document.querySelectorAll('[data-sector]'))button.addEventListener('click',()=>{const example=examples[button.dataset.sector];for(const item of document.querySelectorAll('[data-sector]'))item.setAttribute('aria-pressed',String(item===button));for(const [id,value] of Object.entries({symbol:example.symbol,name:example.title,description:example.description,service:example.service,duration:example.duration,question:example.question,tip:example.tip}))document.getElementById('sector-'+id).textContent=value});
for(const button of document.querySelectorAll('[data-palette]'))button.addEventListener('click',()=>{document.querySelector('[data-brand-demo]').dataset.palette=button.dataset.palette;for(const item of document.querySelectorAll('button[data-palette]'))item.setAttribute('aria-pressed',String(item===button))});
const demo=document.getElementById('demo-dialog'),frame=document.getElementById('demo-frame');let previousFocus;
for(const button of document.querySelectorAll('[data-open-demo]'))button.addEventListener('click',()=>{previousFocus=document.activeElement;if(!frame.getAttribute('src'))frame.src=targets.booking.href;demo.showModal();document.getElementById('close-demo').focus()});
document.getElementById('close-demo').addEventListener('click',()=>demo.close());
demo.addEventListener('close',()=>previousFocus?.focus());
for(const link of document.querySelectorAll('[data-open-faq]'))link.addEventListener('click',()=>{document.getElementById(link.dataset.openFaq).open=true});
