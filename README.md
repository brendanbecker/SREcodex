# SREcodex

SRE skills for OpenAI Codex.

## Quick Start

```bash
git clone git@github.com:brendanbecker/SREcodex.git
cd SREcodex
./scripts/uninstall-bridge.sh
```

The script will:
1. Remove any old bridge symlinks from `~/.codex/`
2. Install skills to `~/.codex/skills/`
3. Prompt you to clean up any MCP server config

Restart Codex after running the script.

## Skills Included

| Skill | Description |
|-------|-------------|
| `document-parser` | Parse large documents exceeding context limits |
| `skill-builder` | Create new skills |
| `time-awareness` | Current date/time information |
| `uv-python` | UV package manager workflow for Python |

## Manual Installation

If you prefer not to run the script, copy skills manually:

```bash
cp -r skills/* ~/.codex/skills/
```

## Adding Skills

1. Create a new directory under `skills/`
2. Add a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: "My Skill"
tags: ["keyword1", "keyword2"]
intent: "Use this when..."
version: "1.0.0"
---

# My Skill

Instructions here...
```

3. Run the install script or copy manually

## License

MIT
