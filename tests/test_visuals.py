from pathlib import Path

from src.visuals import generate_visuals


def test_generate_visuals_slide(tmp_path: Path, monkeypatch):
    # Ensure outputs go to tmp by chdir
    monkeypatch.chdir(tmp_path)
    scenes = [
        {"duration_sec": 2, "on_screen_text": "Scene A"},
        {"duration_sec": 2, "on_screen_text": "Scene B"},
    ]
    outs = generate_visuals(scenes, style="animated slides")
    assert len(outs) == 2
    for p in outs:
        assert Path(p).exists()
