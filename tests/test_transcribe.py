import os
from pathlib import Path
import wave

from src.transcribe import transcribe_audio


def test_transcribe_fallback(tmp_path: Path):
    # create 1s silent wav using stdlib
    wav_path = tmp_path / "silence.wav"
    with wave.open(str(wav_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(b"\x00\x00" * 16000)

    res = transcribe_audio(str(wav_path), language=None)
    assert "transcript" in res
    assert "segments" in res
    assert isinstance(res["segments"], list)
