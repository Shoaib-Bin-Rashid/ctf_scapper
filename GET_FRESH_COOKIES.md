# 🍪 How to Get Fresh Cookies - Complete Guide

Cookies are required for accessing authenticated CTF platforms. Here's the EASIEST and most reliable method:

---

## ⭐ RECOMMENDED: Copy as cURL (Fastest & Most Reliable)

This is the **EASIEST** way to get cookies. Follow these steps:

### Step 1: Open Browser DevTools
1. Go to the CTF website (e.g., https://ctf.0xfun.org/challenges)
2. Make sure you're **logged in**
3. Press `F12` (or Right-click → Inspect)

### Step 2: Go to Network Tab
1. Click on the **Network** tab
2. Refresh the page (`Ctrl+R` or `Cmd+R` on Mac)
3. You'll see requests loading

### Step 3: Copy as cURL
1. Find and **click** on the main request (usually named `challenges` or the page name)
2. **Right-click** on that request
3. Select **Copy** → **Copy as cURL** (or **Copy as cURL (bash)**)

### Step 4: Extract Cookies from cURL Command

After pasting, you'll see something like this:

```bash
curl 'https://ctf.0xfun.org/challenges' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8' \
  -b 'session=361efa74-78d6-41de-9259-8ec23fc7caaa.gZYiouxDqovVGIfeBOUlNpNg3CE; cf_clearance=UbuXNfqRBtDsgFheVUNB5qQIZ2hFDumnNscDJoV0aEY-1770992829-1.2.1.1-0WzPSlqXVgM1CiDK1H7tVbWoh61vLfEsyyCQFgKk1jaNySaeWVFvOVpbusTD.i0fAYfGStsGkHi0RPdxuZmGiQDAWh4lxNrN_Z4Ksys84L1.ss3M6Yxe5YEoM2OiQMwtoGD0KZdiGtVDefsl8So_wmvr1k.aHAoaIhaUOsmd.kCtrbHxzOajs.FRtuWHT13.GBg2e9TS63VMTKfGnGln9mz4kIRqRAW0Hg8Vv3UmbMYjTuflv_C19FvkdUZDBuzR' \
  -H 'priority: u=0, i' \
  ...
```

**Find the line with `-b` flag** (that's the cookies!)

### Step 5: Copy ONLY the Cookie Value

From the `-b` line, copy **ONLY** the value (without `-b` and without quotes):

```
session=361efa74-78d6-41de-9259-8ec23fc7caaa.gZYiouxDqovVGIfeBOUlNpNg3CE; cf_clearance=UbuXNfqRBtDsgFheVUNB5qQIZ2hFDumnNscDJoV0aEY-1770992829-1.2.1.1-0WzPSlqXVgM1CiDK1H7tVbWoh61vLfEsyyCQFgKk1jaNySaeWVFvOVpbusTD.i0fAYfGStsGkHi0RPdxuZmGiQDAWh4lxNrN_Z4Ksys84L1.ss3M6Yxe5YEoM2OiQMwtoGD0KZdiGtVDefsl8So_wmvr1k.aHAoaIhaUOsmd.kCtrbHxzOajs.FRtuWHT13.GBg2e9TS63VMTKfGnGln9mz4kIRqRAW0Hg8Vv3UmbMYjTuflv_C19FvkdUZDBuzR
```

### Step 6: Use the Cookie

Now run the scraper **IMMEDIATELY** (cookies expire in 5-10 minutes!):

```bash
python3 direct_scraper.py "session=361efa74-78d6-41de-9259-8ec23fc7caaa.gZYiouxDqovVGIfeBOUlNpNg3CE; cf_clearance=UbuXNfqRBtDsgFheVUNB5qQIZ2hFDumnNscDJoV0aEY-1770992829-1.2.1.1-0WzPSlqXVgM1CiDK1H7tVbWoh61vLfEsyyCQFgKk1jaNySaeWVFvOVpbusTD.i0fAYfGStsGkHi0RPdxuZmGiQDAWh4lxNrN_Z4Ksys84L1.ss3M6Yxe5YEoM2OiQMwtoGD0KZdiGtVDefsl8So_wmvr1k.aHAoaIhaUOsmd.kCtrbHxzOajs.FRtuWHT13.GBg2e9TS63VMTKfGnGln9mz4kIRqRAW0Hg8Vv3UmbMYjTuflv_C19FvkdUZDBuzR" ./OutputCTF
```

✅ **Done!** The scraper will download all challenges.

---

## 📋 Alternative Methods

### Method 1: Browser Console (Quick)

1. Press `F12` → **Console** tab
2. Type: `document.cookie`
3. Press Enter
4. Copy the output

### Method 2: Network Tab (Manual)

1. `F12` → **Network** tab → Refresh page
2. Click on `challenges` request
3. Scroll to **Request Headers** section
4. Find `cookie:` line
5. Copy the value (everything after `cookie:`)

### Method 3: Application/Storage Tab

1. `F12` → **Application** (Chrome) or **Storage** (Firefox)
2. Click **Cookies** → Select the website
3. Copy values of `session` and `cf_clearance`
4. Format as: `session=XXX; cf_clearance=YYY`

---

## ⚠️ **IMPORTANT: Cookie Expiration!**

### Cookies Expire FAST! (5-10 minutes)

**Common Mistakes:**
- ❌ Getting cookies and waiting 10 minutes before using
- ❌ Closing the browser after copying cookies
- ❌ Using old cookies from yesterday

**Best Practices:**
- ✅ Get fresh cookies RIGHT BEFORE scraping
- ✅ Use cookies IMMEDIATELY after copying
- ✅ Keep browser open during scraping
- ✅ If you see `403 Forbidden` → Get fresh cookies again!

### How to Know if Cookies Expired?

You'll see this error:
```
❌ Failed to fetch challenges: 403 Client Error: Forbidden
```

**Solution:** Refresh the page and get fresh cookies!

---

## 🔥 Quick Reference

### What to Copy:
```
session=YOUR_SESSION_VALUE; cf_clearance=YOUR_CLEARANCE_VALUE
```

### How to Use:
```bash
python3 direct_scraper.py "YOUR_COOKIES" ./output_folder
```

### From cURL:
```bash
# Find this line in cURL output:
-b 'session=XXX; cf_clearance=YYY'

# Copy only this part (without -b):
session=XXX; cf_clearance=YYY
```

---

## 💡 Pro Tips

1. **Use "Copy as cURL"** - It's the fastest method!
2. **Don't wait** - Use cookies within 5 minutes
3. **Refresh often** - If you get errors, get fresh cookies
4. **Keep browser open** - Closing it might invalidate session

---

## Cookie Format Reference

### Correct ✅:
```bash
python3 direct_scraper.py "session=abc123; cf_clearance=xyz789" ./output
```

### Wrong ❌:
```bash
# Missing quotes
python3 direct_scraper.py session=abc123; cf_clearance=xyz789 ./output

# Including -b flag
python3 direct_scraper.py "-b session=abc123; cf_clearance=xyz789" ./output

# Including "cookie:"
python3 direct_scraper.py "cookie: session=abc123; cf_clearance=xyz789" ./output
```

---

**Now you're ready to scrape CTF challenges! 🚀**

For more help, run: `python3 direct_scraper.py --help`
