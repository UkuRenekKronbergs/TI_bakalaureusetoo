# Retsensendi-stiilis hinnang

**Töö:** „Suurel keelemudelil põhineva eestikeelse informaatika teksti tagasisidesüsteemi prototüüp ja pilootuuring”
**Autor:** Uku Renek Kronbergs
**Juhendaja:** Alo Peets, MSc
**Õppekava ja maht:** Informaatika bakalaureusetöö (9 EAP), 2026
**Hindamisalus:** ATI lõputööde nõuded ja hindamiskriteeriumid (jaotised 5.1–5.2.2). Retsensent hindab kolme kriteeriumi: **Sisu**, **Raskusaste**, **Vorm**. Iga kriteerium 1–5 (kümnendkohad lubatud positiivsete skooride puhul). Lõpphinne = (kõikide kriteeriumide skooride summa, sh kaitsmiskomisjoni „Ettekanne”) × 5, mille tulemus on lõpphindes A–F.

> Hinnang on koostatud käesoleva töö lõppversiooni põhjal ja eeldab, et töö esitatakse kaitsmisele kavandatud kujul. Komisjoni „Ettekanne”-skoori käesolev dokument ei aseta, kuna see hinnatakse kaitsmisel.

---

## 1. Sisu (Sisu) — soovitatav skoor: **3,75–4,0**

**Mida kriteerium hindab:** teema aktuaalsus, allikate piisavus ja kriitiline süntees; meetodi põhjendatus ja täielikkus; loogiline ühtsus; põhjalik võrdlus varasemate tulemustega; tulemuste rakendatavus ja **uudsus**; tarkvara kvaliteet.

**Hinnatava töö profiil:**
- Teema on aktuaalne ja õigesti piiritletud: eestikeelne akadeemiline tagasisidestamine on dokumenteerimata lünk, mida töö selgelt sõnastab.
- Teoreetiline taust (peatükk 2) on adekvaatne — Transformer/RLHF/emergent abilities/halutsineerimine/few-shot/CoT/struktureeritud väljund on kõik kaetud, viidatud korrektsete primaarallikatega (Vaswani 2017, Brown 2020, Wei 2022, Ouyang 2022, Liu 2023, Schulhoff 2024 jne).
- Seotud tööd (Burstein, Liang, Kasneci) on käsitletud ning töö enda lünk põhjendatakse veenvalt.
- Operatsionaalsed kategooriamääratlused (tabel 1) ja prompti disaini põhjendused (peatükk 3.4) on professionaalsel tasemel.
- Tarkvara kvaliteet on hea: kihiline backend, Pydantic-skeemi valideerimine, prefill-tehnika, retry-loogika, demo-režiim reprodutseeritavuseks ilma API võtmeta.

**Sisu nõrkused, mis hoiavad skoori 5 alt:**
- **Kvantitatiivse empiirilise hindamise puudumine** on selle kriteeriumi juures kõige raskem koorem. Töö ei esita ühtegi täpsuse, saagise ega F\(_1\)-skoori, kuigi need on rubriigis sõnastatud kui „varasemate tulemustega põhjendatud võrdluse” aluseks olev minimaalne tõenduskeha. Töö ulatusepiirang on ausalt ja korduvalt põhjendatud, mis on metoodiliselt vastutustundlik samm, kuid jätab nõude *de facto* täitmata.
- Empiiriline panus on **kvalitatiivne pilootuuring autori enda annoteeringutega**, valim 3–5 katkendit peatüki tüübi kohta, ilma sõltumatu teise annoteerijata. Kõik kolm uurimisküsimust saavad kvalifitseeritult „esialgse, kvalitatiivse vastuse”.
- Töö enda formulatsiooni järgi on osa täheldatud erinevustest (struktureeritud vs üldine prompt) **prompti disaini kavandatud tautoloogia**, mitte sõltumatu empiiriline tähelepanek. See on aus tunnistus, kuid samas tõdemus, et empiirilist uudsust on tavakohasest vähem.
- Uudsus on **olemas, kuid mõõdukas**: struktureeritud prompti rakendamine eestikeelsele akadeemilisele tekstile on dokumenteeritud lünka adresseeriv samm, kuid metoodika (Schulhoff 2024 jt) on kirjandusest tuntud.

