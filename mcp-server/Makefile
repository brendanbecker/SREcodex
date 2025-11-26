# SREcodex MCP Server - Development Commands
#
# Usage:
#   make setup    - Install dependencies via uv
#   make index    - Index skills to ChromaDB
#   make serve    - Run the MCP server
#   make test     - Quick semantic search test
#   make inspect  - Open MCP Inspector web UI
#   make clean    - Remove ChromaDB data
#   make reindex  - Clean and re-index from scratch

.PHONY: setup index serve test inspect clean reindex help

# Default target
help:
	@echo "SREcodex MCP Server Commands:"
	@echo ""
	@echo "  make setup    - Install dependencies via uv"
	@echo "  make index    - Index skills to ChromaDB"
	@echo "  make serve    - Run the MCP server"
	@echo "  make test     - Quick semantic search test"
	@echo "  make inspect  - Open MCP Inspector web UI"
	@echo "  make clean    - Remove ChromaDB data"
	@echo "  make reindex  - Clean and re-index from scratch"
	@echo ""

# Install dependencies
setup:
	@echo "Installing dependencies..."
	uv sync
	@echo "Done. Run 'make index' to index skills."

# Index skills to ChromaDB
index:
	@echo "Indexing skills to ChromaDB..."
	uv run python index_skills.py
	@echo "Done. Run 'make test' to verify."

# Run MCP server (typically started by Codex automatically)
serve:
	@echo "Starting MCP server..."
	uv run python mcp_server.py

# Quick test - search and show results
test:
	@echo "Testing semantic search..."
	@uv run python test_search.py

# Open MCP Inspector for interactive testing
inspect:
	@echo "Opening MCP Inspector..."
	@echo "This will open a web UI to test search_skills() interactively."
	npx @modelcontextprotocol/inspector uv run python mcp_server.py

# Remove ChromaDB data
clean:
	@echo "Removing ChromaDB data..."
	rm -rf chroma_data/
	@echo "Done. Run 'make index' to rebuild."

# Clean and re-index
reindex: clean index
	@echo "Re-indexing complete."
