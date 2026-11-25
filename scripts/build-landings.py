"""Generate public landing pages and shared navigation from reviewed copy."""
from pathlib import Path
from html import escape as e
import re,json
R=Path(__file__).resolve().parents[1]
# slug, label, title, description, heading, introduction, three explanatory sections, FAQs
pages=[('slim-contactformulier',
  'Slim contactformulier',
  'Slim contactformulier voor je website | Afspraakboeken.be',
  'Verzamel aanvragen via een slim contactformulier in je huisstijl. Ontvang de juiste gegevens en volg elke '
  'aanvraag overzichtelijk op.',
  'Een slim contactformulier, gekoppeld aan je opvolging.',
  'Laat bezoekers vertellen wat ze nodig hebben en eventueel meteen een afspraak kiezen. Elke aanvraag komt '
  'overzichtelijk op je bord. Met de optionele CRM-uitbreiding houd je ook klantgegevens, notities en '
  'vervolgacties bij elkaar.',
  [('Betere gesprekken beginnen met de juiste informatie',
    'Laat een bezoeker een dienst kiezen en vraag de gegevens die je nodig hebt. Denk aan een adres voor een '
    'opmeting of een korte toelichting bij een adviesvraag. Zo kun jij beoordelen of de aanvraag bij je '
    'bedrijf past. Voor eigen extra vragen is er de optionele CRM-uitbreiding.'),
   ('Met of zonder een afspraak',
    'Laat bezoekers meteen een dienst en een vrij moment kiezen. Wil je eerst zelf overleggen? Ontvang dan '
    'alleen een aanvraag, zonder een tijdstip te reserveren.'),
   ('Van je website naar je aanvraagbord',
    'Plaats het formulier rechtstreeks op je website of laat het openen via een knop. Elke aanvraag wordt '
    'bewaard in je omgeving en je krijgt een e-mailmelding. Je ziet wie nog een antwoord nodig heeft.')],
  [('Moet ik mijn website vervangen?',
    'Nee. Je voegt de widget toe aan je bestaande website. Het formulier kan meteen zichtbaar zijn of via '
    'een knop openen.'),
   ('Kan ik zelf de velden kiezen?',
    'Je beheert de standaardvelden in de widgetinstellingen. Eigen extra vragen zijn onderdeel van de '
    'optionele CRM-uitbreiding.'),
   ('Moet iemand altijd een afspraak boeken?',
    'Nee. In de aanvraagmodus sla je de kalender over. Je neemt daarna zelf contact op om de volgende stap '
    'af te spreken.')]),
 ('online-afspraken',
  'Online afspraken',
  'Online boekingssysteem voor je website | Afspraakboeken.be',
  'Een eenvoudig online boekingssysteem voor zelfstandigen en kleine bedrijven. Laat klanten afspraken '
  'boeken en houd de opvolging bij op één bord.',
  'Een online boekingssysteem dat ook de opvolging bijhoudt.',
  'Van een gerichte aanvraag naar een ingeplande afspraak: je klant kiest een dienst, een vrij moment en '
  'vult de nodige gegevens in. Jij begint het gesprek met meer context en volgt de aanvraag verder op vanuit '
  'dezelfde omgeving.',
  [('Jouw diensten, jouw beschikbare momenten',
    'Voeg je diensten toe en bepaal de duur. Stel je beschikbaarheid in en blokkeer momenten waarop je niet '
    'kunt. Bezoekers kiezen uit de beschikbare tijdstippen.'),
   ('Een korte route naar een bevestigde afspraak',
    'Je klant kiest een dienst, een datum en een uur, en vult de gegevens in. Het bedanktscherm bevestigt de '
    'boeking. De afspraak verschijnt in je agenda en op je aanvraagbord.'),
   ('Ook overzicht na het inplannen',
    'Bekijk de contactgegevens en zie wat nog opvolging vraagt. Een afspraak aanpassen of verplaatsen doe je '
    'in de app. Een gekoppelde Google-agenda kan bezette momenten meenemen in je beschikbaarheid.')],
  [('Kan ik een volledige dag blokkeren?',
    'Ja. Geblokkeerde dagen zijn niet beschikbaar voor nieuwe boekingen. Je behoudt zelf controle over je '
    'agenda.'),
   ('Kan ik ook aanvragen zonder afspraak ontvangen?',
    'Ja. Je kunt kiezen voor een aanvraagformulier zonder kalender. Een tijdstip leg je dan later samen '
    'vast.'),
   ('Krijgt mijn klant een bevestiging?',
    'Na het boeken ziet je klant een bevestigingsscherm. Jij ontvangt een e-mailmelding van de boeking. '
    'Automatische bevestigingsmails naar klanten worden hier niet als inbegrepen functie aangeboden.'),
   ('Verstuurt het boekingssysteem een afspraakherinnering?',
    'Automatische afspraakherinneringen per e-mail of sms zijn momenteel niet beschikbaar. De klant ziet na '
    'de boeking een bevestigingsscherm. Jij ontvangt een e-mailmelding en kunt zelf contact opnemen met je '
    'klant.')]),
 ('aanvragen-opvolgen',
  'Aanvragen opvolgen',
  'Eenvoudig leads opvolgen op één bord | Afspraakboeken.be',
  'Volg leads en aanvragen eenvoudig op. Verzamel nieuwe contacten via je website en zie op je bord wie je '
  'nog moet bellen of beantwoorden.',
  'Eindelijk eenvoudig leads opvolgen en verder helpen.',
  'Van een eerste vraag naar een afspraak en een mogelijke nieuwe klant: zie welke stap aan de beurt is. '
  'Verzamel aanvragen op één bord, neem gericht contact op en houd bij wie je al geholpen hebt.',
  [('Nieuwe aanvragen verschijnen vanzelf',
    'Wanneer iemand je formulier invult, verschijnt de aanvraag in de eerste kolom. Je krijgt een melding en '
    'hoeft de gegevens niet vanuit een e-mail over te typen.'),
   ('Maak de kolommen passend voor jouw werk',
    'Begin eenvoudig met Nieuw, Gecontacteerd en Afgerond. Je kunt kolomnamen aanpassen en kolommen '
    'toevoegen. Verplaats de kaart wanneer je een klant hebt gesproken of een aanvraag hebt afgerond.'),
   ('Van interesse naar een volgende stap',
    'Een aanvraag wordt pas een klant als je ermee aan de slag gaat. Bel terug, bespreek de behoefte en plan '
    'waar nodig een afspraak. Ook een lead uit een telefoongesprek voeg je zelf toe aan het bord. Zo werk je '
    'gericht aan het omzetten van interesse in klanten.')],
  [('Is dit aanvraagbord een betaalde CRM-uitbreiding?',
    'Het aanvraagbord hoort bij de basis. De optionele CRM-uitbreiding voegt onder meer klantfiches, interne '
    'notities en opvolgacties toe.'),
   ('Wordt de opvolging automatisch uitgevoerd?',
    'Het ontvangen en bewaren van de aanvraag gebeurt automatisch. Jij neemt contact op en verplaatst de '
    'kaart wanneer je een stap hebt gezet.'),
   ('Kan ik de indeling veranderen?',
    'Ja. Je kunt kolommen hernoemen en toevoegen, zodat het bord aansluit op jouw manier van werken.')]),
 ('crm-voor-zelfstandigen',
  'CRM voor zelfstandigen',
  'Eenvoudig CRM voor zelfstandigen en kmo’s | Afspraakboeken.be',
  'Een eenvoudig CRM voor zelfstandigen en kleine kmo’s. Bewaar contacten, interne notities en opvolgacties '
  'met de optionele CRM-uitbreiding.',
  'Eindelijk een eenvoudig CRM voor zelfstandigen en ondernemers.',
  'Je wilt weten wie je klant is, wat jullie besproken hebben en wat je nog moet doen. De optionele '
  'CRM-uitbreiding brengt contacten, interne notities en opvolgacties samen met je aanvragen. Overzichtelijk '
  'klantenbeheer voor jouw bedrijf, ook als kleine kmo.',
  [('Een klantfiche met de informatie bij elkaar',
    'Bewaar contactgegevens en raadpleeg de informatie die je voor de opvolging nodig hebt. Zo begin je bij '
    'een volgend gesprek met de context van je klant.'),
   ('Leg afspraken en volgende stappen vast',
    'Voeg interne notities en opvolgacties toe. Noteer bijvoorbeeld dat een klant eerst wil overleggen of '
    'dat je later nog eens moet bellen. Jij blijft zelf verantwoordelijk voor die opvolging.'),
   ('Breid verder uit op je aanvraagbord',
    'Het basisbord helpt je aanvragen opvolgen. De CRM-uitbreiding voegt contactbeheer toe, met de '
    'mogelijkheid om contacten te exporteren. Bekijk de formule of vraag ons welke uitbreiding bij jouw zaak '
    'past.')],
  [('Is CRM standaard inbegrepen?',
    'Nee. CRM is een optionele, betalende uitbreiding. Het aanvraagbord is wel onderdeel van de basis. We '
    'lichten de mogelijkheden en prijs toe vóór je activeert.'),
   ('Kan ik contacten exporteren?',
    'Ja. Met de CRM-uitbreiding kun je contacten exporteren als CSV, bijvoorbeeld om ze verder te '
    'verwerken.'),
   ('Is CRM nodig om aanvragen te ontvangen?',
    'Nee. Je kunt starten met het formulier, de agenda en het aanvraagbord. Breid uit als je meer '
    'klantinformatie wilt bijhouden.'),
   ('Past dit CRM bij een kleine kmo?',
    'Als je vooral contacten, aanvragen, notities en volgende acties wilt bijhouden, kun je eenvoudig '
    'beginnen. Bespreek vooraf je team en werkwijze met ons als je uitgebreide toegangsrechten, facturatie '
    'of projectplanning nodig hebt.')]),
 ('sector/dakwerkers',
  'Dakwerkers',
  'CRM en aanvragen opvolgen voor dakwerkers | Afspraakboeken.be',
  'Volg aanvragen voor dakwerken op, plan dakinspecties en opmetingen en breid uit met eenvoudig CRM. Houd '
  'contact en offerteopvolging overzichtelijk.',
  'Aanvragen opvolgen en klanten beheren als dakwerker.',
  'Van een lekkend plat dak tot een volledige dakrenovatie: elke aanvraag vraagt een andere aanpak. Verzamel '
  'de eerste informatie, plan een dakinspectie of opmeting en houd bij wie nog op jouw antwoord wacht. Breid '
  'uit met CRM als je klantnotities en opvolgacties wilt bewaren.',
  [('Dakinspecties en opmetingen gericht voorbereiden',
    'Maak diensten zoals Dakinspectie, Opmeting dakrenovatie en Advies dakisolatie aan. Vraag het werfadres '
    'en een toelichting over de dakwerken. Zo weet je waarover het gesprek gaat voordat je een bezoek '
    'vastlegt.'),
   ('Plan alleen wat je rechtstreeks wilt laten boeken',
    'Een opmeting kan een vaste duur krijgen. Beoordeel je liever eerst de werken en de verplaatsing? '
    'Gebruik dan de aanvraagmodus en spreek het bezoek zelf af. Voor dringende schade kun je op je website '
    'je telefonische bereikbaarheid aangeven.'),
   ('Offerteopvolging op je aanvraagbord',
    'Gebruik kolommen zoals Nieuwe aanvraag, Opmeting gepland, Offerte verstuurd en Nabellen. Jij verplaatst '
    'de kaart wanneer je een stap hebt gezet. Je maakt de offerte in je eigen pakket; het bord helpt je '
    'onthouden welke aanvragen je nog moet opvolgen.')],
  [('Kan ik eerst de aanvraag beoordelen?',
    'Ja. Kies de werkwijze zonder kalender. Er wordt dan geen moment vastgelegd voordat je zelf contact '
    'opneemt.'),
   ('Kan ik het adres laten invullen?',
    'Ja. Je kunt de adresvelden zichtbaar en verplicht maken, zodat je weet waar het plaatsbezoek moet '
    'gebeuren.'),
   ('Maakt het systeem ook offertes?',
    'Nee. Het aanvraagbord helpt je de opvolging bijhouden. Je maakt en verstuurt je offertes via je eigen '
    'werkwijze.'),
   ('Wat voegt CRM toe voor mijn dakbedrijf?',
    'Het aanvraagbord zit in de basis. Met de optionele CRM-uitbreiding bewaar je daarnaast contactgegevens, '
    'interne notities en opvolgacties. Bijvoorbeeld dat je een klant na het bespreken van de dakrenovatie '
    'opnieuw wilt bellen.')]),
 ('sector/beauty-wellness',
  'Beauty & wellness',
  'Online boekingssysteem voor beauty & wellness | Afspraakboeken.be',
  'Een online boekingssysteem voor je schoonheidssalon of wellnesszaak. Laat behandelingen boeken, beheer je '
  'agenda en breid uit met klantenbeheer.',
  'Een online boekingssysteem voor je schoonheidssalon.',
  'Terwijl jij een behandeling uitvoert, kiest een klant online een vrij moment voor laserontharing of '
  'gezichtsverzorging. Beheer je behandelingen en salonagenda in één omgeving, met een aanvraagbord voor '
  'vragen die eerst persoonlijk advies nodig hebben.',
  [('Online afspraken voor jouw behandelingen',
    'Geef laserontharing, een gelaatsverzorging of een kennismaking een eigen omschrijving, duur en prijs. '
    'Je klant kiest een behandeling en ziet de beschikbare momenten in je agenda.'),
   ('Laat je agenda aansluiten op je werkdag',
    'Bepaal je beschikbare momenten en blokkeer dagen waarop je gesloten bent. De klant kiest een tijdstip '
    'en vult de contactgegevens in, gevolgd door een duidelijk bedanktscherm.'),
   ('Houd ook kennismakingsvragen bij',
    'Wil een bezoeker eerst advies? Je kunt ook werken met aanvragen zonder tijdslot. Volg die op via het '
    'bord. Met de optionele CRM-uitbreiding kun je algemene klantnotities en opvolgacties bijhouden.')],
  [('Kan ik verschillende behandelingsduren instellen?',
    'Ja. Je bepaalt de duur per dienst, zodat klanten een passend beschikbaar moment kunnen kiezen.'),
   ('Kunnen klanten ook alleen informatie aanvragen?',
    'Ja. In de aanvraagmodus wordt geen tijdslot geboekt. Je neemt zelf contact op om de vraag of '
    'behandeling te bespreken.'),
   ('Moet een klant online betalen?',
    'Nee. Deze boekingsflow vraagt geen online betaling. Je rekent af via je eigen werkwijze.'),
   ('Verstuurt het boekingssysteem een afspraakherinnering?',
    'Automatische afspraakherinneringen per e-mail of sms zijn momenteel niet beschikbaar. De klant ziet na '
    'de boeking een bevestigingsscherm. Jij ontvangt een e-mailmelding en kunt zelf contact opnemen met je '
    'klant.')]),
 ('sector/installateurs',
  'Installateurs',
  'Klantenbeheer en CRM voor installateurs | Afspraakboeken.be',
  'Houd installatieaanvragen, plaatsbezoeken en opvolging bij. Eenvoudig klantenbeheer voor installateurs, '
  'met een optionele CRM-uitbreiding.',
  'Klantenbeheer voor installateurs, van aanvraag tot plaatsbezoek.',
  'Een aanvraag voor een warmtepomp is iets anders dan airco-onderhoud. Breng installatievragen en '
  'adviesbezoeken samen op één bord. Zie welke klant je moet terugbellen en gebruik de optionele '
  'CRM-uitbreiding voor contactnotities en vervolgacties.',
  [('Van airco-onderhoud tot advies over een warmtepomp',
    'Maak aparte diensten voor een technische opname, een adviesbezoek of onderhoud. Het installatieadres en '
    'een korte toelichting helpen je de vraag te beoordelen. Bij een storing kun je eerst zelf contact '
    'opnemen om de dringendheid en duur in te schatten.'),
   ('Kies wanneer een bezoek rechtstreeks boekbaar is',
    'Werk met vaste momenten voor adviesgesprekken. Is de duur van de opdracht nog onduidelijk? Laat dan '
    'eerst een aanvraag indienen en plan zelf in na overleg. Het systeem plant geen routes tussen adressen.'),
   ('Aanvragen en offertes blijven in beeld',
    'Gebruik bijvoorbeeld de kolommen Nieuw, Technische opname gepland, Offerte verstuurd en Klant '
    'terugbellen. Zo houd je de commerciële opvolging bij. Met CRM voeg je interne notities en opvolgacties '
    'toe. Het systeem maakt geen offertes of werkbonnen.')],
  [('Kan ik onderhoud en advies apart aanbieden?',
    'Ja. Je beheert zelf je diensten en de bijbehorende duur en omschrijving.'),
   ('Plant het systeem mijn verplaatsingen?',
    'Nee. Jij houdt rekening met verplaatsingen en bepaalt welke momenten je openstelt. Bij complexe '
    'planning kun je eerst aanvragen ontvangen zonder tijdslot.'),
   ('Kan ik een telefonisch ontvangen aanvraag toevoegen?',
    'Ja. Je kunt zelf een nieuwe lead toevoegen aan je aanvraagbord.')]),
 ('sector/tuinaannemers',
  'Tuinaannemers',
  'Klantenbeheer voor tuinaannemers | Afspraakboeken.be',
  'Volg aanvragen voor tuinaanleg en tuinonderhoud op. Plan tuinbezoeken en opmetingen en voeg klantnotities '
  'toe met de optionele CRM-uitbreiding.',
  'Overzichtelijk klantenbeheer voor tuinaannemers.',
  'Een terras aanleggen, een tuin renoveren of een onderhoudsvraag: houd nieuwe tuinprojecten bij vanaf het '
  'eerste contact. Plan een tuinbezoek en zie welke klant nog een antwoord of een vervolggesprek verwacht.',
  [('Tuinaanleg en tuinonderhoud apart ontvangen',
    'Bied een tuinbezoek voor een nieuwe aanleg, een opmeting voor een terras of een adviesgesprek over '
    'onderhoud aan. Met het adres en een korte projectomschrijving kun je de eerste vraag gericht '
    'beoordelen.'),
   ('Een kennismaking plannen, op jouw voorwaarden',
    'Bepaal wanneer je plaatsbezoeken kunt doen. Wil je eerst de regio of omvang van de werken bespreken? '
    'Sla de kalender over en ontvang een aanvraag die je zelf inplant.'),
   ('Een tuinproject blijft zichtbaar tot de klant beslist',
    'Houd aanvragen bij in kolommen zoals Tuinbezoek plannen, Offerte besproken en Later opnieuw bellen. '
    'Noteer in de optionele CRM-uitbreiding wat besproken is en welke actie volgt. Offertes berekenen en de '
    'uitvoering plannen doe je via je eigen werkwijze.')],
  [('Kan ik alleen aanvragen ontvangen?',
    'Ja. Je hoeft geen beschikbare agenda te tonen. Je spreekt zelf een plaatsbezoek af nadat je de aanvraag '
    'hebt bekeken.'),
   ('Kan ik eigen vragen over een tuinproject toevoegen?',
    'De basis bevat standaardvelden zoals adres en opmerkingen. Voor eigen extra vragen kun je de optionele '
    'CRM-uitbreiding gebruiken.'),
   ('Kan ik ook de uitvoering van werken plannen?',
    'De tool helpt bij afspraken en aanvraagopvolging. Het is geen volledige werfplanning of planning voor '
    'meerdere ploegen.')])]
