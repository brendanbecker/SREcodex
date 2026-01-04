#!/usr/bin/env bash
#
# uninstall-bridge.sh - Remove SREcodex bridge infrastructure and install native skills
#
# This script:
#   1. Backs up and removes symlinks in ~/.codex/ that pointed to the old bridge
#   2. Copies skills to ~/.codex/skills/ for native Codex skill support
#   3. Prompts user to remove MCP server config from ~/.codex/config.toml
#
# Usage: ./scripts/uninstall-bridge.sh
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
CODEX_DIR="${HOME}/.codex"
BACKUP_DIR="${REPO_DIR}/backups/$(date +%Y%m%d_%H%M%S)"
SKILLS_SOURCE="${REPO_DIR}/skills"

echo "========================================"
echo "SREcodex Bridge Uninstaller"
echo "========================================"
echo ""

# Check if skills source exists
if [[ ! -d "$SKILLS_SOURCE" ]]; then
    echo -e "${RED}Error: Skills directory not found at ${SKILLS_SOURCE}${NC}"
    exit 1
fi

# Create backup directory if we'll need it
backup_needed=false
if [[ -L "${CODEX_DIR}/AGENTS.md" ]] || [[ -L "${CODEX_DIR}/skills" ]]; then
    backup_needed=true
fi

if [[ "$backup_needed" == true ]]; then
    echo -e "${YELLOW}Symlinks detected in ~/.codex/ - will backup before removing${NC}"
    mkdir -p "$BACKUP_DIR"
    echo "Backup directory: $BACKUP_DIR"
    echo ""
fi

# Handle AGENTS.md symlink
if [[ -L "${CODEX_DIR}/AGENTS.md" ]]; then
    target=$(readlink "${CODEX_DIR}/AGENTS.md")
    echo -e "${YELLOW}Found symlink: ~/.codex/AGENTS.md -> ${target}${NC}"

    # Backup the target file if it exists
    if [[ -e "$target" ]]; then
        cp "$target" "${BACKUP_DIR}/AGENTS.md"
        echo "  Backed up to: ${BACKUP_DIR}/AGENTS.md"
    fi

    rm "${CODEX_DIR}/AGENTS.md"
    echo -e "${GREEN}  Removed symlink${NC}"
    echo ""
elif [[ -e "${CODEX_DIR}/AGENTS.md" ]]; then
    echo "~/.codex/AGENTS.md exists but is not a symlink - leaving as-is"
    echo ""
fi

# Handle skills symlink
if [[ -L "${CODEX_DIR}/skills" ]]; then
    target=$(readlink "${CODEX_DIR}/skills")
    echo -e "${YELLOW}Found symlink: ~/.codex/skills -> ${target}${NC}"

    # Backup the target directory if it exists
    if [[ -d "$target" ]]; then
        cp -r "$target" "${BACKUP_DIR}/skills"
        echo "  Backed up to: ${BACKUP_DIR}/skills/"
    fi

    rm "${CODEX_DIR}/skills"
    echo -e "${GREEN}  Removed symlink${NC}"
    echo ""
elif [[ -d "${CODEX_DIR}/skills" ]]; then
    echo "~/.codex/skills/ exists but is not a symlink"
    echo "Existing skills will be preserved, new skills will be merged"
    echo ""
fi

# Create skills directory if needed
if [[ ! -d "${CODEX_DIR}/skills" ]]; then
    mkdir -p "${CODEX_DIR}/skills"
    echo -e "${GREEN}Created ~/.codex/skills/${NC}"
fi

# Copy skills
echo "Installing skills from repo..."
for skill_dir in "${SKILLS_SOURCE}"/*; do
    if [[ -d "$skill_dir" ]]; then
        skill_name=$(basename "$skill_dir")

        # Skip INDEX.md if it's a file
        if [[ -f "$skill_dir" ]]; then
            continue
        fi

        if [[ -d "${CODEX_DIR}/skills/${skill_name}" ]]; then
            echo "  ${skill_name}: exists, updating..."
            rm -rf "${CODEX_DIR}/skills/${skill_name}"
        else
            echo "  ${skill_name}: installing..."
        fi

        cp -r "$skill_dir" "${CODEX_DIR}/skills/"
    fi
done

# Copy INDEX.md if it exists
if [[ -f "${SKILLS_SOURCE}/INDEX.md" ]]; then
    cp "${SKILLS_SOURCE}/INDEX.md" "${CODEX_DIR}/skills/"
    echo "  INDEX.md: installed"
fi

echo ""
echo -e "${GREEN}Skills installed successfully!${NC}"
echo ""

# Check for MCP server config
CONFIG_FILE="${CODEX_DIR}/config.toml"
if [[ -f "$CONFIG_FILE" ]] && grep -q "mcp.servers.srecodex-skills" "$CONFIG_FILE"; then
    echo "========================================"
    echo -e "${YELLOW}ACTION REQUIRED: Update config.toml${NC}"
    echo "========================================"
    echo ""
    echo "The MCP server configuration is no longer needed."
    echo "Please remove the following section from ~/.codex/config.toml:"
    echo ""
    echo -e "${RED}[mcp.servers.srecodex-skills]"
    echo 'command = "uv"'
    echo 'args = ["run", "--directory", "...", "python", "mcp_server.py"]'
    echo -e "${NC}"
    echo ""
fi

# Check for dotcodex symlink
if [[ -L "${CODEX_DIR}/dotcodex" ]]; then
    echo -e "${YELLOW}Note: ~/.codex/dotcodex symlink still exists${NC}"
    echo "You may want to remove it: rm ~/.codex/dotcodex"
    echo ""
fi

echo "========================================"
echo "Done!"
echo "========================================"
if [[ "$backup_needed" == true ]]; then
    echo ""
    echo "Backups saved to: $BACKUP_DIR"
fi
echo ""
echo "Native Codex skills are now installed in ~/.codex/skills/"
echo "Restart Codex to pick up the changes."
