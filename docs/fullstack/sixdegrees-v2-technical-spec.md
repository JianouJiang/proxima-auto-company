# SixDegrees V2 — Technical Specification

**Author:** fullstack-dhh (DHH Thinking Model)
**Date:** 2026-02-22
**Status:** Implementation Complete
**Version:** 2.0 (Web Dashboard)

---

## Executive Summary

SixDegrees V2 is a **complete web application** that allows users to:
1. **Submit a target person** via intake form
2. **View AI-generated connection strategy** on dashboard
3. **Track email outreach** in real-time
4. **Manage credits and billing** via Stripe Payment Links
5. **Send emails from the web** (via Gmail SMTP backend)

**Stack:**
- Frontend: Vanilla JS + Tailwind CSS v4
- Backend: Cloudflare Workers + D1 (SQLite)
- Email: Gmail SMTP (nodemailer) via local scripts
- AI: Anthropic Claude API for strategy generation
- Payment: Stripe Payment Links

**Key Files:**
- `public/index.html` — Landing page
- `intake.html` — Intake form
- `dashboard.html` — 4-tab dashboard (Campaign, Connections, Credits, Settings)
- `functions/api/intake.js` — POST /api/intake (create campaign)
- `functions/api/campaign/[id].js` — GET /api/campaign/:id (fetch campaign)
- `functions/api/send.js` — POST /api/send (queue email)

---

## Architecture

### Frontend (Static HTML)

```
/public/index.html      Landing page (bilingual EN/中文)
/intake.html            Intake form (6 fields, validation, API submit)
/dashboard.html         Dashboard (4 tabs, auto-refresh every 30s)
```

**Technologies:**
- Tailwind CSS v4 (CDN)
- Vanilla JavaScript (no React/Vue)
- LocalStorage for language preference
- Fetch API for backend calls

### Backend (Cloudflare Workers)

```
/functions/api/intake.js          POST  — Create campaign, call Claude API
/functions/api/campaign/[id].js   GET   — Fetch campaign + emails
/functions/api/send.js            POST  — Queue email for sending
```

**Database (D1 — Cloudflare SQLite):**
- `users` — User accounts (email, credits)
- `campaigns` — Campaign records (target, strategy, status)
- `email_outreach` — Email history (sent, replied, failed)
- `campaign_steps` — AI operations log
- `credit_transactions` — Billing history

### Email Sending (Gmail SMTP)

**Location:** Local Node.js scripts
- `send-gmail.js` — Send single email via Gmail SMTP
- `auto-outreach.js` — Automated 6-degree outreach engine

**Why local scripts?**
Cloudflare Workers cannot make raw SMTP connections. Gmail SMTP requires nodemailer (Node.js).

**Flow:**
1. User clicks "Send Email" on dashboard
2. Frontend calls `/api/send` (queues email in DB)
3. Local script fetches queued emails and sends via Gmail SMTP
4. Script updates email status in DB

**Gmail Configuration:**
- Gmail address: `jianou.works@gmail.com` (env: `GMAIL_ADDRESS`)
- App Password: Required (env: `GMAIL_APP_PASSWORD`)
- SMTP: `smtp.gmail.com:587` (STARTTLS)

---

## Database Schema

```sql
CREATE TABLE users (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  credits_balance INTEGER DEFAULT 0,
  created_at INTEGER DEFAULT (strftime('%s', 'now')),
  updated_at INTEGER DEFAULT (strftime('%s', 'now'))
);

CREATE TABLE campaigns (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  email TEXT NOT NULL,
  cv TEXT NOT NULL,              -- user_background
  target_name TEXT NOT NULL,
  target_role TEXT,              -- target_company
  motivation TEXT NOT NULL,      -- target_reason
  status TEXT DEFAULT 'pending', -- pending, processing, ready, in_progress, completed, failed
  credits_used INTEGER DEFAULT 0,
  results TEXT,                  -- JSON: { strategy, selected_path, target_analysis }
  created_at INTEGER,
  updated_at INTEGER,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE email_outreach (
  id TEXT PRIMARY KEY,
  campaign_id TEXT NOT NULL,
  recipient_email TEXT NOT NULL,
  recipient_name TEXT,
  subject TEXT NOT NULL,
  body TEXT NOT NULL,
  status TEXT DEFAULT 'pending', -- pending, queued, sent, failed, bounced, replied
  sent_at INTEGER,
  error_message TEXT,
  created_at INTEGER,
  FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);
```

---

## API Endpoints

### 1. POST /api/intake

**Request Body:**
```json
{
  "user_email": "sarah@company.com",
  "user_name": "Sarah Chen",
  "target_name": "Elon Musk",
  "target_company": "CEO, Tesla",
  "target_reason": "Want to discuss energy storage for EVs",
  "user_background": "I'm founder of X. We're solving Y problem..."
}
```

