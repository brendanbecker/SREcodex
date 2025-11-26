# Features Index

| ID | Title | Priority | Status | Component |
|----|-------|----------|--------|-----------|
| FEAT-001 | Skill Standardization Schema | P1 | resolved | dotcodex/skills |
| FEAT-002 | Librarian Dynamic Discovery Skill | P1 | resolved | dotcodex/skills/core |
| FEAT-003 | MCP & Vector Search Backend | P2 | resolved | mcp-server |
| FEAT-004 | Script-First Programmatic Orchestration | P2 | resolved | dotcodex/config |
| FEAT-005 | OVERPROMPT Workflow Implementation | P1 | resolved | feature-management |

## Dependency Graph

```
FEAT-005 (OVERPROMPT) ─── standalone, enables all others

FEAT-001 (Skill Standardization)
    ├── FEAT-002 (Librarian) ──► FEAT-003 (MCP/Vector)
    └── FEAT-004 (Script-First)
```

## Implementation Order

1. **FEAT-005** (OVERPROMPT) - Process enablement
2. **FEAT-001** (Skill Schema) - Foundation for all skills
3. **FEAT-002** (Librarian) - Discovery with grep fallback
4. **FEAT-004** (Script-First) - Orchestration pattern *(can parallel with FEAT-002)*
5. **FEAT-003** (MCP/Vector) - Semantic search upgrade

## Notes

- FEAT-002 and FEAT-004 can be developed in parallel after FEAT-001
- FEAT-003 is an upgrade to FEAT-002, not a blocker
