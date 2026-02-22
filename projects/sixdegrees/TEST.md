# SixDegrees V2 — Test Plan

**Version:** 2.0 (Web Dashboard)
**Date:** 2026-02-22
**Status:** Ready for QA

---

## Overview

This document provides a comprehensive test plan for SixDegrees V2 web application.

**Scope:**
- Frontend (3 HTML pages)
- Backend (3 API endpoints)
- Database (D1 operations)
- Email integration (Gmail SMTP)
- Bilingual support (EN/中文)

**Test Environment:**
- Local: `wrangler pages dev`
- Production: `https://sixdegrees.pages.dev`

---

## Prerequisites

Before testing, ensure:
- ✅ D1 database created and migrated
- ✅ Environment variables set (`ANTHROPIC_API_KEY`, `GMAIL_ADDRESS`, `GMAIL_APP_PASSWORD`)
- ✅ Gmail App Password generated and tested
- ✅ `npm install` completed in project directory

---

## Test Matrix

| Test ID | Feature | Priority | Status |
|---------|---------|----------|--------|
| T1 | Landing page loads | P0 | ⬜ |
| T2 | Intake form validation | P0 | ⬜ |
| T3 | Campaign creation | P0 | ⬜ |
| T4 | Dashboard rendering | P0 | ⬜ |
| T5 | Language toggle | P1 | ⬜ |
| T6 | Email sending | P0 | ⬜ |
| T7 | Mobile responsiveness | P1 | ⬜ |
| T8 | Payment links | P1 | ⬜ |
| T9 | API error handling | P1 | ⬜ |
| T10 | Cross-browser compatibility | P2 | ⬜ |

**Priority:**
- P0: Critical (must pass before launch)
- P1: High (should pass before launch)
- P2: Medium (nice to have)

---

## Functional Tests

### T1: Landing Page Load

**Goal:** Verify landing page loads correctly with all sections.

**Steps:**
1. Open `https://sixdegrees.pages.dev/` (or `http://localhost:8788/`)
2. Scroll through entire page
3. Click language toggle (EN → 中文 → EN)
4. Click "Start Your First Connection" button

**Expected Results:**
- Page loads in < 2 seconds
- All 7 sections visible (Header, Hero, Proof Points, Trust, Pricing, CTA, Footer)
- Language toggle works (all text changes)
- CTA button redirects to `/intake.html`
- No console errors

**Pass Criteria:**
- ✅ All sections render
- ✅ Language toggle functional
- ✅ CTA button works
- ✅ No JavaScript errors

---

### T2: Intake Form Validation

**Goal:** Test form validation and character limits.

**Steps:**
1. Navigate to `/intake.html`
2. Leave all fields empty, try to submit
3. Fill only 3/6 fields
4. Fill all fields with valid data:
   - Name: "Test User"
   - Email: "test@example.com"
   - Background: "I am a founder of a tech startup working on AI solutions." (repeat to ~200 chars)
   - Target Name: "Elon Musk"
   - Target Company: "CEO, Tesla"
   - Target Reason: "I want to discuss partnership opportunities in the EV space." (repeat to ~300 chars)
5. Watch character counters update
6. Try to exceed 500 chars in Background field
7. Submit form

**Expected Results:**
- Submit button disabled until all 6 fields filled
- Progress bar shows 0/6 → 3/6 → 6/6
- Character counters show "0/500" → "200/500"
- Cannot type beyond 500 characters
- Submit button enabled when all fields valid
- Form shows loading state ("Analyzing your request...")
- Redirects to dashboard after ~3-5 seconds

**Pass Criteria:**
- ✅ Validation prevents empty submission
- ✅ Character limits enforced
- ✅ Progress bar accurate
- ✅ Submit succeeds with valid data
- ✅ Redirect to dashboard with campaign ID in URL

---

### T3: Campaign Creation (API Test)

**Goal:** Verify backend creates campaign and calls Claude API.

**Steps:**
1. Submit intake form (see T2)
2. Wait for redirect to dashboard
3. Extract campaign ID from URL: `?campaign=camp_...`
4. Verify in database:
   ```bash
   wrangler d1 execute sixdegrees-db --command="SELECT * FROM campaigns WHERE id='camp_...';"
   ```
