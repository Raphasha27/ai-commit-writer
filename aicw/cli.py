import click
import subprocess
from .generator import generate_commit_message
from .ollama import query_ollama


@click.group()
def main():
    pass


@main.command()
@click.option("--style", "-s", default="conventional", type=click.Choice(["conventional", "simple", "detailed"]))
@click.option("--model", "-m", default="llama3.2")
@click.option("--interactive", "-i", is_flag=True, help="Review and edit suggestions")
def generate(style, model, interactive):
    diff = get_staged_diff()
    if not diff:
        diff = get_last_diff()
    if not diff:
        click.echo("No changes detected. Stage your changes first with 'git add'", err=True)
        raise SystemExit(1)

    result = query_ollama(diff, model, style)
    if result.startswith("Error:"):
        click.echo(result, err=True)
        raise SystemExit(1)

    if interactive:
        click.echo(f"\nSuggested commit message:\n---\n{result}\n---")
        action = click.prompt("Accept/Edit/Regenerate/Skip", default="accept")
        if action.lower() in ("e", "edit"):
            result = click.edit(result)
        elif action.lower() in ("r", "regenerate"):
            result = query_ollama(diff, model, style)
    else:
        click.echo(result)


@main.command()
def install_hook():
    hook_path = ".git/hooks/prepare-commit-msg"
    hook_content = """#!/bin/sh
COMMIT_MSG_FILE=$1
COMMIT_SOURCE=$2

if [ "$COMMIT_SOURCE" != "message" ]; then
    aicw generate > "$COMMIT_MSG_FILE"
fi
"""
    with open(hook_path, "w") as f:
        f.write(hook_content)
    subprocess.run(["chmod", "+x", hook_path])
    click.echo("Pre-commit hook installed")


def get_staged_diff() -> str:
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""


def get_last_diff() -> str:
    try:
        result = subprocess.run(
            ["git", "diff", "HEAD~1"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""
