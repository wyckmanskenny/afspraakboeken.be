const form=document.getElementById('contact-form');
const status=document.getElementById('contact-status');
const button=form.querySelector('button[type=submit]');
const endpoint='https://app.afspraakboeken.be/api/index.php';
async function availability(){
 try{const response=await fetch(endpoint+'?route=health',{credentials:'omit',cache:'no-store'});const result=await response.json();if(!response.ok||!result.ready)throw new Error();button.disabled=false;status.textContent='';}
 catch{status.textContent='Het contactformulier wordt nog geactiveerd. Je kunt intussen de boekingsdemo bekijken. Er worden nu geen aanvragen verzonden.';}
}
form.addEventListener('submit',async event=>{
 event.preventDefault();if(button.disabled||!form.reportValidity())return;
 button.disabled=true;status.textContent='Je aanvraag versturen…';status.classList.remove('error');
 try{
  const response=await fetch(endpoint+'?route=contact',{method:'POST',credentials:'omit',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(form)))});
  const result=await response.json();if(!response.ok)throw new Error(result.error||'Je aanvraag is niet verzonden. Probeer het opnieuw.');
  form.hidden=true;const done=document.getElementById('contact-success');done.hidden=false;done.focus();
 }catch(error){status.textContent=error.message==='Failed to fetch'?'Je aanvraag is niet verzonden. Controleer je verbinding en probeer opnieuw.':error.message;status.classList.add('error');button.disabled=false;}
});
availability();
