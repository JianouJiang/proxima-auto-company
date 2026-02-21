# Double Mood Phase 1 — Testing Checklist

**Built:** 2026-02-21 (Day 1 of 3-day experiment)
**Status:** Ready for deployment
**File:** `public/index.html` (single file, ~500 lines)

## Pre-Deployment Testing

### Functional Tests

- [ ] **Mood Selection**
  - [ ] Click each of 4 mood buttons
  - [ ] Selected state shows visual feedback (blue ring, scale up)
  - [ ] Button click progresses to before-rating step
  - [ ] Screen reader announces selected mood

- [ ] **Before Rating Slider**
  - [ ] Slider starts at 5/10
  - [ ] Moving slider updates the value display
  - [ ] Min/max values (0, 10) work
  - [ ] Slider color gradient displays correctly
  - [ ] Arrow keys navigate slider (keyboard accessibility)

- [ ] **Breathing Animation (3 cycles)**
  - [ ] Circle animates smoothly (expands/contracts)
  - [ ] "Breathe in..." shows for 4 seconds
  - [ ] "Breathe out..." shows for 6 seconds
  - [ ] Cycle counter dots update (dot 1 → dot 2 → dot 3)
  - [ ] After 3 cycles (~30 seconds), advances to after-rating
  - [ ] Animation runs at 60 FPS (no jank)
  - [ ] Reduced motion preference respected (animation stops)

- [ ] **After Rating Slider**
  - [ ] Slider starts at previous value (or 5/10?)
  - [ ] Slider updates value display
  - [ ] All functionality same as before-slider

- [ ] **Completion & Improvement Calculation**
  - [ ] Improvement = after - before
  - [ ] If improvement > 0: shows "+X" in green
  - [ ] If improvement = 0: shows "maintained peace"
  - [ ] If improvement < 0: shows improvement message
  - [ ] localStorage saves mood log entry
  - [ ] Page refresh still shows success screen

- [ ] **Restart / Again Button**
  - [ ] Resets app to mood picker
  - [ ] Sliders reset to 5/10
  - [ ] Previous mood log persists in localStorage
  - [ ] Can repeat without refresh

### localStorage Tests

- [ ] **Data Persistence**
  - [ ] Complete 1 breathing exercise
  - [ ] Hard refresh page (Cmd+Shift+R or Ctrl+Shift+R)
  - [ ] Mood logs still exist in browser DevTools > Application > localStorage
  - [ ] localStorage key: `double-mood-logs`
  - [ ] Entry has: `date`, `mood`, `before`, `after`, `improvement`

- [ ] **Multiple Sessions**
  - [ ] Complete 3 separate breathing exercises
  - [ ] Each creates separate localStorage entry
  - [ ] No data loss between exercises

### Accessibility Tests

- [ ] **Keyboard Navigation**
  - [ ] Tab moves through all buttons and sliders
  - [ ] Enter/Space activates buttons
  - [ ] Arrow keys adjust sliders
  - [ ] Tab order makes sense (mood > before > button > etc)

- [ ] **Screen Reader (NVDA/JAWS/VoiceOver)**
  - [ ] Page title reads correctly
  - [ ] Buttons announce emoji + text
  - [ ] Slider labels and values read
  - [ ] Status announcements trigger (e.g., "Starting breathing exercise")
  - [ ] Success message reads with improvement delta

- [ ] **Color Contrast**
  - [ ] Text on background passes WCAG AA (4.5:1)
  - [ ] Slider colors visible for colorblind users
  - [ ] No critical information conveyed by color alone

### Mobile Tests (CRITICAL — 95% of users on phone)

**Test on iOS Safari (iPhone 12+) and Android Chrome:**

- [ ] **Viewport & Responsive**
  - [ ] App fits on screen without horizontal scroll
  - [ ] Text readable without zooming
  - [ ] Circle SVG scales responsively
  - [ ] Buttons touch-friendly (min 44px height)

