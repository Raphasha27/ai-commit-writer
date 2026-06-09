# AI Commit Writer

A CLI tool that generates meaningful commit messages from git diffs using local AI (Ollama).

## Features

- Analyzes staged git diffs and generates conventional commit messages
- Supports multiple commit styles (conventional, simple, detailed)
- Interactive mode to accept/edit/regenerate suggestions
- Pre-commit hook integration
- Runs 100% locally via Ollama

## Installation

```bash
pip install ai-commit-writer
```

Or clone and install:

```bash
git clone https://github.com/Raphasha27/ai-commit-writer.git
cd ai-commit-writer
pip install -e .
```

## Usage

```bash
# Generate commit message from staged changes
aicw generate

# Generate from specific diff
git diff --cached | aicw generate

# Use different style
aicw generate --style conventional    # feat: add user auth
aicw generate --style simple          # Add user auth
aicw generate --style detailed        # Full description

# Interactive mode
aicw generate --interactive

# Use as pre-commit hook
aicw install-hook
```

## Commit Styles

- **conventional** (default): Follows Conventional Commits (`feat:`, `fix:`, `chore:`, etc.)
- **simple**: Short imperative sentence
- **detailed**: Multi-line with body and footer

## Configuration

Configuration file at `~/.config/aicw/config.toml`:

```toml
[defaults]
style = "conventional"
model = "llama3.2"
max_length = 72

[hooks]
enabled = true
```

<br/>

---

<h3 align="center">🐍 Part of the <a href="https://github.com/Raphasha27">Raphasha27</a> Ecosystem</h3>

<p align="center">
  <a href="https://github.com/Raphasha27/Raphasha27">
    <img src="https://img.shields.io/badge/Back_to_Profile-0D1117?style=for-the-badge&logo=github&logoColor=white" />
  </a>
  &nbsp;
  <a href="https://raphasha27.github.io/Raphasha27/ai-snake-game/">
    <img src="https://img.shields.io/badge/▶_Play_AI_Snake-0EA5E9?style=for-the-badge&logo=javascript&logoColor=white" />
  </a>
</p>

## License

MIT
