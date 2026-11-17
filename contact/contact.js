'use strict';
const infoForm=document.getElementById('contact-form'),infoStatus=document.getElementById('contact-status'),infoButton=infoForm.querySelector('[type=submit]');
if(new URLSearchParams(location.search).get('interesse')==='crm')infoForm.elements.message.value='Ik ontvang graag meer informatie over de CRM-uitbreiding voor mijn zaak.';
infoForm.addEventListener('submit',async event=>{
 event.preventDefault();if(infoButton.disabled||!infoForm.reportValidity())return;
 const data=Object.fromEntries(new FormData(infoForm));
 if(!data.name.trim()||!data.company.trim()||!data.message.trim()){infoStatus.textContent='Vul je naam, bedrijfsnaam en vraag in.';return;}
 infoButton.disabled=true;infoStatus.textContent='Je vraag wordt verstuurd…';
 try{
  const response=await fetch('https://app.afspraakboeken.be/api/index.php?route=contact',{method:'POST',credentials:'omit',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
  const result=await response.json();if(!response.ok)throw new Error(result.error||'Je vraag kon niet worden verstuurd. Probeer opnieuw.');
  infoForm.hidden=true;const success=document.getElementById('contact-success');success.hidden=false;success.focus();
 }catch(error){infoStatus.textContent=error.message==='Failed to fetch'?'Geen verbinding. Je gegevens blijven staan; probeer opnieuw.':error.message||'Je vraag kon niet worden verstuurd. Probeer opnieuw.';infoButton.disabled=false;}
});
