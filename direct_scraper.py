#!/usr/bin/env python3
"""
Direct CTFd Scraper for 0xfun.org
Uses the working API directly
"""

import requests
import json
from pathlib import Path
from urllib.parse import urljoin, urlparse
import re
import sys
import time

def sanitize_filename(filename):
    """Remove special characters from filename"""
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = filename.strip('._')
    return filename or 'unnamed'

def detect_category(name, tags, category):
    """Detect challenge category"""
    # Use API category if available
    if category and category.lower() != 'misc':
        # Map common categories
        category_map = {
            'warmup': 'Warm-Up',
            'web': 'Web',
            'pwn': 'Pwn',
            'crypto': 'Crypto',
            'reverse': 'Reverse',
            'forensics': 'Forensics',
            'osint': 'OSINT',
            'misc': 'Misc',
            'general': 'General'
        }
        return category_map.get(category.lower(), category)
    
    # Fallback to tag-based detection
    text = f"{name} {' '.join(tags)}".lower()
    
    if any(k in text for k in ['pwn', 'binary', 'exploit', 'buffer', 'rop']):
        return 'Pwn'
    elif any(k in text for k in ['web', 'xss', 'sqli', 'ssrf', 'lfi']):
        return 'Web'
    elif any(k in text for k in ['crypto', 'rsa', 'aes', 'cipher']):
        return 'Crypto'
    elif any(k in text for k in ['reverse', 'rev', 'crackme', 'decompile']):
        return 'Reverse'
    elif any(k in text for k in ['forensics', 'stego', 'pcap', 'memory']):
        return 'Forensics'
    elif any(k in text for k in ['osint', 'recon', 'investigation']):
        return 'OSINT'
    elif any(k in text for k in ['warm', 'welcome', 'intro']):
        return 'Warm-Up'
    else:
        return 'Misc'

def show_cookie_help():
    """Show instructions on how to get cookies"""
    print("\n" + "="*70)
    print("🍪 HOW TO GET COOKIES (Copy as cURL - EASIEST METHOD):")
    print("="*70)
    print("\n⭐ RECOMMENDED: Copy as cURL (Fastest & Most Reliable)")
    print("  1. Open CTF website in browser (https://ctf.0xfun.org/challenges)")
    print("  2. Press F12 → Go to 'Network' tab")
    print("  3. Refresh the page (Ctrl+R or Cmd+R)")
    print("  4. Click on any request (e.g., 'challenges')")
    print("  5. Right-click on the request → Copy → Copy as cURL")
    print("  6. Paste somewhere - you'll see:")
    print()
    print("     curl 'https://ctf.0xfun.org/challenges' \\")
    print("       -H 'accept: text/html...' \\")
    print("       -b 'session=XXX; cf_clearance=YYY' \\  ← THIS LINE!")
    print("       -H 'priority: u=0, i'")
    print()
    print("  7. Copy ONLY the cookie value after '-b' (without -b):")
    print("     session=XXX; cf_clearance=YYY")
    print()
    print("  8. Use it: python3 direct_scraper.py \"session=XXX; cf_clearance=YYY\" ./output")
    print()
    print("="*70)
    print("📌 Alternative Method 1: Network Tab (Manual)")
    print("  1. F12 → Network tab → Refresh page")
    print("  2. Click on 'challenges' request")
    print("  3. Scroll to 'Request Headers' section")
    print("  4. Find 'cookie:' line")
    print("  5. Copy the value (session=XXX; cf_clearance=YYY)")
    print()
    print("📌 Alternative Method 2: Console (Quick)")
    print("  1. F12 → Console tab")
    print("  2. Type: document.cookie")
    print("  3. Press Enter and copy the output")
    print()
    print("⚠️  IMPORTANT: Cookies expire in 5-10 minutes!")
    print("   - Always get FRESH cookies right before scraping")
    print("   - If you get '403 Forbidden', refresh and get new cookies")
    print("   - Don't wait! Use cookies immediately after copying")
    print("="*70 + "\n")

