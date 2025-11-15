# Repository Guidelines

## Project Structure & Module Organization
This repo ships the Codex Skills bootstrap. `scripts/codex-skills` is the CLI Codex calls to list or load skills stored under `${DOTCODEX_DIR:-../dotcodex}/skills/`, which should be symlinked to `~/.codex/skills/` so Codex still reads its default location. `AGENTS-TEMPLATE.md` (at the repo root) is the source file that defines the runtime contract; the installer copies it to `${DOTCODEX_DIR}/AGENTS.md`, and Codex reads that file via `~/.codex/AGENTS.md`. `skills/time-awareness/SKILL.md` exemplifies the YAML-frontmatter layout every skill should follow. Keep scripts under `scripts/`, docs under `docs/`, and treat newly proposed skills as standalone directories beneath `skills/`.

## Build, Test, and Development Commands
- `bash scripts/install-skills.sh` – installs the CLI, copies `AGENTS-TEMPLATE.md` to `${DOTCODEX_DIR}/AGENTS.md`, and refreshes the `~/.codex` symlinks; run after any script or doc change to observe the live layout.
- `codex-skills list` – exercises the discovery path invoked by AGENTS.md. Confirm headings, descriptions, and when_to_use text render cleanly.
- `codex-skills use <skill>` – validates that loading echoes the skill content exactly; verify the announcement prompt matches the AGENTS instructions.
- `shellcheck scripts/codex-skills scripts/install-skills.sh` – lint scripts before review.

## Coding Style & Naming Conventions
Scripts are Bash with `set -euo pipefail`, four-space indentation, lowercase snake_case variables, and double-quoted expansions. Functions wrap `cmd_*` helpers. Skills live under directories named for their trigger (`time-awareness/`) and expose `SKILL.md` with YAML front matter providing `name`, `description`, and `when_to_use`. Documentation lives under `docs/`, while the installed artifact is `${DOTCODEX_DIR:-../dotcodex}/AGENTS.md` (copied from `AGENTS-TEMPLATE.md` and symlinked to `~/.codex/AGENTS.md`) without a suffix.

## Testing Guidelines
Manually test the AGENTS flow: install, open a new shell, confirm the `codex-skills list` output matches expectations, then simulate skill activation per the instructions. When adding skills, include deterministic commands (e.g., `date '+%A'`) and document verification steps inside the skill text. Provide transcripts of the list/use commands when behavior changes, and test installers against a clean temporary `${DOTCODEX_DIR}` (symlink target for `~/.codex`) to avoid polluting real setups.

## Commit & Pull Request Guidelines
Commits use imperative subjects (“Add filesystem skill”), and bodies must describe motivation and the commands executed (installer, list/use tests). PRs should outline how `AGENTS-TEMPLATE.md` changed (especially the <EXTREMELY_IMPORTANT> block), reference any new or removed skills, attach sample CLI output, and mention security impacts if installers touch paths beyond `${DOTCODEX_DIR:-../dotcodex}` or `~/.local/bin`. Always request a Bash-fluent reviewer for script changes.
