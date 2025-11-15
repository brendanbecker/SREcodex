# SREcodex - Get Started in 5 Minutes

## What This Is

SREcodex packages reusable instruction sets (skills) that Codex can discover and apply automatically. Your team creates skills once, and everyone benefits from consistent best practices.

**Key features:**
- Skills self-describe when they should be used (`when_to_use` metadata)
- Codex discovers skills automatically on startup via `codex-skills list`
- CLI tool for listing and loading skills
- Includes `skill-builder` meta-skill that teaches how to create new skills
- Based on Jesse Vincent's [Superpowers](https://github.com/obra/superpowers) architecture

## What's Included

**Core System:**
- `scripts/codex-skills` - CLI with `list` and `use` commands
- `AGENTS-TEMPLATE.md` - Bootstrap instructions installed to `dotcodex/AGENTS.md`
- `scripts/install-skills.sh` - Automated installer

**Included Skills:**
- `time-awareness` - Ensures Codex uses actual system date instead of guessing
- `skill-builder` - Meta-skill with complete guide for creating new skills

## Installation

```bash
# 1. Clone and navigate
git clone git@github.com:brendanbecker/SREcodex.git ~/projects/SREcodex
cd ~/projects/SREcodex/codexskills

# 2. Deploy using Makefile (recommended)
make deploy

# 3. Add to PATH if needed
echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> ~/.bashrc
source ~/.bashrc

# 4. Verify installation
make verify
```

**What `make deploy` does:**
- Creates `~/.local/bin/codex-skills` executable
- Copies `AGENTS-TEMPLATE.md` → `dotcodex/AGENTS.md`
- Copies all skills from `codexskills/skills/` → `dotcodex/skills/`
- Creates symlinks: `~/.codex/AGENTS.md` and `~/.codex/skills/` → `dotcodex/`

**Alternative:** Set `DOTCODEX_DIR` to a custom path before running `make deploy`

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Codex starts                                             │
│    └─> Reads ~/.codex/AGENTS.md                            │
│                                                             │
│ 2. AGENTS.md contains:                                      │
│    <EXTREMELY_IMPORTANT>Run: codex-skills list</...>       │
│    └─> Codex executes immediately                          │
│                                                             │
│ 3. codex-skills list output:                               │
│    - Scans ~/.codex/skills/*/SKILL.md files                │
│    - Parses YAML frontmatter (name, description, when_to_use)│
│    - Shows available skills to Codex                        │
│                                                             │
│ 4. During conversation:                                     │
│    User: "What day is it?"                                  │
│    └─> Codex recognizes time-related trigger               │
│    └─> Runs: codex-skills use time-awareness               │
│    └─> Follows skill instructions (runs date command)      │
└─────────────────────────────────────────────────────────────┘
```

## Verify Installation

```bash
# Test 1: CLI works
codex-skills list
# Expected: Shows time-awareness and skill-builder

# Test 2: Skill loads
codex-skills use time-awareness
# Expected: Displays full skill content

# Test 3: Codex integration
# Start Codex, ask: "What day is it?"
# Expected: Codex announces loading time-awareness, runs date command
```

## Creating Your First Skill

**Step 1:** Load the skill-builder skill to learn the complete process

```bash
codex-skills use skill-builder
```

**Step 2:** Create your skill (minimal example)

```bash
# Create directory
mkdir -p dotcodex/skills/my-workflow

# Create SKILL.md with YAML frontmatter
cat > dotcodex/skills/my-workflow/SKILL.md <<'EOF'
---
name: My Workflow
description: Brief one-line description
when_to_use: Specific triggers, error messages, or symptoms that indicate this skill applies
version: 1.0.0
languages: all
---

# My Workflow

## Overview
Core principle in 1-2 sentences.

## When to Use
- Specific trigger pattern 1
- Error message pattern 2
- Symptom or context 3

## Implementation
1. First step with specific commands
2. Second step with expected output
3. Validation step

## Examples
Concrete before/after examples.
EOF

# Verify
codex-skills list          # Should show your new skill
codex-skills use my-workflow  # Should load it
```

**Step 3:** Test in Codex by asking a question that matches your `when_to_use` triggers

## Troubleshooting

| Issue | Check | Fix |
|-------|-------|-----|
| `command not found` | Is `~/.local/bin` in PATH? | `export PATH="${HOME}/.local/bin:${PATH}"` |
| Skills don't appear | Did installer complete? | Run `make deploy` again |
| Codex doesn't auto-load | Is `when_to_use` specific enough? | Add more detailed triggers in YAML frontmatter |
| Symlinks broken | Check `~/.codex/` directory | Re-run `make deploy` |
| YAML parse error | Frontmatter format correct? | Ensure `---` delimiters, no tabs, proper indentation |

## Security Review

Before deploying to your team, review these components:

**1. Shell Script (`scripts/codex-skills`)**
- Only executes: `find`, `cat`, `dirname`, `basename`, text processing
- No network calls, no sudo, no writes
- Reads from: `~/.codex/skills/` (symlinked to `dotcodex/skills/`)

**2. AGENTS Template (`AGENTS-TEMPLATE.md`)**
- Injected into Codex on startup
- Contains: skill discovery command (`codex-skills list`)
- No external fetches, no system modifications

**3. Skills Content**
- Review each `SKILL.md` for commands it instructs Codex to run
- Verify no sensitive data access or destructive operations

## Makefile Commands

```bash
make deploy          # Install skills system (runs install-skills.sh)
make verify          # Verify installation (runs codex-skills list)
make lint            # Lint shell scripts with shellcheck
make clean-runtime   # Remove dotcodex/skills/ directory
make reset-runtime   # Clean and re-copy all skills
```

## Next Steps

### Today
1. ✅ Complete installation and verification
2. 📖 Read `codex-skills use skill-builder` for detailed skill creation guide
3. 🧪 Test time-awareness skill in Codex
4. ✏️ Create one custom skill for your workflow

### This Week
1. Document 2-3 team standards as skills
2. Review `docs/AGENTS-GUIDE.md` for repository guidelines
3. Train colleagues on skill creation
4. Build library of essential skills

### Resources
- **Skill creation guide:** `codex-skills use skill-builder`
- **Repository standards:** `codexskills/docs/AGENTS-GUIDE.md`
- **Original project:** [Superpowers by Jesse Vincent](https://github.com/obra/superpowers)
- **Blog post:** [Skills for OpenAI Codex](https://blog.fsck.com/2025/10/27/skills-for-openai-codex/)

## License

MIT License - See `codexskills/LICENSE.md`
