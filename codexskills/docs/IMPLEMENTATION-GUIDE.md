# Codex Skills Implementation Guide

**Status:** Based on Jesse Vincent's proven working implementation  
**Confidence:** High - follows patterns that work in production  
**Time to Deploy:** 15-30 minutes

## What Changed from the Original Concept

After reading Jesse's blog post and actual code, we refined the implementation to match what actually works:

### Key Improvements

1. **Added `when_to_use` field** - Critical for skill discovery
2. **Tool mapping** - Explicit Claude-to-Codex translations
3. **Skill announcements** - Codex declares when using skills
4. **Stronger bootstrap** - Uses Jesse's `<EXTREMELY_IMPORTANT>` pattern
5. **Simpler script** - Combined list/use into one clean tool

### What We Kept

- Clean, reviewable implementation
- Single shell script (no external dependencies)
- Standard directory structure inside `${DOTCODEX_DIR:-../dotcodex}` (symlinked to `~/.codex/`)
- YAML frontmatter format
- Comprehensive documentation

## Files Included

### Core System
1. **scripts/codex-skills** - Single script with `list` and `use` commands
2. **AGENTS.md** - Bootstrap configuration with tool mappings
3. **skills/time-awareness/SKILL.md** - Example skill with proper format

### Documentation
4. **docs/ANALYSIS.md** - What we learned from Jesse's implementation
5. **scripts/install-skills.sh** - Automated installer
6. **README.md** - Complete usage guide

## DOTCODEX_DIR Setup

All `.codex` assets now live in a repository you can share with your team. In this layout the repo root contains two folders: `codexskills/` (source) and `dotcodex/` (runtime). Set `DOTCODEX_DIR` to the sibling `../dotcodex` directory and symlink its `AGENTS.md` and `skills/` into `~/.codex` so Codex still finds the expected path.

```bash
cd codexskills
export DOTCODEX_DIR=../dotcodex
mkdir -p "$DOTCODEX_DIR"
mkdir -p ~/.codex
ln -sfn "$DOTCODEX_DIR/AGENTS.md" ~/.codex/AGENTS.md
ln -sfn "$DOTCODEX_DIR/skills" ~/.codex/skills
```

## Quick Installation

```bash
# 1. Download the repository

# 2. Run installer
bash scripts/install-skills.sh

# 3. Update PATH (if needed)
echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> ~/.bashrc
source ~/.bashrc

# 4. Test
codex-skills list

# 5. Try in Codex
# Start Codex and ask: "What day is it?"
```

## How It Works

### Discovery (on Codex startup)

1. Codex reads `~/.codex/AGENTS.md` (symlinked to `${DOTCODEX_DIR}/AGENTS.md`)
2. Sees: `<EXTREMELY_IMPORTANT>RIGHT NOW run: codex-skills list</EXTREMELY_IMPORTANT>`
3. Executes command immediately
4. Sees list of available skills with descriptions
5. Learns when to use each skill

### Activation (during conversation)

1. User asks time-related question
2. Codex recognizes pattern from skill descriptions
3. Runs: `codex-skills use time-awareness`
4. Reads skill instructions
5. Announces: "I've loaded the Time Awareness skill..."
6. Follows instructions (runs `date` commands)

## The Shell Script

### Commands

```bash
codex-skills list               # Show all available skills
codex-skills use <skill-name>   # Load a specific skill
```

### What It Does

**`list` command:**
- Scans `${DOTCODEX_DIR:-../dotcodex}/skills/` (via the `~/.codex/skills/` symlink) for SKILL.md files
- Parses YAML frontmatter (name, description, when_to_use)
- Outputs formatted list for Codex

**`use` command:**
- Reads requested SKILL.md file
- Outputs full content with header
- Codex follows the instructions

### Why This Works

- Pure bash - no dependencies
- Simple file operations - easy to audit
- Clear output format
- Follows Jesse's proven pattern

## The Bootstrap (AGENTS.md)

### Structure

```markdown
<EXTREMELY_IMPORTANT>
Run: codex-skills list
</EXTREMELY_IMPORTANT>

## How to Use Skills
[Instructions]

## Critical Rules  
[Mandatory usage rules]

## Tool Mapping
[Claude-to-Codex translations]
```

### Key Elements

1. **Immediate execution** - `<EXTREMELY_IMPORTANT>` makes Codex run command now
2. **Tool mapping** - TodoWrite → update_plan, etc.
3. **Mandatory language** - "YOU DO NOT HAVE A CHOICE"
4. **Activation rules** - Pattern matching for skills

## SKILL.md Format

### Required YAML Frontmatter

```yaml
---
name: Human-Readable Name
description: One-line summary
when_to_use: Detailed triggers and symptoms
version: 1.0.0
languages: all
---
```

### Required Sections

