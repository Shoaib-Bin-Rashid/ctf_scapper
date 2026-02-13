# 🎯 Ultimate CTF Scraper

<div align="center">

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-CTFd%20%7C%20picoCTF-green.svg)]()

**ONE TOOL FOR ALL CTF PLATFORMS!**

*Automatically download and organize CTF challenges from any platform with a single command*

[Quick Start](#-quick-start) • [Features](#-features) • [Documentation](#-documentation) • [Examples](#-examples)

</div>

---

## 🌟 Why This Tool?

Stop wasting time manually downloading CTF challenges! This tool:
- ✅ **Auto-detects** platform type (CTFd, picoCTF, etc.)
- ✅ **Downloads** all challenges and files automatically  
- ✅ **Organizes** by category (Web, Crypto, Pwn, Reverse, etc.)
- ✅ **Bypasses** Cloudflare protection
- ✅ **Works** with most CTF platforms

**Just ONE command for EVERYTHING!**

---

## ⚡ Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Shoaib-Bin-Rashid/ctf_scapper.git
cd ctf_scapper

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Run with ANY CTF platform!
python3 ctf_scraper_ultimate.py "URL" "COOKIES" ./output
```

### Example Usage

```bash
python3 ctf_scraper_ultimate.py \
  "https://ctf.0xfun.org/challenges" \
  "session=XXX; cf_clearance=YYY" \
  ./0xfun_ctf
```

📖 **[Complete Quick Start Guide →](QUICKSTART.md)**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **Auto-Detection** | Automatically identifies CTFd, picoCTF, or other platforms |
| 📥 **Bulk Download** | Downloads all challenges and files in one go |
| 📁 **Auto-Organization** | Sorts challenges by category (Web, Crypto, Pwn, etc.) |
| 🔒 **Cloudflare Bypass** | Full browser headers for protected sites |
| 🌐 **Universal** | Works with most CTF platforms worldwide |
| ⚡ **Simple** | Just one command for all platforms |

---

## 🎯 Supported Platforms

| Platform | Status | Challenges Tested |
|----------|--------|-------------------|
| **CTFd** | ✅ Full Support | 67+ (0xFun CTF) |
| **picoCTF** | ✅ Full Support | 439+ challenges |
| **Others** | ⚠️ Basic Support | HTML scraping fallback |

### Tested On:
- ✅ 0xFun CTF (CTFd)
- ✅ picoCTF
- ✅ HackTheBox CTF
- ✅ Various university CTFs

---

## 📖 Usage

### The Ultimate Way (Recommended!)

```bash
python3 ctf_scraper_ultimate.py "URL" "COOKIES" ./output
```

**Real Examples:**

```bash
# picoCTF - 439 challenges
python3 ctf_scraper_ultimate.py \
  "https://play.picoctf.org/practice" \
  "sessionid=XXX; csrftoken=YYY" \
  ./picoctf

# 0xFun CTF - 67 challenges
python3 ctf_scraper_ultimate.py \
  "https://ctf.0xfun.org/challenges" \
  "session=XXX; cf_clearance=YYY" \
  ./0xfun

# Any CTFd Platform
python3 ctf_scraper_ultimate.py \
  "https://demo.ctfd.io/challenges" \
  "session=XXX" \
  ./demo
```

## 🛠️ Project Structure

```
ctf_scraper_ultimate.py     # The only tool you need!
requirements.txt            # Dependencies
README.md                   # This file
README.bn.md                # বাংলা ডকুমেন্টেশন
```

**Documentation:**
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [QUICK_REFERENCE.txt](QUICK_REFERENCE.txt) - One-page cheat sheet  
- [GET_FRESH_COOKIES.md](GET_FRESH_COOKIES.md) - Cookie extraction guide
- [WHY_NOT_WORKING.md](WHY_NOT_WORKING.md) - Troubleshooting

---

## 📁 Output Structure

```
output/
├── Web/
│   ├── SQL Injection/
│   │   ├── challenge.txt
│   │   └── app.zip
│   └── XSS Challenge/
│       └── challenge.txt
├── Crypto/
│   └── RSA Baby/
│       ├── challenge.txt
│       └── public.pem
├── Pwn/
├── Reverse/
└── Forensics/
```

Each challenge folder contains:
- `challenge.txt` - Full description, points, tags, author
- Downloaded files (binaries, source code, etc.)

---

## 🔑 Getting Cookies (Easy!)

**Method: Copy as cURL** (30 seconds)

1. Login to the CTF platform
2. Press `F12` → **Network** tab
3. Load the challenges page
4. Right-click any request → **Copy** → **Copy as cURL**
5. Find cookies after `-b`:

```bash
curl 'https://ctf.0xfun.org/challenges' \
  -b 'session=XXX; cf_clearance=YYY'
     ↑_________________________↑
     Copy ONLY this part
```

6. Use immediately (cookies expire in 5-10 minutes!)

📖 **[Detailed Cookie Guide →](GET_FRESH_COOKIES.md)**

---

## 💡 Examples

### Example 1: picoCTF

```bash
python3 ctf_scraper_ultimate.py \
  "https://play.picoctf.org/practice" \
  "sessionid=abc123...; csrftoken=xyz789..." \
  ./picoctf_2024

# ✅ Result: 439 challenges organized by category!
```

### Example 2: 0xFun CTF (Cloudflare Protected)

```bash
python3 ctf_scraper_ultimate.py \
  "https://ctf.0xfun.org/challenges" \
  "session=abc123...; cf_clearance=xyz789..." \
  ./0xfun_ctf

# ✅ Result: 67 challenges with files downloaded!
```

### Example 3: University CTF

```bash
python3 ctf_scraper_ultimate.py \
  "https://university-ctf.edu/challenges" \
  "session=abc123..." \
  ./uni_ctf

# ✅ Auto-detects CTFd and downloads everything!
```

---

## ⚠️ Important Notes

### ✅ DO:
- ✓ Quote the URL: `"https://..."`
- ✓ Quote the cookies: `"session=XXX; cf_clearance=YYY"`
- ✓ Get fresh cookies (< 5 minutes old)
- ✓ Login before getting cookies

### ❌ DON'T:
- ✗ Forget quotes (shell will break!)
- ✗ Use old cookies (they expire quickly)
- ✗ Try to scrape without logging in

---

## 🔧 Troubleshooting

| Issue | Fix |
|-------|-----|
| `zsh: no matches found` | Add quotes around URL |
| `403 Forbidden` | Get fresh cookies |
| `command not found` | Add quotes around cookies |
| Tool not working | Read [WHY_NOT_WORKING.md](WHY_NOT_WORKING.md) |

---

## 📚 Documentation

- **[QUICK_REFERENCE.txt](QUICK_REFERENCE.txt)** - One-page cheat sheet
- **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step beginner guide  
- **[GET_FRESH_COOKIES.md](GET_FRESH_COOKIES.md)** - How to get cookies
- **[WHICH_SCRAPER_TO_USE.md](WHICH_SCRAPER_TO_USE.md)** - Platform guide
- **[WHY_NOT_WORKING.md](WHY_NOT_WORKING.md)** - Troubleshooting
- **[SUMMARY.md](SUMMARY.md)** - Complete overview

---

## 🚀 How It Works

1. **Auto-Detection**: Identifies platform type (CTFd, picoCTF, etc.)
2. **API Access**: Uses platform APIs for fast downloads
3. **Cookie Auth**: Bypasses authentication with your session cookies
4. **Cloudflare Bypass**: Full browser headers for protected sites
5. **Organization**: Auto-categorizes by Web/Crypto/Pwn/etc.
6. **File Downloads**: Grabs all challenge files automatically

---

## 🛠️ Technical Details

### Requirements
- Python 3.6+
- requests
- beautifulsoup4

### Features
- Full Cloudflare bypass headers
- Auto-detection of platform type
- Handles both old and new picoCTF API
- Rate limiting protection (0.5s delays)
- Retry logic for failed downloads
- Smart cookie parsing

### Tested On
- ✅ 0xFun CTF: 67/67 challenges
- ✅ picoCTF: 439/439 challenges
- ✅ Various CTFd platforms

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## ⭐ Star History

If this tool helped you, please consider giving it a star! ⭐

---

<div align="center">

**Made with ❤️ for CTF players worldwide**

[Report Bug](https://github.com/Shoaib-Bin-Rashid/ctf_scapper/issues) • [Request Feature](https://github.com/Shoaib-Bin-Rashid/ctf_scapper/issues)

</div>

---

## 🐛 Troubleshooting

### 403 Forbidden / Cloudflare Issues
- **Problem:** Cookies expired
- **Solution:** Get fresh cookies (F12 → Console → `document.cookie`)

### No Challenges Found
- Try: `python3 ctf_scraper_ultimate.py <URL> -i -v`
- Use: `--platform ctfd` to force CTFd mode

### Validate Cookies
```bash
python3 check_cookies.py
```

---

## 📋 Platform Support

| Platform | Status | Method |
|----------|--------|--------|
| **CTFd** | ✅ Full | API + HTML scraping |
| **Generic** | ✅ Full | HTML parsing fallback |

---

## 🎯 Command Reference

### direct_scraper.py
```bash
python3 direct_scraper.py <COOKIES> [output_dir]
```

### ctf_scraper_ultimate.py
```bash
python3 ctf_scraper_ultimate.py [OPTIONS] <URL>

Options:
  -i, --interactive       Interactive mode
  -c, --cookie COOKIE     Authentication cookie
  -o, --output DIR        Output directory
  -v, --verbose          Verbose output
  --platform TYPE        Force platform (ctfd/generic)
  --dry-run             Preview only
```

---

## 📊 Example Output

Successfully scraped **67 challenges** from 0xFun CTF 2026:
- ✅ 10 categories
- ✅ 40 challenges with files
- ✅ 100% success rate
- ✅ All organized and ready to solve!

---

## 🤝 Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Credits

Built for CTF players who want organized challenge folders! 🎉

**Happy CTF Solving! 🚀**
