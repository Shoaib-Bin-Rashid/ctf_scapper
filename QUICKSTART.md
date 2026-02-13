# Quick Start Guide

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Shoaib-Bin-Rashid/ctf_scapper.git
   cd ctf_scapper
   ```

2. **Set up virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Basic Usage

### Method 1: Using Python directly
```bash
# Activate virtual environment first
source venv/bin/activate

# Run scraper
python ctf_scraper.py https://ctf.example.com/challenges
```

### Method 2: Using bash wrapper
```bash
./scrape_ctf.sh https://ctf.example.com/challenges
```

## Common Scenarios

### 1. Public CTF (No Authentication)
```bash
python ctf_scraper.py https://ctf.example.com/challenges -v
```

### 2. Authenticated CTF (with cookie)
First, get your session cookie from browser:
- Open DevTools (F12)
- Go to Application/Storage → Cookies
- Copy the session cookie value

Then run:
```bash
python ctf_scraper.py https://ctf.example.com/challenges \
  --cookie "session=your_cookie_value_here"
```

### 3. Preview Before Downloading (Dry Run)
```bash
python ctf_scraper.py https://ctf.example.com/challenges --dry-run
```

### 4. Custom Output Directory
```bash
python ctf_scraper.py https://ctf.example.com/challenges \
  -o ~/Documents/CTFs/MyCompetition
```

### 5. Using Configuration File
```bash
# Copy example config
cp config.example.yaml config.yaml

# Edit config.yaml with your settings
nano config.yaml

# Run with config
python ctf_scraper.py https://ctf.example.com/challenges --config config.yaml
```

## Output Structure

After running, you'll get a organized folder structure:

```
ctf_challenges/
└── 0xfun/                    # CTF name
    ├── Pwn/
    │   ├── buffer_overflow/
    │   │   ├── statement.txt
    │   │   └── files/
    │   │       ├── vuln
    │   │       └── libc.so.6
    │   └── rop_chain/
    │       ├── statement.txt
    │       └── files/
    ├── Web/
    │   └── sql_injection/
    │       ├── statement.txt
    │       └── files/
    ├── Crypto/
    ├── Reverse/
    ├── Misc/
    └── Forensics/
```

## Troubleshooting

### Issue: "403 Forbidden" error
**Solution**: The CTF requires authentication. Use `--cookie` or `--token` option.

### Issue: "No challenges found"
**Solutions**:
1. Check if you're on the correct URL (should be the challenges page)
2. Try adding `-v` for verbose output to see what's happening
3. The platform might not be supported - try `--platform generic`
4. Check if authentication is required

### Issue: Files not downloading
**Solutions**:
1. Check your internet connection
2. Some files might require authentication
3. Use `-v` to see which files are failing

### Issue: Wrong categories
**Solution**: Edit `config.yaml` to customize category keywords

## Platform-Specific Tips

### CTFd Platforms
- Most common CTF platform
- Usually auto-detected
- API endpoint preferred (faster): `/api/v1/challenges`

### Custom/Unknown Platforms
Use generic scraper:
```bash
python ctf_scraper.py https://custom-ctf.com/challenges --platform generic -v
```

## Tips & Best Practices

1. **Always test with dry-run first**
   ```bash
   python ctf_scraper.py <url> --dry-run
   ```

2. **Use verbose mode for debugging**
   ```bash
   python ctf_scraper.py <url> -v
   ```

3. **Organize by competition**
   ```bash
   python ctf_scraper.py <url> -o ~/CTFs/CompetitionName
   ```

4. **Keep your cookies secure**
   - Don't commit `config.yaml` with cookies to git (it's in `.gitignore`)
   - Use environment variables for sensitive data

## Advanced Usage

### Custom Category Mappings
Edit `config.example.yaml` and add your own keywords:

```yaml
categories:
  pwn:
    - pwn
    - binary
    - custom_keyword
```

### Batch Scraping Multiple CTFs
Create a script:
```bash
#!/bin/bash
source venv/bin/activate

python ctf_scraper.py https://ctf1.com/challenges -o ./CTF1
python ctf_scraper.py https://ctf2.com/challenges -o ./CTF2
python ctf_scraper.py https://ctf3.com/challenges -o ./CTF3
```

## Getting Help

```bash
python ctf_scraper.py --help
./scrape_ctf.sh --help
```

## What's Next?

After scraping:
1. Navigate to the challenge folder
2. Read `statement.txt` for challenge description
3. Work with files in the `files/` subdirectory
4. Keep your solutions organized in the same folder structure
