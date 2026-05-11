interface Props {
  avatud: boolean;
  onKinnita: () => void;
  onTuhista: () => void;
  mudel: string;
}

export default function PrivaatsusDialoog({
  avatud,
  onKinnita,
  onTuhista,
  mudel,
}: Props) {
  if (!avatud) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 p-6">
        <h2 className="text-lg font-semibold text-gray-900">
          Andmete edastamine välimisele teenusele
        </h2>
        <p className="mt-3 text-sm text-gray-700">
          Sisestatud tekst saadetakse mudelile <strong>{mudel}</strong>{" "}
          analüüsiks. See tähendab, et kolmas pool (Anthropic või OpenAI) saab
          teksti enda serveritesse.
        </p>
        <p className="mt-2 text-sm text-gray-700">
          Kui tekst sisaldab tundlikku infot (isikuandmed, salastatud sisu,
          kolmanda poole intellektuaalomand), <strong>ära jätka</strong>.
        </p>
        <p className="mt-2 text-sm text-gray-700">
          Süsteem ei salvesta sisestatud teksti kettal. Logitakse vaid
          anonüümseid mõõdikuid (leidude arv, kestus).
        </p>
        <div className="mt-6 flex justify-end gap-2">
          <button
            type="button"
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded"
            onClick={onTuhista}
          >
            Tühista
          </button>
          <button
            type="button"
            className="px-4 py-2 text-sm font-medium text-white bg-emerald-700 hover:bg-emerald-800 rounded"
            onClick={onKinnita}
          >
            Olen teadlik, jätka
          </button>
        </div>
      </div>
    </div>
  );
}
