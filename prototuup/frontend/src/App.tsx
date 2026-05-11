import { useCallback, useState } from "react";

import { ApiError, analyysi } from "./api/client";
import KonfPaneel from "./components/KonfPaneel";
import PrivaatsusDialoog from "./components/PrivaatsusDialoog";
import TagasisidePaneel from "./components/TagasisidePaneel";
import TekstSisend from "./components/TekstSisend";
import type {
  AnalyysiPaaring,
  AnalyysiVastus,
  Mudel,
  PeatykiTyyp,
  PromptiTyyp,
} from "./types";
import { MUDELI_NIMED } from "./types";

const PRIVAATSUS_VOTEM = "kvaliteedikontroll.privaatsus.kinnitatud";

export default function App() {
  const [tekst, setTekst] = useState("");
  const [peatykiTyyp, setPeatykiTyyp] = useState<PeatykiTyyp>("sissejuhatus");
  const [promptiTyyp, setPromptiTyyp] = useState<PromptiTyyp>("struktureeritud");
  const [mudel, setMudel] = useState<Mudel>("claude-3-5-sonnet-20241022");

  const [vastus, setVastus] = useState<AnalyysiVastus | null>(null);
  const [laadimine, setLaadimine] = useState(false);
  const [viga, setViga] = useState<string | null>(null);

  const [dialoogAvatud, setDialoogAvatud] = useState(false);

  const tekstiKehtivus = tekst.trim().length >= 50;

  const kaivitaAnalyys = useCallback(async () => {
    setLaadimine(true);
    setViga(null);
    setVastus(null);
    try {
      const paaring: AnalyysiPaaring = {
        tekst,
        peatuki_tyyp: peatykiTyyp,
        prompti_tyyp: promptiTyyp,
        mudel,
      };
      const v = await analyysi(paaring);
      setVastus(v);
    } catch (e) {
      if (e instanceof ApiError) {
        setViga(`Server tagastas vea (${e.status}): ${e.message}`);
      } else if (e instanceof Error) {
        setViga(e.message);
      } else {
        setViga("Tundmatu viga.");
      }
    } finally {
      setLaadimine(false);
    }
  }, [tekst, peatykiTyyp, promptiTyyp, mudel]);

  const onAnalyysiklikk = () => {
    if (!tekstiKehtivus || laadimine) return;
    const kinnitatud = localStorage.getItem(PRIVAATSUS_VOTEM) === "1";
    if (!kinnitatud) {
      setDialoogAvatud(true);
      return;
    }
    void kaivitaAnalyys();
  };

  const onPrivaatsusKinnita = () => {
    localStorage.setItem(PRIVAATSUS_VOTEM, "1");
    setDialoogAvatud(false);
    void kaivitaAnalyys();
  };

  const ekspordi = () => {
    if (!vastus) return;
    const blob = new Blob([JSON.stringify(vastus, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `tagasiside-${peatykiTyyp}-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-gray-200 bg-white">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-xl font-semibold text-gray-900">
            Eestikeelse lõputöö tagasisidesüsteem
          </h1>
          <p className="mt-1 text-sm text-gray-600">
            Tudengi enda kirjutatud teksti automaatne kvaliteedikontroll neljas
            kategoorias. <strong>Süsteem ei kirjuta lõputööd sinu eest.</strong>
          </p>
        </div>
      </header>

      <main className="flex-1">
        <div className="max-w-7xl mx-auto px-4 py-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
          <section className="space-y-4">
            <KonfPaneel
              peatykiTyyp={peatykiTyyp}
              promptiTyyp={promptiTyyp}
              mudel={mudel}
              onPeatykiTyypChange={setPeatykiTyyp}
              onPromptiTyypChange={setPromptiTyyp}
              onMudelChange={setMudel}
              disabled={laadimine}
            />

            <TekstSisend
              tekst={tekst}
              onChange={setTekst}
              disabled={laadimine}
            />

            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={onAnalyysiklikk}
                disabled={!tekstiKehtivus || laadimine}
                className="px-4 py-2 text-sm font-medium text-white bg-emerald-700 hover:bg-emerald-800 disabled:bg-gray-300 disabled:cursor-not-allowed rounded"
              >
                Analüüsi
              </button>
              <button
                type="button"
                onClick={ekspordi}
                disabled={!vastus}
                className="px-4 py-2 text-sm font-medium text-emerald-700 border border-emerald-700 hover:bg-emerald-50 disabled:text-gray-400 disabled:border-gray-300 disabled:cursor-not-allowed rounded"
              >
                Ekspordi JSON
              </button>
              {!tekstiKehtivus && (
                <span className="text-xs text-gray-500">
                  Vähemalt 50 tähemärki on vajalik analüüsi käivitamiseks.
                </span>
              )}
            </div>
          </section>

          <section>
            <TagasisidePaneel
              vastus={vastus}
              laadimine={laadimine}
              viga={viga}
            />
          </section>
        </div>
      </main>

      <footer className="border-t border-gray-200 bg-white">
        <div className="max-w-7xl mx-auto px-4 py-3 text-xs text-gray-500">
          Bakalaureusetöö prototüüp · Tartu Ülikooli arvutiteaduse instituut ·
          2026
        </div>
      </footer>

      <PrivaatsusDialoog
        avatud={dialoogAvatud}
        onKinnita={onPrivaatsusKinnita}
        onTuhista={() => setDialoogAvatud(false)}
        mudel={MUDELI_NIMED[mudel]}
      />
    </div>
  );
}
