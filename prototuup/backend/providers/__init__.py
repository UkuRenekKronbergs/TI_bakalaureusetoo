from .base import LLMProvider, ProviderError
from .demo_provider import DemoProvider

__all__ = ["LLMProvider", "ProviderError", "DemoProvider", "vali_pakkuja"]


def vali_pakkuja(mudeli_nimi: str) -> LLMProvider:
    if mudeli_nimi == "demo":
        return DemoProvider(mudel=mudeli_nimi)
    if mudeli_nimi.startswith("claude"):
        # Anthropic SDK on valikuline sõltuvus; impordime vajaduspõhiselt,
        # et demo-režiim töötaks ka ilma selle paketi paigaldamiseta.
        try:
            from .anthropic_provider import AnthropicProvider
        except ImportError as e:
            raise ProviderError(
                "Anthropic mudeli kasutamiseks tuleb paigaldada `anthropic` pakett."
            ) from e
        return AnthropicProvider(mudel=mudeli_nimi)
    if mudeli_nimi.startswith("gpt"):
        try:
            from .openai_provider import OpenAIProvider
        except ImportError as e:
            raise ProviderError(
                "OpenAI mudeli kasutamiseks tuleb paigaldada `openai` pakett."
            ) from e
        return OpenAIProvider(mudel=mudeli_nimi)
    raise ValueError(f"Tundmatu mudel: {mudeli_nimi}")
