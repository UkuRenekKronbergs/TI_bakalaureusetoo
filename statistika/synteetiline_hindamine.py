"""Sünteetiline hindamis-pipeline'i demonstratsioon.

⚠ SÜNTEETILISED ANDMED ⚠

Käesolev skript NE mõõda LLM-ide tegelikku sooritust. Skript:

1. Loeb käsitsi koostatud testkogu ja kuldstandardi (``andmestik_synth.py``).
2. Genereerib iga (katkend × prompti tüüp × mudel) kombinatsiooni kohta
   sünteetilised „mudeli väljundid", kasutades juhuslike Bernoulli-tõmmistega
   profiilipõhist simulatsiooni. Profiilid (vt allpool ``RECALL`` ja ``FP``)
   on autori postulaat, mitte mõõtmistulemus.
3. Arvutab pipeline'ile standardsed mõõdikud (TP, FP, FN, täpsus, saagis,
   F\textsubscript{1}) iga kategooria × prompti tüüp × mudel kombinatsiooni
   kohta.
4. Kirjutab CSV-failid kausta ``andmed/`` ja graafikud kausta ``joonised_png/``.

Skripti eesmärk on demonstreerida, et hindamis-pipeline on tehniliselt
toimiv: metrikate arvutus on korrektne, tabeli ja graafikute struktuur on
selline, nagu täismahulises hindamises ootus on. Numbrid ise on
sünteetilised. Päris hindamise jaoks tuleb mudelivastused asendada
tegelike LLM-i päringute väljunditega.

Tehniline aluseks:
  - Seeditud Mersenne'i twister (random.seed = 20260512) tagab
    reprodutseeritavuse.
  - Mudeli profiilid on dokumenteeritud, mitte peidetud.
"""

from __future__ import annotations

import csv
import random
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from andmestik_synth import KATEGOORIAD, TESTKOGU

JUUR = Path(__file__).resolve().parent
ANDMED = JUUR / "andmed"
JOONISED = JUUR / "joonised_png"
ANDMED.mkdir(exist_ok=True)
JOONISED.mkdir(exist_ok=True)

SEEME = 20260512  # tagab reprodutseeritavuse


# ---------------------------------------------------------------------------
# MUDELI PROFIILID (autori postulaat, mitte mõõtmistulemus)
# ---------------------------------------------------------------------------
#
# Profiilid peegeldavad thesis ptk 5 pilootuuringus täheldatud kvalitatiivseid
# mustreid:
#   - struktureeritud prompt > üldine prompt enamikus kategooriates;
#   - viitamisvajadus ja struktuur on usaldusväärsemad kui terminoloogia;
#   - Claude 4.7 Opus mõnevõrra tugevam eestikeelse teksti puhul kui GPT-5.5.
# Need on hüpoteesid, mitte mõõdetud väärtused.

# Saagis = tõenäosus, et iga kuldstandardi annotatsioon detekteeritakse.
RECALL: dict[tuple[str, str], dict[str, float]] = {
    ("claude-opus-4-7", "struktureeritud"): {
        "STRUKTUUR":          0.85,
        "AKADEEMILINE_STIIL": 0.80,
        "TERMINOLOOGIA":      0.55,
        "VIITAMISVAJADUS":    0.90,
    },
    ("claude-opus-4-7", "yldine"): {
        "STRUKTUUR":          0.55,
        "AKADEEMILINE_STIIL": 0.70,
        "TERMINOLOOGIA":      0.45,
        "VIITAMISVAJADUS":    0.65,
    },
    ("gpt-5.5", "struktureeritud"): {
        "STRUKTUUR":          0.80,
        "AKADEEMILINE_STIIL": 0.78,
        "TERMINOLOOGIA":      0.50,
        "VIITAMISVAJADUS":    0.85,
    },
    ("gpt-5.5", "yldine"): {
        "STRUKTUUR":          0.50,
        "AKADEEMILINE_STIIL": 0.62,
        "TERMINOLOOGIA":      0.38,
        "VIITAMISVAJADUS":    0.58,
    },
}

# Valepositiivsete tõenäosus katkendi ja kategooria kohta.
# Iga (katkend × kategooria) puhul on selle tõenäosusega vähemalt üks FP.
FP_TOENAOSUS: dict[tuple[str, str], dict[str, float]] = {
    ("claude-opus-4-7", "struktureeritud"): {
        "STRUKTUUR":          0.08,
        "AKADEEMILINE_STIIL": 0.18,
        "TERMINOLOOGIA":      0.30,
        "VIITAMISVAJADUS":    0.12,
    },
    ("claude-opus-4-7", "yldine"): {
        "STRUKTUUR":          0.15,
        "AKADEEMILINE_STIIL": 0.30,
        "TERMINOLOOGIA":      0.40,
        "VIITAMISVAJADUS":    0.20,
    },
    ("gpt-5.5", "struktureeritud"): {
        "STRUKTUUR":          0.10,
        "AKADEEMILINE_STIIL": 0.22,
        "TERMINOLOOGIA":      0.35,
        "VIITAMISVAJADUS":    0.15,
    },
    ("gpt-5.5", "yldine"): {
        "STRUKTUUR":          0.18,
        "AKADEEMILINE_STIIL": 0.35,
        "TERMINOLOOGIA":      0.45,
        "VIITAMISVAJADUS":    0.25,
    },
}

