#!/usr/bin/env python3
"""
Ultimate Universal CTF Scraper v2.0
Auto-detects platform type and scrapes accordingly
Works with: CTFd, picoCTF, and other platforms

Features:
- Secure cookie handling (env vars, file input, Cookie Editor extension)
- Concurrent downloads with progress bars
- Resume capability with state tracking
- Playwright browser fallback when API fails
- Comprehensive error handling and retry logic

Usage:
    python3 ctf_scraper.py "URL" [OPTIONS]

Examples:
    # Using Cookie Editor extension (EASIEST)
    python3 ctf_scraper.py "https://ctf.0xfun.org/challenges" -c "session=XXX; cf_clearance=YYY" ./output

    # Using environment variable (RECOMMENDED for security)
    export CTF_COOKIES="session=XXX; cf_clearance=YYY"
    python3 ctf_scraper.py "https://ctf.0xfun.org/challenges" ./output

    # Using cookies from file
    python3 ctf_scraper.py "https://ctf.0xfun.org/challenges" -c @cookies.txt ./output

    # Dry run to preview
    python3 ctf_scraper.py "URL" --dry-run ./output

    # Browser fallback mode (manual login, no cookies needed)
    python3 ctf_scraper.py --browser "https://ctf.example.com" ./output
"""

import sys
import os
import re
import json
import time
import logging
import threading
from pathlib import Path
from urllib.parse import urlparse, urljoin
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import argparse

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class ScraperState:
    """Manages scraper state for resume capability"""
    
    def __init__(self, state_file: Path):
        self.state_file = state_file
        self.state = self._load()
    
    def _load(self) -> Dict:
        """Load state from file"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                # JSON serializes sets as lists — convert back to sets
                data['completed_challenges'] = set(data.get('completed_challenges', []))
                data['failed_challenges'] = set(data.get('failed_challenges', []))
                return data
            except Exception as e:
                logging.warning(f"Failed to load state: {e}")
        return {
            'completed_challenges': set(),
            'failed_challenges': set(),
            'last_run': None,
            'platform': None
        }
    
    def save(self):
        """Save state to file"""
        try:
            # Convert sets to lists for JSON serialization
            save_data = self.state.copy()
            save_data['completed_challenges'] = list(self.state['completed_challenges'])
            save_data['failed_challenges'] = list(self.state['failed_challenges'])
            save_data['last_run'] = datetime.now().isoformat()
            
            with open(self.state_file, 'w') as f:
                json.dump(save_data, f, indent=2)
        except Exception as e:
            logging.error(f"Failed to save state: {e}")
    
    def is_completed(self, challenge_id: str) -> bool:
        """Check if challenge is already completed"""
        return challenge_id in self.state['completed_challenges']
    
    def mark_completed(self, challenge_id: str):
        """Mark challenge as completed"""
        self.state['completed_challenges'].add(challenge_id)
        if challenge_id in self.state.get('failed_challenges', set()):
            self.state['failed_challenges'].remove(challenge_id)
        self.save()
    
    def mark_failed(self, challenge_id: str):
        """Mark challenge as failed"""
        self.state['failed_challenges'].add(challenge_id)
        self.save()


class UniversalCTFScraper:
    def __init__(self, url: str, cookies_str: Optional[str], output_dir: str, 
                 skip_existing: bool = False, dry_run: bool = False,
                 max_workers: int = 10, timeout: int = 30, verbose: bool = False):
        self.url = url
        self.output_dir = Path(output_dir)
        self.skip_existing = skip_existing
        self.dry_run = dry_run
        self.max_workers = max_workers
        self.timeout = timeout
        
        # Setup logging
        log_level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize session
        self.session = requests.Session()
        
        # Parse and set cookies
        if cookies_str:
            self.cookies = self._parse_cookies(cookies_str)
            self.session.cookies.update(self.cookies)
        else:
            self.cookies = {}
        
        # Extract base URL and domain
        parsed = urlparse(url)
        self.base_url = f"{parsed.scheme}://{parsed.netloc}"
        self.domain = parsed.netloc
        
        # Set up headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            'Accept': 'application/json,text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': self.base_url,
        })
        
        # State management
        self.state = ScraperState(self.output_dir / '.scraper_state.json')
        
        # Thread safety for stats and state
        self._lock = threading.Lock()
        
        # Statistics
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'downloaded_files': 0,
            'failed_files': 0
        }
    
    def _parse_cookies(self, cookies_str: str) -> Dict[str, str]:
        """Parse cookies from string, file, or environment variable"""
        # Check if it's a file reference (@file.txt)
        if cookies_str.startswith('@'):
            file_path = Path(cookies_str[1:])
            if file_path.exists():
                with open(file_path, 'r') as f:
                    cookies_str = f.read().strip()
            else:
                self.logger.error(f"Cookie file not found: {file_path}")
                sys.exit(1)
        
        # Parse cookie string
        cookies = {}
        for cookie in cookies_str.split(';'):
            cookie = cookie.strip()
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookies[key.strip()] = value.strip()
        
        return cookies
    
    def detect_platform(self) -> str:
        """Auto-detect the platform type"""
        self.logger.info(f"🔍 Detecting platform type for {self.domain}...")
        
        # Check for picoCTF
        if 'picoctf' in self.domain.lower():
            self.logger.info("✅ Detected: picoCTF platform")
            return 'picoctf'
        
        # Check for CTFd by trying the API endpoint
        try:
            api_url = urljoin(self.base_url, '/api/v1/challenges')
            resp = self.session.get(api_url, timeout=self.timeout)
            if resp.status_code == 200:
                # Ensure we have content before trying to parse JSON
                if resp.content:
                    data = resp.json()
                    if 'success' in data or 'data' in data:
                        self.logger.info("✅ Detected: CTFd platform")
                        return 'ctfd'
        except requests.exceptions.RequestException as e:
            self.logger.debug(f"CTFd detection failed (network): {e}")
        except json.JSONDecodeError as e:
            self.logger.debug(f"CTFd detection failed (json): {e}")
        
        # Check for picoCTF API even if domain doesn't match
        try:
            api_url = urljoin(self.base_url, '/api/challenges')
            resp = self.session.get(api_url, timeout=self.timeout)
            if resp.status_code == 200 and isinstance(resp.json(), (list, dict)):
                self.logger.info("✅ Detected: picoCTF-style platform")
                return 'picoctf'
        except Exception:
            pass
        
        self.logger.warning("⚠️  Platform type unknown - will try browser fallback")
        return 'unknown'
    
    def scrape_ctfd(self) -> bool:
        """Scrape CTFd-based platform"""
        self.logger.info(f"\n🎯 Scraping CTFd platform: {self.domain}")
        print("=" * 60)
        
        api_url = urljoin(self.base_url, '/api/v1/challenges')
        
        try:
            resp = self.session.get(api_url, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            
            if not data.get('success'):
                self.logger.error("❌ API returned success=false")
                return False
            
            challenges = data.get('data', [])
            self.stats['total'] = len(challenges)
            self.logger.info(f"📦 Found {len(challenges)} challenges\n")
            
            if self.dry_run:
                print("🔍 DRY RUN - Preview of challenges:")
                for chal in challenges[:10]:
                    print(f"  • {chal.get('name')} ({chal.get('category')})")
                if len(challenges) > 10:
                    print(f"  ... and {len(challenges) - 10} more")
                return True

            # Process challenges concurrently with progress bar
            with tqdm(total=len(challenges), desc="Overall Progress", unit="chal") as pbar:
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = {
                        executor.submit(self._process_ctfd_challenge, c): c
                        for c in challenges
                    }
                    for future in as_completed(futures):
                        result = future.result()
                        with self._lock:
                            if result:
                                self.stats['success'] += 1
                            else:
                                self.stats['failed'] += 1
                        pbar.update(1)
            
            self._print_summary()
            return True
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ Network error: {e}")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error scraping CTFd platform: {e}", exc_info=True)
            return False
    
    def _process_ctfd_challenge(self, challenge: Dict) -> bool:
        """Process a single CTFd challenge"""
        try:
            chal_id = str(challenge.get('id'))
            name = challenge.get('name', 'Unknown')
            category = challenge.get('category', 'Misc')

            # Check if already completed (thread-safe read via lock)
            if self.skip_existing and self.state.is_completed(chal_id):
                with self._lock:
                    self.stats['skipped'] += 1
                self.logger.debug(f"⏭️  Skipping {name} (already completed)")
                return True

            self.logger.info(f"📥 Processing: {name} ({category})")

            # Get detailed challenge info with retry
            detail_data = self._fetch_with_retry(
                urljoin(self.base_url, f'/api/v1/challenges/{chal_id}')
            )

            if not detail_data or not detail_data.get('success'):
                self.logger.warning(f"  ⚠️  Failed to get details for {name}")
                with self._lock:
                    self.state.mark_failed(chal_id)
                return False

            chal_detail = detail_data.get('data', {})

            # Create folder structure
            category_folder = self.output_dir / self._sanitize_filename(category)
            challenge_folder = category_folder / self._sanitize_filename(name)
            challenge_folder.mkdir(parents=True, exist_ok=True)

            # Save challenge info
            self._save_challenge_info(challenge_folder, {
                'name': name,
                'category': category,
                'description': chal_detail.get('description', ''),
                'points': chal_detail.get('value', 0),
                'solves': chal_detail.get('solves', 0),
                'tags': chal_detail.get('tags', []),
                'files': chal_detail.get('files', [])
            })

            # Download files concurrently
            files = chal_detail.get('files', [])
            if files:
                self._download_files_concurrent(files, challenge_folder)

            with self._lock:
                self.state.mark_completed(chal_id)
            self.logger.info(f"  ✅ Saved to {challenge_folder}")
            return True

        except Exception as e:
            self.logger.error(f"  ❌ Error processing challenge: {e}", exc_info=True)
            if 'chal_id' in locals():
                with self._lock:
                    self.state.mark_failed(chal_id)
            return False
    
    def _fetch_with_retry(self, url: str, max_retries: int = 3) -> Optional[Dict]:
        """Fetch URL with retry logic"""
        for attempt in range(max_retries):
            try:
                resp = self.session.get(url, timeout=self.timeout)
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    self.logger.debug(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {e}")
                    time.sleep(wait_time)
                else:
                    self.logger.error(f"Failed after {max_retries} retries: {e}")
                    return None
        return None
    
    def _download_files_concurrent(self, files: List[str], output_folder: Path):
        """Download files concurrently with progress bar"""
        if not files:
            return
        
        self.logger.info(f"  📥 Downloading {len(files)} file(s)...")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._download_file, file_url, output_folder): file_url
                for file_url in files
            }
            
            for future in as_completed(futures):
                file_url = futures[future]
                try:
                    success = future.result()
                    with self._lock:
                        if success:
                            self.stats['downloaded_files'] += 1
                        else:
                            self.stats['failed_files'] += 1
                except Exception as e:
                    self.logger.error(f"     ✗ Error downloading {file_url}: {e}")
                    with self._lock:
                        self.stats['failed_files'] += 1
    
    def _download_file(self, file_url: str, output_folder: Path) -> bool:
        """Download a single file with verification"""
        try:
            file_full_url = urljoin(self.base_url, file_url)
            file_name = file_url.split('/')[-1].split('?')[0]
            file_path = output_folder / file_name
            
            # Skip if exists and skip_existing is enabled
            if self.skip_existing and file_path.exists():
                self.logger.debug(f"     ⏭️  {file_name} (exists)")
                return True
            
            # Download with retry
            for attempt in range(3):
                try:
                    resp = self.session.get(file_full_url, timeout=self.timeout * 2, stream=True)
                    resp.raise_for_status()
                    
                    # Get total size
                    total_size = int(resp.headers.get('Content-Length', 0))
                    
                    # Download with progress
                    with open(file_path, 'wb') as f:
                        if total_size > 0:
                            with tqdm(total=total_size, unit='B', unit_scale=True, 
                                    desc=f"     {file_name}", leave=False) as pbar:
                                for chunk in resp.iter_content(chunk_size=8192):
                                    f.write(chunk)
                                    pbar.update(len(chunk))
                        else:
                            for chunk in resp.iter_content(chunk_size=8192):
                                f.write(chunk)
                    
                    # Verify file size if Content-Length was provided
                    if total_size > 0 and file_path.stat().st_size != total_size:
                        self.logger.warning(f"     ⚠️  Size mismatch for {file_name}")
                        if attempt < 2:
                            continue
                    
                    self.logger.info(f"     ✓ {file_name}")
                    return True
                    
                except requests.exceptions.RequestException as e:
                    if attempt < 2:
                        time.sleep(2 ** attempt)
                        continue
                    raise
            
            return False
            
        except Exception as e:
            self.logger.error(f"     ✗ Failed to download {file_name}: {e}")
            return False
    
    def _save_challenge_info(self, folder: Path, info: Dict):
        """Save challenge information to file"""
        with open(folder / 'challenge.txt', 'w', encoding='utf-8') as f:
            f.write(f"Challenge: {info['name']}\n")
            f.write(f"Category: {info['category']}\n")
            f.write(f"Points: {info['points']}\n")
            f.write(f"Solves: {info['solves']}\n")
            if info['tags']:
                f.write(f"Tags: {', '.join(info['tags'])}\n")
            f.write(f"\nDescription:\n{info['description']}\n")
            if info['files']:
                f.write(f"\nFiles:\n")
                for file_url in info['files']:
                    f.write(f"  - {file_url}\n")
    
    def scrape_picoctf(self) -> bool:
        """Scrape picoCTF platform"""
        self.logger.info(f"\n🎯 Scraping picoCTF: {self.domain}")
        print("=" * 60)

        # --- Step 1: Fetch page 1 to get total count, then fetch remaining pages concurrently ---
        first_url = urljoin(self.base_url, '/api/challenges/?page=1')
        self.logger.info("📄 Fetching page 1...")
        try:
            resp = self.session.get(first_url, timeout=self.timeout)
            resp.raise_for_status()
            first_data = resp.json()
        except Exception as e:
            self.logger.error(f"❌ Failed to fetch page 1: {e}")
            return False

        all_challenges = []
        if isinstance(first_data, dict) and 'results' in first_data:
            all_challenges.extend(first_data['results'])
            total_count = first_data.get('count', 0)
            page_size = len(first_data['results'])
            total_pages = (total_count + page_size - 1) // page_size if page_size else 1
            self.logger.info(f"   Found {len(first_data['results'])} challenges (total: {total_count}, pages: {total_pages})")
        elif isinstance(first_data, list):
            all_challenges.extend(first_data)
            total_pages = 1
        else:
            self.logger.warning("⚠️  Unexpected response format")
            return False

        # Fetch remaining pages concurrently
        if total_pages > 1:
            def fetch_page(page_num):
                url = urljoin(self.base_url, f'/api/challenges/?page={page_num}')
                try:
                    r = self.session.get(url, timeout=self.timeout)
                    r.raise_for_status()
                    d = r.json()
                    if isinstance(d, dict) and 'results' in d:
                        return page_num, d['results']
                    elif isinstance(d, list):
                        return page_num, d
                except Exception as e:
                    self.logger.error(f"⚠️  Error on page {page_num}: {e}")
                return page_num, []

            pages_fetched = {1: all_challenges}
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {executor.submit(fetch_page, p): p for p in range(2, total_pages + 1)}
                for future in as_completed(futures):
                    page_num, results = future.result()
                    pages_fetched[page_num] = results
                    self.logger.info(f"📄 Page {page_num}: {len(results)} challenges")

            # Reassemble in order
            all_challenges = []
            for p in sorted(pages_fetched.keys()):
                all_challenges.extend(pages_fetched[p])

        self.stats['total'] = len(all_challenges)
        self.logger.info(f"\n📦 Total challenges found: {len(all_challenges)}\n")

        if self.dry_run:
            print("🔍 DRY RUN - Preview of challenges:")
            for chal in all_challenges[:10]:
                cat = chal.get('category', 'Misc')
                if isinstance(cat, dict):
                    cat = cat.get('name', 'Misc')
                print(f"  • {chal.get('name')} ({cat})")
            if len(all_challenges) > 10:
                print(f"  ... and {len(all_challenges) - 10} more")
            return True

        # --- Step 2: Process challenges concurrently ---
        with tqdm(total=len(all_challenges), desc="Overall Progress", unit="chal") as pbar:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {executor.submit(self._process_picoctf_challenge, c): c for c in all_challenges}
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        self.stats['success'] += 1
                    else:
                        self.stats['failed'] += 1
                    pbar.update(1)

        self._print_summary()
        return True
    
    def _process_picoctf_challenge(self, challenge: Dict) -> bool:
        """Process a single picoCTF challenge"""
        try:
            chal_id = str(challenge.get('id'))
            name = challenge.get('name', 'Unknown')
            
            # Handle category
            category = challenge.get('category', 'Misc')
            if isinstance(category, dict):
                category = category.get('name', 'Misc')
            
            # Check if already completed
            if self.skip_existing and self.state.is_completed(chal_id):
                with self._lock:
                    self.stats['skipped'] += 1
                return True
            
            # Create folder structure
            category_folder = self.output_dir / self._sanitize_filename(category)
            challenge_folder = category_folder / self._sanitize_filename(name)
            challenge_folder.mkdir(parents=True, exist_ok=True)
            
            # Handle event and tags
            event = challenge.get('event', 'Unknown')
            if isinstance(event, dict):
                event = event.get('name', 'Unknown')
            
            tags = challenge.get('tags', [])
            if tags and isinstance(tags[0], dict):
                tags = [tag.get('name', '') for tag in tags]
            
            # Fetch full challenge details from API
            description, hints, files_urls = self._fetch_picoctf_challenge_details_api(chal_id)
            challenge_url = urljoin(self.base_url, f'/practice/challenge/{self._sanitize_url_name(name)}')
            
            # Save challenge info
            with open(challenge_folder / 'challenge.txt', 'w', encoding='utf-8') as f:
                f.write(f"Challenge: {name}\n")
                f.write(f"Category: {category}\n")
                f.write(f"Difficulty: {challenge.get('difficulty', 'N/A')}\n")
                f.write(f"Points: {challenge.get('event_points', 'N/A')}\n")
                f.write(f"Solves: {challenge.get('users_solved', 'N/A')}\n")
                f.write(f"Event: {event}\n")
                f.write(f"Author: {challenge.get('author', 'N/A')}\n")
                if tags:
                    f.write(f"Tags: {', '.join(tags)}\n")
                f.write(f"\nChallenge ID: {chal_id}\n")
                f.write(f"URL: {challenge_url}\n")
                
                # Add description
                if description:
                    f.write(f"\n{'='*60}\n")
                    f.write(f"DESCRIPTION\n")
                    f.write(f"{'='*60}\n")
                    f.write(description)
                    f.write(f"\n")
                
                # Add hints if available
                if hints:
                    f.write(f"\n{'='*60}\n")
                    f.write(f"HINTS\n")
                    f.write(f"{'='*60}\n")
                    for i, hint in enumerate(hints, 1):
                        f.write(f"{i}. {hint}\n")
            
            # Download files
            if files_urls:
                files_folder = challenge_folder / 'files'
                files_folder.mkdir(exist_ok=True)
                for file_url in files_urls:
                    self._download_file(file_url, files_folder)
            
            with self._lock:
                self.state.mark_completed(chal_id)
            return True
            
        except Exception as e:
            self.logger.error(f"  ❌ Error: {e}")
            return False
    
    def _sanitize_url_name(self, name: str) -> str:
        """Convert challenge name to URL-friendly format"""
        # picoCTF uses lowercase with hyphens
        return name.lower().replace(' ', '-').replace('_', '-')
    
    def _fetch_picoctf_challenge_details_api(self, challenge_id: str) -> Tuple[str, List[str], List[str]]:
        """Fetch full challenge details from picoCTF instance API"""
        try:
            api_url = urljoin(self.base_url, f'/api/challenges/{challenge_id}/instance/')
            resp = self.session.get(api_url, timeout=self.timeout)
            if resp.status_code != 200:
                self.logger.debug(f"  ⚠️  Instance API returned {resp.status_code} for challenge {challenge_id}")
                return "", [], []

            data = resp.json()

            # Parse description HTML -> plain text and extract file links
            description = ""
            file_urls = []
            raw_desc = data.get('description', '') or ''
            if raw_desc:
                soup = BeautifulSoup(raw_desc, 'html.parser')
                # Extract file download links before stripping HTML
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href and href not in file_urls:
                        file_urls.append(href)
                description = soup.get_text(separator='\n', strip=True)

            # Parse hints HTML -> plain text
            hints = []
            for hint in data.get('hints', []):
                if isinstance(hint, str) and hint:
                    hint_text = BeautifulSoup(hint, 'html.parser').get_text(strip=True)
                    if hint_text:
                        hints.append(hint_text)
                elif isinstance(hint, dict):
                    raw = hint.get('hint', hint.get('body', hint.get('text', '')))
                    if raw:
                        hints.append(BeautifulSoup(raw, 'html.parser').get_text(strip=True))

            return description, hints, file_urls

        except Exception as e:
            self.logger.debug(f"  ⚠️  Error fetching challenge details from API: {e}")
            return "", [], []

    def _print_summary(self):
        """Print scraping summary"""
        print(f"\n{'='*60}")
        print("📊 SCRAPING SUMMARY")
        print(f"{'='*60}")
        print(f"Total Challenges: {self.stats['total']}")
        print(f"✅ Success: {self.stats['success']}")
        print(f"❌ Failed: {self.stats['failed']}")
        print(f"⏭️  Skipped: {self.stats['skipped']}")
        print(f"📥 Files Downloaded: {self.stats['downloaded_files']}")
        print(f"❌ Files Failed: {self.stats['failed_files']}")
        print(f"{'='*60}")
        print(f"📂 Output: {self.output_dir}")
    
    def scrape(self) -> bool:
        """Main scraping method - auto-detects and scrapes"""
        platform = self.detect_platform()
        self.state.state['platform'] = platform
        
        if platform == 'ctfd':
            return self.scrape_ctfd()
        elif platform == 'picoctf':
            return self.scrape_picoctf()
        else:
            return False
    
    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe filesystem usage"""
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = filename.strip('. ')
        return filename or 'unnamed'


