# SRE Codex Repo

This repository contains two sibling directories:
- `codexskills/` – source with docs, scripts, and skills
- `dotcodex/` – runtime layout Codex reads after running the installer

To work on skills:
1. `cd codexskills`
2. `export DOTCODEX_DIR=../dotcodex`
3. `make deploy` (or `bash scripts/install-skills.sh`)
4. `codex-skills list` to verify

See `codexskills/docs/START-HERE.md` for the full onboarding guide.