MUDELID = ["claude-opus-4-7", "gpt-5.5"]
PROMPTID = ["yldine", "struktureeritud"]


# ---------------------------------------------------------------------------
# Simulatsioon
# ---------------------------------------------------------------------------


def simuleeri() -> dict[tuple[str, str], list[dict]]:
    """Tagastab dict[(mudel, prompt)] -> list[finding-record].

    Iga finding-record sisaldab:
      - katkend_id, kategooria, klassifikatsioon (TP | FP)
    Lisaks lisatakse kuldstandardi puudumised (FN) eraldi.
    """
    rng = random.Random(SEEME)
    valjundid: dict[tuple[str, str], list[dict]] = {
        (m, p): [] for m in MUDELID for p in PROMPTID
    }

    for m in MUDELID:
        for p in PROMPTID:
            r_profiil = RECALL[(m, p)]
            fp_profiil = FP_TOENAOSUS[(m, p)]

            for katkend in TESTKOGU:
                # 1) Kuldstandardi annotatsioonid: TP/FN
                detekteeritud_kuld_index: set[int] = set()
                for i, ann in enumerate(katkend["kuldstandard"]):
                    if rng.random() < r_profiil[ann["kategooria"]]:
                        valjundid[(m, p)].append({
                            "katkend_id": katkend["id"],
                            "peatuki_tyyp": katkend["peatuki_tyyp"],
                            "kategooria": ann["kategooria"],
                            "klassifikatsioon": "TP",
                            "kindlus_kuldist": ann["kindlus"],
                        })
                        detekteeritud_kuld_index.add(i)
                    else:
                        valjundid[(m, p)].append({
                            "katkend_id": katkend["id"],
                            "peatuki_tyyp": katkend["peatuki_tyyp"],
                            "kategooria": ann["kategooria"],
                            "klassifikatsioon": "FN",
                            "kindlus_kuldist": ann["kindlus"],
                        })

                # 2) Valepositiivsed (FP) iga kategooria kohta sõltumatult
                for kat in KATEGOORIAD:
                    if rng.random() < fp_profiil[kat]:
                        valjundid[(m, p)].append({
                            "katkend_id": katkend["id"],
                            "peatuki_tyyp": katkend["peatuki_tyyp"],
                            "kategooria": kat,
                            "klassifikatsioon": "FP",
                            "kindlus_kuldist": "—",
                        })

    return valjundid


# ---------------------------------------------------------------------------
# Mõõdikute arvutus
# ---------------------------------------------------------------------------


def arvuta_moodikud(valjundid) -> pd.DataFrame:
    read = []
    for (m, p), rikastatud in valjundid.items():
        for kat in KATEGOORIAD:
            tp = sum(1 for r in rikastatud if r["kategooria"] == kat and r["klassifikatsioon"] == "TP")
            fp = sum(1 for r in rikastatud if r["kategooria"] == kat and r["klassifikatsioon"] == "FP")
            fn = sum(1 for r in rikastatud if r["kategooria"] == kat and r["klassifikatsioon"] == "FN")
            tapsus = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            saagis = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            if (tapsus + saagis) > 0:
                f1 = 2 * tapsus * saagis / (tapsus + saagis)
            else:
                f1 = 0.0
            read.append({
                "mudel": m,
                "prompti_tyyp": p,
                "kategooria": kat,
                "TP": tp,
                "FP": fp,
                "FN": fn,
                "tapsus": round(tapsus, 3),
                "saagis": round(saagis, 3),
                "F1": round(f1, 3),
            })

    return pd.DataFrame(read)


def kokkuvote(moodikud: pd.DataFrame) -> pd.DataFrame:
    """Macro-keskmised iga (mudel × prompti tüüp) kombinatsiooni kohta."""
    read = []
    for (m, p), grupp in moodikud.groupby(["mudel", "prompti_tyyp"]):
        read.append({
            "mudel": m,
            "prompti_tyyp": p,
            "macro_tapsus": round(grupp["tapsus"].mean(), 3),
            "macro_saagis": round(grupp["saagis"].mean(), 3),
            "macro_F1": round(grupp["F1"].mean(), 3),
            "TP_kokku": int(grupp["TP"].sum()),
            "FP_kokku": int(grupp["FP"].sum()),
            "FN_kokku": int(grupp["FN"].sum()),
        })
    return pd.DataFrame(read)


