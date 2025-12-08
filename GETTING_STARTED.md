# 🎯 GETTING STARTED - Your First 5 Minutes

## Step-by-Step Launch Guide

### ⏱️ Estimated Time: 5 minutes

---

## 📋 Prerequisites Check

Before you begin, make sure you have:
- [ ] **Python 3.8+** installed - [Download here](https://www.python.org/downloads/)
- [ ] **Node.js 18+** installed - [Download here](https://nodejs.org/)
- [ ] **Command Prompt** or Terminal access
- [ ] **Web Browser** (Chrome, Edge, Firefox, or Safari)

Quick check:
```bash
python --version    # Should show 3.8 or higher
node --version      # Should show 18 or higher
```

---

## 🚀 Launch Sequence

### Terminal 1: Backend (FastAPI)

1. **Open Command Prompt**
   - Press `Win + R`
   - Type `cmd`
   - Press Enter

2. **Navigate to backend folder**
   ```bash
   cd d:\personal\AI_embadding\backend
   ```

3. **Run setup** (first time only - takes ~2 minutes)
   ```bash
   setup.bat
   ```
   This will:
   - Create virtual environment
   - Install Python packages
   - Download AI model (~80 MB)

4. **Start the backend**
   ```bash
   run.bat
   ```
   
5. **Wait for this message:**
   ```
   ✅ All services initialized successfully!
   📊 Stats:
      - Products indexed: 15
      - Documents indexed: 6
   ```

6. **Backend is ready when you see:**
   ```
   INFO: Uvicorn running on http://0.0.0.0:8000
   ```

---

### Terminal 2: Frontend (Next.js)

7. **Open NEW Command Prompt**
   - Press `Win + R`
   - Type `cmd`
   - Press Enter

8. **Navigate to frontend folder**
   ```bash
   cd d:\personal\AI_embadding\frontend
   ```

9. **Run setup** (first time only - takes ~1 minute)
   ```bash
   setup.bat
   ```
   This will:
   - Install Node.js packages

10. **Start the frontend**
    ```bash
    run.bat
    ```

11. **Wait for this message:**
    ```
    ✔ Ready in Xms
    ○ Local: http://localhost:3000
    ```

---

### Browser: Open the App

12. **Open your web browser**

13. **Navigate to:**
    ```
    http://localhost:3000
    ```

14. **You should see:**
    - Beautiful dark interface
    - "AI Shopping Assistant" title with gradient
    - Search bar with suggestions
    - Three tabs: Search, Chat, Recommendations

---

## ✅ Quick Test

### Test 1: Search (30 seconds)
1. Click the search bar
2. Type: `rain jacket`
3. Click Search button
4. **Expected**: See 3-4 products (rain jacket, boots, umbrella, poncho)

### Test 2: Chat (30 seconds)
1. Click **Chat** tab
2. Click suggestion: "How do I choose rain gear?"
3. Click Send
4. **Expected**: See detailed answer with sources

### Test 3: Recommendations (30 seconds)
1. Click **Search** tab
2. Search for: `black shirt`
3. Click on the "Black Cotton T-Shirt" card
4. **Expected**: Automatically switch to Recommendations tab with similar products

---

## 🎉 Success!

If all three tests work, congratulations! Your AI Shopping Assistant is fully operational!

---

## 🛟 Troubleshooting

### Backend won't start

**Problem**: Port 8000 already in use
```
Solution: Find and kill process using port 8000
```

**Problem**: Python not found
```
Solution: Install Python from python.org and add to PATH
```

**Problem**: Module not found errors
```
Solution: Delete venv folder, run setup.bat again
```

### Frontend won't start

**Problem**: Port 3000 already in use
```
Solution: Kill process using port 3000 or change port
To change port: In package.json, change "dev" to:
"dev": "next dev -p 3001"
```

**Problem**: npm not found
```
Solution: Install Node.js from nodejs.org
```

**Problem**: Dependencies error
```
Solution: Delete node_modules folder, run setup.bat again
```

### Can't connect to backend

**Problem**: Frontend shows connection errors
```
Solution: 
1. Make sure backend is running (Terminal 1)
2. Check http://localhost:8000/api/health in browser
3. If you see JSON response, backend is working
```

### Search returns nothing

**Problem**: No results when searching
```
Solution:
1. Wait 30 seconds after backend starts (model loading)
2. Check Terminal 1 for "✅ All services initialized"
3. Try refreshing the browser page
```

---

## 📱 What to Try Next

### Example Searches
- `"clothes for rainy weather"`
- `"black shirt"`
- `"running shoes"`
- `"workout gear"`
- `"wireless headphones"`
- `"waterproof items"`

### Example Chat Questions
- "How do I choose rain gear?"
- "What makes a good capsule wardrobe?"
- "Best fitness gear for beginners?"
- "How to care for waterproof clothing?"
- "What tech accessories do I need?"

### Explore Recommendations
1. Search for any product
2. Click on it
3. See similar items
4. Click on a similar item
5. See more recommendations
6. Keep exploring!

---

## 🎓 Understanding What You See

### Search Tab
- **Search Bar**: Type natural language queries
- **Quick Suggestions**: Click to try example searches
- **Product Cards**: 
  - Top: Category icon & brand
  - Middle: Name & description
  - Bottom: Rating, price, tags
  - Click card → Get recommendations

### Chat Tab
- **Question Suggestions**: Click to ask common questions
- **Your Messages**: Blue, on the right
- **AI Responses**: Glass-style, on the left
- **Sources**: Shows which documents were used
- **Related Products**: Suggested items based on your question

### Recommendations Tab
- **Based On**: Shows what product triggered these
- **Similar Products**: Items with similar characteristics
- **Similarity Scores**: How similar (if shown)
- **Click Any Card**: Get recommendations for that product

---

## 📊 Performance Notes

### First Time
- Backend startup: ~30 seconds (downloading model)
- First search: ~5 seconds (loading model into memory)
- Frontend startup: ~10 seconds

### After First Time
- Backend startup: ~10 seconds
- Searches: < 100ms
- Chat responses: < 200ms
- Recommendations: < 50ms

---

## 🎨 UI Features to Notice

1. **Glassmorphism**: Frosted glass effect on cards
2. **Gradient Text**: Purple-blue gradient on headings
3. **Hover Effects**: Cards lift up when you hover
4. **Smooth Animations**: Everything fades and slides smoothly
5. **Tab Transitions**: Smooth switching between features
6. **Loading States**: Spinners and animated dots
7. **Dark Theme**: Easy on the eyes
8. **Background Effects**: Subtle animated gradients

---

## 💡 Pro Tips

1. **Use Quick Suggestions**: Fastest way to see results
2. **Try Natural Language**: "best shoes for running" works better than just "shoes"
3. **Explore Recommendations**: Click through multiple products to discover
4. **Ask Specific Questions**: More context = better chat answers
5. **Check Network Tab**: Open DevTools (F12) to see API calls

---

## 📚 Next Steps

After you're comfortable with the basics:

1. **Read ARCHITECTURE.md** - Understand how it works
2. **Read TESTING.md** - Full testing scenarios
3. **Modify sample_data.py** - Add your own products
4. **Customize the UI** - Change colors in tailwind.config.ts
5. **Add features** - See PROJECT_SUMMARY.md for ideas

---

## 🎯 Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Search tab works
- [ ] Chat tab works  
- [ ] Recommendations tab works
- [ ] UI looks beautiful with animations
- [ ] No errors in browser console
- [ ] Response times are fast

---

## 🆘 Still Need Help?

Check these files in order:
1. **QUICKSTART.md** - Detailed setup
2. **TESTING.md** - Testing scenarios
3. **ARCHITECTURE.md** - Technical details
4. **PROJECT_SUMMARY.md** - Complete overview

---

## 🎊 You're All Set!

**Your AI Shopping Assistant is running!**

- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

**Enjoy exploring your new AI-powered shopping experience!** 🛍️✨
