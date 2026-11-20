'use strict';
// The packaged homepage points to the separate app. The private review copy
// lives under /website/ alongside the app and keeps its navigation local.
const appBase=location.hostname.endsWith('.chatgpt.site')&&location.pathname.startsWith('/website/')?new URL('../',location.href):new URL('https://app.afspraakboeken.be/');
const targets={app:new URL('./',appBase),register:new URL('registreren/',appBase),trial:new URL('registreren/?mode=trial',appBase),booking:new URL('demo/?mode=book&tenant=lune',appBase)};
for(const [key,value] of Object.entries({primary:'#264653',secondary:'#2a9d8f',background:'#f8fafb'}))targets.booking.searchParams.set('theme_'+key,value);
for(const link of document.querySelectorAll('[data-app-link]'))link.href=targets[link.dataset.appLink].href;
const menu=document.querySelector('.menu-toggle'),navigation=document.getElementById('navigation');
const solutionsMenu=document.querySelector('.solutions-menu');
function closeMenu(){if(solutionsMenu)solutionsMenu.open=false;menu.setAttribute('aria-expanded','false');navigation.classList.remove('open')}
menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));navigation.classList.toggle('open',open)});
navigation.addEventListener('click',event=>{if(event.target.closest('a'))closeMenu()});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&menu.getAttribute('aria-expanded')==='true'){closeMenu();menu.focus()}});
for(const button of document.querySelectorAll('[data-palette]'))button.addEventListener('click',()=>{document.querySelector('[data-brand-demo]').dataset.palette=button.dataset.palette;for(const item of document.querySelectorAll('button[data-palette]'))item.setAttribute('aria-pressed',String(item===button))});
const demo=document.getElementById('demo-dialog'),frame=document.getElementById('demo-frame');let previousFocus;
for(const button of document.querySelectorAll('[data-open-demo]'))button.addEventListener('click',()=>{previousFocus=document.activeElement;if(!frame.getAttribute('src'))frame.src=targets.booking.href;demo.showModal();document.getElementById('close-demo').focus()});
document.getElementById('close-demo')?.addEventListener('click',()=>demo.close());
demo?.addEventListener('close',()=>previousFocus?.focus());
for(const link of document.querySelectorAll('[data-open-faq]'))link.addEventListener('click',()=>{document.getElementById(link.dataset.openFaq).open=true});

document.addEventListener('click',event=>{if(solutionsMenu?.open&&!solutionsMenu.contains(event.target))solutionsMenu.open=false;});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&solutionsMenu?.open){solutionsMenu.open=false;solutionsMenu.querySelector('summary').focus();}});
for(const link of navigation.querySelectorAll('a')){const url=new URL(link.href,location.href);if(url.origin===location.origin&&!url.hash&&url.pathname===location.pathname)link.setAttribute('aria-current','page');}

// Hover for a mouse; native details click/keyboard behavior remains available.
let solutionCloseTimer;
solutionsMenu?.addEventListener('pointerenter',event=>{if(event.pointerType!=='mouse')return;document.defaultView.clearTimeout(solutionCloseTimer);solutionsMenu.open=true;});
solutionsMenu?.addEventListener('pointerleave',event=>{if(event.pointerType!=='mouse')return;document.defaultView.clearTimeout(solutionCloseTimer);solutionCloseTimer=document.defaultView.setTimeout(()=>{if(!solutionsMenu.contains(document.activeElement))solutionsMenu.open=false;},220);});
solutionsMenu?.addEventListener('focusout',()=>{document.defaultView.setTimeout(()=>{if(!solutionsMenu.contains(document.activeElement)&&!solutionsMenu.matches(':hover'))solutionsMenu.open=false;},0);});

// Homepage-only shortcuts, revealed after ten percent of the scrollable page.
const floatingActions=document.getElementById('floating-actions');
if(floatingActions){
 const viewport=document.defaultView;
 const updateFloating=()=>{const distance=document.documentElement.scrollHeight-viewport.innerHeight;floatingActions.hidden=distance<=0||viewport.scrollY/distance<0.1;};
 viewport.addEventListener('scroll',updateFloating,{passive:true});viewport.addEventListener('resize',updateFloating);viewport.addEventListener('load',updateFloating);updateFloating();
}
