#!/bin/bash
# Example usage script for CTF Scraper

# This script demonstrates various ways to use the CTF scraper

echo "=== CTF Scraper - Usage Examples ==="
echo ""

# Activate virtual environment
source venv/bin/activate

echo "1. Dry run (preview only - recommended first step)"
echo "   Command: python ctf_scraper.py <URL> --dry-run -v"
echo ""

echo "2. Basic scraping (public CTF)"
echo "   Command: python ctf_scraper.py <URL>"
echo ""

echo "3. With authentication cookie"
echo "   Command: python ctf_scraper.py <URL> --cookie 'session=YOUR_COOKIE'"
echo ""

echo "4. Using configuration file"
echo "   Command: python ctf_scraper.py <URL> --config config.yaml"
echo ""

echo "5. Custom output directory"
echo "   Command: python ctf_scraper.py <URL> -o ~/CTFs/MyCompetition"
echo ""

echo "6. Generic scraper for unknown platforms"
echo "   Command: python ctf_scraper.py <URL> --platform generic -v"
echo ""

echo "=== Quick Test ==="
echo "To test the tool, try:"
echo "  python ctf_scraper.py https://ctf.example.com/challenges --dry-run -v"
echo ""

echo "=== Getting Your Session Cookie ==="
echo "1. Open the CTF website in your browser"
echo "2. Press F12 to open DevTools"
echo "3. Go to Application/Storage tab"
echo "4. Click on Cookies"
echo "5. Find the 'session' cookie and copy its value"
echo "6. Use it with: --cookie 'session=YOUR_VALUE'"
echo ""

echo "For more help, run: python ctf_scraper.py --help"
