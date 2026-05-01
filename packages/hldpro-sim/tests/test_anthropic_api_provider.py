import os

import pytest

from hldprosim.providers import AnthropicApiProvider


def test_anthropic_api_provider_requires_api_key_at_init(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
        AnthropicApiProvider()


@pytest.mark.skipif(not os.environ.get("ANTHROPIC_API_KEY"), reason="ANTHROPIC_API_KEY not set")
def test_anthropic_api_provider_instantiates_with_api_key():
    provider = AnthropicApiProvider()
    assert provider._api_key == os.environ["ANTHROPIC_API_KEY"]
