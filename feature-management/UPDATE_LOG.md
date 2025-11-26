# Update Log

## 2025-11-25

- Initialized feature-management structure
- Created FEAT-001: Skill Standardization Schema
- Created FEAT-005: OVERPROMPT Workflow Implementation
- Created OVERPROMPT.md v1.0.0

## 2025-11-25 (continued)

- Created FEAT-002: Librarian Dynamic Discovery Skill
- Defined grep-based search implementation (pre-MCP)
- Documented upgrade path to semantic search (FEAT-003)

## 2025-11-25 (continued)

- Created FEAT-003: MCP & Vector Search Backend
- Defined ChromaDB setup (Docker and embedded options)
- Documented index_skills.py ingestion pipeline
- Documented mcp_server.py with search_skills() tool
- Specified parent-child indexing pattern (embed intent, retrieve full doc)

## 2025-11-25 (continued)

- Created FEAT-004: Script-First Programmatic Orchestration
- Defined workspace-write sandbox configuration
- Documented Script-First directive standard
- Created Orchestrator skill for multi-skill composition
- Updated implementation order (FEAT-002 and FEAT-004 can parallel)

## 2025-11-25: FEAT-001 Completed

- **FEAT-001: Skill Standardization Schema** resolved
- Created `dotcodex/docs/SKILL-SCHEMA.md` with formal schema specification
- Created `dotcodex/templates/SKILL.template.md` with standardized structure
- Migrated `time-awareness` skill to new schema (tags, intent, Q&A examples)
- Migrated `skill-builder` skill to new schema (updated to teach new format)
- Created `dotcodex/docs/SKILL-MIGRATION-CHECKLIST.md` for remaining skills
- Schema consolidates `description` + `when_to_use` → `intent`
- New `tags` field enables keyword-based discovery
- `## Examples` section now requires Q&A format (minimum 2 pairs)
- Remaining skills pending migration: document-parser, uv-python, uv-env-management
- FEAT-005 (OVERPROMPT Workflow) validated as byproduct

## 2025-11-25: FEAT-002 Completed

- **FEAT-002: Librarian Dynamic Discovery Skill** resolved
- Created `dotcodex/skills/core/librarian/SKILL.md` with FEAT-001 compliant schema
- Librarian includes 4 discovery workflow examples
- Added `search` command to `codex-skills` script with scoring algorithm:
  - Exact tag match: 100 points
  - Tag contains query: 50 points
  - Intent contains query: 30 points
  - Name contains query: 20 points
  - Path contains query: 10 points
- Created `dotcodex/scripts/index-skills.sh` for INDEX.md generation
- Updated `dotcodex/AGENTS.md` with Librarian-first discovery workflow
- Removed static skill listing instructions in favor of on-demand search
- Fixed `((count++))` bug in bash with `set -e` (exit on 0 return)
- Search returns top 3 matches with intent summaries
- End-to-end tested: search finds skills, use command loads them

## 2025-11-26: FEAT-004 Completed

- **FEAT-004: Script-First Programmatic Orchestration** resolved
- Created `dotcodex/config.toml` with `sandbox_mode = "workspace-write"`
- Created `dotcodex/docs/SCRIPT-FIRST-DIRECTIVE.md` with standard directive text
- Created `dotcodex/docs/SCRIPT-FIRST-SKILLS.md` checklist:
  - Applied: document-parser (multi-document processing)
  - Planned: k8s/bulk-restart, logs/cloudwatch-search, monitoring/alert-triage
- Created `dotcodex/skills/core/orchestrator/SKILL.md`:
  - FEAT-001 compliant (YAML frontmatter with tags/intent)
  - Script-first directive included
  - 3 composition examples (deploy+verify+rollback, crashloop restart, health+jira)
  - Templates for sequential, conditional, parallel, and error aggregation patterns
- Updated `dotcodex/templates/SKILL.template.md`:
  - Added `script_first: false` optional field
  - Added commented Script-First Directive section template
- Created `dotcodex/docs/PROGRAMMATIC-ORCHESTRATION.md`:
  - Documents the "Script-First" pattern
  - ASCII diagrams comparing chat-based vs script-first approaches
  - Orchestration patterns with code examples
  - Testing criteria for script-first validation
- Updated `dotcodex/skills/INDEX.md` with Workflow Orchestrator skill
- End-to-end tests documented (require runtime environment for execution)
