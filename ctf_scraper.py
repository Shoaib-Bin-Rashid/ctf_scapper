#!/usr/bin/env python3
"""
CTF Scraper - Main CLI
Automated tool to scrape and organize CTF challenges
"""

import argparse
import sys
import yaml
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

from ctfd_scraper import CTFdScraper
from generic_scraper import GenericScraper
from scraper_base import BaseScraper


def print_banner():
    """Print tool banner"""
    banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════╗
║           CTF Scraper & Organizer v1.0                ║
║     Automated CTF Challenge Downloader & Organizer    ║
╚═══════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


def load_config(config_file: str) -> dict:
    """Load configuration from YAML file"""
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        print(f"{Fore.YELLOW}[WARNING] Config file not found: {config_file}{Style.RESET_ALL}")
        return {}
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Failed to load config: {e}{Style.RESET_ALL}")
        return {}


def detect_platform(url: str) -> str:
    """Detect CTF platform type from URL"""
    # Add more sophisticated detection later
    # For now, default to CTFd as it's most common
    return 'ctfd'


def create_scraper(url: str, args, config: dict) -> BaseScraper:
    """Create appropriate scraper instance based on platform"""
    
    # Get authentication from args or config
    cookie = args.cookie or config.get('auth', {}).get('cookie')
    token = args.token or config.get('auth', {}).get('token')
    
    # Get output directory
    output_dir = args.output or config.get('output_dir', './ctf_challenges')
    
    # Detect platform
    platform = args.platform or detect_platform(url)
    
    # Create scraper instance
    if platform.lower() == 'ctfd':
        return CTFdScraper(
            url=url,
            cookie=cookie,
            token=token,
            output_dir=output_dir,
            verbose=args.verbose
        )
    elif platform.lower() == 'generic':
        return GenericScraper(
            url=url,
            cookie=cookie,
            token=token,
            output_dir=output_dir,
            verbose=args.verbose
        )
    else:
        print(f"{Fore.RED}[ERROR] Unsupported platform: {platform}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Supported platforms: ctfd, generic{Style.RESET_ALL}")
        sys.exit(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Scrape and organize CTF challenges',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  %(prog)s https://ctf.example.com/challenges

  # With authentication
  %(prog)s https://ctf.example.com/challenges --cookie "session=abc123"

  # Using config file
  %(prog)s https://ctf.example.com/challenges --config config.yaml

  # Dry run (preview only)
  %(prog)s https://ctf.example.com/challenges --dry-run

  # Specify output directory
  %(prog)s https://ctf.example.com/challenges -o ./my_ctf
        """
    )
    
    parser.add_argument(
        'url',
        help='URL of the CTF challenges page'
    )
    
    parser.add_argument(
        '-c', '--cookie',
        help='Authentication cookie (format: "key=value; key2=value2")'
    )
    
    parser.add_argument(
        '-t', '--token',
        help='Authentication token (Bearer token)'
    )
    
    parser.add_argument(
        '--config',
        help='Path to configuration YAML file'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output directory for downloaded challenges (default: ./ctf_challenges)'
    )
    
    parser.add_argument(
        '-p', '--platform',
        choices=['ctfd', 'generic'],
        help='CTF platform type (auto-detected if not specified)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview challenges without downloading'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0'
    )
    
    args = parser.parse_args()
    
    # Print banner
    if not args.dry_run:
        print_banner()
    
    # Load config if specified
    config = {}
    if args.config:
        config = load_config(args.config)
    
    # Create scraper
    try:
        scraper = create_scraper(args.url, args, config)
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Failed to create scraper: {e}{Style.RESET_ALL}")
        sys.exit(1)
    
    # Run scraper
    try:
        count = scraper.run(dry_run=args.dry_run)
        
        if count > 0:
            print(f"\n{Fore.GREEN}✓ Successfully processed {count} challenges!{Style.RESET_ALL}")
            if not args.dry_run:
                output_path = Path(args.output or config.get('output_dir', './ctf_challenges'))
                print(f"{Fore.CYAN}Output directory: {output_path.absolute()}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}⚠ No challenges found{Style.RESET_ALL}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Interrupted by user{Style.RESET_ALL}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Fore.RED}[ERROR] Scraping failed: {e}{Style.RESET_ALL}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
