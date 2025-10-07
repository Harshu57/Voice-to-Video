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
    # Professional gradient background
    bg = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(bg)
    
    # Create gradient effect
    for y in range(height):
        color_ratio = y / height
        r = int(20 + (50 - 20) * color_ratio)
        g = int(30 + (60 - 30) * color_ratio)
        b = int(40 + (80 - 40) * color_ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Professional typography
    try:
        title_font = ImageFont.truetype("arial.ttf", 72)
        subtitle_font = ImageFont.truetype("arial.ttf", 48)
    except Exception:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    margin = 100
    words = text.split()
    
    # Split into title and subtitle if possible
    if len(words) > 6:
        mid = len(words) // 2
        title = " ".join(words[:mid])
        subtitle = " ".join(words[mid:])
    else:
        title = text
        subtitle = ""
    
    # Draw title
    title_wrapped = []
    line = ""
    for w in title.split():
        test = (line + " " + w).strip()
        if draw.textlength(test, font=title_font) < (width - 2 * margin):
            line = test
        else:
            title_wrapped.append(line)
            line = w
    if line:
        title_wrapped.append(line)
    
    # Center title
    title_height = len(title_wrapped) * 90
    y_start = (height - title_height) // 2
    if subtitle:
        y_start -= 40
    
    for l in title_wrapped:
        bbox = draw.textbbox((0, 0), l, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y_start), l, font=title_font, fill=(255, 255, 255))
        y_start += 90
    
    # Draw subtitle if exists
    if subtitle:
        subtitle_wrapped = []
        line = ""
        for w in subtitle.split():
            test = (line + " " + w).strip()
            if draw.textlength(test, font=subtitle_font) < (width - 2 * margin):
                line = test
            else:
                subtitle_wrapped.append(line)
                line = w
        if line:
            subtitle_wrapped.append(line)
        
        for l in subtitle_wrapped:
            bbox = draw.textbbox((0, 0), l, font=subtitle_font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, y_start), l, font=subtitle_font, fill=(200, 200, 200))
            y_start += 60
    
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
        
        # Create professional video with transitions
        clip = ImageClip(img_path).set_duration(duration)
        
        # Add fade in/out effects for professional look
        if idx == 1:  # First scene - fade in
            clip = clip.fadein(0.5)
        if idx == len(storyboard):  # Last scene - fade out
            clip = clip.fadeout(0.5)
        
        # Add subtle zoom effect for engagement
        clip = clip.resize(lambda t: 1 + 0.05 * t / duration)
        
        clip.write_videofile(
            clip_path, 
            fps=30,  # Higher FPS for smoothness
            codec="libx264", 
            audio=False, 
            verbose=False, 
            logger=None,
            ffmpeg_params=["-preset", "fast", "-crf", "18"]  # High quality encoding
        )
        outputs.append(clip_path)
    return outputs