5. Check `results` field contains JSON strategy

**Expected Results:**
- Campaign record created in `campaigns` table
- User record created in `users` table (if new email)
- `results` field contains valid JSON:
  ```json
  {
    "strategy": "...",
    "selected_path": { "degree": 3, "confidence": 0.85, ... },
    "target_analysis": "..."
  }
  ```
- Campaign status is "ready"

**Pass Criteria:**
- ✅ Campaign created successfully
- ✅ Strategy JSON valid and non-empty
- ✅ User created if new email
- ✅ Redirect to correct dashboard URL

---

### T4: Dashboard Rendering

**Goal:** Test all 4 tabs and components render correctly.

**Steps:**
1. Open dashboard from T3 (with valid campaign ID)
2. Verify Tab 1 (Your Campaign):
   - Status badge visible
   - 6-degree chain renders (desktop: horizontal, mobile: vertical)
   - Strategy text displayed
   - Email carousel shows placeholder (no emails yet)
   - "Start Campaign" button visible
3. Click Tab 2 (Connections)
   - Shows "No emails sent yet"
4. Click Tab 3 (Credits & Payment)
   - Shows Free plan
   - 3 pricing cards visible
5. Click Tab 4 (Settings)
   - Email and name fields populated
   - Language toggle buttons visible
6. Click "Refresh" button
7. Wait 30 seconds, observe auto-refresh

**Expected Results:**
- All 4 tabs switch correctly
- Tab 1 shows strategy, chain, and buttons
- Tab 2 shows empty state message
- Tab 3 shows pricing cards with "Upgrade" links
- Tab 4 shows user info
- Refresh button fetches latest data
- Auto-refresh triggers every 30 seconds

**Pass Criteria:**
- ✅ All 4 tabs functional
- ✅ 6-degree chain renders on desktop
- ✅ Mobile version stacks vertically
- ✅ Auto-refresh works
- ✅ No console errors

---

### T5: Language Toggle

**Goal:** Test bilingual support across all pages.

**Steps:**
1. Landing page → Click "中文"
   - Verify all text changes to Chinese
   - Reload page → Verify Chinese persists
2. Intake form → Click "EN"
   - Verify all text changes to English
   - Verify placeholders change
3. Dashboard → Toggle language multiple times
   - Verify all tabs support both languages
   - Check email carousel, strategy text, buttons

**Expected Results:**
- Every text element with `data-en` and `data-zh` attributes changes
- Placeholders update in form fields
- Language preference saved to localStorage
- Language persists across page reloads
- No layout breaks with Chinese characters

**Pass Criteria:**
- ✅ All pages support EN and 中文
- ✅ Persistence works via localStorage
- ✅ No text overflow with Chinese
- ✅ Font renders CJK characters correctly

---

### T6: Email Sending

**Goal:** Test email queuing and sending via Gmail SMTP.

**Steps:**
1. Dashboard → Click "Start Campaign" button
2. Verify email preview modal opens
3. Modal shows:
   - To: (recipient email)
   - Subject: (auto-generated)
   - Body: (full email text)
4. Click "Send As-Is"
5. Verify email queued in database:
   ```bash
   wrangler d1 execute sixdegrees-db --command="SELECT * FROM email_outreach WHERE campaign_id='camp_...';"
   ```
6. Run local Gmail SMTP script:
   ```bash
   node send-gmail.js --campaign-id camp_...
   ```
7. Check email inbox for received email
8. Refresh dashboard
9. Verify email status changed to "sent"

**Expected Results:**
- Modal shows correct recipient and content
- Email created in DB with status "queued"
- Gmail script sends email successfully
- Email received in inbox within 1 minute
- Dashboard updates status to "sent" after refresh
- Email card in carousel shows "✓ Sent" badge

**Pass Criteria:**
- ✅ Email queued correctly
- ✅ Gmail SMTP sends successfully
- ✅ Email received in inbox
- ✅ Dashboard reflects sent status
- ✅ No errors in Gmail script output

---

