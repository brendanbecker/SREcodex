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
ln -sfn "${CODEX_DIR}/AGENTS.md" "${AGENTS_LINK}"
ln -sfn "${CODEX_DIR}/skills" "${SKILLS_LINK}"
echo "  ✓ Linked ${AGENTS_LINK} and ${SKILLS_LINK}"

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
    mkdir -p "${SKILLS_DIR}/${skill_name}"
    cp "${skill_md}" "${SKILLS_DIR}/${skill_name}/SKILL.md"
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
echo "Next steps:"
echo "  1. Ensure DOTCODEX_DIR points at your shared dotcodex repo (default: ${DEFAULT_DOTCODEX_DIR})"
echo "  2. ~/.codex already links to DOTCODEX files (AGENTS.md + skills)"
echo "  3. Ensure ~/.local/bin is in your PATH"
echo "  4. Open a new terminal or run: source ~/.bashrc"
echo "  5. Test: codex-skills list"
echo "  6. Start Codex and ask: 'What day is it?'"
echo ""
