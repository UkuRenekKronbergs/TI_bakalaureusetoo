# Statistika, graafikud ja sünteetiline hindamis-demonstratsioon

Käesolev kaust koondab bakalaureusetöö ja prototüübi kohta käivad arvulised
näitajad ühte taasreprodutseeritavasse paketti. Pakett jaguneb kahte ossa:

1. **Faktilised näitajad** (LaTeX-failidest, prototüübi koodist, demo-režiimi
   salvestatud vastustest) — vt skript `koguda.py` ja `joonised.py`.
2. **Sünteetiline hindamis-demonstratsioon** — vt skript `andmestik_synth.py`
   ja `synteetiline_hindamine.py`. **HOIATUS:** sünteetilise osa andmed on
   generatiivse tehisaru (Claude 4.7 Opus) abil koostatud illustratsiooni
   eesmärgil ja **ei mõõda** päris LLM-ide sooritust. Vt thesis
   ptk 5.8 selgesõnaline jalus.

## Käivitamine

```bash
# Faktilised näitajad (LaTeX, kood, demo-vastused)
python koguda.py     # kirjutab CSV-d kausta andmed/
python joonised.py   # joonistab 8 PNG-d kausta joonised_png/

# Sünteetiline hindamis-demonstratsioon
python andmestik_synth.py        # valideerib testkogu (20 katkendit, 42 annot.)
python synteetiline_hindamine.py # simuleerib mudelid, arvutab F1, joonised 09–12
```

Eeldused: Python 3.11+, paketid `pandas`, `matplotlib`, `numpy`. Lisapakette
ei vaja — kõik on standardteegis või juba prototüübi sõltuvustest paigaldatud.
Sünteetiline simulatsioon kasutab fikseeritud seeme'd (`SEEME = 20260512`),
mistõttu skripti uuesti käivitamine annab täpselt samad numbrid.

## Mis kus on

### `koguda.py`
Loeb neli allikat ja kirjutab CSV-d:

| Allikas | Väljundfailid |
|---|---|
| Prototüübi demo-vastused (`prototuup/backend/demo_andmed.py`) | `demo_leiud.csv`, `demo_kategooriad_peatykiti.csv`, `demo_kindlus.csv` |
| Lõputöö LaTeX-failid (ainult `põhi.tex` poolt `\input`-itud) | `teksti_statistika.csv`, `viidete_kokkuvote.csv` |
| Prototüübi koodifailid (välja arvatud `node_modules/`, `dist/`, `__pycache__/`, `package-lock.json`) | `koodi_statistika.csv`, `koodi_kokkuvote.csv` |
| Lisa I tabeli kvoot (käsitsi) | `kavandatud_testkogu.csv` |

### `joonised.py`
Loeb faktilised CSV-d ja toodab 8 PNG-faili (`joonised_png/`):

| Fail | Sisu |
|---|---|
| `01_demo_kategooriad_kokku.png` | Demo-leidude koguarv 4 kategoorias |
| `02_demo_peatykiti_stack.png` | Demo-leiud (peatüki tüüp × kategooria) virnastatult |
| `03_kindlus_jaotus.png` | Kindlushinnangu jaotus kategooriate kaupa |
| `04_sonu_peatykis.png` | Sõnade arv töö igas peatükis |
| `05_viiteid_peatykis.png` | `\cite`-kasutuste arv peatükkide kaupa |
| `06_kood_keeleti.png` | Prototüübi koodi LOC keelte kaupa |
| `07_testkogu_kvoot.png` | Lisa I kavandatud testkogu jaotus |
| `08_teksti_struktuur.png` | Alapeatükid, joonised, tabelid jne peatükkide kaupa (2×2) |

### `andmestik_synth.py` ja `synteetiline_hindamine.py`
**SÜNTEETILISED ANDMED — illustratsiooni eesmärgil.**

`andmestik_synth.py` sisaldab Pythoni konstandina 20 LLM-iga genereeritud
testkatkendit ning 42 LLM-iga koostatud kuldstandardi annotatsiooni
(kategooria, span, lühike kirjeldus, kindlushinnang). Modul on importitav
ja sisaldab funktsiooni `kontrolli_andmete_terviklikkus()`, mis tagab,
et iga annotatsiooni span esineb katkendi tekstis.

