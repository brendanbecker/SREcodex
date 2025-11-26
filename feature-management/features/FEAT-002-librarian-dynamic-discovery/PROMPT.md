# FEAT-002: Librarian Dynamic Discovery Skill

## Objective

Implement a "Librarian" skill that discovers and loads other skills on-demand, eliminating the need to preload all skill definitions into the context window.

## Background

### The Problem

Loading every available skill at startup:
- Consumes excessive tokens (~77K+ for large skill libraries)
- Confuses the model with irrelevant tools
- Reduces response quality by diluting attention

### The Solution (Anthropic's Tool Search Tool Pattern)

> "Instead of loading all tool definitions upfront, the Tool Search Tool discovers tools on-demand. Claude only sees the tools it actually needs for the current task."

The Librarian implements this pattern for Codex:
1. Always loaded in base profile (small footprint)
2. Searches skill repository when capability is needed
3. Returns full SKILL.md content for dynamic loading

### Dependency

**Requires FEAT-001**: Skills must have YAML frontmatter with `name`, `tags`, and `intent` fields for effective searching.

## Implementation Plan

### Section 1: Create Librarian Skill File

**File**: `dotcodex/skills/core/librarian/SKILL.md`

**Structure**:
```yaml
---
name: "Skill Librarian"
tags: ["core", "discovery", "search", "meta"]
intent: "Use this to find and load skills when you encounter a task outside your current capabilities. Search by keyword, domain, or natural language description of what you need to do."
always_load: true
---
```

**Skill Content**:
- Description of the Librarian's purpose
- Usage instructions for the agent
- Search command templates (grep/find based)
- Examples of discovery workflows

### Section 2: Implement Search Logic

**Primary Search Method**: grep over YAML frontmatter

```bash
# Search by keyword in tags/intent
grep -r -l "keyword" dotcodex/skills/*/SKILL.md

# Search intent field specifically
grep -A2 "^intent:" dotcodex/skills/*/SKILL.md | grep -i "search term"
```

**Fallback Search Method**: find by directory name

```bash
# Find skill directories matching pattern
find dotcodex/skills -type d -name "*keyword*"
```

**Search Priority**:
1. Exact tag match
2. Intent field contains query
3. Skill name contains query
4. Directory name contains query

### Section 3: Define Discovery Workflow

When the agent recognizes it lacks a capability:

1. **DETECT**: "I don't have a skill for [X]"
2. **SEARCH**: Call Librarian with query describing needed capability
3. **EVALUATE**: Review returned skill summaries
4. **LOAD**: Read full SKILL.md of best match
5. **EXECUTE**: Apply the newly loaded skill to the task

### Section 4: Update Base Configuration

**File**: `dotcodex/config.toml` or equivalent

Add Librarian to always-loaded skills:

```toml
[skills]
always_load = ["core/librarian"]
```

### Section 5: Refactor Existing Skill References

**Task**: Audit and update any files that statically list available skills.

- Remove hardcoded skill lists from agent prompts
- Replace with Librarian discovery pattern
- Keep only essential always-loaded skills (3-5 max)

### Section 6: Create Search Index Helper (Optional)

**File**: `dotcodex/scripts/index-skills.sh`

Simple script to generate a searchable index:

```bash
#!/bin/bash
# Generate skills index from YAML frontmatter

echo "# Skills Index" > dotcodex/skills/INDEX.md
echo "" >> dotcodex/skills/INDEX.md

for skill in dotcodex/skills/*/SKILL.md; do
  name=$(grep "^name:" "$skill" | cut -d'"' -f2)
  tags=$(grep "^tags:" "$skill" | cut -d'[' -f2 | cut -d']' -f1)
  intent=$(grep "^intent:" "$skill" | cut -d'"' -f2 | head -c 100)
  dir=$(dirname "$skill")

  echo "## $name" >> dotcodex/skills/INDEX.md
  echo "- **Path**: $dir" >> dotcodex/skills/INDEX.md
  echo "- **Tags**: $tags" >> dotcodex/skills/INDEX.md
  echo "- **Intent**: $intent..." >> dotcodex/skills/INDEX.md
  echo "" >> dotcodex/skills/INDEX.md
done
```

## Deliverables

1. `dotcodex/skills/core/librarian/SKILL.md` — The Librarian skill itself
2. Updated `config.toml` — Librarian in always_load
3. `dotcodex/scripts/index-skills.sh` — Index generator (optional)
4. Documentation updates explaining the discovery pattern

## Acceptance Criteria

- [ ] Librarian SKILL.md created with proper YAML frontmatter (FEAT-001 compliant)
- [ ] Librarian includes `## Examples` section with 3+ discovery scenarios
- [ ] Search logic implemented (grep-based, no external dependencies)
- [ ] Config updated to always-load Librarian
- [ ] Static skill lists removed from agent prompts
- [ ] INDEX.md generated successfully by helper script
- [ ] End-to-end test: Agent discovers and loads a skill it didn't have

## Examples (For Librarian SKILL.md)

Include these in the Librarian's own `## Examples` section:

```markdown
## Examples

**User**: "The redis cache is timing out"
**Agent** (thinking): I don't have Redis skills loaded.
**Agent**: Search skills for "redis timeout cache"
**Librarian**: Found `skills/db/redis-tuning/SKILL.md` - "Use for Redis performance issues, timeouts, memory pressure"
**Agent**: [Reads redis-tuning skill, now has capability]

---

**User**: "Parse these CloudWatch logs for errors"
**Agent** (thinking): I need log parsing capabilities.
**Agent**: Search skills for "cloudwatch logs parse errors"
**Librarian**: Found `skills/aws/cloudwatch-logs/SKILL.md` - "Query and analyze CloudWatch log groups"
**Agent**: [Reads cloudwatch-logs skill, executes log analysis]

---

**User**: "Restart the stuck deployment"
**Agent** (thinking): Need Kubernetes deployment management.
**Agent**: Search skills for "kubernetes restart deployment stuck"
**Librarian**: Found `skills/k8s/deployment-ops/SKILL.md` - "Manage deployments, rollouts, restarts"
**Agent**: [Reads deployment-ops skill, performs restart]
```

## Future Enhancement (FEAT-003)

This grep-based implementation will be upgraded to semantic search via MCP/ChromaDB in FEAT-003. The Librarian's interface remains the same; only the search backend changes.

## Notes

- Keep Librarian footprint small (~50 lines) to minimize always-loaded overhead
- Search should complete in <1 second for repositories with <100 skills
- If search returns multiple matches, return top 3 with summaries for agent to choose
