# 🔧 Frontend Troubleshooting Guide

## TypeScript Errors in VS Code

### Problem: Lots of errors in page.tsx, components, etc.
```
Cannot find module 'react'
Cannot find module 'framer-motion'
JSX element implicitly has type 'any'
```

### Solution:
**STEP 1:** Make sure npm install completed
```bash
cd frontend
npm install
```

**STEP 2:** Restart TypeScript Server in VS Code
- Press `Ctrl + Shift + P`
- Type: `TypeScript: Restart TS Server`
- Press Enter

**STEP 3:** If still showing errors
- Close all files
- Reload VS Code: `Ctrl + Shift + P` → `Developer: Reload Window`

---

## Module Not Found Errors

### Problem: "Cannot find module '@/components/...'"

### Check:
1. Is `node_modules` folder present in `frontend/`?
2. Is `tsconfig.json` present?
3. Did npm install finish successfully?

### Solution:
```bash
# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

---

## Port Already in Use

### Problem: "Port 3000 is already in use"

### Solution Option 1: Kill the process
```bash
# Find the process
netstat -ano | findstr :3000

# Kill it (replace XXXX with PID)
taskkill /PID XXXX /F
```

### Solution Option 2: Use different port
Edit `package.json`:
```json
{
  "scripts": {
    "dev": "next dev -p 3001"
  }
}
```

---

## Build Errors

### Problem: Errors when running `npm run dev`

### Check the error message:

**"Module not found"**
```bash
npm install
```

**"Invalid configuration"**
```bash
# Check these files exist:
- next.config.mjs
- tsconfig.json
- tailwind.config.ts
```

**"PostCSS plugin error"**
```bash
npm install -D postcss autoprefixer tailwindcss
```

---

## CSS Not Loading

### Problem: No styling, everything looks plain

### Solution:
1. Check `app/globals.css` exists
2. Check it's imported in `app/layout.tsx`
3. Restart dev server:
   ```bash
   # Stop: Ctrl + C
   npm run dev
   ```

---

## API Connection Errors

### Problem: "Failed to fetch" or network errors

### Checklist:
- [ ] Backend is running on port 8000
- [ ] Check: http://localhost:8000/api/health
- [ ] CORS is enabled in backend
- [ ] `.env.local` has correct API URL

### Fix `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Fast Refresh Not Working

### Problem: Changes don't reflect automatically

### Solution:
```bash
# Restart dev server
# Press Ctrl + C then:
npm run dev
```

---

## Quick Fixes Checklist

When you have ANY error, try these in order:

1. ✅ **Restart TypeScript Server**
   - `Ctrl + Shift + P` → "TypeScript: Restart TS Server"

2. ✅ **Restart Dev Server**
   - Stop: `Ctrl + C`
   - Start: `npm run dev`

3. ✅ **Reinstall Dependencies**
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

4. ✅ **Restart VS Code**
   - `Ctrl + Shift + P` → "Developer: Reload Window"

5. ✅ **Check Node/npm versions**
   ```bash
   node --version  # Should be 18+
   npm --version   # Should be 9+
   ```

---

## Common Commands

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Clear cache and reinstall
rm -rf node_modules package-lock.json .next
npm install
```

---

## Still Having Issues?

1. Check the main README.md
2. Read GETTING_STARTED.md
3. Verify all files are present
4. Check terminal for specific error messages
5. Try the "nuclear option":
   ```bash
   # Delete everything and start fresh
   rm -rf node_modules package-lock.json .next
   npm cache clean --force
   npm install
   ```

---

**Most errors are fixed by:**
1. Running `npm install`
2. Restarting TypeScript Server
3. Restarting VS Code

**Good luck! 🚀**