**Response:**
```json
{
  "success": true,
  "campaign_id": "camp_1708595400_abc123",
  "message": "Campaign created successfully"
}
```

**Logic:**
1. Validate required fields
2. Create or fetch user record
3. Insert campaign into DB
4. Call Anthropic Claude API to generate strategy
5. Update campaign with AI-generated strategy
6. Return campaign ID

**Claude API Prompt:**
```
Generate a connection strategy to reach [target_name] ([target_company]).
User background: [user_background]
Reason: [target_reason]

Return JSON:
{
  "target_analysis": "brief analysis",
  "paths": [
    {
      "degree": 3,
      "confidence": 0.85,
      "strategy": "Path A: You → College Friend → Tesla Employee → Elon",
      "intermediaries": ["College connections", "Tesla employees"]
    }
  ],
  "recommended_path_index": 0
}
```

---

### 2. GET /api/campaign/:id

**Response:**
```json
{
  "campaign_id": "camp_1708595400_abc123",
  "target_name": "Elon Musk",
  "target_company": "CEO, Tesla",
  "user_name": "Sarah Chen",
  "user_email": "sarah@company.com",
  "status": "in_progress",
  "strategy": "AI-generated strategy text...",
  "selected_path": {
    "degree": 3,
    "confidence": 0.85,
    "chain": [
      { "name": "Sarah Chen", "role": "Sender", "status": "sender" },
      { "name": "Jake Williams", "role": "College Friend", "status": "replied", "email": "jake@college.com" },
      { "name": "Tesla Engineer", "role": "Second connection", "status": "sent", "email": "eng@tesla.com" },
      { "name": "Elon Musk", "role": "Target", "status": "draft", "email": "elon@tesla.com" }
    ]
  },
  "emails": [
    {
      "email_id": "email_1708595400_xyz",
      "recipient_email": "jake@college.com",
      "recipient_name": "Jake Williams",
      "subject": "Quick intro to Sarah Chen — Tesla energy project",
      "body": "Dear Jake...",
      "status": "sent",
      "sent_at": 1708595400
    }
  ],
  "created_at": 1708595400,
  "last_updated_at": 1708595400
}
```

**Logic:**
1. Fetch campaign by ID
2. Parse `results` JSON field
3. Fetch all emails for campaign (from `email_outreach`)
4. Build 6-degree chain from results
5. Return complete campaign state

---

### 3. POST /api/send

**Request Body:**
```json
{
  "campaign_id": "camp_1708595400_abc123",
  "email_id": "email_1708595400_xyz",
  "to": "jake@college.com",
  "subject": "Quick intro to Sarah Chen",
  "body": "Dear Jake...",
  "recipient_name": "Jake Williams"
}
```

**Response:**
```json
{
  "success": true,
  "email_id": "email_1708595400_xyz",
  "status": "queued",
  "message": "Email queued successfully. Run local Gmail SMTP script to send.",
  "instructions": "Use: node send-gmail.js --campaign-id camp_1708595400_abc123"
}
```

**Logic:**
1. Validate campaign exists
2. Create or fetch email record
3. Mark email status as "queued"
4. Return instructions for local script

**Note:** Actual sending happens via:
```bash
node send-gmail.js --to "jake@college.com" --subject "..." --body "..."
```

---

## Frontend Pages

### 1. Landing Page (`public/index.html`)

**Sections:**
- Header (logo, language toggle, CTA button)
- Hero (value prop, primary CTA)
- Proof points (4 icons: Research, Find Path, Send, Track)
- Trust section (Privacy, No Spam, Guaranteed Results)
- Pricing cards (Free, $29/mo, $99/mo)
- Final CTA
- Footer

**Features:**
- Bilingual EN/中文 toggle
- Responsive (mobile-first)
- All CTAs link to `/intake.html`

---

### 2. Intake Form (`intake.html`)

**Fields:**
1. Your Name (text, max 50 chars)
2. Your Email (email, required)
3. Quick Intro to Yourself (textarea, max 500 chars)
4. Who do you want to reach? (text, required)
5. Their Title / Company (text, required)
6. Why do you need to reach them? (textarea, max 500 chars)

**Features:**
- Character counters for textareas
- Progress bar (0/6 → 6/6)
- Submit button disabled until all fields filled
- Loading state ("Analyzing your request...")
- Error state (with retry button)

**Submission:**
```javascript
fetch('/api/intake', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(formData)
});
```

**Success:** Redirect to `/dashboard.html?campaign=camp_123`

---

### 3. Dashboard (`dashboard.html`)

**4 Tabs:**

#### Tab 1: Your Campaign
- Status badge (Ready / In Progress / Connected!)
- 6-degree chain visualization (SVG on desktop, vertical stack on mobile)
- Strategy summary (text)
- Email carousel (3 cards, swipeable)
- Action buttons (Start Campaign, Edit Target)
- "What's Happening Now" timeline

