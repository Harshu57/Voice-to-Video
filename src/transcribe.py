from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from moviepy.editor import AudioFileClip

from .config import CONFIG
from .logging_utils import setup_logger

logger = setup_logger(__name__)


def _fallback_transcription(audio_path: str) -> Dict[str, Any]:
    try:
        with AudioFileClip(audio_path) as a:
            duration = float(a.duration or 10.0)
    except Exception:
        duration = 10.0
    segments: List[Dict[str, Any]] = [
        {"start": 0.0, "end": float(duration), "text": "Demo fallback transcript."}
    ]
    return {"transcript": "Demo fallback transcript.", "segments": segments}


def transcribe_audio(audio_path: str, language: Optional[str] = None) -> Dict[str, Any]:
    """
    Transcribe audio using OpenAI Whisper API if available, else local fallback.

    Returns a dict: { "transcript": str, "segments": [{start, end, text}, ...] }
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    if CONFIG.openai_api_key:
        try:
            from openai import OpenAI  # type: ignore

            client = OpenAI(api_key=CONFIG.openai_api_key)
            with open(audio_path, "rb") as f:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=f,
                    response_format="verbose_json",
                    language=language,
                )
            data = json.loads(transcript.model_dump_json()) if hasattr(transcript, "model_dump_json") else transcript  # type: ignore
            text = data.get("text") or data.get("transcript") or ""
            segs = data.get("segments") or []
            segments: List[Dict[str, Any]] = []
            for s in segs:
                segments.append(
                    {
                        "start": float(s.get("start", 0.0)),
                        "end": float(s.get("end", 0.0)),
                        "text": s.get("text", ""),
                    }
                )
            if not segments:
                segments = [{"start": 0.0, "end": max(1.0, float(len(text.split()) / 2.0)), "text": text}]
            return {"transcript": text, "segments": segments}
        except Exception as e:
            logger.warning("OpenAI Whisper failed, using fallback: %s", e)
            return _fallback_transcription(audio_path)
    else:
        logger.info("OPENAI_API_KEY not set, using fallback transcription")
        return _fallback_transcription(audio_path)
