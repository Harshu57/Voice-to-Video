from __future__ import annotations

import datetime as dt
import os
from typing import List

import srt
from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips

from .logging_utils import setup_logger

logger = setup_logger(__name__)


def _ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def assemble_video(scene_videos: List[str], audio_paths: List[str], subtitles: List[str], output_path: str) -> str:
    """
    Concatenate clips, sync audio, and burn (or export) subtitles.
    Produces an MP4 at 1080p (if source allows). Returns output path.
    """
    if len(scene_videos) != len(audio_paths):
        raise ValueError("scene_videos and audio_paths must have the same length")

    _ensure_dir(output_path)

    clips: List[VideoFileClip] = []
    try:
        for v, a in zip(scene_videos, audio_paths):
            vclip = VideoFileClip(v)
            aclip = AudioFileClip(a)
            # Align durations safely to the shorter to avoid reader overrun
            target = min(float(vclip.duration or 0.0), float(aclip.duration or 0.0))
            if target <= 0.0:
                target = float(vclip.duration or aclip.duration or 1.0)
            vclip = vclip.subclip(0, target)
            aclip = aclip.subclip(0, target)
            vclip = vclip.set_audio(aclip)
            clips.append(vclip)
        final = concatenate_videoclips(clips, method="compose")
        final.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24, verbose=False, logger=None)
    finally:
        for c in clips:
            c.close()

    # Write SRT sidecar from provided subtitles, spreading across scenes uniformly
    try:
        total_seconds = sum(VideoFileClip(v).duration for v in scene_videos)
        start = 0.0
        subs = []
        per_scene = total_seconds / max(1, len(subtitles) or len(scene_videos))
        for i, text in enumerate(subtitles or [""] * len(scene_videos), start=1):
            end = min(total_seconds, start + per_scene)
            subs.append(
                srt.Subtitle(index=i, start=dt.timedelta(seconds=start), end=dt.timedelta(seconds=end), content=text or " ")
            )
            start = end
        srt_path = os.path.splitext(output_path)[0] + ".srt"
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt.compose(subs))
    except Exception as e:
        logger.warning("Failed to write SRT: %s", e)

    return output_path
