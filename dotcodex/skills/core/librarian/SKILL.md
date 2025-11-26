---
name: "Skill Librarian"
tags: ["core", "discovery", "search", "meta", "find", "help", "skills", "capability", "tool"]
intent: "Use this to find and load skills when you encounter a task outside your current capabilities. Search by keyword, domain, or natural language description of what you need. Triggers when you think 'I don't have a skill for this' or when the user asks about available capabilities."
always_load: true
version: "1.0.0"
---

# Skill Librarian

## Usage

The Librarian discovers skills on-demand so you don't need every skill preloaded. When you lack capability for a task, search the skill library and dynamically load what you need.

**Use this when:**
- You recognize a task outside your currently loaded skills
- User asks "what can you do?" or "do you have a skill for X?"
- You encounter an unfamiliar domain (Redis, Kubernetes, AWS, etc.)

## Search Commands

```bash
# Search skills by keyword in tags/intent
codex-skills search "keyword"

# Or use grep directly on YAML frontmatter:
grep -r -l "keyword" ~/.codex/skills/*/SKILL.md

# Search intent field specifically
grep -A2 "^intent:" ~/.codex/skills/*/SKILL.md | grep -i "search term"

# Find skill directories by name
find ~/.codex/skills -type d -name "*keyword*"
```

## Discovery Workflow

1. **DETECT**: Recognize you lack capability - "I don't have a skill for [X]"
2. **SEARCH**: `codex-skills search "description of what I need"`
3. **EVALUATE**: Review returned skill summaries (top 3 if multiple)
4. **LOAD**: `codex-skills use <best-match>`
5. **EXECUTE**: Follow the loaded skill's instructions

## Examples

User: "The redis cache is timing out"
Agent: I need Redis troubleshooting skills. Let me search: `codex-skills search "redis timeout cache"`. Found `skills/db/redis-tuning` - loading it now with `codex-skills use db/redis-tuning`, then applying to diagnose the timeout.

---

User: "Parse these CloudWatch logs for errors"
Agent: I need log analysis capabilities. Searching: `codex-skills search "cloudwatch logs parse"`. Found `skills/aws/cloudwatch-logs`. Loading with `codex-skills use aws/cloudwatch-logs` and following its instructions to query the logs.

---

User: "Restart the stuck deployment"
Agent: I need Kubernetes deployment skills. Searching: `codex-skills search "kubernetes restart deployment"`. Found `skills/k8s/deployment-ops`. Loading it to perform the restart safely.

---

User: "What skills do you have for databases?"
Agent: Let me search the library: `codex-skills search "database"`. Found 3 matches: `db/postgres-admin` (PostgreSQL management), `db/redis-tuning` (Redis performance), `db/migrations` (schema migrations). Would you like me to load any of these?

## Search Priority

When multiple skills match, prioritize by:
1. Exact tag match
2. Intent field contains query terms
3. Skill name contains query
4. Directory name contains query

## Quick Reference

| Need | Command |
|------|---------|
| List all skills | `codex-skills list` |
| Search by keyword | `codex-skills search "keyword"` |
| Load specific skill | `codex-skills use skill-name` |
| Browse index | `cat ~/.codex/skills/INDEX.md` |

---

**Remember:** Don't preload everything. Search, evaluate, load what you need, then execute.
