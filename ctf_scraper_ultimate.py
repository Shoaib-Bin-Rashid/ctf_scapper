#!/usr/bin/env python3
"""
Ultimate CTF Scraper - All-in-One Solution
Handles authentication, multiple platforms, and provides interactive setup
"""

import os
import sys
import argparse
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)

from ctfd_scraper import CTFdScraper
from generic_scraper import GenericScraper


def get_cookie_interactive():
    """Interactive cookie input with instructions"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════╗")
    print(f"║     How to get your authentication cookie:           ║")
    print(f"╚═══════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print(f"""
{Fore.YELLOW}Step 1:{Style.RESET_ALL} Open the CTF website in your browser
{Fore.YELLOW}Step 2:{Style.RESET_ALL} Login to the CTF platform
{Fore.YELLOW}Step 3:{Style.RESET_ALL} Press F12 to open Developer Tools
{Fore.YELLOW}Step 4:{Style.RESET_ALL} Go to Application tab (Chrome) or Storage tab (Firefox)
{Fore.YELLOW}Step 5:{Style.RESET_ALL} Click on "Cookies" in the left sidebar
{Fore.YELLOW}Step 6:{Style.RESET_ALL} Select the CTF website domain
{Fore.YELLOW}Step 7:{Style.RESET_ALL} Look for cookie named "session" or similar
{Fore.YELLOW}Step 8:{Style.RESET_ALL} Copy the entire cookie value

{Fore.GREEN}Example format:{Style.RESET_ALL} session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{Fore.CYAN}Alternative - Copy ALL cookies:{Style.RESET_ALL}
In DevTools Console, run:
  document.cookie

Then paste the entire output below.
    """)
    
    cookie = input(f"{Fore.CYAN}Paste your cookie here (or press Enter to skip): {Style.RESET_ALL}").strip()
    return cookie if cookie else None


def auto_detect_platform(url: str, session) -> str:
    """Try to detect the CTF platform type"""
    import requests
    from bs4 import BeautifulSoup
    
    try:
        response = session.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Check for CTFd indicators
        if soup.find('meta', {'name': 'generator', 'content': lambda x: x and 'CTFd' in x}):
            return 'ctfd'
        if 'ctfd' in response.text.lower()[:5000]:
            return 'ctfd'
        
        # Check for rCTF indicators
        if 'rctf' in response.text.lower()[:5000]:
            return 'rctf'
            
    except:
        pass
    
    return 'generic'


def main():
    parser = argparse.ArgumentParser(
        description='🎯 Ultimate CTF Scraper - One tool to scrape them all!',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Fore.GREEN}Quick Examples:{Style.RESET_ALL}
  # Interactive mode (asks for cookie if needed)
  %(prog)s https://ctf.example.com/challenges -i

  # With cookie (for authenticated CTFs)
  %(prog)s https://ctf.example.com/challenges -c "session=YOUR_COOKIE"

  # Dry run to preview challenges
  %(prog)s https://ctf.example.com/challenges --dry-run -v

  # Specify output directory
  %(prog)s https://ctf.example.com/challenges -o ./my_ctf_challenges

{Fore.CYAN}For more help:{Style.RESET_ALL} See QUICKSTART.md or README.md
        """
    )
    
    parser.add_argument('url', help='URL of the CTF challenges page')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Interactive mode (will ask for cookie if needed)')
    parser.add_argument('-c', '--cookie', help='Authentication cookie')
    parser.add_argument('-t', '--token', help='Authentication token')
    parser.add_argument('-o', '--output', default='./ctf_challenges',
                       help='Output directory (default: ./ctf_challenges)')
    parser.add_argument('-p', '--platform', choices=['ctfd', 'generic', 'auto'],
                       default='auto', help='Platform type (default: auto-detect)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview without downloading')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    parser.add_argument('--force', action='store_true',
                       help='Force scraping even if authentication fails')
    
    args = parser.parse_args()
    
    # Banner
    print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════╗
