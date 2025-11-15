# Analysis: Jesse Vincent's Codex Skills Implementation

Based on reviewing Jesse's blog post and actual code, here's what we learned about how Skills actually work in Codex.

## Key Insights from Jesse's Implementation

### 1. Codex's Behavior
- **"really, really likes to follow instructions"** - extremely literal
- Better at using skills than Claude in some ways
- Follows commands exactly as written
- Needs explicit tool mapping (TodoWrite → update_plan, etc.)

### 2. The Three Components (Confirmed)

**Component 1: SKILL.md Files**
- YAML frontmatter with `name`, `description`, `when_to_use` fields
- Markdown instructions
- Lives in `~/.codex/skills/` (personal) or `~/.codex/superpowers/skills/` (shared)

**Component 2: Discovery/Use Tool**
- `superpowers-codex bootstrap` - lists all skills
- `superpowers-codex use-skill <name>` - loads skill content
- Shell script that scans directories and reads files

**Component 3: Bootstrap in AGENTS.md**
- Runs discovery command in `<EXTREMELY_IMPORTANT>` tags
- Includes Claude-to-Codex tool translation dictionary
- Strong imperative language: "IF A SKILL APPLIES, YOU DO NOT HAVE A CHOICE"

### 3. Critical Implementation Details

**Installation Method:**
```markdown
<EXTREMELY_IMPORTANT>
You have superpowers. RIGHT NOW run: `~/.codex/superpowers/.codex/superpowers-codex bootstrap` 
and follow the instructions it returns.
</EXTREMELY_IMPORTANT>
```

**Tool Mapping (Essential for Codex):**
```markdown
**Tool Mapping for Codex:**
- `TodoWrite` → `update_plan` (Codex's planning tool)
- `Task` tool with subagents → Tell user subagents aren't available
- `Skill` tool → `~/.codex/superpowers/.codex/superpowers-codex use-skill`
- `Read`, `Write`, `Edit`, `Bash` → Use native Codex tools
```

**Skills Naming Convention:**
```markdown
- Superpowers skills: `superpowers:skill-name` 
- Personal skills: `skill-name`
- Personal skills override superpowers when names match
```

### 4. What Makes It Work

**Mandatory Workflow Enforcement:**
- "IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT."
- Strong, unambiguous language throughout
- Explicit announcement requirement: "I've read the [Skill Name] skill and I'm using it to [purpose]"

**Codex-Specific Adaptations:**
- Explicit tool mapping because Codex won't substitute automatically
- Clear instructions about what to do when tools don't exist
- Strong imperative language because Codex is very literal

### 5. Skills Directory Structure

```
~/.codex/
├── AGENTS.md                    # Bootstrap configuration
├── skills/                       # Personal skills (user's own)
│   └── skill-name/
│       └── SKILL.md
└── superpowers/                 # Cloned from GitHub
    ├── .codex/
    │   └── superpowers-codex    # Shell script tool
    └── skills/                  # Shared skills library
        └── skill-name/
            └── SKILL.md
```

### 6. SKILL.md Format (From Real Examples)

```markdown
---
name: Human-Readable Name
description: One-line summary for discovery
when_to_use: Detailed triggers and symptoms when this applies
version: 1.0.0
languages: all | [typescript, python] | etc
---

# Skill Name

## Overview
Core principle in 1-2 sentences.

## When to Use
- Specific symptoms and triggers
- Error messages that indicate this skill
- Situations where this applies

## Instructions
Step-by-step process

## Common Mistakes
What goes wrong + fixes

## Examples
Concrete usage examples
```

### 7. The Bootstrap Pattern

Jesse's AGENTS.md pattern:
1. Declares superpowers exist in `<EXTREMELY_IMPORTANT>` block
2. Runs `superpowers-codex bootstrap` command
3. Shows skill listing with metadata
4. Provides tool mappings
5. Sets mandatory usage rules
6. Explains skill naming conventions

### 8. Discovery Command Output

The `bootstrap` command outputs:
- List of available skills
- Name, description, location for each
- Usage instructions
- Critical rules about when/how to use skills

### 9. Use-Skill Command Output

The `use-skill <name>` command outputs:
- Full SKILL.md content
- Header indicating which skill was loaded
- All instructions for agent to follow

## What We Need to Build

Based on Jesse's working implementation, here's what your team needs:

### Minimal Working System

1. **Shell Script: `codex-skills`**
   - `codex-skills list` - discovery function
   - `codex-skills use <name>` - loader function
   - Scans `~/.codex/skills/` for SKILL.md files
   - Parses YAML frontmatter
   - Outputs formatted results

2. **AGENTS.md Bootstrap**
   - Runs `codex-skills list` on startup
   - Provides tool mappings for Codex
   - Sets mandatory usage rules
   - Uses strong imperative language

3. **Sample Skills**
   - Time-awareness (your primary use case)
   - 1-2 others as examples
   - Follow Jesse's SKILL.md format exactly

### Key Differences from My Original Implementation

**What I Got Right:**
- Basic three-component architecture
- YAML frontmatter format
- Strong imperative language in bootstrap
- Mandatory skill usage enforcement

**What I Learned from Jesse:**
- Need explicit tool mapping for Codex
- Skills should announce when they're being used
- Personal skills can override shared skills
- `when_to_use` field is critical for discovery
- Bootstrap should output skill list directly in AGENTS.md

**What to Keep from My Implementation:**
- Clean separation of scripts
- Test-first approach
- Comprehensive documentation
- Installation automation

**What to Change:**
- Add tool mapping section to AGENTS.md
- Include `when_to_use` in YAML frontmatter
- Make skills announce usage
- Follow Jesse's SKILL.md structure more closely

## Recommended Approach

### Phase 1: Validate Core Concept (10 minutes)
Test if Codex actually executes bash blocks in AGENTS.md:

```markdown
# Test AGENTS.md
<EXTREMELY_IMPORTANT>
RIGHT NOW run this command: `echo "Codex can execute bash blocks"` and show me the output.
</EXTREMELY_IMPORTANT>
```

If this works, the whole system will work.

### Phase 2: Minimal Implementation (1 hour)
Build simplified version of Jesse's approach:
- One shell script with `list` and `use` commands
- AGENTS.md with bootstrap and tool mappings
- One working skill (time-awareness)

### Phase 3: Testing & Refinement (30 minutes)
- Test skill discovery
- Test skill activation
- Refine based on actual Codex behavior
- Add second skill to verify system works

### Phase 4: Team Documentation (20 minutes)
- Document your implementation
- Create team installation guide
- Show how to create new skills

## Safety & Review Considerations

Your team will want to review:

1. **The shell script** - what commands does it execute?
2. **AGENTS.md content** - what gets injected into Codex?
3. **Skill content** - what instructions are agents following?
4. **File permissions** - where can it read/write?
5. **Network access** - does it fetch anything external?

All of these are inspectable and auditable in our implementation.

## Bottom Line

Jesse's implementation proves:
- ✅ Skills work in Codex
- ✅ Takes ~2 hours to implement
- ✅ Shell scripts are sufficient
- ✅ AGENTS.md bootstrap works
- ✅ Codex follows instructions very literally

We now have real working code to reference and a proven pattern to follow.

**Next step:** Build minimal implementation based on Jesse's working approach, but as our own clean implementation for team review.