# Sector-specific CRM search intent; retain existing URLs to avoid competing pages.
crm_updates={
 'sector/dakwerkers':('Eenvoudig CRM voor dakwerkers | Afspraakboeken.be','Eenvoudig CRM voor je dakwerkersbedrijf. Verzamel aanvragen voor dakwerken, plan opmetingen en bewaar klantnotities met de optionele CRM-module.','Eenvoudig CRM voor dakwerkers, van dakopmeting tot opvolging.'),
 'sector/beauty-wellness':('Eenvoudig CRM voor je beautysalon | Afspraakboeken.be','Combineer online boekingen met eenvoudig CRM voor je beautysalon. Bewaar contactgegevens en notities en volg aanvragen op vanuit één omgeving.','Eenvoudig CRM voor je beautysalon, naast je online agenda.')
}
for i,page in enumerate(pages):
 if page[0] in crm_updates:
  data=list(page);data[2],data[3],data[4]=crm_updates[page[0]]
  data[7]=list(data[7])+[('Is CRM inbegrepen in het basispakket?','Het aanvraagbord en de afspraakplanning horen bij de basis. Contactfiches, interne notities en opvolgacties zijn onderdeel van de optionele CRM-module. Bekijk de prijzen of vraag ons welk pakket bij je zaak past.')]
  pages[i]=tuple(data)
