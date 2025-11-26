# MCP Server Setup Guide

This guide walks you through setting up the SREcodex semantic skill search server for use with OpenAI Codex.

## Prerequisites

1. **Python 3.11+** with uv installed
2. **Skills indexed** in ChromaDB

## Step 1: Initialize the Server

```bash
cd mcp-server
make setup    # Install dependencies
make index    # Index skills to ChromaDB
make test     # Verify it works
```

You should see output like:
```
Skills indexed: 6

Query: "parse large documents"
  1. Document Parser (relevance: 0.47)
  ...
```

## Step 2: Configure Codex

Add the MCP server to your Codex configuration.

### Option A: Project-level config (recommended)

Create or edit `CODEX.md` in your project root:

```markdown
## MCP Servers

```json
{
  "mcpServers": {
    "srecodex-skills": {
      "command": "uv",
      "args": ["run", "--directory", "/home/becker/projects/SREcodex/mcp-server", "python", "mcp_server.py"]
    }
  }
}
```
```

### Option B: Global config

Edit `~/.codex/config.toml`:

```toml
[mcp.servers.srecodex-skills]
command = "uv"
args = ["run", "--directory", "/home/becker/projects/SREcodex/mcp-server", "python", "mcp_server.py"]
```

### Option C: JSON config

Edit `~/.codex/config.json`:

```json
{
  "mcpServers": {
    "srecodex-skills": {
      "command": "uv",
      "args": ["run", "--directory", "/home/becker/projects/SREcodex/mcp-server", "python", "mcp_server.py"]
    }
  }
}
```

> **Note**: Replace `/home/becker/projects/SREcodex/mcp-server` with the absolute path to your mcp-server directory.

## Step 3: Verify Integration

Start Codex and run:

```
search_skills("help me parse large documents")
```

You should see the Document Parser skill returned with full content.

## Troubleshooting

### "Collection not found"

The skills haven't been indexed yet:
```bash
cd mcp-server && make index
```

### "ChromaDB not available"

Dependencies not installed:
```bash
cd mcp-server && make setup
```

### Server not starting

Test manually:
```bash
cd mcp-server && make serve
```

Should output:
```
Connected to ChromaDB collection: srecodex_skills
Collection contains 6 documents
```

### Tool not appearing in Codex

1. Check the path in your config is absolute
2. Restart Codex after config changes
3. Verify uv is in your PATH

## Re-indexing Skills

After adding or modifying skills in `dotcodex/skills/`:

```bash
cd mcp-server && make reindex
```

## Interactive Testing

To test the MCP server interactively without Codex:

```bash
cd mcp-server && make inspect
```

This opens a web UI where you can call `search_skills()` directly.

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Codex     │────►│ MCP Server  │────►│  ChromaDB   │
│  (Client)   │◄────│  (Bridge)   │◄────│  (Vectors)  │
└─────────────┘     └─────────────┘     └─────────────┘
                          │
                   search_skills(query)
                          │
                   ┌──────▼──────┐
                   │ Full SKILL.md│
                   │  (Retrieved) │
                   └─────────────┘
```

The server embeds only the skill's `intent` field but returns the **full SKILL.md content**, avoiding the RAG chunking problem where partial code breaks functionality.
