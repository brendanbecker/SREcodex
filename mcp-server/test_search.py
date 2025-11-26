#!/usr/bin/env python3
"""Quick test script for semantic search."""

import chromadb
from chromadb.utils import embedding_functions

def main():
    client = chromadb.PersistentClient(path='./chroma_data')
    ef = embedding_functions.DefaultEmbeddingFunction()

    try:
        coll = client.get_collection('srecodex_skills', embedding_function=ef)
    except ValueError:
        print("Error: Collection not found. Run 'make index' first.")
        return 1

    print(f"Skills indexed: {coll.count()}")
    print()

    queries = [
        'parse large documents',
        'run python tests',
        'find and load skills'
    ]

    for q in queries:
        r = coll.query(query_texts=[q], n_results=2)
        print(f'Query: "{q}"')
        for i, (id, meta, dist) in enumerate(zip(
            r['ids'][0],
            r['metadatas'][0],
            r['distances'][0]
        )):
            relevance = 1 - dist
            print(f"  {i+1}. {meta['name']} (relevance: {relevance:.2f})")
        print()

    return 0

if __name__ == "__main__":
    exit(main())
