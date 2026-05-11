import json

import pytest
from fastapi.testclient import TestClient

import main
from demo_andmed import NAIDIS
from providers import DemoProvider, ProviderError, vali_pakkuja


def test_vali_pakkuja_demo_mudeli_korral_tagastab_demo_pakkuja():
    pakkuja = vali_pakkuja("demo")
    assert isinstance(pakkuja, DemoProvider)
    assert pakkuja.mudeli_nimi == "demo"


def test_demo_pakkuja_tagastab_kehtiva_jsoni_kui_prompt_sisaldab_peatuki_tyypi():
    pakkuja = DemoProvider()
    prompt = "Peatüki tüüp: sissejuhatus\nPeatüki tekst:\n\"\"\"\nNäide.\n\"\"\""
    vastus = pakkuja.kysi(prompt)
    andmed = json.loads(vastus)
    assert "leiud" in andmed
    assert len(andmed["leiud"]) == len(NAIDIS["sissejuhatus"]["leiud"])


def test_demo_pakkuja_viskab_vea_kui_peatuki_tyyp_puudub_promptist():
    pakkuja = DemoProvider()
    with pytest.raises(ProviderError):
        pakkuja.kysi("ilma peatüki tüübita prompt")


def test_demo_pakkuja_viskab_vea_tundmatu_peatuki_tyybi_korral():
    pakkuja = DemoProvider()
    with pytest.raises(ProviderError):
        pakkuja.kysi("Peatüki tüüp: olematu\nMuu sisu.")


def test_demo_kannab_andmed_olemas_iga_peatuki_tyybi_jaoks():
    oodatud = {"sissejuhatus", "taust", "metoodika", "tulemused", "kokkuvote"}
    assert set(NAIDIS.keys()) == oodatud


def test_analyse_endpoint_demo_mudeliga_toimib_ilma_välise_pakkujata():
    klient = TestClient(main.app)
    r = klient.post(
        "/api/analyse",
        json={
            "tekst": "Sissejuhatuse näide. " * 10,
            "peatuki_tyyp": "sissejuhatus",
            "prompti_tyyp": "struktureeritud",
            "mudel": "demo",
        },
    )
    assert r.status_code == 200
    keha = r.json()
    assert keha["meta"]["mudel"] == "demo"
    assert len(keha["leiud"]) > 0
