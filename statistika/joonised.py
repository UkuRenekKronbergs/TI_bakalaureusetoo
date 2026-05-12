"""Genereerib statistika CSV-failide põhjal näidisgraafikud (PNG).

Kõik joonised salvestatakse kausta ``joonised_png/``. Iga joonise eel on
loetav pealkiri ja sildid eestikeelsed; kõik andmed pärinevad ``andmed/``
kaustas olevatest CSV-failidest, mis on koostatud ``koguda.py`` skriptiga.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

JUUR = Path(__file__).resolve().parent
ANDMED = JUUR / "andmed"
JOONISED = JUUR / "joonised_png"
JOONISED.mkdir(parents=True, exist_ok=True)

# Värvid: kategooriapõhine palet, et joonised oleksid omavahel kooskõlas.
KATEGOORIA_VARV = {
    "STRUKTUUR": "#1f77b4",
    "AKADEEMILINE_STIIL": "#ff7f0e",
    "TERMINOLOOGIA": "#2ca02c",
    "VIITAMISVAJADUS": "#d62728",
}

KINDLUSE_VARV = {
    "kõrge": "#2ca02c",
    "keskmine": "#ffbf00",
    "madal": "#aaaaaa",
}

plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 110,
    "savefig.bbox": "tight",
})


def _salvesta(nimi: str) -> None:
    rada = JOONISED / f"{nimi}.png"
    plt.savefig(rada)
    plt.close()
    print(f"  -> {rada.relative_to(JUUR.parent)}")


# ---------------------------------------------------------------------------
# 1. Demo-leidude jaotus kategooriate kaupa (kokku üle kõikide peatükkide)
# ---------------------------------------------------------------------------


def joonis_demo_kategooriad_kokku() -> None:
    df = pd.read_csv(ANDMED / "demo_kategooriad_peatykiti.csv")
    kategooriad = [c for c in df.columns if c not in ("peatuki_tyyp", "kokku")]
    summad = df[kategooriad].sum()

    fig, ax = plt.subplots(figsize=(8, 5))
    pulgad = ax.bar(kategooriad, summad.values, color=[KATEGOORIA_VARV[k] for k in kategooriad])
    ax.set_title("Demo-režiimi leidude koguarv kategooriate kaupa\n(kokku üle 5 peatüki tüübi)")
    ax.set_ylabel("Leidude arv")
    ax.set_xlabel("Kategooria")
    for pulk, vaartus in zip(pulgad, summad.values):
        ax.text(pulk.get_x() + pulk.get_width() / 2, vaartus + 0.1, str(vaartus),
                ha="center", va="bottom", fontweight="bold")
    plt.xticks(rotation=15)
    _salvesta("01_demo_kategooriad_kokku")


# ---------------------------------------------------------------------------
# 2. Stacked bar – peatüki tüüp vs kategooria
# ---------------------------------------------------------------------------


def joonis_demo_peatykiti_stack() -> None:
    df = pd.read_csv(ANDMED / "demo_kategooriad_peatykiti.csv")
    kategooriad = [c for c in df.columns if c not in ("peatuki_tyyp", "kokku")]

    fig, ax = plt.subplots(figsize=(9, 5))
    pohi = [0] * len(df)
    for kat in kategooriad:
        ax.bar(df["peatuki_tyyp"], df[kat], bottom=pohi, label=kat, color=KATEGOORIA_VARV[kat])
        pohi = [a + b for a, b in zip(pohi, df[kat])]

    ax.set_title("Demo-režiimi leiud peatüki tüübi ja kategooria kaupa")
    ax.set_ylabel("Leidude arv")
    ax.set_xlabel("Peatüki tüüp")
    ax.legend(title="Kategooria", loc="upper right", fontsize=9)
    _salvesta("02_demo_peatykiti_stack")


# ---------------------------------------------------------------------------
# 3. Kindlushinnangu jaotus kategooriate kaupa
# ---------------------------------------------------------------------------


def joonis_kindlus() -> None:
    df = pd.read_csv(ANDMED / "demo_kindlus.csv")
    kindlused = ["kõrge", "keskmine", "madal"]

    fig, ax = plt.subplots(figsize=(8, 5))
    pohi = [0] * len(df)
    for k in kindlused:
        ax.barh(df["kategooria"], df[k], left=pohi, label=k, color=KINDLUSE_VARV[k])
        pohi = [a + b for a, b in zip(pohi, df[k])]

    ax.set_title("Kindlushinnangu jaotus demo-leidudes")
    ax.set_xlabel("Leidude arv")
    ax.legend(title="Kindlus", loc="lower right", fontsize=9)
    _salvesta("03_kindlus_jaotus")


# ---------------------------------------------------------------------------
# 4. Sõnade arv peatüki kaupa
# ---------------------------------------------------------------------------


def joonis_sonu_peatykis() -> None:
    df = pd.read_csv(ANDMED / "teksti_statistika.csv")
    df["lyhi_nimi"] = df["fail"].str.replace(".tex", "", regex=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    pulgad = ax.bar(df["lyhi_nimi"], df["sonu"], color="#3b82f6")
    ax.set_title(f"Sõnade arv lõputöö peatükkide kaupa (kokku {df['sonu'].sum():,})".replace(",", " "))
    ax.set_ylabel("Sõnade arv")
    ax.set_xlabel("Peatüki fail")
    for pulk, vaartus in zip(pulgad, df["sonu"]):
        ax.text(pulk.get_x() + pulk.get_width() / 2, vaartus + 20, str(vaartus),
                ha="center", va="bottom", fontsize=9)
    plt.xticks(rotation=30, ha="right")
    _salvesta("04_sonu_peatykis")


# ---------------------------------------------------------------------------
# 5. Viidete arv peatüki kaupa
# ---------------------------------------------------------------------------


def joonis_viiteid_peatykis() -> None:
    df = pd.read_csv(ANDMED / "teksti_statistika.csv")
    df["lyhi_nimi"] = df["fail"].str.replace(".tex", "", regex=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    pulgad = ax.bar(df["lyhi_nimi"], df["viiteid"], color="#8b5cf6")
    ax.set_title(f"\\cite-kasutuste arv peatükkide kaupa (kokku {df['viiteid'].sum()})")
    ax.set_ylabel(r"$\backslash$cite-kasutusi")
    ax.set_xlabel("Peatüki fail")
    for pulk, vaartus in zip(pulgad, df["viiteid"]):
        if vaartus > 0:
            ax.text(pulk.get_x() + pulk.get_width() / 2, vaartus + 0.3, str(vaartus),
                    ha="center", va="bottom", fontsize=9)
    plt.xticks(rotation=30, ha="right")
    _salvesta("05_viiteid_peatykis")


# ---------------------------------------------------------------------------
# 6. Prototüübi koodi LOC keelte kaupa
# ---------------------------------------------------------------------------


def joonis_kood_keeleti() -> None:
    df = pd.read_csv(ANDMED / "koodi_kokkuvote.csv")
    # Eemaldame mitte-programmeerimiskeele kirjed visuaalsest fookusest
    fookus = df[df["keel"].isin([
        "Python", "TypeScript", "TypeScript (TSX)", "JavaScript", "JSON", "CSS", "HTML", "YAML",
    ])].copy()
    fookus = fookus.sort_values("koodiridu", ascending=True)

    fig, ax = plt.subplots(figsize=(9, 5))
    pulgad = ax.barh(fookus["keel"], fookus["koodiridu"], color="#0ea5e9")
    ax.set_title(f"Prototüübi koodi ridade arv keelte kaupa (kokku {fookus['koodiridu'].sum():,})".replace(",", " "))
    ax.set_xlabel("Koodi ridu (ilma tühjade ja kommentaarideta)")
    for pulk, vaartus in zip(pulgad, fookus["koodiridu"]):
        ax.text(vaartus + max(fookus["koodiridu"]) * 0.01,
                pulk.get_y() + pulk.get_height() / 2,
                f"{vaartus:,}".replace(",", " "),
                va="center", fontsize=9)
    _salvesta("06_kood_keeleti")


# ---------------------------------------------------------------------------
# 7. Kavandatud testkogu kvoot
# ---------------------------------------------------------------------------


def joonis_testkogu_kvoot() -> None:
    df = pd.read_csv(ANDMED / "kavandatud_testkogu.csv")

    fig, ax = plt.subplots(figsize=(9, 5))
    pulgad = ax.bar(df["peatuki_tyyp"], df["katkendite_arv"], color="#10b981")
    ax.set_title("Kavandatud testkogu (Lisa I): katkendite arv peatüki tüübi kaupa\n"
                 f"Kokku {df['katkendite_arv'].sum()} katkendit; sihtpikkus 230–360 sõna")
    ax.set_ylabel("Katkendite arv")
    ax.set_xlabel("Peatüki tüüp")
    for pulk, vaartus in zip(pulgad, df["katkendite_arv"]):
        ax.text(pulk.get_x() + pulk.get_width() / 2, vaartus + 0.05, str(vaartus),
                ha="center", va="bottom", fontweight="bold")
    _salvesta("07_testkogu_kvoot")


# ---------------------------------------------------------------------------
# 8. Tekstistatistika ülevaade (mitu mõõdikut peatüki kohta)
# ---------------------------------------------------------------------------


def joonis_teksti_struktuur() -> None:
    df = pd.read_csv(ANDMED / "teksti_statistika.csv")
    df["lyhi_nimi"] = df["fail"].str.replace(".tex", "", regex=False)

    fig, axid = plt.subplots(2, 2, figsize=(12, 8))
    axid = axid.flatten()
    moodikud = [
        ("alapeatükke", "Alapeatükkide (\\subsection) arv", "#6366f1"),
        ("alamalapeatükke", "Alamalapeatükkide (\\subsubsection) arv", "#a855f7"),
        ("jooniseid", "Jooniste arv", "#f97316"),
        ("tabeleid", "Tabelite arv", "#0891b2"),
    ]
    for ax, (veerg, pealkiri, varv) in zip(axid, moodikud):
        ax.bar(df["lyhi_nimi"], df[veerg], color=varv)
        ax.set_title(pealkiri, fontsize=11)
        ax.tick_params(axis="x", rotation=45, labelsize=8)
        for sild in ax.get_xticklabels():
            sild.set_ha("right")
        # Numbrid pulkade peale
        for x, y in enumerate(df[veerg]):
            if y > 0:
                ax.text(x, y + 0.05, str(y), ha="center", va="bottom", fontsize=8)

    fig.suptitle("Töö struktuurielemendid peatükkide kaupa", fontsize=14, y=1.00)
    fig.tight_layout()
    _salvesta("08_teksti_struktuur")


# ---------------------------------------------------------------------------
# Käivitus
# ---------------------------------------------------------------------------


def main() -> None:
    print("Genereerin graafikud …")
    joonis_demo_kategooriad_kokku()
    joonis_demo_peatykiti_stack()
    joonis_kindlus()
    joonis_sonu_peatykis()
    joonis_viiteid_peatykis()
    joonis_kood_keeleti()
    joonis_testkogu_kvoot()
    joonis_teksti_struktuur()
    print(f"Valmis. Joonised kaustas: {JOONISED}")


if __name__ == "__main__":
    main()
