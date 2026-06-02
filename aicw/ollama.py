import httpx
import os

DEFAULT_HOST = "http://localhost:11434"

STYLE_PROMPTS = {
    "conventional": (
        "Generate a conventional commit message for the following diff.\n"
        "Use one of: feat, fix, chore, docs, style, refactor, perf, test, build, ci, revert.\n"
        "Format: type(scope): description\n"
        "Body with motivation for the change (if needed)."
    ),
    "simple": (
        "Generate a short, imperative commit message for the following diff.\n"
        "One line only, max 72 characters."
    ),
    "detailed": (
        "Generate a detailed commit message for the following diff.\n"
        "Include:\n"
        "- Subject line (max 72 chars)\n"
        "- Blank line\n"
        "- Body describing what and why\n"
        "- Bullet points for each logical change"
    ),
}


def query_ollama(diff: str, model: str = "llama3.2", style: str = "conventional") -> str:
    host = os.environ.get("OLLAMA_HOST", DEFAULT_HOST)
    style_guide = STYLE_PROMPTS.get(style, STYLE_PROMPTS["conventional"])

    prompt = (
        f"You are a git commit message assistant.\n\n"
        f"{style_guide}\n\n"
        f"Diff:\n{diff}\n\n"
        f"Commit message:"
    )

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3},
    }

    try:
        resp = httpx.post(f"{host}/api/generate", json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "").strip()
    except httpx.ConnectError:
        return "Error: Cannot connect to Ollama. Is it running?"
    except httpx.TimeoutException:
        return "Error: Ollama request timed out. Try a smaller model."
    except Exception as e:
        return f"Error: {str(e)}"