pages.extend([
 ('sector/airco-installateurs','Airco-installateurs',
  'Eenvoudig CRM voor airco-installateurs | Afspraakboeken.be',
  'Houd airco-aanvragen, plaatsbezoeken en klantnotities bij. Eenvoudig CRM voor airco-installateurs, als extra module naast je formulier en aanvraagbord.',
  'Eenvoudig CRM voor airco-installateurs. Meer overzicht tussen twee installaties.',
  'Een vraag over een split-airco, een plaatsbezoek voor meerdere ruimtes of een onderhoudsaanvraag: ontvang alles in dezelfde omgeving. Met de optionele CRM-module bewaar je de contactgegevens, afspraken uit het gesprek en volgende actie bij je klant.',
  [('Ontvang gerichte aanvragen voor airconditioning','Maak diensten voor advies over een nieuwe airco, een plaatsbezoek en onderhoud. Vraag het installatieadres en een toelichting. Met eigen extra vragen in de CRM-module kun je ook vragen hoeveel ruimtes de klant wil koelen.'),
   ('Plan een technische opname wanneer het past','Laat klanten een beschikbaar moment voor een adviesbezoek kiezen. Wil je eerst de situatie bespreken? Ontvang de aanvraag zonder kalender en spreek zelf een bezoek af. Jij houdt rekening met reistijd en de duur van het bezoek.'),
   ('Weet welke klant nog een antwoord verwacht','Gebruik kolommen zoals Nieuw, Plaatsbezoek gepland, Offerte verstuurd en Terugbellen. Bewaar met CRM wat je besproken hebt over de ruimtes en plaatsing. Je offerte maak je via je eigen werkwijze; Afspraakboeken helpt je de aanvraag op te volgen.')],
  [('Is dit een volledig installatiepakket?','Nee. De omgeving helpt je aanvragen, afspraken en contacten beheren. Technische berekeningen, routeplanning en werkbonnen vallen daar niet onder.'),
   ('Kan ik onderhoud en nieuwe installaties apart ontvangen?','Ja. Maak aparte diensten met een eigen omschrijving en duur. Kies of klanten direct boeken of eerst een aanvraag sturen.'),
   ('Moet ik meteen CRM nemen?','Nee. Je kunt starten met het formulier, de agenda en het aanvraagbord. De CRM-module is een optionele uitbreiding voor contactfiches, interne notities en opvolgacties.')]),
 ('sector/elektriciens','Elektriciens',
  'Eenvoudig CRM voor elektriciens | Afspraakboeken.be',
  'Eenvoudig CRM voor elektriciens: verzamel aanvragen voor elektrische werken, plan plaatsbezoeken en volg klanten op. CRM is een optionele uitbreiding.',
  'Eenvoudig CRM voor elektriciens. Houd elke aanvraag in beeld.',
  'Een laadpaal plaatsen, een zekeringkast vervangen of elektrische werken bij een renovatie: elke aanvraag vraagt andere voorbereiding. Verzamel de eerste informatie via je website en houd op je aanvraagbord bij wie je nog moet contacteren. Voeg CRM toe voor contactfiches en interne notities.',
  [('Vraag vooraf waarover de elektrische werken gaan','Bied diensten aan zoals een plaatsbezoek voor renovatie, advies over een laadpaal of een aanvraag voor een nieuwe zekeringkast. Het adres en een korte omschrijving geven je context voordat je terugbelt.'),
   ('Kies zelf wat online boekbaar is','Stel vaste momenten open voor kennismakingen en plaatsbezoeken. Bij een storing of een onduidelijke opdracht laat je eerst een aanvraag sturen. Zo beoordeel je zelf de dringendheid en spreek je een geschikt moment af.'),
   ('Van eerste telefoontje tot duidelijke volgende stap','Voeg ook telefonische aanvragen toe aan het bord. Werk met kolommen zoals Nieuw, Bezoek afgesproken en Offerte opvolgen. Met de optionele CRM-module noteer je wat besproken is en welke opvolgactie nodig is, zodat je het gesprek later gemakkelijk hervat.')],
  [('Is dit geschikt voor een zelfstandige elektricien?','Ja. Je beheert zelf de diensten en kolommen. Je kunt eenvoudig beginnen met aanvragen ontvangen en pas later de optionele CRM-module toevoegen.'),
   ('Kan ik offertes en keuringsverslagen maken?','Nee. Afspraakboeken ondersteunt aanvraagopvolging, afspraakplanning en optioneel klantenbeheer. Offertes en technische documenten maak je via je eigen werkwijze.'),
   ('Kunnen klanten ook alleen informatie aanvragen?','Ja. Met de aanvraagmodus slaan bezoekers de kalender over. Jij neemt daarna contact op en plant eventueel een plaatsbezoek.')])
])
categories=json.loads((R/'scripts/sector-categories.json').read_text())
category_by_slug={'sector/'+c['slug']:c for c in categories}
for c in categories:
 slug='sector/'+c['slug']
 if any(p[0]==slug for p in pages):continue
 sections=c['sections']
 faqs=[(c['question'],c['answer']),('Kan ik starten zonder CRM?','Ja. Het slimme formulier, de afspraakplanning en het aanvraagbord vormen de basis. Contactfiches, interne notities en opvolgacties zijn onderdeel van de optionele CRM-module.'),('Hoe plaats ik dit op mijn website?','Je voegt de widget toe aan je bestaande website. Toon het formulier meteen op de pagina of laat het via een knop openen. Je beheert de diensten en kleuren vanuit je account.')]
 pages.append((slug,c['label'],c['title'],c['description'],c['heading'],c['intro'],sections,faqs))
