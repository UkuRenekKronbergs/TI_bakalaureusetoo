# Eestikeelse lõputöö tagasisidesüsteem – prototüüp

Bakalaureusetöö „Suurte keelemudelite kasutamine eestikeelse tehnilise informaatika teksti kvaliteedikontrolliks” praktiline tulemus. Süsteem võtab sisendiks tudengi enda kirjutatud lõputöö peatüki, suunab selle valitud LLM-ile struktureeritud viibaga ning kuvab kategoriseeritud tagasiside neljas kategoorias: struktuur, akadeemiline stiil, terminoloogia, viitamisvajadus.

> **Oluline**: see süsteem ei kirjuta lõputööd tudengi eest ega asenda juhendajat. See annab tudengi enda kirjutatud tekstile soovituslikku tagasisidet.

## Arhitektuur

```
+------------+        HTTP        +-----------+        HTTPS        +-----------+
|  Frontend  | <----------------> |  Backend  | <-----------------> |  LLM API  |
| React + TS |    /api/analyse    | FastAPI   |   Anthropic/OpenAI  |           |
+------------+                    +-----------+                     +-----------+
```

- **Backend** ([backend/](backend/)): Python 3.12 + FastAPI + Pydantic. Hoiab promptide malle, kombineerib need sisendiga, kutsub LLM-i ja valideerib JSON-vastuse skeemi vastu.
- **Frontend** ([frontend/](frontend/)): React 18 + TypeScript + Tailwind CSS. Kasutajaliides koos privaatsusdialoogi, peatüki tüübi valija, prompti tüübi valija ja kategoriseeritud tagasisidepaneeliga.

## Käivitamine Dockeriga (soovitatav)

Eeldused: Docker Desktop 4 või uuem (Docker Compose v2 sisemiselt).

1. Kopeeri keskkonnamuutujate näidisfail ja lisa oma API võti:
   ```bash
   cp .env.example .env
   # Ava .env oma redaktoris ja täida ANTHROPIC_API_KEY rida.
   ```
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
export ANTHROPIC_API_KEY=sk-ant-...      # PowerShell: $env:ANTHROPIC_API_KEY="sk-ant-..."
uvicorn main:app --reload --port 8000
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

Kõik tundlikud väärtused tulevad keskkonnamuutujatest. Vt [.env.example](.env.example):

| Muutuja                | Vajalik?          | Selgitus                                        |
| ---------------------- | ----------------- | ----------------------------------------------- |
| `ANTHROPIC_API_KEY`    | jah, Claude jaoks | Anthropic Messages API ligipääsuvõti.           |
| `OPENAI_API_KEY`       | ainult GPT jaoks  | OpenAI Chat Completions API võti.               |
| `LOG_LEVEL`            | ei                | DEBUG \| INFO \| WARNING \| ERROR. Vaikimisi INFO. |
| `CORS_ALLOWED_ORIGINS` | ei                | Komaeraldatud frontendi päritolud.              |

## API

`POST /api/analyse`

Päringukeha:
```json
{
  "tekst": "Sisestatud peatüki tekst.",
  "peatuki_tyyp": "sissejuhatus",
  "prompti_tyyp": "struktureeritud",
  "mudel": "claude-3-5-sonnet-20241022"
}
```

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
    "mudel": "claude-3-5-sonnet-20241022",
    "prompti_tyyp": "struktureeritud",
    "peatuki_tyyp": "sissejuhatus",
    "leidude_arv_kategooriate_kaupa": {"VIITAMISVAJADUS": 1},
    "paaringu_kestus_ms": 4283
  }
}
```

## Promptide muutmine

Promptid asuvad eraldi failides ja neid saab muuta ilma koodi puutumata:

- [backend/prompts/yldine.txt](backend/prompts/yldine.txt)
- [backend/prompts/struktureeritud.txt](backend/prompts/struktureeritud.txt)

Mõlemas failis on muutujad `${peatüki_tüüp}` ja `${tekst}`, mis asendatakse päringu käigus.

## Testid

```bash
cd backend
pytest
```

Testid asuvad kaustas [backend/tests/](backend/tests/) ja katavad valideerimisloogika ning prompti malli laadimise ilma välimist API-d puudutamata.

## Privaatsus ja eetika

- Sisestatud tekst saadetakse Anthropici või OpenAI serveritesse. Frontend näitab enne esimest päringut hoiatusdialoogi, mille kasutaja peab kinnitama.
- Backend ei salvesta sisestatud teksti kettal; logitakse vaid anonüümseid sündmuseid (mudel, prompti tüüp, leidude arv kategooriate kaupa, kestus).
- Süsteemi prompt sisaldab selget piirangut, et mudel ei tohi tudengi eest kirjutada. Soovituste pikkus on backendis lõigatud 200 tähemärgini, mis muudab valmis ümber\-kirjutuse tehniliselt ebamugavaks.
