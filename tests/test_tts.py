from pathlib import Path

from src.tts import synthesize_speech


def test_tts_fallback(tmp_path: Path, monkeypatch):
    # Force fallback by clearing env-config via monkeypatch
    monkeypatch.setenv("ELEVENLABS_API_KEY", "")
    monkeypatch.setenv("OPENAI_API_KEY", "")

    scenes = [
        {"script_text": "Hello world"},
        {"script_text": "This is a test"},
    ]
    outs = synthesize_speech(scenes, voice="", speed=1.0)
    assert len(outs) == 2
    for p in outs:
        assert Path(p).exists()
