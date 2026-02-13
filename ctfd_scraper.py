"""
CTFd Platform Scraper
Specialized scraper for CTFd-based CTF platforms
"""

import json
from typing import List, Optional
from urllib.parse import urljoin, urlparse
from scraper_base import BaseScraper, Challenge


class CTFdScraper(BaseScraper):
    """Scraper for CTFd platform"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_base = None
        self.is_api_available = False
        
    def _detect_api_endpoint(self) -> bool:
        """Detect if CTFd API is available"""
        parsed = urlparse(self.url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        # Common CTFd API endpoints
        api_endpoints = [
            f"{base_url}/api/v1/challenges",
            f"{base_url}/api/challenges",
        ]
        
        for endpoint in api_endpoints:
            try:
                self.log(f"Testing API endpoint: {endpoint}")
                response = self.session.get(endpoint, timeout=10, allow_redirects=True)
                
                # Check if response is JSON
                try:
                    data = response.json()
                except:
                    continue
                
                # CTFd API returns success: true/false
                if response.status_code == 200:
                    if isinstance(data, dict) and data.get('success'):
                        self.api_base = endpoint.rsplit('/', 1)[0]
                        self.log(f"Found CTFd API at: {self.api_base}", "SUCCESS")
                        return True
                    # Some CTFd versions return data directly
                    elif isinstance(data, dict) and 'data' in data:
                        self.api_base = endpoint.rsplit('/', 1)[0]
                        self.log(f"Found CTFd API at: {self.api_base}", "SUCCESS")
                        return True
                        
            except Exception as e:
                self.log(f"API endpoint test failed: {e}", "DEBUG")
                continue
        
        return False
    
    def _scrape_via_api(self) -> List[Challenge]:
        """Scrape challenges using CTFd API"""
        challenges = []
        
        try:
            # Get challenges list
            response = self.session.get(f"{self.api_base}/challenges")
            response.raise_for_status()
            data = response.json()
            
            if not data.get('success'):
                self.log("API request failed", "ERROR")
                return []
            
            challenge_list = data.get('data', [])
            self.log(f"API returned {len(challenge_list)} challenges")
            
            # Get details for each challenge
            for chall in challenge_list:
                chall_id = chall.get('id')
                name = chall.get('name', 'Unknown')
                category = chall.get('category', 'Misc')
                
                # Get challenge details
                detail_response = self.session.get(f"{self.api_base}/challenges/{chall_id}")
                if detail_response.status_code == 200:
                    detail_data = detail_response.json()
                    if detail_data.get('success'):
                        chall_detail = detail_data.get('data', {})
                        
                        description = chall_detail.get('description', '')
                        
                        # Format statement
                        statement = f"Challenge: {name}\n"
                        statement += f"Category: {category}\n"
                        statement += f"Points: {chall_detail.get('value', 'N/A')}\n"
                        statement += f"\nDescription:\n{description}\n"
                        
                        # Get file URLs
                        file_urls = []
                        files = chall_detail.get('files', [])
                        for file_path in files:
                            # CTFd files are usually relative paths
                            parsed = urlparse(self.url)
                            base_url = f"{parsed.scheme}://{parsed.netloc}"
                            file_url = urljoin(base_url, file_path)
                            file_urls.append(file_url)
                        
                        challenge = Challenge(
                            name=name,
                            category=category,
                            description=statement,
                            files=file_urls
                        )
                        challenges.append(challenge)
                        self.log(f"Loaded challenge: {name} ({category})")
            
        except Exception as e:
            self.log(f"API scraping failed: {e}", "ERROR")
        
        return challenges
    
    def _scrape_via_html(self) -> List[Challenge]:
        """Scrape challenges by parsing HTML (fallback method)"""
        challenges = []
        
        soup = self.fetch_page(self.url)
        if not soup:
            return challenges
        
        # Try to find challenge cards/elements
        # CTFd typically uses divs with challenge data
        challenge_elements = soup.find_all('div', class_='challenge-button') or \
                           soup.find_all('button', class_='challenge-button') or \
                           soup.find_all('div', attrs={'data-challenge-id': True})
        
        if not challenge_elements:
            self.log("Could not find challenge elements in HTML", "WARNING")
            # Try to find any links that might lead to challenges
            challenge_links = soup.find_all('a', href=lambda x: x and 'challenge' in x.lower())
            self.log(f"Found {len(challenge_links)} potential challenge links")
        
        # Parse each challenge
        for elem in challenge_elements:
            try:
                # Extract challenge name
                name = elem.get('data-name') or \
                       elem.get_text(strip=True) or \
                       'Unknown Challenge'
                
                # Extract category
                category = elem.get('data-category', 'Misc')
                
                # Try to get challenge ID and fetch details
                chall_id = elem.get('data-challenge-id')
                
                description = "No description available (HTML scraping mode)"
                file_urls = []
                
                if chall_id:
                    # Try to fetch challenge modal/details
                    parsed = urlparse(self.url)
                    base_url = f"{parsed.scheme}://{parsed.netloc}"
                    detail_url = f"{base_url}/challenges/{chall_id}"
                    
                    detail_soup = self.fetch_page(detail_url)
                    if detail_soup:
                        # Find description
                        desc_elem = detail_soup.find('div', class_='challenge-desc') or \
                                  detail_soup.find('p', class_='description')
                        if desc_elem:
                            description = desc_elem.get_text(strip=True)
                        
                        # Find file links
                        file_links = detail_soup.find_all('a', href=lambda x: x and 'files' in x.lower())
                        for link in file_links:
                            file_url = urljoin(base_url, link.get('href'))
                            file_urls.append(file_url)
                
                statement = f"Challenge: {name}\n"
                statement += f"Category: {category}\n"
                statement += f"\nDescription:\n{description}\n"
                
                challenge = Challenge(
                    name=name,
                    category=category,
                    description=statement,
                    files=file_urls
                )
                challenges.append(challenge)
                
            except Exception as e:
                self.log(f"Failed to parse challenge element: {e}", "ERROR")
                continue
        
        return challenges
    
    def scrape(self) -> List[Challenge]:
        """Main scraping method for CTFd"""
        self.log("Attempting CTFd scraping...")
        
        # Try API first
        if self._detect_api_endpoint():
            self.log("Using API-based scraping")
            challenges = self._scrape_via_api()
            if challenges:
                return challenges
            self.log("API scraping returned no results, falling back to HTML", "WARNING")
        
        # Fall back to HTML scraping
        self.log("Using HTML-based scraping")
        return self._scrape_via_html()
    
    def _extract_ctf_name(self) -> str:
        """Extract CTF name from page title or URL"""
        try:
            soup = self.fetch_page(self.url)
            if soup:
                title = soup.find('title')
                if title:
                    ctf_name = title.get_text().split('-')[0].strip()
                    return self.sanitize_filename(ctf_name)
        except:
            pass
        
        # Fallback to parent implementation
        return super()._extract_ctf_name()
