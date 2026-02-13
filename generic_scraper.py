"""
Generic/Fallback Scraper
For custom or unknown CTF platforms
"""

from typing import List
from urllib.parse import urljoin
from scraper_base import BaseScraper, Challenge


class GenericScraper(BaseScraper):
    """Generic scraper for custom platforms"""
    
    def scrape(self) -> List[Challenge]:
        """
        Generic scraping approach:
        1. Find all links on the page
        2. Look for patterns that might indicate challenges
        3. Extract what we can
        """
        challenges = []
        
        soup = self.fetch_page(self.url)
        if not soup:
            return challenges
        
        # Look for common patterns
        # Many CTF platforms use cards, tables, or lists for challenges
        
        # Try to find tables with challenge info
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip header
                cells = row.find_all('td')
                if len(cells) >= 2:
                    try:
                        name = cells[0].get_text(strip=True)
                        category = cells[1].get_text(strip=True) if len(cells) > 1 else 'Misc'
                        
                        # Look for links to files
                        file_urls = []
                        for link in row.find_all('a', href=True):
                            href = link['href']
                            if any(ext in href.lower() for ext in ['.zip', '.tar', '.gz', '.txt', '.bin', '.elf']):
                                file_urls.append(urljoin(self.url, href))
                        
                        # Get description if available
                        description = f"Challenge: {name}\nCategory: {category}\n"
                        desc_cell = cells[2] if len(cells) > 2 else None
                        if desc_cell:
                            description += f"\n{desc_cell.get_text(strip=True)}"
                        
                        # Auto-detect category if not clear
                        detected_category = self.detect_category(name, [category])
                        
                        challenge = Challenge(
                            name=name,
                            category=detected_category,
                            description=description,
                            files=file_urls
                        )
                        challenges.append(challenge)
                        
                    except Exception as e:
                        self.log(f"Failed to parse row: {e}", "ERROR")
                        continue
        
        # Try to find card-based layouts
        if not challenges:
            cards = soup.find_all(['div', 'article'], class_=lambda x: x and ('card' in x.lower() or 'challenge' in x.lower()))
            
            for card in cards:
                try:
                    # Try to find title
                    title_elem = card.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                    name = title_elem.get_text(strip=True) if title_elem else 'Unknown'
                    
                    # Try to find category
                    category_elem = card.find(class_=lambda x: x and 'category' in x.lower())
                    category = category_elem.get_text(strip=True) if category_elem else 'Misc'
                    
                    # Get description
                    desc_elem = card.find(['p', 'div'], class_=lambda x: x and ('desc' in x.lower() or 'content' in x.lower()))
                    description = f"Challenge: {name}\nCategory: {category}\n"
                    if desc_elem:
                        description += f"\n{desc_elem.get_text(strip=True)}"
                    
                    # Find files
                    file_urls = []
                    for link in card.find_all('a', href=True):
                        href = link['href']
                        if 'download' in href.lower() or 'file' in href.lower():
                            file_urls.append(urljoin(self.url, href))
                    
                    detected_category = self.detect_category(name, [category])
                    
                    challenge = Challenge(
                        name=name,
                        category=detected_category,
                        description=description,
                        files=file_urls
                    )
                    challenges.append(challenge)
                    
                except Exception as e:
                    self.log(f"Failed to parse card: {e}", "ERROR")
                    continue
        
        # If still no challenges, try to find any links that might be challenges
        if not challenges:
            self.log("No structured challenges found, trying link-based detection", "WARNING")
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link['href']
                text = link.get_text(strip=True)
                
                # Skip navigation links
                if any(skip in href.lower() for skip in ['login', 'logout', 'register', 'profile', 'about']):
                    continue
                
                # Look for challenge-like links
                if text and len(text) > 3 and 'challenge' in href.lower():
                    name = text
                    category = self.detect_category(name)
                    
                    description = f"Challenge: {name}\n"
                    description += f"URL: {urljoin(self.url, href)}\n"
                    description += "\nNote: Auto-detected challenge. Description may be incomplete."
                    
                    challenge = Challenge(
                        name=name,
                        category=category,
                        description=description,
                        files=[]
                    )
                    challenges.append(challenge)
        
        if challenges:
            self.log(f"Generic scraper found {len(challenges)} potential challenges")
        else:
            self.log("No challenges could be detected. The page structure may be unsupported.", "ERROR")
        
        return challenges
