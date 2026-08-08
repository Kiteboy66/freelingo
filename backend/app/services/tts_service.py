import asyncio
import time

import httpx
import openai

from app.core.app_logger import get_logger

logger = get_logger(__name__)

XHOSA_TTS_TIMEOUT_SECONDS = 300.0
XHOSA_TTS_WAKE_RETRY_DELAYS_SECONDS = (1.0, 2.0, 4.0, 8.0, 12.0, 15.0, 15.0, 15.0)
XHOSA_TTS_WAKE_STATUS_CODES = frozenset({502, 503, 504})


class KokoroTTSService:
    def __init__(self, base_url: str, voice: str, xhosa_base_url: str | None = None) -> None:
        self.base_url = base_url
        self.voice = voice
        self.xhosa_base_url = xhosa_base_url.rstrip("/") if xhosa_base_url else None

    async def health(self) -> None:
        """Raise if Kokoro is unreachable."""
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{self.base_url}/v1/models", timeout=5.0)
            r.raise_for_status()

    async def synthesize(
        self, text: str, voice: str | None = None, language: str | None = None
    ) -> bytes:
        """Call Kokoro-FastAPI and return MP3 audio bytes."""
        use_xhosa = bool(language and language.lower().split("-")[0] == "xh")
        base_url = self.xhosa_base_url if use_xhosa and self.xhosa_base_url else self.base_url
        model = "UBC-NLP/Simba-TTS-xho" if use_xhosa else "kokoro"
        async with httpx.AsyncClient() as client:
            request = {
                "model": model,
                "input": text,
                "voice": voice or self.voice,
                "response_format": "mp3",
            }
            retry_delays = XHOSA_TTS_WAKE_RETRY_DELAYS_SECONDS if use_xhosa else ()
            for attempt in range(len(retry_delays) + 1):
                try:
                    response = await client.post(
                        f"{base_url}/v1/audio/speech",
                        json=request,
                        # The first local isiXhosa request may need to wake the
                        # Railway service, download the model, and initialise
                        # Simba TTS. Warm requests are much faster.
                        timeout=XHOSA_TTS_TIMEOUT_SECONDS if use_xhosa else 30.0,
                    )
                    if (
                        use_xhosa
                        and response.status_code in XHOSA_TTS_WAKE_STATUS_CODES
                        and attempt < len(retry_delays)
                    ):
                        await asyncio.sleep(retry_delays[attempt])
                        continue
                    break
                except httpx.ConnectError, httpx.ConnectTimeout:
                    if attempt >= len(retry_delays):
                        raise
                    await asyncio.sleep(retry_delays[attempt])
            response.raise_for_status()
            return response.content


class OpenAITTSService:
    def __init__(
        self,
        api_key: str,
        model: str,
        voice: str,
        speed: float = 1.0,
        timeout: float | None = None,
    ) -> None:
        self._client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model
        self.voice = voice
        self.speed = speed
        self.timeout = timeout

    async def health(self) -> None:
        """Raise if OpenAI TTS is unreachable (lightweight models list call)."""
        await self._client.models.list()

    async def synthesize(
        self, text: str, voice: str | None = None, language: str | None = None
    ) -> bytes:
        """Call OpenAI TTS API and return MP3 audio bytes."""
        _ = language
        text = text.strip()
        if not text:
            logger.warning("[tts-openai] Empty text received for synthesis")
            return b""

        req_voice = (voice or self.voice).strip()
        input_len = len(text)
        start_t = time.perf_counter()
        logger.info(
            "[tts-openai] request_start model=%s voice=%s chars=%d",
            self.model,
            req_voice,
            input_len,
        )
        request_payload = {
            "model": self.model,
            "voice": req_voice,
            "input": text,
            "response_format": "mp3",
            "speed": self.speed,
        }
        if self.timeout is not None:
            request_payload["timeout"] = self.timeout

        response = await self._client.audio.speech.create(**request_payload)
        audio = response.content
        if not audio:
            raise RuntimeError("OpenAI TTS returned empty audio payload")
        elapsed_ms = (time.perf_counter() - start_t) * 1000
        request_id = getattr(response, "request_id", None)
        if request_id is None:
            headers = getattr(response, "headers", None)
            if headers is not None:
                request_id = headers.get("x-request-id")
        logger.info(
            "[tts-openai] request_ok model=%s voice=%s chars=%d bytes=%d ms=%.1f request_id=%s",
            self.model,
            req_voice,
            input_len,
            len(audio),
            round(elapsed_ms, 1),
            request_id,
        )
        return audio