║       🎯 Ultimate CTF Scraper & Organizer v2.0 🎯          ║
║     One Tool to Download and Organize All CTF Challenges   ║
╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """)
    
    # Interactive mode - ask for cookie if needed
    cookie = args.cookie
    if args.interactive and not cookie:
        print(f"{Fore.YELLOW}[!] Interactive mode: Checking if authentication is needed...{Style.RESET_ALL}")
        
        # Quick test to see if URL is accessible
        import requests
        try:
            test_session = requests.Session()
            test_response = test_session.get(args.url, timeout=10)
            if test_response.status_code == 403 or test_response.status_code == 401:
                print(f"{Fore.RED}[!] Authentication required (HTTP {test_response.status_code}){Style.RESET_ALL}")
                cookie = get_cookie_interactive()
            else:
                print(f"{Fore.GREEN}[✓] URL is accessible without authentication{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Could not test URL: {e}{Style.RESET_ALL}")
            if input(f"{Fore.CYAN}Do you want to provide a cookie anyway? (y/n): {Style.RESET_ALL}").lower() == 'y':
                cookie = get_cookie_interactive()
    
    # Auto-detect platform if needed
    platform = args.platform
    if platform == 'auto':
        print(f"{Fore.CYAN}[*] Auto-detecting platform...{Style.RESET_ALL}")
        import requests
        session = requests.Session()
        if cookie:
            for item in cookie.split(';'):
                if '=' in item:
                    key, value = item.strip().split('=', 1)
                    session.cookies.set(key, value)
        
        platform = auto_detect_platform(args.url, session)
        print(f"{Fore.GREEN}[✓] Detected platform: {platform.upper()}{Style.RESET_ALL}")
    
    # Create scraper
    scraper_class = CTFdScraper if platform == 'ctfd' else GenericScraper
    scraper = scraper_class(
        url=args.url,
        cookie=cookie,
        token=args.token,
        output_dir=args.output,
        verbose=args.verbose
    )
    
    # Run scraper
    try:
        print(f"{Fore.CYAN}[*] Starting scraping process...{Style.RESET_ALL}\n")
        count = scraper.run(dry_run=args.dry_run)
        
        if count > 0:
            print(f"\n{Fore.GREEN}{'=' * 60}")
            print(f"✓ SUCCESS! Processed {count} challenges!")
            print(f"{'=' * 60}{Style.RESET_ALL}")
            
            if not args.dry_run:
                output_path = Path(args.output).absolute()
                print(f"\n{Fore.CYAN}📁 Output directory:{Style.RESET_ALL} {output_path}")
                print(f"{Fore.CYAN}📂 Structure:{Style.RESET_ALL}")
                print(f"   {output_path}/")
                print(f"   ├── Pwn/")
                print(f"   ├── Web/")
                print(f"   ├── Crypto/")
                print(f"   ├── Reverse/")
                print(f"   ├── Forensics/")
                print(f"   └── Misc/")
                print(f"\n{Fore.GREEN}Happy hacking! 🚀{Style.RESET_ALL}\n")
        else:
            print(f"\n{Fore.YELLOW}{'=' * 60}")
            print(f"⚠ No challenges found")
            print(f"{'=' * 60}{Style.RESET_ALL}")
            
            if not cookie and not args.force:
                print(f"\n{Fore.CYAN}💡 Troubleshooting tips:{Style.RESET_ALL}")
                print(f"  1. The CTF might require authentication")
                print(f"     Try: {Fore.YELLOW}python {sys.argv[0]} {args.url} -i{Style.RESET_ALL}")
                print(f"  2. Check if the URL is correct")
                print(f"  3. Try with verbose mode: {Fore.YELLOW}-v{Style.RESET_ALL}")
                print(f"  4. Try generic platform: {Fore.YELLOW}--platform generic{Style.RESET_ALL}")
            
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Interrupted by user{Style.RESET_ALL}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Fore.RED}{'=' * 60}")
        print(f"✗ ERROR: {e}")
        print(f"{'=' * 60}{Style.RESET_ALL}")
        
        if args.verbose:
            import traceback
            traceback.print_exc()
        
        print(f"\n{Fore.CYAN}💡 Try:{Style.RESET_ALL}")
        print(f"  • Run with {Fore.YELLOW}-v{Style.RESET_ALL} for verbose output")
        print(f"  • Use {Fore.YELLOW}-i{Style.RESET_ALL} for interactive mode")
        print(f"  • Check QUICKSTART.md for help")
        
        sys.exit(1)


if __name__ == '__main__':
    main()
