"""FastAPI rakendus – peamine sisendpunkt."""

import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from analyysija import AnalyysiViga, analyysi
from models import (
    AnalyysiPaaring,
    AnalyysiVastus,
    Mudel,
    PeatykiTyyp,
    PromptiTyyp,
)

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app = FastAPI(
    title="Eestikeelse lõputöö tagasisidesüsteem",
    description=(
        "Bakalaureusetöö prototüüp. Annab tudengi enda kirjutatud lõputöö "
        "tekstile soovituslikku tagasisidet neljas kategoorias."
    ),
    version="0.1.0",
)

LUBATUD_PARITOLU = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=LUBATUD_PARITOLU,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/api/health")
def tervis() -> dict[str, str]:
    return {"olek": "OK"}


@app.get("/api/options")
def valikud() -> dict[str, list[str]]:
    return {
        "peatuki_tyybid": [t.value for t in PeatykiTyyp],
        "prompti_tyybid": [t.value for t in PromptiTyyp],
        "mudelid": [m.value for m in Mudel],
    }


@app.post(
    "/api/analyse",
    response_model=AnalyysiVastus,
    response_model_by_alias=True,
)
def analyysi_endpoint(paaring: AnalyysiPaaring) -> AnalyysiVastus:
    try:
        return analyysi(paaring)
    except AnalyysiViga as e:
        raise HTTPException(status_code=502, detail=f"Mudeli viga: {e}") from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
