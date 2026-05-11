# Eestikeelse lõputöö tagasisidesüsteem – prototüüp

Bakalaureusetöö „Suurte keelemudelite kasutamine eestikeelse tehnilise informaatika teksti kvaliteedikontrolliks” praktiline tulemus. Süsteem võtab sisendiks tudengi enda kirjutatud lõputöö peatüki, suunab selle valitud LLM-ile struktureeritud viibaga ning kuvab kategoriseeritud tagasiside neljas kategoorias: struktuur, akadeemiline stiil, terminoloogia, viitamisvajadus.

> **Oluline**: see süsteem ei kirjuta lõputööd tudengi eest ega asenda juhendajat. See annab tudengi enda kirjutatud tekstile soovituslikku tagasisidet.

## Demo-režiim (vaikimisi, API võtit ei vaja)

Süsteem käivitub vaikimisi **demo-režiimis**: backend tagastab iga peatüki tüübi jaoks käsitsi koostatud (varem LLM-iga genereeritud) salvestatud näidisvastuse, ilma et midagi internetti läheks. Nii saab süsteemi proovida ka ilma Anthropic või OpenAI võtita.

- Demo-režiimis EI sõltu vastus tegelikult sisestatud tekstist — kuvatakse alati valitud peatüki tüübi salvestatud leiud.
- Frontendi all on nupp **„Lae näidistekst”**, mis paigutab tekstikasti tahtlikult vigase näidisteksti, millele salvestatud leiud vastavad.
- Päris LLM-päringuid tehakse ainult juhul, kui kasutaja valib mudeliks **Claude 4.7 Opus** või **GPT-5.5** ja vastav API võti on seadistatud.

## Arhitektuur

```
+------------+        HTTP        +-----------+        HTTPS        +-----------+
|  Frontend  | <----------------> |  Backend  | <-----------------> |  LLM API  |
| React + TS |    /api/analyse    | FastAPI   |   Anthropic/OpenAI  | (valikuline)
+------------+                    +-----------+                     +-----------+
                                        |
                                        v
                                 +------------+
                                 | Demo-pakkuja|  ← vaikimisi, võrku ei vaja
                                 +------------+
```

- **Backend** ([backend/](backend/)): Python 3.12 + FastAPI + Pydantic. Hoiab promptide malle, demo-näidisvastuseid, kombineerib promptid sisendiga ja (LLM-mudelite korral) kutsub vastavat API-d.
- **Frontend** ([frontend/](frontend/)): React 18 + TypeScript + Tailwind CSS. Kasutajaliides koos privaatsusdialoogi, peatüki tüübi valija, prompti tüübi valija, mudeli valija, näidisteksti laadimise ja kategoriseeritud tagasisidepaneeliga.

## Käivitamine Dockeriga (soovitatav)

Eeldused: Docker Desktop 4 või uuem (Docker Compose v2 sisemiselt).

1. (Valikuline) Kui soovid kasutada päris LLM-mudelit, kopeeri keskkonnamuutujate näidisfail ja lisa oma API võti:
   ```bash
   cp .env.example .env
   # Ava .env oma redaktoris ja täida ANTHROPIC_API_KEY ja/või OPENAI_API_KEY rida.
   ```
   Demo-režiimi kasutamiseks pole seda vaja teha.
2. Käivita kogu süsteem ühe käsuga:
   ```bash
   docker compose up --build
   ```
