# SixDegrees Interaction Design — Engineering Handoff Summary

**For:** fullstack-dhh, devops-hightower, qa-bach
**Date:** 2026-02-22
**Status:** Complete design document ready at `/docs/interaction/sixdegrees-user-flow.md`

---

## Executive Summary

SixDegrees is **NOT a search tool**. It's an **AI agent service that takes action on user's behalf**.

User journey:
1. Landing page (explain value)
2. Intake form (tell AI target person)
3. Gmail sign-in (verify identity, enable email)
4. Dashboard (show plan, track execution, send emails)
5. Payment (Stripe Payment Links when user wants more campaigns)

**Critical principle:** User should trust that the AI will do exactly what they see in the preview.

---

## Five Core Screens (Build Order)

### Priority 1: Intake Form (Critical path blocker)
**Location:** `projects/sixdegrees/intake.html` (already exists, needs update)

**Must collect:**
- User email (auto-filled from email field or form)
- User name
- Target person (name, title/company)
- Why you need to reach them (textarea, 100-500 words)
- Your background (textarea, 100 words)

**Interaction:**
- All fields required before [Submit] enabled
- On submit: "Analyzing your request..." → redirect to OAuth
- Language toggle: EN / 中文 (switch entire form)

**Do NOT:**
- Ask for access permissions on this screen
- Ask for more than 5 input fields
- Show technical jargon

---

### Priority 2: Gmail OAuth / Sign-In
**Location:** `projects/sixdegrees/` (new file or modal)

**Flow:**
1. After intake form submit, show modal: "Sign in with Gmail to start campaign"
2. User clicks [Sign in with Google]
3. Google OAuth consent screen (request scopes: `gmail.send`, `contacts.read`)
4. Redirect to dashboard on success

**Error handling:**
- OAuth timeout: Show "Try again?" with retry button
- User cancels: Return to intake form with message "You can start anytime"

---

### Priority 3: Dashboard (Heart of Product)
**Location:** `projects/sixdegrees/dashboard.html` (already exists, major refactor)

**Four tabs (default: "Your Campaign"):**

#### Tab 1: "Your Campaign"
Shows strategy + live status + email preview carousel.

