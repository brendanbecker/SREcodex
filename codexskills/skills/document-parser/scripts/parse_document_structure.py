#!/usr/bin/env python3
"""
Parse markdown document structure into hierarchical sections with token counts.

Extracts headers, builds section tree, counts tokens per section.
Outputs machine-readable JSON and human-readable section map.

Usage:
    python3 parse_document_structure.py <file.md> [--output structure.json] [--map section_map.md]
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional


def count_tokens(text: str) -> int:
    """
    Count tokens in text using tiktoken (OpenAI's tokenizer).
    Falls back to word-based estimation if tiktoken unavailable.

    Args:
        text: Input text to count tokens

    Returns:
        Estimated token count
    """
    try:
        import tiktoken
        encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 encoding
        return len(encoding.encode(text))
    except ImportError:
        # Fallback: Approximate as 0.75 * word count
        words = len(text.split())
        return int(words * 0.75)


class Section:
    """Represents a document section with hierarchical structure."""

    def __init__(self, title: str, level: int, line_number: int, content: str = ""):
        self.title = title.strip()
        self.level = level
        self.line_number = line_number
        self.content = content
        self.children: List[Section] = []
        self.parent: Optional[Section] = None

    def add_child(self, child: 'Section'):
        """Add a child section."""
        child.parent = self
        self.children.append(child)

    def get_full_content(self) -> str:
        """Get section content including all children."""
        parts = [self.content]
        for child in self.children:
            parts.append(child.get_full_content())
        return "\n".join(parts)

    def to_dict(self, include_content: bool = False) -> Dict[str, Any]:
        """Convert section to dictionary for JSON serialization."""
        token_count = count_tokens(self.content)

        result = {
            "id": self.get_id(),
            "title": self.title,
            "level": self.level,
            "line_number": self.line_number,
            "token_count": token_count,
            "children": [child.to_dict(include_content) for child in self.children]
        }

        if include_content:
            result["content"] = self.content

        return result

    def get_id(self) -> str:
        """Generate unique ID based on position in tree."""
        if self.parent is None:
            return f"section-{self.line_number}"

        sibling_index = self.parent.children.index(self) + 1
        parent_id = self.parent.get_id()
        return f"{parent_id}.{sibling_index}"

    def get_breadcrumb(self) -> str:
        """Get full section path (e.g., 'Chapter 1 > Section 1.1 > Subsection')."""
        if self.parent is None:
            return self.title
        return f"{self.parent.get_breadcrumb()} > {self.title}"


def parse_markdown_structure(content: str) -> List[Section]:
    """
    Parse markdown content and extract hierarchical section structure.

    Args:
        content: Markdown content as string

    Returns:
        List of top-level sections (each may have children)
    """
    lines = content.split('\n')
    sections: List[Section] = []
    current_section: Optional[Section] = None
    section_stack: List[Section] = []
    current_content_lines: List[str] = []

    # Regex for markdown headers (# through ######)
    header_pattern = re.compile(r'^(#{1,6})\s+(.+)$')

    for line_num, line in enumerate(lines, start=1):
        header_match = header_pattern.match(line)

        if header_match:
            # Save content from previous section
            if current_section is not None:
                current_section.content = '\n'.join(current_content_lines).strip()
                current_content_lines = []

            # Extract header info
            header_chars = header_match.group(1)
            level = len(header_chars)
            title = header_match.group(2).strip()

            # Create new section
            new_section = Section(title, level, line_num)

            # Find parent section
            while section_stack and section_stack[-1].level >= level:
                section_stack.pop()

            if section_stack:
                # Add as child to parent
                section_stack[-1].add_child(new_section)
            else:
                # Top-level section
                sections.append(new_section)

            section_stack.append(new_section)
            current_section = new_section

        else:
            # Accumulate content for current section
            if current_section is not None:
                current_content_lines.append(line)

    # Save content from final section
    if current_section is not None:
        current_section.content = '\n'.join(current_content_lines).strip()

    return sections


def generate_section_map(sections: List[Section], indent_level: int = 0) -> str:
    """
    Generate human-readable markdown section map.

    Args:
        sections: List of sections to include
        indent_level: Current indentation level

    Returns:
        Formatted markdown outline
    """
    lines = []
    indent = "  " * indent_level

    for section in sections:
        token_count = count_tokens(section.content)
        lines.append(f"{indent}- {section.title} ({token_count} tokens)")

        if section.children:
            child_map = generate_section_map(section.children, indent_level + 1)
            lines.append(child_map)

    return '\n'.join(lines)


def calculate_statistics(sections: List[Section]) -> Dict[str, Any]:
    """Calculate document statistics."""

    def count_sections(secs: List[Section]) -> int:
        count = len(secs)
        for sec in secs:
            count += count_sections(sec.children)
        return count

    def sum_tokens(secs: List[Section]) -> int:
        total = 0
        for sec in secs:
            total += count_tokens(sec.content)
            total += sum_tokens(sec.children)
        return total

    def collect_token_counts(secs: List[Section]) -> List[int]:
        counts = []
        for sec in secs:
            counts.append(count_tokens(sec.content))
            counts.extend(collect_token_counts(sec.children))
        return counts

    total_sections = count_sections(sections)
    total_tokens = sum_tokens(sections)
    token_counts = collect_token_counts(sections)

    return {
        "total_sections": total_sections,
        "total_tokens": total_tokens,
        "avg_tokens_per_section": total_tokens / total_sections if total_sections > 0 else 0,
        "min_tokens": min(token_counts) if token_counts else 0,
        "max_tokens": max(token_counts) if token_counts else 0
    }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Parse markdown document structure and extract hierarchical sections"
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Input markdown file to parse"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default="structure.json",
        help="Output JSON file for structure (default: structure.json)"
    )
    parser.add_argument(
        "--map",
        type=Path,
        default="section_map.md",
        help="Output markdown file for section map (default: section_map.md)"
    )
    parser.add_argument(
        "--include-content",
        action="store_true",
        help="Include full section content in JSON output"
    )

    args = parser.parse_args()

    # Validate input file
    if not args.input_file.exists():
        print(f"Error: Input file not found: {args.input_file}", file=sys.stderr)
        sys.exit(1)

    # Read markdown content
    try:
        content = args.input_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse structure
    print(f"Parsing {args.input_file}...")
    sections = parse_markdown_structure(content)

    if not sections:
        print("Warning: No sections found in document", file=sys.stderr)
        sys.exit(0)

    # Calculate statistics
    stats = calculate_statistics(sections)

    print(f"Found {stats['total_sections']} sections")
    print(f"Total tokens: {stats['total_tokens']}")
    print(f"Average tokens per section: {stats['avg_tokens_per_section']:.1f}")
    print(f"Token range: {stats['min_tokens']} - {stats['max_tokens']}")

    # Generate JSON output
    output_data = {
        "source_file": str(args.input_file),
        "sections": [s.to_dict(include_content=args.include_content) for s in sections],
        "statistics": stats
    }

    try:
        args.output.write_text(json.dumps(output_data, indent=2), encoding='utf-8')
        print(f"Wrote structure to {args.output}")
    except Exception as e:
        print(f"Error writing JSON output: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate section map
    section_map = f"# Document Structure\n\n"
    section_map += f"Source: {args.input_file}\n\n"
    section_map += generate_section_map(sections)

    try:
        args.map.write_text(section_map, encoding='utf-8')
        print(f"Wrote section map to {args.map}")
    except Exception as e:
        print(f"Error writing section map: {e}", file=sys.stderr)
        sys.exit(1)

    # Identify sections outside target range
    outside_range = []

    def check_range(secs: List[Section]):
        for sec in secs:
            tokens = count_tokens(sec.content)
            if tokens < 400 or tokens > 900:
                outside_range.append((sec.title, tokens, sec.get_breadcrumb()))
            check_range(sec.children)

    check_range(sections)

    if outside_range:
        print(f"\nSections outside 400-900 token target range:")
        for title, tokens, breadcrumb in outside_range[:10]:  # Show first 10
            print(f"  - {title}: {tokens} tokens ({breadcrumb})")
        if len(outside_range) > 10:
            print(f"  ... and {len(outside_range) - 10} more")
    else:
        print("\nAll sections within 400-900 token target range ✓")


if __name__ == "__main__":
    main()
