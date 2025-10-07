from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from .config import CONFIG
from .logging_utils import setup_logger

logger = setup_logger(__name__)


def _fallback_storyboard(transcript: str, tone: str, target_duration_sec: int, language: Optional[str]) -> Dict[str, Any]:
    words = transcript.split()
    
    # Enhanced scene generation based on content type
    if "car" in transcript.lower() or "vehicle" in transcript.lower() or "स्कॉर्पियो" in transcript or "महिंद्रा" in transcript:
        # Car review structure
        scenes = [
            {
                "id": 1,
                "duration_sec": max(5, target_duration_sec // 3),
                "script_text": f"आज हम बात करेंगे {transcript[:40]}... के बारे में। यह एक amazing vehicle है!",
                "visual_description": "Professional car showcase with dynamic camera angles and smooth transitions.",
                "on_screen_text": f"🚗 {transcript[:30]}...",
            },
            {
                "id": 2,
                "duration_sec": max(5, target_duration_sec // 3),
                "script_text": "इसकी मुख्य खूबियां हैं: मजबूत इंजन, comfortable seating, और advanced features।",
                "visual_description": "Close-up shots of car features with professional lighting and smooth transitions.",
                "on_screen_text": "✨ मुख्य Features",
            },
            {
                "id": 3,
                "duration_sec": max(5, target_duration_sec // 3),
                "script_text": "अगर आप भी इसकी तरह एक reliable vehicle चाहते हैं, तो यह perfect choice है!",
                "visual_description": "Final car shot with call-to-action overlay and professional branding.",
                "on_screen_text": "👍 Perfect Choice!",
            }
        ]
    elif "tutorial" in transcript.lower() or "how to" in transcript.lower() or "कैसे" in transcript:
        # Tutorial structure
        scenes = [
            {
                "id": 1,
                "duration_sec": max(5, target_duration_sec // 3),
                "script_text": f"आज हम सीखेंगे {transcript[:40]}... के बारे में। यह बहुत आसान है!",
                "visual_description": "Step-by-step tutorial with clear visual demonstrations and professional presentation.",
                "on_screen_text": f"📚 {transcript[:30]}...",
            },
            {
                "id": 2,
                "duration_sec": max(5, target_duration_sec // 3),
                "script_text": "पहले step में हमें यह करना है... फिर इसके बाद...",
                "visual_description": "Detailed step-by-step process with clear visual cues and smooth transitions.",
                "on_screen_text": "📝 Step by Step",
            },
            {
                "id": 3,
                "duration_sec": max(5, target_duration_sec // 3),
                "script_text": "बस! आपका काम हो गया। अगर video helpful लगी तो like और subscribe करें!",
                "visual_description": "Final result showcase with call-to-action and professional conclusion.",
                "on_screen_text": "✅ Complete!",
            }
        ]
    else:
        # General content structure
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
            # Enhanced visual descriptions based on content
            if i == 1:
                visual_desc = "Eye-catching opening with dynamic text animation and professional background."
                on_screen = f"🎯 {text.strip()[:50]}"
            elif i == len(chunks):
                visual_desc = "Strong closing with call-to-action and professional branding."
                on_screen = f"🎉 {text.strip()[:50]}"
            else:
                visual_desc = "Engaging middle content with smooth transitions and professional styling."
                on_screen = f"📌 {text.strip()[:50]}"
            
            scenes.append(
                {
                    "id": i,
                    "duration_sec": per_scene,
                    "script_text": text.strip() or "Professional content.",
                    "visual_description": visual_desc,
                    "on_screen_text": on_screen,
                }
            )
    
    # Enhanced metadata
    title_options = [
        f"🎬 {transcript[:25]}...",
        f"✨ Professional {transcript[:20]}...",
        f"🚀 Amazing {transcript[:20]}...",
        f"💡 Quick {transcript[:20]}...",
        f"🔥 Viral {transcript[:20]}..."
    ]
    
    return {
        "title": title_options[0],
        "language": language or "auto",
        "tone": tone,
        "scenes": scenes,
        "thumbnail_idea": "Bold, eye-catching title with professional gradient background and engaging visuals.",
        "description": f"Professional {target_duration_sec}-second video about {transcript[:50]}... Perfect for social media sharing!",
        "tags": ["professional", "short-form", "video", "social-media", "viral", "engaging"],
        "title_options": title_options,
        "engagement_hooks": [
            "इस video को देखकर आप हैरान रह जाएंगे!",
            "यह trick जानकर आपका दिमाग उड़ जाएगा!",
            "अगर आप यह जानते हैं तो आप genius हैं!",
            "इस secret को जानकर आप successful हो जाएंगे!"
        ]
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