# ---------------------------------------------------------------------------
# Graafikud
# ---------------------------------------------------------------------------


KATEGOORIA_VARV = {
    "STRUKTUUR": "#1f77b4",
    "AKADEEMILINE_STIIL": "#ff7f0e",
    "TERMINOLOOGIA": "#2ca02c",
    "VIITAMISVAJADUS": "#d62728",
}

MUDELI_VARV = {
    "claude-opus-4-7": "#7c3aed",
    "gpt-5.5": "#0ea5e9",
}

plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 110,
    "savefig.bbox": "tight",
})


def _vesimark_lisa(ax) -> None:
    ax.text(0.5, 0.5, "SÜNTEETILINE\nillustratsioon",
            transform=ax.transAxes,
            fontsize=42, color="gray", alpha=0.10,
            ha="center", va="center", rotation=30,
            zorder=10)


def _salvesta(nimi: str) -> None:
    rada = JOONISED / f"{nimi}.png"
    plt.savefig(rada)
    plt.close()
    print(f"  -> {rada.relative_to(JUUR.parent)}")


def joonis_F1_kategooriapohi(moodikud: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))
    laius = 0.20
    asukohad = list(range(len(KATEGOORIAD)))
    nihked = [-1.5 * laius, -0.5 * laius, 0.5 * laius, 1.5 * laius]

    for nihe, (m, p) in zip(
        nihked,
        [(m, p) for m in MUDELID for p in PROMPTID],
    ):
        v1_jada = [
            moodikud.query("mudel == @m and prompti_tyyp == @p and kategooria == @k")["F1"].iloc[0]
            for k in KATEGOORIAD
        ]
        silt = f"{m} • {p}"
        ax.bar([a + nihe for a in asukohad], v1_jada, laius, label=silt)

    ax.set_xticks(asukohad)
    ax.set_xticklabels(KATEGOORIAD, rotation=10)
    ax.set_ylabel("F₁-skoor")
    ax.set_ylim(0, 1)
    ax.set_title("Sünteetiline F₁ kategooria, mudeli ja prompti tüübi kaupa")
    ax.legend(fontsize=9, loc="upper right")
    _vesimark_lisa(ax)
    _salvesta("09_synth_F1_kategooriapohi")


