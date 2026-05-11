import os

from openai import OpenAI, OpenAIError

from .base import LLMProvider, ProviderError


class OpenAIProvider(LLMProvider):
    def __init__(self, mudel: str = "gpt-5.5", api_key: str | None = None) -> None:
        self._mudel = mudel
        self._klient = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))

    @property
    def mudeli_nimi(self) -> str:
        return self._mudel

    def kysi(self, prompt: str, *, max_tokens: int = 4096, temperature: float = 0.2) -> str:
        try:
            paring = {
                "model": self._mudel,
                "max_completion_tokens": max_tokens,
                "response_format": {"type": "json_object"},
                "messages": [{"role": "user", "content": prompt}],
            }
            if not self._mudel.startswith("gpt-5"):
                paring["temperature"] = temperature

            vastus = self._klient.chat.completions.create(**paring)
        except OpenAIError as e:
            raise ProviderError(f"OpenAI API viga: {e}") from e

        sisu = vastus.choices[0].message.content
        if not sisu:
            raise ProviderError("OpenAI tagastas tühja vastuse")
        return sisu
