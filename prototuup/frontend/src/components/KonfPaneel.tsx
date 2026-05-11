import type {
  Mudel,
  PeatykiTyyp,
  PromptiTyyp,
} from "../types";
import {
  MUDELI_NIMED,
  PEATYKI_NIMED,
  PROMPTI_NIMED,
} from "../types";

interface Props {
  peatykiTyyp: PeatykiTyyp;
  promptiTyyp: PromptiTyyp;
  mudel: Mudel;
  onPeatykiTyypChange: (v: PeatykiTyyp) => void;
  onPromptiTyypChange: (v: PromptiTyyp) => void;
  onMudelChange: (v: Mudel) => void;
  disabled: boolean;
}

export default function KonfPaneel({
  peatykiTyyp,
  promptiTyyp,
  mudel,
  onPeatykiTyypChange,
  onPromptiTyypChange,
  onMudelChange,
  disabled,
}: Props) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
      <label className="block">
        <span className="text-sm font-medium text-gray-700">Peatüki tüüp</span>
        <select
          className="mt-1 block w-full rounded border border-gray-300 px-2 py-1.5 text-sm focus:border-emerald-500 focus:outline-none disabled:bg-gray-100"
          value={peatykiTyyp}
          onChange={(e) => onPeatykiTyypChange(e.target.value as PeatykiTyyp)}
          disabled={disabled}
        >
          {(Object.keys(PEATYKI_NIMED) as PeatykiTyyp[]).map((k) => (
            <option key={k} value={k}>
              {PEATYKI_NIMED[k]}
            </option>
          ))}
        </select>
      </label>

      <label className="block">
        <span className="text-sm font-medium text-gray-700">Prompti tüüp</span>
        <select
          className="mt-1 block w-full rounded border border-gray-300 px-2 py-1.5 text-sm focus:border-emerald-500 focus:outline-none disabled:bg-gray-100"
          value={promptiTyyp}
          onChange={(e) => onPromptiTyypChange(e.target.value as PromptiTyyp)}
          disabled={disabled}
        >
          {(Object.keys(PROMPTI_NIMED) as PromptiTyyp[]).map((k) => (
            <option key={k} value={k}>
              {PROMPTI_NIMED[k]}
            </option>
          ))}
        </select>
      </label>

      <label className="block">
        <span className="text-sm font-medium text-gray-700">Mudel</span>
        <select
          className="mt-1 block w-full rounded border border-gray-300 px-2 py-1.5 text-sm focus:border-emerald-500 focus:outline-none disabled:bg-gray-100"
          value={mudel}
          onChange={(e) => onMudelChange(e.target.value as Mudel)}
          disabled={disabled}
        >
          {(Object.keys(MUDELI_NIMED) as Mudel[]).map((k) => (
            <option key={k} value={k}>
              {MUDELI_NIMED[k]}
            </option>
          ))}
        </select>
      </label>
    </div>
  );
}