3. Ava brauseris [http://localhost:5173](http://localhost:5173).

Pärast töö lõpetamist sulge `Ctrl+C` ja pane konteinerid maha käsuga `docker compose down`.

## Käivitamine ilma Dockerita

### Backend

Eeldused: Python 3.12, `pip`.

```bash
cd backend
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt

# Demo-režiimi kasutamiseks pole API võtit vaja:
uvicorn main:app --reload --port 8000

# Soovi korral päris LLM-mudeli kasutamiseks:
# PowerShell:  $env:ANTHROPIC_API_KEY="sk-ant-..."
# bash/zsh:    export ANTHROPIC_API_KEY=sk-ant-...
```

Backend on nüüd kättesaadav aadressil [http://localhost:8000](http://localhost:8000), automaatne API-dokumentatsioon [http://localhost:8000/docs](http://localhost:8000/docs).

### Frontend

Eeldused: Node.js 22 või uuem.

```bash
cd frontend
npm install
npm run dev
```

Frontend käivitub aadressil [http://localhost:5173](http://localhost:5173) ja proksib `/api/*` päringud backendi pihta (vt [frontend/vite.config.ts](frontend/vite.config.ts)).

## Konfiguratsioon

Demo-režiim ei vaja ühtki keskkonnamuutujat. Allolevad on vajalikud ainult päris LLM-mudelitega kasutamiseks. Vt [.env.example](.env.example):

| Muutuja                | Vajalik?            | Selgitus                                          |
| ---------------------- | ------------------- | ------------------------------------------------- |
| (puudub)               | demo-režiimi jaoks  | Demo-režiim töötab ilma ühegi muutujata.          |
| `ANTHROPIC_API_KEY`    | ainult Claude jaoks | Anthropic Messages API ligipääsuvõti.             |
| `OPENAI_API_KEY`       | ainult GPT jaoks    | OpenAI Chat Completions API võti.                 |
| `LOG_LEVEL`            | ei                  | DEBUG \| INFO \| WARNING \| ERROR. Vaikimisi INFO. |
| `CORS_ALLOWED_ORIGINS` | ei                  | Komaeraldatud frontendi päritolud.                |

## API

`POST /api/analyse`

Päringukeha:
```json
{
  "tekst": "Sisestatud peatüki tekst.",
  "peatuki_tyyp": "sissejuhatus",
  "prompti_tyyp": "struktureeritud",
  "mudel": "demo"
}
```

Mudeli väärtused:
- `demo` — vaikimisi, salvestatud näidisvastus, võrku ei kasuta;
- `claude-opus-4-7` — Anthropic Claude (vajab `ANTHROPIC_API_KEY`);
- `gpt-5.5` — OpenAI GPT (vajab `OPENAI_API_KEY`).

Vastusekeha:
```json
{
  "leiud": [
    {
      "kategooria": "VIITAMISVAJADUS",
      "tsitaat": "Üle 75% arendajatest...",
      "probleem": "Konkreetne arvuline väide ilma viiteta.",
      "põhjendus": "...",
      "soovitus": "Lisa viide originaaluuringule.",
      "kindlus": "kõrge"
    }
  ],
  "meta": {
    "mudel": "demo",
    "prompti_tyyp": "struktureeritud",
    "peatuki_tyyp": "sissejuhatus",
    "leidude_arv_kategooriate_kaupa": {"VIITAMISVAJADUS": 1},
    "paaringu_kestus_ms": 12
  }
}
```

## Promptide muutmine

Promptid asuvad eraldi failides ja neid saab muuta ilma koodi puutumata:

- [backend/prompts/yldine.txt](backend/prompts/yldine.txt)
- [backend/prompts/struktureeritud.txt](backend/prompts/struktureeritud.txt)

Mõlemas failis on muutujad `${peatuki_tyyp}` ja `${tekst}`, mis asendatakse päringu käigus.

## Demo-vastuste muutmine

Demo-režiimi näidistekstid ja salvestatud leiud asuvad failis [backend/demo_andmed.py](backend/demo_andmed.py). Frontendi „Lae näidistekst” nupp loeb sama teksti failist [frontend/src/data/naidisTekstid.ts](frontend/src/data/naidisTekstid.ts) — kui muudad ühte, hoia teine kooskõlas.

## Testid

```bash
cd backend
pytest
```

Testid asuvad kaustas [backend/tests/](backend/tests/) ja katavad valideerimisloogika, prompti malli laadimise ja demo-pakkuja käitumise — ilma välimist API-d puudutamata.

## Privaatsus ja eetika

- **Demo-režiimis** (vaikimisi) ei lahku sisestatud tekst sinu masinast — backend tagastab salvestatud näidisvastuse.
- **Claude / GPT mudelite valikul** saadetakse tekst Anthropici või OpenAI serveritesse. Frontend näitab enne esimest sellist päringut hoiatusdialoogi, mille kasutaja peab kinnitama.
- Backend ei salvesta sisestatud teksti kettal; logitakse vaid anonüümseid sündmuseid (mudel, prompti tüüp, leidude arv kategooriate kaupa, kestus).
- Süsteemi prompt sisaldab selget piirangut, et mudel ei tohi tudengi eest kirjutada. Soovituste pikkus on backendis lõigatud 200 tähemärgini, mis muudab valmis ümberkirjutuse tehniliselt ebamugavaks.
