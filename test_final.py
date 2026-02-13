#!/usr/bin/env python3
"""
Final test with proper decompression
"""

import requests
from bs4 import BeautifulSoup

URL = "https://ctf.0xfun.org/challenges"

COOKIES = {
    'session': 'c88cf6b1-a4d6-49c4-8c4e-5d6e990de49c.PadA7zR2y6eo7uOSzWc7VThAjgI',
    'cf_clearance': 'h3IZjR1O_5giJKraXubGygDCCmr20KVZcjSfhekxcN8-1770984001-1.2.1.1-XaCd3xW8YnVUfPNeCeQtaGA4T4KyCFUYy1esMfrAEm8VaAzrKOsP9pdIjOWMUBQoJH5jv5h742og_ogAbQHw9nsRsULbO71VhexxOSTPMOJmAU0chsJqkYHUIvbwr0BluJj_RilB0Mk4mkxoguFPAysuqJQFHMnAEaaBKWHydWLrOH1_ik8E5GQyCwX9cALzIeS_.kNUyfyyxZKmRNVYpsogDdmAa6XDKYaKTYAHHN79jxE54fHQ_vy9D8Rdl176'
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://ctf.0xfun.org/',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Dest': 'document',
}

print("=" * 80)
print("🎯 FINAL TEST - WITH PROPER HEADERS + COOKIES")
print("=" * 80)

session = requests.Session()
session.headers.update(HEADERS)
session.cookies.update(COOKIES)

try:
    response = session.get(URL, timeout=15)
    
    print(f"\n✅ Status Code: {response.status_code}")
    print(f"✅ Response Length: {len(response.text)} bytes")
    print(f"✅ Encoding: {response.encoding}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find('title')
        print(f"📌 Page Title: {title.get_text() if title else 'N/A'}")
        
        # Look for challenges
        print("\n🔍 Searching for challenges...")
        keywords = ['TLSB', 'Templates', 'UART', 'Shell', 'Perceptions', 
                   'Leonine', 'Schrödinger', 'Delicious', 'Guess']
        
        found_count = 0
        for keyword in keywords:
            if keyword in response.text:
                print(f"   ✅ Found: {keyword}")
                found_count += 1
        
        if found_count > 0:
            print(f"\n🎉 SUCCESS! Found {found_count}/{len(keywords)} challenges!")
        else:
            print(f"\n❌ No challenges found")
        
        # Show HTML structure
        print("\n📄 HTML Preview (first 2000 chars):")
        print("-" * 80)
        print(response.text[:2000])
        print("-" * 80)
        
    else:
        print(f"\n❌ Failed with status {response.status_code}")
        print(response.text[:500])

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("=" * 80)
