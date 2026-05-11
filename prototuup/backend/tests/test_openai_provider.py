from types import SimpleNamespace

from providers.openai_provider import OpenAIProvider


class FakeCompletions:
    def __init__(self) -> None:
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(
            choices=[
                SimpleNamespace(message=SimpleNamespace(content='{"leiud": []}')),
            ]
        )


class FakeClient:
    def __init__(self) -> None:
        self.completions = FakeCompletions()
        self.chat = SimpleNamespace(completions=self.completions)


def test_gpt5_paring_ei_saada_temperature_parameetrit():
    pakkuja = OpenAIProvider(mudel="gpt-5.5", api_key="test")
    klient = FakeClient()
    pakkuja._klient = klient

    assert pakkuja.kysi("prompt") == '{"leiud": []}'
    assert "temperature" not in klient.completions.kwargs


def test_muu_openai_mudel_saab_temperature_parameetri():
    pakkuja = OpenAIProvider(mudel="gpt-4.1", api_key="test")
    klient = FakeClient()
    pakkuja._klient = klient

    pakkuja.kysi("prompt", temperature=0.1)
    assert klient.completions.kwargs["temperature"] == 0.1
