# 🧪 Testing Guide - AI Shopping Assistant

## Quick Test Scenarios

### Scenario 1: Semantic Search Magic ✨

**Test Case**: Search finds products by meaning, not keywords

1. **Search**: "clothes for rainy weather"
   - **Expected**: Rain jacket, waterproof boots, umbrella, poncho
   - **Why**: Understands context of "rainy weather" → waterproof items

2. **Search**: "workout gear for beginners"
   - **Expected**: Yoga mat, running shoes, water bottle, fitness tracker 
   - **Why**: Associates "workout" with fitness category

3. **Search**: "black shirt"
   - **Expected**: Black t-shirt, black hoodie, denim jacket, white tee
   - **Why**: Finds similar clothing items, not just exact matches

4. **Search**: "comfortable footwear"
   - **Expected**: Running shoes, hiking boots
   - **Why**: Semantic understanding of comfort → athletic shoes

### Scenario 2: RAG-Powered Chat 💬

**Test Case**: Chat answers questions using knowledge base

1. **Question**: "How do I choose rain gear?"
   - **Expected**: Detailed answer about waterproof ratings, breathability, fit
   - **Sources**: "How to Choose the Right Rain Gear" guide
   - **Products**: Rain jacket, hiking boots suggested

2. **Question**: "What makes a good capsule wardrobe?"
   - **Expected**: Explanation of essential versatile pieces
   - **Sources**: "Building the Perfect Capsule Wardrobe" guide
   - **Products**: Black t-shirt, hoodie, denim jacket suggested

3. **Question**: "How to maintain waterproof clothing?"
   - **Expected**: Care instructions, washing tips
   - **Sources**: "Caring for Your Waterproof Gear" tutorial
   - **Products**: Related waterproof items

4. **Question**: "Best gear for starting fitness?"
   - **Expected**: Beginner-friendly equipment recommendations
   - **Sources**: "Fitness Gear Essentials for Beginners" guide
   - **Products**: Yoga mat, running shoes, water bottle

### Scenario 3: Smart Recommendations 🎯

**Test Case**: Recommendations based on product similarity

1. **Select**: Black Cotton T-Shirt
   - **Expected**: Black hoodie, white tee, denim jacket
   - **Similarity**: High scores (0.7-0.9) for similar clothing

2. **Select**: Waterproof Rain Jacket
   - **Expected**: Hiking boots, poncho, waterproof items
   - **Similarity**: High scores for rain/waterproof category

3. **Select**: Running Shoes
   - **Expected**: Yoga mat, fitness tracker, athletic wear
   - **Similarity**: High scores for fitness/sports category

4. **Select**: Wireless Earbuds
   - **Expected**: Smartwatch, laptop backpack, tech accessories
   - **Similarity**: High scores for electronics category

## Feature Testing Checklist

### Search Interface
- [ ] Search bar accepts text input
- [ ] Quick suggestions are clickable
- [ ] Loading spinner shows during search
- [ ] Results display in grid layout
- [ ] Each product card shows:
  - [ ] Category icon
  - [ ] Brand name
  - [ ] Product name
  - [ ] Description (truncated)
  - [ ] Rating stars
  - [ ] Price
  - [ ] In stock status
  - [ ] Tags
- [ ] Hover effects work on cards
- [ ] Click on card shows recommendations
- [ ] Empty state shows when no search yet
- [ ] Results count is accurate

### Chat Interface
- [ ] Chat opens in Chat tab
- [ ] Question suggestions are clickable
- [ ] Input field accepts text
- [ ] Send button is disabled when empty
- [ ] Loading dots appear while processing
- [ ] User messages align right (blue)
- [ ] Assistant messages align left (glass)
- [ ] Sources are displayed under answers
- [ ] Messages animate in smoothly
- [ ] Scroll works for long conversations
- [ ] Enter key sends message

### Recommendations
- [ ] Tab switches when product clicked
- [ ] "Based on" text shows source
- [ ] Recommended products display
- [ ] Similarity scores are shown (if available)
- [ ] Can click recommended products for more
- [ ] Empty state when no recommendations
- [ ] Go to Search button works

### UI/UX
- [ ] Dark theme applies consistently
- [ ] Glassmorphism effects visible
- [ ] Gradient text on headings
- [ ] Smooth tab transitions
- [ ] Card hover animations work
- [ ] Button hover/click animations
- [ ] Loading states are clear
- [ ] Responsive on different screen sizes
- [ ] Custom scrollbar styles
- [ ] Background gradients animate

## API Testing

### Using Browser DevTools
1. Open browser DevTools (F12)
2. Go to Network tab
3. Perform actions
4. Check API calls:
   - Status: 200 OK
   - Response time: < 200ms
   - Correct data format