def interactive_mode():
    """Interactive mode to collect cookies and settings"""
    print("\n╔══════════════════════════════════════════════════════════════════╗")
    print("║                                                                  ║")
    print("║           🎯  CTF Scraper - Interactive Mode  🎯                ║")
    print("║                                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝\n")
    
    # Ask if they need help
    print("Need help getting cookies? (y/n): ", end='')
    need_help = input().strip().lower()
    if need_help in ['y', 'yes']:
        show_cookie_help()
    
    print("\n" + "─"*70)
    print("📋 COOKIE COLLECTION")
    print("─"*70)
    
    cookies = {}
    
    # Session cookie (required)
    while True:
        print("\n🔑 Session Cookie (Required):")
        print("   Example: eyJhbGciOiJIUzI1NiJ9...")
        session = input("   Enter session value: ").strip()
        if session:
            cookies['session'] = session
            break
        print("   ❌ Session cookie is required!")
    
    # cf_clearance cookie
    print("\n🔐 Cloudflare Clearance (cf_clearance):")
    print("   Required for Cloudflare-protected sites")
    print("   Press Enter to skip if not needed")
    cf_clearance = input("   Enter cf_clearance value: ").strip()
    if cf_clearance:
        cookies['cf_clearance'] = cf_clearance
    
    # __cfduid cookie
    print("\n🆔 Cloudflare UID (__cfduid):")
    print("   Optional - Press Enter to skip")
    cfduid = input("   Enter __cfduid value: ").strip()
    if cfduid:
        cookies['__cfduid'] = cfduid
    
    # Other cookies
    print("\n➕ Any other cookies? (Press Enter to skip)")
    try:
        while True:
            cookie_name = input("   Cookie name (or Enter to finish): ").strip()
            if not cookie_name:
                break
            cookie_value = input(f"   Value for '{cookie_name}': ").strip()
            if cookie_value:
                cookies[cookie_name] = cookie_value
    except (EOFError, KeyboardInterrupt):
        pass
    
    # Build cookie string
    cookies_str = '; '.join([f"{k}={v}" for k, v in cookies.items()])
    
    print("\n" + "─"*70)
    print("📁 OUTPUT SETTINGS")
    print("─"*70)
    
    # Output directory
    print("\n💾 Output Directory:")
    print("   Default: ./0xfun_ctf")
    try:
        output_dir = input("   Enter output path (or Enter for default): ").strip()
        if not output_dir:
            output_dir = "./0xfun_ctf"
    except (EOFError, KeyboardInterrupt):
        output_dir = "./0xfun_ctf"
    
    print("\n" + "─"*70)
    print("✅ READY TO SCRAPE!")
    print("─"*70)
    print(f"🍪 Cookies collected: {list(cookies.keys())}")
    print(f"📁 Output directory: {output_dir}")
    print("─"*70)
    
    return cookies_str, output_dir

def show_usage():
    """Show usage and help"""
    print("\n" + "="*70)
    print("🎯 CTFd Direct Scraper - Usage Guide")
    print("="*70)
    print("\n📋 COMMAND LINE USAGE:")
    print()
    print("  python3 direct_scraper.py URL \"COOKIES\" ./output_folder")
    print()
    print("  Example:")
    print("  python3 direct_scraper.py https://ctf.0xfun.org/challenges \\")
    print("    \"session=XXX; cf_clearance=YYY\" ./my_ctf")
    print()
    print("📋 INTERACTIVE MODE:")
    print()
    print("  python3 direct_scraper.py")
    print("  (Then follow the prompts)")
    print()
    print("📋 SHOW HELP:")
    print()
    print("  python3 direct_scraper.py --help")
    print("  python3 direct_scraper.py -h")
    print()
    print("="*70)
    print("🔥 QUICK COOKIE EXTRACTION (Copy as cURL):")
    print("="*70)
    print()
    print("1. Browser → F12 → Network tab → Refresh page")
    print("2. Right-click on 'challenges' request → Copy → Copy as cURL")
    print("3. Find the line with '-b' flag:")
    print()
    print("   -b 'session=XXX; cf_clearance=YYY'")
    print()
    print("4. Copy ONLY the cookie value (without -b):")
    print()
    print("   session=XXX; cf_clearance=YYY")
    print()
    print("5. Run:")
    print()
    print("   python3 direct_scraper.py URL \"session=XXX; cf_clearance=YYY\" ./output")
    print()
    print("="*70)
    print("⚠️  COOKIE EXPIRATION WARNING:")
    print("="*70)
    print()
    print("  • Cookies expire in 5-10 minutes!")
    print("  • Get FRESH cookies right before scraping")
    print("  • If you see '403 Forbidden' → Refresh & get new cookies")
    print("  • Use cookies immediately after copying")
    print()
    print("="*70)
    print()

