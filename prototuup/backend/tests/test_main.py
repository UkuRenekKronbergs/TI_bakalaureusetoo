import json

import pytest
from fastapi.testclient import TestClient

import analyysija
import main
from providers.base import LLMProvider


class StubPakkuja(LLMProvider):
    def __init__(self, vastus: str) -> None:
        self._vastus = vastus

    @property
    def mudeli_nimi(self) -> str:
        return "stub"

    def kysi(self, prompt: str, *, max_tokens: int = 4096, temperature: float = 0.2) -> str:
        del prompt, max_tokens, temperature
        return self._vastus


KEHTIV_VASTUS = json.dumps(
    {
        "leiud": [
            {
                "kategooria": "STRUKTUUR",
                "tsitaat": "Peatükk algab kohe alapealkirjaga.",
                "probleem": "Sissejuhatav lõik puudub.",
                "põhjendus": "Lugeja ei saa peatüki sisust ettekujutust.",
                "soovitus": "Lisa peatüki algusesse 3-4 lauseline sissejuhatus.",
                "kindlus": "kõrge",
            }
        ]
    }
)


@pytest.fixture
def klient(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setattr(
        analyysija,
        "vali_pakkuja",
        lambda _mudel: StubPakkuja(KEHTIV_VASTUS),
    )
    return TestClient(main.app)


def test_health_endpoint(klient: TestClient):
    r = klient.get("/api/health")
    assert r.status_code == 200
    assert r.json() == {"olek": "OK"}


def test_options_endpoint_tagastab_loendi(klient: TestClient):
    r = klient.get("/api/options")
    assert r.status_code == 200
    keha = r.json()
    assert "sissejuhatus" in keha["peatuki_tyybid"]
    assert "struktureeritud" in keha["prompti_tyybid"]


def test_analyse_endpoint_kehtiv(klient: TestClient):
    r = klient.post(
        "/api/analyse",
        json={
            "tekst": "Sissejuhatuse teksti näide. " * 10,
            "peatuki_tyyp": "sissejuhatus",
            "prompti_tyyp": "struktureeritud",
            "mudel": "claude-3-5-sonnet-20241022",
        },
    )
    assert r.status_code == 200
    keha = r.json()
    assert len(keha["leiud"]) == 1
    assert keha["meta"]["mudel"] == "claude-3-5-sonnet-20241022"


def test_analyse_endpoint_liiga_lyhike_tekst_400(klient: TestClient):
    r = klient.post(
        "/api/analyse",
        json={
            "tekst": "lühike",
            "peatuki_tyyp": "sissejuhatus",
            "prompti_tyyp": "struktureeritud",
            "mudel": "claude-3-5-sonnet-20241022",
        },
    )
    assert r.status_code == 422


def test_analyse_endpoint_tundmatu_peatyki_tyyp_422(klient: TestClient):
    r = klient.post(
        "/api/analyse",
        json={
            "tekst": "Pikem tekst, mis ületab piiri. " * 10,
            "peatuki_tyyp": "tundmatu",
            "prompti_tyyp": "struktureeritud",
            "mudel": "claude-3-5-sonnet-20241022",
        },
    )
    assert r.status_code == 422
