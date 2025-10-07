from pathlib import Path
import wave

from moviepy.editor import ColorClip

from src.assembler import assemble_video


def test_assemble_video(tmp_path: Path):
    # Create two short colored clips
    v1 = tmp_path / "v1.mp4"
    v2 = tmp_path / "v2.mp4"
    ColorClip(size=(320, 240), color=(255, 0, 0), duration=1).write_videofile(
        str(v1), fps=24, codec="libx264", audio=False, verbose=False, logger=None
    )
    ColorClip(size=(320, 240), color=(0, 255, 0), duration=1).write_videofile(
        str(v2), fps=24, codec="libx264", audio=False, verbose=False, logger=None
    )

    # Create two 1s silent audio files via wave module
    a1 = tmp_path / "a1.wav"
    a2 = tmp_path / "a2.wav"
    for p in (a1, a2):
        with wave.open(str(p), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(b"\x00\x00" * 16000)

    out = tmp_path / "out.mp4"
    srt_texts = ["Hello", "World"]
    result = assemble_video([str(v1), str(v2)], [str(a1), str(a2)], srt_texts, str(out))
    assert Path(result).exists()
