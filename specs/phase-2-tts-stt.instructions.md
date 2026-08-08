---
description: "Phase 2 specification for FreeLingo: local TTS (Kokoro-FastAPI) and STT (faster-whisper) integration with pronunciation exercises, flashcard speaking mode, and frontend audio components."
---

# Phase 2 — Local TTS and STT

## Objective

Add fully local voice synthesis (TTS) and speech recognition (STT) with no external API dependencies. English uses Kokoro and Whisper; isiXhosa uses Simba TTS and Swivuriso STT through the combined `xhosa-speech` service. All speech remains behind backend proxies.

---

## Service architecture

```
Browser                          Backend                      Docker services
┌──────────┐    HTTP    ┌──────────────────────┐   HTTP    ┌───────────────┐
│AudioPlayer│ ────────→ │ POST /api/tts        │ ────────→ │ Kokoro-FastAPI│
│          │ ←──────── │ (audio/mpeg binary)   │ ←──────── │ :8880         │
└──────────┘            │                      │           └───────────────┘
                        │ apps/core/tts_service│
┌──────────┐    HTTP    │                      │   HTTP    ┌───────────────┐
│VoiceRec- │ ────────→ │ POST /api/stt        │ ────────→ │ Whisper ASR   │
│ order    │ ←──────── │ (multipart/form-data) │ ←──────── │ :9000         │
└──────────┘            └──────────────────────┘           └───────────────┘
```

The backend acts as the sole gateway — the frontend never calls Kokoro, Whisper, Simba, Swivuriso, Groq, or OpenAI directly. `TTS_PROVIDER` selects `local` (default) or `openai`; `STT_PROVIDER` selects `local`, `groq`, or `openai`. The former boolean `TTS_ENABLED` and `STT_ENABLED` flags no longer exist.

For a local `xh` request, `KokoroTTSService` and `WhisperSTTService` route to `XHOSA_SPEECH_BASE_URL`. `speech/app.py` lazy-loads `UBC-NLP/Simba-TTS-xho` for MP3 synthesis and `digiphyte/swivuriso-turbo` for transcription, and caches Hugging Face files in the Compose data path. The default Compose service runs on CPU; automatic CUDA selection works when a GPU is exposed to the container, and direct host runs can use MPS for TTS.

---

## TTS Service — Kokoro-FastAPI

### Docker service

- **Image**: `ghcr.io/remsky/kokoro-fastapi-gpu:latest` (default, CUDA GPU)
- **CPU image**: `ghcr.io/remsky/kokoro-fastapi-cpu:latest` (remove `deploy` block for CPU hosts)
- **API**: OpenAI TTS-compatible (`POST /v1/audio/speech`)
- **Parameters**: `model`, `input` (text), `voice`, `response_format` (mp3)
- **Available voices**: `af_heart`, `af_sky`, `bf_emma`, `bm_george`, and others
- **Audio format**: MP3 return
- **Performance**: GPU strongly recommended; CPU fallback works but with significant speed degradation

### Backend integration (`app/services/tts_service.py`)

The `TTSService` class wraps the Kokoro HTTP API:

- `synthesize(text, voice, language)` → returns raw MP3 bytes
- HTTP POST to `{base_url}/v1/audio/speech` with JSON body
- 30-second timeout for Kokoro; 300 seconds for a cold isiXhosa model download
- Raises on non-2xx responses

### Backend router (`app/routers/tts.py`)

- **Endpoint**: `POST /api/tts`
- **Rate limit**: 20 requests/minute
- **Request**: `{ "text": string, "voice": string?, "language": string? }`
- **Response**: `audio/mpeg` binary content
- **Auth**: Requires valid access token
- **Guard**: Returns 503 if the configured TTS service is unavailable
- **Voice preview text**: OpenAI voice previews introduce the AI tutor as Lingu, using the shared `TUTOR_DISPLAY_NAME` prompt constant.
- **isiXhosa cache**: when `TTS_CACHE_ENABLED=true`, successful `xh`/`xh-ZA` MP3s are content-addressed by text, voice, and language under `AUDIO_STORAGE_PATH/tts/xh`.

---

## STT Service — Whisper ASR

### Docker service

