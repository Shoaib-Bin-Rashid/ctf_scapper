#!/usr/bin/env python3
"""
picoCTF Scraper
Downloads challenges from play.picoctf.org
"""

import requests
import json
from pathlib import Path
import re
import sys
import time

def sanitize_filename(filename):
    """Remove special characters from filename"""
    return re.sub(r'[<>:"/\\|?*]', '_', filename).strip()

def detect_category(category_name):
    """Map picoCTF category to folder name"""
    mapping = {
        'Web Exploitation': 'Web',
        'Binary Exploitation': 'Pwn',
        'Reverse Engineering': 'Reverse',
        'Cryptography': 'Crypto',
        'Forensics': 'Forensics',
        'General Skills': 'General',
    }
    return mapping.get(category_name, category_name.replace(' ', '-'))

def interactive_mode():
    """Interactive cookie collection"""
    print("\n" + "="*60)
    print("🍪 picoCTF Cookie Collection")
    print("="*60)
    print("\nHow to get cookies from Browser:")
    print("1. Go to https://play.picoctf.org/practice")
    print("2. Press F12 → Network tab → Refresh page")
    print("3. Click any request → Request Headers → Copy 'cookie' value")
    print("\nExample:")
    print("  cf_clearance=xxx...; csrftoken=yyy...; sessionid=zzz...")
    print("="*60 + "\n")
    
    cookies_str = input("Paste your cookies here: ").strip()
    if not cookies_str:
        print("❌ No cookies provided!")
        sys.exit(1)
    
    output_dir = input("\nOutput folder [./picoctf_download]: ").strip()
    if not output_dir:
        output_dir = "./picoctf_download"
    
    return cookies_str, output_dir

def main():
    print("\n" + "="*60)
    print("🎯 picoCTF Challenge Scraper")
    print("="*60 + "\n")
    
    # Parse arguments
    if len(sys.argv) < 2:
        # Interactive mode
        cookies_str, output_dir = interactive_mode()
    else:
        cookies_str = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "./picoctf_download"
    
    # Parse cookies
    cookies = {}
    for cookie in cookies_str.split('; '):
        if '=' in cookie:
            key, value = cookie.split('=', 1)
            cookies[key] = value
    
    print(f"🍪 Cookies: {list(cookies.keys())}")
    print(f"📁 Output directory: {output_dir}\n")
    
    # Create session
    session = requests.Session()
    session.cookies.update(cookies)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Referer': 'https://play.picoctf.org/practice',
        'X-CSRFToken': cookies.get('csrftoken', ''),
    })
    
    # Get total count
    print("🔗 Fetching challenges from picoCTF...")
    try:
        first_page = session.get('https://play.picoctf.org/api/challenges', timeout=30)
        first_page.raise_for_status()
        first_data = first_page.json()
        
        total_count = first_data.get('count', 0)
        per_page = len(first_data.get('results', []))
        total_pages = (total_count // per_page) + 1
        
        print(f"✅ Found {total_count} challenges across {total_pages} pages!\n")
        
    except Exception as e:
        print(f"❌ Failed to fetch challenges: {e}")
        sys.exit(1)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Fetch all challenges
    all_challenges = []
    for page in range(1, total_pages + 1):
        print(f"📄 Fetching page {page}/{total_pages}...")
        try:
            response = session.get(f'https://play.picoctf.org/api/challenges?page={page}', timeout=30)
            response.raise_for_status()
            page_data = response.json()
            all_challenges.extend(page_data.get('results', []))
            time.sleep(0.3)  # Rate limiting
        except Exception as e:
            print(f"⚠️  Error fetching page {page}: {e}")
    
    print(f"\n✅ Collected {len(all_challenges)} challenges!\n")
    
    # Process challenges
    success_count = 0
    skipped_count = 0
    
    for i, chall in enumerate(all_challenges, 1):
        try:
            name = chall.get('name', 'Unknown')
            category_obj = chall.get('category', {})
            category = category_obj.get('name', 'Misc') if isinstance(category_obj, dict) else str(category_obj)
            difficulty = chall.get('difficulty', 'Unknown')
            author = chall.get('author', 'Unknown')
            event = chall.get('event', {})
            event_name = event.get('name', 'picoCTF') if isinstance(event, dict) else 'picoCTF'
            
            print(f"[{i}/{len(all_challenges)}] {name} [{category}]")
            
            # Detect category
            final_category = detect_category(category)
            
            # Create folder structure
            safe_name = sanitize_filename(name)
            challenge_path = output_path / event_name / final_category / safe_name
            challenge_path.mkdir(parents=True, exist_ok=True)
            
            # Save statement (basic info)
            statement = f"Challenge: {name}\n"
            statement += f"Category: {category}\n"
            statement += f"Difficulty: {difficulty}\n"
            statement += f"Author: {author}\n"
            statement += f"Event: {event_name}\n"
            statement += f"Solved by: {chall.get('users_solved', 0)} users\n"
            statement += f"\nNote: picoCTF API does not expose descriptions or files.\n"
            statement += f"Visit: https://play.picoctf.org/practice/challenge/{chall.get('id')}\n"
            
            statement_file = challenge_path / 'statement.txt'
            with open(statement_file, 'w', encoding='utf-8') as f:
                f.write(statement)
            
            print(f"  ✅ Saved basic info")
            success_count += 1
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            skipped_count += 1
    
    print(f"\n{'='*60}")
    print(f"✅ Successfully processed: {success_count}/{len(all_challenges)}")
    print(f"⚠️  Skipped: {skipped_count}")
    print(f"📁 Output directory: {output_path}")
    print(f"\nℹ️  Note: picoCTF doesn't expose full descriptions/files via API.")
    print(f"   Challenge info saved with links to view online.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