`synteetiline_hindamine.py` simuleerib iga (mudel × prompti tüüp × katkend)
kombinatsiooni jaoks mudeli väljundid sõltumatute Bernoulli-tõmmistega
seeditud juhugeneraatorist (`SEEME = 20260512`). Profiilid (`RECALL` ja
`FP_TOENAOSUS` muutujad faili alguses) kajastavad thesis ptk 5
pilootuuringus täheldatud kvalitatiivseid mustreid, **kuid numbrid ise on
autori postulaat, mitte mõõdetud väärtused**. Skript kirjutab:

| Väljundfail | Sisu |
|---|---|
| `andmed/synth_mudelivastused.csv` | iga „mudeli leid" (TP / FP / FN) eraldi reana |
| `andmed/synth_kategooriapohised_moodikud.csv` | TP, FP, FN, T, S, F\textsubscript{1} (kategooria × mudel × prompti tüüp) |
| `andmed/synth_kokkuvote.csv` | macro-keskmised iga (mudel × prompti tüüp) kombinatsiooni kohta |
| `joonised_png/09_synth_F1_kategooriapohi.png` | F\textsubscript{1} kategooria kaupa (4×4 võrdlus) |
| `joonised_png/10_synth_macro_F1.png` | Macro-F\textsubscript{1} prompti tüübi kaupa |
| `joonised_png/11_synth_TP_FP_FN.png` | TP/FP/FN jaotus kombinatsioonide kaupa |
| `joonised_png/12_synth_tapsus_saagis.png` | Täpsus–saagis-graafik koos F\textsubscript{1} isokõveratega |

Iga sünteetilise graafiku peal on selge vesimärk „SÜNTEETILINE
illustratsioon". Thesis ptk 5.8 vastavad joonised ja tabel kannavad sama
hoiatust.

## Põhinäitajad ühe pilguga

Pärast `koguda.py` käivitamist annab `andmed/` kaust järgmist üldpilti
(viimase käivituse seisuga):

- **Töö maht**: ~7575 sõna 9 peatükis (kõige mahukam: 5-hindamine, ~1910 sõna)
- **Viited**: 32 bibliograafiakirjet, 40 `\cite`-kasutust tekstis
- **Struktuur**: 24 `\subsection` + 14 `\subsubsection`; 3 joonist, 5 tabelit, 3 valemit, 3 koodinäidet
- **Prototüüp**: ~1700 rida käsitsi kirjutatud koodi (Python 926, TSX 512, TS 140, ülejäänud konfiguratsioon)
- **Demo-leiud**: 22 leidu üle 5 peatüki tüübi; AKADEEMILINE\_STIIL kõige sagedasem (10), STRUKTUUR kõige harvem (3)
- **Kavandatud testkogu**: 20 katkendit (kõige rohkem taust: 5; kõige vähem kokkuvõte: 3)

## Andmete tõlgendamise märkused

- **Demo-režiimi leiud** on käsitsi koostatud näidisleiud, mitte tegeliku
  LLM-i tagasiside. Need illustreerivad süsteemi väljundi *kuju*, mitte
  mudeli täpsust või saagist. Tegelike mõõdikute (täpsus, saagis, F\textsubscript{1})
  arvutamine kuulub töö jätkukavasse (vt thesis ptk 5.7).
- **Sõnade arv** on hinnanguline: LaTeX-i käsud, kommentaarid ja
  `minted`-keskkonnad on enne lugemist eemaldatud, kuid mõni piiripealne
  juhtum (nt eestikeelsed sõnad ASCII-kirjavahemärkidega) võib anda paari
  ühiku erinevuse võrreldes Wordi-laadse loendiga.
- **Koodi LOC** loendab mittetühjasid ridu ja jätab välja kommentaaride
  read keele kohta sobivate ühe-rea markeritega (`#`, `//`); kompaktsem
  Pythoni stiil annab seetõttu mõnevõrra madalama numbri kui sama
  funktsionaalsuse TypeScripti realisatsioon. Auto-genereeritud
  `package-lock.json` on välja jäetud.
- **Tekstistatistika filter**: `põhi.tex` poolt `\input`-imata mallifailid
  (nt `2-vormistamine.tex`, `3-tekstiloome.tex`) on välja jäetud.

## Päris empiirilised tulemused (80 päris API-päringut)