def sector_details(slug,label,sections):
 c=category_by_slug.get(slug)
 rows=c['rows'] if c else [(h,t,'Bekijk en volg de aanvraag op in je omgeving') for h,t in sections]
 benefits=c['benefits'] if c else ['Je diensten en beschikbare momenten zelf beheren','Aanvragen verzamelen op één overzichtelijk bord','Optioneel uitbreiden met CRM voor contacten en interne notities']
 table='<section class="wrap sector-usecases"><h2>Zo gebruik je Afspraakboeken in '+e(label.lower())+'</h2><div class="sector-table-scroll" tabindex="0" role="region" aria-label="Praktijkvoorbeelden voor '+e(label)+'"><table><caption>Van klantvraag naar een volgende stap</caption><thead><tr><th scope="col">Situatie</th><th scope="col">Via jouw formulier</th><th scope="col">Jouw opvolging</th></tr></thead><tbody>'+''.join('<tr><th scope="row">'+e(a)+'</th><td>'+e(b)+'</td><td>'+e(d)+'</td></tr>' for a,b,d in rows)+'</tbody></table></div></section>'
 table+='<section class="wrap sector-advantages"><h2>De voordelen voor jouw organisatie</h2><ul>'+''.join('<li>'+e(b)+'</li>' for b in benefits)+'</ul><p>Het aanvraagbord hoort bij de basis. CRM is een optionele uitbreiding. <a href="/prijzen/">Bekijk de pakketten en prijzen</a>.</p></section>'
 if c and c['related']:
  table+='<section class="wrap landing-related"><h2>Meer voorbeelden voor jouw vak</h2><div>'+''.join('<a href="/sector/'+e(k)+'/">'+e(next(p[1] for p in pages if p[0]=='sector/'+k))+'</a>' for k in c['related'])+'</div></section>'
 return table