**Skoori sisuline argument:**
- **4,0** on kaitstav, kui hindaja paneb suurt rõhku metoodika, prompti disaini ja tarkvara kvaliteedile ning aktsepteerib ulatusepiirangu sisulise valikuna, mis on kooskõlas töö mahuga (9 EAP). Pilootuuringu tähelepanekud on kasulikud ja korrektselt sõnastatud.
- **3,5–3,75** on kaitstav, kui hindaja loeb F\(_1\)-skooride puudumist ja ühe annoteerija piiranguid „märkimisväärseteks puudusteks”, mis on rubriigi „3 — vaevu rahuldav” määratluses sõnaselgelt sisse kirjutatud.

---

## 2. Raskusaste (Raskusaste) — soovitatav skoor: **4,0–4,25**

**Mida kriteerium hindab:** bakalaureuse taseme nõuetele vastavus; uudsete (teaduslike) tulemuste, vaatenurkade, tarkvara või käsitluse komplekssus; tehtud töö **kogumaht**.

**Hinnatava töö profiil:**
- Töö mahuline põhi on suur: täielik veebiprototüüp (Python 3.12 + FastAPI backend, React 18 + TypeScript + Tailwind frontend, Docker Compose, Anthropic + OpenAI + demo-pakkujakihid), prompti disain kahes versioonis, kavandatud hindamismetoodika, pilootuuring.
- Tehniline keerukus on hea bakalaureuse taseme jaoks: kihiline arhitektuur, JSON-skeemi valideerimine, prefill, retry, eraldi pakkujakiht — kõik üle baastasemest skripti.
- Töö hõlmab kahte distsipliini (NLP/promptimine ja täisstäki veebiarendus), mis lisab raskusastet.
- Disain\-teaduslik raamistik (Hevner 2004) on kasutatud teadlikult, ning artefakt-hindamine on metoodiliselt põhjendatud.

**Raskuse nõrkused, mis hoiavad skoori 5 alt:**
- Prototüüp ise on **kontseptuaalselt suhteliselt õhuke ümbris LLM-i API ümber**. Suurem osa „intelligentsist” on välise API käes; oma uudse algoritmi disaini ei ole.
- Kavandatud, kuid teostamata hindamine alandab töö tegelikku **läbiviidud** kompleksust — täismahuline annoteerimine, inter-annoteerija kokkulepe ja F\(_1\) arvutamine oleksid olnud raskusastme tipus.
- Mahuliselt on töö pigem keskmine bakalaureusetöö, mitte erandlikult ulatuslik.

**Skoori sisuline argument:**
- **4,0** on hästi kaitstav: bakalaureuse nõuetele selgelt vastav, märkimisväärselt mahuline ja arhitektuurselt põhjendatud töö, ilma erandlikust mahust.
- **4,25** on kaitstav, kui hindaja paneb erilist rõhku tarkvara kvaliteedile, demo-režiimi kavandamise terviklikkusele ja prototüübi reprodutseeritavusele.

---

## 3. Vorm (Vorm) — soovitatav skoor: **4,25–4,5**

**Mida kriteerium hindab:** korrektne akadeemiline keel; selge esitus; tehniline teostus (loogiline struktuur, jooniste, tabelite, illustratsioonide kvaliteet); viitamise korrektsus (stiili järjepidevus, iga allikas viidatud ja viite kanne olemas); **tekstiline ühtsus**.

**Hinnatava töö profiil:**
- Struktuur on loogiline ja iga peatüki sees on sissejuhatav navigeerimislõik — töö järgib oma süsteemis nõutavat tava ja teeb seda hästi.
- Tagasisidekategooriad on määratletud tabeliga (tabel 1), prompti võrdlus on esitatud koodilõikudes, mõõdikud valemitega (eq. 1–3); kõik visuaalsed elemendid on viidatud ja sildistatud.
- Eestikeelne tehniline terminoloogia on järjepidev (vt hiljutised kommitid „poleerisin sõnastust”, „joondasin kokkuvõtte uurimisküsimustega”); ingliskeelsed terminid esitatakse korrektselt kursiivis sulgudes.
- Abstract (eesti ja inglise) on detailne ning vastab töö tegelikule sisule, sealhulgas selgesõnaliselt sõnastatud ulatusepiirangule.
- Lisad on hästi korraldatud: testkogu disain, struktureeritud prompti täistekst, lähtekoodi struktuur, kasutusjuhend koos demo-režiimi käivitamisega.
- „Designed”/„implemented”/„future work” eristus on töös läbivalt järjepidev — väga hea diskursiivne distsipliin.

