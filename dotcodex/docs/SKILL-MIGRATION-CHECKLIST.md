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
| `document-parser` | **Migrated** | Complex skill with scripts, Q&A examples added |
| `uv-python` | **Migrated** | Universal UV workflow, Q&A examples added |

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

## Completion Criteria

All skills are considered migrated when:
1. All skills in `dotcodex/skills/` use the new schema ✅
2. All skills have `## Examples` with minimum 2 Q&A pairs ✅
3. All skills pass the validation checklist ✅
4. `SKILL-SCHEMA.md` accurately reflects current implementation ✅

**Migration completed:** 2025-11-25

---

## References

- `dotcodex/docs/SKILL-SCHEMA.md` - Schema specification
- `dotcodex/templates/SKILL.template.md` - Skill template
- Migrated examples: `time-awareness`, `skill-builder`
