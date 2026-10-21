"""Module 2. F7: the API key must come from the environment, never from the code."""

from pathlib import Path

import pytest

from fieldreports import config

PACKAGE = Path(config.__file__).resolve().parent


def test_flaw_F7_api_key_comes_from_the_environment(monkeypatch):
    monkeypatch.delenv("CREWBOOK_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="CREWBOOK_API_KEY"):
        config.get_api_key()
    monkeypatch.setenv("CREWBOOK_API_KEY", "from-the-environment")
    assert config.get_api_key() == "from-the-environment"
    for source in PACKAGE.glob("*.py"):
        assert "crewbook_live_" not in source.read_text(encoding="utf-8"), source.name