- **Image**: `onerahmet/openai-whisper-asr-webservice:latest-gpu` (default, CUDA GPU)
- **CPU image**: `onerahmet/openai-whisper-asr-webservice:latest` (remove `deploy` block; use smaller model)
- **API**: **NOT** OpenAI-compatible — uses custom endpoint `POST /asr?output=json&language=en&task=transcribe`
- **Form field**: `audio_file` (multipart file upload with filename)
- **Default model**: `large-v3-turbo` (best speed/accuracy ratio, ~8× faster than `large-v3`)
- **Engine**: `faster_whisper` or `ctranslate2`, controlled via `STT_ENGINE` env variable

> **Important**: The STT endpoint was corrected in v1.2.0 from the nonexistent OpenAI-compatible `/v1/audio/transcriptions` to the actual `/asr` endpoint of the `onerahmet/openai-whisper-asr-webservice` image. The OpenAI API format is not supported by this service.

### Backend integration (`app/services/stt_service.py`)

The `STTService` class wraps the Whisper HTTP API:

- `transcribe(audio_bytes, filename, mime_type, language)` → returns transcribed text string
- HTTP POST to `POST /asr?output=json&language=en&task=transcribe`
- Multipart upload with `audio_file` field
- 60-second timeout for Whisper; 600 seconds for a cold isiXhosa model download
- Raises on non-2xx responses

`GroqSTTService` uses Groq's OpenAI-compatible transcription endpoint with `GROQ_STT_MODEL` (default `whisper-large-v3`) and normalizes BCP-47 language values such as `xh-ZA` to `xh`.

### Backend router (`app/routers/stt.py`)

- **Endpoint**: `POST /api/stt`
- **Rate limit**: 20 requests/minute
- **Request**: `multipart/form-data` with `audio` field (binary audio file) and optional `language` ISO code
- **Response**: `{ "text": string }`
- **Auth**: Requires valid access token
- **Guard**: Returns 503 if the configured STT service is unavailable

---

## Environment variables (`.env` additions)

- `TTS_PROVIDER` — Default: `local`; Purpose: Select local or OpenAI TTS
- `TTS_BASE_URL` — Default: `http://kokoro:8880`; Purpose: Kokoro service URL
- `TTS_VOICE` — Default: `af_heart`; Purpose: Default TTS voice
- `STT_PROVIDER` — Default: `local`; Purpose: Select local, Groq, or OpenAI STT
- `STT_BASE_URL` — Default: `http://whisper:9000`; Purpose: Whisper service URL
- `XHOSA_SPEECH_BASE_URL` — Default: `http://xhosa-speech:9100`; Purpose: Simba/Swivuriso service URL
- `XHOSA_TTS_MODEL` — Default: `UBC-NLP/Simba-TTS-xho`; Purpose: isiXhosa TTS model used by the speech container
- `XHOSA_STT_MODEL` — Default: `digiphyte/swivuriso-turbo`; Purpose: South African multilingual STT model used by the speech container
- `XHOSA_SPEECH_DEVICE` — Default: `auto`; Purpose: `auto`, `cpu`, `cuda`, or `mps`
- `STT_MODEL` — Default: `large-v3-turbo`; Purpose: Whisper model (also: `tiny.en`, `small`, `medium`, `large-v3`)
- `STT_ENGINE` — Default: `faster_whisper`; Purpose: Inference engine (`faster_whisper` or `ctranslate2`)
- `GROQ_API_KEY` — Default: empty; Purpose: Authenticate hosted Groq transcription
- `GROQ_STT_MODEL` — Default: `whisper-large-v3`; Purpose: Groq transcription model
- `TTS_CACHE_ENABLED` — Default: `true`; Purpose: Reuse persisted isiXhosa pronunciation MP3s

Voice conversation requires both configured providers to be reachable. isiXhosa local conversation additionally requires `xhosa-speech`.

The Railway speech image is intentionally TTS-only (`SPEECH_STT_ENABLED=false`) and excludes faster-whisper. It pairs Simba with Groq STT, stores Hugging Face model files on `/models/huggingface`, and relies on the backend `/data` volume for generated MP3 caching. The language-aware conversation warmup sends `target_language`; isiXhosa gets a 300-second client timeout for a sleeping or first-download Simba service.

---

## Frontend components

### AudioPlayer (`components/ui/AudioPlayer.tsx`)

Reusable button component for TTS playback:

- Calls `POST /api/tts` with text, active language, and optional voice override
- Receives `audio/mpeg` binary
- Plays via browser `Audio` API (`new Audio(blobUrl).play()`)
- Cleans up `ObjectURL` on playback end
- Shows loading spinner during TTS generation

