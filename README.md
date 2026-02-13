# CTF Scraper & Organizer

Automated tool to scrape CTF competition websites, download all problems with their statements and files, and organize them into a structured folder hierarchy.

## Features

- 🎯 **Multi-platform support**: CTFd, rCTF, and custom platforms
- 🔐 **Authentication**: Support for both public and authenticated CTFs
- 📁 **Auto-organization**: Categorizes problems by type (Pwn, Web, Crypto, Reverse, etc.)
- 📥 **File downloads**: Automatically downloads all challenge files
- 🎨 **Clean structure**: Organized folder hierarchy for easy navigation

## Installation

```bash
# Clone the repository
git clone https://github.com/Shoaib-Bin-Rashid/ctf_scapper.git
cd ctf_scapper

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
# Scrape a public CTF
python ctf_scraper.py https://ctf.example.com/challenges

# Or use the bash wrapper
./scrape_ctf.sh https://ctf.example.com/challenges
```

### With Authentication
```bash
# Using session cookie
python ctf_scraper.py https://ctf.example.com/challenges --cookie "session=your_session_cookie"

# Using config file
python ctf_scraper.py https://ctf.example.com/challenges --config config.yaml
```

### Advanced Options
```bash
# Specify output directory
python ctf_scraper.py https://ctf.example.com/challenges -o ./my_ctf

# Dry run (preview without downloading)
python ctf_scraper.py https://ctf.example.com/challenges --dry-run

# Verbose output
python ctf_scraper.py https://ctf.example.com/challenges -v
```

## Folder Structure

```
<CTF_NAME>/
├── Pwn/
│   ├── buffer_overflow/
│   │   ├── statement.txt
│   │   └── files/
│   │       ├── vuln_binary
│   │       └── libc.so.6
├── Web/
│   ├── sql_injection/
│   │   ├── statement.txt
│   │   └── files/
│   │       └── source.zip
├── Crypto/
├── Reverse/
├── Misc/
└── Forensics/
```

## Configuration

Create a `config.yaml` file:

```yaml
auth:
  cookie: "session=your_session_cookie"
  # or
  token: "your_api_token"

categories:
  pwn: ["pwn", "binary", "exploitation"]
  web: ["web", "webapp", "website"]
  crypto: ["crypto", "cryptography"]
  reverse: ["reverse", "rev", "reversing"]
  forensics: ["forensics", "steganography", "stego"]
  misc: ["misc", "miscellaneous"]

output_dir: "./ctf_challenges"
```

## Supported Platforms

- ✅ CTFd
- 🚧 rCTF (coming soon)
- 🚧 Custom platforms (generic scraper)

## Requirements

- Python 3.8+
- requests
- beautifulsoup4
- lxml
- pyyaml

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

MIT License
