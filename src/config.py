from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class AppConfig:
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    elevenlabs_api_key: str | None = os.getenv("ELEVENLABS_API_KEY")
    pexels_api_key: str | None = os.getenv("PEXELS_API_KEY")
    pika_api_key: str | None = os.getenv("PIKA_API_KEY")
    runway_api_key: str | None = os.getenv("RUNWAY_API_KEY")
    kaiber_api_key: str | None = os.getenv("KAIBER_API_KEY")
    youtube_client_secret_file: str | None = os.getenv("YOUTUBE_CLIENT_SECRET_FILE")
    veo3_api_key: str | None = os.getenv("VEO3_API_KEY")

    openai_tts_voice: str | None = os.getenv("OPENAI_TTS_VOICE")

    max_video_minutes: int = int(os.getenv("MAX_VIDEO_MINUTES", "10"))
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    http_timeout_seconds: int = int(os.getenv("HTTP_TIMEOUT_SECONDS", "30"))
    retry_max_attempts: int = int(os.getenv("RETRY_MAX_ATTEMPTS", "3"))
    retry_backoff_seconds: float = float(os.getenv("RETRY_BACKOFF_SECONDS", "2"))


CONFIG = AppConfig()
