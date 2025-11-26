# Running MCP Server as a Systemd Service

This guide sets up the MCP server to run automatically in the background using systemd user services.

## Prerequisites

- Skills indexed: `make index`
- Server tested: `make test`

## Step 1: Find your uv path

```bash
which uv
```

Note the full path (e.g., `/home/becker/.local/bin/uv`).

## Step 2: Create the service file

```bash
mkdir -p ~/.config/systemd/user
```

Create `~/.config/systemd/user/mcp-skills.service`:

```ini
[Unit]
Description=SREcodex MCP Skills Server
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/becker/projects/SREcodex/mcp-server
ExecStart=/home/becker/.local/bin/uv run python mcp_server.py
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

# Environment (uncomment if needed)
# Environment=PATH=/home/becker/.local/bin:/usr/bin

[Install]
WantedBy=default.target
```

> **Important**: Replace paths with your actual locations:
> - `WorkingDirectory`: Path to your mcp-server directory
> - `ExecStart`: Full path to `uv` binary

## Step 3: Enable and start the service

```bash
# Reload systemd to pick up new service
systemctl --user daemon-reload

# Enable auto-start on login
systemctl --user enable mcp-skills

# Start the service now
systemctl --user start mcp-skills

# Check status
systemctl --user status mcp-skills
```

## Step 4: Verify it's running

```bash
# Check logs
journalctl --user -u mcp-skills -f

# Should show:
# Connected to ChromaDB collection: srecodex_skills
# Collection contains 6 documents
```

## Common Commands

| Command | Description |
|---------|-------------|
| `systemctl --user start mcp-skills` | Start the service |
| `systemctl --user stop mcp-skills` | Stop the service |
| `systemctl --user restart mcp-skills` | Restart after changes |
| `systemctl --user status mcp-skills` | Check if running |
| `journalctl --user -u mcp-skills -f` | Follow logs |
| `journalctl --user -u mcp-skills --since "5 min ago"` | Recent logs |

## Re-indexing Skills

After adding or modifying skills:

```bash
# Re-index
cd ~/projects/SREcodex/mcp-server && make index

# Restart service to pick up changes
systemctl --user restart mcp-skills
```

## Troubleshooting

### Service won't start

Check logs for errors:
```bash
journalctl --user -u mcp-skills -n 50
```

Common issues:
- Wrong path to `uv` — verify with `which uv`
- Wrong `WorkingDirectory` — must be absolute path
- Missing dependencies — run `make setup` first
- ChromaDB not indexed — run `make index` first

### "Failed to connect to bus"

Enable lingering for user services to run without login:
```bash
sudo loginctl enable-linger $USER
```

### Service starts but Codex can't connect

The systemd service runs the server on stdio. Codex spawns its own instance via the config. You may not need the systemd service if Codex manages the process itself.

Check your `~/.codex/config.toml`:
```toml
[mcp.servers.srecodex-skills]
command = "uv"
args = ["run", "--directory", "/home/becker/projects/SREcodex/mcp-server", "python", "mcp_server.py"]
```

Codex will spawn the server on-demand using this config.

### WSL-specific issues

If running in WSL, systemd may not be enabled by default. Check:
```bash
ps -p 1 -o comm=
```

If it shows `init` instead of `systemd`, enable systemd in WSL:

Edit `/etc/wsl.conf`:
```ini
[boot]
systemd=true
```

Then restart WSL:
```powershell
wsl --shutdown
```

## Alternative: On-demand via Codex

If systemd setup is problematic, Codex can spawn the server on-demand. This is the simplest approach — just ensure your config.toml is correct and Codex will manage the process lifecycle.

The systemd approach is useful if:
- You want the server always running
- You want faster first-query response (no spawn delay)
- You're debugging and want persistent logs
