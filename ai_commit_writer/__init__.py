"""ai-commit-writer - AI-powered commit message generator from git diff."""

import subprocess
import os
import sys

try:
    import httpx
    import typer
    from rich.console import Console
except ImportError:
    print("Missing dependencies. Install with: pip install httpx typer rich")
    sys.exit(1)

app = typer.Typer()
console = Console()

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")

PROMPT_TEMPLATE = """Generate a concise, conventional git commit message for the following diff.

Rules:
- First line: type(scope): short summary (max 72 chars)
- Follow conventional commits: feat, fix, chore, docs, style, refactor, perf, test, ci
- If breaking change, add BREAKING CHANGE: description
- Use imperative mood
- Do not wrap in backticks or quotes

DIFF:
{diff}
"""


def get_git_diff(staged: bool = False) -> str:
    """Get git diff from the current repository."""
    cmd = ["git", "diff", "--cached"] if staged else ["git", "diff"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
        if result.returncode != 0:
            console.print("[red]Not a git repository or no changes detected[/]")
            sys.exit(1)
        diff = result.stdout.strip()
        if not diff:
            console.print("[yellow]No diff found. Stage changes with git add first.[/]")
            sys.exit(1)
        return diff
    except FileNotFoundError:
        console.print("[red]Git not found. Install git first.[/]")
        sys.exit(1)


def query_ollama(prompt: str, model: str = OLLAMA_MODEL) -> str:
    """Query Ollama API."""
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False, "options": {"temperature": 0.2}}
    try:
        with httpx.Client(timeout=60) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json().get("response", "").strip()
    except httpx.HTTPError as e:
        console.print(f"[red]Ollama error:[/] {e}")
        sys.exit(1)


@app.command()
def generate(
    staged: bool = typer.Option(True, "--staged/--unstaged", help="Use staged or unstaged diff"),
    model: str = typer.Option(OLLAMA_MODEL, "--model", "-m", help="Ollama model"),
) -> None:
    """Generate a commit message from current git diff."""
    diff = get_git_diff(staged)
    prompt = PROMPT_TEMPLATE.format(diff=diff[:4000])
    console.print(f"[cyan]Generating commit message using {model}...[/]")
    message = query_ollama(prompt, model)
    console.print("\n[bold green]Suggested commit message:[/]")
    console.print(message)


@app.command()
def apply(
    model: str = typer.Option(OLLAMA_MODEL, "--model", "-m", help="Ollama model"),
) -> None:
    """Generate and apply a commit message directly."""
    diff = get_git_diff(staged=True)
    prompt = PROMPT_TEMPLATE.format(diff=diff[:4000])
    console.print(f"[cyan]Generating commit message...[/]")
    message = query_ollama(prompt, model)
    subprocess.run(["git", "commit", "-m", message])


if __name__ == "__main__":
    app()
