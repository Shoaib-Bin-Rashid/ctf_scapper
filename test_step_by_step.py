#!/usr/bin/env python3
"""
Step-by-Step CTF Scraper Tester
Test each step to see what's working and what's not
"""

import requests
from bs4 import BeautifulSoup

print("=" * 80)
print("🧪 CTF SCRAPER - STEP BY STEP TESTING")
print("=" * 80)

URL = "https://ctf.0xfun.org/challenges"

# ============================================================================
# STEP 1: Test basic connection without any cookies
# ============================================================================
print("\n📍 STEP 1: Testing basic connection (NO cookies)")
print("-" * 80)

try:
    response = requests.get(URL, timeout=10)
    print(f"✅ Status Code: {response.status_code}")
    print(f"✅ Response Length: {len(response.text)} bytes")
    print(f"✅ Content Type: {response.headers.get('content-type', 'N/A')}")
    
    # Check for Cloudflare
    if 'cloudflare' in response.text.lower() or 'Just a moment' in response.text:
        print("⚠️  CLOUDFLARE DETECTED!")
        print("    The page is showing Cloudflare challenge")
        cloudflare_detected = True
    else:
        cloudflare_detected = False
        print("✅ No Cloudflare challenge detected")
    
    # Check first 500 chars
    print("\n📄 First 500 characters of response:")
    print("-" * 80)
    print(response.text[:500])
    print("-" * 80)
    
    # Try to parse as HTML
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('title')
    print(f"\n📌 Page Title: {title.get_text() if title else 'No title found'}")
    
    # Look for challenges
    print("\n🔍 Looking for challenge elements...")
    challenges = soup.find_all(['div', 'article'], class_=lambda x: x and 'challenge' in x.lower())
    print(f"   Found {len(challenges)} elements with 'challenge' in class name")
    
except requests.exceptions.RequestException as e:
    print(f"❌ Error: {e}")
    cloudflare_detected = False

# ============================================================================
# STEP 2: Test with cookies (if user provides them)
# ============================================================================
print("\n" + "=" * 80)
print("📍 STEP 2: Testing WITH cookies")
print("-" * 80)

cookie_input = input("\n🍪 Paste your cookies here (from document.cookie), or press Enter to skip:\n> ").strip()

if cookie_input:
    print("\n🔄 Testing with your cookies...")
    
    # Parse cookies
    cookies = {}
    for item in cookie_input.split(';'):
        if '=' in item:
            key, value = item.strip().split('=', 1)
            cookies[key] = value
    
    print(f"📋 Found {len(cookies)} cookies:")
    for key in cookies.keys():
        print(f"   - {key}")
    
    # Make request with cookies
    try:
        response = requests.get(URL, cookies=cookies, timeout=10)
        print(f"\n✅ Status Code: {response.status_code}")
        print(f"✅ Response Length: {len(response.text)} bytes")
        
        # Check for Cloudflare
        if 'cloudflare' in response.text.lower() or 'Just a moment' in response.text:
            print("⚠️  CLOUDFLARE STILL BLOCKING!")
            print("    Cookies might be incomplete or expired")
        else:
            print("✅ No Cloudflare challenge!")
        
        # Check first 500 chars
        print("\n📄 First 500 characters of response:")
        print("-" * 80)
        print(response.text[:500])
        print("-" * 80)
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find('title')
        print(f"\n📌 Page Title: {title.get_text() if title else 'No title found'}")
        
        # Look for challenges
        print("\n🔍 Looking for challenge elements...")
        
        # Try different selectors
        selectors = [
            ('div with "challenge" class', 'div', lambda x: x and 'challenge' in x.lower()),
            ('div with "card" class', 'div', lambda x: x and 'card' in x.lower()),
            ('article tags', 'article', None),
            ('h2, h3, h4 headers', ['h2', 'h3', 'h4'], None),
        ]
        
        for desc, tag, class_filter in selectors:
            if class_filter:
                elements = soup.find_all(tag, class_=class_filter)
            else:
                elements = soup.find_all(tag) if isinstance(tag, str) else soup.find_all(tag)
            
            print(f"   {desc}: {len(elements)} found")
            
            # Show first few
            if elements and len(elements) > 0:
                print(f"      Examples:")
                for elem in elements[:3]:
                    text = elem.get_text(strip=True)[:50]
                    print(f"      - {text}")
        
        # Check if we can find challenge names from your screenshot
        print("\n🎯 Looking for specific challenges from screenshot...")
        keywords = ['TLSB', 'Templates', 'UART', 'Shell', 'Perceptions', 
                   'Leonine', 'Schrödinger', 'Delicious', 'Guess']
        
        for keyword in keywords:
            if keyword.lower() in response.text.lower():
                print(f"   ✅ Found: {keyword}")
            else:
                print(f"   ❌ Missing: {keyword}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
else:
    print("⏭️  Skipped cookie test")

# ============================================================================
# STEP 3: Summary and recommendations
# ============================================================================
print("\n" + "=" * 80)
print("📊 SUMMARY")
print("=" * 80)

if cloudflare_detected:
    print("""
⚠️  CLOUDFLARE IS BLOCKING!

The page is protected by Cloudflare. You MUST:
  1. Open https://ctf.0xfun.org/challenges in browser
  2. Let the page load completely
  3. Press F12 → Console tab
  4. Type: document.cookie
  5. Copy ALL output
  6. Run this script again and paste it
    """)
else:
    if cookie_input:
        print("""
✅ SUCCESS! Cookies are working!

Next steps:
  1. Run the full scraper with these cookies
  2. Use the -v flag to see detailed output
        """)
    else:
        print("""
ℹ️  The page might be accessible without cookies.

But you should still provide cookies to be safe.
Try running STEP 2 with cookies.
        """)

print("=" * 80)
print("\n💡 To run full scraper after testing:")
print("   python ctf_scraper_ultimate.py https://ctf.0xfun.org/challenges \\")
print("     -c \"YOUR_COOKIES\" -v")
print("=" * 80)
