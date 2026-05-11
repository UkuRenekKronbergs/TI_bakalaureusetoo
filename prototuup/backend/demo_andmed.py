"""Demo-režiimi salvestatud vastused ja näidistekstid.

Need on käsitsi koostatud (ja varem LLM-iga genereeritud) näidisvastused,
mis vastavad altpoolt leitavatele näidistekstidele. Vastust kasutatakse,
kui valitud mudeliks on "demo" — selleks ei lähe ühtegi võrgupäringut välja.
"""

from __future__ import annotations

import json
from typing import Any


# Iga peatüki tüübi jaoks on käsitsi koostatud näidistekst, millesse on
# tahtlikult sisse jäetud kõikidesse neljasse kategooriasse mahtuvaid vigu,
# ning vastav käsitsi koostatud "leidude" loend. Demo-režiimis tagastab
# pakkuja täpselt selle, sõltumata sellest, mida kasutaja tegelikult sisestab.
NAIDIS: dict[str, dict[str, Any]] = {
    "sissejuhatus": {
        "tekst": (
            "1. Sissejuhatus\n"
            "1.1 Probleemi püstitus\n"
            "Tegelikult on tarkvaraarenduses asi see, et üle 75% arendajatest "
            "kasutab oma igapäevatöös mingisugust raamistikku. Mina arvan, et "
            "see on päris lahe trend. Käesolevas töös vaatlen, kuidas frameworkid "
            "ja raamistikud mõjutavad koodi kvaliteeti, kusjuures kasutan läbisegi "
            "termineid „lõim” ja „niit”, et lugejal oleks põnevam. Esimese hooga "
            "võiks öelda, et see kõik on selge, aga päris nii lihtne see pole.\n"
        ),
        "leiud": [
            {
                "kategooria": "STRUKTUUR",
                "tsitaat": "1. Sissejuhatus\n1.1 Probleemi püstitus\nTegelikult on tarkvaraarenduses…",
                "probleem": "Peatükk algab kohe alapealkirjaga ilma sissejuhatava lõiguta.",
                "põhjendus": "Lugeja saab peatüki sisust parema ülevaate, kui pealkirja ja esimese alampealkirja vahel on lühike sissejuhatav lõik.",
                "soovitus": "Lisa 1. peatüki ja 1.1 vahele 3–4 lauseline sissejuhatav lõik, mis tutvustab peatüki ülesehitust.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "tsitaat": "Tegelikult on tarkvaraarenduses asi see, et …",
                "probleem": "Kõnekeelsed sõnad „tegelikult”, „asi see, et”.",
                "põhjendus": "Akadeemilises tekstis välditakse täitesõnu ja kõnekeelt; need ei lisa infot.",
                "soovitus": "Sõnasta lause umbisikulises kõneviisis ja eemalda täitesõnad.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "tsitaat": "Mina arvan, et see on päris lahe trend.",
                "probleem": "Mina-vorm ja kõnekeelne hinnang („päris lahe”).",
                "põhjendus": "Bakalaureusetöös välditakse mina-vormi ja subjektiivseid hinnanguid ilma toetava allikata.",
                "soovitus": "Asenda umbisikulise vormiga ja toeta hinnang allikaga või eemalda see.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "TERMINOLOOGIA",
                "tsitaat": "kasutan läbisegi termineid „lõim” ja „niit”",
                "probleem": "Sama mõiste tähistamiseks kasutatakse kahte erinevat terminit.",
                "põhjendus": "Lugeja jaoks tekib segadus, kas tegu on sama või erineva mõistega.",
                "soovitus": "Vali üks termin (soovitatavalt „lõim”) ja kasuta seda läbivalt.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "TERMINOLOOGIA",
                "tsitaat": "frameworkid ja raamistikud",
                "probleem": "Ingliskeelne termin esitatakse ilma esmakasutuse selgituseta.",
                "põhjendus": "Eestikeelses tekstis tuleks eelistada eestikeelset terminit ja vajadusel sulgudes esitada ingliskeelne vaste.",
                "soovitus": "Kasuta „raamistik (ingl framework)” esmakasutusel ja edaspidi ainult eestikeelset terminit.",
                "kindlus": "keskmine",
            },
            {
                "kategooria": "VIITAMISVAJADUS",
                "tsitaat": "üle 75% arendajatest kasutab oma igapäevatöös mingisugust raamistikku",
                "probleem": "Konkreetne arvuline väide ilma viiteta.",
                "põhjendus": "Statistiline väide peab põhinema kontrollitaval allikal (uuringul, raportil).",
                "soovitus": "Lisa viide originaaluuringule (nt Stack Overflow või JetBrains arendajaküsitlus).",
                "kindlus": "kõrge",
            },
        ],
    },
    "taust": {
        "tekst": (
            "2. Taust\n"
            "Suurte keelemudelite ajalugu algas 2017. aastal, kui ilmus Transformer "
            "arhitektuur. Kõik teavad, et tänapäeval on need mudelid kõikjal. "
            "GPT-3 omas 175 miljardit parameetrit. Käesolevas töös vaatleme, kuidas "
            "neid LLM-e (large language model) saab kasutada kvaliteedikontrolliks, "
            "kusjuures kasutame nii sõna „LLM” kui „suur keelemudel” samas tähenduses.\n"
        ),
        "leiud": [
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "tsitaat": "Kõik teavad, et tänapäeval on need mudelid kõikjal.",
                "probleem": "Määramatu üldistus („kõik teavad”).",
                "põhjendus": "Akadeemilises tekstis ei kasutata fraasi „kõik teavad” — see on subjektiivne ja toetamata üldistus.",
                "soovitus": "Asenda konkreetse väitega, mida saab viitega toetada.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "TERMINOLOOGIA",
                "tsitaat": "nii sõna „LLM” kui „suur keelemudel” samas tähenduses",
                "probleem": "Sama mõistet tähistatakse läbisegi mitme terminiga.",
                "põhjendus": "Vali üks põhitermin ja selgita esmakasutusel lühend; muidu lugeja peab pidevalt mõtlema, kas tegu on sama mõistega.",
                "soovitus": "Esmakasutusel: „suur keelemudel (LLM, ingl large language model)”; edaspidi kasuta läbivalt ühte vormi.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "VIITAMISVAJADUS",
                "tsitaat": "Suurte keelemudelite ajalugu algas 2017. aastal, kui ilmus Transformer arhitektuur.",
                "probleem": "Konkreetne ajalooline väide ilma viiteta.",
                "põhjendus": "Transformeri kasutuselevõtu väide nõuab viidet originaalartiklile.",
                "soovitus": "Lisa viide artiklile Vaswani jt „Attention Is All You Need” (2017).",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "VIITAMISVAJADUS",
                "tsitaat": "GPT-3 omas 175 miljardit parameetrit.",
                "probleem": "Konkreetne arvuline väide ilma viiteta.",
                "põhjendus": "Parameetrite arvu väide vajab viidet algallikale (Brown jt 2020).",
                "soovitus": "Lisa viide originaalpublikatsioonile.",
                "kindlus": "kõrge",
            },
        ],
    },
    "metoodika": {
        "tekst": (
            "3. Metoodika\n"
            "3.1 Andmestik\n"
            "Andmete jaoks võtsin kokku 20 bakalaureusetööd ja siis ma analüüsisin "
            "neid. Iga töö puhul vaatasin, kas seal on probleeme ja siis kirjutasin "
            "üles. See protsess oli päris pikk, aga ma sain hakkama. Tegelikult oli "
            "see asi üsna lihtne, kuna kõik tööd olid ühesuguse struktuuriga ja kõik "
            "teavad, et see lihtsustab analüüsi.\n"
        ),
        "leiud": [
            {
                "kategooria": "STRUKTUUR",
                "tsitaat": "3. Metoodika\n3.1 Andmestik\nAndmete jaoks võtsin kokku 20 bakalaureusetööd…",
                "probleem": "Peatükk algab kohe alapealkirjaga ilma sissejuhatava lõiguta.",
                "põhjendus": "Lugeja ei saa enne alampeatükki ülevaadet, milliseid metoodika samme käesolev peatükk üldse käsitleb.",
                "soovitus": "Lisa 3. peatüki algusesse lõik, mis loetleb metoodika peamised sammud.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "tsitaat": "võtsin kokku 20 bakalaureusetööd ja siis ma analüüsisin neid",
                "probleem": "Mina-vorm metoodika kirjelduses.",
                "põhjendus": "Akadeemilises tekstis kirjeldatakse metoodikat tavaliselt umbisikulises kõneviisis, et fookus oleks protsessil, mitte autoril.",
                "soovitus": "Sõnasta umbisikuliseks („koguti 20 bakalaureusetööd, mida seejärel analüüsiti”).",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "tsitaat": "See protsess oli päris pikk, aga ma sain hakkama.",
                "probleem": "Kõnekeelne ja subjektiivne hinnang („päris pikk”, „sain hakkama”).",
                "põhjendus": "Akadeemiline tekst ei hinda autori enesetunnet vaid protsessi parameetreid.",
                "soovitus": "Asenda mõõdetavate näitajatega (nt analüüsiks kulus ligikaudu 40 tundi).",
                "kindlus": "keskmine",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "tsitaat": "kõik teavad, et see lihtsustab analüüsi",
                "probleem": "Määramatu üldistus.",
                "põhjendus": "Üldistus ilma allikata ei sobi metoodika põhjendamiseks.",
                "soovitus": "Põhjenda struktuuri ühtsuse mõju analüüsile konkreetse argumendi või allikaga.",
                "kindlus": "kõrge",
            },
        ],
    },
    "tulemused": {
        "tekst": (
            "4. Tulemused\n"
            "4.1 Üldine pilt\n"
            "Tabel 4.1 näitab tulemusi.\n"
            "Tulemustest selgus, et süsteem leidis keskmiselt 6,3 probleemi peatüki "
            "kohta ning täpsus oli 87%. See on päris hea tulemus. Võrdluseks võib "
            "öelda, et inimene leiab keskmiselt sama palju. Süsteemi precision oli "
            "kõrge ning recall oli ka okei.\n"
        ),
        "leiud": [
            {
                "kategooria": "STRUKTUUR",
                "tsitaat": "4.1 Üldine pilt\nTabel 4.1 näitab tulemusi.",
                "probleem": "Alampeatükk algab kohe tabeliviitega ilma sissejuhatava lauseta.",
                "põhjendus": "Lugejale tuleks enne tabelit selgitada, mida tabel sisaldab ja milline järeldus sealt tuleb.",
                "soovitus": "Lisa enne tabeliviidet 1–2 lauset, mis tutvustavad tabeli sisu ja peamist tähelepanekut.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "tsitaat": "See on päris hea tulemus.",
                "probleem": "Subjektiivne hinnang ilma võrdlusaluseta.",
                "põhjendus": "„Päris hea” pole akadeemiliselt sisukas hinnang — vajalik on võrdlus baasjooneega või varasema tööga.",
                "soovitus": "Asenda kvantitatiivse võrdlusega varasema töö või baasjoone vastu.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "TERMINOLOOGIA",
                "tsitaat": "Süsteemi precision oli kõrge ning recall oli ka okei.",
                "probleem": "Ingliskeelsed terminid ilma esmakasutuse selgituseta ja kõnekeelne hinnang („okei”).",
                "põhjendus": "Eestikeelses tekstis tuleks kasutada „täpsus” ja „saagis” (esmakasutusel sulgudes ingliskeelne vaste).",
                "soovitus": "Esmakasutusel: „täpsus (ingl precision)” ja „saagis (ingl recall)”; eemalda „okei”.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "VIITAMISVAJADUS",
                "tsitaat": "inimene leiab keskmiselt sama palju",
                "probleem": "Võrdlus inimese sooritusega ilma viite või enda mõõtmiseta.",
                "põhjendus": "Sellise võrdluse aluseks peab olema kas tsiteeritav uuring või enda eksperiment.",
                "soovitus": "Lisa viide allikale või kirjelda, kuidas inimese sooritust selles töös mõõdeti.",
                "kindlus": "kõrge",
            },
        ],
    },
    "kokkuvote": {
        "tekst": (
            "5. Kokkuvõte\n"
            "Käesolevas töös sai uuritud, kuidas suuri keelemudeleid saab kasutada "
            "eestikeelse lõputöö kvaliteedikontrolliks. Tulemused näitavad, et asi "
            "töötab päris hästi. Tegelikult oli see üks lahe töö ja ma õppisin palju. "
            "Üle 90% katseisikutest leidis süsteemi kasulikuks. Edaspidi võiks teha "
            "veel asju, näiteks rohkem teste.\n"
        ),
        "leiud": [
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "tsitaat": "Tulemused näitavad, et asi töötab päris hästi.",
                "probleem": "Kõnekeelsed sõnad „asi”, „päris hästi”.",
                "põhjendus": "Kokkuvõte peaks sõnastama tulemused konkreetsete arvude või kategooriatega, mitte kõnekeelsete hinnangutega.",
                "soovitus": "Asenda konkreetse näitajaga (nt „süsteem leidis keskmiselt 6,3 probleemi peatüki kohta täpsusega 87%”).",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "tsitaat": "Tegelikult oli see üks lahe töö ja ma õppisin palju.",
                "probleem": "Mina-vorm ja kõnekeelne hinnang isikliku õppimiskogemuse kohta.",
                "põhjendus": "Bakalaureusetöö kokkuvõte fokuseerib teaduslikule panusele, mitte autori isiklikule kogemusele.",
                "soovitus": "Eemalda lause või asenda see töö tegeliku panuse kirjeldusega.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "tsitaat": "Edaspidi võiks teha veel asju, näiteks rohkem teste.",
                "probleem": "Ebamäärane tulevikutöö kirjeldus („veel asju”).",
                "põhjendus": "Tulevikutöö lõik peaks loetlema konkreetseid suundi, mitte üldsõnaliselt mainima „asju”.",
                "soovitus": "Loetle 2–3 konkreetset suunda (nt suurem valim, võrdlus muude mudelitega).",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "VIITAMISVAJADUS",
                "tsitaat": "Üle 90% katseisikutest leidis süsteemi kasulikuks.",
                "probleem": "Konkreetne arvuline väide ilma viiteta töö hindamise peatükile.",
                "põhjendus": "Tulemuse esitus kokkuvõttes peab viitama vastava peatüki konkreetsele tabelile või joonisele.",
                "soovitus": "Lisa viide hindamise peatüki tulemustabelile (nt „vt tabel 5.1”).",
                "kindlus": "keskmine",
            },
        ],
    },
}


def naidisteksti_tagasta(peatuki_tyyp: str) -> str:
    """Tagastab demo-režiimi näidisteksti antud peatüki tüübi jaoks."""
    return NAIDIS[peatuki_tyyp]["tekst"]


def kantud_vastus_jsonina(peatuki_tyyp: str) -> str:
    """Tagastab salvestatud leidude loendi JSON-stringina.

    Vastus on tahtlikult samas kujus, nagu LLM tagastaks: ühe võtmega „leiud”
    objekt, mille väärtus on leidude loend. Nii saab demo-pakkuja seda
    kasutada täpselt nagu päris pakkuja vastust.
    """
    keha = {"leiud": NAIDIS[peatuki_tyyp]["leiud"]}
    return json.dumps(keha, ensure_ascii=False)
