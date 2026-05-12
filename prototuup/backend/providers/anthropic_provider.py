import os

from anthropic import Anthropic, APIError

from .base import LLMProvider, ProviderError


class AnthropicProvider(LLMProvider):
    def __init__(self, mudel: str = "claude-opus-4-7", api_key: str | None = None) -> None:
        self._mudel = mudel
        self._klient = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    @property
    def mudeli_nimi(self) -> str:
        return self._mudel

    def kysi(self, prompt: str, *, max_tokens: int = 4096, temperature: float = 0.2) -> str:
        # Uuemad Claude-mudelid (nt claude-opus-4-7, claude-sonnet-4-*) ei
        # toeta assistant-message prefill'i ega temperature-parameetrit;
        # vanematel mudelitel (nt claude-3-5-*) on mõlemad toetatud.
        uus_pere = (
            self._mudel.startswith("claude-opus-4-")
            or self._mudel.startswith("claude-sonnet-4-")
        )
        messages: list[dict] = [{"role": "user", "content": prompt}]
        if not uus_pere:
            messages.append({"role": "assistant", "content": "{"})

        paring = {
            "model": self._mudel,
            "max_tokens": max_tokens,
            "messages": messages,
        }
        if not uus_pere:
            paring["temperature"] = temperature

        try:
            sonum = self._klient.messages.create(**paring)
        except APIError as e:
            raise ProviderError(f"Anthropic API viga: {e}") from e

        if not sonum.content:
            raise ProviderError("Anthropic tagastas tühja vastuse")

        plokk = sonum.content[0]
        if plokk.type != "text":
            raise ProviderError(f"Ootamatu sisuploki tüüp: {plokk.type}")

        # Vanade mudelite puhul prefill'i tõttu peame tagastama "{" + tekst,
        # uuematel mudelitel tagastame ainult mudeli enda väljundi
        return plokk.text if uus_pere else ("{" + plokk.text)
