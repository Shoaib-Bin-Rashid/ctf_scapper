# 🚀 QUICK START GUIDE

## ONE COMMAND FOR ALL CTF PLATFORMS! 

```bash
python3 ctf_scraper_ultimate.py "URL" "COOKIES" ./output
```

---

## 📋 Step-by-Step

### Step 1: Get Cookies (30 seconds)

1. Open your browser and login to the CTF platform
2. Press `F12` to open DevTools
3. Go to **Network** tab
4. Load the challenges page
5. Right-click any request → **Copy** → **Copy as cURL**

You'll see something like:
```bash
curl 'https://ctf.0xfun.org/challenges' \
  -H 'accept: text/html...' \
  -b 'session=abc123; cf_clearance=xyz789'
     ↑_______________________________↑
     Copy ONLY this part
```

### Step 2: Run the Scraper

```bash
python3 ctf_scraper_ultimate.py \
  "https://ctf.0xfun.org/challenges" \
  "session=abc123; cf_clearance=xyz789" \
  ./my_ctf_output
```

### Step 3: Done! ✅

Check your output folder - all challenges are organized by category!

---

## 💡 Real Examples

### Example 1: 0xFun CTF

```bash
python3 ctf_scraper_ultimate.py \
  "https://ctf.0xfun.org/challenges" \
  "session=361efa74-78d6-41de-9259-8ec23fc7caaa.gZYiouxDqovVGIfeBOUlNpNg3CE; cf_clearance=t4GYXCrc48TbyUz7uhiMHirvtwIMgnZlG76Mngadi8M-1770991935-1.2.1.1" \
  ./0xfun_ctf
```

### Example 2: picoCTF

```bash
python3 ctf_scraper_ultimate.py \
  "https://play.picoctf.org/practice" \
  "sessionid=93wmny7jqfeo6k3w8a50xq65mcr1g5jy; csrftoken=yK8PNkcgMzeR9A0Hi6HR5BLNW3iMN6cM" \
  ./picoctf
```

### Example 3: Any CTFd Platform

```bash
python3 ctf_scraper_ultimate.py \
  "https://demo.ctfd.io/challenges" \
  "session=your_session_cookie_here" \
  ./demo_ctf
```

---

## ⚠️ Common Mistakes

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| Missing quotes around URL | `"https://site.com/challenges"` |
| Missing quotes around cookies | `"session=XXX; cf_clearance=YYY"` |
| Old/expired cookies | Get fresh cookies (< 5 min old) |
| Not logged in | Login first, then get cookies |

---

## 🎯 What It Does

1. **Auto-detects** platform type (CTFd, picoCTF, etc.)
2. **Downloads** all challenge statements
3. **Downloads** all challenge files
4. **Organizes** into folders:
   ```
   output/
   ├── Web/
   │   ├── SQL Injection 101/
   │   │   ├── challenge.txt
   │   │   └── app.zip
   │   └── XSS Challenge/
   │       └── challenge.txt
   ├── Crypto/
   │   └── RSA Baby/
   │       ├── challenge.txt
   │       └── public.pem
   └── Pwn/
       └── Buffer Overflow/
           ├── challenge.txt
           └── binary
   ```

---

## 🔧 Troubleshooting

### "zsh: no matches found"
→ You forgot to quote the URL! Add quotes:
```bash
python3 ctf_scraper_ultimate.py "URL" "COOKIES" ./output
                                  ↑   ↑
```

### "403 Forbidden" errors
→ Cookies expired! Get fresh cookies and try again immediately.

### "command not found"
→ You forgot to quote the cookies! They contain `;` characters.

---

## 📚 Need More Help?

```bash
# Show help
python3 ctf_scraper_ultimate.py --help

# Read detailed guides
cat GET_FRESH_COOKIES.md      # How to get cookies
cat WHY_NOT_WORKING.md        # Troubleshooting guide
```

---

## 🎉 That's It!

**One tool. All platforms. Super simple.**

```bash
python3 ctf_scraper_ultimate.py "URL" "COOKIES" ./output
```

Happy hacking! 🚀
