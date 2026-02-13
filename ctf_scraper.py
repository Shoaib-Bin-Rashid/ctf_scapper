#!/usr/bin/env python3
"""
Universal CTFd Scraper
Works with any CTFd-based platform
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
    return re.sub(r'[<>:"/\\|?*]', '_', filename).strip()

def detect_category(name, tags, category):
    """Detect challenge category"""
    name_lower = name.lower()
    tags_lower = ' '.join(tags).lower()
    
    if 'web' in category.lower() or 'web' in name_lower:
        return 'Web'
    elif 'pwn' in category.lower() or 'binary' in category.lower():
        return 'Pwn'
    elif 'crypto' in category.lower():
        return 'Crypto'
    elif 'reverse' in category.lower() or 'rev' in category.lower():
        return 'Rev'
    elif 'forensic' in category.lower():
        return 'Forensic'
    elif 'osint' in category.lower():
        return 'OSINT'
    elif 'misc' in category.lower():
        return 'Misc'
    elif 'hardware' in category.lower():
        return 'Hardware'
    elif 'warm' in name_lower or 'warmup' in category.lower():
        return 'Warm-Up'
    else:
        return category.replace(' ', '-')

def extract_base_url(url):
    """Extract base URL"""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"

def extract_ctf_name(url):
    """Try to extract CTF name from URL"""
    parsed = urlparse(url)
    domain = parsed.netloc.replace('www.', '')
    
    # Try to get a meaningful name from domain
    parts = domain.split('.')
    if len(parts) >= 2:
        main_part = parts[0]
        # Clean up common patterns
        if main_part in ['ctf', 'play', 'challenges']:
            # Use second part
            if len(parts) >= 2:
                return parts[1].replace('-', '_').upper() + "_CTF"
        return main_part.replace('-', '_').upper() + "_CTF"
    
    return "CTF_Download"

def main():
    print("\n" + "="*70)
    print("🎯 Universal CTFd Scraper")
    print("="*70 + "\n")
    
    # Parse arguments
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print("Usage:")
        print(f"  {sys.argv[0]} URL \"COOKIES\" [OUTPUT_DIR]")
        print()
        print("Example:")
        print(f"  {sys.argv[0]} https://ctf.0xfun.org/challenges \\")
        print('    "session=XXX; cf_clearance=YYY" ./output')
        print()
        print("Arguments:")
        print("  URL          - CTF website URL (e.g., https://ctf.0xfun.org/challenges)")
        print("  COOKIES      - Cookie string from browser")
        print("  OUTPUT_DIR   - Output directory (optional, default: ./ctf_download)")
        print()
        print("How to get cookies:")
        print("  1. Browser → F12 → Network → Refresh")
        print("  2. Right-click request → Copy → Copy as cURL")
        print("  3. Find: -b 'session=XXX; cf_clearance=YYY'")
        print("  4. Copy cookie value")
        sys.exit(0 if sys.argv[1] in ['-h', '--help'] else 1)
    
    ctf_url = sys.argv[1]
    cookies_str = sys.argv[2] if len(sys.argv) > 2 else ""
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "./ctf_download"
    
    if not cookies_str:
        print("❌ Error: Cookies required!")
        print(f"Usage: {sys.argv[0]} URL \"COOKIES\" [OUTPUT_DIR]")
        sys.exit(1)
    
    # Extract base URL and CTF name
    base_url = extract_base_url(ctf_url)
    ctf_name = extract_ctf_name(ctf_url)
    
    print(f"🌐 URL: {ctf_url}")
    print(f"🏠 Base: {base_url}")
    print(f"📛 CTF: {ctf_name}")
    
    # Parse cookies
    cookies = {}
    for item in cookies_str.split(';'):
        if '=' in item:
            key, value = item.strip().split('=', 1)
            cookies[key] = value
    
    print(f"🍪 Cookies: {list(cookies.keys())}")
    print(f"📁 Output: {output_dir}\n")
    
    # Setup session
    session = requests.Session()
    session.cookies.update(cookies)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': base_url,
    })
    
    # Try API endpoint
    api_url = urljoin(base_url, '/api/v1/challenges')
    print(f"🔗 Fetching: {api_url}")
    
    try:
        response = session.get(api_url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        time.sleep(0.5)
        
        if not data.get('success'):
            print("❌ API returned success=false")
            sys.exit(1)
        
        challenges = data.get('data', [])
        print(f"✅ Found {len(challenges)} challenges!\n")
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        sys.exit(1)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Process challenges
    success_count = 0
    error_count = 0
    
    for i, chall in enumerate(challenges, 1):
        try:
            chall_id = chall.get('id')
            name = chall.get('name', 'Unknown')
            category = chall.get('category', 'Misc')
            
            print(f"[{i}/{len(challenges)}] {name} [{category}]")
            
            # Get details
            detail_url = urljoin(base_url, f'/api/v1/challenges/{chall_id}')
            detail_response = session.get(detail_url, timeout=30)
            time.sleep(0.5)
            
            if detail_response.status_code != 200:
                print(f"  ⚠️  Failed (HTTP {detail_response.status_code})")
                error_count += 1
                continue
            
            detail_data = detail_response.json()
            if not detail_data.get('success'):
                print(f"  ⚠️  API error")
                error_count += 1
                continue
            
            chall_detail = detail_data.get('data', {})
            description = chall_detail.get('description', 'No description')
            value = chall_detail.get('value', 0)
            tags = [t.get('value', '') for t in chall.get('tags', [])]
            
            # Detect category
            final_category = detect_category(name, tags, category)
            
            # Create folders
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
            
            print(f"  ✅ Saved")
            
            # Download files
            files = chall_detail.get('files', [])
            if files:
                print(f"  📥 {len(files)} file(s)...")
                for file_path in files:
                    try:
                        file_url = urljoin(base_url, file_path)
                        file_name = file_url.split('/')[-1].split('?')[0]
                        safe_file_name = sanitize_filename(file_name)
                        
                        file_response = session.get(file_url, stream=True, timeout=30)
                        file_response.raise_for_status()
                        
                        file_dest = files_path / safe_file_name
                        with open(file_dest, 'wb') as f:
                            for chunk in file_response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        
                        print(f"    ✅ {safe_file_name}")
                        time.sleep(0.3)
                    except Exception as e:
                        print(f"    ❌ {file_name}: {e}")
            
            success_count += 1
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            error_count += 1
    
    print(f"\n{'='*70}")
    print(f"✅ Success: {success_count}/{len(challenges)}")
    print(f"❌ Errors: {error_count}")
    print(f"📁 Output: {output_path / ctf_name}")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
