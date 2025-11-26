# FEAT-007: Skill Audit Script

## Objective

Create a script that audits all SKILL.md files and produces a quality report, identifying issues like missing fields, stale versions, and incomplete content.

## Background

As the skill library grows, manual review becomes impractical. An audit script can surface issues in one pass:
- Missing or empty frontmatter fields
- Stale version numbers
- Very short intents (likely incomplete)
- `script_first: true` skills missing the Script-First Directive section

## Deliverables

### 1. Audit Script

Create `dotcodex/scripts/skill-audit.py` (or `.sh`):

```python
#!/usr/bin/env python3
"""
Skill Audit Report Generator
Analyzes all SKILL.md files for quality issues.
"""

import os
import yaml
from pathlib import Path

SKILLS_DIR = "../skills"
MIN_INTENT_LENGTH = 100  # Characters
CURRENT_VERSION = "1.0.0"

def audit_skill(filepath):
    issues = []

    with open(filepath) as f:
        content = f.read()

    # Parse frontmatter
    if not content.startswith('---'):
        return [("ERROR", "Missing YAML frontmatter")]

    parts = content.split('---', 2)
    try:
        meta = yaml.safe_load(parts[1])
    except:
        return [("ERROR", "Invalid YAML frontmatter")]

    # Check required fields
    for field in ['name', 'tags', 'intent']:
        if not meta.get(field):
            issues.append(("ERROR", f"Missing required field: {field}"))

    # Check intent length
    intent = meta.get('intent', '')
    if len(intent) < MIN_INTENT_LENGTH:
        issues.append(("WARNING", f"Intent too short ({len(intent)} chars, min {MIN_INTENT_LENGTH})"))

    # Check version
    version = meta.get('version', '')
    if not version:
        issues.append(("WARNING", "Missing version field"))
    elif version < CURRENT_VERSION:
        issues.append(("INFO", f"Stale version: {version}"))

    # Check script_first directive
    if meta.get('script_first'):
        if 'Script-First Directive' not in content:
            issues.append(("WARNING", "script_first=true but missing Directive section"))

    return issues

def main():
    print("Skill Audit Report")
    print("=" * 50)

    skills_path = Path(__file__).parent.parent / "skills"

    for skill_file in skills_path.rglob("SKILL.md"):
        issues = audit_skill(skill_file)
        rel_path = skill_file.relative_to(skills_path.parent)

        if issues:
            print(f"\n⚠️  {rel_path}")
            for level, msg in issues:
                print(f"    [{level}] {msg}")
        else:
            print(f"\n✅ {rel_path}")

if __name__ == "__main__":
    main()
```

### 2. Makefile Target (Optional)

```makefile
skill-audit:
	python dotcodex/scripts/skill-audit.py
```

## Example Output

```
Skill Audit Report
==================================================

✅ skills/uv-python/SKILL.md

⚠️  skills/document-parser/SKILL.md
    [WARNING] script_first=true but missing Directive section

⚠️  skills/old-example/SKILL.md
    [WARNING] Intent too short (45 chars, min 100)
    [INFO] Stale version: 0.1.0

❌ skills/broken/SKILL.md
    [ERROR] Missing required field: tags
```

## Acceptance Criteria

- [ ] Script finds all SKILL.md files recursively
- [ ] Reports missing required fields (name, tags, intent)
- [ ] Reports short intents (< 100 chars configurable)
- [ ] Reports missing version field
- [ ] Reports stale versions (< current)
- [ ] Reports script_first skills missing directive section
- [ ] Clear visual output (✅/⚠️/❌ indicators)
- [ ] Exit code reflects issues found (0=clean, 1=warnings, 2=errors)

## Testing Plan

1. Run against current skill set → should pass with no errors
2. Create test skill with short intent → should show warning
3. Create test skill missing tags → should show error
4. Verify exit codes work correctly
