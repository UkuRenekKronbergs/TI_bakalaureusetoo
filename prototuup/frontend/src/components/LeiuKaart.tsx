import type { Kindlus, Leid } from "../types";

interface Props {
  leid: Leid;
}

const KINDLUSE_STIIL: Record<Kindlus, { silt: string; klass: string }> = {
  kõrge: {
    silt: "Kõrge kindlus",
    klass: "bg-emerald-100 text-emerald-900 border-emerald-300",
  },
  keskmine: {
    silt: "Keskmine kindlus",
    klass: "bg-amber-100 text-amber-900 border-amber-300",
  },
  madal: {
    silt: "Madal kindlus",
    klass: "bg-gray-100 text-gray-700 border-gray-300",
  },
};

export default function LeiuKaart({ leid }: Props) {
  const stiil = KINDLUSE_STIIL[leid.kindlus];
  return (
    <article className="border border-gray-200 rounded-lg bg-white shadow-sm p-4">
      <div className="flex items-start justify-between gap-3">
        <h4 className="text-sm font-semibold text-gray-900">
          {leid.probleem}
        </h4>
        <span
          className={`text-xs font-medium px-2 py-0.5 rounded border ${stiil.klass}`}
        >
          {stiil.silt}
        </span>
      </div>
      <blockquote className="mt-2 border-l-4 border-amber-400 bg-amber-50 px-3 py-2 text-sm text-gray-800 italic">
        „{leid.tsitaat}”
      </blockquote>
      <dl className="mt-3 text-sm space-y-2">
        <div>
          <dt className="font-medium text-gray-700 inline">Põhjendus: </dt>
          <dd className="inline text-gray-700">{leid.põhjendus}</dd>
        </div>
        <div>
          <dt className="font-medium text-gray-700 inline">Soovitus: </dt>
          <dd className="inline text-gray-700">{leid.soovitus}</dd>
        </div>
      </dl>
    </article>
  );
}