**Vormi nõrkused, mis hoiavad skoori 5 alt:**
- **Pealkirja erinevus tiitellehe ja litsentsi vahel.** Põhipealkiri (põhi.tex): „Suurel keelemudelil põhineva eestikeelse informaatika teksti tagasisidesüsteemi prototüüp ja pilootuuring”. Litsentsileht (11-litsents.tex:12): „Suurte keelemudelite kasutamine eestikeelse tehnilise informaatika teksti kvaliteedikontrolliks”. See on **konkreetne vormiline viga**, mis nõuab parandamist enne kaitsmist.
- Korduvad „ulatusest välja jäetud” / „kavandatud jätkukavasse” lauseesinemised mitmes peatükis on metoodiliselt põhjendatud, kuid lugemiskogemuses pisut väsitavad — pinges B+/A− tasemel oleks need kondenseeritud ühe selge kasti või tabeli abil ühte kohta.
- Mõned alapeatükid (eriti 2.3 alajaotused) ei alga sissejuhatava lõiguga — sama veaga, mille tuvastamise vastu tagasiside-prototüüp on suunatud. See on iseenesest harmless, kuid peegellaadne.

**Skoori sisuline argument:**
- **4,5** on kaitstav, kui pealkirja-erinevus parandatakse enne esitamist. Vormi disain, struktuur ja terminoloogiline järjepidevus on töö selge tugevus.
- **4,25** on sobiv, kui pealkirja-erinevus jääb sisse — see on konkreetne, lokaliseeritav vorminõude rikkumine, mis ATI rubriigi „viitamise/vormistamise korrektsus” all on oluline.

---

## Kokkuvõttev hinne — A–F skaala

Iga rida näitab võimaliku Komisjoni „Ettekanne”-skoori juures (oletatav 4,0) tekkivat lõpphinnet:

| Stsenaarium | Sisu | Raskus | Vorm | Ettekanne | Summa | ×5 | Lõpphinne |
|---|---|---|---|---|---|---|---|
| Konservatiivne | 3,5 | 4,0 | 4,25 | 4,0 | 15,75 | 78,75 | **C (hea)** |
| Tõenäoline (pealkiri parandatud) | 4,0 | 4,0 | 4,5 | 4,0 | 16,5 | 82,5 | **B (väga hea)** |
| Heatahtlik | 4,0 | 4,25 | 4,5 | 4,5 | 17,25 | 86,25 | **B (väga hea), B/A piir lähedal** |

**Retsensendi soovitatav lõpphinne enne kaitsmisettekannet: B (väga hea), 81–87 punkti.**

A-d ei toeta empiirilise hindamise teadlik väljajätmine, sest ATI rubriigi „Sisu” määratluses on „põhjalik ja põhjendatud võrdlus varasemate tulemustega” üks võtmesõnastusi ning käesolev töö annab võrdluse pigem kvalitatiivse pilootuuringuna kui kvantitatiivse arvulise võrdlusena. D ja allapoole ei ole toetatud, kuna ühelgi kriteeriumil ei ole „märkimisväärseid puudusi” rubriigi 3-määratluse mõttes — kõikidel on selgelt positiivne sisu ja ükski ei kuku miinimumnõuete alla.

---

## Tasemepõhine kaardistus (A–E)

Iga kriteeriumi puhul on näidatud, kus hinnatav töö paikneb iga lõpphinde tasemel.

