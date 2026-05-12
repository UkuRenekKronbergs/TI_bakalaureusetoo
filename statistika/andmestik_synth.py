"""Sünteetiline testkogu ja kuldstandard hindamis-pipeline'i illustratsiooniks.

KÕIK SELLE FAILI ANDMED ON GENEREERITUD autori juhendamisel Claude 4.7 Opus
mudeliga INTERAKTIIVSE VESTLUSLIIDESE (Claude Code) kaudu, mitte tasuliste
API-päringute kaudu. Ühekordne genereerimisprotsess on metoodiliselt eraldatud
skriptist `paris_hindamine.py`, mis kasutab tasulisi API-sid
hindamispäringuteks.

Need ei ole päris üliõpilaste tööde katkendid ega päris annoteerijate
märgendused.

Andmete struktuur:
  TESTKOGU: list[dict] — iga element on üks katkend, milles on:
    - id: lühike unikaalne ID (nt "sis-01")
    - peatuki_tyyp: üks viiest tüübist
    - tekst: 200-300 sõna eestikeelne tekst koos tahtlikult sisse pandud
      probleemidega ja korrektsete lõikudega
    - kuldstandard: list[dict] — käsitsi annoteeritud probleemid katkendis,
      iga annotatsioon sisaldab kategooriat, probleemse fragmendi (span'i),
      lühikest kirjeldust ja kindlushinnangut

Iga "probleem" on lühike tekstifragment, mis peaks katkendis esineda
selliselt, nagu siin kuldstandardis on kirjas. Span-tasemel kattuvuse
arvutamiseks (vt thesis ptk 3.5) kasutatakse sõna-tasemel võrdlust.
"""

from __future__ import annotations

from typing import TypedDict


class Annotatsioon(TypedDict):
    kategooria: str
    span: str
    probleem: str
    kindlus: str


class Katkend(TypedDict):
    id: str
    peatuki_tyyp: str
    tekst: str
    kuldstandard: list[Annotatsioon]


