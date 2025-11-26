# Migrating Existing Skills

This guide helps upgrade pre-existing skills to the FEAT-001 compliant format with YAML frontmatter and few-shot examples.

## What Needs to Change

Old skills may be missing:

| Required | Purpose |
|----------|---------|
| YAML frontmatter | `name`, `tags`, `intent` for semantic search |
| `## Examples` section | Few-shot Q&A pairs for accuracy |
| `## Usage` section | When to use / not use |

## Quick Check

Run this to see which skills need migration:

```bash
cd mcp-server && make index 2>&1 | grep -E "(SKIP|Indexed)"
```

Skills showing `SKIP: No frontmatter` need updating.

## Migration Prompt

Copy this prompt into Codex or Claude to migrate a skill:

---

```
Migrate this skill to the FEAT-001 compliant format.

Skill file: [PATH_TO_SKILL.md]

Requirements:
1. Add YAML frontmatter with:
   - name: Human-readable skill name
   - tags: 3-5 searchable keywords
   - intent: 2-3 sentences describing WHEN to use this skill (trigger phrases, symptoms, use cases)
   - version: "1.0.0"
   - languages: all (or specific languages)

2. Ensure these sections exist:
   - ## Usage (what it does, when to use, when NOT to use)
   - ## Examples (minimum 3 few-shot User/Agent pairs)
   - ## Implementation (the actual commands/code)

3. Keep all existing functionality intact

4. Use the template at dotcodex/templates/SKILL.template.md as reference

Output the complete updated skill file.
```

---

## Batch Migration Script

For multiple skills, use this prompt:

---

```
Scan dotcodex/skills/ for skills missing YAML frontmatter.

For each skill found:
1. Read the current content
2. Infer appropriate name, tags, and intent from the content
3. Add proper frontmatter
4. Ensure Examples section exists (create from existing content if possible)
5. Write the updated file

Report which skills were updated and what was added.
```

---

## Manual Migration Steps

1. **Open the skill file**

2. **Add frontmatter at the top:**
   ```yaml
   ---
   name: "Your Skill Name"
   tags: ["keyword1", "keyword2", "keyword3"]
   intent: "Use this when the user needs to [specific task]. Good for [symptoms/triggers]."
   version: "1.0.0"
   languages: all
   ---
   ```

3. **Add Examples section** (if missing):
   ```markdown
   ## Examples

   User: "How do I [common request]?"
   Agent: [Exact response with commands]

   User: "[Variation of request]"
   Agent: [Appropriate response]

   User: "[Edge case]"
   Agent: [How to handle it]
   ```

4. **Re-index:**
   ```bash
   cd mcp-server && make reindex
   ```

## Validation

After migration, verify the skill is indexed:

```bash
cd mcp-server
uv run python -c "
import chromadb
from chromadb.utils import embedding_functions
client = chromadb.PersistentClient('./chroma_data')
coll = client.get_collection('srecodex_skills', embedding_function=embedding_functions.DefaultEmbeddingFunction())
for item in coll.get()['metadatas']:
    print(f\"- {item['name']}\")
"
```

Your skill should appear in the list.

## Example Migration

**Before:**
```markdown
# Redis Troubleshooting

Use this to fix Redis issues.

## Commands

Check status:
\`\`\`bash
redis-cli ping
\`\`\`
```

**After:**
```markdown
---
name: "Redis Troubleshooting"
tags: ["redis", "cache", "database", "troubleshooting", "performance"]
intent: "Use this when Redis is slow, timing out, or returning errors. Good for connection issues, memory problems, and cache debugging."
version: "1.0.0"
languages: all
---

# Redis Troubleshooting

## Usage

Diagnose and fix common Redis issues including connection failures, timeouts, memory pressure, and slow queries.

**Use this skill when:**
- Redis commands are timing out
- Cache hit rates are low
- Memory usage is high
- Connections are being refused

**Don't use when:**
- Setting up Redis for the first time (use redis-setup skill)
- Configuring Redis Cluster (use redis-cluster skill)

## Examples

User: "Redis is timing out, help me debug"
Agent: First check if Redis is responding: `redis-cli ping`. Then check memory: `redis-cli info memory | grep used_memory_human`

User: "Why is my Redis so slow?"
Agent: Check slow queries with `redis-cli slowlog get 10` and monitor real-time with `redis-cli monitor` (careful in production)

User: "Redis connection refused"
Agent: Verify Redis is running: `systemctl status redis`. Check bind address in /etc/redis/redis.conf and ensure port 6379 is open.

## Implementation

### Quick Reference

| Task | Command |
|------|---------|
| Check status | `redis-cli ping` |
| Memory usage | `redis-cli info memory` |
| Slow queries | `redis-cli slowlog get 10` |
| Connected clients | `redis-cli info clients` |

### Step-by-Step

1. **Verify connectivity**
   \`\`\`bash
   redis-cli ping
   # Should return PONG
   \`\`\`

2. **Check memory**
   \`\`\`bash
   redis-cli info memory | grep used_memory_human
   \`\`\`

3. **Review slow log**
   \`\`\`bash
   redis-cli slowlog get 10
   \`\`\`
```

## Need Help?

If you're unsure how to write the `intent` field, think about:
- What would someone type when they need this skill?
- What symptoms would they describe?
- What keywords would they use?

The intent field is the most important — it's what the semantic search matches against.
