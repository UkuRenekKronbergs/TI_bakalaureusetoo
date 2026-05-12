"""Kogub bakalaureusetöö ja prototüübi kohta statistilisi näitajaid.

Skript loeb kolm allikat ja kirjutab CSV-failid kausta ``andmed/``:

1. Prototüübi demo-režiimi leiud (``demo_andmed.NAIDIS``):
   - ``demo_leiud.csv`` – iga leid eraldi reana;
   - ``demo_kategooriad_peatykiti.csv`` – leidude arv (peatüki tüüp × kategooria);
   - ``demo_kindlus.csv`` – kindlushinnangu jaotus.

2. Lõputöö LaTeX-failide tekstistatistika:
   - ``teksti_statistika.csv`` – iga peatüki kohta sõnade arv, viidete arv,
     jooniste arv, tabelite arv, valemite arv, koodinäidete arv ja
     alapeatükkide arv.

3. Prototüübi koodi statistika:
   - ``koodi_statistika.csv`` – iga koodifaili kohta keel, ridade arv (ilma
     tühjade ja kommentaarideta) ning faili suurus baitides;
   - ``koodi_kokkuvote.csv`` – keelte kaupa kogusumma.

4. Kavandatud testkogu kvoot (Lisa I tabel):
   - ``kavandatud_testkogu.csv`` – peatüki tüüp, katkendite arv ja sihtpikkused.

Andmed on faktilised, mitte simuleeritud. Skripti uuesti käivitamine annab
samad tulemused.
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

# Repositooriumi juur — kahe taseme jagu üles statistika/koguda.py-st
JUUR = Path(__file__).resolve().parent.parent
ANDMED = Path(__file__).resolve().parent / "andmed"
ANDMED.mkdir(parents=True, exist_ok=True)

# Et saaksime importida prototüübi demo_andmed mooduli.
sys.path.insert(0, str(JUUR / "prototuup" / "backend"))


# ---------------------------------------------------------------------------
# 1. Demo-prototüübi leiud
# ---------------------------------------------------------------------------


def kogu_demo_leiud() -> None:
    """Kirjutab demo-režiimi leidudest kolm CSV-faili."""
    from demo_andmed import NAIDIS  # noqa: WPS433 — käivituseks vajalik

    # demo_leiud.csv – iga leid eraldi reana
    with (ANDMED / "demo_leiud.csv").open("w", encoding="utf-8", newline="") as f:
        kirjutaja = csv.writer(f)
        kirjutaja.writerow([
            "peatuki_tyyp",
            "kategooria",
            "kindlus",
            "probleem",
            "soovituse_pikkus",
            "tsitaadi_pikkus",
        ])
        for peatyk, sisu in NAIDIS.items():
            for leid in sisu["leiud"]:
                kirjutaja.writerow([
                    peatyk,
                    leid["kategooria"],
                    leid["kindlus"],
                    leid["probleem"],
                    len(leid["soovitus"]),
                    len(leid["tsitaat"]),
                ])

    # demo_kategooriad_peatykiti.csv – leidude arv peatüki tüübi ja kategooria kaupa
    kategooriad = ["STRUKTUUR", "AKADEEMILINE_STIIL", "TERMINOLOOGIA", "VIITAMISVAJADUS"]
    with (ANDMED / "demo_kategooriad_peatykiti.csv").open("w", encoding="utf-8", newline="") as f:
        kirjutaja = csv.writer(f)
        kirjutaja.writerow(["peatuki_tyyp", *kategooriad, "kokku"])
        for peatyk, sisu in NAIDIS.items():
            arvud = Counter(leid["kategooria"] for leid in sisu["leiud"])
            rida = [peatyk] + [arvud.get(k, 0) for k in kategooriad]
            rida.append(sum(arvud.get(k, 0) for k in kategooriad))
            kirjutaja.writerow(rida)

    # demo_kindlus.csv – kindlushinnangu jaotus kategooriate kaupa
    kindlused = ["kõrge", "keskmine", "madal"]
    with (ANDMED / "demo_kindlus.csv").open("w", encoding="utf-8", newline="") as f:
        kirjutaja = csv.writer(f)
        kirjutaja.writerow(["kategooria", *kindlused])
        jaotus: dict[str, Counter] = {k: Counter() for k in kategooriad}
        for sisu in NAIDIS.values():
            for leid in sisu["leiud"]:
                jaotus[leid["kategooria"]][leid["kindlus"]] += 1
        for kat in kategooriad:
            kirjutaja.writerow([kat] + [jaotus[kat].get(k, 0) for k in kindlused])


# ---------------------------------------------------------------------------
# 2. Lõputöö tekstistatistika
# ---------------------------------------------------------------------------


# LaTeX-i puhastamine sõnaloenduseks
_COMMENT_RE = re.compile(r"(?<!\\)%.*?$", re.MULTILINE)
_OPT_RE = re.compile(r"\\[a-zA-Z]+(\[[^\]]*\])*(\{[^{}]*\})*")
_MATH_RE = re.compile(r"\$[^$]*\$")
_MINTED_RE = re.compile(r"\\begin\{minted\}.*?\\end\{minted\}", re.DOTALL)


def _loe_tekstid(fail: Path) -> str:
    return fail.read_text(encoding="utf-8")


def _sonade_arv(tekst: str) -> int:
    """Loendab sõnu LaTeX-tekstis pärast käskude ja kommentaaride eemaldamist."""
    t = _MINTED_RE.sub(" ", tekst)
    t = _COMMENT_RE.sub("", t)
    t = _MATH_RE.sub(" ", t)
    t = _OPT_RE.sub(" ", t)
    t = re.sub(r"[\{\}\[\]\\]+", " ", t)
    t = re.sub(r"[~_^&]+", " ", t)
    sonad = [s for s in t.split() if re.search(r"[A-Za-zÕÄÖÜõäöüŠšŽž]", s)]
    return len(sonad)


def _loenda(tekst: str, muster: str) -> int:
    return len(re.findall(muster, tekst))


def _kasutatud_sektsioonid() -> list[Path]:
    """Leiab failid, mille põhi.tex tegelikult \\input-ib.

    Mall sisaldab kasutamata jäänud peatükke (nt 2-vormistamine.tex),
    millede sõnu lõputöö koondisse ei tasu lugeda.
    """
    pohi = (JUUR / "estonian" / "põhi.tex").read_text(encoding="utf-8")
    sektsioonid = JUUR / "estonian" / "sektsioonid"
    nimed = re.findall(r"\\input\{sektsioonid/([^\}]+)\}", pohi)
    failid = [sektsioonid / f"{n}.tex" for n in nimed if (sektsioonid / f"{n}.tex").exists()]
    return failid


def kogu_teksti_statistika() -> None:
    failid = _kasutatud_sektsioonid()

    with (ANDMED / "teksti_statistika.csv").open("w", encoding="utf-8", newline="") as f:
        kirjutaja = csv.writer(f)
        kirjutaja.writerow([
            "fail",
            "sonu",
            "viiteid",
            "jooniseid",
            "tabeleid",
            "valemeid",
            "koodinäiteid",
            "alapeatükke",
            "alamalapeatükke",
        ])
        for fail in failid:
            t = _loe_tekstid(fail)
            kirjutaja.writerow([
                fail.name,
                _sonade_arv(t),
                _loenda(t, r"\\cite\{"),
                _loenda(t, r"\\begin\{figure\}"),
                _loenda(t, r"\\begin\{table\}"),
                _loenda(t, r"\\begin\{equation\}"),
                _loenda(t, r"\\begin\{minted\}"),
                _loenda(t, r"\\subsection\{"),
                _loenda(t, r"\\subsubsection\{"),
            ])

    # Eraldi: bib-kirjete arv ja viidete kogusumma kõigi peatükkide peale.
    bib = (JUUR / "estonian" / "viited.bib").read_text(encoding="utf-8")
    bib_kirjeid = len(re.findall(r"^@\w+\{", bib, re.MULTILINE))
    yldine_viiteid = sum(_loenda(_loe_tekstid(f), r"\\cite\{") for f in failid)
    with (ANDMED / "viidete_kokkuvote.csv").open("w", encoding="utf-8", newline="") as f:
        kirjutaja = csv.writer(f)
        kirjutaja.writerow(["bib_kirjeid", "cite_kasutusi_tekstis"])
        kirjutaja.writerow([bib_kirjeid, yldine_viiteid])


# ---------------------------------------------------------------------------
# 3. Prototüübi koodi statistika
# ---------------------------------------------------------------------------


_FAILI_TYYBID = {
    ".py": ("Python", "#"),
    ".ts": ("TypeScript", "//"),
    ".tsx": ("TypeScript (TSX)", "//"),
    ".js": ("JavaScript", "//"),
    ".css": ("CSS", None),
    ".html": ("HTML", None),
    ".yml": ("YAML", "#"),
    ".yaml": ("YAML", "#"),
    ".json": ("JSON", None),
    ".txt": ("Tekst", None),
    ".md": ("Markdown", None),
}

_VALISTA_KAUSTAD = {"node_modules", "__pycache__", ".venv", "dist", ".git"}
_VALISTA_FAILID = {"package-lock.json"}  # auto-genereeritud, mitte kirjutatud kood


def _on_kommentaar(rida: str, kommentaar_alustus: str | None) -> bool:
    if kommentaar_alustus is None:
        return False
    return rida.strip().startswith(kommentaar_alustus)


def kogu_koodi_statistika() -> None:
    prot = JUUR / "prototuup"
    read: list[tuple[str, str, int, int]] = []

    for fail in prot.rglob("*"):
        if not fail.is_file():
            continue
        # Välista hooldatud kaustad
        if any(osa in _VALISTA_KAUSTAD for osa in fail.parts):
            continue
        if fail.name in _VALISTA_FAILID:
            continue
        if fail.suffix not in _FAILI_TYYBID:
            continue

        keel, kommentaar = _FAILI_TYYBID[fail.suffix]
        try:
            sisu = fail.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            sisu = fail.read_text(encoding="utf-8", errors="ignore")
        koodiridu = sum(
            1
            for rida in sisu.splitlines()
            if rida.strip() and not _on_kommentaar(rida, kommentaar)
        )
        suurus = fail.stat().st_size
        read.append((str(fail.relative_to(JUUR)).replace("\\", "/"), keel, koodiridu, suurus))

    with (ANDMED / "koodi_statistika.csv").open("w", encoding="utf-8", newline="") as f:
        kirjutaja = csv.writer(f)
        kirjutaja.writerow(["fail", "keel", "koodiridu", "suurus_baitides"])
        for r in sorted(read, key=lambda x: (x[1], -x[2])):
            kirjutaja.writerow(r)

    # Kokkuvõte keelte kaupa
    keeleti: dict[str, dict[str, int]] = {}
    for _, keel, ridu, suurus in read:
        d = keeleti.setdefault(keel, {"faile": 0, "ridu": 0, "baite": 0})
        d["faile"] += 1
        d["ridu"] += ridu
        d["baite"] += suurus

    with (ANDMED / "koodi_kokkuvote.csv").open("w", encoding="utf-8", newline="") as f:
        kirjutaja = csv.writer(f)
        kirjutaja.writerow(["keel", "faile", "koodiridu", "suurus_baitides"])
        for keel in sorted(keeleti, key=lambda k: -keeleti[k]["ridu"]):
            v = keeleti[keel]
            kirjutaja.writerow([keel, v["faile"], v["ridu"], v["baite"]])


# ---------------------------------------------------------------------------
# 4. Kavandatud testkogu kvoot (Lisa I tabel)
# ---------------------------------------------------------------------------


_TESTKOGU = [
    ("sissejuhatus",       4, 250, 320),
    ("taust",              5, 280, 360),
    ("metoodika",          4, 270, 330),
    ("tulemused",          4, 240, 290),
    ("kokkuvote",          3, 230, 260),
]


def kogu_kavandatud_testkogu() -> None:
    with (ANDMED / "kavandatud_testkogu.csv").open("w", encoding="utf-8", newline="") as f:
        kirjutaja = csv.writer(f)
        kirjutaja.writerow(["peatuki_tyyp", "katkendite_arv", "sihtpikkus_min", "sihtpikkus_max"])
        for rida in _TESTKOGU:
            kirjutaja.writerow(rida)


# ---------------------------------------------------------------------------
# Käivitus
# ---------------------------------------------------------------------------


def main() -> None:
    print("Kogun demo-prototüübi leiud …")
    kogu_demo_leiud()
    print("Kogun lõputöö tekstistatistika …")
    kogu_teksti_statistika()
    print("Kogun prototüübi koodi statistika …")
    kogu_koodi_statistika()
    print("Kirjutan kavandatud testkogu kvoot …")
    kogu_kavandatud_testkogu()
    print(f"Valmis. Andmed kaustas: {ANDMED}")


if __name__ == "__main__":
    main()
