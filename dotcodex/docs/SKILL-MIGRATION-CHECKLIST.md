# Skill Migration Checklist

**Version**: 1.0.0
**Created**: 2025-11-25

---

## Overview

This document tracks the migration of existing skills from the legacy format (`description`, `when_to_use`) to the new standardized schema (`tags`, `intent`).

## Migration Status

| Skill | Status | Notes |
|-------|--------|-------|
| `time-awareness` | **Migrated** | Baseline example |
| `skill-builder` | **Migrated** | Meta-skill, updated to teach new schema |
| `document-parser` | Pending | Complex skill with scripts |
| `uv-python` | Pending | Universal UV workflow |
| `uv-env-management` | Pending | Workspace-specific system |

---

## Migration Steps

For each pending skill, follow these steps:

### Step 1: Update YAML Frontmatter

**Before (Legacy):**
```yaml
---
name: Skill Name
description: One-line summary
when_to_use: When to trigger this skill
version: 1.0.0
languages: all
---
```

**After (New Schema):**
```yaml
---
name: "Skill Name"
tags: ["keyword1", "keyword2", "keyword3"]
intent: "[Combine description + when_to_use into comprehensive trigger description]"
version: "1.0.0"
languages: all
---
```

**Field Mapping:**
1. Keep `name` as-is (add quotes)
2. Extract keywords from `description` and `when_to_use` → create `tags` array
3. Combine `description` + `when_to_use` → create `intent` field
4. Keep `version` and `languages`
5. Add `risk_level` or `requires_confirmation` if applicable

### Step 2: Rename Overview to Usage

Change:
```markdown
## Overview
```

To:
```markdown
## Usage
```

Add explicit "Use this skill when:" and "Don't use when:" sections.

### Step 3: Add/Reformat Examples Section

Ensure the skill has an `## Examples` section with Q&A format:

```markdown
## Examples

User: "[Common phrasing of request]"
Agent: [Exact action or response]

User: "[Variation or edge case]"
Agent: [Appropriate response]
```

**Minimum 2 examples required.**

### Step 4: Validate

Run through the validation checklist:

- [ ] YAML frontmatter has `---` delimiters
- [ ] Required fields present: `name`, `tags`, `intent`
- [ ] `tags` array has at least 3 keywords
- [ ] `intent` is detailed and specific
- [ ] `## Examples` section exists with at least 2 Q&A pairs
- [ ] Examples use `User: "..."` / `Agent: ...` format
- [ ] No tabs in YAML (use spaces only)

---

## Pending Skills Details

### document-parser

**Location:** `dotcodex/skills/document-parser/SKILL.md`

**Current State:**
- Uses `description`, `when_to_use` format
- Has extensive implementation details
- Has examples but not in Q&A format

**Migration Notes:**
- Complex skill with Python scripts
- Preserve all implementation details
- Convert examples to Q&A format
- Add tags for: document, parse, chunk, RAG, large, token, structure, metadata

### uv-python

**Location:** `dotcodex/skills/uv-python/SKILL.md`

**Current State:**
- Uses `description`, `when_to_use` format
- Good examples but not in Q&A format

**Migration Notes:**
- Straightforward migration
- Add tags for: uv, python, pip, pytest, jupyter, dependency, virtual environment
- Convert "Real-World Examples" to Q&A format

### uv-env-management

**Location:** `dotcodex/skills/uv-env-management/SKILL.md`

**Current State:**
- Uses `description`, `when_to_use` format
- Workspace-specific documentation
- Limited examples section

**Migration Notes:**
- Add Q&A examples for common workflows
- Add tags for: workspace, project, template, agent, RAG, notebook, API
- Consider risk_level for directory operations

---

## Completion Criteria

All skills are considered migrated when:
1. All skills in `dotcodex/skills/` use the new schema
2. All skills have `## Examples` with minimum 2 Q&A pairs
3. All skills pass the validation checklist
4. `SKILL-SCHEMA.md` accurately reflects current implementation

---

## References

- `dotcodex/docs/SKILL-SCHEMA.md` - Schema specification
- `dotcodex/templates/SKILL.template.md` - Skill template
- Migrated examples: `time-awareness`, `skill-builder`
