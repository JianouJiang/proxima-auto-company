# SixDegrees V2 — Engineering Handoff

**To:** devops-hightower, qa-bach
**From:** fullstack-dhh
**Date:** 2026-02-22
**Status:** Ready for deployment and testing

---

## What Was Built

Complete web application for SixDegrees with:
- ✅ Landing page (bilingual EN/中文)
- ✅ Intake form (6 fields, validation, API integration)
- ✅ Dashboard (4 tabs, auto-refresh, email carousel)
- ✅ Backend API (intake, campaign fetch, email send)
- ✅ D1 database schema
- ✅ Gmail SMTP integration (local scripts)

**Total Build Time:** ~6 hours
**Lines of Code:** ~2,500 lines (HTML + JS + API)

---

## File Locations

### Frontend (HTML)
```
/projects/sixdegrees/public/index.html     Landing page
/projects/sixdegrees/intake.html            Intake form
/projects/sixdegrees/dashboard.html         Dashboard
```

### Backend (Cloudflare Pages Functions)
```
/projects/sixdegrees/functions/api/intake.js         POST /api/intake
/projects/sixdegrees/functions/api/campaign/[id].js  GET /api/campaign/:id
/projects/sixdegrees/functions/api/send.js           POST /api/send
```

### Database
```
/projects/sixdegrees/schema.sql             D1 schema (5 tables, 6 indexes)
```

### Email Scripts (Local)
```
/projects/sixdegrees/send-gmail.js          Gmail SMTP sender
/projects/sixdegrees/auto-outreach.js       Auto-outreach engine
/projects/gmail-engine/send.js              Gmail nodemailer module
```

---

## Deployment Checklist (devops-hightower)

### 1. Environment Setup

**Cloudflare Secrets (required):**
```bash
wrangler secret put ANTHROPIC_API_KEY
wrangler secret put GMAIL_ADDRESS
wrangler secret put GMAIL_APP_PASSWORD
```

**Local Development (`.dev.vars`):**
```
ANTHROPIC_API_KEY=sk-ant-...
GMAIL_ADDRESS=jianou.works@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password
```

**Get Gmail App Password:**
1. Go to Google Account → Security
2. Enable 2-Step Verification
3. Search "App passwords" → Generate → Select "Mail" and "Other"
4. Copy 16-character password

---

### 2. Database Migration

**Create D1 database:**
```bash
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/sixdegrees

# Create database
wrangler d1 create sixdegrees-db

# Note the database ID, add to wrangler.toml:
# [[d1_databases]]
# binding = "DB"
# database_name = "sixdegrees-db"
# database_id = "your-database-id"

# Run migrations
wrangler d1 execute sixdegrees-db --file=schema.sql
```

**Verify tables:**
```bash
wrangler d1 execute sixdegrees-db --command="SELECT name FROM sqlite_master WHERE type='table';"
```

Expected output: `users`, `campaigns`, `email_outreach`, `campaign_steps`, `credit_transactions`

---

### 3. Deploy to Cloudflare Pages

**Option A: Automatic (recommended)**
```bash
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/sixdegrees

# Deploy
wrangler pages deploy . --project-name sixdegrees

# Note the URL: https://sixdegrees.pages.dev
```

**Option B: Git Integration**
1. Push to GitHub: `proxima-auto-company/projects/sixdegrees`
2. Connect to Cloudflare Pages dashboard
3. Build settings: `public/` as build directory
4. Functions: Auto-detected from `functions/` directory

---

### 4. Configure DNS (Optional)

If using custom domain:
```bash
wrangler pages domain add sixdegrees.pages.dev sixdegrees.com
```

Add CNAME record:
```
sixdegrees.com → sixdegrees.pages.dev
```

---

### 5. Test Deployment

**Health check:**
```bash
# Landing page
curl https://sixdegrees.pages.dev/

# API test
curl -X POST https://sixdegrees.pages.dev/api/intake \
  -H "Content-Type: application/json" \
  -d '{
    "user_email": "test@example.com",
    "user_name": "Test User",
    "target_name": "Elon Musk",
    "target_company": "CEO, Tesla",
    "target_reason": "Test campaign",
    "user_background": "Testing the system"
  }'

# Expected response: { "success": true, "campaign_id": "camp_..." }
```

---

### 6. Gmail SMTP Setup (Local)

**Install dependencies:**
```bash
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/sixdegrees
npm install
```

**Test Gmail sending:**
```bash
# Single email
node send-gmail.js --to "your-email@example.com" --subject "Test" --body "Hello from SixDegrees"

# Expected output: "Email sent successfully! Message ID: ..."
```

**Auto-outreach engine:**
```bash
# Send degree 1 emails (from outreach-chain.json)
node auto-outreach.js --degree 1

# Check replies
node auto-outreach.js --check-replies
```

---

### 7. Monitoring Setup

**Cloudflare Analytics:**
- Enable Web Analytics in Cloudflare Dashboard
- Add custom event tracking (optional)

**Error Tracking:**
Add to `wrangler.toml`:
```toml
[observability]
enabled = true
head_sampling_rate = 1
```

