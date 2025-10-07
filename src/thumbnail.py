from __future__ import annotations

import os
from typing import Optional

from PIL import Image, ImageDraw, ImageFont


def create_thumbnail(title: str, out_path: str, bg_color=(24, 24, 28), size=(1280, 720), overlay_path: Optional[str] = None) -> str:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img = Image.new("RGB", size, color=bg_color)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 72)
    except Exception:
        font = ImageFont.load_default()
    margin = 60
    text = title.strip()[:80]
    draw.text((margin, size[1] // 3), text, font=font, fill=(240, 240, 240))
    if overlay_path and os.path.exists(overlay_path):
        overlay = Image.open(overlay_path).convert("RGBA").resize((size[0] // 3, size[1] // 3))
        img.paste(overlay, (size[0] - overlay.width - margin, size[1] - overlay.height - margin), overlay)
    img.save(out_path)
    return out_path
