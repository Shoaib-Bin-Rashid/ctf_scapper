#!/usr/bin/env python3
"""
Test with FULL browser headers to bypass Cloudflare
"""

import requests
from bs4 import BeautifulSoup

URL = "https://ctf.0xfun.org/challenges"

# Your cookies
COOKIES = {
    'session': 'c88cf6b1-a4d6-49c4-8c4e-5d6e990de49c.PadA7zR2y6eo7uOSzWc7VThAjgI',
    'cf_clearance': 'h3IZjR1O_5giJKraXubGygDCCmr20KVZcjSfhekxcN8-1770984001-1.2.1.1-XaCd3xW8YnVUfPNeCeQtaGA4T4KyCFUYy1esMfrAEm8VaAzrKOsP9pdIjOWMUBQoJH5jv5h742og_ogAbQHw9nsRsULbO71VhexxOSTPMOJmAU0chsJqkYHUIvbwr0BluJj_RilB0Mk4mkxoguFPAysuqJQFHMnAEaaBKWHydWLrOH1_ik8E5GQyCwX9cALzIeS_.kNUyfyyxZKmRNVYpsogDdmAa6XDKYaKTYAHHN79jxE54fHQ_vy9D8Rdl176'
}

# Full browser headers from your request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://ctf.0xfun.org/challenges',
    'Sec-Ch-Ua': '"Not.A/Brand";v="99", "Chromium";v="136"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Upgrade-Insecure-Requests': '1',
}

print("=" * 80)
print("🧪 TESTING WITH FULL BROWSER HEADERS + COOKIES")
print("=" * 80)

try:
    response = requests.get(URL, headers=HEADERS, cookies=COOKIES, timeout=15)
    
    print(f"\n✅ Status Code: {response.status_code}")
    print(f"✅ Response Length: {len(response.text)} bytes")
    print(f"✅ Content Type: {response.headers.get('content-type', 'N/A')}")
    
    # Check for Cloudflare
    if 'Just a moment' in response.text or 'cf-chl' in response.text:
        print("❌ CLOUDFLARE STILL BLOCKING!")
        print("\n📄 Response preview:")
        print(response.text[:500])
    else:
        print("✅ SUCCESS! No Cloudflare challenge!")
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find('title')
        print(f"\n📌 Page Title: {title.get_text() if title else 'N/A'}")
        
        # Look for challenges
        print("\n🔍 Looking for challenges...")
        
        # Search for keywords from screenshot
        keywords = ['TLSB', 'Templates', 'UART', 'Shell', 'Perceptions']
        found = 0
        for keyword in keywords:
            if keyword in response.text:
                print(f"   ✅ Found: {keyword}")
                found += 1
            else:
                print(f"   ❌ Missing: {keyword}")
        
        if found > 0:
            print(f"\n�� SUCCESS! Found {found}/{len(keywords)} challenges!")
            print("\n📄 Response preview (first 1000 chars):")
            print("-" * 80)
            print(response.text[:1000])
        else:
            print("\n⚠️  No challenges found in response")
            print("\n📄 Response preview:")
            print(response.text[:1000])

except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