**Recommended:** Set up Sentry for error monitoring (future)

---

## Testing Plan (qa-bach)

### Critical User Flows

#### Flow 1: New Campaign Creation
1. **Start:** Open `https://sixdegrees.pages.dev/`
2. Click "Start Your First Connection"
3. Fill intake form:
   - Name: "Sarah Chen"
   - Email: "sarah@company.com"
   - Background: "Founder of energy tech startup"
   - Target: "Elon Musk"
   - Company: "CEO, Tesla"
   - Reason: "Want to discuss energy storage for EVs"
4. Click "Let AI Research & Plan"
5. **Expected:** Loading state → Redirect to dashboard

**Verification:**
- Campaign ID in URL: `?campaign=camp_...`
- Strategy text displayed
- 6-degree chain rendered
- Status badge shows "Ready to Launch"

---

#### Flow 2: Dashboard Navigation
1. **Start:** Dashboard from Flow 1
2. Click each tab:
   - Your Campaign (default)
   - Connections (should show "No emails sent yet")
   - Credits & Payment (shows Free plan)
   - Settings (shows email, name)
3. Click "Refresh" button
4. **Expected:** Data reloads without error

**Verification:**
- All tabs switch correctly
- No console errors
- Auto-refresh triggers every 30s

---

#### Flow 3: Language Toggle
1. **Start:** Landing page
2. Click "中文" button (top-right)
3. **Expected:** All text switches to Chinese
4. Click "EN" button
5. **Expected:** All text switches back to English
6. Reload page
7. **Expected:** Language persists

**Verification:**
- Every text element changes
- Placeholders update
- Language saved to localStorage

---

#### Flow 4: Email Preview
1. **Start:** Dashboard with campaign
2. Click "Start Campaign" button
3. **Expected:** Email preview modal opens
4. Modal shows: To, Subject, Body
5. Click "Send As-Is"
6. **Expected:** Email queued, instructions shown

**Verification:**
- Modal content correct
- Email added to DB with status "queued"
- Dashboard updates after send

---

#### Flow 5: Email Sending (Local Script)
1. **Prerequisite:** Campaign with queued email
2. Run: `node send-gmail.js --campaign-id camp_...`
3. **Expected:** Email sends via Gmail SMTP
4. Check email inbox
5. Refresh dashboard
6. **Expected:** Email status changes to "sent"

**Verification:**
- Email received in inbox
- Subject matches dashboard preview
- Status updated in DB and dashboard

---

### Edge Cases to Test

#### Edge Case 1: Invalid Email Format
1. Intake form → Enter "not-an-email" in email field
2. Submit form
3. **Expected:** Browser validation error, form blocked

---

#### Edge Case 2: Empty Form Submission
1. Intake form → Leave all fields empty
2. Click submit button
3. **Expected:** Submit button disabled (greyed out)

---

#### Edge Case 3: Network Error
1. Disconnect internet
2. Submit intake form
3. **Expected:** Error state shown: "Network error. Please try again."
4. "Try Again" button visible

---

#### Edge Case 4: Campaign Not Found
1. Dashboard → Manually change URL to `?campaign=invalid_id`
2. **Expected:** Alert "Campaign not found" → Redirect to intake

---

#### Edge Case 5: Long Text Overflow
1. Intake form → Enter 500 characters in "Why reach them?" field
2. **Expected:** Character counter shows "500/500"
3. Try to type more
4. **Expected:** Input blocked at 500 chars

---

### Performance Tests

#### Test 1: Landing Page Load
- **Metric:** First Contentful Paint < 1s
- **Tool:** Chrome DevTools Lighthouse
- **Target:** Score > 90

#### Test 2: Intake Form Submit
- **Metric:** Submit → Redirect < 5s (includes Claude API)
- **Tool:** Chrome DevTools Network tab
- **Target:** Total time < 5000ms

#### Test 3: Dashboard Auto-Refresh
- **Metric:** Refresh cycle < 500ms
- **Tool:** Console.log timing
- **Target:** 30s interval consistent

---

### Bilingual Testing

**Test all screens in both languages:**
- Landing page (EN/中文)
- Intake form (EN/中文)
- Dashboard all 4 tabs (EN/中文)
- Email preview modal (EN/中文)

**Verify:**
- No text overflow (Chinese characters are wider)
- Font renders correctly (CJK font fallback works)
- All placeholders translate

---

### Mobile Testing

**Devices to test:**
- iPhone SE (375px width)
- iPhone 12 (390px width)
- iPad (768px width)

**Key checks:**
- 6-degree chain stacks vertically on mobile
- Email carousel is swipeable
- All buttons have 44x44px touch targets
- No horizontal scroll

---

### Browser Testing

**Required browsers:**
- Chrome (latest)
- Safari (latest)
- Firefox (latest)
- Edge (latest)