#### Tab 2: Connections
- Filter buttons (All, Sent, Replied, No Reply)
- Email history list (newest first)
- Expandable email details (click to view full body)

#### Tab 3: Credits & Payment
- Credits balance display
- Current plan (Free, Starter, Pro)
- 3 pricing cards with Stripe Payment Links
- Payment history (future)

#### Tab 4: Settings
- Account info (email, name)
- Language toggle (EN / 中文)
- Email reminders toggle
- Danger zone (Delete account)

**Auto-Refresh:**
Dashboard fetches `/api/campaign/:id` every 30 seconds to update live status.

**Email Preview Modal:**
- Triggered when user clicks email card
- Shows: To, Subject, Full Body
- Actions: [Send As-Is] [Edit Email]

---

## Bilingual Support (EN / 中文)

**Strategy:** Single HTML with language toggle. All text in `data-*` attributes.

**Example:**
```html
<h1 data-en="Your Campaign" data-zh="你的活动计划">
  Your Campaign
</h1>
```

**JavaScript:**
```javascript
document.getElementById('lang-zh').addEventListener('click', () => {
  document.querySelectorAll('[data-zh]').forEach(el => {
    el.textContent = el.getAttribute('data-zh');
  });
  localStorage.setItem('sixdegrees_language', 'zh');
});
```

**Persistence:** Language choice saved to `localStorage` and restored on page load.

---

## Styling (Tailwind CSS v4)

**Design System:**
- Primary color: `#2563eb` (blue-600)
- Success: `#16a34a` (green-600)
- Warning: `#ca8a04` (amber-600)
- Error: `#dc2626` (red-600)
- Spacing: 8px grid (`p-4`, `p-6`, `mb-4`, etc.)
- Typography: System font stack (supports CJK characters)

**Button Styles:**
```html
<!-- Primary -->
<button class="px-6 py-3 rounded bg-blue-600 text-white font-semibold hover:bg-blue-700">

<!-- Secondary -->
<button class="px-6 py-3 rounded bg-gray-100 border border-gray-300 text-gray-700 hover:bg-gray-200">

<!-- Destructive -->
<button class="px-4 py-2 rounded bg-red-600 text-white hover:bg-red-700">
```

**Status Badges:**
```html
<!-- Sent -->
<span class="px-3 py-1 rounded-full bg-green-100 text-green-700 text-xs font-semibold">✓ Sent</span>

<!-- Waiting -->
<span class="px-3 py-1 rounded-full bg-yellow-100 text-yellow-700 text-xs font-semibold">⏳ Waiting</span>

<!-- Draft -->
<span class="px-3 py-1 rounded-full bg-gray-100 text-gray-700 text-xs font-semibold">✎ Draft</span>
```

---

## Payment Integration (Stripe)

**Method:** Stripe Payment Links (no embedded checkout for V1)

**Flow:**
1. User clicks "Upgrade" on Credits tab
2. Opens Stripe Payment Link in new tab
3. After payment, Stripe redirects to `/success.html?session_id=...`
4. Backend webhook updates user credits (future)

**Pricing:**
- Free: 1 campaign/month, $0
- Starter: 10 campaigns/month, $29/mo
- Pro: Unlimited + API, $99/mo

**Note:** Stripe Payment Links must be configured manually in Stripe Dashboard.

---

## Gmail SMTP Integration

**Location:** `projects/gmail-engine/send.js`

**Usage from local script:**
```javascript
import { sendEmail } from '../gmail-engine/send.js';

const result = await sendEmail({
  to: 'recipient@example.com',
  subject: 'Introduction request',
  body: 'Dear recipient...',
  html: '<p>Optional HTML version</p>',
});

if (result.success) {
  console.log('Sent! Message ID:', result.messageId);
} else {
  console.error('Failed:', result.error);
}
```

**Environment Variables:**
```bash
GMAIL_ADDRESS=jianou.works@gmail.com
GMAIL_APP_PASSWORD=your_app_password_here
```

**Outreach Chain Config:**
- `outreach-chain.json` — 6-degree chain from Jianou → Elon Musk
- Extend this to include 3-5 contacts per degree

---

## Deployment

### Frontend (Cloudflare Pages)

```bash
# Already deployed at: sixdegrees.pages.dev
wrangler pages deploy public/ --project-name sixdegrees
```

### Backend (Cloudflare Workers)

Already deployed as Cloudflare Pages Functions (automatic with `functions/` directory).

### Database (D1)

```bash
# Create database
wrangler d1 create sixdegrees-db

# Run migrations
wrangler d1 execute sixdegrees-db --file=schema.sql

# Test locally
wrangler pages dev
```

### Email Sending (Local)

