# SREcodex Feature Management

This directory tracks features, bugs, and improvements for SREcodex using a structured workflow.

## Quick Start

To process the feature backlog:

1. Read `OVERPROMPT.md`
2. Follow the phases in order
3. The workflow is self-documenting

## Structure

```
feature-management/
├── OVERPROMPT.md        # Self-executing workflow
├── features/            # Active feature requests
│   ├── features.md      # Summary index of all features
│   └── FEAT-XXX-*/      # Individual feature directories
│       ├── feature_request.json  # Structured metadata
│       └── PROMPT.md             # Implementation specification
├── bugs/                # Bug reports
│   └── bugs.md          # Summary index of all bugs
├── completed/           # Archived completed work items
├── human-actions/       # Items requiring human intervention
└── UPDATE_LOG.md        # Change history
```

## Creating New Features

1. Create directory: `features/FEAT-XXX-slug/`
2. Add `feature_request.json` with required metadata
3. Add `PROMPT.md` with implementation instructions
4. Update `features/features.md` index

## Current Focus: Advanced Tool Use Upgrade

The initial feature set establishes infrastructure for intelligent skill discovery:

| Priority | Feature | Description |
|----------|---------|-------------|
| P1 | FEAT-001 | Skill Standardization Schema |
| P1 | FEAT-002 | Librarian Dynamic Discovery Skill |
| P1 | FEAT-005 | OVERPROMPT Workflow Implementation |
| P2 | FEAT-003 | MCP & Vector Search Backend |
| P2 | FEAT-004 | Script-First Programmatic Orchestration |

See `features/features.md` for the dependency graph and full index.

Pattern reference: `~/projects/featmgmt`
