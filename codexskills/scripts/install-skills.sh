#!/usr/bin/env bash
# install-skills.sh - Install Codex Skills System
# Based on Jesse Vincent's proven superpowers implementation

set -euo pipefail
shopt -s nullglob

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
DOCS_DIR="${REPO_ROOT}/docs"
SKILL_SOURCE_DIR="${REPO_ROOT}/skills"
CODEX_SCRIPT="${SCRIPT_DIR}/codex-skills"
AGENTS_SOURCE="${REPO_ROOT}/AGENTS-TEMPLATE.md"
REPO_PARENT="$(cd "${REPO_ROOT}/.." && pwd)"

echo "=== Codex Skills System Installer ==="
echo ""

# Paths
DEFAULT_DOTCODEX_DIR="${REPO_PARENT}/dotcodex"
CODEX_DIR_RAW="${DOTCODEX_DIR:-${DEFAULT_DOTCODEX_DIR}}"
CODEX_DIR="$(cd "${CODEX_DIR_RAW}" 2>/dev/null && pwd || echo "${CODEX_DIR_RAW}")"
SKILLS_DIR="${CODEX_DIR}/skills"
BIN_DIR="${HOME}/.local/bin"
AGENTS_LINK="${HOME}/.codex/AGENTS.md"
SKILLS_LINK="${HOME}/.codex/skills"

# 1. Create directory structure
echo "[1/6] Preparing directory structure..."
mkdir -p "${CODEX_DIR}"
mkdir -p "${SKILLS_DIR}"
mkdir -p "${BIN_DIR}"
echo "  ✓ Using DOTCODEX_DIR target: ${CODEX_DIR}"
if [[ -z "${DOTCODEX_DIR:-}" ]]; then
    echo "    (set DOTCODEX_DIR to override the default sibling ${DEFAULT_DOTCODEX_DIR})"
fi
echo "  ✓ Created ${SKILLS_DIR}"
echo "  ✓ Ensured ${BIN_DIR} exists"

# 2. Ensure ~/.codex/AGENTS.md and ~/.codex/skills point to DOTCODEX_DIR
echo "[2/6] Ensuring ~/.codex symlinks point to DOTCODEX_DIR..."
mkdir -p "${HOME}/.codex"

# Remove existing skills directory/link to ensure clean symlink creation
rm -rf "${SKILLS_LINK}"

ln -sfn "${CODEX_DIR}/AGENTS.md" "${AGENTS_LINK}"
ln -sfn "${CODEX_DIR}/skills" "${SKILLS_LINK}"
echo "  ✓ Linked ${AGENTS_LINK} and ${SKILLS_LINK}"

# Store DOTCODEX_DIR location for codex-skills command
echo "DOTCODEX_DIR=${CODEX_DIR}" > "${HOME}/.codex/config.env"
echo "  ✓ Saved config to ~/.codex/config.env"

# 3. Install codex-skills script
echo "[3/6] Installing codex-skills command..."
cp "${CODEX_SCRIPT}" "${BIN_DIR}/codex-skills"
chmod +x "${BIN_DIR}/codex-skills"
echo "  ✓ Installed to ${BIN_DIR}/codex-skills"

# 4. Install AGENTS.md
echo "[4/6] Installing AGENTS.md..."
if [[ -f "${CODEX_DIR}/AGENTS.md" ]]; then
    backup="${CODEX_DIR}/AGENTS.md.backup.$(date +%Y%m%d_%H%M%S)"
    cp "${CODEX_DIR}/AGENTS.md" "${backup}"
    echo "  ✓ Backed up existing AGENTS.md to $(basename $backup)"
fi

cp "${AGENTS_SOURCE}" "${CODEX_DIR}/AGENTS.md"
echo "  ✓ Installed AGENTS.md"

