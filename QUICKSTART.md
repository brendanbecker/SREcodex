# SREcodex Quick Start

Get the MCP semantic skill search running in 5 minutes.

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) installed
- Codex CLI configured

## Step 1: Index Skills

```bash
cd mcp-server
make setup    # Install dependencies
make index    # Index skills to ChromaDB
make test     # Verify (should show 6+ skills)
```

## Step 2: Configure Codex

Add to `~/.codex/config.toml`:

```toml
[mcp.servers.srecodex-skills]
command = "uv"
args = ["run", "--directory", "/path/to/SREcodex/mcp-server", "python", "mcp_server.py"]
```

Replace `/path/to/SREcodex` with your actual path.

## Step 3: (Optional) Run as Background Service

```bash
# Create systemd service
mkdir -p ~/.config/systemd/user
cp docs/mcp-skills.service ~/.config/systemd/user/

# Edit paths in the service file, then:
systemctl --user daemon-reload
systemctl --user enable --now mcp-skills
```

Or see [mcp-server/SYSTEMD.md](mcp-server/SYSTEMD.md) for manual setup.

## Step 4: Test in Codex

Restart Codex, then:

```
What MCP tools do you have available?
```

Should show `search_skills` from `srecodex-skills`.

Test with:
```
Parse and summarize /path/to/some/large/document.pdf
```

## Adding New Skills

1. Create skill following the template:
   ```bash
   cp dotcodex/templates/SKILL.template.md dotcodex/skills/my-skill/SKILL.md
   ```

2. Edit the skill with proper YAML frontmatter

3. Re-index:
   ```bash
   cd mcp-server && make reindex
   ```

4. Restart systemd service (if using):
   ```bash
   systemctl --user restart mcp-skills
   ```

## Migrating Existing Skills

See [MIGRATE-SKILLS.md](MIGRATE-SKILLS.md) for upgrading pre-existing skills to the new format.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `search_skills` not showing | Restart Codex after config change |
| "Collection not found" | Run `make index` |
| Service won't start | Check `journalctl --user -u mcp-skills` |
| No skills indexed | Ensure skills have YAML frontmatter |

## Documentation

- [mcp-server/SETUP.md](mcp-server/SETUP.md) — Detailed Codex integration
- [mcp-server/SYSTEMD.md](mcp-server/SYSTEMD.md) — Background service setup
- [dotcodex/docs/SKILL-SCHEMA.md](dotcodex/docs/SKILL-SCHEMA.md) — Skill format spec