Run local scripts to send emails:
```bash
# Send single email
node send-gmail.js --to "recipient@example.com" --subject "Test" --body "Hello"

# Auto-outreach engine
node auto-outreach.js --degree 1

# Check replies
node auto-outreach.js --check-replies
```

---

## Environment Variables

**Required:**
- `ANTHROPIC_API_KEY` — Claude API key (for strategy generation)
- `GMAIL_ADDRESS` — Gmail sender address
- `GMAIL_APP_PASSWORD` — Gmail App Password (not regular password)

**Cloudflare Secrets:**
```bash
wrangler secret put ANTHROPIC_API_KEY
wrangler secret put GMAIL_ADDRESS
wrangler secret put GMAIL_APP_PASSWORD
```

**Local Development:**
Create `.dev.vars`:
```
ANTHROPIC_API_KEY=sk-ant-...
GMAIL_ADDRESS=jianou.works@gmail.com
GMAIL_APP_PASSWORD=your_app_password
```

---

## Testing

See `TEST.md` for complete test plan.

**Quick Test Flow:**
1. Open `/public/index.html` (landing page)
2. Click "Start Now" → `/intake.html`
3. Fill all 6 fields, submit
4. Verify redirect to `/dashboard.html?campaign=camp_...`
5. Check dashboard shows strategy, 6-degree chain, email carousel
6. Switch tabs (Connections, Credits, Settings)
7. Toggle language (EN ↔ 中文)
8. Click "Refresh" — verify data updates

---

## Known Limitations (V1)

1. **Email sending requires local script** — Not automated from web
2. **No Gmail OAuth** — Using App Password for V1 (OAuth requires complex flow)
3. **No reply detection** — Manual check via `auto-outreach.js --check-replies`
4. **No Stripe webhook** — Credits not auto-updated after payment
5. **No email editing** — User sees preview but can't edit before send
6. **No multi-campaign support** — Dashboard shows single campaign

**V2 Roadmap:**
- Add Gmail OAuth for web-based email sending
- Implement Stripe webhook for auto-credit updates
- Add email editing modal
- Support multiple campaigns per user
- Auto-reply detection via Gmail API
- API access for Pro users

---

## File Structure

```
projects/sixdegrees/
├── public/
│   └── index.html              Landing page
├── intake.html                 Intake form
├── dashboard.html              Dashboard (4 tabs)
├── functions/
│   └── api/
│       ├── intake.js           POST /api/intake
│       ├── campaign/
│       │   └── [id].js         GET /api/campaign/:id
│       └── send.js             POST /api/send
├── schema.sql                  D1 database schema
├── wrangler.toml               Cloudflare configuration
├── send-gmail.js               Gmail SMTP sender (local)
├── auto-outreach.js            Auto-outreach engine (local)
└── outreach-chain.json         6-degree chain config
```

---

## Key Decisions (DHH Principles)

### 1. Vanilla JS over React
**Why:** This is a 3-page app with minimal state. React adds 100KB+ for zero benefit. Vanilla JS + Tailwind keeps it fast and simple.

### 2. Cloudflare Workers over AWS Lambda
**Why:** Workers are faster (edge), cheaper ($0 for low traffic), and integrate natively with D1 (SQLite). No cold starts.

### 3. Gmail SMTP over MailChannels
**Why:** MailChannels was deprecated. Gmail SMTP is free (15K sends/day), reliable, and uses existing Gmail account.

### 4. Local email scripts over web API
**Why:** Cloudflare Workers can't make raw SMTP connections. Local scripts via nodemailer is the simplest path for V1.

### 5. Stripe Payment Links over embedded checkout
**Why:** Payment Links take 5 minutes to set up, no code needed, mobile-friendly, and Stripe handles everything. Embedded checkout requires complex integration.

### 6. Bilingual via data attributes over separate sites
**Why:** One codebase, instant language switch, no server-side rendering needed. LocalStorage persists choice.

### 7. Tailwind CDN over build process
**Why:** No build step = faster iteration. For production, switch to compiled Tailwind to remove unused classes.

---

## Metrics

**Performance Targets:**
- Landing page load: < 1s
- Intake form submit: < 3s (includes Claude API call)
- Dashboard load: < 1s
- Dashboard auto-refresh: < 500ms

**User Flow Targets:**
- Landing → Dashboard: < 5 minutes
- Campaign creation success rate: > 90%
- Email send success rate: > 95%

---

## Next Actions

1. **Deploy to production** — `wrangler pages publish`
2. **Configure Stripe Payment Links** — Add real pricing
3. **Test end-to-end flow** — Real campaign + email send
4. **Add monitoring** — Cloudflare Analytics + error tracking
5. **Launch on Product Hunt** — Announce V2

---

**Document Status:** ✓ Complete
**Implementation Status:** ✓ Complete
**Deployment Status:** Pending (local testing complete)
