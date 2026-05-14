# Suurel keelemudelil põhinev eestikeelse informaatika teksti tagasisidesüsteem

See repositoorium sisaldab Uku Renek Kronbergsi 2026. aasta Tartu Ülikooli informaatika bakalaureusetöö LaTeX-allikaid, veebiprototüüpi, hindamisskripte ja tulemuste andmestikku.

Töö eesmärk on kavandada ja realiseerida suurel keelemudelil põhinev prototüüp, mis annab eestikeelsele informaatika lõputöö tekstile automaatset tagasisidet neljas kategoorias: struktuur, akadeemiline stiil, terminoloogia järjepidevus ja viitamisvajadus. Lisaks hinnatakse, kui hästi selline süsteem töötab kvalitatiivses pilootuuringus ja 20 sünteetilise testkatkendi põhjal tehtud empiirilises hindamises.

## Töö info

| Väli | Väärtus |
| --- | --- |
| Pealkiri | Suurel keelemudelil põhineva eestikeelse informaatika teksti tagasisidesüsteemi prototüüp ja pilootuuring |
| Autor | Uku Renek Kronbergs |
| Juhendaja | Alo Peets, MSc |
| Õppekava | Informaatika |
| Töö liik | Bakalaureusetöö, 9 EAP |
| Aasta | 2026 |
| Märksõnad | suured keelemudelid, eesti keel, akadeemiline tekst, tagasiside, prototüüp, pilootuuring, promptimine |

## Mida repositoorium sisaldab

```text
.
├── thesis.tex                    # põhiline LaTeX-i sisenemispunkt
├── thesis_AI.tex                 # sama töö AI generated vesimärgiga esilehel
├── thesis_AI.pdf                 # kompileeritud vesimärgiga PDF
├── estonian/                     # töö eestikeelsed peatükid, joonised ja viited
├── unitartucs/                   # TÜ arvutiteaduse instituudi LaTeX-klass
├── prototuup/                    # FastAPI + React prototüüp
├── statistika/                   # andmestik, hindamisskriptid, CSV-d ja graafikud
├── RETSENSIOON.md                # retsensiooni/ülevaatuse märkmed
└── 2026_02_03_...pdf             # lõputööde koostamise ja hindamise juhend
```

Malli ingliskeelne osa on samuti repositooriumis alles, kuid käesolev töö kasutab eestikeelset põhifaili `estonian/põhi.tex`.

## Põhitulemused

Töös valmis lokaalselt käivitatav veebiprototüüp, kus kasutaja sisestab enda kirjutatud lõputöö peatüki, valib peatükitüübi, prompti tüübi ja mudeli ning saab kategoriseeritud tagasiside.

Empiirilises hindamises kasutati 20 sünteetilist testkatkendit ja 42 kuldstandardi annotatsiooni. Iga katkend analüüsiti kahe mudeli ja kahe promptiga, kokku 80 päris API-päringut. Parim kombinatsioon oli `GPT-5.5` koos struktureeritud promptiga:

| Mudel | Prompt | Macro F1 | Täpsus | Saagis |
| --- | --- | ---: | ---: | ---: |
| Claude 4.7 Opus | struktureeritud | 0,46 | 0,33 | 0,93 |
| Claude 4.7 Opus | üldine | 0,41 | 0,29 | 0,79 |
| GPT-5.5 | struktureeritud | 0,56 | 0,47 | 0,77 |
| GPT-5.5 | üldine | 0,38 | 0,27 | 0,85 |

Tulemused näitavad, et struktureeritud prompt parandas F1-skoori mõlemal mudelil. Mudelid kaldusid eelistama saagist täpsusele: nad leidsid suure osa kuldstandardi probleemidest, kuid pakkusid ka palju lisaleide, mida tuleb kasutajal kriitiliselt kontrollida. Süsteemi roll on seega tagasisidevahend, mitte juhendaja ega lõputöö autor.

Oluline piirang: testkogu ja kuldstandard on autori juhendamisel LLM-i abil koostatud sünteetilised tekstid. Hindamispäringud ise on päris API-päringud ning toorvastused on salvestatud kausta `statistika/andmed/paris_vastused/`.

## Lõputöö kompileerimine

LaTeX-i kompileerimiseks on vaja LuaLaTeX-i, `latexmk`-i, `biber`-it ja Pygmentsit, sest töö kasutab `fontspec`, `biblatex` ja `minted` pakette.

```bash
latexmk -lualatex -shell-escape thesis.tex
```

AI-vesimärgiga versiooni kompileerimiseks:

```bash
latexmk -lualatex -shell-escape thesis_AI.tex
```

Windowsis sobib TeX Live. Kui kasutad minimaalset paigaldust, peavad vähemalt olemas olema töö mallis kasutatud paketid, sh `fontspec`, `biblatex`, `biber`, `minted`, `babel-estonian`, `tabularray`, `graphicx` ja `draftwatermark`.

## Prototüübi käivitamine

Prototüüp asub kaustas `prototuup/`. Vaikimisi töötab see demo-režiimis ega vaja API-võtmeid.

```bash
cd prototuup
docker compose up --build
```

Seejärel ava brauseris `http://localhost:5173`.

Päris LLM-mudelite kasutamiseks lisa `prototuup/.env` faili `ANTHROPIC_API_KEY` ja/või `OPENAI_API_KEY`. Täpsem juhend on failis `prototuup/README.md`.

## Statistika ja hindamise kordamine

Statistika ja hindamisandmed asuvad kaustas `statistika/`.

```bash
cd statistika
python koguda.py
python joonised.py
```

Olemasolevate päris API-vastuste uuesti skoorimiseks:

```bash
python paris_hindamine.py --ainult-skoori
```

Täielik `python paris_hindamine.py` võib teha uusi Anthropic/OpenAI API-päringuid, kui vastusefailid puuduvad. Selleks on vaja API-võtmeid ning päringud võivad tekitada kulu. Kasutatud testjooksus oli 80 päringu kogukulu ligikaudu 3,88 USD.

Sünteetilise pipeline'i varasem demonstratsioon on alles skriptides `andmestik_synth.py` ja `synteetiline_hindamine.py`, kuid töö põhijäreldused tuginevad salvestatud päris API-vastustele.

## Testid

Backendi testid:

```bash
cd prototuup/backend
pytest
```

Need kontrollivad andmemudeleid, promptide laadimist, demo-pakkujat ja analüüsiloogikat ilma väliseid API-sid puudutamata.

## Privaatsus ja eetika

Demo-režiimis ei saadeta sisestatud teksti välistele teenustele. Claude'i või GPT mudeli valimisel liigub tekst vastava teenusepakkuja API-sse, mistõttu prototüüp näitab enne esimest päringut privaatsushoiatust.

Süsteem on mõeldud tudengi enda kirjutatud teksti tagasisidestamiseks. See ei kirjuta lõputööd tudengi eest, ei asenda juhendajat ega anna autoriteetset hinnet. Iga soovitus vajab kasutaja kriitilist kontrolli.

## Täpsemad juhendid

- `prototuup/README.md`: veebirakenduse arhitektuur, käivitamine, API ja privaatsus.
- `statistika/README.md`: CSV-d, graafikud, sünteetiline testkogu, päris API-päringute tulemused ja jätkukava.
- `estonian/sektsioonid/10-lisad.tex`: testkogu disain, struktureeritud prompti täistekst, lähtekoodi ja andmestiku kirjeldus ning prototüübi kasutusjuhend.
