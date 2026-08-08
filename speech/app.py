"""Local isiXhosa speech service backed by Simba TTS and Swivuriso STT."""

from __future__ import annotations

import asyncio
import io
import os
import subprocess
import tempfile
import wave
from pathlib import Path
from typing import Annotated

import numpy as np
import torch
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, VitsModel

try:
    from faster_whisper import WhisperModel
except ImportError:  # The Railway image intentionally deploys TTS only.
    WhisperModel = None  # type: ignore[assignment,misc]

TTS_MODEL_ID = os.getenv("XHOSA_TTS_MODEL", "UBC-NLP/Simba-TTS-xho")
STT_MODEL_ID = os.getenv("XHOSA_STT_MODEL", "digiphyte/swivuriso-turbo")
DEVICE = os.getenv("SPEECH_DEVICE", "auto")
STT_ENABLED = os.getenv("SPEECH_STT_ENABLED", "true").lower() in {"1", "true", "yes"}

app = FastAPI(title="FreeLingo isiXhosa Speech", version="1.0.0")

_tts_model: VitsModel | None = None
_tts_tokenizer = None
_stt_model: object | None = None
_tts_lock = asyncio.Lock()
_stt_lock = asyncio.Lock()


class SpeechRequest(BaseModel):
    model: str = TTS_MODEL_ID
    input: str = Field(min_length=1, max_length=5000)
    voice: str | None = None
    response_format: str = "mp3"


def _torch_device() -> str:
    if DEVICE != "auto":
        return DEVICE
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def _whisper_device() -> tuple[str, str]:
    device = _torch_device()
    if device == "mps":
        return "cpu", "int8"
    return (device, "float16") if device == "cuda" else ("cpu", "int8")


async def _load_tts() -> tuple[VitsModel, object]:
    global _tts_model, _tts_tokenizer
    if _tts_model is None or _tts_tokenizer is None:
        async with _tts_lock:
            if _tts_model is None or _tts_tokenizer is None:
                device = _torch_device()
                _tts_tokenizer = await asyncio.to_thread(
                    AutoTokenizer.from_pretrained, TTS_MODEL_ID
                )
                model = await asyncio.to_thread(VitsModel.from_pretrained, TTS_MODEL_ID)
                _tts_model = model.to(device).eval()
    return _tts_model, _tts_tokenizer


async def _load_stt():
    global _stt_model
    if not STT_ENABLED:
        raise RuntimeError(
            "Local STT is disabled; use the configured hosted STT provider"
        )
    if WhisperModel is None:
        raise RuntimeError("faster-whisper is not installed in this image")
    if _stt_model is None:
        async with _stt_lock:
            if _stt_model is None:
                device, compute_type = _whisper_device()
                _stt_model = await asyncio.to_thread(
                    WhisperModel,
                    STT_MODEL_ID,
                    device=device,
                    compute_type=compute_type,
                )
    return _stt_model


def _wav_bytes(samples: np.ndarray, sample_rate: int) -> bytes:
    normalized = np.clip(samples, -1.0, 1.0)
    pcm = (normalized * 32767).astype("<i2").tobytes()
    output = io.BytesIO()
    with wave.open(output, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm)
    return output.getvalue()


def _mp3_bytes(wav_bytes: bytes) -> bytes:
    result = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            "pipe:0",
            "-f",
            "mp3",
            "-codec:a",
            "libmp3lame",
            "-q:a",
            "3",
            "pipe:1",
        ],
        input=wav_bytes,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0 or not result.stdout:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


@app.get("/")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "tts_model": TTS_MODEL_ID,
        "stt_model": STT_MODEL_ID if STT_ENABLED else "disabled",
    }


@app.get("/v1/models")
async def models() -> dict[str, list[dict[str, str]]]:
    models = [{"id": TTS_MODEL_ID}]
    if STT_ENABLED:
        models.append({"id": STT_MODEL_ID})
    return {"data": models}


@app.post("/v1/audio/speech")
async def synthesize(body: SpeechRequest) -> Response:
    if body.response_format not in {"mp3", "wav"}:
        raise HTTPException(
            status_code=400, detail="response_format must be mp3 or wav"
        )
    try:
        model, tokenizer = await _load_tts()
        device = _torch_device()
        encoded = tokenizer(body.input.strip(), return_tensors="pt")
        encoded = {name: tensor.to(device) for name, tensor in encoded.items()}
        with torch.inference_mode():
            waveform = (
                model(**encoded).waveform.squeeze().detach().float().cpu().numpy()
            )
        wav_audio = await asyncio.to_thread(
            _wav_bytes, waveform, int(model.config.sampling_rate)
        )
        if body.response_format == "wav":
            return Response(wav_audio, media_type="audio/wav")
        mp3_audio = await asyncio.to_thread(_mp3_bytes, wav_audio)
        return Response(mp3_audio, media_type="audio/mpeg")
    except Exception as exc:
        raise HTTPException(
            status_code=503, detail=f"isiXhosa TTS failed: {exc}"
        ) from exc


def _transcribe_file(model: object, path: str) -> str:
    # Swivuriso extends Whisper with South African languages that faster-whisper's
    # language allow-list does not know. Auto-detection is therefore intentional.
    segments, _info = model.transcribe(  # type: ignore[attr-defined]
        path, language=None, beam_size=5, vad_filter=True
    )
    return " ".join(segment.text.strip() for segment in segments).strip()


@app.post("/asr")
async def transcribe(
    audio_file: Annotated[UploadFile, File()],
    output: Annotated[str, Query()] = "json",
    task: Annotated[str, Query()] = "transcribe",
) -> JSONResponse:
    if not STT_ENABLED:
        raise HTTPException(status_code=404, detail="Local STT is disabled")
    if output != "json" or task != "transcribe":
        raise HTTPException(
            status_code=400, detail="Only JSON transcription is supported"
        )
    suffix = Path(audio_file.filename or "audio.wav").suffix or ".wav"
    data = await audio_file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Audio file is empty")
    temp_path = ""
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
            temp_file.write(data)
            temp_path = temp_file.name
        model = await _load_stt()
        text = await asyncio.to_thread(_transcribe_file, model, temp_path)
        return JSONResponse({"text": text})
    except Exception as exc:
        raise HTTPException(
            status_code=503, detail=f"isiXhosa STT failed: {exc}"
        ) from exc
    finally:
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)
