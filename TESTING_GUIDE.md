# Testing Guide: Problem History, Favorites, and Export/Share

## Setup

1. Ensure backend is running:
   ```bash
   cd backend
   python main.py
   # Should see "Uvicorn running on http://127.0.0.1:8000"
   ```

2. Open frontend (choose one method):
   ```bash
   # Option A: Direct file
   open frontend_backend_integration.html

   # Option B: Python server
   python3 -m http.server 8001
   # Then visit: http://localhost:8001/frontend_backend_integration.html
   ```

## Test Scenarios

### Scenario 1: Problem History

**Goal**: Verify that problem history saves and persists

1. **Initial state**
   - Load page
   - History panel should NOT be visible (no history yet)

2. **First problem**
   - Type: "How do I prioritize product features?"
   - Click "ASK"
   - Wait for results
   - Scroll up - **History panel should now appear**
   - Panel shows: problem text, category, result count, date

3. **Second problem**
   - Type: "How do I hire better engineers?"
   - Click "ASK"
   - Results appear
   - **History panel should show 2 items**, newest first

4. **Re-ask from history**
   - In history panel, click "Re-ask" on first problem
   - Input field populates with problem text
   - Results load automatically

5. **Persistence**
   - Press F5 to refresh page
   - **History panel should still show both problems**
   - Data persists in localStorage

6. **Clear history**
   - Click "Clear All" in history panel
   - Confirm in dialog
   - **History panel disappears**
   - Refresh page - still gone

7. **History limit (20 items)**
   - Add 25 different problems
   - Go back to beginning
   - **Only last 20 problems should remain**

**Expected**: ✅ All history persists across sessions, Re-ask works, limit enforced

---

### Scenario 2: Favorites

**Goal**: Verify that favorite solutions can be saved and viewed

1. **Initial state**
   - Load page
   - No "Saved Insights" panel visible

2. **Ask a question**
   - Type: "How do I build a great product?"
   - Click "ASK"
   - Wait for results
   - **Each solution card should have a star (☆) icon** in top-right

3. **Add favorites**
   - Click star on first solution → **should turn filled (★) and gold**
   - Star on second solution
   - Scroll down - **"Saved Insights" panel appears** with 2 favorite cards

4. **Verify favorite display**
   - Each card shows:
     - Speaker icon (e.g., 🎯)
     - Speaker name
     - Problem text (small)
     - Quote text
   - X button to remove

5. **Remove favorite**
   - In "Saved Insights", click X on a favorite
   - **Card disappears from panel**
   - Scroll up - star in original card is now empty (☆) again

6. **Persistence**
   - Refresh page (F5)
   - Ask a different question
   - **"Saved Insights" panel still shows saved favorites**
   - Star state matches for any repeated problems

7. **Multiple problems**
   - Ask "How do I communicate better?"
   - Star 2 solutions
   - Ask "How do I scale?"
   - Star 1 solution
   - Scroll down - **"Saved Insights" shows all 5 favorites grouped**

**Expected**: ✅ Favorites save locally, UI state syncs, cross-problem tracking works

---

### Scenario 3: Export (JSON)

**Goal**: Verify JSON export downloads correctly

1. **Get results**
   - Ask: "How do I hire better engineers?"
   - Wait for results

2. **Open export modal**
   - Click "📥 Export" button (top right of results)
   - **Modal appears** with title "Export Results"
   - Two buttons visible: "📄 Export as JSON", "📝 Export as Text"

3. **Export as JSON**
   - Click "📄 Export as JSON"
   - **File downloads** named `wwld-export-[timestamp].json`
   - Modal closes

4. **Verify JSON content**
   - Open downloaded file in text editor
   - **Structure should include**:
     ```json
     {
       "problem": "How do I hire better engineers?",
       "category": "Building Teams",
       "timestamp": "2024-01-15T10:30:00.000Z",
       "solutions": [
         {
           "speaker": "...",
           "role": "...",
           "icon": "...",
           "insight": "...",
           "framework1": "...",
           "framework2": "...",
           "episode": "...",
           "timestamp": "..."
         }
       ]
     }
     ```

5. **Multiple exports**
   - Ask different question
   - Export as JSON again
   - **New file downloads** with different timestamp
   - Content matches new problem

**Expected**: ✅ JSON files download with correct structure and data

---

### Scenario 4: Export (Text)

**Goal**: Verify text export downloads in human-readable format

1. **Get results** (from previous scenario)

2. **Open export modal**
   - Click "📥 Export"
   - **Modal should appear**

3. **Export as text**
   - Click "📝 Export as Text"
   - **File downloads** named `wwld-export-[timestamp].txt`
   - Modal closes

4. **Verify text content**
   - Open in text editor
   - **Should be human-readable**:
     ```
     WWLD - What Would Lenny Do?
     ==================================================

     Problem: How do I hire better engineers?
     Category: Building Teams
     Date: 1/15/2024, 10:30:00 AM

     Solution 1: Jake Knapp
     --------------------------------------------------
     Role: Designer & Strategist
     Insight: "The best engineers..."
     Frameworks: Energy Framework, RICE Model
     Episode: Episode 42: Hiring Strategies
     Timestamp: 12:34
     ```

**Expected**: ✅ Text file is readable and includes all solution data

---