class BrowserFallbackScraper:
    """Playwright-based browser scraper for when API methods fail"""
    
    def __init__(self, url: str, output_dir: str, verbose: bool = False):
        self.url = url
        self.output_dir = Path(output_dir)
        self.verbose = verbose
        
        # Setup logging
        log_level = logging.DEBUG if verbose else logging.INFO
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
    
    def scrape_with_browser(self) -> bool:
        """Open browser, wait for user to login, then scrape"""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("\n❌ Playwright not installed!")
            print("Install it with: pip install playwright && playwright install chromium")
            return False
        
        print("\n" + "="*60)
        print("🌐 BROWSER FALLBACK MODE")
        print("="*60)
        print("\n📖 Instructions:")
        print("  1. Browser will open automatically")
        print("  2. Log in to the CTF platform if needed")
        print("  3. Navigate to the challenges page")
        print("  4. Press ENTER in this terminal when ready")
        print("  5. The scraper will extract all visible challenges")
        print("\n⚠️  Note: Keep the browser window open until scraping completes!")
        
        input("\n➡️  Press ENTER to open browser...")
        
        try:
            with sync_playwright() as p:
                # Launch browser in headed mode
                browser = p.chromium.launch(headless=False)
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                )
                page = context.new_page()
                
                # Navigate to URL
                print(f"\n🌐 Opening: {self.url}")
                page.goto(self.url, wait_until='networkidle')
                
                print("\n✅ Browser opened!")
                print("👉 Please log in and navigate to the challenges page")
                
                input("\n➡️  Press ENTER when you're on the challenges page and ready to scrape...")
                
                # Get current URL to detect platform
                current_url = page.url
                print(f"\n🔍 Current URL: {current_url}")
                
                # Detect platform from current page
                platform = self._detect_platform_from_page(page, current_url)
                print(f"✅ Detected platform: {platform}")
                
                # Extract cookies for potential API calls
                cookies = context.cookies()
                cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
                
                # Try API scraping with extracted cookies first
                if platform in ['ctfd', 'picoctf']:
                    print("\n🔄 Attempting API scraping with browser cookies...")
                    parsed = urlparse(current_url)
                    base_url = f"{parsed.scheme}://{parsed.netloc}"
                    
                    scraper = UniversalCTFScraper(
                        url=base_url + ('/challenges' if 'challenges' not in current_url else ''),
                        cookies_str=cookie_str,
                        output_dir=str(self.output_dir),
                        verbose=self.verbose
                    )
                    
                    if scraper.scrape():
                        print("\n✅ API scraping successful!")
                        browser.close()
                        return True
                    else:
                        print("\n⚠️  API scraping failed, falling back to HTML parsing...")
                
                # Fallback to HTML scraping
                print("\n🔄 Scraping challenges from current page...")
                challenges = self._scrape_from_html(page, platform)
                
                if challenges:
                    print(f"\n✅ Found {len(challenges)} challenges")
                    self._save_challenges(challenges)
                    print(f"📂 Saved to: {self.output_dir}")
                else:
                    print("\n⚠️  No challenges found on this page")
                
                print("\n✅ You can close the browser now")
                input("➡️  Press ENTER to close browser and exit...")
                
                browser.close()
                return len(challenges) > 0
                
        except Exception as e:
            self.logger.error(f"❌ Browser scraping failed: {e}", exc_info=True)
            return False
    
    def _detect_platform_from_page(self, page, url: str) -> str:
        """Detect platform type from current page"""
        try:
            # Check URL patterns
            if 'picoctf' in url.lower():
                return 'picoctf'
            
            # Check page content
            content = page.content()
            if 'CTFd' in content or '/api/v1/challenges' in content:
                return 'ctfd'
            
            # Try to detect by checking for specific elements
            if page.query_selector('[data-ctfd]') or page.query_selector('.challenge-button'):
                return 'ctfd'
            
        except Exception as e:
            self.logger.debug(f"Platform detection error: {e}")
        
        return 'unknown'
    
    def _scrape_from_html(self, page, platform: str) -> List[Dict]:
        """Scrape challenges from HTML"""
        challenges = []
        
        try:
            if platform == 'ctfd':
                challenges = self._scrape_ctfd_html(page)
            elif platform == 'picoctf':
                challenges = self._scrape_picoctf_html(page)
            else:
                challenges = self._scrape_generic_html(page)
        except Exception as e:
            self.logger.error(f"HTML scraping error: {e}", exc_info=True)
        
        return challenges
    
    def _scrape_ctfd_html(self, page) -> List[Dict]:
        """Scrape CTFd challenges from HTML"""
        challenges = []
        
        # Wait for challenges to load
        page.wait_for_selector('.challenge-button, [class*="challenge"]', timeout=5000)
        
        # Get all challenge elements
        challenge_elements = page.query_selector_all('.challenge-button, [class*="challenge-card"]')
        
        for elem in challenge_elements:
            try:
                name = elem.query_selector('[class*="name"], .challenge-name, h3, h4')
                category = elem.query_selector('[class*="category"], .badge')
                
                if name:
                    challenges.append({
                        'name': name.inner_text().strip(),
                        'category': category.inner_text().strip() if category else 'Misc',
                        'platform': 'ctfd'
                    })
            except Exception as e:
                self.logger.debug(f"Error parsing challenge element: {e}")
                continue
        
        return challenges
    
    def _scrape_picoctf_html(self, page) -> List[Dict]:
        """Scrape picoCTF challenges from HTML"""
        challenges = []
        
        # picoCTF specific selectors
        challenge_elements = page.query_selector_all('[class*="challenge"], .problem-card, [data-challenge]')
        
        for elem in challenge_elements:
            try:
                name = elem.query_selector('h3, h4, [class*="title"]')
                category = elem.query_selector('[class*="category"], .badge')
                
                if name:
                    challenges.append({
                        'name': name.inner_text().strip(),
                        'category': category.inner_text().strip() if category else 'Misc',
                        'platform': 'picoctf'
                    })
            except Exception as e:
                self.logger.debug(f"Error parsing challenge: {e}")
                continue
        
        return challenges
    
    def _scrape_generic_html(self, page) -> List[Dict]:
        """Generic HTML scraping"""
        challenges = []
        
        # Try common patterns
        selectors = [
            'article', 'li', '[class*="card"]', '[class*="item"]',
            '[class*="challenge"]', '[class*="problem"]'
        ]
        
        for selector in selectors:
            elements = page.query_selector_all(selector)
            if len(elements) > 5:  # Likely found the right pattern
                for elem in elements[:50]:  # Limit to prevent noise
                    text = elem.inner_text().strip()
                    if text and len(text) < 200:
                        challenges.append({
                            'name': text.split('\n')[0],
                            'category': 'Unknown',
                            'platform': 'generic'
                        })
                break
        
        return challenges
    
    def _save_challenges(self, challenges: List[Dict]):
        """Save scraped challenges"""
        for chal in challenges:
            category_folder = self.output_dir / UniversalCTFScraper._sanitize_filename(chal['category'])
            challenge_folder = category_folder / UniversalCTFScraper._sanitize_filename(chal['name'])
            challenge_folder.mkdir(parents=True, exist_ok=True)
            
            with open(challenge_folder / 'challenge.txt', 'w', encoding='utf-8') as f:
                f.write(f"Challenge: {chal['name']}\n")
                f.write(f"Category: {chal['category']}\n")
                f.write(f"Platform: {chal['platform']}\n")
                f.write(f"\nScraped via browser fallback mode\n")
                f.write(f"Log in to the platform to view full details and download files\n")