def main():
    # Check for help flag
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_usage()
        show_cookie_help()
        sys.exit(0)
    
    # Check if interactive mode
    if len(sys.argv) < 2:
        cookies_str, output_dir = interactive_mode()
    else:
        cookies_str = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "./0xfun_ctf"
    
    # Parse cookies
    cookies = {}
    for item in cookies_str.split(';'):
        if '=' in item:
            key, value = item.strip().split('=', 1)
            cookies[key] = value
    
    print(f"🍪 Cookies: {list(cookies.keys())}")
    print(f"📁 Output directory: {output_dir}\n")
    
    # Setup session with enhanced headers
    session = requests.Session()
    session.cookies.update(cookies)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Ch-Ua': '"Not.A/Brand";v="99", "Chromium";v="136"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Referer': 'https://ctf.0xfun.org/login',
    })
    
    # Get challenges from API
    print("🔗 Fetching challenges from API...")
    try:
        response = session.get('https://ctf.0xfun.org/api/v1/challenges', timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('success'):
            print("❌ API returned success=false")
            sys.exit(1)
        
        challenges = data.get('data', [])
        print(f"✅ Found {len(challenges)} challenges!\n")
        
    except Exception as e:
        print(f"❌ Failed to fetch challenges: {e}")
        sys.exit(1)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Process each challenge
    ctf_name = "0xFun_CTF_2026"
    success_count = 0
    error_count = 0
    
    for i, chall in enumerate(challenges, 1):
        try:
            chall_id = chall.get('id')
            name = chall.get('name', 'Unknown')
            category = chall.get('category', 'Misc')
            
            print(f"[{i}/{len(challenges)}] Processing: {name} [{category}]")
            
            # Get challenge details
            detail_url = f'https://ctf.0xfun.org/api/v1/challenges/{chall_id}'
            detail_response = session.get(detail_url, timeout=30)
            
            # Add delay to prevent rate limiting
            time.sleep(0.5)
            
            if detail_response.status_code != 200:
                print(f"  ⚠️  Failed to get details (HTTP {detail_response.status_code})")
                error_count += 1
                continue
            
            detail_data = detail_response.json()
            if not detail_data.get('success'):
                print(f"  ⚠️  API returned success=false for details")
                error_count += 1
                continue
            
            chall_detail = detail_data.get('data', {})
            description = chall_detail.get('description', 'No description')
            value = chall_detail.get('value', 0)
            tags = [t.get('value', '') for t in chall.get('tags', [])]
            
            # Detect category
            final_category = detect_category(name, tags, category)
            
            # Create folder structure
            safe_name = sanitize_filename(name)
            challenge_path = output_path / ctf_name / final_category / safe_name
            files_path = challenge_path / 'files'
            
            challenge_path.mkdir(parents=True, exist_ok=True)
            files_path.mkdir(exist_ok=True)
            
            # Save statement
            statement = f"Challenge: {name}\n"
            statement += f"Category: {final_category}\n"
            statement += f"Points: {value}\n"
            if tags:
                statement += f"Tags: {', '.join(tags)}\n"
            statement += f"\nDescription:\n{description}\n"
            
            statement_file = challenge_path / 'statement.txt'
            with open(statement_file, 'w', encoding='utf-8') as f:
                f.write(statement)
            
            print(f"  ✅ Saved statement")
            
            # Download files
            files = chall_detail.get('files', [])
            if files:
                print(f"  📥 Downloading {len(files)} file(s)...")
                for file_path in files:
                    try:
                        file_url = urljoin('https://ctf.0xfun.org', file_path)
                        file_name = file_url.split('/')[-1].split('?')[0]
                        safe_file_name = sanitize_filename(file_name)
                        
                        file_response = session.get(file_url, stream=True, timeout=30)
                        file_response.raise_for_status()
                        
                        file_dest = files_path / safe_file_name
                        with open(file_dest, 'wb') as f:
                            for chunk in file_response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        
                        print(f"    ✅ {safe_file_name}")
                        time.sleep(0.3)  # Small delay after file download
                    except Exception as e:
                        print(f"    ❌ Failed to download {file_name}: {e}")
            
            success_count += 1
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            error_count += 1
    
    print(f"\n{'='*60}")
    print(f"✅ Successfully processed: {success_count}/{len(challenges)}")
    print(f"❌ Errors: {error_count}")
    print(f"📁 Output directory: {output_path / ctf_name}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