### Scenario 5: Share (Generate Link)

**Goal**: Verify shareable URL generation and copying

1. **Get results**
   - Ask: "What's the best way to launch?"
   - Wait for results

2. **Open share modal**
   - Click "🔗 Share" (top right of results)
   - **Share modal appears** with title "Share Results"
   - Link field shows a long URL starting with current page URL
   - **URL format**: `http://localhost:8001/frontend_backend_integration.html?shared=[long-encoded-string]`

3. **Copy link**
   - Click "📋 Copy Link"
   - **Feedback message appears**: "✓ Copied to clipboard!"
   - Message disappears after 2 seconds

4. **Verify copy**
   - Paste in browser address bar or text editor
   - URL should be valid and very long

**Expected**: ✅ URL generated and copied to clipboard successfully

---

### Scenario 6: Share (Load Shared Results)

**Goal**: Verify that shared links load correctly in new session

1. **Generate share link** (from Scenario 5)
   - Copy share URL from modal

2. **Open in new window**
   - Right-click "Open in new tab"
   - OR manually paste URL in new browser tab
   - **Page loads**
   - **Results appear immediately** (no need to click "ASK")
   - Same problem and solutions display

3. **Verify UI state**
   - Results section is active
   - All 3 solutions visible with correct data
   - Can scroll and interact normally

4. **Test interaction in shared view**
   - Try starring solutions → **favorites work**
   - Try exporting → **export works**
   - Try generating new share link → **generates new URL**
   - Go back → **returns to input screen**

5. **Cross-browser share**
   - Copy URL
   - Open in different browser (if available)
   - Paste in address bar
   - **Results load in new browser too**

6. **Incognito/Private share**
   - Copy URL
   - Open incognito/private window
   - Paste URL
   - **Results still load** (history/favorites are session-specific)

**Expected**: ✅ Shared links work across browsers and sessions

---

### Scenario 7: Integration Test (All Features)

**Goal**: Verify features work together seamlessly

1. **Complete workflow**
   ```
   Ask "How do I build a successful product?"
   ↓ (History: +1 entry)
   Results appear
   ↓
   Star 2 solutions
   ↓ (Favorites panel shows 2 cards)
   Click "Export as JSON"
   ↓ (Download wwld-export-[timestamp].json)
   Click "Share"
   ↓ (Generate URL)
   Copy link
   ↓
   Open new tab
   Paste URL
   ↓ (Same results appear)
   Refresh page
   ↓ (All features still work)
   ```

2. **Verify state after workflow**
   - History panel shows problem
   - Favorites panel shows 2 solutions
   - Can re-ask from history
   - Can remove from favorites
   - Exported file is valid
   - Shared URL works

**Expected**: ✅ All features work together without conflicts

---

## Edge Cases to Test

### Edge Case 1: Empty Results
- Ask extremely vague question (e.g., "xyz")
- If no solutions found, modal shouldn't appear
- Back button works normally

### Edge Case 2: Duplicate History Entries
- Ask "How do I prioritize?"
- Ask same question again
- History should show only 1 entry (most recent)

### Edge Case 3: localStorage Disabled
- Disable localStorage in browser dev tools
- Ask question
- **Should not crash**, history/favorites just won't persist
- Export/Share should still work

### Edge Case 4: Long Problem Text
- Ask 200+ character question
- History displays with ellipsis (truncated)
- Export/Share includes full text

### Edge Case 5: Favorites Without Results Visible
- Ask question, star solution
- Go back to input
- Refresh page
- Favorites panel should still be visible on results (if you ask same question)

---

## Debugging

### Check localStorage
```javascript
// In browser console
localStorage.getItem('problemHistory')  // Shows history array
localStorage.getItem('favorites')       // Shows favorites array
localStorage.clear()                    // Clear all data
```

### Check Clipboard
- If copy button doesn't show feedback, browser might not support Clipboard API
- Check browser console for errors
- Test in Chrome 63+ or newer

### Network issues
- If backend not responding, "Failed to connect" error appears
- Check: `http://localhost:8000/health`
- Ensure backend is running on port 8000

---

## Success Criteria

✅ **Problem History**
- [x] Saves after each query
- [x] Shows in collapsible panel
- [x] Re-ask functionality works
- [x] Persists across page refreshes
- [x] Limits to 20 entries
- [x] Can be cleared

✅ **Favorites**
- [x] Star buttons appear on solutions
- [x] Toggle filled/empty state
- [x] Save to localStorage
- [x] Display in "Saved Insights" panel
- [x] Persist across sessions
- [x] Can be removed

✅ **Export**
- [x] Modal appears with options
- [x] JSON export downloads
- [x] Text export downloads
- [x] Files contain correct data

✅ **Share**
- [x] Generate URL with encoded results
- [x] Copy to clipboard works
- [x] Shared URL loads results
- [x] Works across browsers/sessions

✅ **Integration**
- [x] Features don't conflict
- [x] UI responsive and polished
- [x] No console errors
- [x] Mobile responsive

---

## Reporting Issues

If you find issues, note:
1. Browser (Chrome, Firefox, Safari, Edge, version)
2. What you were trying to do
3. Expected vs actual behavior
4. Console errors (F12 → Console tab)
5. localStorage state (check with `localStorage.getItem('problemHistory')`)
