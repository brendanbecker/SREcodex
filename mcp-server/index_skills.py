#!/usr/bin/env python3
"""
Skill Indexing Pipeline for SREcodex

Parses YAML frontmatter from SKILL.md files, embeds intent fields,
and stores full documents in ChromaDB for semantic search.

Key Design Decisions:
- Parent-Child Indexing: Embed only the intent field, retrieve full document
- This avoids RAG chunking that breaks executable code
- Idempotent: Safe to re-run (uses upsert)

Usage:
    python index_skills.py                    # Index from default path
    python index_skills.py --skills-dir PATH  # Index from custom path
    python index_skills.py --chroma-path PATH # Use custom ChromaDB path
"""

import argparse
import os
import sys
from pathlib import Path

import yaml
import chromadb
from chromadb.utils import embedding_functions


# Default configuration
DEFAULT_SKILLS_DIR = "../dotcodex/skills"
DEFAULT_CHROMA_PATH = "./chroma_data"
COLLECTION_NAME = "srecodex_skills"


def parse_skill_file(filepath: str) -> dict | None:
    """
    Extract YAML frontmatter and full content from SKILL.md file.

    Returns dict with id, name, tags, intent, risk_level, full_content
    or None if file doesn't have valid frontmatter.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Could not read {filepath}: {e}")
        return None

    # Check for YAML frontmatter (between --- markers)
    if not content.startswith('---'):
        print(f"SKIP: No frontmatter in {filepath}")
        return None

    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"SKIP: Invalid frontmatter format in {filepath}")
        return None

    try:
        metadata = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        print(f"SKIP: YAML parse error in {filepath}: {e}")
        return None

    if not metadata:
        print(f"SKIP: Empty frontmatter in {filepath}")
        return None

    # Extract fields with defaults
    return {
        "id": filepath,
        "name": metadata.get("name", ""),
        "tags": metadata.get("tags", []),
        "intent": metadata.get("intent", ""),
        "risk_level": metadata.get("risk_level", "unknown"),
        "version": metadata.get("version", ""),
        "full_content": content  # Store complete file for retrieval
    }


def build_searchable_text(skill: dict) -> str:
    """
    Combine metadata fields into single searchable string.

    This is what gets embedded - the intent field plus supporting context.
    The full skill content is stored separately for retrieval.
    """
    parts = [
        skill["name"],
        skill["intent"],
        " ".join(skill["tags"])
    ]
    return " | ".join(filter(None, parts))


def find_skill_files(skills_dir: str) -> list[str]:
    """Find all SKILL.md files recursively in the skills directory."""
    skill_files = []
    skills_path = Path(skills_dir).resolve()

    if not skills_path.exists():
        print(f"ERROR: Skills directory not found: {skills_path}")
        return []

    for root, dirs, files in os.walk(skills_path):
        for file in files:
            if file == "SKILL.md":
                skill_files.append(os.path.join(root, file))

    return skill_files


def index_skills(skills_dir: str, chroma_path: str) -> int:
    """
    Main indexing function.

    Returns the number of skills successfully indexed.
    """
    print(f"Indexing skills from: {os.path.abspath(skills_dir)}")
    print(f"ChromaDB path: {os.path.abspath(chroma_path)}")

    # Find all SKILL.md files
    skill_files = find_skill_files(skills_dir)
    print(f"Found {len(skill_files)} SKILL.md files")

    if not skill_files:
        print("No skill files found. Nothing to index.")
        return 0

    # Parse all skill files
    skills = []
    for filepath in skill_files:
        skill = parse_skill_file(filepath)
        if skill:
            skills.append(skill)

    print(f"Parsed {len(skills)} valid skills (with frontmatter)")

    if not skills:
        print("No valid skills to index.")
        return 0

    # Initialize ChromaDB
    print("Initializing ChromaDB...")
    client = chromadb.PersistentClient(path=chroma_path)

    # Use default embedding function (all-MiniLM-L6-v2)
    # Can be upgraded to OpenAI/Cohere embeddings for better accuracy
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()

    # Get or create collection
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn,
        metadata={"description": "SREcodex skills for semantic search"}
    )

    # Prepare batch upsert data
    ids = []
    documents = []
    metadatas = []

    for skill in skills:
        # Use relative path from skills dir as ID for cleaner display
        rel_path = os.path.relpath(skill["id"], os.path.dirname(skills_dir))
        ids.append(rel_path)

        # This text gets embedded for search
        documents.append(build_searchable_text(skill))

        # Store full content and metadata for retrieval
        metadatas.append({
            "name": skill["name"],
            "tags": ",".join(skill["tags"]) if skill["tags"] else "",
            "risk_level": skill["risk_level"],
            "version": skill["version"],
            "full_content": skill["full_content"]  # Complete skill file
        })

    # Upsert to collection (safe to re-run)
    print("Upserting to ChromaDB...")
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print(f"Successfully indexed {len(skills)} skills to ChromaDB")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Total documents in collection: {collection.count()}")

    # Show indexed skills
    print("\nIndexed skills:")
    for skill in skills:
        print(f"  - {skill['name']}")

    return len(skills)


def main():
    parser = argparse.ArgumentParser(
        description="Index SREcodex skills for semantic search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python index_skills.py
    python index_skills.py --skills-dir /path/to/skills
    python index_skills.py --chroma-path /custom/chroma/path
        """
    )
    parser.add_argument(
        "--skills-dir",
        default=DEFAULT_SKILLS_DIR,
        help=f"Path to skills directory (default: {DEFAULT_SKILLS_DIR})"
    )
    parser.add_argument(
        "--chroma-path",
        default=DEFAULT_CHROMA_PATH,
        help=f"Path to ChromaDB data directory (default: {DEFAULT_CHROMA_PATH})"
    )

    args = parser.parse_args()

    count = index_skills(args.skills_dir, args.chroma_path)

    if count == 0:
        sys.exit(1)

    print("\nIndexing complete!")


if __name__ == "__main__":
    main()
