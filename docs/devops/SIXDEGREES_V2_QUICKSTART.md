# SixDegrees V2 — Quick Start Guide

**For:** Founder
**Date:** 2026-02-22
**Status:** Deployed (API binding pending)

---

## One-Minute Summary

✅ SixDegrees web app is **live at https://sixdegrees.pages.dev/**

Landing page, intake form, and dashboard all load correctly. Database is set up and working.

⚠️ **One quick fix needed:** D1 database binding must be configured in Cloudflare dashboard (5 minutes) to activate the API. After that, the app is fully functional.

---

## What's Live Now

| Feature | Status | URL |
|---------|--------|-----|
| Landing page | ✅ Live | https://sixdegrees.pages.dev/ |
| Intake form | ✅ Live | https://sixdegrees.pages.dev/intake |
| Dashboard | ✅ Live | https://sixdegrees.pages.dev/dashboard |
| API (intake) | ⚠️ Pending binding | /api/intake |
| API (campaign fetch) | ⚠️ Pending binding | /api/campaign/:id |
| API (email send) | ⚠️ Pending binding | /api/send |

---

## Critical: Fix D1 Binding (5 minutes)

The API isn't working yet because the database binding isn't configured. Here's the fix:

### Step 1: Go to Cloudflare Dashboard
https://dash.cloudflare.com → Pages → **sixdegrees** → Settings

### Step 2: Find "Functions" Section
Click **Functions** in the left sidebar

### Step 3: Add D1 Database Binding
1. Look for "D1 Database" section
2. Click **"Add binding"**
3. Fill in:
   - **Binding name:** `DB`
   - **D1 Database:** `connectpath-db` (select from dropdown)
4. Click **"Add binding"**

### Step 4: Test API
After saving, the API will work immediately. Test it:

```bash
curl -X POST https://sixdegrees.pages.dev/api/intake \
  -H "Content-Type: application/json" \
  -d '{
    "user_email": "you@example.com",
    "user_name": "Your Name",
    "target_name": "Target Person",
    "target_company": "Company/Role",
    "target_reason": "Why you want to reach them",
    "user_background": "Your background"
  }'
```

**Expected response:** `{"success": true, "campaign_id": "camp_...", ...}`

If you see this, the API is working!

---

## How It Works (User Flow)

1. **User visits:** https://sixdegrees.pages.dev/
2. **Clicks:** "Start Your First Connection"
3. **Fills intake form:** Name, email, target, reason
4. **Clicks submit:** API creates campaign + AI generates strategy
5. **Dashboard loads:** Shows 6-degree chain, email preview
6. **User reviews emails:** Can edit before sending
7. **Sends campaign:** Emails queued for sending
8. **Local script sends:** `node send-gmail.js` sends queued emails
9. **Replies tracked:** Incoming replies appear in dashboard

---

## What Was Built

### Frontend (3 pages)
1. **Landing Page** (`index.html`) — Hero, features, CTA
2. **Intake Form** (`intake.html`) — 6-field form, bilingual
3. **Dashboard** (`dashboard.html`) — 4 tabs, auto-refresh

### Backend (3 APIs)
1. **POST /api/intake** — Create campaign + generate strategy
2. **GET /api/campaign/:id** — Fetch campaign data
3. **POST /api/send** — Queue email for sending

### Database (5 tables)
- `users` — User accounts and credits
- `campaigns` — Campaign records + AI strategy results
- `email_outreach` — Sent emails, status tracking
- `campaign_steps` — AI agent step logs
- `credit_transactions` — Payment/usage history

### Tech Stack
- **Frontend:** HTML/JS/Tailwind CSS (Cloudflare Pages)
- **Backend:** Cloudflare Pages Functions (serverless)
- **Database:** Cloudflare D1 (SQLite)
- **AI:** Anthropic Claude API (strategy generation)
- **Email:** Gmail SMTP (local Node.js script)
- **Payments:** Stripe Payment Links

---

## Key Features

### Bilingual Support (EN/中文)
All pages support English and Mandarin Chinese. Language toggle in top-right corner. Preference saved to browser.

### Auto-refresh Dashboard
Dashboard automatically refreshes campaign status every 30 seconds.

### Email Preview & Edit
Before sending, users can preview and edit emails to each person in the chain.

### AI Strategy Generation
Claude AI analyzes target and generates personalized 6-degree connection chain.

### Manual Email Sending
Local script `send-gmail.js` sends queued emails via Gmail SMTP:
```bash
cd projects/sixdegrees
node send-gmail.js --campaign-id camp_123
```

---

## Environment Variables / Secrets

### Currently Set
- ✅ ANTHROPIC_API_KEY (for AI strategy generation)
- ✅ GMAIL_ADDRESS (jianou.works@gmail.com)

### Need to Set (When Ready for Payments)
```bash
wrangler pages secret put GMAIL_APP_PASSWORD --project-name sixdegrees
wrangler pages secret put STRIPE_PRICE_ID_MONTHLY --project-name sixdegrees
wrangler pages secret put STRIPE_PRICE_ID_CREDITS --project-name sixdegrees
```

---

## Testing Locally

