"""Päris empiiriline hindamine — kutsub välja tegelikud LLM API-d.

Erinevus skriptist ``synteetiline_hindamine.py``: see skript saadab iga
katkendi tegelike Anthropici ja OpenAI API-de poole ning skoorib päris
mudelivastused autori käsitsi koostatud kuldstandardi vastu.

KÄSITSI KOOSTATUD osa:
  - 20 testkatkendit (``andmestik_synth.py`` — LLM-i abiga koostatud,
    eksplitsiitselt deklareeritud thesis ptk 1 deklaratsioonis)
  - 42 kuldstandardi annotatsiooni (samas failis)

PÄRIS MÕÕDETUD osa:
  - Mudelite väljundid: tegelikud API-päringud Anthropici Claude-le ja
    OpenAI GPT-le
  - TP/FP/FN klassifikatsioon: arvutatud span-tasemel kattuvuse põhjal
    (50% sõnatasemel + sama kategooria, vt thesis ptk 3.5)

Kasutamine:
  python paris_hindamine.py                   # täielik käivitus (~$3-5)
  python paris_hindamine.py --kuiv 1          # dry-run 1 katkendi peal
  python paris_hindamine.py --mudelid claude  # ainult Claude (~$2)
  python paris_hindamine.py --ainult-skoori   # ära tee uusi API-päringuid;
                                              # skoori olemasolevad vastused

Iga API-päringu täielik toores vastus salvestatakse failisüsteemi
(``andmed/paris_vastused/{mudel}__{prompt}__{katkend_id}.json``), nii et
skripti uuesti käivitamine on resumable — kui mõni katkend on juba
töödeldud, siis seda uuesti välja ei kutsuta.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

# Paneme prototüübi backend sys.path-i, et saaksime analyysi() funktsiooni importida
JUUR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(JUUR / "prototuup" / "backend"))

# Laeb .env keskkonnamuutujad enne kui pakkujad importitakse
from dotenv import load_dotenv

load_dotenv(JUUR / "prototuup" / ".env", override=True)

from andmestik_synth import KATEGOORIAD, TESTKOGU  # noqa: E402

from analyysija import AnalyysiViga, analyysi  # noqa: E402
from models import (  # noqa: E402
    AnalyysiPaaring,
    Mudel,
    PeatykiTyyp,
    PromptiTyyp,
)

STATISTIKA = Path(__file__).resolve().parent
ANDMED = STATISTIKA / "andmed"
VASTUSED = ANDMED / "paris_vastused"
JOONISED = STATISTIKA / "joonised_png"
VASTUSED.mkdir(parents=True, exist_ok=True)
JOONISED.mkdir(parents=True, exist_ok=True)

MUDELID = [Mudel.CLAUDE_OPUS_4_7, Mudel.GPT_5_5]
PROMPTID = [PromptiTyyp.YLDINE, PromptiTyyp.STRUKTUREERITUD]


# ---------------------------------------------------------------------------
# Päringute teostus
# ---------------------------------------------------------------------------


def vastuse_fail(mudel: str, prompt: str, katkend_id: str) -> Path:
    return VASTUSED / f"{mudel}__{prompt}__{katkend_id}.json"


def kutsu_api(katkend: dict, mudel: Mudel, prompt: PromptiTyyp) -> dict | None:
    """Tagastab JSON-na salvestatava dict-i või None, kui kõik katsed ebaõnnestusid."""
    paaring = AnalyysiPaaring(
        tekst=katkend["tekst"],
        peatuki_tyyp=PeatykiTyyp(katkend["peatuki_tyyp"]),
        prompti_tyyp=prompt,
        mudel=mudel,
    )
    try:
        vastus = analyysi(paaring)
    except AnalyysiViga as e:
        return {
            "viga": str(e),
            "katkend_id": katkend["id"],
            "mudel": mudel.value,
            "prompti_tyyp": prompt.value,
        }
    return {
        "katkend_id": katkend["id"],
        "mudel": mudel.value,
        "prompti_tyyp": prompt.value,
        "kestus_ms": vastus.meta.paaringu_kestus_ms,
        "leiud": [
            {
                "kategooria": leid.kategooria.value,
                "tsitaat": leid.tsitaat,
                "probleem": leid.probleem,
                "põhjendus": leid.pohjendus,
                "soovitus": leid.soovitus,
                "kindlus": leid.kindlus.value,
            }
            for leid in vastus.leiud
        ],
    }


def kogu_paris_vastused(piir_katkendeid: int | None, ainult_mudelid: list[Mudel] | None) -> int:
    mudelid = ainult_mudelid or MUDELID
    katkendid = TESTKOGU if piir_katkendeid is None else TESTKOGU[:piir_katkendeid]
    kokku = len(katkendid) * len(PROMPTID) * len(mudelid)
    tehtud = 0
    vahele_jäetud = 0

    print(f"Plaanitud: {kokku} päringut ({len(katkendid)} katkendit × {len(PROMPTID)} prompti × {len(mudelid)} mudelit)")
    print()
    algus_aeg = time.monotonic()

    for k_i, katkend in enumerate(katkendid, 1):
        for m in mudelid:
            for p in PROMPTID:
                tehtud += 1
                rada = vastuse_fail(m.value, p.value, katkend["id"])
                if rada.exists():
                    # Resumable: ära kutsu uuesti
                    olemas = json.loads(rada.read_text(encoding="utf-8"))
                    if "viga" not in olemas:
                        vahele_jäetud += 1
                        continue

                print(f"[{tehtud}/{kokku}] {katkend['id']} • {m.value} • {p.value} ... ", end="", flush=True)
                t0 = time.monotonic()
                tulemus = kutsu_api(katkend, m, p)
                kestus = time.monotonic() - t0
                if tulemus and "viga" not in tulemus:
                    leide = len(tulemus["leiud"])
                    print(f"{leide} leidu, {kestus:.1f}s")
                else:
                    print(f"VIGA: {tulemus.get('viga', '?')[:80]}")
                rada.write_text(json.dumps(tulemus, ensure_ascii=False, indent=2), encoding="utf-8")

    total = time.monotonic() - algus_aeg
    print()
    print(f"Valmis. Uusi päringuid: {kokku - vahele_jäetud}, vahelejäetud: {vahele_jäetud}, aeg: {total:.1f}s")
    return kokku - vahele_jäetud


# ---------------------------------------------------------------------------
# Skoorimine — TP/FP/FN arvutus
# ---------------------------------------------------------------------------


def _normaliseeri(s: str) -> list[str]:
    """Normaliseeri sõna-tasemel võrdluseks: väiketähed, ainult sõnamärgid."""
    import re
    return re.findall(r"\w+", s.lower())


def span_kattub(mudeli_tsitaat: str, gold_span: str, lavi: float = 0.5) -> bool:
    """Tagastab True, kui kahe spani sõnatasemel kattuvus on ≥ ``lavi``.

    Kattuvuse mõõdik: ühiste sõnade hulk jagatud lühema spani sõnade arvuga
    (assümeetriline, kuna pikem span võib sisaldada ka muud konteksti).
    """
    m = set(_normaliseeri(mudeli_tsitaat))
    g = set(_normaliseeri(gold_span))
    if not m or not g:
        return False
    ühised = m & g
    väiksem = min(len(m), len(g))
    return len(ühised) / väiksem >= lavi


def skoori_uks_katkend(mudeli_leiud: list[dict], kuldstandard: list[dict]) -> list[dict]:
    """Tagastab klassifikatsiooni-kirjete loendi (TP/FP/FN) ühe katkendi kohta."""
    kirjed = []
    detekteeritud_gold = set()

    # Iga mudeli leid: kas TP (kattub mõne golddiga) või FP
    for leid in mudeli_leiud:
        leitud_match = -1
        for gi, gold in enumerate(kuldstandard):
            if gi in detekteeritud_gold:
                continue
            if leid["kategooria"] != gold["kategooria"]:
                continue
            if span_kattub(leid.get("tsitaat", ""), gold["span"]):
                leitud_match = gi
                break
        if leitud_match >= 0:
            detekteeritud_gold.add(leitud_match)
            kirjed.append({
                "kategooria": leid["kategooria"],
                "klassifikatsioon": "TP",
                "mudeli_kindlus": leid.get("kindlus", "—"),
                "gold_kindlus": kuldstandard[leitud_match]["kindlus"],
            })
        else:
            kirjed.append({
                "kategooria": leid["kategooria"],
                "klassifikatsioon": "FP",
                "mudeli_kindlus": leid.get("kindlus", "—"),
                "gold_kindlus": "—",
            })

    # Iga gold, mida ei detekteeritud → FN
    for gi, gold in enumerate(kuldstandard):
        if gi not in detekteeritud_gold:
            kirjed.append({
                "kategooria": gold["kategooria"],
                "klassifikatsioon": "FN",
                "mudeli_kindlus": "—",
                "gold_kindlus": gold["kindlus"],
            })

    return kirjed


def kogu_kõik_kirjed() -> dict[tuple[str, str], list[dict]]:
    """Skoorib kõik salvestatud vastused gold-i vastu."""
    tulemused: dict[tuple[str, str], list[dict]] = {
        (m.value, p.value): [] for m in MUDELID for p in PROMPTID
    }
    for katkend in TESTKOGU:
        for m in MUDELID:
            for p in PROMPTID:
                rada = vastuse_fail(m.value, p.value, katkend["id"])
                if not rada.exists():
                    continue
                vastus = json.loads(rada.read_text(encoding="utf-8"))
                if "viga" in vastus:
                    continue
                kirjed = skoori_uks_katkend(vastus["leiud"], katkend["kuldstandard"])
                for k in kirjed:
                    k["katkend_id"] = katkend["id"]
                    k["peatuki_tyyp"] = katkend["peatuki_tyyp"]
                tulemused[(m.value, p.value)].extend(kirjed)
    return tulemused


# ---------------------------------------------------------------------------
# Mõõdikud + kirjutamine
# ---------------------------------------------------------------------------


def arvuta_moodikud_csv(tulemused: dict[tuple[str, str], list[dict]]) -> None:
    import pandas as pd
    read = []
    for (m, p), kirjed in tulemused.items():
        for kat in KATEGOORIAD:
            tp = sum(1 for r in kirjed if r["kategooria"] == kat and r["klassifikatsioon"] == "TP")
            fp = sum(1 for r in kirjed if r["kategooria"] == kat and r["klassifikatsioon"] == "FP")
            fn = sum(1 for r in kirjed if r["kategooria"] == kat and r["klassifikatsioon"] == "FN")
            T = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            S = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            F1 = 2 * T * S / (T + S) if (T + S) > 0 else 0.0
            read.append({
                "mudel": m, "prompti_tyyp": p, "kategooria": kat,
                "TP": tp, "FP": fp, "FN": fn,
                "tapsus": round(T, 3), "saagis": round(S, 3), "F1": round(F1, 3),
            })

    df = pd.DataFrame(read)
    df.to_csv(ANDMED / "paris_kategooriapohised_moodikud.csv", index=False, encoding="utf-8")

    # Macro-keskmised
    kokk = []
    for (m, p), g in df.groupby(["mudel", "prompti_tyyp"]):
        kokk.append({
            "mudel": m, "prompti_tyyp": p,
            "macro_tapsus": round(g["tapsus"].mean(), 3),
            "macro_saagis": round(g["saagis"].mean(), 3),
            "macro_F1": round(g["F1"].mean(), 3),
            "TP_kokku": int(g["TP"].sum()),
            "FP_kokku": int(g["FP"].sum()),
            "FN_kokku": int(g["FN"].sum()),
        })
    kokk_df = pd.DataFrame(kokk)
    kokk_df.to_csv(ANDMED / "paris_kokkuvote.csv", index=False, encoding="utf-8")
    print()
    print("PÄRIS empiirilised tulemused:")
    print(kokk_df.to_string(index=False))


# ---------------------------------------------------------------------------
# Graafikud
# ---------------------------------------------------------------------------


def joonista() -> None:
    import matplotlib.pyplot as plt
    import pandas as pd

    plt.rcParams.update({
        "font.size": 11,
        "axes.titlesize": 12,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.dpi": 110,
        "savefig.bbox": "tight",
    })

    df = pd.read_csv(ANDMED / "paris_kategooriapohised_moodikud.csv")
    kokk = pd.read_csv(ANDMED / "paris_kokkuvote.csv")

    # 1) Macro F1 võrdlus
    fig, ax = plt.subplots(figsize=(9, 5))
    laius = 0.35
    mudelid = sorted(kokk["mudel"].unique())
    asukohad = list(range(len(mudelid)))
    yld = [kokk.query("mudel == @m and prompti_tyyp == 'yldine'")["macro_F1"].iloc[0] for m in mudelid]
    str_ = [kokk.query("mudel == @m and prompti_tyyp == 'struktureeritud'")["macro_F1"].iloc[0] for m in mudelid]
    ax.bar([a - laius/2 for a in asukohad], yld, laius, label="Üldine prompt", color="#94a3b8")
    ax.bar([a + laius/2 for a in asukohad], str_, laius, label="Struktureeritud prompt", color="#22c55e")
    for x, (yg, ys) in enumerate(zip(yld, str_)):
        ax.text(x - laius/2, yg + 0.01, f"{yg:.2f}", ha="center", fontsize=9)
        ax.text(x + laius/2, ys + 0.01, f"{ys:.2f}", ha="center", fontsize=9, fontweight="bold")
        ax.text(x, max(yg, ys) + 0.05, f"+{(ys - yg):.2f}", ha="center", fontsize=9, color="#16a34a")
    ax.set_xticks(asukohad)
    ax.set_xticklabels(mudelid)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Macro F₁ (päris)")
    ax.set_title("Päris empiiriline macro F₁: üldine vs struktureeritud prompt")
    ax.legend(fontsize=9)
    plt.savefig(JOONISED / "13_paris_macro_F1.png")
    plt.close()
    print("  -> 13_paris_macro_F1.png")

    # 2) F1 kategooria kaupa
    fig, ax = plt.subplots(figsize=(12, 6))
    laius = 0.20
    asukohad = list(range(len(KATEGOORIAD)))
    nihked = [-1.5*laius, -0.5*laius, 0.5*laius, 1.5*laius]
    for nihe, (m, p) in zip(nihked, [(m, p) for m in mudelid for p in ["yldine", "struktureeritud"]]):
        v = [df.query("mudel == @m and prompti_tyyp == @p and kategooria == @k")["F1"].iloc[0] for k in KATEGOORIAD]
        ax.bar([a + nihe for a in asukohad], v, laius, label=f"{m} • {p}")
    ax.set_xticks(asukohad)
    ax.set_xticklabels(KATEGOORIAD, rotation=10)
    ax.set_ylabel("F₁")
    ax.set_ylim(0, 1)
    ax.set_title("Päris empiiriline F₁ kategooria, mudeli ja prompti tüübi kaupa")
    ax.legend(fontsize=9)
    plt.savefig(JOONISED / "14_paris_F1_kategooriapohi.png")
    plt.close()
    print("  -> 14_paris_F1_kategooriapohi.png")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    par = argparse.ArgumentParser()
    par.add_argument("--kuiv", type=int, default=None,
                     help="Ainult N esimest katkendit (dry-run)")
    par.add_argument("--mudelid", choices=["claude", "gpt", "kõik"], default="kõik",
                     help="Millised mudelid kasutada")
    par.add_argument("--ainult-skoori", action="store_true",
                     help="Ära tee uusi API-päringuid; skoori olemasolevad")
    args = par.parse_args()

    if args.mudelid == "claude":
        ainult = [Mudel.CLAUDE_OPUS_4_7]
    elif args.mudelid == "gpt":
        ainult = [Mudel.GPT_5_5]
    else:
        ainult = None

    if not args.ainult_skoori:
        kogu_paris_vastused(args.kuiv, ainult)

    print()
    print("Skoorin vastused gold-standardi vastu...")
    tulemused = kogu_kõik_kirjed()
    arvuta_moodikud_csv(tulemused)

    # Detailne kirjete fail
    import csv
    with (ANDMED / "paris_klassifikatsioonid.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["mudel", "prompti_tyyp", "katkend_id", "peatuki_tyyp", "kategooria",
                    "klassifikatsioon", "mudeli_kindlus", "gold_kindlus"])
        for (m, p), kirjed in tulemused.items():
            for k in kirjed:
                w.writerow([m, p, k["katkend_id"], k["peatuki_tyyp"], k["kategooria"],
                            k["klassifikatsioon"], k["mudeli_kindlus"], k["gold_kindlus"]])
    print(f"  -> andmed/paris_klassifikatsioonid.csv")

    print()
    print("Joonistan graafikud...")
    joonista()


if __name__ == "__main__":
    main()
