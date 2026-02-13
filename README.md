# CTF Scraper & Organizer - Ultimate Edition

🎯 **One tool to download and organize all your CTF challenges automatically!**

Automated tool to scrape CTF competition websites, download all problems with their statements and files, and organize them into a structured folder hierarchy by category.

## ✨ Features

- 🎯 **Multi-platform support**: CTFd, rCTF, and custom platforms
- 🔐 **Smart authentication**: Automatic detection + interactive cookie input
- 📁 **Auto-organization**: Categorizes by type (Pwn, Web, Crypto, Reverse, etc.)
- 📥 **Batch downloads**: Automatically downloads all challenge files
- 🎨 **Clean structure**: Organized folder hierarchy for easy navigation
- 🔄 **Retry logic**: Automatic retries with exponential backoff
- 👁️ **Dry-run mode**: Preview before downloading
- 🎨 **Beautiful CLI**: Colored output with progress indicators
- 🤖 **Platform auto-detection**: Automatically detects CTF platform type

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/Shoaib-Bin-Rashid/ctf_scapper.git
cd ctf_scapper

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Usage

#### 🌟 **Ultimate Tool** (Recommended - Interactive Mode)

```bash
# Interactive mode - asks for cookie if needed
python ctf_scraper_ultimate.py https://ctf.example.com/challenges -i

# Or provide cookie directly
python ctf_scraper_ultimate.py https://ctf.example.com/challenges \
  -c "session=YOUR_COOKIE" -v
```

#### 📝 **Standard Tool**

```bash
# Basic usage
python ctf_scraper.py https://ctf.example.com/challenges

# With authentication
python ctf_scraper.py https://ctf.example.com/challenges \
  --cookie "session=YOUR_COOKIE"

# Preview before downloading (dry-run)
python ctf_scraper.py https://ctf.example.com/challenges --dry-run
```

#### 🔧 **Bash Wrapper**

```bash
# Easiest way - automatic dependency check
./scrape_ctf.sh https://ctf.example.com/challenges
```

## 📖 Getting Your Session Cookie

The tool needs a session cookie for authenticated CTFs. Here's how:

1. **Open the CTF website** in your browser
2. **Login** to your account
3. **Press F12** to open Developer Tools
4. Go to **Application** (Chrome) or **Storage** (Firefox)
5. Click **Cookies** → Select the CTF domain
6. Find the `session` cookie
7. **Copy its value**

### Quick Console Method
In browser console (F12 → Console):
```javascript
document.cookie
```
Copy the entire output.

## 📂 Output Structure

```
ctf_challenges/
└── CTF_Name/
    ├── Pwn/
    │   ├── buffer_overflow/
    │   │   ├── statement.txt
    │   │   └── files/
    │   │       ├── vuln_binary
    │   │       └── libc.so.6
    │   └── rop_chain/
    │       └── statement.txt
    ├── Web/
    │   └── sql_injection/
    │       ├── statement.txt
    │       └── files/
    ├── Crypto/
    ├── Reverse/
    ├── Forensics/
    └── Misc/
```

## 🎯 Advanced Usage

### Configuration File

Create `config.yaml`:
```yaml
auth:
  cookie: "session=your_session_cookie"

categories:
  pwn: ["pwn", "binary", "exploitation"]
  web: ["web", "webapp", "xss", "sqli"]
  crypto: ["crypto", "rsa", "aes"]
  reverse: ["reverse", "rev", "crackme"]
  forensics: ["forensics", "stego", "pcap"]
  misc: ["misc", "trivia"]

output_dir: "./ctf_challenges"
```

Then run:
```bash
python ctf_scraper.py <URL> --config config.yaml
```

### All Command Options

```bash
# Ultimate Tool
python ctf_scraper_ultimate.py [OPTIONS] <URL>

Options:
  -i, --interactive       Interactive mode (recommended)
  -c, --cookie COOKIE     Authentication cookie
  -t, --token TOKEN       API token
  -o, --output DIR        Output directory (default: ./ctf_challenges)
  -p, --platform TYPE     Platform: ctfd, generic, auto (default: auto)
  --dry-run              Preview without downloading
  -v, --verbose          Verbose output
  --force                Force even if auth fails
  -h, --help             Show help message
```

## 🔍 Platform Support

| Platform | Status | Features |
|----------|--------|----------|
| **CTFd** | ✅ Full | API + HTML scraping, auto-detection |
| **Generic** | ✅ Full | HTML parsing, fallback for unknown platforms |
| **rCTF** | 🚧 Coming | Planned for next version |

## 💡 Examples

### Example 1: Test with Dry Run
```bash
python ctf_scraper_ultimate.py https://ctf.0xfun.org/challenges \
  --dry-run -v
```

### Example 2: Authenticated Scraping
```bash
python ctf_scraper_ultimate.py https://ctf.0xfun.org/challenges \
  -c "session=eyJhbGciOiJIUzI1NiJ9..." \
  -o ~/CTFs/0xfun_2026 \
  -v
```

### Example 3: Interactive Mode
```bash
python ctf_scraper_ultimate.py https://ctf.0xfun.org/challenges -i
# Tool will ask for cookie if needed
```

### Example 4: Generic Platform
```bash
python ctf_scraper_ultimate.py https://custom-ctf.com/challenges \
  --platform generic -v
```

## 🐛 Troubleshooting

### "403 Forbidden" Error
**Solution**: The CTF requires authentication.
```bash
python ctf_scraper_ultimate.py <URL> -i
```

### "No challenges found"
**Solutions**:
1. Check if URL points to challenges page
2. Try with authentication: `-i` or `-c "cookie"`
3. Try generic scraper: `--platform generic`
4. Use verbose mode: `-v`

### Files not downloading
**Solutions**:
- Check internet connection
- Verify file URLs need authentication
- Use `-v` to see which files fail

### Wrong categories
**Solution**: Customize in `config.yaml`

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Detailed setup and usage guide
- **[TEST_GUIDE.md](test_run/TEST_GUIDE.md)** - Testing instructions
- **[examples.sh](examples.sh)** - Usage examples

## 🛠️ Development

### Project Structure
```
ctf_scrapper/
├── ctf_scraper_ultimate.py  ⭐ Main ultimate tool
├── ctf_scraper.py           Standard CLI
├── scraper_base.py          Base scraper class
├── ctfd_scraper.py          CTFd platform support
├── generic_scraper.py       Generic fallback
├── scrape_ctf.sh            Bash wrapper
├── requirements.txt         Dependencies
└── config.example.yaml      Config template
```

### Dependencies
- `requests` - HTTP client
- `beautifulsoup4` - HTML parsing
- `lxml` - Fast XML/HTML processing
- `pyyaml` - Configuration files
- `colorama` - Colored terminal output

## 🤝 Contributing

Contributions welcome! Please feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Add support for more platforms

## 📝 License

MIT License - See [LICENSE](LICENSE) file

## 🎓 Use Cases

Perfect for:
- 🏆 CTF players organizing challenges
- 📚 Archiving CTF competitions
- 🔍 Analyzing challenge distributions
- 📁 Offline challenge access
- 🎯 Team collaboration on CTFs

## ⚡ Performance

- **Fast**: Parallel downloads with connection pooling
- **Smart**: Auto-retry with exponential backoff
- **Efficient**: Dry-run mode prevents wasted bandwidth
- **Reliable**: Comprehensive error handling

## 🌟 Why This Tool?

❌ **Before**: Manually clicking, downloading, organizing each challenge  
✅ **After**: One command, everything organized perfectly!

---

**Made with ❤️ for the CTF community**

*Happy hacking! 🚀*
