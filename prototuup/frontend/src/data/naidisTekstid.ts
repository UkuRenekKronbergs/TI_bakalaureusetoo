import type { PeatykiTyyp } from "../types";

export const NAIDIS_TEKSTID: Record<PeatykiTyyp, string> = {
  sissejuhatus: [
    "1. Sissejuhatus",
    "1.1 Probleemi püstitus",
    "Tegelikult on tarkvaraarenduses asi see, et üle 75% arendajatest kasutab oma igapäevatöös mingisugust raamistikku. Mina arvan, et see on päris lahe trend. Käesolevas töös vaatlen, kuidas frameworkid ja raamistikud mõjutavad koodi kvaliteeti, kusjuures kasutan läbisegi termineid „lõim” ja „niit”, et lugejal oleks põnevam. Esimese hooga võiks öelda, et see kõik on selge, aga päris nii lihtne see pole.",
  ].join("\n"),
  taust: [
    "2. Taust",
    "Suurte keelemudelite ajalugu algas 2017. aastal, kui ilmus Transformer arhitektuur. Kõik teavad, et tänapäeval on need mudelid kõikjal. GPT-3 omas 175 miljardit parameetrit. Käesolevas töös vaatleme, kuidas neid LLM-e (large language model) saab kasutada kvaliteedikontrolliks, kusjuures kasutame nii sõna „LLM” kui „suur keelemudel” samas tähenduses.",
  ].join("\n"),
  metoodika: [
    "3. Metoodika",
    "3.1 Andmestik",
    "Andmete jaoks võtsin kokku 20 bakalaureusetööd ja siis ma analüüsisin neid. Iga töö puhul vaatasin, kas seal on probleeme ja siis kirjutasin üles. See protsess oli päris pikk, aga ma sain hakkama. Tegelikult oli see asi üsna lihtne, kuna kõik tööd olid ühesuguse struktuuriga ja kõik teavad, et see lihtsustab analüüsi.",
  ].join("\n"),
  tulemused: [
    "4. Tulemused",
    "4.1 Üldine pilt",
    "Tabel 4.1 näitab tulemusi.",
    "Tulemustest selgus, et süsteem leidis keskmiselt 6,3 probleemi peatüki kohta ning täpsus oli 87%. See on päris hea tulemus. Võrdluseks võib öelda, et inimene leiab keskmiselt sama palju. Süsteemi precision oli kõrge ning recall oli ka okei.",
  ].join("\n"),
  kokkuvote: [
    "5. Kokkuvõte",
    "Käesolevas töös sai uuritud, kuidas suuri keelemudeleid saab kasutada eestikeelse lõputöö kvaliteedikontrolliks. Tulemused näitavad, et asi töötab päris hästi. Tegelikult oli see üks lahe töö ja ma õppisin palju. Üle 90% katseisikutest leidis süsteemi kasulikuks. Edaspidi võiks teha veel asju, näiteks rohkem teste.",
  ].join("\n"),
};