### Sisu
| Tase | Mida nõuab | Käesolev töö selles tasemes |
|---|---|---|
| **A** | Praktiliselt veatu, vähemalt mõnes aspektis silmapaistev. Põhjalik kvantitatiivne võrdlus varasemate tulemustega. Selge uudsus. | **Ei küüni** — kvantitatiivset võrdlust ei esitata; uudsus on mõõdukas (rakenduslik). |
| **B** | Hea taseme töö ilma märkimisväärsete puudusteta. Solidne metoodika, korrektne süntees, kvalitatiivselt põhjendatud järeldused. | **Sobib siia**, kui aktsepteeritakse ulatusepiirang sisulise disainivalikuna. Metoodika ja teoreetiline raamistik on B-taseme tugevused; pilootuuring annab kvalitatiivselt usaldusväärseid esialgseid vastuseid. |
| **C** | Vastab nõuetele, kuid on märgatavaid nõrkusi ühel alal — nt pinnapealne süntees, nõrk varasemate tulemuste võrdlus, tagasihoidlik maht. | **Sobib siia**, kui hindaja peab F\(_1\)-skooride puudumist „märkimisväärseks puuduseks”. Töö siiski ei oleks sügavamal kui ülemine C, kuna teoreetiline ja prototüübipoolne sisu on tugev. |
| **D** | Vaevu rahuldav, mitu märkimisväärset puudust: nõrk taustakirjandus, ebapiisavalt põhjendatud meetodid, anekdootlik hindamine. | **Ei küüni allapoole** — taustakirjandus on detailne, meetodid hästi põhjendatud, pilootuuring on sõnastatud teadlikult, mitte anekdootlikult. |
| **E** | Napilt läbisaamine; nõrkused mitmel rindel; metoodika napilt põhjendatud. | Ei käi. |

### Raskusaste
| Tase | Mida nõuab | Käesolev töö selles tasemes |
|---|---|---|
| **A** | Erakordselt kompleksne või mahukas; uudsed teaduslikud tulemused. | **Ei küüni** — prototüüp on rakenduslik ümbris LLM API ümber; uudset algoritmi disaini ei ole. |
| **B** | Bakalaureusetaseme nõuetele kindlalt vastav, hea kompleksusega, märkimisväärse mahuga. | **Sobib siia** — täisstäki veebirakendus, kihiline arhitektuur, kaks LLM-pakkujat + demo-pakkuja, struktureeritud prompti disain, kavandatud hindamismetoodika. |
| **C** | Bakalaureusetaseme miinimumnõuetele vastav, kuid pigem standardne maht ja keerukus. | **Allpool käesolevat tööd** — käesolev maht ja arhitektuur on üle standardse bakalaureusetöö. |
| **D** | Bakalaureusetaseme alaservas; tehniline kompleksus minimaalne. | Ei käi. |
| **E** | Vaevu bakalaureusetaseme nõuetele vastav. | Ei käi. |

### Vorm
| Tase | Mida nõuab | Käesolev töö selles tasemes |
|---|---|---|
| **A** | Praktiliselt veatu vorm, kõik viited korrektsed, terviktekst sujuv; väljapaistev tehniline teostus (joonised, tabelid). | **Lähedal, ei küüni** — pealkirja-erinevus tiitellehe ja litsentsi vahel on konkreetne viga; kui see parandatakse, on töö A-tasemele lähemal. Mõnedel alapeatükkidel puuduvad sissejuhatavad lõigud (mille puudust töö ise prototüübis tuvastab). |
| **B** | Hea akadeemiline keel, järjepidevus, korrektsed viited, selge struktuur. | **Sobib siia** — keel ja terminoloogia järjepidevus on hästi hoolitsetud; struktuur on selge ja navigeeritav; viited on järjepidevad. |
| **C** | Vastab nõuetele, kuid esineb märgatavaid vormistusprobleeme. | Allpool käesolevat tööd. |
| **D**–**E** | — | Ei käi. |

---

## Retsensendi konkreetsed märkused autorile (parandamiseks enne kaitsmist)

1. **Pealkirja ühtlustamine (kõrge prioriteet, vormiline viga).** [estonian/sektsioonid/11-litsents.tex:12](estonian/sektsioonid/11-litsents.tex) sisaldab erinevat pealkirja võrreldes [estonian/põhi.tex:5](estonian/põhi.tex)-ga. Litsentsi tekst peab kasutama sama pealkirja, mis tiitellehel. See on lihtne, kuid kohustuslik parandus.

