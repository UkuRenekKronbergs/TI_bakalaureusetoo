from abc import ABC, abstractmethod


class ProviderError(Exception):
    pass


class LLMProvider(ABC):
    @abstractmethod
    def kysi(self, prompt: str, *, max_tokens: int = 4096, temperature: float = 0.2) -> str:
        ...

    @property
    @abstractmethod
    def mudeli_nimi(self) -> str:
        ...
