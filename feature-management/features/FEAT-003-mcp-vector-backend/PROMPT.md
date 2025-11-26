# FEAT-003: MCP & Vector Search Backend

## Objective

Build a semantic search backend for the Librarian skill using ChromaDB for vector storage and an MCP server to expose the search capability to Codex.

## Background

### The RAG Problem with Code

Standard RAG relies on **chunking**—splitting documents into small segments (~500 tokens).

| Content Type | Chunking Effect |
|--------------|-----------------|
| Prose | Works fine (retrieve a paragraph) |
| Code/Skills | **Catastrophic** (20 lines from a 50-line script = broken) |

### The Solution: Parent-Child Indexing

- **Vectorize**: Only the *intent* (description, tags, header metadata)
- **Retrieve**: The *full document* (complete SKILL.md)

This gives semantic search benefits without breaking executable code.

### Architecture Overview

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

## Implementation Plan

### Section 1: ChromaDB Setup

**Location**: `mcp-server/docker-compose.yml` or local Python

**Option A: Docker Container** (Recommended for isolation)

```yaml
# mcp-server/docker-compose.yml
version: '3.8'
services:
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    volumes:
      - chroma_data:/chroma/chroma
    environment:
      - ANONYMIZED_TELEMETRY=false

volumes:
  chroma_data:
```

**Option B: Local Python Process**

```python
# Embedded in mcp_server.py
import chromadb
client = chromadb.PersistentClient(path="./chroma_data")
```

**Data Model**:

| Field     | Type   | Description                             |
|-----------|--------|-----------------------------------------|
| id        | string | File path (e.g., skills/k8s/restart.md) |
| embedding | vector | Vector representation of intent field   |
| metadata  | JSON   | {tags: [], risk_level: "", name: ""}    |
| document  | string | Full raw text of SKILL.md               |

### Section 2: Ingestion Pipeline

**File**: `mcp-server/index_skills.py`

**Purpose**: Scan skills repository, parse YAML frontmatter, embed intents, upsert to ChromaDB.

**Logic**:

```python
#!/usr/bin/env python3
"""
Skill Indexing Pipeline for SREcodex
Parses YAML frontmatter, embeds intent, stores full documents in ChromaDB.
"""

import os
import yaml
import chromadb
from chromadb.utils import embedding_functions

# Configuration
SKILLS_DIR = "../dotcodex/skills"
CHROMA_PATH = "./chroma_data"
COLLECTION_NAME = "srecodex_skills"

def parse_skill_file(filepath: str) -> dict | None:
    """Extract YAML frontmatter and full content from SKILL.md"""
    with open(filepath, 'r') as f:
        content = f.read()

    # Check for YAML frontmatter (between --- markers)
    if not content.startswith('---'):
        print(f"SKIP: No frontmatter in {filepath}")
        return None

    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"SKIP: Invalid frontmatter in {filepath}")
        return None

    try:
        metadata = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        print(f"SKIP: YAML parse error in {filepath}: {e}")
        return None

    return {
        "id": filepath,
        "name": metadata.get("name", ""),
        "tags": metadata.get("tags", []),
        "intent": metadata.get("intent", ""),
        "risk_level": metadata.get("risk_level", "unknown"),
        "full_content": content  # Store complete file
    }

def build_searchable_text(skill: dict) -> str:
    """Combine metadata fields into single searchable string"""
    parts = [
        skill["name"],
        skill["intent"],
        " ".join(skill["tags"])
    ]
    return " | ".join(filter(None, parts))

def index_skills():
    """Main indexing function"""
    # Initialize ChromaDB
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Use default embedding function (or configure OpenAI/other)
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()

    # Get or create collection
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn
    )

    # Find all SKILL.md files
    skills = []
    for root, dirs, files in os.walk(SKILLS_DIR):
        for file in files:
            if file == "SKILL.md":
                filepath = os.path.join(root, file)
                skill = parse_skill_file(filepath)
                if skill:
                    skills.append(skill)

    print(f"Found {len(skills)} valid skills")

    # Prepare batch upsert
    ids = []
    documents = []
    metadatas = []

    for skill in skills:
        ids.append(skill["id"])
        documents.append(build_searchable_text(skill))  # This gets embedded
        metadatas.append({
            "name": skill["name"],
            "tags": ",".join(skill["tags"]),
            "risk_level": skill["risk_level"],
            "full_content": skill["full_content"]  # Store for retrieval
        })

    # Upsert to collection
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print(f"Indexed {len(skills)} skills to ChromaDB")

if __name__ == "__main__":
    index_skills()
```

**Trigger**: Run on CI/CD deploy or manual refresh:

```bash
cd mcp-server && python index_skills.py
```

### Section 3: MCP Server

**File**: `mcp-server/mcp_server.py`

**Purpose**: Bridge between Codex and ChromaDB. Expose search_skills() tool.

**Implementation**:

