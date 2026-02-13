# 🎯 Which Scraper to Use?

## Quick Guide

| Platform Type | Scraper to Use | Example URL |
|---------------|----------------|-------------|
| **CTFd-based** | `ctf_scraper.py` | `https://ctf.0xfun.org/challenges` |
| **picoCTF** | `picoctf_scraper.py` | `https://play.picoctf.org/practice` |

---

## 📋 Usage Patterns

### For CTFd Platforms (Most CTFs)

```bash
python3 ctf_scraper.py "URL" "COOKIES" ./output
```

**⚠️ Important: Always quote the URL!**

Examples:
```bash
# 0xFun CTF
python3 ctf_scraper.py "https://ctf.0xfun.org/challenges" \
  "session=XXX; cf_clearance=YYY" ./0xfun

# HackTheBox CTF
python3 ctf_scraper.py "https://ctf.hackthebox.com/challenges" \
  "session=XXX" ./htb

# Any CTFd platform
python3 ctf_scraper.py "https://demo.ctfd.io/challenges" \
  "session=XXX" ./demo
```

### For picoCTF

```bash
python3 picoctf_scraper.py "COOKIES" ./output
```

Example:
```bash
python3 picoctf_scraper.py \
  "sessionid=XXX; csrftoken=YYY; cf_clearance=ZZZ" \
  ./picoctf
```

---

## ⚠️ Shell Escaping Rules

### URLs with Special Characters

URLs often contain special characters that need escaping:

| Character | Why It's Special | Solution |
|-----------|------------------|----------|
| `?` | Glob pattern in zsh/bash | Quote the URL |
| `&` | Background process | Quote the URL |
| `*` | Wildcard | Quote the URL |
| `;` | Command separator | Quote the URL |

### ✅ ALWAYS Quote URLs

**Correct:**
```bash
python3 ctf_scraper.py "https://play.picoctf.org/practice?page=1" "COOKIES" ./out
python3 ctf_scraper.py 'https://ctf.com/challenges?cat=web&page=2' "COOKIES" ./out
```

**Wrong:**
```bash
python3 ctf_scraper.py https://play.picoctf.org/practice?page=1 "COOKIES" ./out
# Error: zsh: no matches found
```

### Cookie Quoting

**Cookies MUST also be quoted** because they contain `;` and `=`:

```bash
python3 ctf_scraper.py "URL" "session=XXX; cf_clearance=YYY" ./output
                              ↑                              ↑
                              Quote start                    Quote end
```

---

## 🔍 How to Identify Platform Type?

### CTFd Platforms

Look for these signs:
- URL patterns: `/challenges`, `/scoreboard`, `/users`
- API endpoint: `/api/v1/challenges`
- Common domains: Many university and company CTFs
- Examples: 0xFun, HackTheBox CTF, many others

**Use:** `ctf_scraper.py`

### picoCTF Platform

Look for these signs:
- Domain: `play.picoctf.org`
- URL patterns: `/practice`, `/competitions`
- Different API structure

**Use:** `picoctf_scraper.py`

---

## 📖 Complete Examples

### Example 1: 0xFun CTF (CTFd)

```bash
# Get cookies from browser
# Then run:

python3 ctf_scraper.py \
  "https://ctf.0xfun.org/challenges" \
  "session=abc123; cf_clearance=xyz789" \
  ./0xfun_download
```

### Example 2: picoCTF

```bash
# Get cookies from browser
# Then run:

python3 picoctf_scraper.py \
  "sessionid=abc123; csrftoken=xyz789; cf_clearance=def456" \
  ./picoctf_download
```

### Example 3: URL with Query Parameters

```bash
# URL has ?page=1 - MUST quote it!

python3 ctf_scraper.py \
  "https://demo.ctfd.io/challenges?category=web&page=1" \
  "session=abc123" \
  ./demo_ctf
```

---

## 🛠️ Troubleshooting

### Error: `zsh: no matches found`

**Cause:** URL not quoted, contains special characters

**Solution:** Add quotes around the URL
```bash
# Before (wrong)
python3 ctf_scraper.py https://site.com/challenges?page=1 "cookies" ./out

# After (correct)
python3 ctf_scraper.py "https://site.com/challenges?page=1" "cookies" ./out
```

### Error: `command not found: =XXX`

**Cause:** Cookies not quoted

**Solution:** Add quotes around cookies
```bash
# Before (wrong)
python3 ctf_scraper.py "URL" session=XXX; cf_clearance=YYY ./out

# After (correct)
python3 ctf_scraper.py "URL" "session=XXX; cf_clearance=YYY" ./out
```

### Error: `403 Forbidden`

**Cause:** Wrong scraper for the platform OR expired cookies

**Solution:** 
1. Check if using correct scraper (CTFd vs picoCTF)
2. Get fresh cookies

---

## 💡 Pro Tips

1. **Always quote URLs and cookies** - Prevents 99% of shell issues
2. **Use the right scraper** - CTFd platforms ≠ picoCTF
3. **Fresh cookies** - Get them right before running
4. **Check platform type** - Look at URL structure and API endpoints

---

## Quick Reference Card

```bash
# CTFd Platforms (0xFun, HTB, most others)
python3 ctf_scraper.py "URL" "COOKIES" ./output

# picoCTF
python3 picoctf_scraper.py "COOKIES" ./output

# ALWAYS use quotes for URLs and cookies!
```

---

**Remember: Quote everything, use the right scraper, get fresh cookies! 🚀**
