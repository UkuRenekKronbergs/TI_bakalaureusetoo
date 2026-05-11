"""Demo-pakkuja: tagastab salvestatud vastuse ilma välisteenuseta.

Selleks et süsteemi saaks proovida ka ilma Anthropic/OpenAI API võtmeta,
on demo-režiimis iga peatüki tüübi jaoks käsitsi koostatud näidisvastus
(vt `demo_andmed.NAIDIS`). Pakkuja loeb prompti sisust välja peatüki
tüübi ja tagastab vastava JSON-i.
"""

from __future__ import annotations

import re

from demo_andmed import NAIDIS, kantud_vastus_jsonina

from .base import LLMProvider, ProviderError

_PEATYKI_MUSTER = re.compile(r"Peatüki tüüp:\s*(\S+)")


class DemoProvider(LLMProvider):
    def __init__(self, mudel: str = "demo") -> None:
        self._mudel = mudel

    @property
    def mudeli_nimi(self) -> str:
        return self._mudel

    def kysi(
        self, prompt: str, *, max_tokens: int = 4096, temperature: float = 0.2
    ) -> str:
        del max_tokens, temperature
        vaste = _PEATYKI_MUSTER.search(prompt)
        if not vaste:
            raise ProviderError(
                "Demo-pakkuja ei suutnud promptist peatüki tüüpi tuvastada."
            )
        tyyp = vaste.group(1).strip()
        if tyyp not in NAIDIS:
            raise ProviderError(
                f"Demo-pakkujal pole näidisvastust peatüki tüübile '{tyyp}'."
            )
        return kantud_vastus_jsonina(tyyp)
