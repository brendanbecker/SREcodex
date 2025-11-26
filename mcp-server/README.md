# SREcodex MCP Server

Semantic skill discovery backend using ChromaDB for vector storage and the MCP protocol for integration with Codex.

## Overview

This server enables natural language skill search. Instead of keyword matching, it uses semantic embeddings to find skills by intent.

**Key Design: Parent-Child Indexing**
- **Embed**: Only the intent field (searchable signal)
- **Retrieve**: Full SKILL.md content (executable payload)

This avoids the RAG chunking problem where partial code retrieval breaks skill functionality.

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Codex     │────►│ MCP Server  │────►│  ChromaDB   │
│  (Client)   │◄────│ (Bridge)    │◄────│  (Vectors)  │
└─────────────┘     └─────────────┘     └─────────────┘
                          │
                   search_skills()
                          │
                   ┌──────▼──────┐
                   │ Full SKILL.md│
                   │  (Retrieved) │
                   └─────────────┘
```

## Quick Start

```bash
cd mcp-server
make setup    # Install dependencies
make index    # Index skills to ChromaDB
make test     # Verify semantic search works
```

**Next step**: [Configure Codex to use this server →](SETUP.md)

### Use in Codex

Once configured, the `search_skills` tool is available:

```
search_skills(query="help me debug kubernetes pod crashes")
```

## Make Commands

| Command | Description |
|---------|-------------|
| `make setup` | Install dependencies via uv |
| `make index` | Index skills to ChromaDB |
| `make serve` | Run the MCP server manually |
| `make test` | Quick semantic search test |
| `make inspect` | Open MCP Inspector web UI |
| `make clean` | Remove ChromaDB data |
| `make reindex` | Clean and re-index from scratch |

## Files

| File | Purpose |
|------|---------|
| `SETUP.md` | **Codex integration guide** |
| `Makefile` | Development commands (setup, index, test, etc.) |
| `index_skills.py` | Ingestion pipeline - parses skills and stores in ChromaDB |
| `mcp_server.py` | MCP server - exposes `search_skills()` tool |
| `pyproject.toml` | Python project config and dependencies |
| `docker-compose.yml` | Optional Docker setup for ChromaDB |

## Commands

### Indexing

```bash
# Index from default location
python index_skills.py

# Index from custom path
python index_skills.py --skills-dir /path/to/skills

# Use custom ChromaDB path
python index_skills.py --chroma-path /custom/db/path
```

### Server

The server is typically started automatically by Codex, but can be run manually:

```bash
python mcp_server.py
```

### Docker (Alternative)

For isolated ChromaDB:

```bash
docker-compose up -d
```

Note: The default setup uses embedded Python ChromaDB, which is simpler for local development.

## Re-indexing

Run after adding or modifying skills:

```bash
python index_skills.py
```

The indexer uses upsert, so it's safe to re-run.

## Troubleshooting

### "Collection not found"

Run the indexer first:
```bash
python index_skills.py
```

### "chromadb not installed"

Install dependencies:
```bash
pip install -r requirements.txt
```

### No skills indexed

Check that skills have YAML frontmatter:
```yaml
---
name: "Skill Name"
tags: ["tag1", "tag2"]
intent: "Description of when to use this skill"
---
```

### Search returns irrelevant results

The default embedding model (all-MiniLM-L6-v2) is lightweight but limited. For better accuracy, consider upgrading to OpenAI or Cohere embeddings in future iterations.

## Data Model

ChromaDB collection structure:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Relative path (e.g., `dotcodex/skills/uv-python/SKILL.md`) |
| `document` | string | Searchable text (name + intent + tags) |
| `embedding` | vector | Auto-generated from document field |
| `metadata.name` | string | Skill name |
| `metadata.tags` | string | Comma-separated tags |
| `metadata.full_content` | string | Complete SKILL.md content |

## Fallback Behavior

If ChromaDB is unavailable, the server returns an error with grep fallback instructions:

```
Error: ChromaDB collection not available.
Fallback: Use grep to search skills manually:
  grep -r -l 'keyword' ~/.codex/skills/*/SKILL.md
```

## Dependencies

- `chromadb>=0.4.0` - Vector database
- `mcp>=0.1.0` - Model Context Protocol
- `pyyaml>=6.0` - YAML parsing
- `anyio>=4.0.0` - Async support

## Future Enhancements

- **Better Embeddings**: Upgrade to OpenAI/Cohere for improved accuracy
- **Hybrid Search**: Combine vector search with BM25 keyword matching
- **Caching**: Add query result caching
- **Metrics**: Track search quality and usage patterns