Skript `paris_hindamine.py` käivitas tegelikud API-päringud Anthropic Claude 4.7 Opus ja OpenAI GPT-5.5 mudelitele 20 sünteetilise testkatkendi vastu, mõlema prompti versiooniga (üldine + struktureeritud) — kokku 80 päringut. Tegelikud salvestatud vastused on kaustas `andmed/paris_vastused/`.

**Tegelik tokenikulu ja rahaline kogukulu** (Anthropici ja OpenAI arvelduste paneelide andmed; mõlemad pakkujad arveldavad USD-s):

| Mudel | Päringuid | Sisend-tokeneid | Väljund-tokeneid | Maksumus (USD) |
|---|---:|---:|---:|---:|
| Claude 4.7 Opus | 40 | 57 967 | 77 228 | $2,22 |
| GPT-5.5         | 40 | 34 177 | 49 663 | $1,66 |
| **Kokku**       | **80** | **92 144** | **126 891** | **$3,88** |

Kogu kestus: ~37 minutit (keskmine ~28 sekundit päringu kohta). Kogukulu jäi $10 USD eelarves alla 40 % (ligikaudu €3,6 kursi 1 USD ≈ 0,93 EUR juures, mai 2026); piirav tegur on inimese kuldstandardi annoteerimise aeg, mitte arvutuslik mahukus.

| Mudel | Prompti tüüp | Macro T | Macro S | Macro F₁ | TP | FP | FN |
|---|---|---|---|---|---|---|---|
| Claude 4.7 Opus | struktureeritud | 0,33 | 0,93 | 0,46 | 39 |  79 |  3 |
| Claude 4.7 Opus | üldine          | 0,29 | 0,79 | 0,41 | 34 | 100 |  8 |
| **GPT-5.5** | **struktureeritud** | **0,47** | **0,77** | **0,56** | **34** | **39** | **8** |
| GPT-5.5 | üldine          | 0,27 | 0,85 | 0,38 | 33 | 102 |  9 |

**Päris empiirilises hindamises on parim kombinatsioon GPT-5.5 + struktureeritud prompt (F₁ = 0,56),** mitte Claude (vastupidi varasema sünteetilise demonstratsiooni postuleeritud profiilile). Mudelid on kallutatud saagise poole — kõrge saagis (0,77--0,93), madalam täpsus (0,27--0,47). See tähendab, et mudelid leiavad peaaegu kõik kuldstandardi probleemid, kuid signaleerivad ka palju kandidaate, mida autori-poolne kuldstandard probleemiks ei pidanud.

## Sünteetiline pipeline-demonstratsioon (varasem iteratsioon)

Skript `synteetiline_hindamine.py` jätkab eksisteerimist eelmise iteratsiooni demonstratsioonina, kus mudelivastused simuleeriti seeditud Bernoulli-tõmmistega (mitte tegelikud API-päringud). Vt vastavad CSV-d kausta `andmed/synth_*.csv` ja graafikud `joonised_png/09_synth*..12_synth*.png`. **Sünteetilised numbrid ei mõõda päris LLM-ide sooritust.** Erinevus päris vs sünteetiliste tulemuste vahel ongi õpetlik: päris mõõtmine andis hoopis erinevad mustrid (GPT-5.5 > Claude struktureeritud prompti puhul; mudelid saagisele kallutatud).

## Edasised analüüsisuunad (jätkukava)

Päris üliõpilastöödel sama metoodika kohaldamine kuulub jätkukavasse:

1. Päris katkendite kogumine TÜ arvutiteaduse instituudi avalikest töödest (2020--2024) — asendab praeguse sünteetilise testkogu (`andmestik_synth.py`).
2. Sõltumatu teise annoteerija lisamine — inter-annoteerija kokkuleppe (Coheni $\kappa$) arvutamine kategooriate kaupa.
3. Kindlushinnangu kalibratsioon — kõrge kindlusega leidude osakaal tegelikult tõestest leidudest (andmed olemas failis `andmed/paris_klassifikatsioonid.csv`).
4. Span-tasemel kattuvuse 50% läve tundlikkusanalüüs (kontrollimine 30% ja 70% läviga).
5. Suurem testkogu (100+ katkendit) statistilise usaldusvahemiku jaoks.