**Known issues:**
- Safari may have LocalStorage restrictions in Private mode (language won't persist)

---

## API Integration Testing

### Test 1: POST /api/intake

**Request:**
```bash
curl -X POST https://sixdegrees.pages.dev/api/intake \
  -H "Content-Type: application/json" \
  -d '{
    "user_email": "test@example.com",
    "user_name": "Test User",
    "target_name": "Elon Musk",
    "target_company": "CEO, Tesla",
    "target_reason": "Testing campaign creation",
    "user_background": "QA tester"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "campaign_id": "camp_1708595400_abc123",
  "message": "Campaign created successfully"
}
```

**Verify:**
- Campaign exists in D1 database
- `results` field contains strategy JSON
- User created if new email

---

### Test 2: GET /api/campaign/:id

**Request:**
```bash
curl https://sixdegrees.pages.dev/api/campaign/camp_1708595400_abc123
```

**Expected Response:**
```json
{
  "campaign_id": "camp_1708595400_abc123",
  "target_name": "Elon Musk",
  "target_company": "CEO, Tesla",
  "status": "ready",
  "strategy": "...",
  "selected_path": { ... },
  "emails": [],
  "created_at": 1708595400
}
```

**Verify:**
- Returns 404 for invalid campaign ID
- All fields present and correct type

---

### Test 3: POST /api/send

**Request:**
```bash
curl -X POST https://sixdegrees.pages.dev/api/send \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": "camp_1708595400_abc123",
    "to": "recipient@example.com",
    "subject": "Test Email",
    "body": "This is a test email.",
    "recipient_name": "Test Recipient"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "email_id": "email_1708595400_xyz",
  "status": "queued",
  "message": "Email queued successfully. Run local Gmail SMTP script to send.",
  "instructions": "Use: node send-gmail.js --campaign-id camp_1708595400_abc123"
}
```

**Verify:**
- Email record created with status "queued"
- Campaign status unchanged

---

## Known Issues & Limitations

### Issue 1: Email Sending Not Automated
**Impact:** User must run local script to send emails
**Workaround:** Run `node send-gmail.js --campaign-id [ID]`
**V2 Plan:** Implement web-based email sending via Cloudflare Durable Objects

### Issue 2: No Gmail OAuth
**Impact:** Uses App Password (less secure than OAuth)
**Workaround:** Gmail App Password works fine for V1
**V2 Plan:** Implement OAuth 2.0 flow for Gmail access

### Issue 3: Dashboard Only Shows Single Campaign
**Impact:** User with multiple campaigns sees only one
**Workaround:** URL parameter determines which campaign to show
**V2 Plan:** Add campaign selector dropdown

### Issue 4: No Stripe Webhook
**Impact:** Credits not auto-updated after payment
**Workaround:** Manual credit adjustment in DB
**V2 Plan:** Implement Stripe webhook handler

### Issue 5: No Reply Detection
**Impact:** User must manually check replies
**Workaround:** Run `node auto-outreach.js --check-replies`
**V2 Plan:** Implement Gmail API for auto-reply detection

---

## Rollback Plan

If deployment fails:

1. **Frontend:** Revert to previous version via Cloudflare Pages dashboard
2. **Database:** Restore from D1 backup (if available)
3. **Secrets:** Verify environment variables are set correctly

**Critical Data:** Campaign records in D1 database. Ensure backups before major changes.

---

## Post-Deployment Actions

### Immediate (Day 1)
- [ ] Verify all 3 pages load correctly
- [ ] Test intake form → dashboard flow
- [ ] Send 1 test email via Gmail SMTP
- [ ] Check language toggle works
- [ ] Monitor Cloudflare Analytics

### Within 1 Week
- [ ] Run full QA test plan
- [ ] Fix any bugs discovered
- [ ] Add Stripe Payment Links
- [ ] Test complete user flow (landing → payment)
- [ ] Set up error monitoring (Sentry)

### Within 1 Month
- [ ] Implement Stripe webhook
- [ ] Add campaign selector for multi-campaign users
- [ ] Optimize Claude API prompt for better strategies
- [ ] Add email editing modal
- [ ] Launch on Product Hunt

---

## Support & Troubleshooting

### Common Issues

**"Campaign not found" error:**
- Check campaign ID in URL
- Verify campaign exists in D1: `wrangler d1 execute sixdegrees-db --command="SELECT * FROM campaigns WHERE id='camp_...'"`

**"Email send failed" error:**
- Check Gmail App Password is correct
- Verify Gmail SMTP is not blocked (some networks block port 587)
- Check error message in `email_outreach.error_message` field

**Dashboard not loading:**
- Check browser console for errors
- Verify API endpoint returns data: `curl https://sixdegrees.pages.dev/api/campaign/[ID]`
- Clear browser cache and LocalStorage

**Language toggle not working:**
- Check LocalStorage is enabled (disabled in Private mode)
- Verify all text elements have `data-en` and `data-zh` attributes

---

## Contact

**Questions?** Reach out to:
- fullstack-dhh (technical implementation)
- devops-hightower (deployment issues)
- qa-bach (testing failures)

**Escalation:** CEO (Bezos) for strategic decisions

---

**Handoff Status:** ✓ Complete
**Next Steps:** Deploy to production + Full QA testing
**Estimated Deployment Time:** 2-3 hours (including testing)
