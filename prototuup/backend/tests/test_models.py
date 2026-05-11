import pytest
from pydantic import ValidationError

from models import Kategooria, Kindlus, Leid, MudelivasusVorming


def test_leid_aktsepteerib_pohjenduse_alias():
    leid = Leid(
        kategooria=Kategooria.STRUKTUUR,
        tsitaat="Näite tsitaat.",
        probleem="Näite probleem.",
        **{"põhjendus": "Sest nii."},
        soovitus="Näite soovitus.",
        kindlus=Kindlus.KORGE,
    )
    assert leid.pohjendus == "Sest nii."


def test_soovitus_lyhendatakse_kuni_200_margini():
    pikk = "x" * 500
    leid = Leid(
        kategooria=Kategooria.STRUKTUUR,
        tsitaat="t",
        probleem="p",
        **{"põhjendus": "põ"},
        soovitus=pikk,
        kindlus=Kindlus.MADAL,
    )
    assert len(leid.soovitus) == 200


def test_kindlus_madal_voti_ei_aktsepteeritud():
    with pytest.raises(ValidationError):
        Leid(
            kategooria=Kategooria.STRUKTUUR,
            tsitaat="t",
            probleem="p",
            **{"põhjendus": "põ"},
            soovitus="s",
            kindlus="ebamäärane",  # type: ignore[arg-type]
        )


def test_mudelivasus_aktsepteerib_tyhja_loendi():
    v = MudelivasusVorming(leiud=[])
    assert v.leiud == []
