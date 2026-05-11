from enum import Enum

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
    CLAUDE_OPUS_4_7 = "claude-opus-4-7"
    GPT_5 = "gpt-5"


class Leid(BaseModel):
    kategooria: Kategooria
    tsitaat: str
    probleem: str = Field(..., max_length=400)
    pohjendus: str = Field(..., alias="põhjendus", max_length=600)
    soovitus: str
    kindlus: Kindlus

    model_config = {"populate_by_name": True}

    @field_validator("tsitaat", "soovitus", mode="before")
    @classmethod
    def trunkeeri_kuni_200(cls, v: object) -> object:
        if isinstance(v, str):
            return v[:200]
        return v


class AnalyysiPaaring(BaseModel):
    tekst: str = Field(..., min_length=50, max_length=20_000)
    peatuki_tyyp: PeatykiTyyp
    prompti_tyyp: PromptiTyyp = PromptiTyyp.STRUKTUREERITUD
    mudel: Mudel = Mudel.CLAUDE_OPUS_4_7


class AnalyysiMeta(BaseModel):
    mudel: str
    prompti_tyyp: str
    peatuki_tyyp: str
    leidude_arv_kategooriate_kaupa: dict[str, int]
    paaringu_kestus_ms: int


class AnalyysiVastus(BaseModel):
    leiud: list[Leid]
    meta: AnalyysiMeta


class MudeliVastuseVorming(BaseModel):
    leiud: list[Leid]