### Using cURL (Command Line)

#### Test Search
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"rain jacket\", \"limit\": 5}"
```

#### Test Chat
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"How do I choose rain gear?\", \"context_limit\": 3}"
```

#### Test Recommendations
```bash
curl -X POST http://localhost:8000/api/recommend \
  -H "Content-Type: application/json" \
  -d "{\"product_id\": \"prod_005\", \"limit\": 5}"
```

#### Get All Products
```bash
curl http://localhost:8000/api/products
```

#### Health Check
```bash
curl http://localhost:8000/api/health
```

## Performance Testing

### Response Time Benchmarks

| Endpoint | Expected Time | Acceptable |
|----------|--------------|------------|
| Search | < 100ms | < 200ms |
| Chat | < 150ms | < 300ms |
| Recommend | < 50ms | < 100ms |
| Products | < 30ms | < 50ms |

### Load Testing (Optional)

Using Apache Bench:
```bash
# Test search endpoint
ab -n 100 -c 10 -p search.json -T application/json http://localhost:8000/api/search
```

Where `search.json`:
```json
{"query": "black shirt", "limit": 10}
```

### Memory Usage
- Backend: ~200-300 MB (model loaded)
- Frontend: ~50-100 MB
- ChromaDB: ~10-20 MB (demo data)

## Edge Cases

### Empty Results
1. Search for "nonexistent product xyz"
   - Should return empty results gracefully
   - Should show helpful empty state

### Special Characters
1. Search for "shirt's & jacket's"
   - Should handle apostrophes and symbols
   - Should still return relevant results

### Very Long Queries
1. Type a very long question in chat
   - Should handle gracefully
   - Should truncate if needed

### Rapid Clicking
1. Click search button multiple times quickly
   - Should debounce/prevent duplicate requests
   - Should show loading state

### Network Errors
1. Stop backend, try searching
   - Should show error message
   - Should not crash frontend

## Browser Compatibility

Test in multiple browsers:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if on Mac)

## Mobile Testing

Test responsive design:
- [ ] Mobile view (< 768px)
- [ ] Tablet view (768px - 1024px)
- [ ] Desktop view (> 1024px)

Features to check on mobile:
- [ ] Search bar is usable
- [ ] Cards stack vertically
- [ ] Tab buttons are accessible
- [ ] Chat interface is usable
- [ ] Text is readable
- [ ] Touch interactions work

## Accessibility Testing

Basic checks:
- [ ] Tab navigation works
- [ ] Focus indicators visible
- [ ] Alt text for icons (if images added)
- [ ] Sufficient color contrast
- [ ] Screen reader compatible (basic)

## Common Issues & Solutions

### Issue: Search returns no results
**Solution**: 
- Check backend is running
- Check browser console for errors
- Verify API URL is correct

### Issue: Chat not responding
**Solution**:
- Check backend initialization completed
- Wait 30 seconds after backend start
- Check documents are indexed

### Issue: Recommendations not showing
**Solution**:
- First perform a search
- Click on a product card
- Check active tab switched to Recommendations

### Issue: Slow performance
**Solution**:
- First request is slower (model warm-up)
- Subsequent requests should be fast
- Check CPU/memory usage

### Issue: UI looks broken
**Solution**:
- Run `npm install` in frontend
- Clear browser cache
- Check tailwind.config.ts exists

## Success Criteria

Your application passes testing if:
1. ✅ All 3 features work (Search, Chat, Recommend)
2. ✅ UI is beautiful and responsive
3. ✅ No console errors
4. ✅ API responds within time limits
5. ✅ Animations are smooth
6. ✅ Data is accurate and relevant

## Test Automation (Future)

### Backend Tests (pytest)
```python
# tests/test_search.py
def test_search_products():
    response = client.post("/api/search", 
        json={"query": "rain jacket", "limit": 5})
    assert response.status_code == 200
    assert len(response.json()["results"]) > 0
```

### Frontend Tests (Jest/React Testing Library)
```typescript
// __tests__/SearchBar.test.tsx
it('calls onSearch when form submitted', () => {
  const mockSearch = jest.fn();
  render(<SearchBar onSearch={mockSearch} />);
  // ... test implementation
});
```

## Reporting Issues

When reporting issues, include:
1. What you were doing
2. What you expected
3. What actually happened
4. Browser and OS
5. Console errors (if any)
6. Screenshots (if relevant)

---

**Happy Testing! 🧪**

For questions or issues, check:
- README.md - Project overview
- QUICKSTART.md - Setup guide
- ARCHITECTURE.md - Technical details
