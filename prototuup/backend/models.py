from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class Kategooria(str, Enum):
    STRUKTUUR = "STRUKTUUR"
    AKADEEMILINE_STIIL = "AKADEEMILINE_STIIL"
    TERMINOLOOGIA = "TERMINOLOOGIA"
    VIITAMISVAJADUS = "VIITAMISVAJADUS"
    MUU = "MUU"


class Kindlus(str, Enum):
    KORGE = "kõrge"
    KESKMINE = "keskmine"
    MADAL = "madal"


class PeatykiTyyp(str, Enum):
    SISSEJUHATUS = "sissejuhatus"
    TAUST = "taust"
    METOODIKA = "metoodika"
    TULEMUSED = "tulemused"
    KOKKUVOTE = "kokkuvote"


class PromptiTyyp(str, Enum):
    YLDINE = "yldine"
    STRUKTUREERITUD = "struktureeritud"


class Mudel(str, Enum):
    CLAUDE_3_5_SONNET = "claude-3-5-sonnet-20241022"
    GPT_4O = "gpt-4o-2024-08-06"


class Leid(BaseModel):
    kategooria: Kategooria
    tsitaat: str = Field(..., max_length=400)
    probleem: str = Field(..., max_length=400)
    pohjendus: str = Field(..., alias="põhjendus", max_length=600)
    soovitus: str = Field(..., max_length=200)
    kindlus: Kindlus

    model_config = {"populate_by_name": True}

    @field_validator("soovitus")
    @classmethod
    def trunkeeri_soovitus(cls, v: str) -> str:
        return v[:200]


class AnalyysiPaaring(BaseModel):
    tekst: str = Field(..., min_length=50, max_length=20_000)
    peatuki_tyyp: PeatykiTyyp
    prompti_tyyp: PromptiTyyp = PromptiTyyp.STRUKTUREERITUD
    mudel: Mudel = Mudel.CLAUDE_3_5_SONNET


class AnalyysiMeta(BaseModel):
    mudel: str
    prompti_tyyp: str
    peatuki_tyyp: str
    leidude_arv_kategooriate_kaupa: dict[str, int]
    paaringu_kestus_ms: int


class AnalyysiVastus(BaseModel):
    leiud: list[Leid]
    meta: AnalyysiMeta


class MudelivasusVorming(BaseModel):
    leiud: list[Leid]
