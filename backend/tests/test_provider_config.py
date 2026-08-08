from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from app.core.config import Settings, settings
from app.main import app
from app.services.stt_service import GroqSTTService


def _settings(database_url: str) -> Settings:
    return Settings(
        DATABASE_URL=database_url,
        SECRET_KEY="x" * 32,
    )


def test_neon_database_url_is_normalized_for_asyncpg() -> None:
    settings = _settings(
        "postgresql://user:pass@example.neon.tech/db" "?sslmode=require&channel_binding=require"
    )

    assert settings.DATABASE_URL == (
        "postgresql+asyncpg://user:pass@example.neon.tech/db?ssl=require"
    )


def test_existing_async_database_url_is_preserved() -> None:
    settings = _settings("postgresql+asyncpg://user:pass@postgres/db")

    assert settings.DATABASE_URL == "postgresql+asyncpg://user:pass@postgres/db"


def test_groq_stt_uses_openai_compatible_endpoint() -> None:
    service = GroqSTTService("groq-test", "whisper-large-v3")

    assert service.model == "whisper-large-v3"
    assert service.provider_name == "groq"
    assert str(service._client.base_url) == "https://api.groq.com/openai/v1/"


@pytest.mark.asyncio
async def test_groq_stt_normalizes_bcp47_language_code() -> None:
    service = GroqSTTService("groq-test", "whisper-large-v3")
    service._client.audio.transcriptions.create = AsyncMock(
        return_value=SimpleNamespace(text="  Molo  ")
    )

    result = await service.transcribe(b"wav", language="xh-ZA")

    assert result == "Molo"
    service._client.audio.transcriptions.create.assert_awaited_once()
    request = service._client.audio.transcriptions.create.await_args.kwargs
    assert request["language"] == "xh"
    assert request["model"] == "whisper-large-v3"


@pytest.mark.asyncio
async def test_xhosa_tts_audio_is_cached(client, test_user, tmp_path) -> None:
    _user, headers = test_user
    tts_service = SimpleNamespace(synthesize=AsyncMock(return_value=b"mp3-audio"))
    had_previous_service = hasattr(app.state, "tts_service")
    previous_service = getattr(app.state, "tts_service", None)
    app.state.tts_service = tts_service

    try:
        with (
            patch.object(settings, "AUDIO_STORAGE_PATH", str(tmp_path)),
            patch.object(settings, "TTS_CACHE_ENABLED", True),
            patch.object(settings, "TTS_PROVIDER", "local"),
        ):
            first = await client.post(
                "/api/tts",
                headers=headers,
                json={"text": "Molo", "language": "xh-ZA"},
            )
            second = await client.post(
                "/api/tts",
                headers=headers,
                json={"text": "Molo", "language": "xh-ZA"},
            )
    finally:
        if had_previous_service:
            app.state.tts_service = previous_service
        else:
            del app.state.tts_service

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.content == b"mp3-audio"
    assert second.content == b"mp3-audio"
    tts_service.synthesize.assert_awaited_once_with("Molo", None, "xh-ZA")