- [ ] **Performance**
  - [ ] Page loads in <1 second (test on 3G throttle)
  - [ ] Animation smooth on older phones (iPhone 8, Pixel 3)
  - [ ] No layout shift while loading

- [ ] **Touch Interaction**
  - [ ] Sliders work with finger swipe
  - [ ] Buttons responsive to touch
  - [ ] No "hover" state confuses touch users

- [ ] **System Integration**
  - [ ] Can add to home screen (PWA-ready, though not full PWA)
  - [ ] Works in Safari private mode
  - [ ] Works in Chrome incognito

### Browser Compatibility

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Safari iOS 15+
- [ ] Chrome Android

### Visual Polish Tests

- [ ] **Design System Compliance**
  - [ ] Colors match design-system.md specs
  - [ ] Spacing follows Tailwind grid (4px baseline)
  - [ ] Typography matches (system font stack, font sizes)
  - [ ] Border radius consistent (rounded-lg = 8px)

- [ ] **Animations**
  - [ ] Breathing circle easing feels natural
  - [ ] Success message slides up smoothly
  - [ ] Button hover/active states visible
  - [ ] No animation jank or stuttering

- [ ] **Bilingual Content**
  - [ ] English text readable and centered
  - [ ] Chinese text readable and centered
  - [ ] No text overflow in either language
  - [ ] Emojis render consistently across both

### Edge Cases

- [ ] **User cancels breathing mid-exercise**
  - [ ] (Doesn't apply yet — no skip button in Phase 1)

- [ ] **Very fast network vs slow 3G**
  - [ ] Tailwind CDN loads from cache
  - [ ] SVG renders immediately
  - [ ] No Flash of Unstyled Content (FOUC)

- [ ] **Zero JavaScript** (paranoia check)
  - [ ] HTML structure valid without JS
  - [ ] Basic form submission would work (not implemented, but structure allows)

## Deployment Checklist

- [ ] **Code Review**
  - [ ] No console errors
  - [ ] No hardcoded secrets/API keys
  - [ ] No unused code
  - [ ] localStorage key name clear (no conflicts)

- [ ] **Cloudflare Pages Setup**
  ```bash
  wrangler pages deploy projects/double-mood/public --project-name=double-mood
  ```
  - [ ] Deployment succeeds
  - [ ] HTTPS certificate auto-generated
  - [ ] URL: https://double-mood.pages.dev

- [ ] **DNS/Custom Domain (if using)**
  - [ ] CNAME points to Cloudflare Pages
  - [ ] SSL certificate valid

- [ ] **Analytics Placeholder**
  - [ ] (Not implemented in Phase 1, but prepare for Phase 2)

## Post-Deployment (Live Testing)

- [ ] **Real device testing**
  - [ ] Access from real iPhone
  - [ ] Access from real Android
  - [ ] Breathing animation smooth on real devices

- [ ] **Share-ability Check**
  - [ ] QR code to app works
  - [ ] Share link works
  - [ ] Open Graph meta tags set (if needed for Phase 2)

- [ ] **First User Experience**
  - [ ] No confusing onboarding
  - [ ] Clear call-to-action
  - [ ] Success message feels rewarding

## Known Limitations (Phase 1)

- No email/account system
- No weekly reports
- No payment
- No backend
- No authentication
- No weekly digest emails
- No detailed analytics (beyond localStorage)
- No user segmentation
- No A/B testing

These are all Phase 2+ features.

## Success Metrics (3-day experiment)

**Ship metrics:**
- Loads <1s ✓
- Breathing animation 60fps ✓
- localStorage works ✓
- Bilingual UI correct ✓
- Mobile responsive ✓

**User metrics (by Day 3):**
- 10+ visitors
- 5+ completed exercises
- 3+ returning visitors

**If all tests pass and metrics hit:** Ship to production and ask founder to tweet.
**If metrics miss:** Kill project, pivot to different hypothesis.

---

**Tested By:** [QA Bach]
**Date:** [TBD]
**Status:** [PENDING]
