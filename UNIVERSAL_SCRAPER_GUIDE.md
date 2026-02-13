# 🌍 Universal CTF Scraper - User Guide

## ✨ What's New?

The scraper is now **UNIVERSAL**! It works with **ANY** CTFd-based platform!

---

## 🚀 Usage

### Basic Command:

```bash
python3 ctf_scraper.py URL "COOKIES" OUTPUT_DIR
```

### Parameters:

| Parameter | Description | Required | Example |
|-----------|-------------|----------|---------|
| `URL` | CTF website URL | ✅ Yes | `https://ctf.0xfun.org/challenges` |
| `COOKIES` | Cookie string from browser | ✅ Yes | `"session=XXX; cf_clearance=YYY"` |
| `OUTPUT_DIR` | Output directory | ❌ No (default: `./ctf_download`) | `./my_ctf` |

---

## 🔥 Real Examples

### Example 1: 0xFun CTF

```bash
python3 ctf_scraper.py \
  https://ctf.0xfun.org/challenges \
  "session=XXX; cf_clearance=YYY" \
  ./0xfun_download
```

### Example 2: picoCTF

```bash
python3 ctf_scraper.py \
  https://play.picoctf.org/practice \
  "session=XXX; cf_clearance=YYY" \
  ./picoctf_download
```

### Example 3: HackTheBox CTF

```bash
python3 ctf_scraper.py \
  https://ctf.hackthebox.com/challenges \
  "session=XXX; cf_clearance=YYY" \
  ./htb_ctf
```

### Example 4: Any CTFd Platform

```bash
python3 ctf_scraper.py \
  https://your-ctf-site.com/challenges \
  "session=XXX; cf_clearance=YYY" \
  ./output
```

---

## 🍪 How to Get Cookies

### Quick Method (Copy as cURL):

1. **Browser** → F12 → **Network** tab
2. Refresh page (Ctrl+R)
3. Right-click on any request → **Copy** → **Copy as cURL**
4. Find the line with `-b` flag:
   ```
   -b 'session=XXX; cf_clearance=YYY'
   ```
5. Copy ONLY the cookie value (without `-b`)

### Then Run:

```bash
python3 ctf_scraper.py URL "session=XXX; cf_clearance=YYY" ./output
```

---

## ⚠️ Important Notes

### Cookie Expiration

- Cookies expire in **5-10 minutes**!
- Get fresh cookies **RIGHT BEFORE** scraping
- If you see `403 Forbidden` → Get new cookies

### Supported Platforms

✅ **Works with ANY CTFd-based platform:**
- 0xFun CTF
- picoCTF  
- HackTheBox CTF
- CTFd Demo
- Most university CTFs
- And many more!

---

## 📁 Output Structure

```
output_dir/
└── 0XFUN_CTF/          (Auto-detected from URL)
    ├── Web/
    │   └── Challenge_Name/
    │       ├── statement.txt
    │       └── files/
    ├── Crypto/
    ├── OSINT/
    └── Warm-Up/
```

**CTF name is auto-detected from the URL!**

Examples:
- `https://ctf.0xfun.org` → `0XFUN_CTF`
- `https://play.picoctf.org` → `PICOCTF_CTF`
- `https://demo.ctfd.io` → `DEMO_CTF`

---

## 🎯 Complete Example (Copy-Paste Ready)

### Step 1: Get Fresh Cookies

```bash
# 1. Open CTF site in browser
# 2. F12 → Network → Refresh
# 3. Right-click request → Copy as cURL
# 4. Find: -b 'session=XXX; cf_clearance=YYY'
# 5. Copy cookie value
```

### Step 2: Run Scraper

```bash
python3 ctf_scraper.py \
  https://ctf.0xfun.org/challenges \
  "session=361efa74-78d6-41de-9259-8ec23fc7caaa.gZYiouxDqovVGIfeBOUlNpNg3CE; cf_clearance=UbuXNfqRBtDsgFheVUNB5qQIZ2hFDumnNscDJoV0aEY-1770992829-1.2.1.1-0WzPSlqXVgM1CiDK1H7tVbWoh61vLfEsyyCQFgKk1jaNySaeWVFvOVpbusTD.i0fAYfGStsGkHi0RPdxuZmGiQDAWh4lxNrN_Z4Ksys84L1.ss3M6Yxe5YEoM2OiQMwtoGD0KZdiGtVDefsl8So_wmvr1k.aHAoaIhaUOsmd.kCtrbHxzOajs.FRtuWHT13.GBg2e9TS63VMTKfGnGln9mz4kIRqRAW0Hg8Vv3UmbMYjTuflv_C19FvkdUZDBuzR" \
  ./OutputCTF
```

### Step 3: Check Results

```bash
ls -la ./OutputCTF/0XFUN_CTF/
```

---

## 📖 Help Command

```bash
python3 ctf_scraper.py --help
python3 ctf_scraper.py -h
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `403 Forbidden` | Get fresh cookies (they expired) |
| `Invalid URL` | Make sure URL starts with http:// or https:// |
| `No challenges found` | Check if you're logged in |
| `Connection error` | Check internet, try again |

---

## 💡 Pro Tips

1. **Fresh Cookies**: Always get them right before scraping
2. **URL Format**: Use the full URL including `/challenges` or `/practice`
3. **Output Dir**: Can be relative (`./output`) or absolute (`/home/user/ctf`)
4. **Multiple CTFs**: Use different output dirs for different CTFs

---

## ✅ Advantages of Universal Scraper

| Feature | Old `direct_scraper.py` | New `ctf_scraper.py` |
|---------|------------------------|---------------------|
| Hardcoded URL | ❌ Yes (0xfun only) | ✅ No (any URL) |
| Manual editing | ❌ Required | ✅ Not needed |
| Platform support | ❌ One platform | ✅ Any CTFd platform |
| Auto CTF name | ❌ No | ✅ Yes |
| Ease of use | ⚠️ Moderate | ✅ Very Easy |

---

**The tool is now truly universal! Use it with any CTFd platform! 🌍🚀**
