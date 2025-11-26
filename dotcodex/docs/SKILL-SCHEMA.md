# Skill Schema Specification

**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-11-25

---

## Overview

This document defines the standardized structure for all SKILL.md files in the SREcodex skill library. The schema separates searchable metadata (YAML frontmatter) from executable content, enabling future vector indexing while improving model accuracy through few-shot examples.

## YAML Frontmatter Schema

Every SKILL.md file MUST begin with a YAML frontmatter block:

```yaml
---
name: "Human-readable skill name"
tags: ["keyword1", "keyword2", "keyword3"]
intent: "Natural language description of when to use this skill. Be specific about trigger phrases, user requests, symptoms, and use cases."
version: "1.0.0"
languages: all
risk_level: low
requires_confirmation: false
---
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Human-readable skill name. Use Title Case. Should be descriptive and searchable. |
| `tags` | string[] | Keywords for search/discovery. Include trigger words, synonyms, and related concepts. Minimum 3 tags recommended. |
| `intent` | string | Comprehensive description of when to use this skill. Combine what the skill does with when to trigger it. Include specific user phrases, error messages, and symptoms. |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `version` | string | `"1.0.0"` | Semantic version of the skill. |
| `languages` | string \| string[] | `"all"` | Programming languages this skill applies to. Use `"all"` for universal skills. |
| `risk_level` | string | - | Risk classification: `"low"`, `"medium"`, or `"high"`. Use for skills that modify files, execute commands, or access external systems. |
| `requires_confirmation` | boolean | `false` | If `true`, agent should confirm with user before executing. Use for destructive or irreversible operations. |

### Field Guidelines

#### `name`
- Use Title Case: "Time Awareness" not "time-awareness"
- Be descriptive: "UV Python Workflow" not "UV"
- Keep it concise: 2-4 words typically

#### `tags`
- Include the skill name words (without spaces)
- Add common trigger phrases users might say
- Include related tools, technologies, or concepts
- Include error messages or symptoms if applicable

**Good tags example:**
```yaml
tags: ["date", "time", "today", "tomorrow", "schedule", "deadline", "calendar", "temporal", "timezone"]
```

#### `intent`
- Start with what the skill does
- Include when to use it (trigger conditions)
- Be specific about user phrases that should activate the skill
- Mention error messages or symptoms if relevant
- This field is critical for discovery - be thorough

**Good intent example:**
```yaml
intent: "Provides current date/time information for temporal queries and calculations. Use when user asks about dates, times, schedules, 'today', 'tomorrow', 'this week', deadlines, or anything requiring knowledge of current time. Triggers on relative time references, temporal calculations, or scheduling tasks."
```

---

## Document Structure

After the YAML frontmatter, SKILL.md files MUST follow this structure:

```markdown
---
[YAML frontmatter]
---

# [Skill Name]

## Usage

[Brief explanation of what this skill does and the core principle. 2-3 sentences.]

## Examples

User: "[Common phrasing of request]"
Agent: [Exact action or response]

User: "[Variation or edge case]"
Agent: [Appropriate response]

[Minimum 2 examples required]

## Implementation

[Detailed step-by-step instructions, code examples, workflows]
```

### Section Requirements

#### `# [Skill Name]`
Main heading matching the `name` field in frontmatter.

#### `## Usage`
- Brief explanation of what the skill does
- Core principle or philosophy
- When to use and when NOT to use
- 2-5 sentences

#### `## Examples` (REQUIRED)
Few-shot Q&A pairs demonstrating skill usage:
- Minimum 2 examples required
- Use format: `User: "..."` followed by `Agent: ...`
- Include common case and at least one edge case or variation
- Examples should be concrete and actionable

**Example format:**
```markdown
## Examples

User: "What day is it today?"
Agent: Run `date '+%Y-%m-%d %A'` and respond with full date context.

User: "How many days until my deadline on December 15th?"
Agent: Calculate days remaining using `date -d "2025-12-15" +%s` minus current timestamp, then report the count with the target date.
```

#### `## Implementation`
Detailed instructions for executing the skill:
- Step-by-step workflows
- Code examples with comments
- Command references
- Common mistakes and how to avoid them
- Troubleshooting tips

---

## Validation Checklist

Before committing a skill, verify:

- [ ] YAML frontmatter has `---` delimiters
- [ ] Required fields present: `name`, `tags`, `intent`
- [ ] Tags array has at least 3 keywords
- [ ] Intent is detailed and specific
- [ ] `## Examples` section has at least 2 Q&A pairs
- [ ] Examples use `User: "..."` / `Agent: ...` format
- [ ] No tabs in YAML (use spaces only)
- [ ] Headers use proper `##` markdown format

---

## Migration from Legacy Format

Skills using the legacy format (`description`, `when_to_use`) should be migrated:

| Legacy Field | New Field | Migration |
|--------------|-----------|-----------|
| `name` | `name` | Keep as-is |
| `description` | → `intent` | Merge into intent |
| `when_to_use` | → `intent` | Merge into intent |
| `version` | `version` | Keep as-is |
| `languages` | `languages` | Keep as-is |
| (none) | `tags` | Extract keywords from description/when_to_use |

See `SKILL-MIGRATION-CHECKLIST.md` for step-by-step migration instructions.

---

## References

- [Anthropic Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use) - Design principles
- `dotcodex/templates/SKILL.template.md` - Skill template
- `dotcodex/docs/SKILL-MIGRATION-CHECKLIST.md` - Migration guide