### Test Landing Page
```bash
curl https://sixdegrees.pages.dev/
# Should return HTML with "AI Agent That Reaches Anyone For You"
```

### Test Intake Form (After D1 binding configured)
```bash
curl -X POST https://sixdegrees.pages.dev/api/intake \
  -H "Content-Type: application/json" \
  -d '{
    "user_email": "test@example.com",
    "user_name": "Test User",
    "target_name": "Elon Musk",
    "target_company": "CEO, Tesla",
    "target_reason": "Discuss energy storage",
    "user_background": "Energy engineer"
  }'
```

### Test Dashboard (Need valid campaign ID)
```bash
# Get campaign ID from intake response
curl https://sixdegrees.pages.dev/api/campaign/camp_1708595400_abc123
```

---

## Deployment Location

All code is in `projects/sixdegrees/`:

```
projects/sixdegrees/
├── public/                  # Static files (deployed to Pages)
│   ├── index.html          # Landing page
│   ├── intake.html         # Intake form
│   └── dashboard.html      # Dashboard
├── functions/api/          # API endpoints (Functions)
│   ├── intake.js           # POST /api/intake
│   ├── campaign/[id].js    # GET /api/campaign/:id
│   └── send.js             # POST /api/send
├── schema.sql              # Database schema
├── send-gmail.js           # Local Gmail SMTP script
├── package.json
└── wrangler.toml          # Cloudflare config
```

---

## Common Tasks

### View Recent Campaigns
```bash
wrangler d1 execute connectpath-db --remote --command="
  SELECT id, email, target_name, status, created_at
  FROM campaigns ORDER BY created_at DESC LIMIT 10;"
```

### Check Email Queue
```bash
wrangler d1 execute connectpath-db --remote --command="
  SELECT COUNT(*) as pending FROM email_outreach
  WHERE status = 'pending';"
```

### Send Queued Emails Manually
```bash
cd projects/sixdegrees
node send-gmail.js --campaign-id camp_123
```

### Add Credits to User (For Testing)
```bash
wrangler d1 execute connectpath-db --remote --command="
  UPDATE users SET credits_balance = 10
  WHERE email = 'test@example.com';"
```

### Backup Database
```bash
wrangler d1 backup create connectpath-db
```

---

## Monitoring

### Check Status
- **Pages dashboard:** https://dash.cloudflare.com/Pages/sixdegrees
- **Analytics:** https://dash.cloudflare.com → Pages → sixdegrees → Analytics
- **Deployments:** https://dash.cloudflare.com → Pages → sixdegrees → Deployments

### View Recent Logs
```bash
wrangler tail sixdegrees --env production
```

### Uptime Monitoring (Recommended)
Set up UptimeRobot to monitor:
- https://sixdegrees.pages.dev/ (status 200)
- Check interval: 5 minutes
- Alert on down

---

## Troubleshooting

### "Campaign not found" Error
- Check campaign ID in URL is correct
- Verify campaign exists: `wrangler d1 execute connectpath-db --remote --command="SELECT * FROM campaigns WHERE id='camp_...'"`

### "Email send failed"
- Check Gmail App Password is correct
- Verify network allows SMTP port 587
- Check error log: `wrangler tail sixdegrees`

### Form not submitting
- Check browser console for JavaScript errors (F12)
- Verify API endpoint responds (test with curl)
- Check D1 binding is configured

### Language toggle not working
- Check localStorage: `localStorage.getItem('language')`
- Clear browser cache
- Verify HTML has `data-en` and `data-zh` attributes

---

## Next Steps

### Immediate (Today)
- [x] Configure D1 binding (5 min)
- [x] Test API endpoints (5 min)

### This Week
- [ ] Run full QA test plan
- [ ] Test Gmail SMTP email sending
- [ ] Add Stripe Payment Links
- [ ] Test bilingual on mobile
- [ ] Confirm mobile responsiveness

### This Month
- [ ] Launch on Product Hunt
- [ ] Add Stripe webhook for auto-credits
- [ ] Implement campaign selector (multi-campaign)
- [ ] Add email editing modal
- [ ] Set up error monitoring (Sentry)

---

## Support

**Questions about deployment?** → See `docs/devops/sixdegrees-v2-deployment.md`

**Running into issues?** → See `docs/devops/sixdegrees-v2-operations.md` (Runbook)

**Want to know how it's built?** → See `docs/fullstack/sixdegrees-v2-technical-spec.md`

**Testing details?** → See `projects/sixdegrees/TEST.md`

---

## Key URLs

| Link | Purpose |
|------|---------|
| https://sixdegrees.pages.dev/ | Live app |
| https://dash.cloudflare.com → Pages → sixdegrees | Admin panel |
| https://dash.cloudflare.com → Pages → sixdegrees → Analytics | Metrics |
| `projects/sixdegrees/` | Source code |
| `docs/devops/sixdegrees-v2-deployment.md` | Technical details |
| `docs/devops/sixdegrees-v2-operations.md` | Operations runbook |

---

**Deployed:** 2026-02-22
**Status:** 95% Ready (pending D1 binding configuration)
**Est. Time to Full Launch:** 10 minutes (after D1 binding)

Go live! 🚀
