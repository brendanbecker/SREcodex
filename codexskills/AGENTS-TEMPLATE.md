# Codex Skills System

<EXTREMELY_IMPORTANT>
You have a Skills system with a **Librarian** for on-demand discovery. Don't preload everything - search for what you need.

**On startup, load the Librarian:**
```bash
codex-skills use core/librarian
```

**When you need a capability you don't have:**
```bash
codex-skills search "keyword or description"
```

This returns the top matching skills. Then load what you need.
</EXTREMELY_IMPORTANT>

## Core Commands

| Command | Purpose |
|---------|---------|
| `codex-skills use core/librarian` | Load the discovery skill (always do this first) |
| `codex-skills search "query"` | Find skills by keyword/description |
| `codex-skills use <path>` | Load a specific skill |
| `codex-skills list` | Browse all available skills |

## Discovery Workflow

**When you load a skill:**
1. Search: `codex-skills search "what I need"`
2. Evaluate: Review the top 3 matches
3. Load: `codex-skills use <best-match-path>`
4. Announce: "I've loaded the [Skill Name] skill for [purpose]"
5. Execute: Follow the skill's instructions exactly

## Critical Rules

<EXTREMELY_IMPORTANT>
**IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.**

Before starting ANY task:
1. Think: "Do I have the right skill for this?"
2. If uncertain, search: `codex-skills search "relevant keywords"`
3. If a relevant skill exists, load it with `codex-skills use <path>`
4. Follow the skill's instructions exactly
5. Announce when you're using a skill

Skills contain expert knowledge and best practices. When a skill exists for your task, using it is **mandatory**, not optional.
</EXTREMELY_IMPORTANT>

## Skill Activation Rules

- Use `codex-skills search` when you recognize you lack capability for a task
- As soon as you recognize a matching pattern in the conversation, search and load the appropriate skill
- Example: for any temporal question ("What day is it?", "How many days until..."), search "time date" and load the matching skill

## Tool Mapping Reference

If skills reference tools you don't have natively, use these equivalents:

- `TodoWrite` → `update_plan` (your planning/task tracking tool)
- `Skill` tool → `codex-skills use <skill-name>` command (already available)
- `Read`, `Write`, `Edit`, `Bash` → Use your native file and shell tools

If a skill mentions a tool you truly don't have and there's no equivalent, inform the user and adapt the approach using your available tools.

## Skills Location

Skills live under `${DOTCODEX_DIR:-../dotcodex}/skills/`, which should be symlinked to `~/.codex/skills/` so Codex can keep using its default path.

Set `DOTCODEX_DIR` to your shared `dotcodex` repository and keep `~/.codex/AGENTS.md` and `~/.codex/skills` pointing at it with:
```bash
export DOTCODEX_DIR=../dotcodex   # customize if needed
mkdir -p ~/.codex
ln -sfn "$DOTCODEX_DIR/AGENTS.md" ~/.codex/AGENTS.md
ln -sfn "$DOTCODEX_DIR/skills" ~/.codex/skills
```

Each skill is a directory containing a `SKILL.md` file with instructions.
