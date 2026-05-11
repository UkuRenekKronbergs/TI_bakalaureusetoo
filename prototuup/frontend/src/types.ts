export type Kategooria =
  | "STRUKTUUR"
  | "AKADEEMILINE_STIIL"
  | "TERMINOLOOGIA"
  | "VIITAMISVAJADUS"
  | "MUU";

export type Kindlus = "kõrge" | "keskmine" | "madal";

export type PeatykiTyyp =
  | "sissejuhatus"
  | "taust"
  | "metoodika"
  | "tulemused"
  | "kokkuvote";

export type PromptiTyyp = "yldine" | "struktureeritud";

export type Mudel = "claude-opus-4-7" | "gpt-5";

export interface Leid {
  kategooria: Kategooria;
  tsitaat: string;
  probleem: string;
  põhjendus: string;
  soovitus: string;
  kindlus: Kindlus;
}

export interface AnalyysiMeta {
  mudel: string;
  prompti_tyyp: string;
  peatuki_tyyp: string;
  leidude_arv_kategooriate_kaupa: Record<string, number>;
  paaringu_kestus_ms: number;
}

export interface AnalyysiVastus {
  leiud: Leid[];
  meta: AnalyysiMeta;
}

export interface AnalyysiPaaring {
  tekst: string;
  peatuki_tyyp: PeatykiTyyp;
  prompti_tyyp: PromptiTyyp;
  mudel: Mudel;
}

export const KATEGOORIA_NIMED: Record<Kategooria, string> = {
  STRUKTUUR: "Struktuur",
  AKADEEMILINE_STIIL: "Akadeemiline stiil",
  TERMINOLOOGIA: "Terminoloogia",
  VIITAMISVAJADUS: "Viitamisvajadus",
  MUU: "Muu",
};

export const PEATYKI_NIMED: Record<PeatykiTyyp, string> = {
  sissejuhatus: "Sissejuhatus",
  taust: "Taust ja seotud tööd",
  metoodika: "Metoodika",
  tulemused: "Tulemused",
  kokkuvote: "Kokkuvõte",
};

export const PROMPTI_NIMED: Record<PromptiTyyp, string> = {
  yldine: "Üldine prompt",
  struktureeritud: "Struktureeritud prompt",
};

export const MUDELI_NIMED: Record<Mudel, string> = {
  "claude-opus-4-7": "Claude 4.7 Opus",
  "gpt-5": "GPT-5",
};