2. **„Out-of-scope” põhjenduse kondenseerimine (keskmine prioriteet).** Ulatusepiirangu sõnastus kordub vähemalt 6 kohas. Selgele lugejasõbralikule esitusele aitaks kaasa üks selgelt eristuv (näiteks kasti või eraldi alapeatükina) „Töö ulatuse piiritlemine: mis sees, mis välja jäetud, miks” — millele teised peatükid lihtsalt viitavad. See vähendab tunnet, et autor enesekaitseliselt taastab piirangut, ja annab lugejale ühe autoritatiivse koha kontrollida.

3. **Sissejuhatavate lõikude lisamine alapeatükkide algusse (madal prioriteet, vormiline järjepidevus).** Mitu alajaotust 2.3 all (2.3.1–2.3.4) algavad pealkirja järel kohe põhitekstiga. See on samasugune muster, mille prototüüp on disainitud kasutajale tagasisidena tuvastama. Retsensent on enesepeegelduses sümpaatne, kuid vormiline järjepidevus selles küsimuses tõstaks „Vorm” skoori.

4. **Pilootuuringu tugevuse tagasihoidlikum sõnastus arutelus (madal prioriteet).** Lõik 5.4 võib tugevamalt rõhutada, et üldise ja struktureeritud prompti sisuline võrdlus on sõltuv post-hoc käsitsi kategoriseerimisest — see on töös juba mainitud, kuid arutelus tasub seda korrata, et lugejale on selge, kui suur osa täheldatud erinevustest on disaini-tautoloogia ja kui suur osa potentsiaalne empiiriline efekt.

5. **Mõõdikute valemite näidisarvutus (madal prioriteet).** Valemid eq. 1–3 on standardsed, kuid lugejale aitaks üks lühike näidisarvutus (näiteks: kui kategoorias on TP=5, FP=2, FN=3, siis Täpsus = 0,71, Saagis = 0,625, F\(_1\) = 0,67). See teeks töö kavandatud hindamismetoodika rakendatavuse veelgi konkreetsemaks ja võiks aidata Sisu-skoori.

6. **Jätkukava ajaraami täpsustamine (valikuline).** Kokkuvõte loetleb 7 jätkukava sammu. Mõnele neist (eriti samm 1–2: testkogu koostamine ja kuldstandardi annoteerimine) realistliku ajaraami pakkumine (näiteks „kestab 4–6 nädalat üliõpilase tüüpilise koormuse juures”) muudab kava usaldusväärsemaks ja vastab kaitsmiskomisjoni tüüpilisele küsimusele „kas see on tegelikult teostatav?”.

---

## Retsensendi lõppjäreldus

Käesolev töö on **tugev B-taseme („väga hea”) bakalaureusetöö**, mis on metoodiliselt korrektne, tehniliselt hästi teostatud ja vormiliselt korralik. Selle peamine puudus — kvantitatiivse empiirilise hindamise teadlik väljajätt — on autori poolt ausalt ja korduvalt sõnastatud ning kavandatud jätkukavasse. Ulatusepiirang on metoodiline distsipliin, mitte varjamine; see on hindaja jaoks oluline eristus.

A-taset ei toeta selle töö raamides eelkõige see, et ATI rubriik nõuab Sisu-kriteeriumi tipus „põhjalikku ja põhjendatud võrdlust varasemate tulemustega”, mida käesolev töö annab kvalitatiivselt, mitte kvantitatiivselt. C-taseme alla ei pea töö samuti laskuma, kuna ükski kriteerium ei sisalda märkimisväärseid puudusi rubriigi 3-määratluse mõttes ja kõik kolm kriteeriumi on selgelt positiivsed.

**Soovitatav lõpphinne kaitsmisettekande eel: B (väga hea), 82–85 punkti.** Kui jätkukava (täismahuline hindamine F\(_1\)-skooridega ja inter-annoteerija kokkuleppega) viiakse läbi magistriõppes või avaldatavas artiklis, on käesolev töö selle jaoks tugev alusplatvorm.
