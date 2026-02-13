#!/usr/bin/env python3
"""
Quick Cookie Checker - Verify if your cookies are still valid
Usage: python3 check_cookies.py
"""

import sys
import requests

def check_cookies():
    """Interactive cookie checker"""
    
    print("=" * 60)
    print("🍪 COOKIE VALIDATOR FOR ctf.0xfun.org")
    print("=" * 60)
    print()
    
    print("📋 Step 1: Go to https://ctf.0xfun.org/challenges in your browser")
    print("📋 Step 2: Press F12 → Console")
    print("📋 Step 3: Type: document.cookie")
    print("📋 Step 4: Copy the entire output")
    print()
    
    print("Paste your cookies here (or press Ctrl+C to cancel):")
    try:
        cookies_str = input("> ").strip()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled")
        sys.exit(0)
    
    if not cookies_str:
        print("\n❌ No cookies provided!")
        sys.exit(1)
    
    # Parse cookies
    cookies = {}
    for item in cookies_str.split(';'):
        if '=' in item:
            key, value = item.strip().split('=', 1)
            cookies[key] = value
    
    print()
    print(f"✅ Found {len(cookies)} cookies: {list(cookies.keys())}")
    print()
    
    # Check what we have
    has_session = 'session' in cookies
    has_cf_clearance = 'cf_clearance' in cookies
    
    if has_session:
        print("✅ session cookie found")
    else:
        print("❌ session cookie missing!")
    
    if has_cf_clearance:
        print("✅ cf_clearance cookie found")
    else:
        print("❌ cf_clearance cookie missing (CRITICAL!)")
    
    print()
    
    if not (has_session and has_cf_clearance):
        print("⚠️  WARNING: Missing required cookies!")
        print("   Make sure you're logged in and copied ALL cookies.")
        print()
    
    # Test the cookies
    print("🧪 Testing cookies...")
    print()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://ctf.0xfun.org/challenges',
    }
    
    url = "https://ctf.0xfun.org/challenges"
    
    try:
        session = requests.Session()
        session.cookies.update(cookies)
        response = session.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            print("✅ ✅ ✅  SUCCESS!!! Cookies are VALID! ✅ ✅ ✅")
            print()
            print(f"📄 Page loaded: {len(response.text)} bytes")
            
            # Check for Cloudflare
            if 'Just a moment' in response.text or 'cf-chl' in response.text:
                print("⚠️  WARNING: Cloudflare challenge detected")
                print("   Cookies might be expired or site is rate-limiting")
            else:
                print("✅ No Cloudflare challenge detected")
                
                # Check for CTFd
                if 'CTFd' in response.text or 'api/v1/challenges' in response.text:
                    print("✅ CTFd platform detected")
                    
                    # Try API
                    api_url = "https://ctf.0xfun.org/api/v1/challenges"
                    api_resp = session.get(api_url, headers=headers, timeout=15)
                    
                    if api_resp.status_code == 200:
                        try:
                            data = api_resp.json()
                            if 'data' in data:
                                count = len(data['data'])
                                print(f"✅ API works! Found {count} challenges")
                                print()
                                print("🎉 YOU'RE READY TO SCRAPE!")
                                print()
                                print("Run this command:")
                                print(f'python3 ctf_scraper_ultimate.py {url} -c "{cookies_str[:50]}..." -v')
                            else:
                                print("⚠️  API returned data but format unexpected")
                        except:
                            print("⚠️  API response not valid JSON")
                    else:
                        print(f"⚠️  API returned {api_resp.status_code}")
                        print("   Might need to scrape HTML instead")
            
        elif response.status_code == 403:
            print("❌ FAILED: 403 Forbidden")
            if 'cloudflare' in response.text.lower():
                print("   🔒 Cloudflare is blocking - cookies are EXPIRED!")
                print()
                print("   Solution: Get FRESH cookies (they expire in ~10 min)")
            else:
                print("   🔒 Authentication failed")
                print()
                print("   Solution: Make sure you're logged in")
        
        elif response.status_code == 429:
            print("❌ FAILED: 429 Too Many Requests")
            print("   ⏱  You're being rate-limited. Wait a few minutes.")
        
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    
    except requests.exceptions.Timeout:
        print("❌ FAILED: Request timed out")
        print("   The site might be down or blocking your IP")
    except requests.exceptions.ConnectionError:
        print("❌ FAILED: Connection error")
        print("   Check your internet connection")
    except Exception as e:
        print(f"❌ FAILED: {e}")
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    check_cookies()
