# ConnectPath — Manual Test Cases

**For qa-bach: Complete testing checklist before launch**

---

## Test Environment Setup

1. **Browser**: Chrome/Firefox/Safari (test all three)
2. **Mobile**: iOS Safari + Android Chrome (real devices)
3. **Network**: Normal + Slow 3G (DevTools throttling)

---

## Test Suite 1: Core Search Functionality

### Test 1.1: Happy Path - Well-Connected Users

**Input**:
- Person A: `torvalds`
- Person B: `tj`

**Expected Result**:
- ✅ Path found (likely 1-2 degrees)
- ✅ Shows connection chain with names
- ✅ Displays degree count
- ✅ Shows confidence score (> 70%)
- ✅ "New Search" button visible

**Why this test**: Both are famous open source developers, highly connected

---

### Test 1.2: No Path - Unconnected Users

**Input**:
- Person A: `testuser99999`
- Person B: `randomuser88888`

**Expected Result**:
- ✅ "No path found" message
- ✅ Shows "X profiles searched"
- ✅ Provides suggestions (try different names, etc.)
- ✅ "Try Again" button visible

**Why this test**: Random users have no followers, should fail gracefully

---

### Test 1.3: Self-Search

**Input**:
- Person A: `torvalds`
- Person B: `torvalds`

**Expected Result**:
- ✅ Path with 1 node (same person)
- ✅ Degree: 0
- ✅ Confidence: 100%

**Why this test**: Edge case, should handle same person gracefully

---

### Test 1.4: Invalid Username

**Input**:
- Person A: `this-user-definitely-does-not-exist-12345`
- Person B: `tj`

**Expected Result**:
- ✅ "No path found" or "User not found" message
- ✅ Suggestion to check spelling
- ✅ No 500 error

**Why this test**: Error handling for non-existent users

---

### Test 1.5: Empty Input

**Input**:
- Person A: (empty)
- Person B: (empty)

**Expected Result**:
- ✅ Browser validation prevents submit
- ✅ "Please fill out this field" message
- ✅ Button disabled or shows error

**Why this test**: Client-side validation works

---

## Test Suite 2: Rate Limiting

### Test 2.1: First 3 Searches

**Steps**:
1. Open in fresh incognito window
2. Do search 1 → Check counter shows "2/3 left"
3. Do search 2 → Check counter shows "1/3 left"
4. Do search 3 → Check counter shows "0/3 left"

**Expected Result**:
- ✅ Counter decrements correctly
- ✅ All 3 searches execute successfully

---

### Test 2.2: 4th Search Shows Paywall

**Steps**:
1. After 3 searches (from Test 2.1)
2. Try 4th search

**Expected Result**:
- ✅ Paywall appears: "You've used your free searches!"
- ✅ Gumroad link visible: "Upgrade for $9.99/month"
- ✅ Search button disabled
- ✅ No search executes

---

### Test 2.3: Daily Reset

**Steps**:
1. Do 3 searches
2. Change system date to tomorrow (or wait 24 hours)
3. Refresh page

**Expected Result**:
- ✅ Counter resets to "3/3 left"
- ✅ Can search again

**Note**: This is client-side only. Server-side KV resets at UTC midnight.

---

### Test 2.4: Server-Side Rate Limit Bypass Attempt

**Steps**:
1. Do 3 searches
2. Clear localStorage (DevTools → Application → Local Storage → Clear)
3. Refresh page
4. Try another search

**Expected Result**:
- ✅ Client shows "3/3 left" (localStorage cleared)
- ✅ Server still blocks 4th search (KV remembers IP)
- ✅ Returns 429 error: "Daily free search limit reached"

---

## Test Suite 3: Bilingual Support

### Test 3.1: Language Toggle

**Steps**:
1. Load page (default: English)
2. Click language toggle button (top right)
3. Verify all text switches to Chinese
4. Click again
5. Verify all text switches back to English