def get_cookies_securely() -> Optional[str]:
    """Get cookies securely from environment or prompt"""
    # Check environment variable first
    cookies = os.environ.get('CTF_COOKIES')
    if cookies:
        print("✅ Using cookies from CTF_COOKIES environment variable")
        return cookies

    # Prompt user with clear instructions
    print("\n🔐 No cookies found. How to get them:\n")
    print("  Method 1 — Cookie Editor Extension (EASIEST) ⭐")
    print("    1. Install 'Cookie Editor' browser extension")
    print("    2. Login to the CTF platform")
    print("    3. Click Cookie Editor icon → Export → 'Header String'")
    print("    4. Paste when prompted below (or use: -c \"paste_here\")\n")
    print("  Method 2 — Environment Variable (most secure)")
    print("    export CTF_COOKIES=\"session=xxx; cf_clearance=yyy\"\n")
    print("  Method 3 — Cookie File")
    print("    echo \"session=xxx\" > cookies.txt && -c @cookies.txt\n")
    print("  Method 4 — Browser Mode (no cookies needed)")
    print("    python3 ctf_scraper.py --browser \"URL\" ./output\n")

    choice = input("➡️  Paste cookies now? (y/N): ").strip().lower()
    if choice == 'y':
        return input("🔐 Paste cookies: ").strip()

    return None


