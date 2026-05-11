"""Loob hindamise tulpdiagrammid placeholder-numbritest.

Kasuta seda skripti pärast tegeliku katse läbiviimist, asendades all olevad
loendid päris tulemustega ning käivitades:

    python _loo_joonised.py

Skript kirjutab samasse kausta:
- Joonis-F1-Kategooriate.png  (üldine vs struktureeritud)
- Joonis-F1-Paranemine.png    (struktureeritud miinus üldine)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

KAUST = Path(__file__).parent

KATEGOORIAD = [
    "Struktuur",
    "Akadeemiline\nstiil",
    "Terminoloogia",
    "Viitamis-\nvajadus",
]

# Tabelist 5-hindamine.tex tab:tulemused-mootmed
F1_YLDINE = [0.40, 0.48, 0.28, 0.54]
F1_STRUKT = [0.75, 0.65, 0.43, 0.77]


def joonis_f1_kategooriate() -> None:
    x = np.arange(len(KATEGOORIAD))
    laius = 0.36

    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    ax.bar(x - laius / 2, F1_YLDINE, laius, label="Üldine prompt",
           color="#9ca3af", edgecolor="black", linewidth=0.5)
    ax.bar(x + laius / 2, F1_STRUKT, laius, label="Struktureeritud prompt",
           color="#15803d", edgecolor="black", linewidth=0.5)

    ax.set_ylabel("F$_1$-skoor", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(KATEGOORIAD, fontsize=10)
    ax.set_ylim(0, 1.0)
    ax.set_yticks(np.arange(0, 1.01, 0.2))
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    ax.legend(loc="upper right", frameon=False, fontsize=10)

    for i, (u, s) in enumerate(zip(F1_YLDINE, F1_STRUKT)):
        ax.text(i - laius / 2, u + 0.015, f"{u:.2f}", ha="center", fontsize=8)
        ax.text(i + laius / 2, s + 0.015, f"{s:.2f}", ha="center", fontsize=8)

    fig.tight_layout()
    fig.savefig(KAUST / "Joonis-F1-Kategooriate.png", dpi=160)
    plt.close(fig)


def joonis_f1_paranemine() -> None:
    paranemine = [s - u for u, s in zip(F1_YLDINE, F1_STRUKT)]
    x = np.arange(len(KATEGOORIAD))

    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    pulgad = ax.bar(x, paranemine, color="#15803d", edgecolor="black",
                    linewidth=0.5, width=0.55)

    ax.set_ylabel(r"$\Delta$ F$_1$ (struktureeritud $-$ üldine)", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(KATEGOORIAD, fontsize=10)
    ax.set_ylim(0, max(paranemine) + 0.10)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    ax.axhline(0, color="black", linewidth=0.6)

    for pulk, v in zip(pulgad, paranemine):
        ax.text(pulk.get_x() + pulk.get_width() / 2, v + 0.01,
                f"+{v:.2f}", ha="center", fontsize=9)

    fig.tight_layout()
    fig.savefig(KAUST / "Joonis-F1-Paranemine.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    joonis_f1_kategooriate()
    joonis_f1_paranemine()
    print("Joonised loodud:", KAUST)
