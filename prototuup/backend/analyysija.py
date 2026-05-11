"""Analüüsija – ühendab prompti malli, LLM-i pakkuja ja vastuse valideerimise."""

from __future__ import annotations

import json
import logging
import time
from collections import Counter
from pathlib import Path
from string import Template

from pydantic import ValidationError

from models import (
    AnalyysiMeta,
    AnalyysiPaaring,
    AnalyysiVastus,
    Leid,
    MudelivasusVorming,
)
from providers import LLMProvider, ProviderError, vali_pakkuja

PROMPTI_KAUST = Path(__file__).parent / "prompts"
MAX_PARANDUSKATSED = 1

logger = logging.getLogger(__name__)


class AnalyysiViga(Exception):
    pass


def _lae_prompti_mall(prompti_tyyp: str) -> Template:
    failinimi = {
        "yldine": "yldine.txt",
        "struktureeritud": "struktureeritud.txt",
    }[prompti_tyyp]
    sisu = (PROMPTI_KAUST / failinimi).read_text(encoding="utf-8")
    return Template(sisu)


def _ekstraktee_json(tekst: str) -> str:
    """Lõika tekstist välja esimene JSON-objekt.

    Mudel võib mõnikord tagastada JSON-i koos selgituse või koodiblokimärgenditega
    (```json ... ```), seega otsime esimese ``{``-ga algava ja viimase ``}``-ga
    lõppeva osa.
    """
    algus = tekst.find("{")
    lopp = tekst.rfind("}")
    if algus == -1 or lopp == -1 or lopp <= algus:
        raise AnalyysiViga(f"Mudeli vastuses ei õnnestunud JSON-i leida: {tekst[:200]}")
    return tekst[algus : lopp + 1]


def _valideeri_vastus(toores_tekst: str) -> MudelivasusVorming:
    json_tekst = _ekstraktee_json(toores_tekst)
    try:
        andmed = json.loads(json_tekst)
    except json.JSONDecodeError as e:
        raise AnalyysiViga(f"Mudeli vastus pole kehtiv JSON: {e}") from e
    try:
        return MudelivasusVorming.model_validate(andmed)
    except ValidationError as e:
        raise AnalyysiViga(f"Mudeli vastus ei vasta skeemile: {e}") from e


def _kysi_paranduseks(
    pakkuja: LLMProvider, esialgne_prompt: str, esialgne_vastus: str, viga: str
) -> str:
    parandus_prompt = (
        f"{esialgne_prompt}\n\n"
        f"--- SINU EELMINE VASTUS ---\n{esialgne_vastus}\n\n"
        f"--- VEATEAVE ---\n{viga}\n\n"
        "Palun paranda vastus nii, et see vastaks ülaltoodud skeemile. "
        "Vasta ainult JSON-iga."
    )
    return pakkuja.kysi(parandus_prompt)


def _ehita_meta(
    leiud: list[Leid], paaring: AnalyysiPaaring, kestus_ms: int
) -> AnalyysiMeta:
    loendur = Counter(leid.kategooria.value for leid in leiud)
    return AnalyysiMeta(
        mudel=paaring.mudel.value,
        prompti_tyyp=paaring.prompti_tyyp.value,
        peatuki_tyyp=paaring.peatuki_tyyp.value,
        leidude_arv_kategooriate_kaupa=dict(loendur),
        paaringu_kestus_ms=kestus_ms,
    )


def analyysi(paaring: AnalyysiPaaring) -> AnalyysiVastus:
    pakkuja = vali_pakkuja(paaring.mudel.value)
    mall = _lae_prompti_mall(paaring.prompti_tyyp.value)
    prompt = mall.substitute(
        peatüki_tüüp=paaring.peatuki_tyyp.value,
        tekst=paaring.tekst,
    )

    algus = time.monotonic()
    try:
        toores = pakkuja.kysi(prompt)
    except ProviderError as e:
        raise AnalyysiViga(str(e)) from e

    katse = 0
    while True:
        try:
            valideeritud = _valideeri_vastus(toores)
            break
        except AnalyysiViga as e:
            katse += 1
            if katse > MAX_PARANDUSKATSED:
                logger.warning("Mudel ei suuda vormingut järgida: %s", e)
                raise
            logger.info("Vormingu viga, küsime parandust (katse %d): %s", katse, e)
            try:
                toores = _kysi_paranduseks(pakkuja, prompt, toores, str(e))
            except ProviderError as pe:
                raise AnalyysiViga(str(pe)) from pe

    kestus_ms = int((time.monotonic() - algus) * 1000)
    leiud = valideeritud.leiud
    meta = _ehita_meta(leiud, paaring, kestus_ms)
    logger.info(
        "Analüüs valmis: mudel=%s, prompt=%s, leide=%d, kestus=%dms",
        meta.mudel,
        meta.prompti_tyyp,
        len(leiud),
        kestus_ms,
    )
    return AnalyysiVastus(leiud=leiud, meta=meta)
