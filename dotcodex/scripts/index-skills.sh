#!/bin/bash
# index-skills.sh - Generate searchable index from skill YAML frontmatter
# Part of FEAT-002: Librarian Dynamic Discovery

set -euo pipefail

# Determine skills directory
CODEX_CONFIG="${HOME}/.codex/config.env"
if [[ -f "${CODEX_CONFIG}" ]]; then
    source "${CODEX_CONFIG}"
fi

CODEX_DIR="${DOTCODEX_DIR:-${HOME}/.codex}"
SKILLS_DIR="${CODEX_DIR}/skills"
INDEX_FILE="${SKILLS_DIR}/INDEX.md"

if [[ ! -d "${SKILLS_DIR}" ]]; then
    echo "Error: Skills directory not found at ${SKILLS_DIR}"
    exit 1
fi

echo "Generating skills index at ${INDEX_FILE}..."

# Start index file
cat > "${INDEX_FILE}" << 'HEADER'
# Skills Index

Auto-generated index of available skills. Use `codex-skills search <query>` for dynamic discovery.

| Skill | Tags | Intent Summary | Path |
|-------|------|----------------|------|
HEADER

# Parse each SKILL.md and add to index
while IFS= read -r -d '' skill_file; do
    skill_dir=$(dirname "${skill_file}")
    skill_path=${skill_dir#${SKILLS_DIR}/}

    # Parse YAML frontmatter
    name="" tags="" intent=""
    in_frontmatter=false

    while IFS= read -r line; do
        if [[ "$line" == "---" ]]; then
            if $in_frontmatter; then
                break
            else
                in_frontmatter=true
                continue
            fi
        fi

        if $in_frontmatter; then
            if [[ "$line" =~ ^name:[[:space:]]*(.+)$ ]]; then
                name=$(echo "${BASH_REMATCH[1]}" | sed 's/^["\x27]\|["\x27]$//g')
            elif [[ "$line" =~ ^tags:[[:space:]]*(.+)$ ]]; then
                tags=$(echo "${BASH_REMATCH[1]}" | sed 's/\[//;s/\]//;s/"//g;s/,/, /g')
            elif [[ "$line" =~ ^intent:[[:space:]]*(.+)$ ]]; then
                intent=$(echo "${BASH_REMATCH[1]}" | sed 's/^["\x27]\|["\x27]$//g' | head -c 80)
            fi
        fi
    done < "${skill_file}"

    # Add row to table
    echo "| ${name:-${skill_path}} | ${tags} | ${intent}... | \`${skill_path}\` |" >> "${INDEX_FILE}"
done < <(find "${SKILLS_DIR}" -name "SKILL.md" -type f -print0 | sort -z)

# Add footer
cat >> "${INDEX_FILE}" << 'FOOTER'

---

## Quick Commands

```bash
# List all skills with descriptions
codex-skills list

# Search for a skill
codex-skills search "keyword"

# Load a skill
codex-skills use <path>
```

## Regenerate Index

```bash
./dotcodex/scripts/index-skills.sh
```
FOOTER

echo "Done! Index written to ${INDEX_FILE}"
echo ""
echo "Skills indexed:"
grep -c "^\|" "${INDEX_FILE}" | awk '{print $1 - 2}'
