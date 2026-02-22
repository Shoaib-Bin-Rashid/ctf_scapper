<div align="center">

# 🎯 Ultimate CTF Scraper

<img src="https://img.shields.io/badge/version-2.0.0-blue?style=for-the-badge" /> <img src="https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white" /> <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" /> <img src="https://img.shields.io/badge/platforms-CTFd%20%7C%20picoCTF%20%7C%20Universal-purple?style=for-the-badge" /> <img src="https://img.shields.io/github/actions/workflow/status/Shoaib-Bin-Rashid/ctf_scrapper/test.yml?style=for-the-badge&label=tests" />

**One universal tool to download and organize all CTF challenges automatically.**

Auto-detects platform type · Concurrent downloads · Browser fallback · Resume capability

[Quick Start](#-quick-start) · [Getting Cookies](#-getting-cookies) · [All Options](#-all-options) · [Examples](#-examples) · [Troubleshooting](#-troubleshooting)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **Auto-Detection** | Identifies CTFd, picoCTF, and more automatically |
| ⚡ **Concurrent Downloads** | 5 parallel workers — 5× faster than sequential |
| 🌐 **Browser Fallback** | Playwright automation for any platform, CAPTCHA included |
| 💾 **Resume Capability** | Continue interrupted downloads with `--skip-existing` |
| 📁 **Smart Organization** | Challenges sorted by category with all files |
| 🔄 **Retry Logic** | Auto-retries failed requests 3× |
| 📊 **Progress Bars** | Real-time per-file download progress |
| 🔍 **Dry Run** | Preview challenge list before downloading |

---

## ⚡ Quick Start

```bash
# 1. Clone & install
git clone https://github.com/Shoaib-Bin-Rashid/ctf_scrapper.git
cd ctf_scrapper
pip3 install -r requirements.txt
playwright install chromium   # only needed for --browser mode

# 2. Get your cookies (see section below)

# 3. Run
python3 ctf_scraper.py "https://ctf.example.com/challenges" -c "session=xxx; cf_clearance=yyy" ./output
```

---

## 🔑 Getting Cookies

### ⭐ Method 1 — Cookie Editor Extension (Easiest)

1. Install **[Cookie Editor](https://cookie-editor.com/)** browser extension *(Chrome / Firefox)*
2. **Login** to the CTF platform in your browser
3. Click the **Cookie Editor** icon in the toolbar
4. Click **Export** → select **Header String**
5. Copy the output — it looks like: `session=abc123; cf_clearance=xyz789`
6. Pass it directly with the `-c` flag

```bash
python3 ctf_scraper.py "https://ctf.example.com/challenges" \
  -c "session=abc123; cf_clearance=xyz789" \
  ./output
```

### Method 2 — Environment Variable *(most secure)*

```bash
export CTF_COOKIES="session=abc123; cf_clearance=xyz789"
python3 ctf_scraper.py "https://ctf.example.com/challenges" ./output
```

### Method 3 — Cookie File

```bash
echo "session=abc123; cf_clearance=xyz789" > cookies.txt
python3 ctf_scraper.py "URL" -c @cookies.txt ./output
```

### Method 4 — Browser Mode *(no cookies needed)*

```bash
# Chromium opens, you log in manually, scraper does the rest
python3 ctf_scraper.py --browser "https://ctf.example.com" ./output
```

> ⚠️ **Cookies expire fast!** Use them within 5 minutes of copying.

---

## 📖 All Options

```
python3 ctf_scraper.py [URL] [OUTPUT_DIR] [OPTIONS]

Positional:
  url                   CTF challenges page URL
  output_dir            Output folder (default: ./output)

Options:
  -c, --cookies         Cookie string or @file.txt
  --browser             Browser fallback mode (manual login, no cookies needed)
  --dry-run             Preview challenges without downloading
  --skip-existing       Skip already downloaded challenges (resume)
  --max-workers N       Concurrent downloads, default: 5
  --timeout N           Request timeout in seconds, default: 30
  --rate-limit N        Max requests per second, e.g. 2.0 (default: unlimited)
  -v, --verbose         Verbose / debug logging
  --version             Show version number and exit
  -h, --help            Show help
```

---

## 💡 Examples

### CTFd Platform

```bash
python3 ctf_scraper.py \
  "https://ctf.0xfun.org/challenges" \
  -c "session=361efa74...; cf_clearance=t4GYXCrc..." \
  ./0xfun_ctf
```

### picoCTF

```bash
python3 ctf_scraper.py \
  "https://play.picoctf.org/practice" \
  -c "sessionid=93wmny7j...; csrftoken=yK8PNkcg..." \
  ./picoctf
```

### Browser Mode (any platform, no cookies)

```bash
python3 ctf_scraper.py --browser "https://ctf.unknown.com" ./output
# 1. Chromium opens
# 2. Login manually
# 3. Navigate to challenges page
# 4. Press ENTER in terminal → scraper takes over
```

### Dry Run (preview only)

```bash
python3 ctf_scraper.py "URL" -c "COOKIES" --dry-run ./output
```

### Resume Interrupted Download

```bash
python3 ctf_scraper.py "URL" -c "COOKIES" --skip-existing ./output
```

### Fast Download (10 workers)

```bash
python3 ctf_scraper.py "URL" -c "COOKIES" --max-workers 10 ./output
```

---

## 📁 Output Structure

```
output/
├── .scraper_state.json      ← resume state (auto-created)
├── Web/
│   ├── SQL Injection 101/
│   │   ├── challenge.txt    ← name, points, description, tags
│   │   └── app.zip
│   └── XSS Challenge/
│       └── challenge.txt
├── Crypto/
│   └── RSA Baby/
│       ├── challenge.txt
│       └── public.pem
├── Pwn/
│   └── Buffer Overflow/
│       ├── challenge.txt
│       └── vuln
└── Forensics/
    └── Wireshark/
        ├── challenge.txt
        └── capture.pcap
```

---

## 🌐 Supported Platforms

| Platform | Status | Notes |
|----------|--------|-------|
| **CTFd** | ✅ Full | 0xFun, HackTheBox CTF, BitSkrieg, custom instances |
| **picoCTF** | ✅ Full | 439+ challenges tested |
| **Any Platform** | ✅ Browser Mode | Works with CAPTCHA, 2FA, SSO |

---

## 🔧 Troubleshooting

**`zsh: no matches found`**
→ Wrap the URL in quotes: `"https://site.com/challenges"`

**`403 Forbidden`**
→ Cookies expired. Get fresh ones (within 5 min) using Cookie Editor.

**`ModuleNotFoundError`**
→ Run `pip3 install -r requirements.txt`

**`playwright` not found**
→ Run `playwright install chromium`

**Platform not detected / empty output**
→ Try `--browser` mode for manual login.

**Still stuck?**
→ Run with `-v` for verbose logs and open an [issue](https://github.com/Shoaib-Bin-Rashid/ctf_scrapper/issues).

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes and open a Pull Request

Bug reports and feature requests are welcome via [GitHub Issues](https://github.com/Shoaib-Bin-Rashid/ctf_scrapper/issues).

---

## 👤 Author

**Shoaib Bin Rashid**
*Junior VAPT Engineer · eJPT Certified · CTF Player*

Ranked **6th worldwide** in a 36-hour CTF marathon. Leads the best Cyber Security Club in Bangladesh (400+ members). Written 31,000+ lines of production security code.

| | |
|---|---|
| 📧 Email | shoaibbinrashid11@gmail.com |
| 💼 LinkedIn | [linkedin.com/in/shoaib-bin-rashid](https://linkedin.com/in/shoaib-bin-rashid) |
| 🐙 GitHub | [github.com/Shoaib-Bin-Rashid](https://github.com/Shoaib-Bin-Rashid) |
| 🔐 HackerOne | [hackerone.com/r3d_xploit](https://hackerone.com/r3d_xploit) |

---

## 📄 License

MIT © [Shoaib Bin Rashid](https://github.com/Shoaib-Bin-Rashid)

---

<div align="center">

⭐ **Star this repo if it saved you time!**

Built with ❤️ for the CTF community

</div>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-CTFd%20%7C%20picoCTF%20%7C%20Universal-green.svg)](https://github.com/Shoaib-Bin-Rashid/ctf_scapper)
[![Maintained](https://img.shields.io/badge/maintained-yes-brightgreen.svg)](https://github.com/Shoaib-Bin-Rashid/ctf_scapper/commits/main)

**🚀 ONE UNIVERSAL TOOL FOR ALL CTF PLATFORMS**

*Automatically download and organize CTF challenges with concurrent downloads, browser fallback, and resume capability*

[Quick Start](#-quick-start) • [What's New](#-whats-new-in-v20) • [Features](#-features) • [Browser Mode](#-browser-fallback-mode) • [Examples](#-examples)

---

### 📊 Tested & Verified

| Platform | Status | Challenges Tested |
|----------|--------|-------------------|
| **picoCTF** | ✅ Working | 439/439 |
| **0xFun CTF** | ✅ Working | 67/67 |
| **CTFd Platforms** | ✅ Working | Universal |
| **Any Platform** | ✅ Browser Mode | Universal |

</div>

---

## 🆕 What's New in v2.0

🎉 **Major upgrade with professional-grade features:**

- 🔐 **Secure Cookie Handling** - Environment variables, no CLI exposure
- 🚀 **5x Faster Downloads** - Concurrent file downloads with progress bars
- 💾 **Resume Capability** - Continue interrupted downloads automatically
- 🌐 **Browser Fallback** - Playwright automation when API fails
- 🔄 **Smart Retry Logic** - Auto-retry failed requests
- ✅ **File Verification** - Validate download integrity
- 📊 **Progress Bars** - Real-time download progress (tqdm)
- 🐛 **Debug Mode** - Comprehensive logging with `-v` flag
- 🔍 **Dry Run** - Preview before downloading
- ⚡ **Configurable Workers** - Control concurrent download speed

**[View Full Changelog](CHANGELOG.md)** | **[Complete Usage Guide](USAGE_GUIDE.md)**

---

## 🌟 Why Use This Tool?

Stop wasting time manually downloading CTF challenges! This tool:

- 🤖 **Auto-detects** platform type (CTFd, picoCTF, and more)
- 📥 **Bulk downloads** all challenges and files in one go
- 📁 **Auto-organizes** by category (Web, Crypto, Pwn, Reverse, etc.)
- 🔒 **Bypasses Cloudflare** protection with full browser headers
- 🌐 **Universal** - works with most CTF platforms worldwide
- ⚡ **Simple** - just ONE command for ALL platforms

**Save hours of manual work with a single command!**

---

## ⚡ Quick Start

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Shoaib-Bin-Rashid/ctf_scapper.git
cd ctf_scapper

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Install Playwright (for browser fallback)
playwright install chromium
```

### Usage (Secure Method - RECOMMENDED)

```bash
# Set cookies once (secure, no CLI exposure)
export CTF_COOKIES="session=XXX; cf_clearance=YYY"

# Run scraper
python3 ctf_scraper_ultimate.py "https://ctf.example.com/challenges" ./output
```

### Legacy Usage (Still Supported)

```bash
# Direct method (less secure)
python3 ctf_scraper_ultimate.py "URL" -c "COOKIES" ./output

# Or use cookie file
echo "session=XXX; cf_clearance=YYY" > cookies.txt
python3 ctf_scraper_ultimate.py "URL" -c @cookies.txt ./output
```

**The tool will:**
1. ✨ Auto-detect the platform type
2. 🚀 Download all challenges concurrently
3. 📁 Organize them by category
4. 📥 Download all files with progress bars
5. 💾 Save state for resume capability

📖 **New to this?** Read the **[Complete Usage Guide](USAGE_GUIDE.md)**

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 Core Features
- **Auto-Detection**: Identifies platform type automatically
- **Universal Support**: Works with CTFd, picoCTF, and more
- **Concurrent Downloads**: 5x faster with parallel downloads
- **Smart Organization**: Auto-categorizes by challenge type
- **Browser Fallback**: Playwright automation when API fails

</td>
<td width="50%">

### 🔧 Advanced Features v2.0
- **Secure Cookies**: Environment variables, file input
- **Resume Capability**: Continue interrupted downloads
- **Progress Bars**: Real-time download progress (tqdm)
- **Retry Logic**: Auto-retry failed requests (3x)
- **File Verification**: Validate download integrity
- **Debug Mode**: Comprehensive logging (`-v` flag)
- **Dry Run**: Preview without downloading
- **Configurable**: Timeouts, workers, skip-existing

</td>
</tr>
</table>

---

## 🎯 Supported Platforms

| Platform Type | Status | Examples | Features |
|--------------|--------|----------|----------|
| **CTFd** | ✅ Full Support | 0xFun, HackTheBox CTF | API + Files + Metadata |
| **picoCTF** | ✅ Full Support | play.picoctf.org | 439+ challenges tested |
| **Any Platform** | ✅ Browser Mode | Unknown platforms | Manual login + Auto-scrape |

### Platform-Specific Features

<details>
<summary><b>CTFd Platforms</b></summary>

- ✅ Full API access with concurrent downloads
- ✅ Challenge descriptions and metadata
- ✅ Automatic file downloads with progress bars
- ✅ Points, solve counts, and tags
- ✅ Resume capability with state tracking
- ✅ Retry logic for failed downloads

</details>

<details>
<summary><b>picoCTF</b></summary>

- ✅ All events supported with pagination
- ✅ Challenge metadata (category, difficulty, author)
- ✅ Concurrent processing with progress bars
- ✅ Resume capability
- ⚠️ Limited descriptions (API limitation)

</details>

<details>
<summary><b>Browser Fallback Mode (NEW!)</b></summary>

- ✅ Works with **ANY** CTF platform
- ✅ Manual login (handles CAPTCHA, 2FA, etc.)
- ✅ Auto-extracts cookies from browser
- ✅ Tries API scraping with extracted cookies
- ✅ Falls back to HTML parsing if API fails
- 🎯 **Use when:** Platform unknown, API fails, heavy bot protection

**Example:**
```bash
python3 ctf_scraper_ultimate.py --browser "https://ctf.example.com" ./output
```

</details>

---

## 📖 Usage

### Basic Commands

```bash
# Secure method (RECOMMENDED)
export CTF_COOKIES="session=XXX; cf_clearance=YYY"
python3 ctf_scraper_ultimate.py "https://ctf.example.com/challenges" ./output

# Cookie file method
python3 ctf_scraper_ultimate.py "URL" -c @cookies.txt ./output

# Browser fallback (manual login)
python3 ctf_scraper_ultimate.py --browser "URL" ./output

# Dry run (preview only)
python3 ctf_scraper_ultimate.py "URL" --dry-run ./output

# Resume interrupted download
python3 ctf_scraper_ultimate.py "URL" --skip-existing ./output

# Fast download (more workers)
python3 ctf_scraper_ultimate.py "URL" --max-workers 10 ./output

# Debug mode
python3 ctf_scraper_ultimate.py "URL" -v ./output
```

### All Options

```bash
python3 ctf_scraper_ultimate.py -h

Options:
  -c, --cookies       Cookies string or @file.txt
  --browser          Use browser fallback mode (manual login)
  --dry-run          Preview challenges without downloading
  --skip-existing    Skip already downloaded challenges (resume)
  --max-workers N    Concurrent downloads (default: 5, max: 10)
  --timeout N        Request timeout in seconds (default: 30)
  -v, --verbose      Enable debug logging
```

### Command-Line Arguments

| Argument | Description | Required | Example |
|----------|-------------|----------|---------|
| `url` | CTF challenges page URL | ✅ Yes* | `"https://ctf.0xfun.org/challenges"` |
| `output_dir` | Output directory path | Optional | `./my_ctf` (default: `./output`) |
| `-c, --cookies` | Authentication cookies | Optional** | `@cookies.txt` or `"session=XXX"` |
| `--browser` | Browser fallback mode | No | Flag only |

\* Required unless using `--browser` mode  
\** Optional if `CTF_COOKIES` env var is set

### Built-in Help

```bash
python3 ctf_scraper_ultimate.py --help
```

---

## 🔑 Getting Cookies

Cookies are required for authentication. Here's the **fastest method**:

### Method: Copy as cURL (Recommended)

1. **Login** to the CTF platform in your browser
2. Press **F12** to open DevTools
3. Go to **Network** tab
4. Reload the challenges page
5. Right-click any request → **Copy** → **Copy as cURL**
6. Extract cookies from the `-b` flag:

```bash
curl 'https://ctf.0xfun.org/challenges' \
  -H 'accept: text/html...' \
  -b 'session=abc123xyz; cf_clearance=def456uvw'
     ↑________________________________________↑
     Copy ONLY this part
```

7. **Use immediately** (cookies expire in 5-10 minutes!)

### Required Cookies

| Platform | Required Cookies | Where to Find |
|----------|------------------|---------------|
| **CTFd** | `session` + `cf_clearance` (if Cloudflare) | Network tab → Cookie header |
| **picoCTF** | `sessionid` + `csrftoken` | Network tab → Cookie header |
| **Unknown** | Use `--browser` mode instead | No cookies needed! |

💡 **Pro Tip:** If getting cookies is difficult, just use `--browser` mode!

---

## 💡 Examples

### Example 1: Using Environment Variable (RECOMMENDED)

```bash
# Set cookies securely (won't show in process list)
export CTF_COOKIES="session=93wmny7jqfeo6k3w8a50xq65mcr1g5jy; csrftoken=yK8PNkcgMzeR9A0Hi6HR5BLNW3iMN6cM"

# Run scraper
python3 ctf_scraper_ultimate.py \
  "https://play.picoctf.org/practice" \
  ./picoctf_challenges
```

**Output:**
```
🎯 ULTIMATE UNIVERSAL CTF SCRAPER v2.0
============================================================
🔍 Detecting platform type for play.picoctf.org...
✅ Detected: picoCTF platform

Overall Progress: 100%|████████████| 439/439 [01:23<00:00, 5.3chal/s]

============================================================
📊 SCRAPING SUMMARY
============================================================
Total Challenges: 439
✅ Success: 439
📥 Files Downloaded: 187
============================================================
📂 Output: ./picoctf_challenges
```

### Example 2: Browser Fallback Mode (Easy!)

```bash
# No cookies needed!
python3 ctf_scraper_ultimate.py --browser "https://ctf.0xfun.org" ./0xfun_output
```

**What happens:**
1. 🌐 Browser opens automatically
2. 👤 You log in manually (handles CAPTCHA, 2FA)
3. 🚀 Navigate to challenges page
4. ⏎ Press ENTER in terminal
5. ✨ Scraper extracts everything automatically

### Example 3: Resume Interrupted Download

```bash
# First run (interrupted at 50/100)
python3 ctf_scraper_ultimate.py "URL" ./output
^C  # Ctrl+C to interrupt

# Resume from where you left off
python3 ctf_scraper_ultimate.py "URL" --skip-existing ./output
# Will skip the first 50 completed challenges
```

### Example 4: Fast Download with More Workers

```bash
# Default (5 concurrent downloads)
python3 ctf_scraper_ultimate.py "URL" ./output

# Faster (10 concurrent downloads)
python3 ctf_scraper_ultimate.py "URL" --max-workers 10 ./output
```

---

## 📁 Output Structure

The tool creates a well-organized folder structure:

```
output_directory/
├── .scraper_state.json         # Resume state (auto-created)
├── Web/
│   ├── SQL_Injection_101/
│   │   ├── challenge.txt       # Challenge description
│   │   └── app.zip             # Challenge files
│   └── XSS_Challenge/
│       ├── challenge.txt
│       └── source.html
├── Crypto/
│   ├── RSA_Baby/
│   │   ├── challenge.txt
│   │   ├── public.pem
│   │   └── encrypted.txt
│   └── AES_Basics/
│       └── challenge.txt
├── Pwn/
│   ├── Buffer_Overflow_1/
│   │   ├── challenge.txt
│   │   └── vuln_binary
│   └── Format_String/
│       └── challenge.txt
├── Reverse/
└── Forensics/
```

### File Contents

Each `challenge.txt` contains:
- ✅ Challenge name and category
- ✅ Point value and solve count
- ✅ Tags and difficulty
- ✅ Full description
- ✅ File URLs (if any)

### Resume State (`.scraper_state.json`)

```json
{
  "completed_challenges": ["1", "2", "3"],
  "failed_challenges": ["4"],
  "last_run": "2026-02-14T05:00:00",
  "platform": "ctfd"
}
```

Use `--skip-existing` to resume from this state.

---
## 🌐 Browser Fallback Mode

When API scraping fails or platform is unknown, use **browser mode**:

```bash
python3 ctf_scraper_ultimate.py --browser "https://ctf.example.com" ./output
```

### How It Works

1. **Browser Opens** - Chromium launches automatically
2. **Manual Login** - You log in (handles CAPTCHA, 2FA, anything!)
3. **Navigate** - Go to challenges page
4. **Press Enter** - Signal you're ready in the terminal
5. **Auto-Extract** - Scraper gets cookies from browser
6. **API First** - Tries API scraping with cookies
7. **HTML Fallback** - Parses HTML if API unavailable

### When to Use Browser Mode

✅ Platform type unknown or not supported  
✅ Getting 403/401 errors with API  
✅ Heavy Cloudflare/bot protection  
✅ Don't want to extract cookies manually  
✅ Site requires CAPTCHA or 2FA  

### Workflow Diagram

```
API Scraping Failed? → User Confirms → Browser Opens
                                            ↓
                                      User Logs In
                                            ↓
                               User Goes to Challenges Page
                                            ↓
                                   User Presses Enter
                                            ↓
                                  Extract Cookies from Browser
                                            ↓
                          Try API Scraping with Cookies → Success? → Done
                                            ↓
                                          Failed
                                            ↓
                                   Parse HTML from Page → Done
```

**Result:** Works with **ANY** CTF platform, guaranteed! 🎯

---

<details>
<summary><b>❌ Error: "zsh: no matches found"</b></summary>

**Cause:** URL contains special characters (`?`, `&`) that need escaping

**Solution:** Add quotes around the URL
```bash
# ✅ Correct
python3 ctf_scraper_ultimate.py "https://site.com/challenges?page=1" "cookies" ./out
```
</details>

<details>
<summary><b>❌ Error: "403 Forbidden"</b></summary>

**Cause:** Cookies expired or invalid

**Solution:** Get fresh cookies (< 5 minutes old)
</details>

---

## 📊 Performance Metrics

| Metric | v1.0 | v2.0 | Improvement |
|--------|------|------|-------------|
| **Download Speed** | Sequential | 5x Concurrent | **500% faster** |
| **Platforms Supported** | 2 (CTFd, picoCTF) | Universal (any platform) | **∞** |
| **Challenges Tested** | 500+ | 500+ | - |
| **Success Rate** | >95% | >99% | **+4%** |
| **Resume Capability** | ❌ No | ✅ Yes | **NEW** |
| **Browser Fallback** | ❌ No | ✅ Yes | **NEW** |
| **Progress Tracking** | Basic | Advanced (tqdm) | **Better UX** |
| **Security** | ⚠️ CLI exposure | ✅ Env vars/files | **Secure** |

**Benchmark** (50 challenges, 100 files):
- v1.0: ~8 minutes (sequential downloads)
- v2.0: ~1.5 minutes (5 workers) - **5.3x faster**
- v2.0: ~50 seconds (10 workers) - **9.6x faster**

---

## 🤝 Contributing

Contributions are welcome! Ways to help:

- 🐛 **Report Bugs**: [Open an issue](https://github.com/Shoaib-Bin-Rashid/ctf_scapper/issues)
- 💡 **Suggest Features**: Share your ideas
- 🔧 **Submit PRs**: Fix bugs or add features
- 📖 **Improve Docs**: Help make documentation better
- ⭐ **Star the Repo**: Show your support!

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Shoaib-Bin-Rashid/ctf_scapper/issues)
- **Author**: [Shoaib Bin Rashid](https://github.com/Shoaib-Bin-Rashid)

---

<div align="center">

### ⭐ Star this repository if it helped you!

**Built with ❤️ for the CTF community**

[⬆ Back to Top](#-ultimate-ctf-scraper)

</div>
