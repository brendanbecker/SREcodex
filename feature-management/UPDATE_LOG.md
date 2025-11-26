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
