from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from .config import CONFIG
from .logging_utils import setup_logger

logger = setup_logger(__name__)


def _fallback_storyboard(transcript: str, tone: str, target_duration_sec: int, language: Optional[str]) -> Dict[str, Any]:
    words = transcript.split()
    # Optimize for short-form content (30 seconds max)
    n_scenes = max(2, min(4, max(1, len(words) // 15)))
    chunks: List[str] = []
    if n_scenes > 0:
        size = max(1, len(words) // n_scenes)
        for i in range(n_scenes):
            chunk = " ".join(words[i * size : (i + 1) * size]) or transcript
            chunks.append(chunk)
    scenes: List[Dict[str, Any]] = []
    per_scene = max(3, target_duration_sec // max(1, n_scenes))
    for i, text in enumerate(chunks, start=1):
        scenes.append(
            {
                "id": i,
                "duration_sec": per_scene,
                "script_text": text.strip() or "Intro.",
                "visual_description": "Professional slide with gradient background and centered typography.",
                "on_screen_text": text.strip()[:60],  # Shorter for mobile viewing
            }
        )
    return {
        "title": f"Professional {transcript[:30]}...",
        "language": language or "auto",
        "tone": tone,
        "scenes": scenes,
        "thumbnail_idea": "Bold title with professional gradient background.",
        "description": f"Professional short-form video about {transcript[:50]}...",
        "tags": ["professional", "short-form", "video", "auto"],
        "title_options": [f"{transcript[:25]}...", f"Professional {transcript[:20]}...", f"Quick {transcript[:20]}..."],
    }


def generate_script(
    transcript: str,
    tone: str = "conversational",
    target_duration_sec: int = 90,
    language: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate a structured storyboard JSON using OpenAI if available, else fallback."""
    if CONFIG.openai_api_key:
        try:
            from openai import OpenAI  # type: ignore

            system_prompt = (
                "You are a helpful assistant that converts user speech transcripts into a concise, scene-by-scene video storyboard. "
                "Output JSON with keys: title, scenes[], thumbnail_idea, description, tags, title_options. "
                "Each scene must have duration_sec, script_text, visual_description, on_screen_text. "
                "Ensure language matches the transcript language. Return ONLY minified JSON."
            )
            user_prompt = (
                f"Please turn the following transcript into a video storyboard with 3–6 scenes.\n"
                f"Tone: {tone}\n"
                f"Target duration (sec): {target_duration_sec}\n"
                f"Transcript language (auto-detected): {language or 'auto'}\n"
                f"Transcript:\n\"\"\"\n{transcript}\n\"\"\"\n"
            )
            client = OpenAI(api_key=CONFIG.openai_api_key)
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.6,
            )
            content = resp.choices[0].message.content  # type: ignore
            data = json.loads(content)
            # basic validation
            assert isinstance(data.get("scenes"), list)
            return data
        except Exception as e:
            logger.warning("OpenAI script generation failed, using fallback: %s", e)
            return _fallback_storyboard(transcript, tone, target_duration_sec, language)
    else:
        logger.info("OPENAI_API_KEY not set, using local storyboard fallback")
        return _fallback_storyboard(transcript, tone, target_duration_sec, language)
