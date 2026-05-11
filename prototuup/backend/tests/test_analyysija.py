import json

import pytest

import analyysija
from models import (
    AnalyysiPaaring,
    Mudel,
    PeatykiTyyp,
    PromptiTyyp,
)
from providers.base import LLMProvider


class StubPakkuja(LLMProvider):
    def __init__(self, vastused: list[str]) -> None:
        self._vastused = list(vastused)
        self.kysitud_promptid: list[str] = []

    @property
    def mudeli_nimi(self) -> str:
        return "stub"

    def kysi(self, prompt: str, *, max_tokens: int = 4096, temperature: float = 0.2) -> str:
        del max_tokens, temperature
        self.kysitud_promptid.append(prompt)
        return self._vastused.pop(0)


KEHTIVA_VASTUSE_KEHA = json.dumps(
    {
        "leiud": [
            {
                "kategooria": "VIITAMISVAJADUS",
                "tsitaat": "Üle 75% arendajatest kasutab Reactit.",
                "probleem": "Konkreetne arvuline väide ilma viiteta.",
                "põhjendus": "Numbrilist väidet peab toetama allikas.",
                "soovitus": "Lisa viide originaaluuringule.",
                "kindlus": "kõrge",
            }
        ]
    }
)


@pytest.fixture
def asenda_pakkuja(monkeypatch: pytest.MonkeyPatch):
    konteiner: dict[str, StubPakkuja] = {}

    def asenda_vastustega(vastused: list[str]) -> StubPakkuja:
        pakkuja = StubPakkuja(vastused)
        konteiner["pakkuja"] = pakkuja
        monkeypatch.setattr(analyysija, "vali_pakkuja", lambda _mudel: pakkuja)
        return pakkuja

    return asenda_vastustega


def teha_paaring(tekst: str | None = None) -> AnalyysiPaaring:
    return AnalyysiPaaring(
        tekst=tekst or ("Sõnad sõnade järel " * 20),
        peatuki_tyyp=PeatykiTyyp.SISSEJUHATUS,
        prompti_tyyp=PromptiTyyp.STRUKTUREERITUD,
        mudel=Mudel.CLAUDE_3_5_SONNET,
    )


def test_kehtiva_jsoni_korral_tagastatakse_leiud(asenda_pakkuja):
    asenda_pakkuja([KEHTIVA_VASTUSE_KEHA])
    vastus = analyysija.analyysi(teha_paaring())
    assert len(vastus.leiud) == 1
    assert vastus.leiud[0].kategooria.value == "VIITAMISVAJADUS"
    assert vastus.meta.leidude_arv_kategooriate_kaupa == {"VIITAMISVAJADUS": 1}


def test_jsoni_kus_on_lisatekst_ekstraktitakse(asenda_pakkuja):
    saastunud = "Siin on selgitus.\n```json\n" + KEHTIVA_VASTUSE_KEHA + "\n```\nLõpp."
    asenda_pakkuja([saastunud])
    vastus = analyysija.analyysi(teha_paaring())
    assert len(vastus.leiud) == 1


def test_vigane_skeem_tekitab_paranduspaaringu(asenda_pakkuja):
    vigane = json.dumps({"leiud": [{"kategooria": "TUNDMATU"}]})
    pakkuja = asenda_pakkuja([vigane, KEHTIVA_VASTUSE_KEHA])
    vastus = analyysija.analyysi(teha_paaring())
    assert len(vastus.leiud) == 1
    assert len(pakkuja.kysitud_promptid) == 2


def test_korduvalt_vigane_skeem_viskab_erandit(asenda_pakkuja):
    vigane = "see pole isegi mitte JSON"
    asenda_pakkuja([vigane, vigane])
    with pytest.raises(analyysija.AnalyysiViga):
        analyysija.analyysi(teha_paaring())


def test_promptisse_pannakse_peatuki_tyyp_ja_tekst(asenda_pakkuja):
    pakkuja = asenda_pakkuja([KEHTIVA_VASTUSE_KEHA])
    paaring = teha_paaring(tekst="Spetsiifiline tekst, mille leidmist soovin.")
    analyysija.analyysi(paaring)
    saadetud = pakkuja.kysitud_promptid[0]
    assert "sissejuhatus" in saadetud
    assert "Spetsiifiline tekst, mille leidmist soovin." in saadetud
