# 🎯 Ultimate CTF Scraper

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-CTFd%20%7C%20picoCTF-green.svg)](https://github.com/Shoaib-Bin-Rashid/ctf_scapper)
[![Maintained](https://img.shields.io/badge/maintained-yes-brightgreen.svg)](https://github.com/Shoaib-Bin-Rashid/ctf_scapper/commits/main)

**🚀 ONE UNIVERSAL TOOL FOR ALL CTF PLATFORMS**

*Automatically download and organize CTF challenges from any platform with a single command*

[Quick Start](#-quick-start) • [Features](#-features) • [Usage](#-usage) • [Examples](#-examples) • [Troubleshooting](#-troubleshooting)

---

### 📊 Tested & Verified

| Platform | Status | Challenges Tested |
|----------|--------|-------------------|
| **picoCTF** | ✅ Working | 439/439 |
| **0xFun CTF** | ✅ Working | 67/67 |
| **CTFd Platforms** | ✅ Working | Universal |

</div>

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
```

### Usage

```bash
python3 ctf_scraper_ultimate.py "URL" "COOKIES" ./output
```

**That's it!** The tool will:
1. Auto-detect the platform type
2. Download all challenges
3. Organize them by category
4. Download all associated files

📖 **New to this?** Read the [QUICKSTART.md](QUICKSTART.md) guide

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 Core Features
- **Auto-Detection**: Identifies platform type automatically
- **Universal Support**: Works with CTFd, picoCTF, and more
- **Bulk Download**: Get all challenges in one command
- **Smart Organization**: Auto-categorizes by challenge type

</td>
<td width="50%">

### 🔧 Advanced Features
- **Cloudflare Bypass**: Full browser header simulation
- **File Downloads**: Grabs all challenge files
- **Rate Limiting**: Prevents server bans
- **Error Handling**: Retry logic for failed downloads

</td>
</tr>
</table>

---

## 🎯 Supported Platforms

| Platform Type | Status | Examples | Notes |
|--------------|--------|----------|-------|
| **CTFd** | ✅ Full Support | 0xFun, HackTheBox CTF, university CTFs | Most common platform |
| **picoCTF** | ✅ Full Support | play.picoctf.org | 439+ challenges tested |
| **Generic** | ⚠️ Basic | HTML scraping fallback | Limited features |

### Platform-Specific Features

<details>
<summary><b>CTFd Platforms</b></summary>

- ✅ Full API access
- ✅ Challenge descriptions
- ✅ File downloads
- ✅ Points and solve counts
- ✅ Tags and categories
- ✅ Author information

</details>

<details>
<summary><b>picoCTF</b></summary>

- ✅ All events supported
- ✅ Challenge metadata
- ✅ Difficulty ratings
- ✅ Category classification
- ⚠️ Limited descriptions (API limitation)

</details>

---

## 📖 Usage

### Basic Command

```bash
python3 ctf_scraper_ultimate.py "<CTF_URL>" "<COOKIES>" <OUTPUT_DIR>
```

### Command-Line Arguments

| Argument | Description | Required | Example |
|----------|-------------|----------|---------|
| `URL` | CTF challenges page URL | ✅ Yes | `"https://ctf.0xfun.org/challenges"` |
| `COOKIES` | Authentication cookies | ✅ Yes | `"session=XXX; cf_clearance=YYY"` |
| `OUTPUT_DIR` | Output directory path | ✅ Yes | `./my_ctf` |

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

| Platform | Required Cookies |
|----------|------------------|
| **CTFd** | `session` + `cf_clearance` (if Cloudflare protected) |
| **picoCTF** | `sessionid` + `csrftoken` |

---

## 💡 Examples

### Example 1: picoCTF (439 Challenges)

```bash
python3 ctf_scraper_ultimate.py \
  "https://play.picoctf.org/practice" \
  "sessionid=93wmny7jqfeo6k3w8a50xq65mcr1g5jy; csrftoken=yK8PNkcgMzeR9A0Hi6HR5BLNW3iMN6cM" \
  ./picoctf_challenges
```

**Output:**
```
✅ Successfully scraped 439/439 challenges
📂 Output: ./picoctf_challenges
```

### Example 2: 0xFun CTF (Cloudflare Protected)

```bash
python3 ctf_scraper_ultimate.py \
  "https://ctf.0xfun.org/challenges" \
  "session=361efa74-78d6-41de-9259-8ec23fc7caaa.gZYiouxDqovVGIfeBOUlNpNg3CE; cf_clearance=t4GYXCrc48TbyUz7uhiMHirvtwIMgnZlG76Mngadi8M-1770991935-1.2.1.1" \
  ./0xfun_ctf
```

**Output:**
```
✅ Successfully scraped 67/67 challenges
📂 Output: ./0xfun_ctf
```

### Example 3: Any CTFd Platform

```bash
python3 ctf_scraper_ultimate.py \
  "https://demo.ctfd.io/challenges" \
  "session=your_session_cookie_here" \
  ./demo_ctf
```

---

## 📁 Output Structure

The tool creates a well-organized folder structure:

```
output_directory/
├── Web/
│   ├── SQL_Injection_101/
│   │   ├── challenge.txt      # Challenge description
│   │   └── app.zip            # Challenge files
│   └── XSS_Challenge/
│       ├── challenge.txt
│       └── source.html
├── Crypto/
│   ├── RSA_Baby/
│   │   ├── challenge.txt
│   │   └── public.pem
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
- Challenge name and category
- Point value
- Solve count
- Tags
- Full description
- File URLs (if any)

---


## 🔧 Advanced Troubleshooting

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

| Metric | Value |
|--------|-------|
| **Platforms Supported** | 3+ (CTFd, picoCTF, Generic) |
| **Challenges Tested** | 500+ |
| **Success Rate** | >95% |
| **Average Speed** | ~2 challenges/second |

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