def main():
    parser = argparse.ArgumentParser(
        description='Ultimate Universal CTF Scraper v2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Getting Cookies (EASIEST METHOD ⭐):
  1. Install "Cookie Editor" browser extension
  2. Login to the CTF platform
  3. Click Cookie Editor icon → Export → "Header String"
  4. Use with -c flag: -c "session=xxx; cf_clearance=yyy"

Examples:
  # Cookie Editor method (easiest)
  %(prog)s "https://ctf.example.com/challenges" -c "session=XXX; cf_clearance=YYY" ./output

  # Environment variable (most secure)
  export CTF_COOKIES="session=XXX; cf_clearance=YYY"
  %(prog)s "https://ctf.0xfun.org/challenges" ./output

  # Cookie file
  %(prog)s "https://ctf.example.com/challenges" -c @cookies.txt ./output

  # Browser fallback (no cookies needed, manual login)
  %(prog)s --browser "https://ctf.example.com" ./output

  # Dry run (preview without downloading)
  %(prog)s "URL" -c "COOKIES" --dry-run ./output

  # Resume interrupted download
  %(prog)s "URL" -c "COOKIES" --skip-existing ./output
        """
    )
    
    parser.add_argument('url', nargs='?', help='CTF platform URL')
    parser.add_argument('output_dir', nargs='?', default='./output', help='Output directory (default: ./output)')
    parser.add_argument('-c', '--cookies', help='Cookies string or @file.txt')
    parser.add_argument('--browser', action='store_true', help='Use browser fallback mode')
    parser.add_argument('--dry-run', action='store_true', help='Preview challenges without downloading')
    parser.add_argument('--skip-existing', action='store_true', help='Skip already downloaded challenges')
    parser.add_argument('--max-workers', type=int, default=10, help='Max concurrent downloads (default: 10)')
    parser.add_argument('--timeout', type=int, default=30, help='Request timeout in seconds (default: 30)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.url and not args.browser:
        parser.print_help()
        sys.exit(1)
    
    print("\n" + "="*60)
    print("🎯 ULTIMATE UNIVERSAL CTF SCRAPER v2.0")
    print("="*60)
    
    try:
        # Browser fallback mode
        if args.browser:
            if not args.url:
                args.url = input("➡️  Enter CTF URL: ").strip()
            
            browser_scraper = BrowserFallbackScraper(args.url, args.output_dir, args.verbose)
            success = browser_scraper.scrape_with_browser()
            sys.exit(0 if success else 1)
        
        # Normal API scraping mode
        cookies = args.cookies or get_cookies_securely()
        
        if not cookies:
            print("\n⚠️  No cookies provided. Attempting without authentication...")
            print("    (This may fail for platforms requiring login)\n")
        
        scraper = UniversalCTFScraper(
            url=args.url,
            cookies_str=cookies,
            output_dir=args.output_dir,
            skip_existing=args.skip_existing,
            dry_run=args.dry_run,
            max_workers=args.max_workers,
            timeout=args.timeout,
            verbose=args.verbose
        )
        
        success = scraper.scrape()
        
        # Offer browser fallback if API scraping failed
        if not success:
            print("\n" + "="*60)
            print("⚠️  API SCRAPING FAILED")
            print("="*60)
            print("\n💡 Would you like to try browser fallback mode?")
            print("   This will open a browser where you can login manually.")
            
            choice = input("\n➡️  Try browser mode? (Y/n): ").strip().lower()
            if choice != 'n':
                browser_scraper = BrowserFallbackScraper(args.url, args.output_dir, args.verbose)
                success = browser_scraper.scrape_with_browser()
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        logging.error(f"\n❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
