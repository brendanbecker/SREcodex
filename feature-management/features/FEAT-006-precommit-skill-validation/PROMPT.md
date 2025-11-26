# FEAT-006: Pre-commit Hook for SKILL.md Validation

## Objective

Create a git pre-commit hook that validates SKILL.md files have required YAML frontmatter before allowing commits.

## Background

The MCP indexer (`index_skills.py`) silently skips SKILL.md files missing proper frontmatter. This creates a frustrating debugging experience—skills appear to exist but don't show up in semantic search.

A pre-commit hook catches these issues immediately, before they enter the repo.

## Deliverables

### 1. Pre-commit Hook Script

Create `.git/hooks/pre-commit` or use the `pre-commit` framework:

```bash
#!/bin/bash
# Validate SKILL.md files have required frontmatter

for file in $(git diff --cached --name-only | grep 'SKILL\.md$'); do
    if [[ ! -f "$file" ]]; then
        continue  # File was deleted
    fi

    # Check for YAML frontmatter delimiter
    if ! head -1 "$file" | grep -q '^---$'; then
        echo "ERROR: $file missing YAML frontmatter (must start with ---)"
        exit 1
    fi

    # Check required fields
    for field in name tags intent; do
        if ! grep -q "^${field}:" "$file"; then
            echo "ERROR: $file missing required field '$field' in frontmatter"
            exit 1
        fi
    done
done

echo "SKILL.md validation passed"
```

### 2. Optional: pre-commit Framework Config

If using the `pre-commit` Python framework:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: validate-skill-frontmatter
        name: Validate SKILL.md frontmatter
        entry: scripts/validate-skill.sh
        language: script
        files: SKILL\.md$
```

## Acceptance Criteria

- [ ] Hook prevents commits of SKILL.md files missing `---` delimiter
- [ ] Hook prevents commits of SKILL.md files missing `name` field
- [ ] Hook prevents commits of SKILL.md files missing `tags` field
- [ ] Hook prevents commits of SKILL.md files missing `intent` field
- [ ] Hook passes for valid SKILL.md files
- [ ] Hook ignores deleted files
- [ ] Clear error messages indicate which file and field failed

## Testing Plan

1. Create a test SKILL.md without frontmatter → commit should fail
2. Create a test SKILL.md with frontmatter but missing `tags` → commit should fail
3. Create a valid SKILL.md → commit should succeed
4. Delete a SKILL.md → commit should succeed (no validation needed)
