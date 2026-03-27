#!/bin/bash
# Banana Claude -- Install Script
# Standalone installer -- copies skill to ~/.claude/skills/ for Claude Code.
# For plugin installation, use: /plugin marketplace add AgriciDaniel/banana-claude
#
# Usage:
#   ./install.sh                    # Install skill only
#   ./install.sh --with-mcp KEY    # Install skill + configure MCP with API key
#   ./install.sh --uninstall        # Remove skill

set -euo pipefail

SKILL_NAME="banana"
SKILL_DIR="$HOME/.claude/skills/$SKILL_NAME"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/skills/$SKILL_NAME"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Uninstall
if [[ "${1:-}" == "--uninstall" ]]; then
    if [[ -d "$SKILL_DIR" ]]; then
        rm -rf "$SKILL_DIR"
        info "Removed skill from $SKILL_DIR"
    else
        warn "Skill not found at $SKILL_DIR"
    fi
    exit 0
fi

# Check source exists
if [[ ! -d "$SOURCE_DIR" ]]; then
    error "Source directory not found: $SOURCE_DIR"
    exit 1
fi

# Install skill
info "Installing Banana Claude skill..."
mkdir -p "$SKILL_DIR"
cp -r "$SOURCE_DIR"/* "$SKILL_DIR/"
chmod +x "$SKILL_DIR/scripts/"*.py 2>/dev/null || true
info "Skill installed to $SKILL_DIR"

# Create data directory for cost tracking and presets
mkdir -p "$HOME/.banana/presets"
info "Created ~/.banana/ for cost tracking and presets"

# Configure MCP if requested
if [[ "${1:-}" == "--with-mcp" ]]; then
    API_KEY="${2:-}"
    if [[ -z "$API_KEY" ]]; then
        error "API key required: ./install.sh --with-mcp YOUR_KEY"
        exit 1
    fi
    info "Configuring MCP server..."
    python3 "$SKILL_DIR/scripts/setup_mcp.py" --key "$API_KEY"
fi

# Validate
info "Running validation..."
python3 "$SKILL_DIR/scripts/validate_setup.py"

echo ""
info "Installation complete!"
echo "  Skill: /banana"
echo "  Location: $SKILL_DIR"
echo ""
echo "Next steps:"
echo "  1. Get a free API key: https://aistudio.google.com/apikey"
echo "  2. In Claude Code, run: /banana setup"
echo "  3. Restart Claude Code"
echo "  4. Try: /banana generate \"a cat astronaut in space\""
