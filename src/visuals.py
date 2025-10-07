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


def _generate_with_runway_api(prompt: str, duration: int) -> str:
    """
    Generate video using RunwayML API (free tier available)
    """
    try:
        import requests
        
        # RunwayML API endpoint
        url = "https://api.runwayml.com/v1/image_to_video"
        headers = {
            "Authorization": f"Bearer {CONFIG.runway_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "text_prompt": prompt,
            "duration": duration,
            "resolution": "1280x720"
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        if response.status_code == 200:
            video_url = response.json().get("video_url")
            # Download and save video
            video_response = requests.get(video_url)
            output_path = os.path.join("outputs", "visuals", f"runway_scene.mp4")
            _ensure_dir(output_path)
            with open(output_path, "wb") as f:
                f.write(video_response.content)
            return output_path
    except Exception as e:
        logger.warning("RunwayML API failed: %s", e)
    return None


def _generate_with_pika_api(prompt: str, duration: int) -> str:
    """
    Generate video using Pika Labs API (free tier available)
    """
    try:
        import requests
        
        # Pika Labs API endpoint
        url = "https://api.pika.art/v1/generate"
        headers = {
            "Authorization": f"Bearer {CONFIG.pika_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": "16:9"
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        if response.status_code == 200:
            video_url = response.json().get("video_url")
            # Download and save video
            video_response = requests.get(video_url)
            output_path = os.path.join("outputs", "visuals", f"pika_scene.mp4")
            _ensure_dir(output_path)
            with open(output_path, "wb") as f:
                f.write(video_response.content)
            return output_path
    except Exception as e:
        logger.warning("Pika Labs API failed: %s", e)
    return None


def generate_visuals(storyboard: List[Dict[str, Any]], style: str) -> List[str]:
    """
    For each scene, create a short clip. Try AI APIs first, then fallback to professional slides.
    """
    outputs: List[str] = []
    width, height = 1920, 1080

    for idx, scene in enumerate(storyboard, start=1):
        duration = max(1, int(scene.get("duration_sec", 5)))
        text = str(scene.get("on_screen_text") or scene.get("script_text") or "Scene")
        
        # Try AI video generation APIs in order of preference
        ai_output = None
        
        # Try RunwayML first (most reliable)
        if CONFIG.runway_api_key:
            runway_prompt = f"Cinematic video: {text}. Professional quality, smooth motion."
            ai_output = _generate_with_runway_api(runway_prompt, duration)
        
        # Try Pika Labs if RunwayML fails
        if not ai_output and CONFIG.pika_api_key:
            pika_prompt = f"Professional video scene: {text}. High quality, cinematic style."
            ai_output = _generate_with_pika_api(pika_prompt, duration)
        
        if ai_output:
            outputs.append(ai_output)
            continue
        
        # Fallback to professional slides (always works)
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
