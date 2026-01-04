# Document Parser Skill - Setup Guide

## Sandbox Configuration for Script Execution

This skill includes Python scripts that need to execute in read-only sandbox mode. To enable script execution from the skills directory, you need to configure Claude Code's sandbox allowlist.

### Quick Setup

Add this configuration to `~/.codex/config.toml`:

```toml
[sandbox]
# Allow execution of scripts from the skills directory
allowed_paths = [
    "~/.codex/skills/document-parser/scripts",
    "~/.local/bin"
]

# Alternative: Use DOTCODEX_DIR variable if configured
# allowed_paths = [
#     "${DOTCODEX_DIR}/skills/document-parser/scripts",
#     "~/.local/bin"
# ]
```

### Full Configuration Example

If you don't have a `[sandbox]` section yet, add this to `~/.codex/config.toml`:

```toml
model = "gpt-5.1-codex"

[notice]
hide_gpt5_1_migration_prompt = true

[sandbox]
# Read-only mode with script execution allowlist
mode = "read-only"
allowed_paths = [
    "~/.codex/skills/*/scripts",      # All skill scripts
    "~/.local/bin",                   # User binaries
    "/usr/bin/python3",               # Python interpreter
    "/usr/local/bin/python3"
]
```

### Verification

After updating your config, restart Claude Code and verify:

```bash
# Test that scripts can be executed
cd ~/.codex/skills/document-parser
python3 scripts/parse_document_structure.py --help
python3 scripts/extract_metadata.py --help
```

## Alternative: Using `dangerouslyDisableSandbox`

**⚠️ Security Warning:** This approach disables sandbox protection and should only be used in trusted environments.

The SKILL.md includes instructions for Codex to use `dangerouslyDisableSandbox: true` when running skill scripts. This is a fallback if sandbox allowlist configuration isn't available.

### Recommended Approach

1. **Preferred:** Configure sandbox allowlist (see above)
2. **Development:** Use `dangerouslyDisableSandbox` flag temporarily
3. **Production:** Always use sandbox with proper allowlist

## Python Dependencies

The scripts require these Python packages:

```bash
# Optional: For faster token counting
pip install tiktoken

# Required for metadata extraction (if using BeautifulSoup)
pip install markdown beautifulsoup4
```

**Note:** Scripts will work without `tiktoken` by falling back to word-based token estimation.

## Security Considerations

### What the Scripts Do

**parse_document_structure.py:**
- ✅ Reads markdown files (read-only)
- ✅ Writes JSON output files (configurable location)
- ✅ No network access
- ✅ No system modifications

**extract_metadata.py:**
- ✅ Reads markdown files (read-only)
- ✅ Writes JSON output files (configurable location)
- ✅ No network access
- ✅ No system modifications

### Safe Usage Pattern

Both scripts only:
1. Read input markdown files
2. Write output JSON/markdown files to specified locations
3. Use standard library functions
4. No shell command execution
5. No network requests

### Recommended Sandbox Policy

```toml
[sandbox]
mode = "read-only"
allowed_paths = [
    "~/.codex/skills/*/scripts"  # Allow all skill scripts
]
allowed_commands = [
    "python3",
    "python"
]
```

## Troubleshooting

### "Permission denied" when running scripts

**Solution:** Add skill scripts directory to sandbox allowlist in `~/.codex/config.toml`

### "python3 not found"

**Solution:** Install Python 3:
```bash
# Ubuntu/Debian
sudo apt-get install python3

# macOS
brew install python3
```

### "tiktoken module not found"

**Solution:** This is optional. Either:
1. Install tiktoken: `pip install tiktoken`
2. Use fallback word-based estimation (automatic)

### Scripts run but output is empty

**Solution:** Check file paths are absolute, not relative:
```bash
# Bad
python3 scripts/parse_document_structure.py document.md

# Good
python3 scripts/parse_document_structure.py /full/path/to/document.md
```

## Testing the Setup

Create a test document and verify scripts work:

```bash
# Create test markdown
cat > /tmp/test.md <<'EOF'
# Test Document

## Section 1
This is a test section with some content.

## Section 2
Another section with more content.
EOF

# Test structure parsing
cd ~/.codex/skills/document-parser
python3 scripts/parse_document_structure.py /tmp/test.md

# Should output:
# Found 3 sections
# Total tokens: ~XX
# Wrote structure to structure.json
# Wrote section map to section_map.md

# Test metadata extraction
python3 scripts/extract_metadata.py /tmp/test.md

# Should output:
# Found 0 tables
# Found 0 code blocks
# ...
# Wrote metadata to metadata.json

# Clean up
rm /tmp/test.md structure.json section_map.md metadata.json
```

## Integration with Codex

When properly configured, Codex will:

1. **Detect document parsing needs** (via `when_to_use` triggers)
2. **Load the skill** (`codex-skills use document-parser`)
3. **Execute scripts** with proper sandbox permissions
4. **Process results** and present them to the user

### Example Workflow

```
User: "Parse this large document: /path/to/doc.md"

Codex:
1. Recognizes trigger phrase "parse"
2. Loads document-parser skill
3. Runs: python3 ~/.codex/skills/document-parser/scripts/parse_document_structure.py /path/to/doc.md
4. Runs: python3 ~/.codex/skills/document-parser/scripts/extract_metadata.py /path/to/doc.md
5. Presents results: "Found 56 sections, 47k tokens, extracted 54 tables..."
```

## Additional Resources

- **Skill Documentation:** See `SKILL.md` for complete usage guide
- **Chunking Principles:** See `references/chunking_principles.md` for RAG methodology
- **Codex Skills Guide:** See `codexskills/docs/START-HERE.md` for framework overview
