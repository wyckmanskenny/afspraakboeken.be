(()=>{
'use strict';
const root=document.getElementById('sector-walkthrough');if(!root)return;
const screen=document.getElementById('walkthrough-screen'),caption=document.getElementById('walkthrough-caption'),audience=document.getElementById('walkthrough-audience'),play=document.getElementById('walkthrough-play'),progress=document.getElementById('walkthrough-progress');
const sectors={
 dak:{business:'Dakwerken De Linde',service:'Opmeting dak',other:'Advies over dakrenovatie',duration:'45 min',field:'Adres van de woning',value:'Voorbeeldstraat 12, Gent',color:'#264653',tint:'#edf3f5'},
 airco:{business:'Klimaat aan Huis',service:'Advies & opmeting airco',other:'Onderhoud airco',duration:'45 min',field:'Adres van de woning',value:'Voorbeeldstraat 12, Gent',color:'#246c82',tint:'#eaf4f7'},
 solar:{business:'Zon op je Dak',service:'Advies zonnepanelen',other:'Controle bestaande installatie',duration:'30 min',field:'Adres van de woning',value:'Voorbeeldstraat 12, Gent',color:'#735a17',tint:'#fff6dc'},
 beauty:{business:'Studio Lune',service:'Laserontharing',other:'Gezichtsverzorging',duration:'45 min',field:'Wil je vooraf iets meegeven?',value:'Dit is mijn eerste bezoek.',color:'#7c4960',tint:'#faf0f4'},
 hair:{business:'Atelier Haar',service:'Knippen & brushing',other:'Adviesgesprek kleuring',duration:'60 min',field:'Wil je vooraf iets meegeven?',value:'Graag advies over mijn kapsel.',color:'#6a5144',tint:'#f7f0e9'},
 catering:{business:'Aan Tafel Catering',service:'Kennismaking voor je feest',other:'Menu bespreken',duration:'45 min',field:'Vertel ons over je plannen',value:'Een familiefeest voor 30 personen.',color:'#8b4935',tint:'#fff0e7'},
 garden:{business:'Groen & Buiten',service:'Tuinbezoek & opmeting',other:'Advies tuinonderhoud',duration:'45 min',field:'Adres van de tuin',value:'Voorbeeldstraat 12, Gent',color:'#3d694b',tint:'#edf5eb'},
 cleaning:{business:'Helder Schoon',service:'Plaatsbezoek voor een offerte',other:'Kennismaking bedrijfsschoonmaak',duration:'30 min',field:'Adres van het pand',value:'Voorbeeldstraat 12, Gent',color:'#256c70',tint:'#e9f6f5'},
 coach:{business:'Ruimte voor Groei',service:'Kennismakingsgesprek',other:'Individuele coaching',duration:'30 min',field:'Waar wil je aan werken?',value:'Meer rust en overzicht in mijn werk.',color:'#675481',tint:'#f3eff9'},
 garage:{business:'Garage De Baan',service:'Onderhoud wagen',other:'Diagnose & advies',duration:'60 min',field:'Wil je vooraf iets meegeven?',value:'Graag een jaarlijks onderhoud.',color:'#3e5879',tint:'#edf2f9'}
};
let selected='dak',step=0,timer=null,inView=!('IntersectionObserver' in window),wanted=true;
const reduced=window.matchMedia?.('(prefers-reduced-motion: reduce)');if(reduced?.matches)wanted=false;
const captions=['Je klant ziet de diensten van jouw zaak.','Een klik op de dienst opent meteen de kalender.','Je klant ziet welke dagen en uren beschikbaar zijn.','Een dag en een uur zijn gekozen.','Alleen nog de gegevens die jij nodig hebt.','Je klant vult de gegevens in en bevestigt de boeking.','Je klant ziet meteen een duidelijke bevestiging.','Automatisch: de aanvraag staat op je bord, de afspraak in je agenda en jij krijgt een e-mailmelding.','Jij volgt op: na contact verplaats je de kaart. Zo zie je wie al geholpen is.'];
const times=['09:00','11:00','14:30'];
function render(){
 const s=sectors[selected],filled=step>=5;root.style.setProperty('--sector-accent',s.color);root.style.setProperty('--sector-tint',s.tint);root.dataset.step=String(step);root.dataset.sector=selected;
 audience.textContent=step>=7?'2. Dit zie jij als ondernemer':'1. Dit ziet je klant';caption.textContent=captions[step];progress.textContent=(step+1)+' / 9';
 let html=`<div class="walk-business"><span aria-hidden="true">${s.business.slice(0,1)}</span><strong>${s.business}</strong></div>`;
 if(step<6)html+=`<div class="walk-steps"><span class="${step<2?'current':''}">1 Dienst</span><span class="${step>=2&&step<4?'current':''}">2 Moment</span><span class="${step>=4?'current':''}">3 Gegevens</span></div>`;
 if(step<2)html+=`<h3>Waarmee kunnen we je helpen?</h3><p>Kies een dienst.</p><div class="walk-service ${step===1?'picked click-pulse':''}"><strong>${s.service}</strong><small>${s.duration}</small>${step===1?'<span class="walk-check">✓</span>':''}</div><div class="walk-service"><strong>${s.other}</strong><small>Op afspraak</small></div>`;
 else if(step<4)html+=`<h3>Wanneer past het voor jou?</h3><p>${s.service} · ${s.duration}</p><div class="walk-month"><strong>Voorbeeldweek</strong><span>Jouw vrije momenten</span></div><div class="walk-dates">${['ma','di','wo','do','vr'].map((d,i)=>`<span class="${i===0?'unavailable':step===3&&i===2?'picked click-pulse':''}"><small>${d}</small><b>${18+i}</b></span>`).join('')}</div><div class="walk-times">${times.map(t=>`<span class="${step===3&&t==='11:00'?'picked':''}">${t}</span>`).join('')}</div><p class="walk-hint">Grijs: niet beschikbaar.</p>`;
 else if(step<6)html+=`<h3>Bijna geregeld.</h3><p>${s.service} · woensdag om 11:00</p><div class="walk-fields"><div><small>Je naam</small><span>${filled?'Emma Janssens':'Je naam'}</span></div><div><small>E-mailadres</small><span>${filled?'emma@example.test':'Je e-mailadres'}</span></div><div><small>${s.field}</small><span>${filled?s.value:'Jouw toelichting'}</span></div></div><div class="walk-submit ${filled?'click-pulse':''}">Afspraak bevestigen</div>`;
 else if(step===6)html+=`<div class="walk-thanks"><span aria-hidden="true">✓</span><h3>Bedankt voor je boeking!</h3><p>Je afspraak bij ${s.business} is bevestigd.</p><div>${s.service}<br><strong>Woensdag om 11:00</strong></div></div>`;
 else html=`<div class="walk-board-heading"><strong>${s.business}</strong><span>Aanvragen${step===7?'<b>1</b>':''}</span></div><h3>Elke aanvraag op zijn plek.</h3><div class="walk-board"><div><strong>Nieuw <small>${step===7?'1':'0'}</small></strong>${step===7?card(s):'<p>Alles opgevolgd.</p>'}</div><div><strong>Gecontacteerd <small>${step===8?'1':'0'}</small></strong>${step===8?card(s):'<p>Nog geen kaarten.</p>'}</div></div><div class="walk-receipts"><span>✓ In je agenda</span><span>✓ E-mailmelding naar jou</span><span>✓ Gegevens bewaard</span></div><p class="walk-hint">${step===7?'Dit gebeurt automatisch na de boeking.':'Deze stap doe jij na het contacteren van je klant.'}</p>`;
 screen.innerHTML=html;play.textContent=step===8?'Opnieuw afspelen':wanted?'Pauzeren':'Afspelen';document.getElementById('walkthrough-next').disabled=step===8;
}
function card(s){return `<article class="walk-lead"><small>${s.service}</small><strong>Emma Janssens</strong><p>Woensdag · 11:00</p><span>${step===8?'Contact opgenomen':'Klaar om op te volgen'}</span></article>`;}
function schedule(){window.clearTimeout(timer);if(wanted&&inView&&!document.hidden&&step<8)timer=window.setTimeout(()=>{step++;render();schedule();},step===6?3000:step>=7?3600:2200);}
function choose(key){selected=key;step=0;wanted=!reduced?.matches;for(const button of document.querySelectorAll('button[data-sector]'))button.setAttribute('aria-pressed',String(button.dataset.sector===key));render();schedule();}
for(const button of document.querySelectorAll('button[data-sector]'))button.addEventListener('click',()=>choose(button.dataset.sector));
play.addEventListener('click',()=>{if(step===8){step=0;wanted=true;}else wanted=!wanted;render();schedule();});
document.getElementById('walkthrough-next').addEventListener('click',()=>{wanted=false;step=Math.min(8,step+1);render();schedule();});
document.getElementById('walkthrough-replay').addEventListener('click',()=>{step=0;wanted=!reduced?.matches;render();schedule();});
document.addEventListener('visibilitychange',schedule);
if('IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;schedule();},{threshold:.15});observer.observe(root);}
reduced?.addEventListener?.('change',event=>{if(event.matches){wanted=false;render();schedule();}});
render();schedule();
})();