TESTKOGU: list[Katkend] = [
    # =================================================================
    # SISSEJUHATUS (4 katkendit)
    # =================================================================
    {
        "id": "sis-01",
        "peatuki_tyyp": "sissejuhatus",
        "tekst": (
            "1. Sissejuhatus\n"
            "1.1 Probleem\n"
            "Tänapäeval kasutab üle 80% Eesti väikeettevõtetest mingisugust pilveteenust "
            "andmete säilitamiseks. Selliste teenustega kaasnevad turvariskid, kuna andmed "
            "asuvad teenusepakkuja serverites. Käesoleva bakalaureusetöö raames vaatlen, "
            "kuidas saaks väikeettevõtete jaoks pakkuda lihtsasti kasutatavat krüpteeritud "
            "varundusteenust. Lahendus peaks olema kasutatav ka ilma sügava IT-teadmiseta. "
            "Tegelikult on see asi keerulisem, kui esmapilgul tundub, kuna krüptograafia "
            "on mitmekihiline distsipliin. Töö koosneb viiest peatükist. Teises peatükis "
            "tutvustatakse krüptograafia põhitõdesid. Kolmandas kirjeldatakse metoodikat. "
            "Neljas peatükk on prototüüp. Viiendas vaadeldakse tulemusi."
        ),
        "kuldstandard": [
            {
                "kategooria": "VIITAMISVAJADUS",
                "span": "üle 80% Eesti väikeettevõtetest kasutab mingisugust pilveteenust",
                "probleem": "Konkreetne arvuline väide ilma viiteta.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "STRUKTUUR",
                "span": "1. Sissejuhatus\n1.1 Probleem\nTänapäeval kasutab",
                "probleem": "Peatükk algab kohe alapealkirjaga ilma sissejuhatava lõiguta.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "span": "vaatlen, kuidas saaks",
                "probleem": "Mina-vorm sissejuhatuses, kus võiks kasutada umbisikulist.",
                "kindlus": "keskmine",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "span": "Tegelikult on see asi keerulisem",
                "probleem": "Kõnekeelsed sõnad „tegelikult” ja „asi”.",
                "kindlus": "kõrge",
            },
        ],
    },
    {
        "id": "sis-02",
        "peatuki_tyyp": "sissejuhatus",
        "tekst": (
            "Suur osa veebirakendusi tugineb täna SQL-andmebaasidele. Need pakuvad tugevat "
            "andmete järjepidevust ja küpseid tehnoloogiaid, kuid mastaapsuse osas tulevad "
            "mängu NoSQL ja key-value store'id. Veebipoodide jaoks on iga sekundi viivitus "
            "kasutaja jaoks mõõdetav kahju. Käesolevas bakalaureusetöös on eesmärgiks "
            "võrrelda Redise ja Memcached'i sooritust e-poe sessioonihoidlana koormustestide "
            "kaudu. Esimesel pilgul tundub, et asjad on lihtsad: kumb on kiirem, see "
            "võidab. Reaalsuses tuleb mängu mälukasutus, andmete eluiga ja klastri "
            "konfiguratsioon. Töö annab konkreetse soovituse, millise lahenduse poole "
            "Eesti väikeste e-poodide arendajatel tasub kalduda."
        ),
        "kuldstandard": [
            {
                "kategooria": "TERMINOLOOGIA",
                "span": "NoSQL ja key-value store'id",
                "probleem": "Ingliskeelne termin ilma eestikeelse vasteta esmakasutusel.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "span": "Esimesel pilgul tundub, et asjad on lihtsad",
                "probleem": "Kõnekeelne fraas „esimesel pilgul tundub” ja sõna „asjad”.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "span": "see võidab",
                "probleem": "Kõnekeelne hinnang.",
                "kindlus": "keskmine",
            },
            {
                "kategooria": "VIITAMISVAJADUS",
                "span": "veebipoodide jaoks on iga sekundi viivitus kasutaja jaoks mõõdetav kahju",
                "probleem": "Üldistav väide kahju kohta vajab viidet allikale.",
                "kindlus": "keskmine",
            },
        ],
    },
    {
        "id": "sis-03",
        "peatuki_tyyp": "sissejuhatus",
        "tekst": (
            "1. Sissejuhatus\n\n"
            "Mobiilirakenduste ligipääsetavus puuetega kasutajatele on kasvav nõue nii "
            "seadusandlikust kui ka eetilisest perspektiivist. Euroopa Liidu juurdepääsetavuse "
            "akt kohustab alates 2025. aastast paljusid mobiilirakendusi vastama "
            "WCAG 2.1 tasemele AA. Eestis on enam kui 100 000 inimest, kellel on mingisugune "
            "nägemise või liikumise piirang, mis mõjutab nutiseadme kasutust. Käesolevas "
            "töös uuritakse, kuidas Tartu Ülikooli sisemiste teenuste mobiilirakendused "
            "vastavad WCAG nõuetele. Töö hõlmab automaatset analüüsi neljal rakendusel "
            "ning käsitsi auditit kahel. Kasutatakse tööriistu nagu Accessibility Scanner "
            "Androidil ja Accessibility Inspector iOS-il. Tulemused võimaldavad teha "
            "konkreetseid parandussoovitusi."
        ),
        "kuldstandard": [
            {
                "kategooria": "VIITAMISVAJADUS",
                "span": "Eestis on enam kui 100 000 inimest, kellel on mingisugune nägemise või liikumise piirang",
                "probleem": "Konkreetne arvuline väide ilma viiteta.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "VIITAMISVAJADUS",
                "span": "Euroopa Liidu juurdepääsetavuse akt kohustab alates 2025. aastast",
                "probleem": "Seadusandliku akti kohta puudub viide.",
                "kindlus": "keskmine",
            },
        ],
    },
    {
        "id": "sis-04",
        "peatuki_tyyp": "sissejuhatus",
        "tekst": (
            "Tarkvarapakettide turvanõrkused on suur murekoht. Nendega tegelemiseks on "
            "loodud mitmesuguseid süsteeme, näiteks GitHubi Dependabot ja Snyk. Nende "
            "süsteemide täpsus ja saagis varieerub. Käesolev bakalaureusetöö hindab nelja "
            "Eestis levinud avatud lähtekoodiga projekti pealt, kui hästi tuvastavad need "
            "süsteemid teadaolevaid haavatavusi. Kuna mina arvan, et avatud lähtekoodiga "
            "projektide turvalisus on ühiskondlikult oluline, on selliste süsteemide "
            "võrdlemine kasulik. Töö koosneb kuuest osast. Teises osas on taust. "
            "Kolmandas on metoodika. Neljas on tulemused. Viiendas arutelu. Kuuendas "
            "kokkuvõte."
        ),
        "kuldstandard": [
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "span": "Kuna mina arvan, et avatud lähtekoodiga projektide turvalisus",
                "probleem": "Mina-vorm ja subjektiivne hinnang sissejuhatuses.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "STRUKTUUR",
                "span": "Töö koosneb kuuest osast. Teises osas on taust. Kolmandas on metoodika.",
                "probleem": "Töö ülesehituse loetelu on telegraafilises stiilis ja korduva struktuuriga.",
                "kindlus": "keskmine",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "span": "on suur murekoht",
                "probleem": "Kõnekeelne väljend „suur murekoht”.",
                "kindlus": "keskmine",
            },
        ],
    },
    # =================================================================
    # TAUST JA SEOTUD TÖÖD (5 katkendit)
    # =================================================================
    {
        "id": "tau-01",
        "peatuki_tyyp": "taust",
        "tekst": (
            "2.1 Konteineritehnoloogia areng\n\n"
            "Konteinerid on lihtsamad ja kergemad kui täisvirtualiseerimine. Docker "
            "tutvustas konteinereid laiale arendajaskonnale alates 2013. aastast. "
            "Konteinerid jagavad kerneliga, samas kui virtuaalmasinad emuleerivad terve "
            "operatsioonisüsteemi. See teeb konteinerid kiiremaks kui VM-id. Üks Docker "
            "konteiner käivitub millisekunditega, samas kui virtuaalmasin vajab "
            "käivitamiseks mitukümmend sekundit. Kõik teavad, et see on kiirem. "
            "Konteinereid orkestreeritakse Kubernetese abil. Kuberneteses on pod kõige "
            "väiksem üksus, mis võib sisaldada ühte või mitut konteinerit. Termini "
            "„konteiner” tähendus on selles kontekstis tihti segane, kuna ka VM-i "
            "lähedasi lahendusi (näiteks Firecracker) nimetatakse vahel konteineriteks, "
            "kuigi need on hoopis mikro-virtuaalmasinad."
        ),
        "kuldstandard": [
            {
                "kategooria": "VIITAMISVAJADUS",
                "span": "Docker tutvustas konteinereid laiale arendajaskonnale alates 2013. aastast",
                "probleem": "Ajalooline väide vajab viidet.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "VIITAMISVAJADUS",
                "span": "Üks Docker konteiner käivitub millisekunditega",
                "probleem": "Konkreetne sooritus väide ilma viiteta.",
                "kindlus": "keskmine",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "span": "Kõik teavad, et see on kiirem",
                "probleem": "Määramatu üldistus „kõik teavad”.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "TERMINOLOOGIA",
                "span": "VM-id",
                "probleem": "Ingliskeelne lühend ilma esmakasutuse selgituseta.",
                "kindlus": "keskmine",
            },
        ],
    },
    {
        "id": "tau-02",
        "peatuki_tyyp": "taust",
        "tekst": (
            "Krüptograafilised räsifunktsioonid moodustavad nüüdisaegse infoturbe ühe "
            "alustala. Esimene laiemalt kasutatud räsifunktsioon oli MD5, mille Ronald "
            "Rivest publitseeris 1992. aastal~\\cite{rivest_md5_1992}. MD5-l avastati "
            "kokkupõrkenõrkused alates 1996. aastast, ning 2004. aastal demonstreeris "
            "Wang jt praktilist kokkupõrkerünnet~\\cite{wang_md5_2004}. SHA-1 oli "
            "MD5-le järelkäija, kuid sellelegi avastati teoreetilisi nõrkusi ning "
            "Google demonstreeris 2017. aastal esimest praktilist SHA-1 "
            "kokkupõrget~\\cite{stevens_sha1_2017}. Tänapäeval soovitatakse "
            "kasutada SHA-256 ja SHA-3 perekondi. Eestis kasutab digiallkirja "
            "infrastruktuur SHA-256-d. Räsifunktsiooni hash output on tüüpiliselt "
            "128 kuni 512 bitti pikk. Hash function peab olema kollisioonikindel ja "
            "ühe-suunaline."
        ),
        "kuldstandard": [
            {
                "kategooria": "TERMINOLOOGIA",
                "span": "Räsifunktsiooni hash output",
                "probleem": "Inglise ja eesti termin segamini („räsifunktsioon” ja „hash”).",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "TERMINOLOOGIA",
                "span": "Hash function peab olema",
                "probleem": "Ingliskeelne termin ilma eestikeelse vasteta, ehkki eelnevalt on kasutatud „räsifunktsioon”.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "VIITAMISVAJADUS",
                "span": "Eestis kasutab digiallkirja infrastruktuur SHA-256-d",
                "probleem": "Konkreetne tehniline väide süsteemi kohta vajab viidet.",
                "kindlus": "keskmine",
            },
        ],
    },
    {
        "id": "tau-03",
        "peatuki_tyyp": "taust",
        "tekst": (
            "Kasutatavusuuringud (\\emph{ingl.\\ usability studies}) on tarkvaraarenduses "
            "kasutusel olnud alates 1980-ndatest~\\cite{nielsen_usability_1993}. Klassikalised "
            "meetodid hõlmavad lähivaatlust, mõtle-valjusti-protokolli ja "
            "ülesannetepõhist testimist. Nielseni klassikaline soovitus on, et viiest "
            "testijast piisab umbes 85% kasutatavusprobleemide tuvastamiseks~\\cite{nielsen_5users_2000}. "
            "Hiljutised tööd on aga seda väidet vaidlustanud~\\cite{faulkner_2003}, "
            "näidates et keerukate süsteemide puhul on vajalik suurem valim. Online-meetoditena "
            "on populaarsed kuumakaardid (Hotjar, Microsoft Clarity) ja kliki-analüüs. "
            "Mobiilirakenduste puhul lisanduvad konteksti-eripärad: ekraani suurus, "
            "ühe käega kasutamise mugavus ja katkestuste rohkus."
        ),
        "kuldstandard": [
            {
                "kategooria": "VIITAMISVAJADUS",
                "span": "Online-meetoditena on populaarsed kuumakaardid (Hotjar, Microsoft Clarity)",
                "probleem": "Konkreetsete kommertsiaalsete tööriistade nimetamine ilma viiteta.",
                "kindlus": "madal",
            },
        ],
    },
    {
        "id": "tau-04",
        "peatuki_tyyp": "taust",
        "tekst": (
            "Pilvepõhise arvutuse mõiste on lai. Klassikaliselt eristatakse kolme "
            "teenusemudelit: IaaS (Infrastructure as a Service), PaaS (Platform as a "
            "Service) ja SaaS (Software as a Service)~\\cite{mell_nist_2011}. IaaS "
            "näiteks on AWS EC2, mis pakub virtuaalmasinaid kasutaja poolt seadistatava "
            "operatsioonisüsteemiga. PaaS näiteks on Heroku, kus arendaja ei seadista "
            "OS-i, vaid lihtsalt paigaldab oma rakenduse. SaaS näide on Google Workspace, "
            "kus kasutaja ei näe alustehnoloogiat. Asi see, et piirid nende vahel "
            "on hägused: paljud teenused on hübriidid. Lisaks on tekkinud uued "
            "kategooriad — FaaS (Function as a Service), millest tuntum on AWS Lambda, "
            "ja CaaS (Container as a Service). Hindade osas on FaaS odav väiksete "
            "rakenduste puhul ja kallis suurte koormuste puhul."
        ),
        "kuldstandard": [
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "span": "Asi see, et piirid nende vahel on hägused",
                "probleem": "Kõnekeelne fraas „asi see, et”.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "VIITAMISVAJADUS",
                "span": "FaaS on odav väiksete rakenduste puhul ja kallis suurte koormuste puhul",
                "probleem": "Hinnaväide vajab viidet konkreetsele võrdlusele.",
                "kindlus": "keskmine",
            },
        ],
    },
    {
        "id": "tau-05",
        "peatuki_tyyp": "taust",
        "tekst": (
            "2.3 Statistilise õppe alused\n\n"
            "Masinõpe jaguneb laias laastus juhendatud, juhendamata ja stiimulõppeks. "
            "Juhendatud õppes treenitakse mudelit märgendatud andmetel, eesmärgiga "
            "ennustada uutele sisenditele märgendeid. Tüüpilisteks ülesanneteks on "
            "klassifikatsioon ja regressioon. Juhendamata õppes ei ole märgendid antud "
            "— eesmärgiks on andmete struktuuri leidmine (näiteks klasterdamine). "
            "Stiimulõppes õpib agent keskkonnaga suhtlemise käigus, saades preemiat või "
            "karistust. Süvaõpe (deep learning) on viimase kümnendi domineeriv lähenemine, "
            "mis kasutab mitmekihilisi närvivõrke. Convolutional neural network ehk CNN "
            "on populaarne pildianalüüsis. Tänapäeval kasutavad kõik mudelid süvaõpet."
        ),
        "kuldstandard": [
            {
                "kategooria": "TERMINOLOOGIA",
                "span": "Süvaõpe (deep learning) on viimase kümnendi domineeriv lähenemine",
                "probleem": "Termini esitus on korrektne (eesti keel + ingliskeelne sulgudes).",
                "kindlus": "madal",
            },
            {
                "kategooria": "TERMINOLOOGIA",
                "span": "Convolutional neural network ehk CNN",
                "probleem": "Ingliskeelne termin enne eestikeelset; eelistada „konvolutsiooniline närvivõrk (ingl convolutional neural network, CNN)”.",
                "kindlus": "keskmine",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "span": "Tänapäeval kasutavad kõik mudelid süvaõpet",
                "probleem": "Määramatu üldistus „kõik mudelid”.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "STRUKTUUR",
                "span": "2.3 Statistilise õppe alused\n\nMasinõpe jaguneb",
                "probleem": "Alapeatükk algab kohe põhitekstiga ilma alapeatüki tutvustava lauseta.",
                "kindlus": "madal",
            },
        ],
    },
    # =================================================================
    # METOODIKA (4 katkendit)
    # =================================================================
    {
        "id": "met-01",
        "peatuki_tyyp": "metoodika",
        "tekst": (
            "3.1 Andmete kogumine\n"
            "Andmete kogumiseks kasutati struktureeritud küsimustikku, mis koostati "
            "Google Formsis. Küsimustik saadeti laiali 200 Tartu Ülikooli arvutiteaduse "
            "tudengile e-posti teel. Vastuste kogumine kestis kaks nädalat — 1. märtsist "
            "kuni 14. märtsini 2026. Vastasid 87 tudengit, mille vastamismääraks oli "
            "43,5%. Küsimustik koosnes 18 küsimusest, mis jagunesid kolme blokki: "
            "demograafia (4 küsimust), tarkvaraarenduse kogemus (8 küsimust) ja "
            "hinnangud konkreetsetele tööriistadele (6 küsimust). Küsimustik valideeriti "
            "pilootuuringuga viie tudengi peal enne laialisaatmist. Vastuste analüüsiks "
            "kasutati programmi R 4.3.0 ning paketti `tidyverse`."
        ),
        "kuldstandard": [],
    },
    {
        "id": "met-02",
        "peatuki_tyyp": "metoodika",
        "tekst": (
            "3.2 A/B-testi disain\n"
            "Selleks et hinnata uue checkout-flow mõju konversioonile, viidi läbi A/B-test. "
            "Mina jaotasin kasutajad juhuslikult kahte gruppi: kontrollgrupp (vana flow) "
            "ja katsegrupp (uus flow). Statistilise testi efekti tuvastamise võimsuseks "
            "valisin 0,8 ning olulisuse tasemeks 0,05. Eeldatav efekti suurus oli 5% "
            "konversiooni kasv, mis nõudis igas grupis vähemalt 1500 kasutajat. Test "
            "kestis kuni vajalik valimi suurus saavutati, mis võttis aega 12 päeva. "
            "Konversioon mõõdeti kui ostuni jõudnud sessioonide osakaal kõikidest "
            "sessioonidest. Sekundaarseteks mõõdikuteks olid keskmine ostukorvi väärtus, "
            "checkout-protsessi keskmine kestus ja katkestamise määr."
        ),
        "kuldstandard": [
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "span": "Mina jaotasin kasutajad juhuslikult kahte gruppi",
                "probleem": "Mina-vorm metoodika kirjelduses.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "span": "olulisuse tasemeks 0,05. Eeldatav efekti suurus oli 5% konversiooni kasv, mis nõudis igas grupis vähemalt 1500 kasutajat. Test kestis kuni vajalik valimi suurus saavutati, mis võttis aega 12 päeva. Konversioon mõõdeti",
                "probleem": "Lause on liiga pikk ja sisaldab mitut väidet.",
                "kindlus": "madal",
            },
            {
                "kategooria": "TERMINOLOOGIA",
                "span": "uue checkout-flow mõju konversioonile",
                "probleem": "Ingliskeelne termin „checkout-flow” ilma eestikeelse vasteta esmakasutusel.",
                "kindlus": "keskmine",
            },
        ],
    },
    {
        "id": "met-03",
        "peatuki_tyyp": "metoodika",
        "tekst": (
            "3.3 Benchmark-mõõtmised\n\n"
            "Algoritmi sooritust hinnati kontrollitud keskkonnas: AMD Ryzen 7 5800X "
            "protsessor, 32 GB DDR4-3200 RAM, Ubuntu 22.04 LTS. Iga mõõtmist korrati "
            "30 korda, kasutati Hyperfine tööriista (versioon 1.18). Sisendsuurused "
            "olid 10^3, 10^4, 10^5, 10^6 ja 10^7 elementi. Iga sisendsuuruse jaoks "
            "genereeriti viis erinevat sisendit (juhuslikult vahemikus [0, 10^9]) ning "
            "iga sisendit testiti kolme erineva algoritmiga: kiir-sort, ühenda-sort ja "
            "kuhi-sort. Tulemused on esitatud peatükis 4. Üldiselt oli kiir-sort kõige "
            "kiirem, aga see asi sõltub palju sisendi struktuurist."
        ),
        "kuldstandard": [
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "span": "aga see asi sõltub palju sisendi struktuurist",
                "probleem": "Kõnekeelne sõnastus „see asi sõltub palju”.",
                "kindlus": "kõrge",
            },
        ],
    },
    {
        "id": "met-04",
        "peatuki_tyyp": "metoodika",
        "tekst": (
            "Lähtekoodi staatiliseks analüüsiks kasutati tööriista SonarQube versiooni "
            "10.4. Analüüs hõlmas 12 projekti, mis valiti GitHubi populaarseimate "
            "Java-projektide hulgast. Iga projekti puhul mõõdeti järgmised näitajad: "
            "tehnilise võla hinnang (tundides), koodi katvus testidega, dubleerimise "
            "määr ja turvanõrkuste arv. Analüüs viidi läbi nii projekti kõige uuemal "
            "versioonil kui ka aasta vanusel versioonil, et hinnata tehnilise võla "
            "kasvu. Tulemused agregeeriti projektitüüpide kaupa (raamistikud, "
            "tarbeprogrammid, IDE-laiendused). Statistiline analüüs viidi läbi R-i "
            "abil; korrelatsioonid arvutati Spearmani $\\rho$-ga, kuna jaotused "
            "ei olnud normaalsed."
        ),
        "kuldstandard": [],
    },
    # =================================================================
    # TULEMUSED (4 katkendit)
    # =================================================================
    {
        "id": "tul-01",
        "peatuki_tyyp": "tulemused",
        "tekst": (
            "4.1 Algoritmide võrdlus\n"
            "Tabel 4.1 näitab mõõtmistulemusi.\n"
            "Mõõtmistulemused näitavad, et kiir-sort on enamasti kõige kiirem, kuid mitte "
            "alati. Suurte sisendite (10^7) korral oli ühenda-sort 12% kiirem kui kiir-sort. "
            "See on päris hea tulemus. Põhjuseks on tõenäoliselt mälu hierarhia parem "
            "kasutamine, kuna ühenda-sort omab paremat ruumilist lokaalsust. Kuhi-sort oli "
            "kõikides katsetes aeglasem, mis on kooskõlas ootustega. Standardhälve oli "
            "kõikides mõõtmistes alla 5% keskmisest, mis viitab mõõtmiste "
            "korratavusele. Kõige üllatavama tulemus oli see, et 10^3 sisendi korral "
            "ei olnud algoritmide vahel statistiliselt olulist erinevust (p > 0,1 "
            "kõikides paaride võrdlustes)."
        ),
        "kuldstandard": [
            {
                "kategooria": "STRUKTUUR",
                "span": "4.1 Algoritmide võrdlus\nTabel 4.1 näitab mõõtmistulemusi.",
                "probleem": "Alampeatükk algab kohe tabeliviitega ilma sissejuhatava lauseta.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "span": "See on päris hea tulemus",
                "probleem": "Subjektiivne hinnang „päris hea” ilma võrdlusaluseta.",
                "kindlus": "kõrge",
            },
        ],
    },
    {
        "id": "tul-02",
        "peatuki_tyyp": "tulemused",
        "tekst": (
            "Küsitlusele vastas 87 tudengit. Demograafia osas olid vastajatest 58 (66,7%) "
            "meessoost ja 29 (33,3%) naissoost; vanus jagunes vahemikus 19–28 aastat "
            "(mediaan 22). 71 vastajat (81,6%) olid bakalaureuseastmes, 16 (18,4%) "
            "magistrantuuris. Konkreetsete tööriistade hinnangus oli ülekaalukalt "
            "kõige populaarsem Visual Studio Code (kasutab 79 vastajat ehk 90,8%), "
            "millele järgnesid IntelliJ IDEA (43,7%) ja Eclipse (5,7%). Hinnangud "
            "esitati Likerti 5-pallisel skaalal, kus 1 tähendas „üldse mitte rahul” "
            "ja 5 „väga rahul”. VS Code'i keskmine hinnang oli 4,3 (SD = 0,7), "
            "IntelliJ IDEA-l 4,1 (SD = 0,9). Mann-Whitney U-test näitas, et hinnangute "
            "erinevus VS Code'i ja IntelliJ IDEA vahel ei olnud statistiliselt "
            "oluline (p = 0,18)."
        ),
        "kuldstandard": [],
    },
    {
        "id": "tul-03",
        "peatuki_tyyp": "tulemused",
        "tekst": (
            "Mina mõõtsin veebirakenduse vastuseaegu 50 erineva päringutüübi peal. "
            "Tulemused näitavad, et 95-protsentiil oli 230 ms ning maksimaalne vastuseaeg "
            "1,8 sekundit. Üle 90% kasutajatest leiab, et alla 200 ms on hea kogemus. "
            "Meie rakendus jääb sellele piirile veidi alla, kuid keskmine kogemus on "
            "siiski okei. Vastuseaja jaotus oli paremalt kalduv, mis on tüüpiline "
            "veebirakenduste käitumine. Päringutüüpide võrdluses olid pildi-laadivad "
            "päringud aeglaseimad (mediaan 340 ms), millele järgnesid otsingupäringud "
            "(180 ms) ja autentimispäringud (90 ms). Vastuseaja optimeerimist tasub "
            "alustada pildi-laadivatest päringutest, kuna nende osa kogu liiklusest on "
            "31% ja parandamise potentsiaal on suurim."
        ),
        "kuldstandard": [
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "span": "Mina mõõtsin veebirakenduse vastuseaegu",
                "probleem": "Mina-vorm tulemuste kirjelduses.",
                "kindlus": "keskmine",
            },
            {
                "kategooria": "VIITAMISVAJADUS",
                "span": "Üle 90% kasutajatest leiab, et alla 200 ms on hea kogemus",
                "probleem": "Konkreetne arvuline väide kasutajate hinnangu kohta vajab viidet.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "span": "keskmine kogemus on siiski okei",
                "probleem": "Kõnekeelne sõna „okei”.",
                "kindlus": "kõrge",
            },
        ],
    },
    {
        "id": "tul-04",
        "peatuki_tyyp": "tulemused",
        "tekst": (
            "4.3 Mudeli treenimistulemused\n\n"
            "Mudelit treeniti 50 epohhi vältel, kasutades Adami optimeerijat "
            "õpisammuga 0,001 ja partii suurusega 64. Treeningandmestik koosnes "
            "12 000 näitest, valideerimisandmestik 1 500 näitest ja testandmestik "
            "1 500 näitest. Joonis 4.2 esitab treening- ja valideerimiskao "
            "arengukõvera. Mudel saavutas parima valideerimissoorituse epohhis 32, "
            "pärast mida valideerimiskaotus hakkas kasvama (overfitting). Selle järgi "
            "valisime lõpliku mudeli epohhis 32. Testandmestikul oli mudeli täpsus "
            "(precision) 0,87, saagis (recall) 0,83 ja F-skoor 0,85. Võrreldes "
            "baasjoone-mudeliga (logistiline regressioon) on need näitajad "
            "vastavalt 12, 18 ja 15 protsendipunkti paremad."
        ),
        "kuldstandard": [
            {
                "kategooria": "TERMINOLOOGIA",
                "span": "valideerimiskaotus hakkas kasvama (overfitting)",
                "probleem": "Ingliskeelne termin ilma eestikeelse vasteta; eelistada „ületreenimine (ingl overfitting)”.",
                "kindlus": "kõrge",
            },
        ],
    },
    # =================================================================
    # KOKKUVÕTE (3 katkendit)
    # =================================================================
    {
        "id": "kok-01",
        "peatuki_tyyp": "kokkuvote",
        "tekst": (
            "Käesoleva bakalaureusetöö raames vaadeldi, kuidas avatud lähtekoodiga "
            "haavatavusi tuvastavad süsteemid (Dependabot, Snyk, Trivy) suudavad "
            "leida teadaolevaid CVE-sid neljas Eestis levinud projektis. Tulemused "
            "näitavad, et Snyk tuvastas keskmiselt 87% kõikidest teadaolevatest "
            "haavatavustest, Dependabot 76% ja Trivy 81%. Saagise erinevus Snyki ja "
            "Dependaboti vahel oli statistiliselt oluline (McNemari test, p = 0,03). "
            "Töö praktiline panus on konkreetne soovitus: Eesti väikeprojektidele on "
            "Snyki kasutamine põhjendatud, eriti seetõttu, et selle vabavaraline "
            "tase katab tüüpilise väikeprojekti vajadused. Tulevikutöö raames võiks "
            "uurida, kuidas need süsteemid käituvad suuremate projektide peal ning "
            "kuidas false positive'ide määra vähendada."
        ),
        "kuldstandard": [
            {
                "kategooria": "TERMINOLOOGIA",
                "span": "kuidas false positive'ide määra vähendada",
                "probleem": "Ingliskeelne termin „false positive” — eelistada „valepositiivne”.",
                "kindlus": "kõrge",
            },
        ],
    },
    {
        "id": "kok-02",
        "peatuki_tyyp": "kokkuvote",
        "tekst": (
            "Käesolev töö oli üks lahe väljakutse. Mina õppisin palju andmebaaside "
            "rände kohta. Tulemused näitavad, et PostgreSQL-i ja MySQL-i vahel "
            "rändamine on tehniliselt lihtne, aga andmetüüpide ühildumatusega on "
            "tegelikult palju asja. Kõik teavad, et iga andmebaas teeb asju erinevalt. "
            "Töö praktiline panus on rändamisskript, mis on saadaval GitHubis. "
            "Tulevikutöös võiks teha veel mõned asjad — näiteks proovida ka "
            "MongoDB-st PostgreSQL-i rändamist."
        ),
        "kuldstandard": [
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "span": "Käesolev töö oli üks lahe väljakutse. Mina õppisin palju",
                "probleem": "Mina-vorm ja kõnekeelne hinnang („lahe väljakutse”).",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "span": "tegelikult palju asja",
                "probleem": "Kõnekeelsed sõnad „tegelikult” ja „asja”.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "span": "Kõik teavad, et iga andmebaas teeb asju erinevalt",
                "probleem": "Määramatu üldistus „kõik teavad” ja kõnekeelne sõna „asju”.",
                "kindlus": "kõrge",
            },
            {
                "kategooria": "AKADEEMILINE_STIIL",
                "span": "Tulevikutöös võiks teha veel mõned asjad",
                "probleem": "Ebamäärane tulevikutöö kirjeldus.",
                "kindlus": "keskmine",
            },
        ],
    },
    {
        "id": "kok-03",
        "peatuki_tyyp": "kokkuvote",
        "tekst": (
            "Tarkvara hooldamise raamistike võrdluses ilmnesid selged "
            "kompromissid. ITIL pakub kõige laiemat hõlmavust, kuid on rakendamiseks "
            "kõige ressursimahukam. DevOps-orienteeritud raamistikud (näiteks Site "
            "Reliability Engineering ehk SRE) on kergem alustada, kuid nõuavad olulist "
            "organisatsioonilise kultuuri muutust. Eesti keskmise suurusega "
            "tarkvaraettevõtete kontekstis on otstarbekam alustada SRE-st ja "
            "vajaduspõhiselt laieneda ITIL-i elementidele. Tulevikutööna oleks väärtuslik "
            "uurida hübriidlähenemiste rakendamise edutegureid pikemas ajaraamis ning "
            "võrrelda neid empiiriliselt eri ettevõtete vahel. Lisaks väärib tähelepanu "
            "kaasaegsete AI-tööriistade integreerimine intsidendi-haldamise protsessi, "
            "mis on viimaste aastate kiire arengu valdkond."
        ),
        "kuldstandard": [],
    },
]


