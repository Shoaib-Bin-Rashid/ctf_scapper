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
            
        # Set a reasonable user agent
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        
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
        """Download a file from URL to destination"""
        try:
            if filename is None:
                # Extract filename from URL or Content-Disposition header
                filename = url.split('/')[-1].split('?')[0]
            
            filename = self.sanitize_filename(filename)
            filepath = destination / filename
            
            self.log(f"Downloading: {url} -> {filepath}")
            
            response = self.session.get(url, stream=True, timeout=30)
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
            self.log(f"Failed to download {url}: {e}", "ERROR")
            return False
    
    def save_statement(self, challenge_path: Path, statement: str):
        """Save challenge statement to text file"""
        statement_file = challenge_path / 'statement.txt'
        with open(statement_file, 'w', encoding='utf-8') as f:
            f.write(statement)
        self.log(f"Saved statement: {statement_file}")
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'lxml')
        except Exception as e:
            self.log(f"Failed to fetch {url}: {e}", "ERROR")
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
