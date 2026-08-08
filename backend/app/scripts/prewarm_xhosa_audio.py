"""Generate and persist every audio clip used by the guided isiXhosa sprint."""

from __future__ import annotations

import asyncio
import hashlib
import os
import uuid

from app.data.xh.guided_course import GUIDED_XHOSA_A1_DAYS


def _course_texts() -> list[str]:
    return sorted(
        {
            *(phrase.text for guided_day in GUIDED_XHOSA_A1_DAYS for phrase in guided_day.phrases),
            *(line.text for guided_day in GUIDED_XHOSA_A1_DAYS for line in guided_day.dialogue),
        }
    )


def _cache_path(text: str, audio_storage_path: str) -> str:
    cache_key = hashlib.sha256(f"xh-ZA::{text}".encode()).hexdigest()[:24]
    return os.path.join(audio_storage_path, "tts", "xh", f"{cache_key}.mp3")


async def main() -> None:
    from app.core.config import settings  # noqa: PLC0415
    from app.services.tts_service import KokoroTTSService  # noqa: PLC0415

    if not settings.XHOSA_SPEECH_BASE_URL:
        raise RuntimeError("XHOSA_SPEECH_BASE_URL is not configured")

    service = KokoroTTSService(
        settings.TTS_BASE_URL,
        settings.TTS_VOICE,
        settings.XHOSA_SPEECH_BASE_URL,
    )
    texts = _course_texts()
    generated = 0
    cached = 0

    for index, text in enumerate(texts, start=1):
        path = _cache_path(text, settings.AUDIO_STORAGE_PATH)
        if os.path.isfile(path):
            cached += 1
            print(f"[{index}/{len(texts)}] cached")
            continue

        audio = await service.synthesize(text, language="xh-ZA")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        temporary_path = f"{path}.{uuid.uuid4().hex}.tmp"
        with open(temporary_path, "wb") as audio_file:  # noqa: PTH123
            audio_file.write(audio)
        os.replace(temporary_path, path)
        generated += 1
        print(f"[{index}/{len(texts)}] generated ({len(audio)} bytes)")

    print(f"Ready: {len(texts)} clips ({generated} generated, {cached} already cached)")


if __name__ == "__main__":
    asyncio.run(main())