### T7: Mobile Responsiveness

**Goal:** Verify app works on mobile devices.

**Test Devices:**
- iPhone SE (375px width)
- iPhone 12 (390px width)
- iPad (768px width)

**Steps for each device:**
1. Open landing page
   - Verify hero section stacks vertically
   - Check pricing cards are 1 column on mobile
2. Open intake form
   - Verify form fields are full-width
   - Test character counter visibility
3. Open dashboard
   - Verify 6-degree chain stacks vertically
   - Test email carousel is swipeable
   - Check all tabs accessible (horizontal scroll if needed)

**Expected Results:**
- All touch targets ≥ 44x44px
- No horizontal scroll on any screen
- Text readable without zooming
- Buttons and form fields accessible
- 6-degree chain vertical on mobile
- Email carousel swipeable

**Pass Criteria:**
- ✅ No layout breaks on 375px width
- ✅ All interactions work with touch
- ✅ No horizontal scroll
- ✅ Touch targets meet 44x44px minimum

---

### T8: Payment Links

**Goal:** Verify Stripe Payment Links work.

**Steps:**
1. Dashboard → Credits & Payment tab
2. Click "Upgrade" on Starter plan ($29/mo)
3. Verify Stripe checkout page opens in new tab
4. (Do not complete payment in testing)
5. Close Stripe tab
6. Repeat for Pro plan ($99/mo)

**Expected Results:**
- Stripe Payment Link opens in new tab
- Correct pricing displayed ($29 or $99)
- Billing interval shows "monthly"
- After payment (in production), user redirected to `/success.html`

**Pass Criteria:**
- ✅ Links open Stripe checkout
- ✅ Correct pricing shown
- ✅ Links target "_blank" (new tab)

**Note:** Stripe Payment Links must be configured manually in Stripe Dashboard before testing.

---

### T9: API Error Handling

**Goal:** Test API gracefully handles errors.

**Test Cases:**

#### 9.1: Invalid Campaign ID
```bash
curl https://sixdegrees.pages.dev/api/campaign/invalid_id
```
**Expected:** `{ "success": false, "error": "Campaign not found" }`
**Status Code:** 404

#### 9.2: Missing Required Fields
```bash
curl -X POST https://sixdegrees.pages.dev/api/intake \
  -H "Content-Type: application/json" \
  -d '{ "user_email": "test@example.com" }'
```
**Expected:** `{ "success": false, "error": "Missing required fields" }`
**Status Code:** 400

#### 9.3: Invalid Email Format
Submit intake form with email "not-an-email"
**Expected:** Browser validation error, form blocked

#### 9.4: Network Error
1. Disconnect internet
2. Submit intake form
3. **Expected:** Error state shown: "Network error. Please try again."

**Pass Criteria:**
- ✅ All error responses have proper HTTP status codes
- ✅ Error messages are user-friendly (no stack traces)
- ✅ Frontend shows error states gracefully

---

### T10: Cross-Browser Compatibility

**Goal:** Verify app works in major browsers.

**Browsers to Test:**
- Chrome (latest)
- Safari (latest)
- Firefox (latest)
- Edge (latest)

**Test Matrix:**
| Feature | Chrome | Safari | Firefox | Edge |
|---------|--------|--------|---------|------|
| Landing page load | ⬜ | ⬜ | ⬜ | ⬜ |
| Intake form submit | ⬜ | ⬜ | ⬜ | ⬜ |
| Dashboard tabs | ⬜ | ⬜ | ⬜ | ⬜ |
| Language toggle | ⬜ | ⬜ | ⬜ | ⬜ |
| Email modal | ⬜ | ⬜ | ⬜ | ⬜ |

**Pass Criteria:**
- ✅ All features work in all 4 browsers
- ⚠️ Minor styling differences acceptable
- ❌ Blocking bugs must be fixed

