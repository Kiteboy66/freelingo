![Hosted](https://img.shields.io/badge/hosted%20service-available-green?style=flat-square)
![License](https://img.shields.io/badge/license-AGPL%20v3-blue?style=flat-square)
![Next.js](https://img.shields.io/badge/next.js-16-black?style=flat-square)
![Python](https://img.shields.io/badge/python-3.14-blue?style=flat-square)
![Self-hosted](https://img.shields.io/badge/self--hosted-yes-orange?style=flat-square)
![Version](https://img.shields.io/badge/version-1.9.0-brightgreen?style=flat-square)

<p align="left">
  <img src="assets/logo_large.png" alt="FreeLingo logo" />
</p>

Open source AI language learning platform available in two modes: self-hosted (free, run it on your own
infrastructure) and as a hosted service operated by the FreeLingo team with a free plan and paid subscriptions.
A language model evaluates your CEFR level, generates a personalized study plan, and guides you through
grammar, vocabulary, reading comprehension, writing lessons, AI-generated listening exercises, and AI-generated reading exercises — with optional voice features.

The study plan follows a CEFR-aligned curriculum (A1-C2) organized into units with
clear competencies and prerequisites. After a deterministic placement assessment,
FreeLingo creates a weekly roadmap based on your selected intensity (2, 4, 8, 12, or
16 weeks), then unlocks lessons in sequence: grammar, vocabulary, reading, writing,
and review.

isiXhosa (`xh-ZA`) is available as a conversation-first **A1 two-week sprint**. It is intentionally scoped to the content that exists today rather than claiming unsupported A2–C2 coverage: 13 guided practice sessions, pronunciation of the `c`/`q`/`x` click families, and a final basic-conversation check.

The platform combines structure and adaptation: lessons are generated within
curriculum boundaries with native-language support for lesson and exercise explanations,
flashcards use SM-2 spaced repetition, and the AI tutor provides contextual streaming
feedback in English (with optional brief support in the learner's native language).
Lingu's durable memories are global across learning languages: the tutor can save useful facts through native tool calling, while every authenticated user can manually add, review, delete, or clear memories from Settings. Removing a learning language preserves those account memories.
Listening exercises are generated on demand by the
LLM, synthesised to MP3 via TTS, and cached per CEFR level — the user listens,
answers 5 comprehension questions, and earns XP before the transcript is revealed.
Reading exercises follow the same caching model but without audio — the AI generates
a passage and 5 comprehension questions displayed side by side; the user reads and
answers immediately, earning XP per correct answer.
Progress tracking includes XP, streaks, skill scores, unit competencies, and an
end-of-level completion test.

## Hosted service

> **Don't want to manage your own server?**  
> FreeLingo is available as a fully managed hosted service at **[freelingo.app](https://freelingo.app)**.

Sign up, start with a free plan, or upgrade to a subscription for unlimited access — no Docker, no GPU, no maintenance required.
The hosted instance is operated by the FreeLingo team and always runs the latest stable version.

Self-hosting remains free and open source under the AGPL-3.0 licence. The hosted service exists for users who prefer a managed experience.

## For businesses

Need FreeLingo for your team or organisation?

- **Private / on-premise deployment** — Deploy FreeLingo on your own infrastructure with full control over data and configuration. Ideal for schools, language academies, and companies with data-sovereignty requirements.
- **Dedicated managed instance** — A turnkey deployment operated exclusively for your organisation: setup, hosting, maintenance, and updates included. Your data stays isolated in a dedicated environment.
- **Commercial licence** — Organisations that need to deploy a customised or white-labelled version without the open-source obligations of the AGPL can obtain a commercial licence. See [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md) for details.

[Get in touch](https://freelingo.app) via the contact form to discuss your requirements.

If FreeLingo is useful to you or your organisation, consider [**sponsoring the project on GitHub**](https://github.com/sponsors/artcc) to support continued development and keep the self-hosted version free for everyone.

---

## Architecture

Monorepo: `backend/` (Python FastAPI) + `frontend/` (Next.js 16 App Router)
deployed via Docker Compose with PostgreSQL 16 and Redis 7.
The backend proxies all external services (Ollama, Kokoro, Whisper, and the local isiXhosa speech service) —
the frontend never calls them directly.

## Repository

```
freelingo/
├── assets/                          # Logos and static assets
├── backend/                         # FastAPI (Python)
├── data/                            # Shared data files
├── docs/                            # GitHub Pages landing site
├── frontend/                        # Next.js (React)
├── messages/                        # i18n translation files (de, en, es, fr, it, nl, pl, pt, ro, ru)
├── speech/                          # Local isiXhosa Simba TTS + Swivuriso STT service
├── specs/                           # Specification files
├── AGENTS.md                        # AI assistant instructions
├── CHANGELOG.md                     # Version history
├── CODE_OF_CONDUCT.md               # Community guidelines
├── COMMERCIAL_LICENSE.md            # Commercial licence terms
├── CONTRIBUTING.md                  # Contribution guidelines
├── CONTRIBUTOR_LICENSE_AGREEMENT.md # CLA for contributors
├── DEVELOPMENT.md                   # Local development setup
├── docker-compose.yml               # Production deployment
├── docker-compose.dev.yml           # Development deployment
├── LICENSE                          # AGPL-3.0 licence
├── README.md                        # This file
└── run-dev.sh                       # Development helper script
```

## Stack

| Layer    | Technology                                               |
| -------- | -------------------------------------------------------- |
| Frontend | Next.js 16+, shadcn/ui, Tailwind CSS, Zustand, next-intl |
| Backend  | FastAPI, SQLAlchemy async, Alembic, Pydantic v2          |
| Database | PostgreSQL 16                                            |
| Cache    | Redis 7                                                  |
| LLM      | Ollama (local) · Gemini · OpenAI · Anthropic · DeepSeek  |
| TTS      | Kokoro-FastAPI · Simba isiXhosa (local) · OpenAI TTS API |
| STT      | faster-whisper · Swivuriso isiXhosa (local) · Groq · OpenAI |
| Auth     | JWT (access + refresh), multi-user, roles (admin/user).  |
| Deploy   | Docker Compose · Railway                                 |

## Phases

| Phase | Name                    | Status      |
| ----- | ----------------------- | ----------- |
| 1     | Learning platform       | ✅ Complete |
| 1+    | Learning Resources Hub  | ✅ Complete |
| 2     | Local TTS + STT         | ✅ Complete |
| 3     | Real-time conversation  | ✅ Complete |
| 4     | Multi-language support  | ✅ Complete |
| 5     | Stripe subscriptions    | ✅ Complete |
| 6     | Listening               | ✅ Complete |
| 7     | Reading                 | ✅ Complete |
| 8     | Feedback board          | ✅ Complete |
| 9     | Memory                  | ✅ Complete |
| 10    | Multi-Language Learning | ✅ Complete |
| 11    | User reviews            | ✅ Complete |

## Quick start

### Option A — Git clone + Docker Compose

**Requirements:** Docker, Docker Compose, Git, and [Ollama](https://ollama.com) running on the host.

```bash
# 1. Clone the repository
git clone https://github.com/artcc/freelingo.git
cd freelingo

# 2. Configure environment
cp .env.example .env
# Edit .env: set OLLAMA_BASE_URL, choose your model, and review other settings

# 3. Pull the recommended model (run on the host, not inside Docker)
ollama pull gemma4:e4b

# 4. Start all services (migrations run automatically on first start)
docker compose up -d
```

Access at `http://localhost:3000` (or `http://<server-ip>:3000`).  
The first registered user becomes admin automatically.

---

### Option B — Portainer (Stack)

1. Open Portainer → **Stacks** → **Add stack**.
2. Choose **Repository** and enter the repo URL, or paste the contents of `docker-compose.yml` directly into the Web editor.
3. Scroll down to **Environment variables** and add the variables from `.env.example` (at minimum: `SECRET_KEY`, `OLLAMA_BASE_URL`, `POSTGRES_PASSWORD`).
4. Click **Deploy the stack**.
5. Access the app at `http://<server-ip>:3000`. Database migrations run automatically when the backend starts.

> **Tip:** If Ollama runs on the same host as Portainer, set `OLLAMA_BASE_URL=http://host.docker.internal:11434`. On Linux you may need to add the `extra_hosts` entry in the compose file (already included by default).

## Operational notes

- The recommended model for Ollama is `gemma4:e4b`. It can be changed in `.env`.
- The backend acts as a proxy for Ollama/TTS/STT calls so the frontend never talks directly to those services.
- The `LLM_PROVIDER` field controls the LLM provider: `ollama`, `gemini`, `openai`, `anthropic`, or `deepseek`. The free-first Railway profile uses Gemini.
- `TTS_PROVIDER` and `STT_PROVIDER` are independent. TTS supports `local` or `openai`; STT supports `local`, `groq`, or `openai`.
- New-user and subscription quota defaults are configurable in `.env` with `DEFAULT_CONVERSATION_*`, `DEFAULT_MONTHLY_TOKENS_LIMIT`, and `ASSESSMENT_VOICE_TRIAL_DURATION_SECONDS`. Quota values of `0` mean unlimited. Conversation duration defaults must use the same supported options as the settings UI: `900` or `1800` seconds for max duration, and `60`, `180`, or `300` seconds for inactivity timeout.
- Freemium quotas for the hosted free plan are configurable via `FREEMIUM_CHAT_DAILY_MESSAGES`, `FREEMIUM_LESSONS_DAILY`, `FREEMIUM_LISTENING_WEEKLY`, `FREEMIUM_READING_WEEKLY`, and `FREEMIUM_VOICE_WEEKLY_MINUTES`. A quota value of `0` blocks the feature entirely for free users. New users receive a `FREEMIUM_TRIAL_DAYS`-day full-access trial when `FREEMIUM_TRIAL_ENABLED=true`. Self-hosted deployments ignore all freemium settings (everything is free).
- Supported study languages include English (`en-GB`, `en-US`), Spanish (`es-ES`), Italian (`it-IT`), Portuguese (`pt-PT`), German (`de-DE`), French (`fr-FR`), Japanese (`ja-JP`), Korean (`ko-KR`), Mainland Chinese (`zh-CN`), and the A1 isiXhosa sprint (`xh-ZA`). The study language is chosen on `/onboarding` and can be expanded later from Settings → My Languages. The user's native language is asked during registration and is used for flashcard translations, tutor feedback, lesson native explanations, and cached native-language help in static grammar, phrasebook, and vocabulary resources.

## Free-first Railway deployment

The repository includes a three-service Railway profile for the isiXhosa sprint:

- `frontend`: Next.js, public domain, root directory `/`, config path `/frontend/railway.toml`
- `backend`: FastAPI, public domain plus private service networking, root directory `/backend`, config path `/backend/railway.toml`, persistent volume mounted at `/data`
- `xhosa-speech`: Simba TTS only, private service networking, root directory `/speech`, config path `/speech/railway.toml`, persistent model volume mounted at `/models/huggingface`

Use the matching `railway.*.env.example` file for each service. The recommended external free tiers are Neon Postgres, Upstash Redis, Gemini for the tutor, and Groq Whisper for speech recognition. The backend accepts a standard Neon `postgresql://` URL and normalizes its SSL query parameters for asyncpg; an Upstash `rediss://` URL works directly.

Set `BACKEND_URL=http://backend.railway.internal:8000` on the frontend and use `http://xhosa-speech.railway.internal:9100` for both backend speech URLs. Generate public Railway domains for the frontend and backend, then set `NEXT_PUBLIC_API_URL` on the frontend to the backend's public `https://` domain so browser WebSocket voice sessions connect correctly. Keep `LLM_PROVIDER=gemini`, `STT_PROVIDER=groq`, and `TTS_PROVIDER=local` for this profile.

Enable Railway serverless sleeping to minimise idle usage. The first Simba request after a sleep or fresh deployment downloads/loads the model and can take several minutes; later requests and generated isiXhosa MP3s are served from persistent caches. Gemini's free tier may use submitted content to improve Google products, so do not enter sensitive personal information while using that tier.

## Linux host: Redis memory overcommit

Redis requires `vm.overcommit_memory=1` on the host to safely perform background saves (RDB snapshots). Without it, a `fork()` under low memory can fail and Redis may lose data on restart.

Run once on the server:

```bash
sudo sysctl vm.overcommit_memory=1
echo "vm.overcommit_memory = 1" | sudo tee -a /etc/sysctl.conf
```

The first command applies the setting immediately (no reboot needed); the second persists it across reboots. This is a host-level setting — it cannot be applied from within the container without elevated privileges.

## Reverse proxy requirement (real-time conversation)

The real-time voice conversation feature uses a WebSocket connection (`/ws/conversation`). Next.js does not proxy WebSocket upgrades natively, so **a reverse proxy is required in any production deployment** to route `/ws/*` traffic to the backend container.

This is also a hard browser requirement: `getUserMedia` (microphone access) only works in a [secure context](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts) — HTTPS or localhost. A reverse proxy terminating TLS is therefore mandatory for the conversation feature to work at all in production.

The WebSocket URL is derived automatically from `window.location`, so no extra configuration is needed on the frontend side — just ensure your reverse proxy forwards `/ws/*` to `backend:8000`.

## Enabling TTS & STT

TTS and STT are selected independently via `.env`.

### Provider options

| Variable         | Values             | Notes                                                         |
| ---------------- | ------------------ | ------------------------------------------------------------- |
| `TTS_PROVIDER`   | `local` · `openai` | `local` uses Kokoro-FastAPI; `openai` uses OpenAI TTS API     |
| `STT_PROVIDER`   | `local` · `groq` · `openai` | `groq` uses hosted Whisper; `local` and `openai` retain their existing paths |
| `OPENAI_API_KEY` | string             | Required for `openai` provider on either service              |
| `GROQ_API_KEY`   | string             | Required when `STT_PROVIDER=groq`                              |

When the active language is isiXhosa and the providers are `local`, FreeLingo automatically routes TTS and STT to `XHOSA_SPEECH_BASE_URL`. With the Railway profile, TTS stays local through Simba while Groq handles STT. Other languages continue to use their selected providers.

When using `openai` providers, the `kokoro` and `whisper` Docker services can be removed from the stack — no local GPU required.

### Option A — Local providers (self-hosted, GPU recommended)

The `kokoro` and `whisper` services in `docker-compose.yml` are pre-configured for NVIDIA GPUs.

```env
TTS_PROVIDER=local
STT_PROVIDER=local
```

For isiXhosa, Compose also builds `xhosa-speech`. Its first use downloads and caches the free models under `${DATA_PATH}/models/huggingface`:

- TTS: [`UBC-NLP/Simba-TTS-xho`](https://huggingface.co/UBC-NLP/Simba-TTS-xho) (CC BY 4.0)
- STT: [`digiphyte/swivuriso-turbo`](https://huggingface.co/digiphyte/swivuriso-turbo) (MIT)

The default Compose service is portable and runs on CPU. If CUDA is exposed to the container, `XHOSA_SPEECH_DEVICE=auto` uses it automatically; a direct host run on Apple silicon can use MPS for Simba TTS while Swivuriso falls back to CPU. Initial model download and first inference are slower than later requests.

The Kokoro image (`ghcr.io/remsky/kokoro-fastapi-gpu`) supports all NVIDIA architectures via two builds: `:latest-cu128` (0.4.0+) for Blackwell/RTX 50-series, and `:latest` for Maxwell through Hopper (confirmed Pascal/GTX 10xx support).

For CPU-only hosts, replace the image tags and remove the `deploy` block in `docker-compose.yml`:

```yaml
kokoro:
  image: ghcr.io/remsky/kokoro-fastapi-cpu:latest
  restart: unless-stopped

whisper:
  image: onerahmet/openai-whisper-asr-webservice:latest
  restart: unless-stopped
  environment:
    - ASR_MODEL=base
    - ASR_ENGINE=faster_whisper
```

> Use `ASR_MODEL=base` or `small` on CPU. Larger models are very slow without a GPU.

#### TTS voice options (Kokoro-82M)

All voices are for English only — Kokoro-82M does not ship multilingual voices. Grades reflect training data quality and quantity.

> **Multilingual learners:** Kokoro cannot produce non-English audio. isiXhosa is the exception because local mode routes it to Simba TTS. Other non-English languages require a compatible local provider or `TTS_PROVIDER=openai`.

| Voice        | Gender | Accent   | Grade |
| ------------ | ------ | -------- | ----- |
| `af_heart`   | F      | American | A ⭐  |
| `af_bella`   | F      | American | A-    |
| `af_nicole`  | F      | American | B-    |
| `am_fenrir`  | M      | American | C+    |
| `am_michael` | M      | American | C+    |
| `am_puck`    | M      | American | C+    |
| `bf_emma`    | F      | British  | B-    |
| `bm_george`  | M      | British  | C     |

Set with `TTS_VOICE=<voice>` in `.env`. Default: `af_heart`.

See the [full list of available voices](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md) on HuggingFace.

#### STT model options (Whisper)

| Model            | VRAM   | Speed vs large | Notes                                       |
| ---------------- | ------ | -------------- | ------------------------------------------- |
| `tiny.en`        | ~1 GB  | ~10x           | Very low accuracy                           |
| `small.en`       | ~2 GB  | ~4x            | OK for CPU                                  |
| `medium`         | ~5 GB  | ~2x            | Good balance                                |
| `large-v3-turbo` | ~6 GB  | ~8x            | **Recommended** — best speed/accuracy ratio |
| `large-v3`       | ~10 GB | 1x             | Maximum accuracy                            |

Set with `STT_MODEL=<model>` in `.env`. Default: `large-v3-turbo`.

| Engine           | Notes                                                                       |
| ---------------- | --------------------------------------------------------------------------- |
| `faster_whisper` | **Recommended** — 4× faster than openai_whisper, lower VRAM via CTranslate2 |
| `openai_whisper` | Original PyTorch implementation                                             |
| `whisperx`       | Adds speaker diarization; requires HuggingFace token                        |

Set with `STT_ENGINE=<engine>` in `.env`. Default: `faster_whisper`.

### Option B — OpenAI providers (no local GPU needed)

```env
TTS_PROVIDER=openai
STT_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

Uses the same `OPENAI_API_KEY` as the LLM if `LLM_PROVIDER=openai`. No extra services needed.

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for instructions on running the project locally for development on macOS.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on reporting bugs and suggesting features. By opening a pull request you accept the [Contributor License Agreement](CONTRIBUTOR_LICENSE_AGREEMENT.md).

> **External code contributions (pull requests) are temporarily not being accepted.** Bug reports and feature suggestions via issues are still welcome.

## License

Distributed under the [GNU Affero General Public License v3](LICENSE).

Organisations that need to deploy FreeLingo without the AGPL's copyleft obligations can obtain a **commercial licence**. See [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md) or [get in touch](https://freelingo.app) via the contact form.

## Author

**Arturo Carretero Calvo** — [@artcc](https://github.com/artcc)