header=(R/'partials/header.html').read_text().strip()
links={'/alles-in-1/#contactformulier':'/slim-contactformulier/','/alles-in-1/#afspraken':'/online-afspraken/','/alles-in-1/#aanvragen':'/aanvragen-opvolgen/','/alles-in-1/#crm':'/crm-voor-zelfstandigen/'}
for old,new in links.items():header=header.replace(old,new)
(R/'partials/header.html').write_text(header+'\n')
footer='<footer class="footer marketing-footer wrap"><div class="footer-brand"><a class="logo" href="/"><strong>afspraakboeken<span>.be</span></strong></a><p>Van eerste aanvraag tot duidelijke opvolging.</p></div><nav aria-label="Oplossingen in de footer"><h2>Oplossingen</h2>'+''.join(f'<a href="/{p[0]}/">{e(p[1])}</a>' for p in pages[:4])+'<a href="/alles-in-1/">Alle oplossingen</a></nav><nav aria-label="Sectoren in de footer"><h2>Sectoren</h2>'+''.join(f'<a href="/{p[0]}/">{e(p[1])}</a>' for p in [next(p for p in pages if p[0]=='sector/'+c['slug']) for c in categories[:6]])+'<a href="/sector/">Bekijk alle sectoren</a></nav><nav aria-label="Over Afspraakboeken.be"><h2>Afspraakboeken.be</h2><a href="/prijzen/">Prijzen</a><a href="https://app.afspraakboeken.be/demo/?mode=choose&amp;tenant=lune&amp;v=0.20.1">Bekijk de demo</a><a href="/contact/">Contacteer ons</a><a href="https://app.afspraakboeken.be/">Inloggen</a><a href="/#privacy">Privacyinformatie</a></nav><div class="footer-bottom"><small>© 2026 Afspraakboeken.be</small><small>Wycked Media ®</small></div></footer>'
(R/'partials/footer.html').write_text(footer+'\n')
home=(R/'index.html').read_text()
walk=re.search(r'(<div id="sector-walkthrough".*?</noscript></div>)',home).group(1)
keys={'sector/dakwerkers':'dak','sector/beauty-wellness':'beauty','sector/installateurs':'airco','sector/tuinaannemers':'garden','online-afspraken':'dak'}
def shell(slug,title,desc,body,animated=False):
 url='https://afspraakboeken.be/'+slug+'/'
 return '<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="index,follow,max-image-preview:large"><title>'+e(title)+'</title><meta name="description" content="'+e(desc)+'"><link rel="canonical" href="'+url+'"><meta property="og:type" content="website"><meta property="og:locale" content="nl_BE"><meta property="og:title" content="'+e(title)+'"><meta property="og:description" content="'+e(desc)+'"><meta property="og:url" content="'+url+'"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/site.css?v=0.20.8"><script src="/site.js?v=0.20.1" defer></script>'+('<script src="/sector-demo.js?v=0.16.0" defer></script>' if animated else '')+'<script src="/privacy.js?v=0.20.0" data-gtm="GTM-KDF5GK88" defer></script></head><body><a class="skip" href="#inhoud">Naar de inhoud</a>'+header+'<main id="inhoud">'+body+'</main>'+footer+'</body></html>\n'