```python
#!/usr/bin/env python3
"""
MCP Server for SREcodex Skill Discovery
Exposes search_skills() tool for semantic skill lookup.
"""

from mcp.server import Server
from mcp.types import Tool, TextContent
import chromadb
from chromadb.utils import embedding_functions

# Configuration
CHROMA_PATH = "./chroma_data"
COLLECTION_NAME = "srecodex_skills"
DEFAULT_RESULTS = 3

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
embedding_fn = embedding_functions.DefaultEmbeddingFunction()
collection = chroma_client.get_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_fn
)

# Initialize MCP server
server = Server("srecodex-skills")

@server.list_tools()
async def list_tools():
    """Expose available tools to Codex"""
    return [
        Tool(
            name="search_skills",
            description="Search the SREcodex skills library using natural language. Returns full skill definitions for the most relevant matches.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language description of the capability needed (e.g., 'fix redis timeout issues')"
                    },
                    "n_results": {
                        "type": "integer",
                        "description": "Number of results to return (default: 3, max: 5)",
                        "default": 3
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool calls from Codex"""
    if name != "search_skills":
        raise ValueError(f"Unknown tool: {name}")

    query = arguments["query"]
    n_results = min(arguments.get("n_results", DEFAULT_RESULTS), 5)

    # Query ChromaDB
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["metadatas", "distances"]
    )

    # Format response
    output = []
    for i, (id, metadata, distance) in enumerate(zip(
        results["ids"][0],
        results["metadatas"][0],
        results["distances"][0]
    )):
        relevance = 1 - distance  # Convert distance to similarity
        output.append(f"""
## Match {i+1}: {metadata['name']} (relevance: {relevance:.2f})
**Path**: {id}
**Tags**: {metadata['tags']}

### Full Skill Content:
{metadata['full_content']}
---
""")

    return [TextContent(
        type="text",
        text="\n".join(output) if output else "No matching skills found."
    )]

if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream)

    asyncio.run(main())
```

### Section 4: Codex Configuration

**File**: `dotcodex/config.toml`

Add MCP server configuration:

```toml
[mcp]
servers = [
    { name = "srecodex-skills", command = "python", args = ["mcp-server/mcp_server.py"] }
]
```

Or if using Docker:

```toml
[mcp]
servers = [
    { name = "srecodex-skills", command = "docker", args = ["exec", "mcp-server", "python", "mcp_server.py"] }
]
```

### Section 5: Update Librarian Skill

**File**: `dotcodex/skills/core/librarian/SKILL.md`

Update the search method to use MCP tool:

```markdown
## Search Method

**Primary (Semantic)**: Use the `search_skills` MCP tool
```
search_skills(query="natural language description of need")
```

**Fallback (Keyword)**: If MCP unavailable, use grep:
```bash
grep -r -l "keyword" dotcodex/skills/*/SKILL.md
```
```

### Section 6: Requirements & Dependencies

**File**: `mcp-server/requirements.txt`

```
chromadb>=0.4.0
mcp>=0.1.0
pyyaml>=6.0
```

**File**: `mcp-server/README.md`

```markdown
# SREcodex MCP Server

Semantic skill discovery backend using ChromaDB.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Index skills:
   ```bash
   python index_skills.py
   ```

3. Start server (usually done automatically by Codex):
   ```bash
   python mcp_server.py
   ```

## Docker Setup (Alternative)

```bash
docker-compose up -d
```

## Re-indexing

Run after adding/modifying skills:

```bash
python index_skills.py
```
```

## Deliverables

| File | Purpose |
|------|---------|
| `mcp-server/docker-compose.yml` | ChromaDB container setup |
| `mcp-server/index_skills.py` | Ingestion pipeline |
| `mcp-server/mcp_server.py` | MCP server with search_skills tool |
| `mcp-server/requirements.txt` | Python dependencies |
| `mcp-server/README.md` | Setup documentation |
| `dotcodex/config.toml` | MCP server configuration |
| Updated Librarian SKILL.md | Use MCP tool for search |

## Acceptance Criteria

- [ ] ChromaDB running locally (Docker or embedded)
- [ ] `index_skills.py` successfully parses YAML frontmatter from all FEAT-001 compliant skills
- [ ] `index_skills.py` stores full document content (not chunks)
- [ ] `mcp_server.py` exposes `search_skills()` tool via MCP protocol
- [ ] Codex config.toml updated with MCP server reference
- [ ] End-to-end test: Query "redis timeout" returns redis-related skill with full content
- [ ] Librarian skill updated to use MCP tool as primary search method
- [ ] Fallback to grep works when MCP unavailable

## Testing Plan

### Unit Tests

```python
# test_index_skills.py
def test_parse_skill_file_valid():
    """Should extract frontmatter and full content"""

def test_parse_skill_file_no_frontmatter():
    """Should return None for files without ---"""

def test_build_searchable_text():
    """Should combine name, intent, tags"""
```

### Integration Tests

```python
# test_mcp_server.py
async def test_search_skills_returns_results():
    """Query should return matching skills"""

async def test_search_skills_includes_full_content():
    """Results should include complete SKILL.md content"""

async def test_search_skills_relevance_ordering():
    """Results should be ordered by semantic similarity"""
```

### Manual Verification

1. Index a set of test skills
2. Query with natural language: "help me debug kubernetes pod crashes"
3. Verify returned skill is relevant and complete
4. Verify skill can be executed without errors

## Future Enhancements

- **Embedding Model**: Upgrade from default to OpenAI/Cohere embeddings for better accuracy
- **Hybrid Search**: Combine vector search with BM25 keyword matching
- **Caching**: Add query result caching for frequently used searches
- **Metrics**: Track search quality and usage patterns
