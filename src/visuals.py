from __future__ import annotations

import os
from typing import Any, Dict, List

from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip

from .config import CONFIG
from .logging_utils import setup_logger

logger = setup_logger(__name__)


def _ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def _text_to_slide(text: str, width: int = 1920, height: int = 1080) -> Image.Image:
    bg = Image.new("RGB", (width, height), color=(18, 18, 22))
    draw = ImageDraw.Draw(bg)
    try:
        font = ImageFont.truetype("arial.ttf", 64)
    except Exception:
        font = ImageFont.load_default()
    margin = 80
    wrapped = []
    words = text.split()
    line = ""
    for w in words:
        test = (line + " " + w).strip()
        if draw.textlength(test, font=font) < (width - 2 * margin):
            line = test
        else:
            wrapped.append(line)
            line = w
    if line:
        wrapped.append(line)
    y = (height - (len(wrapped) * 80)) // 2
    for l in wrapped:
        draw.text((margin, y), l, font=font, fill=(240, 240, 240))
        y += 80
    return bg


def generate_visuals(storyboard: List[Dict[str, Any]], style: str) -> List[str]:
    """
    For each scene, create a short clip. If external APIs are unavailable, create slide-based clips.
    """
    outputs: List[str] = []
    width, height = 1920, 1080

    # For brevity, we directly use slide fallback. API integrations can be added similarly.
    for idx, scene in enumerate(storyboard, start=1):
        duration = max(1, int(scene.get("duration_sec", 5)))
        text = str(scene.get("on_screen_text") or scene.get("script_text") or "Scene")
        img = _text_to_slide(text, width, height)
        img_path = os.path.join("outputs", "visuals", f"scene_{idx:02d}.png")
        _ensure_dir(img_path)
        img.save(img_path)
        clip_path = os.path.join("outputs", "visuals", f"scene_{idx:02d}.mp4")
        clip = ImageClip(img_path).set_duration(duration)
        clip.write_videofile(clip_path, fps=24, codec="libx264", audio=False, verbose=False, logger=None)
        outputs.append(clip_path)
    return outputs