def save(slug,text):
 p=R/slug/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
cta='<div class="actions"><a class="button light" href="https://app.afspraakboeken.be/registreren/?mode=trial">14 dagen gratis proberen</a><a class="text-link" href="/contact/">Contacteer ons</a></div><p class="landing-note">Geen creditcard nodig. Geen automatische betaling.</p>'
for slug,label,title,desc,heading,intro,sections,faqs in pages:
 sector=slug.startswith('sector/')
 animated=slug in keys
 if animated:visual=walk.replace('class="sector-walkthrough"',f'class="sector-walkthrough" data-initial-sector="{keys[slug]}"')
 elif slug in category_by_slug:
  c=category_by_slug[slug]
  visual='<div class="landing-preview"><small>Voorbeeld voor '+e(label)+'</small><h2>'+e(c['rows'][0][0])+'</h2><div class="demo-field">Naam en contactgegevens</div><div class="demo-field tall">'+e(c['rows'][0][1])+'</div><div class="demo-field">'+e(c['rows'][0][2])+'</div><p>Jij kiest of bezoekers direct boeken of eerst een aanvraag sturen.</p></div>'
 elif slug=='slim-contactformulier':visual='<div class="landing-preview"><small>Voorbeeld · formulier op je website</small><h2>Vertel ons over je plannen.</h2><div class="demo-field">Naam</div><div class="demo-field">E-mailadres</div><div class="demo-field tall">Waarmee kunnen we je helpen?</div><span class="demo-action">Aanvraag versturen</span><p>De aanvraag verschijnt automatisch op jouw bord.</p></div>'
 elif slug=='aanvragen-opvolgen':visual='<div class="landing-preview"><small>Voorbeeld · jouw aanvraagbord</small><h2>Wie vraagt je aandacht?</h2><div class="mini-board-columns"><div><strong>Nieuw</strong><article>Sam Peeters<small>Vraag over een plaatsbezoek</small></article></div><div><strong>Gecontacteerd</strong><article>Noor Jacobs<small>Wacht op antwoord</small></article></div><div><strong>Afgerond</strong><article>Alex Claes<small>Opvolging klaar</small></article></div></div><p>Jij verplaatst de kaart na het opvolgen.</p></div>'
 else:visual='<div class="landing-preview"><small>Voorbeeld · optionele CRM-uitbreiding</small><h2>Sam Peeters</h2><div class="demo-field">Contactgegevens · sam@example.test</div><div class="demo-field tall">Interne notitie<br>Bespreekt de plannen deze week met de partner.</div><div class="demo-field">Volgende actie · opnieuw bellen</div><p>Fictieve gegevens. Alle context bij je contact.</p></div>'
 body='<div class="wrap landing-breadcrumb"><a href="/">Home</a> / <a href="'+('/sector/' if slug.startswith('sector/') else '/alles-in-1/')+'">'+('Sectoren' if slug.startswith('sector/') else 'Oplossingen')+'</a> / '+e(label)+'</div><section class="wrap landing-hero"><div><h1>'+e(heading)+'</h1><p class="landing-intro">'+e(intro)+'</p>'+cta+'</div>'+visual+'</section>'
 body+='<section class="wrap landing-benefits" aria-label="Zo helpt het jouw zaak">'+''.join('<article><h2>'+e(h)+'</h2><p>'+e(t)+'</p></article>' for h,t in sections)+'</section>'
 if sector:body+=sector_details(slug,label,sections)
 body+='<section class="wrap landing-faq"><h2>Veelgestelde vragen</h2>'+''.join('<details><summary>'+e(q)+'</summary><p>'+e(a)+'</p></details>' for q,a in faqs)+'</section>'
 related=[p for p in pages if p[0]!=slug and (not p[0].startswith('sector/') if sector else p[0].startswith('sector/'))][:4]
 body+='<section class="wrap landing-related"><h2>'+('Ook handig voor jouw zaak' if sector else 'Bekijk het voor jouw zaak')+'</h2><div>'+''.join(f'<a href="/{p[0]}/">{e(p[1])}</a>' for p in related)+'</div></section><section class="wrap solution-help"><h2>Ontdek wat bij jouw werkwijze past.</h2><p>Probeer de omgeving of bespreek eerst je vragen met ons.</p>'+cta+'</section>'
 save(slug,shell(slug,title,desc,body,animated))
