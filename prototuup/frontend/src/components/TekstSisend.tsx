interface Props {
  tekst: string;
  onChange: (uus: string) => void;
  disabled: boolean;
}

export default function TekstSisend({ tekst, onChange, disabled }: Props) {
  const sonadeArv = tekst.trim() ? tekst.trim().split(/\s+/).length : 0;
  return (
    <div>
      <label className="block">
        <span className="text-sm font-medium text-gray-700">
          Lõputöö peatüki tekst
        </span>
        <textarea
          className="mt-1 block w-full min-h-[20rem] rounded border border-gray-300 px-3 py-2 text-sm font-mono focus:border-emerald-500 focus:outline-none disabled:bg-gray-100"
          value={tekst}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Kleebi siia oma lõputöö peatükk (200–4000 sõna). Süsteem analüüsib ainult sisestatud teksti."
          disabled={disabled}
        />
      </label>
      <p className="mt-1 text-xs text-gray-500">
        Sõnu: {sonadeArv}. Märke: {tekst.length}.
      </p>
    </div>
  );
}