```markdown
# Skill Name

## Overview
Core principle (1-2 sentences)

## When to Use
- Specific triggers
- Error patterns
- Symptoms

## Core Pattern (optional)
Before/after comparison

## Quick Reference
Table of common operations

## Implementation
Step-by-step instructions

## Common Mistakes
What goes wrong + fixes

## Real-World Examples
Concrete usage examples
```

### Critical: `when_to_use` Field

This is how Codex discovers when to load your skill. Be specific:

❌ **Bad:** "For time-related queries"
✅ **Good:** "When user asks about dates, times, 'today', 'tomorrow', deadlines, or anything requiring current time"

## Creating New Skills

### 1. Create Directory

```bash
skills_dir="${DOTCODEX_DIR:-${HOME}/dotcodex}/skills"
mkdir -p "${skills_dir}/my-skill"
```

### 2. Create SKILL.md

```bash
cat > "${skills_dir}/my-skill/SKILL.md" <<'EOF'
---
name: My Skill
description: What this does in one line
when_to_use: Specific triggers, error messages, symptoms that indicate this skill
version: 1.0.0
languages: all
---

# My Skill

## Overview
Core principle.

## When to Use
- Trigger 1
- Trigger 2

## Implementation
1. Step 1
2. Step 2

## Examples
Concrete examples.
EOF
```

### 3. Test

```bash
# Verify it appears
codex-skills list

# Verify it loads
codex-skills use my-skill

# Test in Codex
# Ask a question that should trigger the skill
```

## Testing Your Installation

### Test 1: Command Works

```bash
codex-skills list
# Should show time-awareness skill
```

### Test 2: Skill Loads

```bash
codex-skills use time-awareness
# Should show full skill content
```

### Test 3: Codex Integration

Start Codex and try:
```
User: "What day is it?"

Expected:
- Codex announces loading time-awareness skill
- Runs date command
- Provides current date
```

## Differences from Jesse's Full Implementation

### What We Didn't Include

- **Superpowers library** - Jesse has 20+ pre-built skills
- **Auto-updates** - His system syncs with GitHub
- **Subagents** - Advanced workflow features
- **Multiple skill sources** - Personal + shared skills

### What We Focused On

- **Minimal working system** - Prove the concept
- **Team-reviewable** - Clean, inspectable code
- **Your use case** - Time-awareness specifically
- **Easy extension** - Simple to add more skills

### Why This Approach

1. **Security** - Your team can audit everything
2. **Control** - You own the implementation
3. **Learning** - Understand how it works
4. **Customization** - Adapt to your needs

## Validation Checklist

Before deploying to team:

- [ ] Ran `bash scripts/install-skills.sh` successfully
- [ ] `codex-skills list` shows time-awareness skill
- [ ] `codex-skills use time-awareness` loads content
- [ ] Codex actually uses skill when asking "What day is it?"
- [ ] Team has reviewed the shell script
- [ ] Team has reviewed AGENTS.md content
- [ ] Team has reviewed skill content
- [ ] Documented how to create new skills

## Next Steps

### Immediate (Today)

1. Install and test the system
2. Verify Codex uses time-awareness skill
3. Create one custom skill for your workflow

### This Week

1. Document team standards as skills
2. Train team on creating skills
3. Build library of 3-5 essential skills

### This Month

1. Share skills across team
2. Integrate into onboarding
3. Measure impact on code quality

## Troubleshooting

### Codex doesn't run bootstrap command

**Check:** Is `<EXTREMELY_IMPORTANT>` tag present in AGENTS.md?  
**Fix:** Ensure exact format from AGENTS.md

### Skills don't activate automatically

**Check:** Is `when_to_use` field descriptive enough?  
**Fix:** Add more specific triggers and symptoms

### Command not found

**Check:** Is ~/.local/bin in PATH?  
**Fix:** `export PATH="${HOME}/.local/bin:${PATH}"`

### Skill shows wrong name

**Check:** YAML frontmatter format correct?  
**Fix:** Ensure `---` delimiters and no tabs

## Security Considerations

What your security team should review:

1. **Shell script** - What commands can it execute?
   - Answer: Only `find`, `cat`, `dirname`, `basename`, standard text processing

2. **File access** - Where can it read/write?
   - Answer: Only reads from `${DOTCODEX_DIR:-../dotcodex}/skills/` (through the `~/.codex/skills/` symlink), no writes

3. **AGENTS.md** - What gets injected?
   - Answer: Skill listing command and usage instructions

4. **Network** - Does it phone home?
   - Answer: No network access at all

5. **Privileges** - Does it need sudo?
   - Answer: No, all user-level operations

## Support

- **Full implementation details:** ANALYSIS.md
- **Original approach:** First version files (for comparison)
- **Jesse's blog:** https://blog.fsck.com/2025/10/27/skills-for-openai-codex/
- **Jesse's repo:** https://github.com/obra/superpowers

## License

This implementation is provided for your professional use. Modify as needed for your organization.

---

**Ready to deploy!** This is a proven, working pattern refined from Jesse Vincent's production implementation.
