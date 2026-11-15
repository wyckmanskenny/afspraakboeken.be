import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const {Window}=await import(process.env.HAPPY_DOM_MODULE||'happy-dom');
const html=fs.readFileSync(new URL('../index.html',import.meta.url),'utf8');
const code=fs.readFileSync(new URL('../contact.js',import.meta.url),'utf8');
const tick=()=>new Promise(resolve=>setTimeout(resolve,5));
async function setup(fetch){
 const window=new Window({url:'https://afspraakboeken.be/'});
 window.document.body.innerHTML=html.match(/<body[^>]*>([\s\S]*)<\/body>/)[1].replace(/<script[\s\S]*?<\/script>/g,'');
 vm.runInNewContext(code,{document:window.document,FormData:window.FormData,fetch,console});await tick();
 return window;
}
test('The contact form stays disabled until the database is ready',async()=>{
 const w=await setup(async()=>({ok:false,json:async()=>({ready:false})}));
 assert.equal(w.document.querySelector('#contact-form button').disabled,true);
 assert.equal(w.document.getElementById('contact-success').hidden,true);
 assert.ok(w.document.getElementById('contact-status').textContent.includes('geen aanvragen verzonden'));
 await w.happyDOM.close();
});
test('A saved contact request shows success; a failed request keeps the entered data',async()=>{
 for(const succeeds of [true,false]){
  const requests=[];
  const w=await setup(async(url,options={})=>{
   if(!options.body)return {ok:true,json:async()=>({ready:true})};
   requests.push(JSON.parse(options.body));
   return {ok:succeeds,json:async()=>succeeds?{message:'Received'}:{error:'Niet opgeslagen'}};
  });
  const form=w.document.getElementById('contact-form');
  for(const [key,value] of Object.entries({name:'Test Name',company:'Test Company',email:'test@example.test',message:'A test request'}))form.querySelector(`[name=${key}]`).value=value;
  form.dispatchEvent(new w.Event('submit',{bubbles:true,cancelable:true}));await tick();
  assert.equal(requests.length,1);assert.equal(form.hidden,succeeds);assert.equal(w.document.getElementById('contact-success').hidden,!succeeds);
  if(!succeeds){assert.equal(form.querySelector('[name=message]').value,'A test request');assert.equal(w.document.getElementById('contact-status').textContent,'Niet opgeslagen');assert.equal(form.querySelector('button').disabled,false);}
  await w.happyDOM.close();
 }
});
test('The homepage uses manual onboarding and the isolated public demo',()=>{
 assert.match(html,/href="#contact">Account aanvragen/);
 assert.match(html,/src="\.\/contact\.js(?:\?[^\"]*)?"/);
 assert.ok(!html.includes('data-app-link="register"'));
 assert.match(fs.readFileSync(new URL('../site.js',import.meta.url),'utf8'),/demo\/\?mode=book&tenant=lune/);
});