**Known Issues:**
- Safari Private Mode may block localStorage (language won't persist)

---

## Performance Tests

### P1: Page Load Performance

**Tool:** Chrome DevTools Lighthouse

**Targets:**
- Performance Score: ≥ 90
- First Contentful Paint: < 1.0s
- Largest Contentful Paint: < 2.5s
- Time to Interactive: < 3.0s

**Test:**
1. Open Chrome DevTools → Lighthouse
2. Run audit on each page
3. Record scores

**Pass Criteria:**
- ✅ All pages score ≥ 90
- ✅ LCP < 2.5s
- ✅ No blocking resources

---

### P2: API Response Time

**Targets:**
- POST /api/intake: < 5s (includes Claude API call)
- GET /api/campaign/:id: < 500ms
- POST /api/send: < 300ms

**Test:**
```bash
# Test intake API
time curl -X POST https://sixdegrees.pages.dev/api/intake -d '{...}'

# Test campaign API
time curl https://sixdegrees.pages.dev/api/campaign/camp_...

# Test send API
time curl -X POST https://sixdegrees.pages.dev/api/send -d '{...}'
```

**Pass Criteria:**
- ✅ All endpoints respond within target times
- ✅ No timeouts (30s limit)

---

### P3: Database Query Performance

**Test:**
```bash
# Campaign fetch (should be instant)
time wrangler d1 execute sixdegrees-db --command="SELECT * FROM campaigns WHERE id='camp_...';"

# Email history (should scale to 100+ emails)
time wrangler d1 execute sixdegrees-db --command="SELECT * FROM email_outreach WHERE campaign_id='camp_...';"
```

**Pass Criteria:**
- ✅ Queries return in < 100ms
- ✅ Indexes improve query speed

---

## Security Tests

### S1: SQL Injection

**Test:**
```bash
curl https://sixdegrees.pages.dev/api/campaign/camp_' OR '1'='1
```
**Expected:** 404 (campaign not found), not SQL error

**Pass Criteria:**
- ✅ Parameterized queries prevent injection
- ✅ No SQL error messages exposed

---

### S2: XSS Prevention

**Test:**
1. Intake form → Enter `<script>alert('XSS')</script>` in Target Name field
2. Submit form
3. View dashboard

**Expected:** Script tags escaped, no alert popup

**Pass Criteria:**
- ✅ All user input sanitized
- ✅ No JavaScript execution from user input

---

### S3: Environment Variables

**Test:**
1. Check public HTML files don't contain:
   - `ANTHROPIC_API_KEY`
   - `GMAIL_APP_PASSWORD`
2. Verify secrets only in Cloudflare Workers environment

**Pass Criteria:**
- ✅ No secrets in client-side code
- ✅ API keys only accessible server-side

---

## Regression Tests

After any code changes, re-run:
- [ ] T1 (Landing page load)
- [ ] T2 (Intake form validation)
- [ ] T3 (Campaign creation)
- [ ] T6 (Email sending)

---

## Test Report Template

**Test Date:** YYYY-MM-DD
**Tester:** [Name]
**Environment:** Production / Local

| Test ID | Status | Notes |
|---------|--------|-------|
| T1 | ✅ PASS | All sections loaded |
| T2 | ✅ PASS | Validation works |
| T3 | ⚠️ WARN | Claude API slow (6s) |
| T4 | ✅ PASS | All tabs functional |
| T5 | ❌ FAIL | Chinese text overflow on mobile |
| ... | ... | ... |

**Summary:**
- Tests Passed: X/10
- Tests Failed: X/10
- Blockers: [List P0 failures]
- Next Steps: [Actions needed]

---

## Post-Launch Monitoring

After deployment, monitor:
- [ ] Cloudflare Analytics (page views, errors)
- [ ] API success rate (via logs)
- [ ] Email delivery rate (Gmail SMTP logs)
- [ ] User complaints (support inbox)
- [ ] Performance metrics (Lighthouse CI)

**Alerts to Set Up:**
- Error rate > 5%
- API response time > 10s
- Database queries failing

---

## Contact

**Issues during testing?** Report to:
- fullstack-dhh (code bugs)
- devops-hightower (deployment issues)
- qa-bach (test plan updates)

**Escalation:** CEO (Bezos) for critical blocking issues

---

**Test Plan Status:** ✓ Complete
**Ready for QA:** Yes
**Estimated Test Time:** 4-6 hours (full suite)
