"""
CTF Scraper Base Class
Provides common functionality for all platform-specific scrapers
"""

import os
import re
import requests
from typing import List, Dict, Optional
from pathlib import Path
from bs4 import BeautifulSoup


class Challenge:
    """Represents a single CTF challenge"""
    
    def __init__(self, name: str, category: str, description: str, files: List[str] = None):
        self.name = name
        self.category = category
        self.description = description
        self.files = files or []
        
    def __repr__(self):
        return f"Challenge(name='{self.name}', category='{self.category}', files={len(self.files)})"


class BaseScraper:
    """Base scraper class with common functionality"""
    
    CATEGORY_KEYWORDS = {
        'pwn': ['pwn', 'binary', 'exploitation', 'buffer', 'overflow'],
        'web': ['web', 'webapp', 'website', 'http', 'xss', 'sqli'],
        'crypto': ['crypto', 'cryptography', 'rsa', 'aes', 'cipher'],
        'reverse': ['reverse', 'rev', 'reversing', 'crackme', 're'],
        'forensics': ['forensics', 'forensic', 'steganography', 'stego', 'pcap'],
        'misc': ['misc', 'miscellaneous', 'trivia']
    }
    
    def __init__(self, url: str, cookie: Optional[str] = None, token: Optional[str] = None, 
                 output_dir: str = "./ctf_challenges", verbose: bool = False):
        self.url = url
        self.cookie = cookie
        self.token = token
        self.output_dir = Path(output_dir)
        self.verbose = verbose
        self.session = requests.Session()
        
        # Setup authentication
        if cookie:
            self.session.cookies.update(self._parse_cookie(cookie))
        if token:
            self.session.headers.update({'Authorization': f'Bearer {token}'})
            
        # Set a reasonable user agent to avoid bot detection
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # Set timeout and retry strategy
        self.timeout = 30
        self.max_retries = 3
        
    def _parse_cookie(self, cookie_string: str) -> dict:
        """Parse cookie string into dict"""
        cookies = {}
        for item in cookie_string.split(';'):
            if '=' in item:
                key, value = item.strip().split('=', 1)
                cookies[key] = value
        return cookies
    
    def log(self, message: str, level: str = "INFO"):
        """Log messages if verbose mode is enabled"""
        if self.verbose:
            print(f"[{level}] {message}")
    
    def sanitize_filename(self, filename: str) -> str:
        """Remove special characters from filename"""
        # Remove or replace special characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = re.sub(r'\s+', '_', filename)
        filename = filename.strip('._')
        return filename or 'unnamed'
    
    def detect_category(self, challenge_name: str, tags: List[str] = None) -> str:
        """Detect challenge category based on name and tags"""
        text = challenge_name.lower()
        
        # Check tags first if available
        if tags:
            for tag in tags:
                tag_lower = tag.lower()
                for category, keywords in self.CATEGORY_KEYWORDS.items():
                    if tag_lower in keywords:
                        return category.capitalize()
        
        # Check challenge name
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    return category.capitalize()
        
        # Default category
        return 'Misc'
    
    def create_folder_structure(self, ctf_name: str, category: str, challenge_name: str) -> Path:
        """Create folder structure for a challenge"""
        ctf_name = self.sanitize_filename(ctf_name)
        category = self.sanitize_filename(category)
        challenge_name = self.sanitize_filename(challenge_name)
        
        challenge_path = self.output_dir / ctf_name / category / challenge_name
        files_path = challenge_path / 'files'
        
        challenge_path.mkdir(parents=True, exist_ok=True)
        files_path.mkdir(exist_ok=True)
        
        self.log(f"Created folder: {challenge_path}")
        return challenge_path
    
    def download_file(self, url: str, destination: Path, filename: Optional[str] = None) -> bool:
        """Download a file from URL to destination with retry logic"""
        for attempt in range(self.max_retries):
            try:
                if filename is None:
                    # Extract filename from URL or Content-Disposition header
                    filename = url.split('/')[-1].split('?')[0]
                
                filename = self.sanitize_filename(filename)
                filepath = destination / filename
                
                self.log(f"Downloading: {url} -> {filepath}")
                
                response = self.session.get(url, stream=True, timeout=self.timeout, allow_redirects=True)
                response.raise_for_status()
                
                # Try to get filename from Content-Disposition header
                if 'Content-Disposition' in response.headers:
                    cd = response.headers['Content-Disposition']
                    if 'filename=' in cd:
                        filename_match = re.search(r'filename[^;=\n]*=(([\'"]).*?\2|[^;\n]*)', cd)
                        if filename_match:
                            filename = filename_match.group(1).strip('\'"')
                            filepath = destination / self.sanitize_filename(filename)
                
                # Download file
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                self.log(f"Downloaded: {filename}", "SUCCESS")
                return True
                
            except Exception as e:
                self.log(f"Download attempt {attempt + 1} failed: {e}", "WARNING")
                if attempt < self.max_retries - 1:
                    import time
                    time.sleep(2 ** attempt)
                else:
                    self.log(f"Failed to download {url}: {e}", "ERROR")
        
        return False
    
    def save_statement(self, challenge_path: Path, statement: str):
        """Save challenge statement to text file"""
        statement_file = challenge_path / 'statement.txt'
        with open(statement_file, 'w', encoding='utf-8') as f:
            f.write(statement)
        self.log(f"Saved statement: {statement_file}")
    
    def fetch_page(self, url: str, retries: int = None) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page with retry logic"""
        if retries is None:
            retries = self.max_retries
            
        last_error = None
        for attempt in range(retries):
            try:
                self.log(f"Fetching {url} (attempt {attempt + 1}/{retries})")
                response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
                response.raise_for_status()
                
                # Check for Cloudflare challenge
                if 'Just a moment' in response.text or 'cf-chl' in response.text:
                    self.log("Cloudflare/bot protection detected - authentication required", "WARNING")
                    return None
                
                return BeautifulSoup(response.text, 'lxml')
            except requests.exceptions.HTTPError as e:
                last_error = e
                if e.response.status_code == 403:
                    # Check if it's Cloudflare
                    if 'cloudflare' in e.response.text.lower() or 'cf-chl' in e.response.text:
                        self.log(f"403 Forbidden - Cloudflare protection detected. Login required to get valid cookies.", "WARNING")
                    else:
                        self.log(f"403 Forbidden - Authentication required", "WARNING")
                elif e.response.status_code == 404:
                    self.log(f"404 Not Found - URL may be incorrect", "ERROR")
                    break
                else:
                    self.log(f"HTTP error {e.response.status_code}: {e}", "WARNING")
            except requests.exceptions.Timeout:
                last_error = Exception("Request timeout")
                self.log(f"Request timeout (attempt {attempt + 1}/{retries})", "WARNING")
            except Exception as e:
                last_error = e
                self.log(f"Error fetching page: {e}", "WARNING")
            
            if attempt < retries - 1:
                import time
                time.sleep(2 ** attempt)  # Exponential backoff
        
        self.log(f"Failed to fetch {url} after {retries} attempts: {last_error}", "ERROR")
        return None
    
    def scrape(self) -> List[Challenge]:
        """
        Main scraping method - must be implemented by platform-specific scrapers
        Returns a list of Challenge objects
        """
        raise NotImplementedError("Subclasses must implement scrape()")
    
    def run(self, dry_run: bool = False) -> int:
        """
        Run the scraper
        Returns the number of challenges scraped
        """
        self.log(f"Starting scrape of {self.url}")
        
        # Get challenges
        challenges = self.scrape()
        
        if not challenges:
            self.log("No challenges found", "WARNING")
            return 0
        
        self.log(f"Found {len(challenges)} challenges")
        
        if dry_run:
            self.log("DRY RUN - No files will be downloaded", "INFO")
            for challenge in challenges:
                print(f"  - {challenge.category}/{challenge.name} ({len(challenge.files)} files)")
            return len(challenges)
        
        # Process each challenge
        ctf_name = self._extract_ctf_name()
        
        for i, challenge in enumerate(challenges, 1):
            self.log(f"[{i}/{len(challenges)}] Processing: {challenge.name}")
            
            # Create folder structure
            challenge_path = self.create_folder_structure(
                ctf_name, challenge.category, challenge.name
            )
            
            # Save statement
            self.save_statement(challenge_path, challenge.description)
            
            # Download files
            files_path = challenge_path / 'files'
            for file_url in challenge.files:
                self.download_file(file_url, files_path)
        
        self.log(f"Scraping complete! Processed {len(challenges)} challenges", "SUCCESS")
        return len(challenges)
    
    def _extract_ctf_name(self) -> str:
        """Extract CTF name from URL or page title"""
        # Try to get from URL
        from urllib.parse import urlparse
        parsed = urlparse(self.url)
        domain = parsed.netloc.replace('www.', '')
        return domain.split('.')[0] if domain else 'ctf'
