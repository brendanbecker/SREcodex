#!/usr/bin/env python3
"""
Extract metadata from markdown documents.

Extracts tables, code blocks, benchmarks (metrics/percentages), and key terms
(techniques, models, acronyms) from markdown content.

Usage:
    python3 extract_metadata.py <file.md> [--output metadata.json]
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Set
from collections import defaultdict


def extract_tables(content: str) -> List[Dict[str, Any]]:
    """
    Extract markdown tables from content.

    Args:
        content: Markdown content

    Returns:
        List of table dictionaries with headers and rows
    """
    tables = []
    lines = content.split('\n')
    table_id = 1
    current_section = "Document"

    # Track current section for context
    section_pattern = re.compile(r'^(#{1,6})\s+(.+)$')

    i = 0
    while i < len(lines):
        line = lines[i]

        # Update current section
        section_match = section_pattern.match(line)
        if section_match:
            current_section = section_match.group(2).strip()
            i += 1
            continue

        # Check if this line starts a table (has | characters)
        if '|' in line and line.strip().startswith('|'):
            # Extract table
            table_lines = [line]
            i += 1

            # Collect all lines in the table
            while i < len(lines) and '|' in lines[i]:
                table_lines.append(lines[i])
                i += 1

            # Parse table
            if len(table_lines) >= 2:  # Need at least header + separator
                # Parse header
                header_line = table_lines[0]
                headers = [cell.strip() for cell in header_line.split('|')[1:-1]]

                # Skip separator line (if present)
                start_idx = 2 if len(table_lines) > 2 and re.match(r'\|[\s\-:|]+\|', table_lines[1]) else 1

                # Parse rows
                rows = []
                for row_line in table_lines[start_idx:]:
                    if '|' in row_line:
                        cells = [cell.strip() for cell in row_line.split('|')[1:-1]]
                        if cells and any(cells):  # Skip empty rows
                            rows.append(cells)

                if headers and rows:
                    tables.append({
                        "id": f"table-{table_id}",
                        "section": current_section,
                        "headers": headers,
                        "rows": rows,
                        "row_count": len(rows),
                        "column_count": len(headers)
                    })
                    table_id += 1
        else:
            i += 1

    return tables


def extract_code_blocks(content: str) -> List[Dict[str, Any]]:
    """
    Extract code blocks from markdown.

    Args:
        content: Markdown content

    Returns:
        List of code block dictionaries
    """
    code_blocks = []
    lines = content.split('\n')
    code_id = 1
    current_section = "Document"

    # Track current section
    section_pattern = re.compile(r'^(#{1,6})\s+(.+)$')

    i = 0
    while i < len(lines):
        line = lines[i]

        # Update current section
        section_match = section_pattern.match(line)
        if section_match:
            current_section = section_match.group(2).strip()
            i += 1
            continue

        # Check for code block start (```)
        if line.strip().startswith('```'):
            # Extract language tag
            language = line.strip()[3:].strip() or "text"

            # Collect code content
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1

            if code_lines:
                code_blocks.append({
                    "id": f"code-{code_id}",
                    "section": current_section,
                    "language": language,
                    "content": '\n'.join(code_lines),
                    "line_count": len(code_lines)
                })
                code_id += 1

            i += 1  # Skip closing ```
        else:
            i += 1

    return code_blocks


def extract_benchmarks(content: str) -> List[Dict[str, Any]]:
    """
    Extract benchmarks (percentages, metrics, performance numbers).

    Args:
        content: Markdown content

    Returns:
        List of benchmark dictionaries
    """
    benchmarks = []
    current_section = "Document"

    # Track current section
    section_pattern = re.compile(r'^(#{1,6})\s+(.+)$')

    # Patterns for benchmarks
    # Percentages: 95.2%, 0.94
    percentage_pattern = re.compile(r'(\d+\.?\d*)\s*%')
    # Decimal metrics: 0.95, F1: 0.94
    decimal_pattern = re.compile(r'(\w+):\s*(\d\.\d+)')
    # Integer metrics: 1000 iterations, 500ms
    integer_pattern = re.compile(r'(\d+)\s*(ms|tokens|seconds|iterations|examples|samples)')

    lines = content.split('\n')

    for line in lines:
        # Update section context
        section_match = section_pattern.match(line)
        if section_match:
            current_section = section_match.group(2).strip()
            continue

        # Extract percentages
        for match in percentage_pattern.finditer(line):
            value = match.group(1)
            context = line.strip()
            benchmarks.append({
                "metric": "Percentage",
                "value": f"{value}%",
                "context": context,
                "section": current_section
            })

        # Extract decimal metrics
        for match in decimal_pattern.finditer(line):
            metric_name = match.group(1)
            value = match.group(2)
            context = line.strip()
            benchmarks.append({
                "metric": metric_name,
                "value": value,
                "context": context,
                "section": current_section
            })

        # Extract integer metrics
        for match in integer_pattern.finditer(line):
            value = match.group(1)
            unit = match.group(2)
            context = line.strip()
            benchmarks.append({
                "metric": unit.capitalize(),
                "value": value,
                "context": context,
                "section": current_section
            })

    return benchmarks


def extract_key_terms(content: str) -> Dict[str, List[str]]:
    """
    Extract key terms: techniques, models, acronyms.

    Args:
        content: Markdown content

    Returns:
        Dictionary with categorized key terms
    """
    # Common ML/AI techniques
    technique_patterns = [
        r'\b(RAG|Retrieval[\s-]Augmented[\s-]Generation)\b',
        r'\b(Fine[\s-]tuning|Finetuning)\b',
        r'\b(Few[\s-]shot|Zero[\s-]shot|One[\s-]shot)\s+learning\b',
        r'\b(Transfer\s+learning)\b',
        r'\b(Reinforcement\s+learning|RLHF)\b',
        r'\b(Supervised|Unsupervised|Self[\s-]supervised)\s+learning\b',
        r'\b(Prompt\s+engineering)\b',
        r'\b(Chain[\s-]of[\s-]thought|CoT)\b',
        r'\b(Embedding|Embeddings)\b',
        r'\b(Attention\s+mechanism)\b',
        r'\b(Transformer)\b',
    ]

    # Common models
    model_patterns = [
        r'\b(GPT[\s-]?[0-9]+(?:\.[0-9]+)?)\b',
        r'\b(Claude(?:[\s-][0-9]+)?)\b',
        r'\b(BERT|RoBERTa|ALBERT)\b',
        r'\b(T5|BART)\b',
        r'\b(Llama[\s-]?[0-9]*)\b',
        r'\b(PaLM[\s-]?[0-9]*)\b',
        r'\b(Mistral[\s-]?[0-9]*)\b',
        r'\b(Gemini)\b',
    ]

    # Acronyms (all caps, 2-6 letters)
    acronym_pattern = r'\b([A-Z]{2,6})\b'

    # Extract matches
    techniques: Set[str] = set()
    models: Set[str] = set()
    acronyms: Set[str] = set()

    # Extract techniques
    for pattern in technique_patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            techniques.add(match.group(1))

    # Extract models
    for pattern in model_patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            models.add(match.group(1))

    # Extract acronyms
    acronym_matches = re.finditer(acronym_pattern, content)
    common_words = {'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HIS', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO', 'WHO', 'BOY', 'DID', 'ITS', 'LET', 'PUT', 'SAY', 'SHE', 'TOO', 'USE'}

    for match in acronym_matches:
        acronym = match.group(1)
        # Filter out common words and markdown headers
        if acronym not in common_words and acronym not in ['MD', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6']:
            acronyms.add(acronym)

    return {
        "techniques": sorted(list(techniques)),
        "models": sorted(list(models)),
        "acronyms": sorted(list(acronyms))
    }


def generate_statistics(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Generate summary statistics for extracted metadata."""
    stats = {
        "total_tables": len(metadata.get("tables", [])),
        "total_code_blocks": len(metadata.get("code_blocks", [])),
        "total_benchmarks": len(metadata.get("benchmarks", [])),
        "total_techniques": len(metadata.get("key_terms", {}).get("techniques", [])),
        "total_models": len(metadata.get("key_terms", {}).get("models", [])),
        "total_acronyms": len(metadata.get("key_terms", {}).get("acronyms", []))
    }

    # Language distribution in code blocks
    if metadata.get("code_blocks"):
        lang_counts = defaultdict(int)
        for block in metadata["code_blocks"]:
            lang_counts[block["language"]] += 1
        stats["code_languages"] = dict(lang_counts)

    # Sections with most tables
    if metadata.get("tables"):
        section_counts = defaultdict(int)
        for table in metadata["tables"]:
            section_counts[table["section"]] += 1
        stats["sections_with_tables"] = dict(sorted(section_counts.items(), key=lambda x: x[1], reverse=True)[:5])

    return stats


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Extract metadata (tables, code, benchmarks, terms) from markdown"
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Input markdown file to parse"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default="metadata.json",
        help="Output JSON file for metadata (default: metadata.json)"
    )

    args = parser.parse_args()

    # Validate input
    if not args.input_file.exists():
        print(f"Error: Input file not found: {args.input_file}", file=sys.stderr)
        sys.exit(1)

    # Read content
    try:
        content = args.input_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract metadata
    print(f"Extracting metadata from {args.input_file}...")

    metadata = {
        "source_file": str(args.input_file),
        "tables": extract_tables(content),
        "code_blocks": extract_code_blocks(content),
        "benchmarks": extract_benchmarks(content),
        "key_terms": extract_key_terms(content)
    }

    # Add statistics
    metadata["statistics"] = generate_statistics(metadata)

    # Print summary
    stats = metadata["statistics"]
    print(f"Found {stats['total_tables']} tables")
    print(f"Found {stats['total_code_blocks']} code blocks")
    print(f"Found {stats['total_benchmarks']} benchmarks")
    print(f"Found {stats['total_techniques']} techniques")
    print(f"Found {stats['total_models']} models")
    print(f"Found {stats['total_acronyms']} acronyms")

    if stats.get("code_languages"):
        print(f"\nCode languages: {', '.join(stats['code_languages'].keys())}")

    # Write output
    try:
        args.output.write_text(json.dumps(metadata, indent=2), encoding='utf-8')
        print(f"\nWrote metadata to {args.output}")
    except Exception as e:
        print(f"Error writing output: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
