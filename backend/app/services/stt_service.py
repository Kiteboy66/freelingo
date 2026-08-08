import io

import httpx
import openai

from app.core.app_logger import get_logger

logger = get_logger(__name__)

XHOSA_STT_TIMEOUT_SECONDS = 600.0


class WhisperSTTService:
    def __init__(self, base_url: str, xhosa_base_url: str | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.xhosa_base_url = xhosa_base_url.rstrip("/") if xhosa_base_url else None

    async def health(self) -> None:
        """Raise if Whisper ASR is unreachable."""
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{self.base_url}/", timeout=5.0)
            r.raise_for_status()

    async def transcribe(
        self,
        audio_bytes: bytes,
        filename: str = "audio.wav",
        mime_type: str = "audio/wav",
        language: str = "en",
    ) -> str:
        """Send audio to Whisper ASR and return the transcribed text.

        Compatible with onerahmet/openai-whisper-asr-webservice which exposes
        POST /asr?output=json&language=<code> (not the OpenAI /v1/audio/transcriptions path).
        """
        use_xhosa = language.lower().split("-")[0] == "xh"
        base_url = (
            self.xhosa_base_url if use_xhosa and self.xhosa_base_url else self.base_url
        )
        params = {"output": "json", "task": "transcribe"}
        if not use_xhosa:
            params["language"] = language

        async with httpx.AsyncClient() as client:
            logger.debug(
                "[stt] POST /asr — %d bytes, filename=%s lang=%s",
                len(audio_bytes),
                filename,
                language,
            )
            response = await client.post(
                f"{base_url}/asr",
                params=params,
                files={"audio_file": (filename, audio_bytes, mime_type)},
                # Swivuriso is lazy-loaded and its first request includes the
                # one-time model download on a fresh self-hosted install.
                timeout=XHOSA_STT_TIMEOUT_SECONDS if use_xhosa else 60.0,
            )
            logger.debug("[stt] Response status: %s", response.status_code)
            response.raise_for_status()
            data = response.json()
            # Response: {"text": "...", ...}
            text = data.get("text", "").strip()
            logger.info("[stt] Transcribed: %r", text)
            return text


class OpenAISTTService:
    def __init__(
        self,
        api_key: str,
        model: str,
        *,
        base_url: str | None = None,
        provider_name: str = "openai",
    ) -> None:
        self._client = openai.AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.provider_name = provider_name

    async def health(self) -> None:
        """Raise if the OpenAI-compatible STT API is unreachable."""
        await self._client.models.list()

    async def transcribe(
        self,
        audio_bytes: bytes,
        filename: str = "audio.wav",
        mime_type: str = "audio/wav",
        language: str = "en",
    ) -> str:
        """Transcribe audio using an OpenAI-compatible Whisper API."""
        audio_file = (filename, io.BytesIO(audio_bytes), mime_type)
        language_code = language.lower().split("-")[0]
        response = await self._client.audio.transcriptions.create(
            model=self.model,
            file=audio_file,
            language=language_code,
            timeout=60.0,
        )
        text = response.text.strip()
        logger.info("[stt-%s] Transcribed: %r", self.provider_name, text)
        return text


class GroqSTTService(OpenAISTTService):
    """Groq-hosted Whisper through its OpenAI-compatible endpoint."""

    def __init__(self, api_key: str, model: str) -> None:
        super().__init__(
            api_key,
            model,
            base_url="https://api.groq.com/openai/v1",
            provider_name="groq",
        )
