#!/usr/bin/env python3
"""
MCP Server for SREcodex Skill Discovery

Exposes search_skills() tool for semantic skill lookup via the MCP protocol.
Uses ChromaDB as the vector store backend.

Key Design:
- Returns FULL skill content, not chunks
- Graceful degradation if ChromaDB unavailable
- Configurable result count

Usage:
    python mcp_server.py                     # Start with default settings
    python mcp_server.py --chroma-path PATH  # Custom ChromaDB path

The server communicates via stdio using the MCP protocol.
"""

import argparse
import asyncio
import os
import sys
from typing import Any

try:
    import chromadb
    from chromadb.utils import embedding_functions
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("WARNING: chromadb not installed. Install with: pip install chromadb", file=sys.stderr)

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    from mcp.server.stdio import stdio_server
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("WARNING: mcp not installed. Install with: pip install mcp", file=sys.stderr)


# Configuration
DEFAULT_CHROMA_PATH = "./chroma_data"
COLLECTION_NAME = "srecodex_skills"
DEFAULT_RESULTS = 3
MAX_RESULTS = 5


class SkillSearchServer:
    """MCP Server for semantic skill search."""

    def __init__(self, chroma_path: str):
        self.chroma_path = chroma_path
        self.collection = None
        self.server = None
        self._init_chromadb()
        self._init_mcp_server()

    def _init_chromadb(self):
        """Initialize ChromaDB connection."""
        if not CHROMADB_AVAILABLE:
            print("ChromaDB not available - search will return errors", file=sys.stderr)
            return

        try:
            client = chromadb.PersistentClient(path=self.chroma_path)
            embedding_fn = embedding_functions.DefaultEmbeddingFunction()

            # Try to get existing collection
            self.collection = client.get_collection(
                name=COLLECTION_NAME,
                embedding_function=embedding_fn
            )
            print(f"Connected to ChromaDB collection: {COLLECTION_NAME}", file=sys.stderr)
            print(f"Collection contains {self.collection.count()} documents", file=sys.stderr)
        except Exception as e:
            print(f"WARNING: Could not connect to ChromaDB: {e}", file=sys.stderr)
            print("Run 'python index_skills.py' first to create the collection", file=sys.stderr)
            self.collection = None

    def _init_mcp_server(self):
        """Initialize MCP server and register handlers."""
        if not MCP_AVAILABLE:
            return

        self.server = Server("srecodex-skills")

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Expose available tools to Codex."""
            return [
                Tool(
                    name="search_skills",
                    description=(
                        "Search the SREcodex skills library using natural language. "
                        "Returns full skill definitions for the most relevant matches. "
                        "Use this when you need a capability you don't currently have loaded."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": (
                                    "Natural language description of the capability needed "
                                    "(e.g., 'fix redis timeout issues', 'parse large documents', "
                                    "'run python tests with pytest')"
                                )
                            },
                            "n_results": {
                                "type": "integer",
                                "description": f"Number of results to return (default: {DEFAULT_RESULTS}, max: {MAX_RESULTS})",
                                "default": DEFAULT_RESULTS
                            }
                        },
                        "required": ["query"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Handle tool calls from Codex."""
            if name != "search_skills":
                return [TextContent(
                    type="text",
                    text=f"Unknown tool: {name}"
                )]

            return await self._search_skills(arguments)

    async def _search_skills(self, arguments: dict) -> list[TextContent]:
        """Execute skill search and format results."""
        query = arguments.get("query", "")
        n_results = min(arguments.get("n_results", DEFAULT_RESULTS), MAX_RESULTS)

        if not query:
            return [TextContent(
                type="text",
                text="Error: 'query' parameter is required"
            )]

        if not self.collection:
            return [TextContent(
                type="text",
                text=(
                    "Error: ChromaDB collection not available. "
                    "Run 'python index_skills.py' to index skills first. "
                    "Fallback: Use grep to search skills manually:\n"
                    "  grep -r -l 'keyword' ~/.codex/skills/*/SKILL.md"
                )
            )]

        try:
            # Query ChromaDB
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=["metadatas", "distances"]
            )

            if not results["ids"][0]:
                return [TextContent(
                    type="text",
                    text=f"No skills found matching: '{query}'"
                )]

            # Format response
            output = [f"# Search Results for: '{query}'\n"]

            for i, (id, metadata, distance) in enumerate(zip(
                results["ids"][0],
                results["metadatas"][0],
                results["distances"][0]
            )):
                # Convert distance to similarity score (lower distance = higher similarity)
                # ChromaDB uses L2 distance by default
                relevance = max(0, 1 - (distance / 2))  # Normalize to 0-1 range

                output.append(f"""
## Match {i+1}: {metadata.get('name', 'Unknown')} (relevance: {relevance:.2f})

**Path**: {id}
**Tags**: {metadata.get('tags', 'none')}
**Version**: {metadata.get('version', 'unknown')}

### Full Skill Content:

{metadata.get('full_content', 'Content not available')}

---
""")

            return [TextContent(
                type="text",
                text="\n".join(output)
            )]

        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error searching skills: {e}"
            )]

    async def run(self):
        """Run the MCP server."""
        if not MCP_AVAILABLE:
            print("ERROR: MCP library not available. Install with: pip install mcp", file=sys.stderr)
            sys.exit(1)

        if not self.server:
            print("ERROR: Server not initialized", file=sys.stderr)
            sys.exit(1)

        from mcp.server import InitializationOptions
        from mcp.types import ServerCapabilities

        init_options = InitializationOptions(
            server_name="srecodex-skills",
            server_version="0.1.0",
            capabilities=ServerCapabilities(tools={})
        )

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream, init_options)


def main():
    parser = argparse.ArgumentParser(
        description="MCP Server for SREcodex skill semantic search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This server provides semantic skill discovery via the MCP protocol.

Prerequisites:
    1. Index skills first: python index_skills.py
    2. Configure in ~/.codex/config.toml or CODEX.md

Example config.toml:
    [mcp]
    servers = [
        { name = "srecodex-skills", command = "python", args = ["mcp-server/mcp_server.py"] }
    ]
        """
    )
    parser.add_argument(
        "--chroma-path",
        default=DEFAULT_CHROMA_PATH,
        help=f"Path to ChromaDB data directory (default: {DEFAULT_CHROMA_PATH})"
    )

    args = parser.parse_args()

    # Resolve path relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chroma_path = os.path.join(script_dir, args.chroma_path) if not os.path.isabs(args.chroma_path) else args.chroma_path

    server = SkillSearchServer(chroma_path)
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
