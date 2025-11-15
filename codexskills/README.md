# Codex Skills Bootstrap

Repository for building and distributing Codex Skill bundles. It now follows a tidy layout:

- `docs/` – AGENTS contract, analysis, implementation guide, and onboarding instructions
- `scripts/` – executable tooling (`codex-skills`, `install-skills.sh`)
- `skills/` – each skill in its own folder with `SKILL.md`

## Getting Started

```bash
cd codexskills
export DOTCODEX_DIR=../dotcodex
bash scripts/install-skills.sh
codex-skills list
```

### Using the Makefile

The repo also provides a Makefile in `codexskills/` so you can run the common flows without memorizing commands:

```bash
make deploy           # runs DOTCODEX_DIR=../dotcodex bash scripts/install-skills.sh
make verify           # runs DOTCODEX_DIR=../dotcodex codex-skills list
make lint             # shellchecks the scripts
make clean-runtime    # removes installed skills from ../dotcodex
```

Run these from inside `codexskills/`. Set `DOTCODEX_DIR=/path/to/runtime` first if you want a different destination.

## Adding a Skill

```bash
mkdir -p skills/my-skill
${EDITOR:-vim} skills/my-skill/SKILL.md
DOTCODEX_DIR=../dotcodex bash scripts/install-skills.sh
codex-skills use my-skill
```
Edit docs under `docs/` as needed and rerun the installer (pointing at `../dotcodex`) to update the runtime tree. For a full onboarding walkthrough, read `docs/START-HERE.md`. Licensing details are in `LICENSE.md`.

## Attribution

This implementation is based on the Skills architecture from [Jesse Vincent's Superpowers project](https://github.com/obra/superpowers). Jesse pioneered the concept of using SKILL.md files to teach AI coding assistants reusable techniques and workflows.

His [blog post about porting Skills to Codex](https://blog.fsck.com/2025/10/27/skills-for-openai-codex/) demonstrated that the approach works great with OpenAI Codex and provided the foundation for this implementation.

Thank you to Jesse for building Superpowers, documenting it thoroughly, and sharing it under the MIT License.
