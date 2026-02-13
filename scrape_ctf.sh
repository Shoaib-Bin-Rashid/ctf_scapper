#!/bin/bash
# CTF Scraper Bash Wrapper
# Easy-to-use wrapper for the Python CTF scraper

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/ctf_scraper.py"

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo -e "${RED}Error: ctf_scraper.py not found${NC}"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check if dependencies are installed
check_dependencies() {
    python3 -c "import requests, bs4, yaml, colorama" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}Warning: Some dependencies are missing${NC}"
        echo -e "${BLUE}Installing dependencies...${NC}"
        pip3 install -r "$SCRIPT_DIR/requirements.txt"
    fi
}

# Show help
show_help() {
    cat << EOF
${BLUE}CTF Scraper & Organizer${NC}
Automated tool to scrape and organize CTF challenges

${GREEN}Usage:${NC}
  $0 <url> [options]

${GREEN}Examples:${NC}
  # Basic scraping
  $0 https://ctf.example.com/challenges

  # With authentication cookie
  $0 https://ctf.example.com/challenges -c "session=abc123"

  # Dry run (preview only)
  $0 https://ctf.example.com/challenges --dry-run

  # Specify output directory
  $0 https://ctf.example.com/challenges -o ./my_ctf

  # Use config file
  $0 https://ctf.example.com/challenges --config config.yaml

  # Verbose mode
  $0 https://ctf.example.com/challenges -v

${GREEN}Options:${NC}
  -c, --cookie <cookie>     Authentication cookie
  -t, --token <token>       Authentication token
  --config <file>           Configuration file
  -o, --output <dir>        Output directory
  -p, --platform <type>     Platform type (ctfd, generic)
  --dry-run                 Preview without downloading
  -v, --verbose             Verbose output
  -h, --help                Show this help

${GREEN}Quick Start:${NC}
  1. Install dependencies: pip3 install -r requirements.txt
  2. Run scraper: $0 <ctf_url>
  3. Find downloaded challenges in ./ctf_challenges/

EOF
}

# Parse arguments
if [ $# -eq 0 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_help
    exit 0
fi

# Check dependencies before running
check_dependencies

# Run the Python script with all arguments
python3 "$PYTHON_SCRIPT" "$@"
