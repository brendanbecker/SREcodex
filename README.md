# dotcodex Repo

This repo now holds two sibling directories:

- `codexskills/` – source of truth with docs, scripts, and skills you edit.
- `dotcodex/` – runtime layout Codex should read (populated via the installer).

To work on skills:
1. `cd codexskills`
2. Edit docs/skills/scripts as needed
3. Run `export DOTCODEX_DIR=../dotcodex && bash scripts/install-skills.sh`
4. Verify with `codex-skills list`

For detailed onboarding see `codexskills/docs/START-HERE.md`.
