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
        try:
            sonum = self._klient.messages.create(
                model=self._mudel,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": "{"},
                ],
            )
        except APIError as e:
            raise ProviderError(f"Anthropic API viga: {e}") from e

        if not sonum.content:
            raise ProviderError("Anthropic tagastas tühja vastuse")

        plokk = sonum.content[0]
        if plokk.type != "text":
            raise ProviderError(f"Ootamatu sisuploki tüüp: {plokk.type}")

        return "{" + plokk.text
