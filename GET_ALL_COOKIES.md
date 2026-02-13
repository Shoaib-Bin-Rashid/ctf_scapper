# 🍪 How to Get ALL Cookies (Including Cloudflare)

## The Problem You're Facing

You can see https://ctf.0xfun.org/challenges in your browser, but the scraper gets 403 Forbidden.

**Why?** Cloudflare uses multiple cookies for bot protection:
- `session` - Your login session
- `cf_clearance` - Cloudflare challenge clearance
- `__cfduid` - Cloudflare user identifier
- And possibly others

You only copied the `session` cookie, so Cloudflare is blocking the scraper!

---

## ✅ SOLUTION: Get ALL Cookies

### Method 1: Using Browser Console (EASIEST!)

1. **Open the CTF website** in your browser
   - Go to https://ctf.0xfun.org/challenges
   - Make sure the page loads completely

2. **Press F12** to open DevTools

3. **Go to Console tab**

4. **Run this command:**
   ```javascript
   document.cookie
   ```

5. **Copy the ENTIRE output**
   - It will look like: `cookie1=value1; cookie2=value2; cookie3=value3`
   - **Copy ALL of it!**

6. **Use it with the scraper:**
   ```bash
   python ctf_scraper_ultimate.py https://ctf.0xfun.org/challenges \
     -c "PASTE_ALL_COOKIES_HERE" -v
   ```

---

### Method 2: Using DevTools Application Tab

1. **Open the website** and press F12

2. **Go to Application tab** (Chrome) or **Storage tab** (Firefox)

3. **Click on Cookies** → **ctf.0xfun.org**

4. **You'll see multiple cookies:**
   ```
   session         = dcd45189-c36b-4926-8528-9cd6590c543b.K4YLy4RqtvJ4z3kZoEPearY2I00
   cf_clearance    = abc123xyz... (Cloudflare clearance)
   __cfduid        = d123... (Cloudflare UID)
   ```

5. **Format them ALL like this:**
   ```
   session=VALUE1; cf_clearance=VALUE2; __cfduid=VALUE3
   ```

6. **Use with scraper:**
   ```bash
   python ctf_scraper_ultimate.py https://ctf.0xfun.org/challenges \
     -c "session=VALUE1; cf_clearance=VALUE2; __cfduid=VALUE3" -v
   ```

---

## 🎯 Example

### What you did (WRONG ❌):
```bash
python ctf_scraper_ultimate.py https://ctf.0xfun.org/challenges \
  -c "dcd45189-c36b-4926-8528-9cd6590c543b.K4YLy4RqtvJ4z3kZoEPearY2I00"
```
Only has session cookie → Cloudflare blocks it!

### What you should do (CORRECT ✅):
```bash
python ctf_scraper_ultimate.py https://ctf.0xfun.org/challenges \
  -c "session=dcd45189-c36b-4926-8528-9cd6590c543b.K4YLy4RqtvJ4z3kZoEPearY2I00; cf_clearance=abc123xyz; __cfduid=d123"
```
Has ALL cookies → Cloudflare allows it!

---

## 📝 Step-by-Step for ctf.0xfun.org

1. **Open Chrome/Firefox**
2. **Go to** https://ctf.0xfun.org/challenges
3. **Wait** for page to fully load (you should see challenges)
4. **Press F12**
5. **Console tab**
6. **Type:** `document.cookie`
7. **Press Enter**
8. **Right-click the output** → Copy
9. **Run:**
   ```bash
   python ctf_scraper_ultimate.py https://ctf.0xfun.org/challenges \
     -c "PASTE_HERE" -v
   ```

---

## 🔍 What Should the Cookie String Look Like?

### ✅ GOOD (Multiple cookies):
```
session=abc123; cf_clearance=xyz789; __cfduid=def456
```

### ❌ BAD (Only one cookie):
```
dcd45189-c36b-4926-8528-9cd6590c543b.K4YLy4RqtvJ4z3kZoEPearY2I00
```

---

## 🚀 Quick Test After Getting Cookies

```bash
# Test with all cookies
python ctf_scraper_ultimate.py https://ctf.0xfun.org/challenges \
  -c "YOUR_FULL_COOKIE_STRING" \
  --dry-run -v

# If it works, do full scrape:
python ctf_scraper_ultimate.py https://ctf.0xfun.org/challenges \
  -c "YOUR_FULL_COOKIE_STRING" \
  -o test_run/0xfun_output \
  -v
```

---

## 💡 Pro Tip

The cookie string from `document.cookie` is EXACTLY what you need!

**Don't manually pick cookies** - just copy the entire output of `document.cookie`!

---

## ⚠️ Common Mistakes

1. ❌ Only copying session cookie
2. ❌ Missing `cf_clearance` (Cloudflare's most important cookie)
3. ❌ Not including semicolons between cookies
4. ❌ Copying cookie names without values

---

## ✅ Success Checklist

- [ ] Page loads in browser (showing challenges)
- [ ] Used `document.cookie` in Console
- [ ] Copied ENTIRE output (with semicolons)
- [ ] String contains multiple cookies
- [ ] Pasted in `-c` parameter
- [ ] Tool works! 🎉

---

Try again with ALL cookies and it should work! 🚀
