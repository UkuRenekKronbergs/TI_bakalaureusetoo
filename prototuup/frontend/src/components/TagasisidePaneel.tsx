import { useState } from "react";

import type { AnalyysiVastus, Kategooria, Leid } from "../types";
import { KATEGOORIA_NIMED } from "../types";
import LeiuKaart from "./LeiuKaart";

interface Props {
  vastus: AnalyysiVastus | null;
  laadimine: boolean;
  viga: string | null;
}

const KATEGOORIA_JARJEKORD: Kategooria[] = [
  "STRUKTUUR",
  "AKADEEMILINE_STIIL",
  "TERMINOLOOGIA",
  "VIITAMISVAJADUS",
  "MUU",
];

function rühmita(leiud: Leid[]): Record<Kategooria, Leid[]> {
  const tulem: Record<Kategooria, Leid[]> = {
    STRUKTUUR: [],
    AKADEEMILINE_STIIL: [],
    TERMINOLOOGIA: [],
    VIITAMISVAJADUS: [],
    MUU: [],
  };
  leiud.forEach((l) => tulem[l.kategooria].push(l));
  return tulem;
}

export default function TagasisidePaneel({
  vastus,
  laadimine,
  viga,
}: Props) {
  const [avatudKategooriad, setAvatudKategooriad] = useState<
    Record<Kategooria, boolean>
  >({
    STRUKTUUR: true,
    AKADEEMILINE_STIIL: true,
    TERMINOLOOGIA: true,
    VIITAMISVAJADUS: true,
    MUU: true,
  });

  if (laadimine) {
    return (
      <div className="rounded border border-gray-200 bg-white p-6 text-center text-gray-600">
        <div className="inline-block h-5 w-5 animate-spin rounded-full border-2 border-emerald-600 border-t-transparent" />
        <p className="mt-3 text-sm">Mudel analüüsib teksti…</p>
      </div>
    );
  }

  if (viga) {
    return (
      <div className="rounded border border-red-200 bg-red-50 p-4 text-sm text-red-800">
        <p className="font-medium">Analüüs ebaõnnestus.</p>
        <p className="mt-1">{viga}</p>
      </div>
    );
  }

  if (!vastus) {
    return (
      <div className="rounded border border-dashed border-gray-300 bg-white p-6 text-center text-sm text-gray-500">
        Sisesta peatüki tekst ja vajuta <em>Analüüsi</em>, et kuvatakse
        kategoriseeritud tagasiside.
      </div>
    );
  }

  const ryhmad = rühmita(vastus.leiud);

  return (
    <div className="space-y-3">
      <div className="rounded border border-amber-300 bg-amber-50 p-3 text-xs text-amber-900">
        <strong>Meelespea:</strong> see süsteem annab soovituslikku tagasisidet
        sinu enda kirjutatud tekstile. See ei kirjuta lõputööd sinu eest. Kontrolli
        iga soovitust ja sõnasta vajadusel ümber.
      </div>

      <div className="rounded border border-gray-200 bg-white px-3 py-2 text-xs text-gray-600">
        Mudel: <strong>{vastus.meta.mudel}</strong> · Prompt:{" "}
        <strong>{vastus.meta.prompti_tyyp}</strong> · Kestus:{" "}
        {(vastus.meta.paaringu_kestus_ms / 1000).toFixed(1)} s · Leide kokku:{" "}
        <strong>{vastus.leiud.length}</strong>
      </div>

      {KATEGOORIA_JARJEKORD.map((k) => {
        const ssrysm = ryhmad[k];
        if (ssrysm.length === 0) return null;
        const avatud = avatudKategooriad[k];
        return (
          <section
            key={k}
            className="rounded border border-gray-200 bg-white"
          >
            <button
              type="button"
              onClick={() =>
                setAvatudKategooriad((prev) => ({ ...prev, [k]: !prev[k] }))
              }
              className="flex w-full items-center justify-between px-4 py-3 text-left text-sm font-semibold text-gray-900 hover:bg-gray-50"
              aria-expanded={avatud}
            >
              <span>
                {KATEGOORIA_NIMED[k]}{" "}
                <span className="ml-2 text-xs font-normal text-gray-500">
                  ({ssrysm.length})
                </span>
              </span>
              <span aria-hidden>{avatud ? "▾" : "▸"}</span>
            </button>
            {avatud && (
              <div className="border-t border-gray-100 p-3 space-y-3">
                {ssrysm.map((leid, i) => (
                  <LeiuKaart key={i} leid={leid} />
                ))}
              </div>
            )}
          </section>
        );
      })}
    </div>
  );
}
