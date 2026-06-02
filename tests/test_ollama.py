from .ollama import STYLE_PROMPTS


def test_style_prompts_defined():
    assert "conventional" in STYLE_PROMPTS
    assert "simple" in STYLE_PROMPTS
    assert "detailed" in STYLE_PROMPTS


def test_style_prompts_not_empty():
    for name, prompt in STYLE_PROMPTS.items():
        assert len(prompt) > 20, f"{name} prompt is too short"