# 5. Install bundled skills
echo "[5/6] Installing bundled skills..."
skills_found=false
for skill_md in "${SKILL_SOURCE_DIR}"/*/SKILL.md; do
    skills_found=true
    skill_name=$(basename "$(dirname "${skill_md}")")
    skill_source_dir="$(dirname "${skill_md}")"

    # Create skill directory
    mkdir -p "${SKILLS_DIR}/${skill_name}"

    # Copy entire skill directory (including scripts, references, etc.)
    cp -r "${skill_source_dir}"/* "${SKILLS_DIR}/${skill_name}/"

    echo "  ✓ Installed ${skill_name} skill"
done

if ! $skills_found; then
    echo "  ⚠ No skills found under ${SKILL_SOURCE_DIR}"
fi

# 6. Verify installation
echo "[6/6] Verifying installation..."
if command -v codex-skills &> /dev/null; then
    echo "  ✓ codex-skills command available"
elif [[ -x "${BIN_DIR}/codex-skills" ]]; then
    echo "  ⚠ codex-skills installed but not in PATH"
    echo "    Add to your ~/.bashrc or ~/.zshrc:"
    echo "    export PATH=\"\${HOME}/.local/bin:\${PATH}\""
else
    echo "  ✗ codex-skills not found"
    exit 1
fi

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Structure:"
echo "  ${CODEX_DIR}/AGENTS.md"
echo "  ${CODEX_DIR}/skills/time-awareness/SKILL.md"
echo "  ${BIN_DIR}/codex-skills"
echo ""

# Check if any skills with scripts were installed
has_scripts=false
for skill_dir in "${SKILLS_DIR}"/*; do
    if [[ -d "${skill_dir}/scripts" ]]; then
        has_scripts=true
        break
    fi
done

if $has_scripts; then
    config_file="${HOME}/.codex/config.toml"

    # Check existing config
    config_exists=false
    has_sandbox_section=false
    has_allowed_paths=false
    already_configured=false

    if [[ -f "${config_file}" ]]; then
        config_exists=true

        # Check if [sandbox] section exists
        if grep -q '^\[sandbox\]' "${config_file}"; then
            has_sandbox_section=true
        fi

        # Check if allowed_paths exists
        if grep -q 'allowed_paths' "${config_file}"; then
            has_allowed_paths=true

            # Check if skills/*/scripts is already in allowed_paths
            if grep -A 5 'allowed_paths' "${config_file}" | grep -q 'skills.*scripts'; then
                already_configured=true
            fi
        fi
    fi

    if $already_configured; then
        echo "✓ Sandbox configuration detected"
        echo ""
        echo "  Your ~/.codex/config.toml already includes skill script paths."
        echo "  No configuration changes needed."
        echo ""
    else
        echo "⚠️  SANDBOX CONFIGURATION REQUIRED"
        echo ""
        echo "Some skills include executable scripts. To allow Claude Code to run them"
        echo "in read-only sandbox mode:"
        echo ""

        if ! $config_exists; then
            # No config file - provide complete config
            echo "Create ~/.codex/config.toml with:"
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            cat <<'EOF'
[sandbox]
# Allow execution of scripts from skills directory
allowed_paths = [
    "~/.codex/skills/*/scripts",
    "~/.local/bin",
    "/usr/bin/python3"
]
EOF
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        elif ! $has_sandbox_section; then
            # Has config but no [sandbox] section - add section
            echo "Add this section to ~/.codex/config.toml:"
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            cat <<'EOF'
[sandbox]
# Allow execution of scripts from skills directory
allowed_paths = [
    "~/.codex/skills/*/scripts",
    "~/.local/bin",
    "/usr/bin/python3"
]
EOF
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        elif ! $has_allowed_paths; then
            # Has [sandbox] but no allowed_paths - add to existing section
            echo "Add to the existing [sandbox] section in ~/.codex/config.toml:"
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            cat <<'EOF'
allowed_paths = [
    "~/.codex/skills/*/scripts",
    "~/.local/bin",
    "/usr/bin/python3"
]
EOF
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        else
            # Has [sandbox] and allowed_paths but missing skill scripts path
            echo "Add to the allowed_paths array in ~/.codex/config.toml:"
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            cat <<'EOF'
    "~/.codex/skills/*/scripts",
EOF
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        fi

        echo ""
        echo "After updating config.toml, restart Claude Code."
        echo ""
    fi
fi

echo "Next steps:"
echo "  1. Ensure DOTCODEX_DIR points at your shared dotcodex repo (default: ${DEFAULT_DOTCODEX_DIR})"
echo "  2. ~/.codex already links to DOTCODEX files (AGENTS.md + skills)"
echo "  3. Ensure ~/.local/bin is in your PATH"
echo "  4. Open a new terminal or run: source ~/.bashrc"
echo "  5. Test: codex-skills list"
echo "  6. Start Codex and ask: 'What day is it?'"
echo ""
