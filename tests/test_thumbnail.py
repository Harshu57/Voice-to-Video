from pathlib import Path

from src.thumbnail import create_thumbnail


def test_create_thumbnail(tmp_path: Path):
    out = tmp_path / "thumb.jpg"
    res = create_thumbnail("Test Title", str(out))
    assert Path(res).exists()