body='<section class="wrap solution-intro"><h1>Slimme formulieren, afspraken en klantopvolging voor jouw sector.</h1><p>Kies dezelfde sector als bij je gratis proefperiode. Ontdek hoe je aanvragen verzamelt, gesprekken inplant en klanten opvolgt met de functies die bij jouw werk passen.</p></section><section class="wrap sector-catalogue" aria-labelledby="category-title"><h2 id="category-title">Alle sectoren</h2><div class="sector-directory">'
for c in categories:
 p=next(p for p in pages if p[0]=='sector/'+c['slug'])
 body+='<a href="/'+p[0]+'/"><h3>'+e(c['label'])+'</h3><p>'+e(p[3])+'</p><span>Bekijk de mogelijkheden</span></a>'
body+='</div></section><section class="wrap sector-catalogue" aria-labelledby="profession-title"><h2 id="profession-title">Specifiek voor jouw beroep</h2><div class="sector-directory">'+''.join('<a href="/'+p[0]+'/"><h3>'+e(p[1])+'</h3><p>'+e(p[3])+'</p><span>Bekijk de mogelijkheden</span></a>' for p in pages[4:] if p[0] not in category_by_slug)+'</div></section><section class="wrap solution-help"><h2>Bespreek jouw werkwijze.</h2><p>Twijfel je welke aanpak past? Vertel ons hoe je klanten vandaag contact opnemen en wat je eenvoudiger wilt maken.</p>'+cta+'</section>'
save('sector',shell('sector','Online afspraken en CRM per sector | Afspraakboeken.be','Bekijk alle 13 sectoren: van bouw en beauty tot sport, onderwijs en zakelijke diensten. Ontdek slimme formulieren, afspraakplanning en optioneel CRM.',body))
paths=['index.html','prijzen/index.html','alles-in-1/index.html','contact/index.html','algemene-voorwaarden/index.html','cookiebeleid/index.html']+[p[0]+'/index.html' for p in pages]+['sector/index.html']
for path in paths:
 p=R/path;s=p.read_text();s=re.sub(r'<header class="header">[\s\S]*?</header>',lambda _:header,s,count=1);s=re.sub(r'<footer\b[\s\S]*?</footer>',lambda _:footer,s,count=1)
 for old,new in links.items():s=s.replace('href="'+old+'"','href="'+new+'"')
 s=re.sub(r'site\.(css|js)\?v=[\d.]+',r'site.\1?v=0.20.1',s);p.write_text(s)
(R/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>https://afspraakboeken.be/'+p.removesuffix('index.html')+'</loc></url>\n' for p in paths)+'</urlset>\n')
(R/'deployment.json').write_text(json.dumps({'version':'0.20.1','site':'afspraakboeken.be','release':'all-registration-sectors-with-usecases-and-benefits'},indent=2)+'\n')

# Static-host fallback: an immediate refresh when Apache redirects are unavailable.
for old in ['voor','voor/dakwerkers','voor/beauty-wellness','voor/installateurs','voor/tuinaannemers']:
    target='https://afspraakboeken.be/'+old.replace('voor','sector',1)+'/'
    save(old,'<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0; url='+target+'"><link rel="canonical" href="'+target+'"><title>Pagina verhuisd · Afspraakboeken.be</title><script src="/privacy.js?v=0.20.0" data-gtm="GTM-KDF5GK88" defer></script></head><body><p>Deze pagina is verhuisd. <a href="'+target+'">Bekijk de sectorpagina</a>.</p></body></html>')
