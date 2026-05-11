from .base import LLMProvider, ProviderError
from .anthropic_provider import AnthropicProvider
from .openai_provider import OpenAIProvider

__all__ = ["LLMProvider", "ProviderError", "AnthropicProvider", "OpenAIProvider"]


def vali_pakkuja(mudeli_nimi: str) -> LLMProvider:
    if mudeli_nimi.startswith("claude"):
        return AnthropicProvider(mudel=mudeli_nimi)
    if mudeli_nimi.startswith("gpt"):
        return OpenAIProvider(mudel=mudeli_nimi)
    raise ValueError(f"Tundmatu mudel: {mudeli_nimi}")
