from __future__ import annotations

import json
import os

from src.script_gen import generate_script
from src.tts import synthesize_speech
from src.visuals import generate_visuals
from src.assembler import assemble_video


def main() -> None:
    os.makedirs("outputs/final", exist_ok=True)

    with open("assets/demo/sample_transcript.txt", "r", encoding="utf-8") as f:
        transcript = f.read().strip()

    storyboard = generate_script(transcript, tone="friendly", target_duration_sec=30, language="hi")
    scenes = storyboard["scenes"]

    audio_paths = synthesize_speech(scenes, voice="", speed=1.0)
    scene_videos = generate_visuals(scenes, style="animated slides")

    subtitles = [s.get("on_screen_text") or s.get("script_text") or "" for s in scenes]
    out = assemble_video(scene_videos, audio_paths, subtitles, "outputs/final/demo_out.mp4")

    print("Storyboard:\n", json.dumps(storyboard, ensure_ascii=False, indent=2))
    print("Video:", out)


if __name__ == "__main__":
    main()