**Expected Result**:
- ✅ All labels switch (Person A → 起点人物)
- ✅ Button text switches (Find Connection → 查找连接)
- ✅ Help text switches
- ✅ Footer switches
- ✅ Tagline switches

---

### Test 3.2: Search in Chinese

**Steps**:
1. Toggle to Chinese
2. Enter search
3. Click "查找连接"
4. Verify results display

**Expected Result**:
- ✅ Search executes (backend doesn't care about UI language)
- ✅ Results show in correct language
- ✅ Error messages in Chinese if applicable

---

### Test 3.3: Language Persistence

**Steps**:
1. Toggle to Chinese
2. Do a search
3. Click "新搜索" (New Search)
4. Check if language stays Chinese

**Expected Result**:
- ✅ Language stays Chinese after new search
- ✅ Language toggle state persists during session

**Note**: Language does NOT persist across page refreshes (by design, no localStorage used)

---

## Test Suite 4: Mobile Responsiveness

### Test 4.1: iPhone (Portrait)

**Device**: iPhone 12/13/14 (390px width)

**Expected Result**:
- ✅ No horizontal scroll
- ✅ Input fields full width
- ✅ Buttons tapable (min 44px height)
- ✅ Text readable (min 16px font)
- ✅ Language toggle button visible and tapable
- ✅ Results display properly (no overflow)

---

### Test 4.2: Android (Portrait)

**Device**: Pixel 5 (393px width)

**Expected Result**:
- Same as Test 4.1
- ✅ No layout differences from iOS

---

### Test 4.3: Tablet (iPad)

**Device**: iPad (768px width)

**Expected Result**:
- ✅ Layout centered (max-width 640px)
- ✅ Generous white space on sides
- ✅ All features work same as desktop

---

### Test 4.4: Small Phone (Landscape)

**Device**: iPhone SE (667px width, landscape)

**Expected Result**:
- ✅ Header doesn't overflow
- ✅ Form still usable
- ✅ Results readable

---

## Test Suite 5: Error Handling

### Test 5.1: Network Offline

**Steps**:
1. Open DevTools → Network → Offline
2. Try to search

**Expected Result**:
- ✅ Loading spinner shows
- ✅ After timeout, shows error: "Search failed" or "Network error"
- ✅ Graceful error message, not blank screen

---

### Test 5.2: GitHub API Down (Simulated)

**Steps**:
1. Temporarily break `GITHUB_TOKEN` in Cloudflare Dashboard
2. Try to search

**Expected Result**:
- ✅ Returns error message (not 500)
- ✅ Suggests trying later
- ✅ Does not crash

---

### Test 5.3: Slow Connection (3G)

**Steps**:
1. DevTools → Network → Slow 3G
2. Try to search

**Expected Result**:
- ✅ Loading spinner shows
- ✅ Eventually returns result (may take 10-15 seconds)
- ✅ No timeout error (unless backend times out)

---

## Test Suite 6: UI/UX Details

### Test 6.1: Loading State

**Steps**:
1. Enter search
2. Click "Find Connection"
3. Observe loading state

**Expected Result**:
- ✅ Form disappears immediately
- ✅ Loading spinner appears
- ✅ Text shows "Searching for connections..."
- ✅ Spinner animates smoothly

---

### Test 6.2: Success State

**Steps**:
1. Do successful search (e.g., `torvalds` → `tj`)

**Expected Result**:
- ✅ Green border on results card
- ✅ Checkmark (✓) in title
- ✅ Path displays with arrows (↓)
- ✅ Stats show degree + confidence
- ✅ "New Search" button works

---

### Test 6.3: Failure State

**Steps**:
1. Do failed search (e.g., `randomuser123` → `randomuser456`)

**Expected Result**:
- ✅ Red border on results card
- ✅ X icon in title
- ✅ Error message explains why
- ✅ Suggestions provided
- ✅ "Try Again" button works

---

### Test 6.4: Back to Search

**Steps**:
1. Do any search (success or fail)
2. Click "New Search" or "Try Again"

**Expected Result**:
- ✅ Results disappear
- ✅ Form reappears
- ✅ Input fields cleared
- ✅ Ready for new search

---

## Test Suite 7: Integration Tests

### Test 7.1: Gumroad Link

**Steps**:
1. Do 3 searches to hit paywall
2. Click "Upgrade for $9.99/month" link

**Expected Result**:
- ✅ Opens Gumroad in new tab
- ✅ Shows correct product (ConnectPath Unlimited)
- ✅ Price shows $9.99/month

---

### Test 7.2: Multiple Browser Tabs

**Steps**:
1. Open ConnectPath in 2 tabs
2. Do 2 searches in Tab 1
3. Do 1 search in Tab 2
4. Check counter in both tabs

**Expected Result**:
- ✅ Both tabs should show "0/3 left" (localStorage syncs)
- ✅ 4th search in either tab shows paywall

**Note**: If tabs don't sync, that's OK (acceptable UX degradation)

---

### Test 7.3: Different IPs

**Steps**:
1. Do 3 searches from IP 1 (e.g., home WiFi)
2. Switch to IP 2 (e.g., mobile hotspot)
3. Try another search

**Expected Result**:
- ✅ Can search again (server-side rate limit is per-IP)
- ✅ New IP gets fresh 3 searches

---

## Test Suite 8: Performance

### Test 8.1: Page Load Speed

**Steps**:
1. Open DevTools → Network → Clear cache
2. Load ConnectPath
3. Check load time

**Expected Result**:
- ✅ DOMContentLoaded < 1 second
- ✅ Fully loaded < 2 seconds
- ✅ No large assets (images, fonts)

---

### Test 8.2: Search Latency

**Steps**:
1. Do search with well-connected users
2. Measure time from click to results

**Expected Result**:
- ✅ < 5 seconds for most searches
- ✅ < 10 seconds worst case

---

## Test Suite 9: Accessibility

### Test 9.1: Keyboard Navigation

**Steps**:
1. Use Tab key to navigate
2. Press Enter to submit form
3. Navigate results with keyboard

**Expected Result**:
- ✅ Can tab through all inputs
- ✅ Enter key submits form
- ✅ Buttons have focus states

---

### Test 9.2: Screen Reader (Optional)

**Steps**:
1. Enable VoiceOver (Mac) or TalkBack (Android)
2. Navigate page

**Expected Result**:
- ✅ Form labels read correctly
- ✅ Button purpose clear
- ✅ Results readable

**Note**: Not critical for MVP, but good to check

---

## Critical Bugs (Ship Blockers)

These MUST work before launch:

- [ ] Search executes and returns result (success or fail)
- [ ] Rate limiting prevents >3 searches
- [ ] Mobile layout doesn't break
- [ ] Gumroad link works
- [ ] No console errors on page load

## Non-Critical Bugs (Fix in V1.1)

These can be fixed after launch:

- Low confidence scores (< 50%)
- Slow searches (> 10 seconds)
- Language toggle edge cases
- Search history not saved

---

## Sign-Off Checklist

After all tests pass:

- [ ] Tested in Chrome
- [ ] Tested in Safari
- [ ] Tested on iPhone (real device)
- [ ] Tested on Android (real device)
- [ ] Tested rate limiting
- [ ] Tested bilingual toggle
- [ ] Tested Gumroad link
- [ ] No console errors
- [ ] No visual bugs
- [ ] Performance acceptable (< 5s search)

**QA Sign-Off**:

Name: _______________
Date: _______________
Status: ☐ Pass ☐ Fail (see bug report)

---

**Total Test Cases**: 35
**Estimated Testing Time**: 2-3 hours
**Critical Tests**: 15 (must pass before launch)
**Nice-to-Have Tests**: 20 (can fix later)

---

**For qa-bach**: Focus on critical tests first. If those pass, we ship. Non-critical bugs can be fixed in V1.1 after launch.
