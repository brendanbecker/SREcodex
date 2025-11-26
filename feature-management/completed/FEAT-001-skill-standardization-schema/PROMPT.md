# FEAT-001: Skill Standardization Schema

## Objective

Define and implement a standardized structure for all SKILL.md files that separates searchable metadata from executable content, enabling future vector indexing while improving model accuracy through few-shot examples.

## Background

Current skills lack consistent structure. To support:
- **Dynamic Discovery**: Vector search needs clean metadata to embed
- **Few-Shot Accuracy**: Models perform better with concrete Q&A examples
- **RAG Without Chunking**: Full document retrieval requires clear signal/payload separation

Reference: [Anthropic Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)

## Deliverables

### 1. Schema Definition

Define the YAML frontmatter schema:

```yaml
---
name: "Human-readable skill name"
tags: ["keyword1", "keyword2", "keyword3"]
intent: "Natural language description of when to use this skill. Be specific about trigger phrases and use cases."
risk_level: "low|medium|high"  # Optional
requires_confirmation: false    # Optional
---
```

### 2. SKILL.md Template

Create `dotcodex/templates/SKILL.template.md` with:
- YAML frontmatter block
- `# Skill: [name]` header
- `## Usage` section
- `## Examples` section (minimum 2 few-shot pairs)
- `## Implementation` section (the executable payload)

### 3. Examples Section Standard

All skills must include:

```markdown
## Examples

User: "[Common phrasing of request]"
Agent: [Exact action or command]

User: "[Edge case or variation]"
Agent: [Appropriate response]
```

### 4. Migration Checklist

Audit existing skills in `dotcodex/skills/` and list those requiring updates.

## Acceptance Criteria

- [ ] Schema formally documented in `dotcodex/docs/SKILL-SCHEMA.md`
- [ ] Template created at `dotcodex/templates/SKILL.template.md`
- [ ] At least 2 existing skills migrated to new format as examples
- [ ] Migration checklist created for remaining skills

## Notes

This feature is a prerequisite for:
- FEAT-002: Librarian Dynamic Discovery Skill
- FEAT-003: MCP & Vector Search Backend
- FEAT-004: Script-First Programmatic Orchestration