def joonis_macro_F1(kokk: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    laius = 0.35
    mudelid = MUDELID
    asukohad = list(range(len(mudelid)))

    yld = [
        kokk.query("mudel == @m and prompti_tyyp == 'yldine'")["macro_F1"].iloc[0]
        for m in mudelid
    ]
    str_ = [
        kokk.query("mudel == @m and prompti_tyyp == 'struktureeritud'")["macro_F1"].iloc[0]
        for m in mudelid
    ]

    ax.bar([a - laius / 2 for a in asukohad], yld, laius, label="Üldine prompt", color="#94a3b8")
    ax.bar([a + laius / 2 for a in asukohad], str_, laius, label="Struktureeritud prompt", color="#22c55e")

    for x, (y_g, y_s) in enumerate(zip(yld, str_)):
        ax.text(x - laius / 2, y_g + 0.01, f"{y_g:.2f}", ha="center", fontsize=9)
        ax.text(x + laius / 2, y_s + 0.01, f"{y_s:.2f}", ha="center", fontsize=9, fontweight="bold")
        ax.text(x, max(y_g, y_s) + 0.05, f"+{(y_s - y_g):.2f}",
                ha="center", fontsize=9, color="#16a34a")

    ax.set_xticks(asukohad)
    ax.set_xticklabels(mudelid)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Macro F₁")
    ax.set_title("Sünteetiline macro F₁: üldine vs struktureeritud prompt")
    ax.legend(loc="upper left", fontsize=9)
    _vesimark_lisa(ax)
    _salvesta("10_synth_macro_F1")


def joonis_TP_FP_FN(moodikud: pd.DataFrame) -> None:
    fig, axid = plt.subplots(2, 2, figsize=(13, 8))
    axid = axid.flatten()

    kombinatsioonid = [(m, p) for m in MUDELID for p in PROMPTID]
    for ax, (m, p) in zip(axid, kombinatsioonid):
        all = moodikud.query("mudel == @m and prompti_tyyp == @p")
        x = list(all["kategooria"])
        tp = list(all["TP"])
        fp = list(all["FP"])
        fn = list(all["FN"])

        ax.bar(x, tp, label="TP", color="#22c55e")
        ax.bar(x, fp, bottom=tp, label="FP", color="#ef4444")
        ax.bar(x, fn, bottom=[a + b for a, b in zip(tp, fp)], label="FN", color="#94a3b8")
        ax.set_title(f"{m} • {p}", fontsize=11)
        ax.tick_params(axis="x", rotation=15, labelsize=8)
        ax.set_ylabel("Leidude arv")
        ax.legend(fontsize=8)
        _vesimark_lisa(ax)

    fig.suptitle("Sünteetiline TP / FP / FN jaotus kombinatsioonide kaupa", fontsize=14, y=1.00)
    fig.tight_layout()
    _salvesta("11_synth_TP_FP_FN")


def joonis_tapsus_saagis(moodikud: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9, 7))

    for (m, p), grupp in moodikud.groupby(["mudel", "prompti_tyyp"]):
        marker = "o" if p == "struktureeritud" else "s"
        for kat in KATEGOORIAD:
            rida = grupp[grupp["kategooria"] == kat].iloc[0]
            ax.scatter(rida["saagis"], rida["tapsus"],
                       color=MUDELI_VARV[m], marker=marker,
                       s=180, alpha=0.85, edgecolors="black", linewidths=1)
            ax.annotate(kat[:4], (rida["saagis"], rida["tapsus"]),
                        xytext=(7, 7), textcoords="offset points",
                        fontsize=8, color="#374151")

    # F1 isokõverad
    import numpy as np
    s_grid = np.linspace(0.01, 1, 100)
    for f in [0.4, 0.6, 0.8]:
        p_iso = (f * s_grid) / (2 * s_grid - f)
        kehtiv = (p_iso > 0) & (p_iso < 1)
        ax.plot(s_grid[kehtiv], p_iso[kehtiv], "--", color="#cbd5e1", linewidth=0.8)
        ax.text(0.95, (f * 0.95) / (2 * 0.95 - f) if (2 * 0.95 - f) > 0 else 0.95,
                f"F₁={f:.1f}", fontsize=8, color="#94a3b8")

    # Legend
    legendi_elemendid = [
        plt.scatter([], [], color=MUDELI_VARV["claude-opus-4-7"], s=120, edgecolors="black", label="Claude 4.7 Opus"),
        plt.scatter([], [], color=MUDELI_VARV["gpt-5.5"], s=120, edgecolors="black", label="GPT-5.5"),
        plt.scatter([], [], color="white", marker="o", s=120, edgecolors="black", label="Struktureeritud"),
        plt.scatter([], [], color="white", marker="s", s=120, edgecolors="black", label="Üldine"),
    ]
    ax.legend(handles=legendi_elemendid, fontsize=9, loc="lower right")

    ax.set_xlabel("Saagis (recall)")
    ax.set_ylabel("Täpsus (precision)")
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, 1.05)
    ax.set_title("Sünteetiline täpsus–saagis-graafik kategooriate ja mudelite kaupa\n(siltidena kategooria nime esimesed 4 tähemärki)")
    _vesimark_lisa(ax)
    _salvesta("12_synth_tapsus_saagis")


# ---------------------------------------------------------------------------
# Käivitus
# ---------------------------------------------------------------------------


def main() -> None:
    print("Simuleerin mudelite väljundid (seed = 20260512) ...")
    valjundid = simuleeri()

    # Salvesta detailne tabel
    with (ANDMED / "synth_mudelivastused.csv").open("w", encoding="utf-8", newline="") as f:
        kirjutaja = csv.writer(f)
        kirjutaja.writerow(["mudel", "prompti_tyyp", "katkend_id", "peatuki_tyyp",
                            "kategooria", "klassifikatsioon", "kindlus_kuldist"])
        for (m, p), rikastatud in valjundid.items():
            for r in rikastatud:
                kirjutaja.writerow([m, p, r["katkend_id"], r["peatuki_tyyp"],
                                    r["kategooria"], r["klassifikatsioon"],
                                    r["kindlus_kuldist"]])
    print(f"  -> andmed/synth_mudelivastused.csv")

    moodikud = arvuta_moodikud(valjundid)
    moodikud.to_csv(ANDMED / "synth_kategooriapohised_moodikud.csv", index=False, encoding="utf-8")
    print(f"  -> andmed/synth_kategooriapohised_moodikud.csv")

    kokk = kokkuvote(moodikud)
    kokk.to_csv(ANDMED / "synth_kokkuvote.csv", index=False, encoding="utf-8")
    print(f"  -> andmed/synth_kokkuvote.csv")

    print()
    print("Sünteetilised tulemused (macro-keskmised):")
    print(kokk.to_string(index=False))

    print()
    print("Joonistan graafikud ...")
    joonis_F1_kategooriapohi(moodikud)
    joonis_macro_F1(kokk)
    joonis_TP_FP_FN(moodikud)
    joonis_tapsus_saagis(moodikud)


if __name__ == "__main__":
    main()