Used in:

- **Flashcards**: 🔊 button on each card for word pronunciation
- **Lessons**: 🔊 button on example sentences and vocabulary items
- **Pronunciation exercises**: the target sentence always has audio

### VoiceRecorder (`components/ui/VoiceRecorder.tsx`)

Reusable button component for STT recording:

- Requests microphone via `navigator.mediaDevices.getUserMedia({ audio: true })`
- Records audio using `MediaRecorder` API (codec: `audio/webm`)
- Maximum recording length: configurable via `maxSeconds` prop (default 5 s for exercises, unlimited for conversation)
- Stops automatically after max duration
- Uploads audio plus the active ISO language via `POST /api/stt` as multipart/form-data
- Returns transcribed text to parent component
- Shows recording indicator (animated red dot)

---

## Pronunciation exercises

### New exercise type: `pronunciation`

Added to the exercise mix in lesson content. Properties:

- `target_sentence`: the English text to pronounce
- `hint`: guidance about the sound or pattern to practice (e.g. "Focus on the 'th' sound")

User flow:

1. Student sees the target sentence
2. Presses 🔊 to hear the correct pronunciation (TTS)
3. Presses microphone button to record their own pronunciation
4. Recording is sent to `/api/stt` for transcription
5. Transcribed text is compared to the target sentence by the LLM
6. Score (0.0–1.0) and detailed feedback are returned

The pronunciation evaluation prompt (`PRONUNCIATION_EVAL_PROMPT` in `services/lesson_generator.py`) instructs the LLM to assess the match between expected and transcribed text, accounting for phonetic similarity and common pronunciation errors for the student's native language.

### Scoring guidelines

- 0.9–1.0 — Meaning: Excellent; Criteria: Near-native pronunciation, all phonemes correct
- 0.7–0.89 — Meaning: Good; Criteria: Minor errors, understandable
- 0.4–0.69 — Meaning: Needs work; Criteria: Several phoneme errors, still intelligible
- 0.0–0.39 — Meaning: Poor; Criteria: Mostly unintelligible or no speech detected

---

## Flashcards speaking mode

An additional review mode on the `/flashcards` page:

- Shows the English definition (not the word)
- User speaks the word aloud
- STT transcribes the audio
- Transcription is compared to the correct word
- SM-2 quality rating derived from the match: `5` for exact match, `2` for incorrect
- Works alongside standard mode (written recall)

---

## Frontend API proxies

Both TTS and STT use dedicated Next.js Route Handlers to avoid issues with Next.js rewrites buffering or transforming binary/multipart data:

- TTS — Route Handler: `src/app/api/tts/route.ts`; Purpose: Forwards binary audio without transformation
- STT — Route Handler: `src/app/api/stt/route.ts`; Purpose: Forwards multipart form-data preserving file attachment

Both proxies attach the `Authorization` header from the auth store and forward the response body unchanged.

---

## GPU vs CPU

Both services default to GPU images with CUDA support. For CPU-only hosts:

- Kokoro TTS — CPU image: `ghcr.io/remsky/kokoro-fastapi-cpu:latest`; Additional changes: Remove the `deploy.resources.reservations.devices` block
- Whisper STT — CPU image: `onerahmet/openai-whisper-asr-webservice:latest`; Additional changes: Remove the `deploy` block; set `STT_MODEL=tiny.en` or `small` for acceptable performance

The `deploy` block must be removed entirely on CPU hosts — Docker will error if it references NVIDIA devices without the NVIDIA runtime installed.

---

## Phase 2 completion criteria (all met by v1.2.0)

- [x] Kokoro returns audio correctly from the backend (`POST /api/tts`)
- [x] Whisper transcribes browser-recorded audio correctly (`POST /api/stt`)
- [x] STT endpoint uses correct API: `POST /asr?output=json&language=en&task=transcribe` (not OpenAI API)
- [x] Audio button functional in flashcards and lessons
- [x] Pronunciation recording and evaluation operational
- [x] Flashcard speaking mode functional
- [x] Frontend API proxies handle binary and multipart correctly
- [x] Provider availability guards return 503 when a configured speech service is unavailable
- [x] isiXhosa local requests route to Simba TTS and Swivuriso STT with no paid API
- [x] GPU used by both services (CPU-only hosts supported with compose changes)
- [x] No regressions in Phase 1 features
