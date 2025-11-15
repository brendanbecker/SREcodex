# SREcodex – Skills for Codex

This repository packages everything you need to run the Skills system locally and share it with teammates. It contains two sibling directories:

- [`codexskills/`](codexskills) – editable source (docs, scripts, skills, Makefile)
- [`dotcodex/`](dotcodex) – runtime layout Codex reads after running the installer

## Quick Start

```bash
git clone git@github.com:brendanbecker/SREcodex.git
cd SREcodex/codexskills
export DOTCODEX_DIR=../dotcodex   # or any absolute path you prefer
make deploy                       # or bash scripts/install-skills.sh
make verify                       # runs codex-skills list against DOTCODEX_DIR
```

The installer copies `AGENTS.md` and all `skills/*/SKILL.md` files into `DOTCODEX_DIR` and refreshes the `~/.codex/AGENTS.md` and `~/.codex/skills` symlinks so Codex immediately sees the new instructions.

## Repository Layout

| Path | Purpose |
|------|---------|
| [`codexskills/AGENTS-TEMPLATE.md`](codexskills/AGENTS-TEMPLATE.md) | Template copied to `dotcodex/AGENTS.md` for Codex to read |
| [`codexskills/docs/AGENTS-GUIDE.md`](codexskills/docs/AGENTS-GUIDE.md) | Repository guidelines and review checklist |
| [`codexskills/docs/START-HERE.md`](codexskills/docs/START-HERE.md) | Onboarding playbook (full walkthrough) |
| [`codexskills/README.md`](codexskills/README.md) | Developer-facing README inside the source tree |
| [`codexskills/scripts/`](codexskills/scripts) | `codex-skills` CLI + `install-skills.sh` installer |
| [`codexskills/skills/`](codexskills/skills) | Each skill lives in its own folder with `SKILL.md` |
| [`dotcodex/`](dotcodex) | Generated runtime files that Codex reads |

## Makefile Shortcuts

From the `codexskills/` directory you can run:

```bash
make deploy        # DOTCODEX_DIR=../dotcodex bash scripts/install-skills.sh
make verify        # DOTCODEX_DIR=../dotcodex codex-skills list
make lint          # shellcheck scripts/codex-skills and scripts/install-skills.sh
make clean-runtime # remove installed skills from DOTCODEX_DIR
```

Override `DOTCODEX_DIR=/absolute/path` if you want to target a different runtime directory.

## Creating or Updating Skills

1. Edit/create folders under [`codexskills/skills`](codexskills/skills) (each with `SKILL.md`).
2. Update docs as needed (e.g., [`docs/START-HERE.md`](codexskills/docs/START-HERE.md)).
3. Run `make deploy` to copy the new skills into `dotcodex/`.
4. Run `codex-skills list` (or `make verify`) to confirm activation.

## Attribution & License

This implementation is based on the Skills architecture from [Jesse Vincent's Superpowers project](https://github.com/obra/superpowers) and his blog post about [porting Skills to Codex](https://blog.fsck.com/2025/10/27/skills-for-openai-codex/). See [`codexskills/CREDITS.md`](codexskills/CREDITS.md) and [`codexskills/LICENSE.md`](codexskills/LICENSE.md) for attribution and licensing.
