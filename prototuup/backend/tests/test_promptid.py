from string import Template

from analyysija import _lae_prompti_mall


def test_yldine_prompt_aktsepteerib_substitutsiooni():
    mall = _lae_prompti_mall("yldine")
    assert isinstance(mall, Template)
    valmis = mall.substitute(peatuki_tyyp="taust", tekst="näide")
    assert "taust" in valmis
    assert "näide" in valmis


def test_struktureeritud_prompt_sisaldab_eetilist_piirangut():
    mall = _lae_prompti_mall("struktureeritud")
    valmis = mall.substitute(peatuki_tyyp="metoodika", tekst="t")
    assert "EI OLE LUBATUD" in valmis
    assert "STRUKTUUR" in valmis
    assert "VIITAMISVAJADUS" in valmis
    assert "JSON" in valmis


def test_struktureeritud_prompt_keelab_umbersonastuse():
    mall = _lae_prompti_mall("struktureeritud")
    valmis = mall.substitute(peatuki_tyyp="t", tekst="t")
    assert "MITTE valmis ümbersõnastus" in valmis
