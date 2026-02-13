# Testing Guide for CTF Scraper

## Test Results for https://ctf.0xfun.org/challenges

### Test Run #1: Without Authentication
```bash
python ctf_scraper_ultimate.py https://ctf.0xfun.org/challenges --dry-run -v
```

**Result:** ❌ **403 Forbidden**
- The website requires authentication
- Need to login and provide session cookie

### How to Test with Authentication

#### Step 1: Login to the CTF Website
1. Open https://ctf.0xfun.org in your browser
2. Create an account or login
3. Navigate to /challenges page

#### Step 2: Extract Your Session Cookie

**Method A: Using Browser DevTools**
1. Press `F12` to open Developer Tools
2. Go to **Application** tab (Chrome) or **Storage** tab (Firefox)
3. Click **Cookies** → Select `ctf.0xfun.org`
4. Find the `session` cookie
5. Copy its value

**Method B: Using Console**
1. Press `F12` and go to **Console** tab
2. Type: `document.cookie`
3. Copy the entire output

#### Step 3: Run the Scraper with Cookie

**Interactive Mode (Recommended):**
```bash
python ctf_scraper_ultimate.py https://ctf.0xfun.org/challenges -i -v
```
The tool will ask for your cookie if needed.

**Direct Mode:**
```bash
python ctf_scraper_ultimate.py https://ctf.0xfun.org/challenges \
  -c "session=YOUR_SESSION_COOKIE_HERE" \
  -o test_run/0xfun_ctf \
  -v
```

**Example with actual cookie:**
```bash
python ctf_scraper_ultimate.py https://ctf.0xfun.org/challenges \
  -c "session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoxMjM0fQ.abcdef..." \
  -o test_run/0xfun_ctf \
  -v
```

### Expected Output Structure

After successful scraping:
```
test_run/0xfun_ctf/
├── Pwn/
│   ├── buffer_overflow_101/
│   │   ├── statement.txt
│   │   └── files/
│   │       ├── vuln
│   │       └── libc.so.6
│   └── rop_challenge/
│       ├── statement.txt
│       └── files/
├── Web/
│   ├── sql_injection_basics/
│   │   ├── statement.txt
│   │   └── files/
│   └── xss_challenge/
│       ├── statement.txt
│       └── files/
├── Crypto/
├── Reverse/
├── Forensics/
└── Misc/
```

## Testing with Other CTF Platforms

### Public CTFs (No Auth Required)

Try with public CTFs for testing:
```bash
# Test with a public CTFd instance (if available)
python ctf_scraper_ultimate.py <PUBLIC_CTF_URL> --dry-run -v

# Example with generic scraper
python ctf_scraper_ultimate.py <ANY_CTF_URL> --platform generic -v
```

### Creating a Mock Test

If you want to test the tool without a real CTF:

1. **Create a simple HTML test page:**
```bash
cd test_run
mkdir -p mock_ctf
cat > mock_ctf/index.html << 'EOF'
<html>
<head><title>Mock CTF</title></head>
<body>
<h1>Challenges</h1>
<table>
<tr><th>Name</th><th>Category</th><th>Description</th></tr>
<tr><td>Test Pwn Challenge</td><td>Pwn</td><td>A test binary exploitation challenge</td></tr>
<tr><td>Test Web Challenge</td><td>Web</td><td>A test web security challenge</td></tr>
<tr><td>Test Crypto Challenge</td><td>Crypto</td><td>A test cryptography challenge</td></tr>
</table>
</body>
</html>
EOF
```

2. **Serve it locally:**
```bash
cd mock_ctf
python3 -m http.server 8000
```

3. **Test the scraper:**
```bash
python ctf_scraper_ultimate.py http://localhost:8000 --platform generic -v
```

## Troubleshooting Common Issues

### Issue 1: "403 Forbidden"
**Solution:** Provide authentication cookie
```bash
python ctf_scraper_ultimate.py <URL> -i
```

### Issue 2: "No challenges found"
**Solutions:**
- Verify you're on the correct challenges page URL
- Try different platform: `--platform generic`
- Check if authentication is required
- Use verbose mode to see what's happening: `-v`

### Issue 3: "Files not downloading"
**Solutions:**
- Check your internet connection
- Some files may require authentication
- Check file URLs in verbose mode
- Try downloading manually first to test

### Issue 4: "Wrong categories"
**Solution:** Customize category mappings in `config.yaml`

## Dry Run vs Real Run

### Dry Run (Safe - No Downloads)
```bash
python ctf_scraper_ultimate.py <URL> --dry-run -v
```
- Shows what will be scraped
- No files downloaded
- No folders created
- Quick preview

### Real Run (Downloads Everything)
```bash
python ctf_scraper_ultimate.py <URL> -o ./my_ctf -v
```
- Downloads all challenges
- Creates folder structure
- Downloads all files
- Can take time depending on size

## Performance Tips

1. **Use dry-run first** to see what you'll get
2. **Use verbose mode** to monitor progress
3. **Specify output directory** to organize better
4. **Check disk space** before large downloads

## Next Steps

1. ✅ Get your session cookie from the CTF website
2. ✅ Run with `-i` interactive mode
3. ✅ Use `--dry-run` first to preview
4. ✅ Run full scrape when ready
5. ✅ Organize and solve challenges!

## Example Complete Workflow

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Test with dry run
python ctf_scraper_ultimate.py https://ctf.0xfun.org/challenges --dry-run

# 3. If authentication needed, use interactive mode
python ctf_scraper_ultimate.py https://ctf.0xfun.org/challenges -i -v

# 4. Full scrape
python ctf_scraper_ultimate.py https://ctf.0xfun.org/challenges \
  -c "YOUR_COOKIE" \
  -o ~/CTFs/0xfun_2026 \
  -v

# 5. Navigate to challenges
cd ~/CTFs/0xfun_2026
ls -la

# 6. Start solving!
cd Pwn/buffer_overflow_101
cat statement.txt
```

## Success Criteria

The scraper is working correctly when:
- ✅ It detects the platform type
- ✅ It connects to the CTF website (200 OK or authenticated)
- ✅ It finds and lists challenges
- ✅ It creates proper folder structure
- ✅ It downloads challenge statements
- ✅ It downloads challenge files
- ✅ Categories are assigned correctly

**Happy CTF Playing! 🚀**