**Key elements:**
- Status badge (Connected! / In Progress / Ready to Launch)
- 6-degree chain visualization (SVG diagram with status for each node)
- Text summary: "Path B (3 degrees, 85% confidence): You → Friend → Tesla Emp → Elon"
- Timeline of events: "Today 3:15 PM — Email #1 sent"
- Email preview carousel: slide through each email before/after send
- [View Full Plan] button (shows all ranked paths)
- [Start Campaign] button (primary, sends Email #1)
- [Edit Target] button (restart with new target)

**Auto-refresh:** Every 30 seconds, check for new replies

#### Tab 2: "Connections"
Email history with status.

**Features:**
- Filter: [All] [Sent] [Replied] [No Reply]
- List of emails (newest first)
- Each email shows: recipient, subject, status, timestamp
- Click to expand: full email body + reply text (if exists)
- [View reply] [Edit] [Forward follow-up] actions

#### Tab 3: "Credits & Payment"
Pricing + subscription management.

**Show:**
- Current balance: "7 campaigns remaining"
- Billing plan: "Free ($0/month)"
- Three pricing cards with [Upgrade] buttons → Stripe Payment Links

**Do NOT ask for credit card on dashboard.** Link to Stripe Payment Links.

#### Tab 4: "Settings"
Account + language + privacy.

**Show:**
- Email address
- Name
- Language toggle: [English] [中文]
- Email reminders: [Toggle ON/OFF]
- Danger zone: [Disconnect Gmail] [Delete account]

---

### Priority 4: Landing Page (Already exists, minor tweaks)
**Location:** `projects/sixdegrees/index.html`

**Tweaks:**
- Ensure clear CTA: "Start Your First Connection" (links to `intake.html`)
- Add language toggle (EN / 中文)
- Clarify: "AI does the research. AI finds the connections. AI writes the emails. You get the result."

---

### Priority 5: Email Preview Modal (New)
**Triggered:** When user clicks [Start Campaign] or views email in dashboard

**Shows:**
- To: [recipient name]
- Subject: [auto-generated]
- Full email body
- Two buttons: [Send As-Is] [Edit This Email]

**If user clicks [Edit]:**
- Unlock subject and body for editing
- Show live character count (max 500 words)
- [Send] [Discard] buttons

---

## Backend / API Requirements

### 1. POST /api/intake
**Accepts:**
```json
{
  "user_email": "sarah@company.com",
  "user_name": "Sarah Chen",
  "target_name": "Roelof Botha",
  "target_company": "Sequoia Capital",
  "target_reason": "Series A fundraising discussion",
  "user_background": "Founder of energy tech startup X"
}
```

**Returns:**
```json
{
  "success": true,
  "campaign_id": "uuid",
  "oauth_redirect_url": "https://accounts.google.com/o/oauth2/v2/auth?..."
}
```

**Action:** Create campaign record, return OAuth consent URL

---

### 2. GET /api/campaign/:campaign_id
**Requires:** OAuth token (JWT or session)

**Returns:**
```json
{
  "campaign_id": "uuid",
  "target_name": "Roelof Botha",
  "status": "in_progress",
  "selected_path": {
    "degree": 3,
    "confidence": 0.85,
    "chain": [
      { "user_id": "...", "name": "Sarah Chen", "status": "sender" },
      { "contact_id": "...", "name": "Jake", "email": "jake@college.com", "status": "sent" },
      { "contact_id": "...", "name": "Tesla Emp", "email": "emp@tesla.com", "status": "sent" },
      { "target_id": "...", "name": "Roelof", "email": "roelof@sequoia.com", "status": "draft" }
    ]
  },
  "emails": [
    {
      "email_id": "uuid",
      "degree": 1,
      "recipient_email": "jake@college.com",
      "subject": "Quick intro to Sarah Chen...",
      "body": "Dear Jake...",
      "status": "sent",
      "sent_at": 1708595400,
      "reply_received": true,
      "reply_text": "Happy to help! Let me intro you to..."
    }
  ],
  "created_at": 1708595400,
  "last_updated_at": 1708595400
}
```

---

### 3. POST /api/campaign/:campaign_id/send
**Accepts:**
```json
{
  "degree": 1,
  "email_id": "uuid"
}
```

**Action:**
1. Get email draft from database
2. Send via Gmail SMTP (using MailChannels or Resend API)
3. Log to `email_outreach` table
4. Return status

**Returns:**
```json
{
  "success": true,
  "email_id": "uuid",
  "status": "sent",
  "sent_at": 1708595400,
  "message": "Email delivered successfully"
}
```

---

### 4. POST /api/oauth/callback
**Triggered:** After user completes Google OAuth consent

**Action:**
1. Exchange authorization code for access token
2. Store token in secure session/cookie
3. Redirect to dashboard with campaign_id

---

### 5. GET /api/dashboard
**Requires:** OAuth token

**Returns:**
```json
{
  "user_email": "sarah@company.com",
  "user_name": "Sarah Chen",
  "credits": 7,
  "plan": "free",
  "campaigns": [
    { "campaign_id": "...", "target_name": "Roelof Botha", "status": "in_progress" }
  ],
  "language": "en"
}
```

---

## Frontend Implementation Checklist

- [ ] Intake form validation (all fields required, character limits)
- [ ] Language toggle (EN / 中文) on every page
- [ ] OAuth sign-in button integration
- [ ] Dashboard tab navigation
- [ ] 6-degree chain SVG visualization
- [ ] Email preview modal (view/edit)
- [ ] Real-time status updates (auto-refresh every 30s)
- [ ] Email carousel (swipe through emails)
- [ ] Stripe Payment Links integration (for upgrade buttons)
- [ ] Responsive design (mobile-first)
- [ ] Loading states (spinners, skeleton screens)
- [ ] Error states (friendly messages, retry buttons)
- [ ] Bilingual strings (`/lang/strings.json`)

---

## QA Test Plan

**Critical flows:**
1. Landing → Intake → OAuth → Dashboard (new campaign)
2. View campaign in progress (emails sent, waiting for reply)
3. Completed campaign (all emails sent, target replied)
4. Payment flow (click Upgrade, Stripe link opens)
5. Language toggle (EN ↔ 中文)
6. Error recovery (OAuth timeout, email send failure)

**Edge cases:**
- User closes browser during OAuth → Return to intake, session preserved
- Target person not found → Campaign still creates, AI uses alternative strategy
- No connection path found → Show "No path found. Try different target?"
- User clicks [Edit Email] → Verify character limit enforced
- User clicks [Send As-Is] → Verify email actually sends

---

## Design Files Location

All interaction design docs: `/home/jianoujiang/Desktop/proxima-auto-company/docs/interaction/`

- **Main doc:** `sixdegrees-user-flow.md` (794 lines, comprehensive)
- **Summary:** This file (`SIXDEGREES_HANDOFF.md`)

---

## Key Reminders for Engineering

1. **No technical jargon in UI.** User never sees "database," "API," "job queue," "UUID."
2. **Always show preview before sending.** Email preview modal is non-negotiable.
3. **Language first.** Every element must support EN / 中文.
4. **Mobile-friendly.** Dashboard must be usable on iPhone (user checks on the go).
5. **Graceful errors.** Every error has a human message + action button.
6. **Fast feedback.** Dashboard updates every 30s; user knows what's happening.

---

**Document Status:** ✓ Ready for engineering kickoff
**Questions?** See main doc: `/docs/interaction/sixdegrees-user-flow.md`
