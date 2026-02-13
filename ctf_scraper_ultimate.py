#!/usr/bin/env python3
"""
Ultimate Universal CTF Scraper
Auto-detects platform type and scrapes accordingly
Works with: CTFd, picoCTF, and other platforms

Usage:
    python3 ctf_scraper_ultimate.py "URL" "COOKIES" ./output
    
Example:
    python3 ctf_scraper_ultimate.py "https://ctf.0xfun.org/challenges" "session=XXX; cf_clearance=YYY" ./0xfun
    python3 ctf_scraper_ultimate.py "https://play.picoctf.org/practice" "sessionid=XXX; csrftoken=YYY" ./pico
"""

import sys
import os
import re
import json
import time
from pathlib import Path
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup


class UniversalCTFScraper:
    def __init__(self, url, cookies_str, output_dir):
        self.url = url
        self.cookies_str = cookies_str
        self.output_dir = Path(output_dir)
        self.session = requests.Session()
        
        # Parse cookies
        self.cookies = {}
        for cookie in cookies_str.split(';'):
            cookie = cookie.strip()
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                self.cookies[key.strip()] = value.strip()
        
        self.session.cookies.update(self.cookies)
        
        # Extract base URL and domain
        parsed = urlparse(url)
        self.base_url = f"{parsed.scheme}://{parsed.netloc}"
        self.domain = parsed.netloc
        
        # Set up headers (full browser simulation for Cloudflare bypass)
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': self.base_url,
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Sec-Ch-Ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Upgrade-Insecure-Requests': '1',
            'Priority': 'u=0, i'
        })
        
        # Auto-detect CTF name
        self.ctf_name = self._extract_ctf_name()
        
    def _extract_ctf_name(self):
        """Extract CTF name from domain"""
        domain_parts = self.domain.split('.')
        if 'picoctf' in self.domain:
            return 'PICOCTF'
        elif len(domain_parts) >= 2:
            return domain_parts[-2].upper().replace('-', '_')
        return 'CTF'
    
    def detect_platform(self):
        """Auto-detect the platform type"""
        print(f"🔍 Detecting platform type for {self.domain}...")
        
        # Check for picoCTF
        if 'picoctf' in self.domain.lower():
            print("✅ Detected: picoCTF platform")
            return 'picoctf'
        
        # Check for CTFd by trying the API endpoint
        try:
            api_url = urljoin(self.base_url, '/api/v1/challenges')
            resp = self.session.get(api_url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if 'success' in data or 'data' in data:
                    print("✅ Detected: CTFd platform")
                    return 'ctfd'
        except Exception as e:
            pass
        
        # Check for specific API patterns
        try:
            # Try picoCTF API even if domain doesn't match
            api_url = urljoin(self.base_url, '/api/challenges')
            resp = self.session.get(api_url, timeout=10)
            if resp.status_code == 200 and isinstance(resp.json(), list):
                print("✅ Detected: picoCTF-style platform")
                return 'picoctf'
        except Exception:
            pass
        
        print("⚠️  Using generic HTML scraper (platform type unknown)")
        return 'generic'
    
    def scrape_ctfd(self):
        """Scrape CTFd-based platform"""
        print(f"\n🎯 Scraping CTFd platform: {self.domain}")
        print("=" * 60)
        
        api_url = urljoin(self.base_url, '/api/v1/challenges')
        
        try:
            resp = self.session.get(api_url, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            
            if not data.get('success'):
                print(f"❌ API returned success=false")
                return
            
            challenges = data.get('data', [])
            print(f"📦 Found {len(challenges)} challenges\n")
            
            success_count = 0
            
            for idx, challenge in enumerate(challenges, 1):
                try:
                    chal_id = challenge.get('id')
                    name = challenge.get('name', 'Unknown')
                    category = challenge.get('category', 'Misc')
                    
                    print(f"[{idx}/{len(challenges)}] {name} ({category})")
                    
                    # Get detailed challenge info
                    detail_url = urljoin(self.base_url, f'/api/v1/challenges/{chal_id}')
                    detail_resp = self.session.get(detail_url, timeout=30)
                    detail_resp.raise_for_status()
                    detail_data = detail_resp.json()
                    
                    if not detail_data.get('success'):
                        print(f"  ⚠️  Failed to get details")
                        continue
                    
                    chal_detail = detail_data.get('data', {})
                    
                    # Create category folder
                    category_folder = self.output_dir / self._sanitize_filename(category)
                    challenge_folder = category_folder / self._sanitize_filename(name)
                    challenge_folder.mkdir(parents=True, exist_ok=True)
                    
                    # Save challenge info
                    info = {
                        'name': name,
                        'category': category,
                        'description': chal_detail.get('description', ''),
                        'points': chal_detail.get('value', 0),
                        'solves': chal_detail.get('solves', 0),
                        'tags': chal_detail.get('tags', []),
                        'files': chal_detail.get('files', [])
                    }
                    
                    # Write info file
                    with open(challenge_folder / 'challenge.txt', 'w', encoding='utf-8') as f:
                        f.write(f"Challenge: {name}\n")
                        f.write(f"Category: {category}\n")
                        f.write(f"Points: {info['points']}\n")
                        f.write(f"Solves: {info['solves']}\n")
                        if info['tags']:
                            f.write(f"Tags: {', '.join(info['tags'])}\n")
                        f.write(f"\nDescription:\n{info['description']}\n")
                        if info['files']:
                            f.write(f"\nFiles:\n")
                            for file_url in info['files']:
                                f.write(f"  - {file_url}\n")
                    
                    # Download files
                    files = chal_detail.get('files', [])
                    if files:
                        print(f"  📥 Downloading {len(files)} file(s)...")
                        for file_url in files:
                            try:
                                file_full_url = urljoin(self.base_url, file_url)
                                file_name = file_url.split('/')[-1].split('?')[0]
                                file_path = challenge_folder / file_name
                                
                                file_resp = self.session.get(file_full_url, timeout=30)
                                file_resp.raise_for_status()
                                
                                with open(file_path, 'wb') as f:
                                    f.write(file_resp.content)
                                print(f"     ✓ {file_name}")
                            except Exception as e:
                                print(f"     ✗ Failed to download {file_name}: {e}")
                    
                    print(f"  ✅ Saved to {challenge_folder}")
                    success_count += 1
                    
                    # Rate limiting
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"  ❌ Error: {e}")
                    continue
            
            print(f"\n{'='*60}")
            print(f"✅ Successfully scraped {success_count}/{len(challenges)} challenges")
            print(f"📂 Output: {self.output_dir}")
            
        except Exception as e:
            print(f"❌ Error scraping CTFd platform: {e}")
    
    def scrape_picoctf(self):
        """Scrape picoCTF platform"""
        print(f"\n🎯 Scraping picoCTF: {self.domain}")
        print("=" * 60)
        
        all_challenges = []
        page = 1
        
        # Fetch all pages
        while True:
            api_url = urljoin(self.base_url, f'/api/challenges/?page={page}')
            print(f"📄 Fetching page {page}...")
            
            try:
                resp = self.session.get(api_url, timeout=30)
                resp.raise_for_status()
                data = resp.json()
                
                # Check if it's the new paginated format
                if isinstance(data, dict) and 'results' in data:
                    results = data['results']
                    all_challenges.extend(results)
                    print(f"   Found {len(results)} challenges")
                    
                    # Check if there's a next page
                    if not data.get('next'):
                        break
                elif isinstance(data, list):
                    # Old format (list of challenges)
                    if not data:
                        break
                    all_challenges.extend(data)
                    print(f"   Found {len(data)} challenges")
                    
                    if len(data) < 100:  # Last page
                        break
                else:
                    print(f"⚠️  Unexpected response format")
                    break
                
                page += 1
                time.sleep(0.5)
                
            except Exception as e:
                print(f"⚠️  Error on page {page}: {e}")
                break
        
        print(f"\n📦 Total challenges found: {len(all_challenges)}\n")
        
        success_count = 0
        
        for idx, challenge in enumerate(all_challenges, 1):
            try:
                name = challenge.get('name', 'Unknown')
                
                # Handle category (can be string or dict)
                category = challenge.get('category', 'Misc')
                if isinstance(category, dict):
                    category = category.get('name', 'Misc')
                
                print(f"[{idx}/{len(all_challenges)}] {name} ({category})")
                
                # Create folder structure
                category_folder = self.output_dir / self._sanitize_filename(category)
                challenge_folder = category_folder / self._sanitize_filename(name)
                challenge_folder.mkdir(parents=True, exist_ok=True)
                
                # Handle event (can be string or dict)
                event = challenge.get('event', 'Unknown')
                if isinstance(event, dict):
                    event = event.get('name', 'Unknown')
                
                # Handle tags (can be list of strings or list of dicts)
                tags = challenge.get('tags', [])
                if tags and isinstance(tags[0], dict):
                    tags = [tag.get('name', '') for tag in tags]
                
                # Save challenge info
                with open(challenge_folder / 'challenge.txt', 'w', encoding='utf-8') as f:
                    f.write(f"Challenge: {name}\n")
                    f.write(f"Category: {category}\n")
                    f.write(f"Difficulty: {challenge.get('difficulty', 'N/A')}\n")
                    f.write(f"Event: {event}\n")
                    f.write(f"Author: {challenge.get('author', 'N/A')}\n")
                    if tags:
                        f.write(f"Tags: {', '.join(tags)}\n")
                    f.write(f"\nChallenge ID: {challenge.get('id', 'N/A')}\n")
                    
                    # Note: picoCTF API doesn't expose full descriptions in list view
                    f.write(f"\nNote: Login to https://play.picoctf.org to view full description\n")
                
                print(f"  ✅ Saved to {challenge_folder}")
                success_count += 1
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        print(f"\n{'='*60}")
        print(f"✅ Successfully scraped {success_count}/{len(all_challenges)} challenges")
        print(f"📂 Output: {self.output_dir}")
    
    def scrape_generic(self):
        """Generic HTML scraper for unknown platforms"""
        print(f"\n🎯 Using generic scraper for: {self.domain}")
        print("=" * 60)
        print("⚠️  This platform type is not fully supported yet.")
        print("    The scraper will attempt basic HTML parsing.\n")
        
        try:
            resp = self.session.get(self.url, timeout=30)
            resp.raise_for_status()
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Save raw HTML for manual inspection
            output_file = self.output_dir / 'challenges_page.html'
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(resp.text)
            
            print(f"✅ Saved HTML to: {output_file}")
            print(f"\n💡 Please inspect the HTML and report the platform type")
            print(f"   so we can add proper support for it!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def scrape(self):
        """Main scraping method - auto-detects and scrapes"""
        platform = self.detect_platform()
        
        if platform == 'ctfd':
            self.scrape_ctfd()
        elif platform == 'picoctf':
            self.scrape_picoctf()
        else:
            self.scrape_generic()
    
    @staticmethod
    def _sanitize_filename(filename):
        """Sanitize filename for safe filesystem usage"""
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = filename.strip('. ')
        return filename or 'unnamed'


def show_help():
    """Display help message"""
    help_text = """
╔══════════════════════════════════════════════════════════════════╗
║           🎯 ULTIMATE UNIVERSAL CTF SCRAPER 🎯                   ║
╚══════════════════════════════════════════════════════════════════╝

📖 ONE TOOL FOR ALL PLATFORMS!

✅ Auto-detects: CTFd, picoCTF, and other platforms
✅ Downloads: Challenge statements and files
✅ Organizes: Categorized folder structure

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 USAGE:

    python3 ctf_scraper_ultimate.py "URL" "COOKIES" ./output

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 HOW TO GET COOKIES:

1. Open browser DevTools (F12)
2. Go to Network tab
3. Load the challenges page
4. Right-click any request → Copy → Copy as cURL
5. Find the part after -b or --cookie

Example cURL output:
    curl 'https://ctf.0xfun.org/challenges' \\
      -b 'session=XXX; cf_clearance=YYY'
         ↑_________________________↑
         Copy this part (the cookies)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 EXAMPLES:

# CTFd platform (0xFun)
python3 ctf_scraper_ultimate.py \\
  "https://ctf.0xfun.org/challenges" \\
  "session=abc123; cf_clearance=xyz789" \\
  ./0xfun_output

# picoCTF
python3 ctf_scraper_ultimate.py \\
  "https://play.picoctf.org/practice" \\
  "sessionid=abc123; csrftoken=xyz789" \\
  ./picoctf_output

# HackTheBox CTF
python3 ctf_scraper_ultimate.py \\
  "https://ctf.hackthebox.com/challenges" \\
  "session=abc123" \\
  ./htb_output

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  IMPORTANT:

✓ ALWAYS quote the URL (especially if it has ? or & characters)
✓ ALWAYS quote the cookies (they contain ; and = characters)
✓ Get FRESH cookies (they expire in 5-10 minutes!)
✓ Make sure you're logged in before copying cookies

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 SUPPORTED PLATFORMS:

✅ CTFd-based (most CTF competitions)
✅ picoCTF
⚠️  Others (basic HTML scraping)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 MORE HELP:

    cat GET_FRESH_COOKIES.md      # Cookie extraction guide
    cat WHICH_SCRAPER_TO_USE.md   # Platform selection guide
    cat WHY_NOT_WORKING.md        # Troubleshooting

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    print(help_text)


def main():
    if len(sys.argv) == 1 or '--help' in sys.argv or '-h' in sys.argv:
        show_help()
        sys.exit(0)
    
    if len(sys.argv) != 4:
        print("❌ Error: Invalid number of arguments\n")
        print("Usage: python3 ctf_scraper_ultimate.py \"URL\" \"COOKIES\" ./output")
        print("\nFor help: python3 ctf_scraper_ultimate.py --help")
        sys.exit(1)
    
    url = sys.argv[1]
    cookies = sys.argv[2]
    output_dir = sys.argv[3]
    
    print("\n" + "="*60)
    print("🎯 ULTIMATE UNIVERSAL CTF SCRAPER")
    print("="*60)
    print(f"URL: {url}")
    print(f"Output: {output_dir}")
    print("="*60 + "\n")
    
    try:
        scraper = UniversalCTFScraper(url, cookies, output_dir)
        scraper.scrape()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