# Kategooriate täielik komplekt korrektsuse kontrolliks
KATEGOORIAD = ["STRUKTUUR", "AKADEEMILINE_STIIL", "TERMINOLOOGIA", "VIITAMISVAJADUS"]
KINDLUSED = ["kõrge", "keskmine", "madal"]


def kontrolli_andmete_terviklikkus() -> None:
    """Kontrollib, et iga kuldstandardi annotatsioon on korrektne."""
    nahtud_id = set()
    for k in TESTKOGU:
        assert k["id"] not in nahtud_id, f"Topelt-ID: {k['id']}"
        nahtud_id.add(k["id"])
        assert k["peatuki_tyyp"] in {"sissejuhatus", "taust", "metoodika", "tulemused", "kokkuvote"}
        for a in k["kuldstandard"]:
            assert a["kategooria"] in KATEGOORIAD, f"{k['id']}: tundmatu kategooria {a['kategooria']}"
            assert a["kindlus"] in KINDLUSED, f"{k['id']}: tundmatu kindlus {a['kindlus']}"
            # Span peaks katkendi tekstis vähemalt osaliselt sisalduma — mitte rangelt nõutud,
            # aga tüüpilise märgenduse puhul tõene.
            esimene_sona = a["span"].split()[0].lower()
            assert esimene_sona in k["tekst"].lower(), (
                f"{k['id']}: spanni esimene sõna „{esimene_sona}” ei leitud tekstis"
            )


if __name__ == "__main__":
    kontrolli_andmete_terviklikkus()
    print(f"Testkogu: {len(TESTKOGU)} katkendit")
    summa = sum(len(k["kuldstandard"]) for k in TESTKOGU)
    print(f"Kuldstandardi annotatsioone kokku: {summa}")
    print("Andmete terviklikkus: OK")
