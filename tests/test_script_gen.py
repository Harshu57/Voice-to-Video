from src.script_gen import generate_script


def test_generate_script_fallback():
    transcript = "यह एक डेमो ट्रांसक्रिप्ट है जो हिंदी में है।"
    res = generate_script(transcript, tone="friendly", target_duration_sec=60, language="hi")
    assert "title" in res
    assert isinstance(res.get("scenes"), list)
    assert len(res["scenes"]) >= 1
