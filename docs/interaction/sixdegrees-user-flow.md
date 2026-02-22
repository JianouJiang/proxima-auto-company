# SixDegrees User Flow — Interaction Design

**Author:** Alan Cooper (Interaction Design Director)
**Date:** 2026-02-22
**Goal:** Transform SixDegrees from "search tool" → "AI agent that actively reaches people on your behalf"

---

## Core Design Principle: Goal-Directed

**Primary User Goal:** Reach a specific person through a chain of existing connections, WITHOUT doing the research or writing emails myself.

**NOT:** "I want to search for connections" (task-based)
**YES:** "I want to have someone introduce me to person X, and I want the AI to handle everything" (goal-based)

This distinction determines everything downstream.

---

## Primary Persona: The Ambitious Founder

**Name:** Sarah Chen
**Background:** 28-year-old founder, Series A fundraising
**Situation:** "I need to get 20 minutes with Sequoia's Roelof Botha to discuss my energy tech startup"
**Pain:** "I don't know Roelof. I've wasted 50+ hours on LinkedIn stalking. I've sent 5 cold emails that got no reply. I hate writing emails."
**Success Metric:** "Roelof replies to my email within 48 hours"

**Sarah's typical workflow:**
1. Identifies a target person (investor, customer, partner)
2. Has vague sense she knows someone who knows someone
3. Currently: spends 5-10 hours researching on LinkedIn, writing emails, tracking replies
4. Desired: "Tell SixDegrees the target, go make a coffee, check dashboard for results"

---

## Secondary Persona: The Researcher

**Name:** Marcus Washington
**Background:** Academic trying to partner with industry
**Situation:** "I need to reach an engineer at Google working on differentiable programming"
**Pain:** "I don't network well. I don't know what industry people do. I don't want to seem desperate in emails."
**Success Metric:** "Establish a real conversation with someone at the target company"

---

## Information Architecture: 5 Core Screens

### Screen 1: Landing Page (Public)
**Purpose:** Explain what SixDegrees does, NOT how it works technically.

**User Needs:**
- "What is this?" (value proposition)
- "Will this work for ME?" (relevance check)
- "Is it safe?" (trust/privacy)
- "What's the catch?" (pricing)

**Key Elements:**
- Hero: "AI Agent That Reaches Anyone For You"
- One clear CTA: "Start Your First Connection"
- 3-4 proof points (not features):
  - "Research your target's background & interests"
  - "Find the shortest path through YOUR network"
  - "Personalize outreach from YOU (not a bot)"
  - "Get replies within 48 hours (or credits back)"
- Trust signals: Privacy policy, no spam guarantee
- Pricing preview: "Free trial: 1 connection. Then $29/month for 10/month"

**Do NOT:**
- Explain technical architecture
- Use jargon like "6-degree graph algorithm"
- Mention database schemas
- Show CLI commands

---

### Screen 2: Intake Form
**Purpose:** Capture target + context. Single page, 90 seconds.

**Mental Model:** "Tell me who you're trying to reach, and why. That's all I need."

**Input Fields (in this order):**

```
┌─ Your Email (optional now, required to start)
├─ Your Name
├─ Who do you want to reach?
│  └─ Name [textbox: "Elon Musk"]
│  └─ Title/Company [textbox: "CEO, Tesla"]
│  └─ Why them? [textarea: "Want to discuss energy storage for EVs"]
├─ Quick intro to yourself (100 words)
│  └─ [textarea: "I'm founder of X. We're solving Y problem..."]
└─ [Blue Button: "Let AI Research & Plan"]
```

**Interaction Patterns:**

| User Action | Feedback | Next State |
|------------|----------|-----------|
| Fills form | Progress bar shows 4/4 filled | Submit button becomes enabled (was greyed out) |
| Clicks submit | Page says "Analyzing your request..." | Spinner shows for 2 sec, then redirects to Sign-In |
| All fields empty | Submit button greyed out, helpful message: "Help us understand your goal" | No state change |
| Target person doesn't exist | Advisory message when they blur the field: "We couldn't find public info. That's OK—tell us what you know" | Field stays editable |

**Error Prevention (not error handling):**
- "Your Name" has character limit of 50 with live counter
- "Why them?" has 500-char limit with encouraging message "Tell the story..."
- If user lands here without email, they see: "Almost there—just sign in with Gmail to start"

**Success State:**
After submit, page transitions to Google Sign-In (OAuth flow).

---

### Screen 3: Gmail Sign-In (Authentication Gate)

**Why now, not earlier?**
- Founder wants to see the plan BEFORE asking for permissions
- NO: Ask for email on landing page
- YES: Get email on intake form, then auth for dashboard

**Mental Model:** "I'm logging in so the AI can use my Gmail to send emails from MY account to MY network."

**Implementation:**
```
┌─ Centered modal with logo
├─ "Sign In with Google"
├─ [Blue Button: Google OAuth flow]
├─ Privacy note below:
│  └─ "We read your contacts to find connection chains.
│     └─ We never sell data or access without your permission.
│     └─ View our privacy policy."
└─ [Option: "Continue as guest (no email sending)"]
```

**Scopes Required (minimum):**
- `gmail.send` — to send emails from user's Gmail
- `contacts.read` — to find connection paths
- `profile` — to get user name/email

**Persona Concern (Sarah):** "Will this spam my contacts or look weird?"
**Solution:** On next screen, show her EXACTLY who we're contacting before sending anything.

---

### Screen 4: Dashboard (The Heart of It)
**Purpose:** Show Sarah the AI's plan, monitor execution, manage credits.

**This is where the magic happens.**

**Four sections (tabs + scroll):**

#### Section 4A: "Your Campaign" Tab (Default view when first visit)

```
┌─ Top Bar
│  ├─ [Breadcrumb: "Elon Musk" | Collapse/Expand]
│  └─ Status badge: [Connected! 🎉] or [In Progress...] or [Ready to Launch]
│
├─ AI Strategy Card
│  ├─ "AI Plan to Reach Elon Musk"
│  ├─ Text summary (150 words):
│  │   "We found 3 connection paths to your target:
│  │    Path A: You → Friend A → Researcher B → Engineer C → Elon (5 degrees)
│  │    Path B: You → College Friend → Tesla Employee → Elon (3 degrees)
│  │    Path C: You → Advisor → VC → Elon (4 degrees)
│  │
│  │    We're going with Path B (shortest + highest probability).
│  │    Total timeline: 8 days (3 email cycles with 48hr response windows)."
│  │
│  ├─ Visual: 6-Degree Chain Diagram (SVG)
│  │   [You] → [College Friend] → [Tesla Emp.] → [Elon]
│  │   (each node clickable to see email draft)
│  │
│  └─ Actions:
│     ├─ [View Full Plan (shows all paths ranked)]
│     ├─ [Start Campaign] (launch emails)
│     └─ [Edit Target] (change who we're reaching)
│
├─ Live Status Section (Only shown if campaign is active)
│  ├─ "What's Happening Now" (auto-refresh every 30 sec)
│  ├─ Timeline of events:
│  │   "Today 3:15 PM — Email #1 sent to College Friend"
│  │   "Yesterday 2:40 PM — AI analyzed College Friend's network"
│  │   "2 days ago — Plan completed"
│  │
│  └─ Next milestone:
│     "Waiting for College Friend's reply (48 hours timeout)"
│     [Progress bar: 32 hours elapsed]
│
└─ Email Preview Carousel
   ├─ Email #1 (To: College Friend):
   │  ├─ Subject: "Quick intro to Sarah Chen — Tesla energy project"
   │  ├─ Preview text (first 100 chars)
   │  ├─ [View full email]
   │  ├─ Status: ✓ Sent (3 hours ago)
   │  └─ Reply: Not yet (waiting)
   │
   ├─ Email #2 (To: Tesla Employee):
   │  ├─ [Waiting for Email #1 reply before sending]
   │  ├─ Status: ⏳ Draft (ready to send)
   │  └─ Scheduled: When #1 gets reply
   │
   └─ Email #3 (To: Elon):
      ├─ [Chain depends on Email #2]
      ├─ Status: ⏳ Not yet drafted
      └─ [View strategy]
```

**Key Interaction Pattern:** User should understand at a glance:
- "Who are we contacting?" (6-degree chain)
- "What will the email say?" (preview)
- "What's happening RIGHT NOW?" (status)
- "What do I do next?" (action buttons)

**No jargon. No machine language. Everything in human terms.**

---

#### Section 4B: "Connections" Tab (Email History)

```
┌─ Filters: [All] [Sent] [Replied] [No Reply]
│
├─ Email List (chronological, newest first)
│  │
│  ├─ [Sent 6 hours ago] → College Friend (john@college.com)
│  │  ├─ Subject: "Quick intro to Sarah Chen..."
│  │  ├─ Status: ✓ Delivered
│  │  └─ [View email] [View reply] [Forward/Follow-up]
│  │
│  ├─ [Sent yesterday] → Friend of Friend (alice@company.com)
│  │  ├─ Subject: "Connection request from Sarah..."
│  │  ├─ Status: ✓ Read (2x)
│  │  └─ [View email] [View reply] [Forward/Follow-up]
│  │
│  └─ [Draft] → Tesla Engineer (engineering@tesla.com)
│     ├─ Subject: (auto-generated)
│     ├─ Status: ⏳ Waiting for trigger
│     └─ [Preview] [Edit] [Send manually]
│
└─ Details Panel (when user clicks an email)
   ├─ Full email body
   ├─ Recipient's reply (if exists)
   ├─ Next-step suggestion from AI
   └─ [Mark as done] or [Schedule follow-up]
```

**Principle:** User can see exactly what was sent, to whom, and what happened. No surprises.

---

#### Section 4C: "Credits & Payment" Tab

```
┌─ Credit Balance Display
│  ├─ You have 7 campaigns remaining
│  ├─ Plan: "Starter ($0/month free trial)"
│  └─ Next billing: N/A
│
├─ Pricing Cards (three options):
│  │
│  ├─ Card 1: Free
│  │  ├─ "1 campaign/month"
│  │  ├─ "Always free"
│  │  └─ [Current plan ✓]
│  │
│  ├─ Card 2: Starter ($29/month)
│  │  ├─ "10 campaigns/month"
│  │  ├─ "Priority AI planning"
│  │  ├─ [Upgrade button → Stripe Payment Link]
│  │  └─ "Try free for 30 days"
│  │
│  └─ Card 3: Pro ($99/month)
│     ├─ "Unlimited campaigns"
│     ├─ "API access"
│     ├─ "Dedicated support"
│     └─ [Upgrade button → Stripe Payment Link]
│
└─ Payment History
   ├─ No payments yet
   └─ "Upgrade to see billing history"
```

**Why Stripe Payment Links (not embedded form)?**
- Fastest to implement ✓
- Handles security/PCI compliance ✓
- User trusts Stripe ✓
- Mobile-friendly ✓

**No payment wall on first campaign.** Free trial: 1 complete campaign.

---

#### Section 4D: "Settings" Tab (Minimal)

```
┌─ Account
│  ├─ Email: sarah@company.com
│  ├─ Name: Sarah Chen
│  └─ [Edit]
│
├─ Preferences
│  ├─ Language: [English ▼] [中文]
│  ├─ Email reminders: [Toggle: ON]
│  ├─ Email every 6 hours about campaign status
│  │
│  └─ Privacy
│     ├─ Share my profile (for network analysis): [Toggle: ON]
│     └─ (Explains: "Helps AI find better connection paths")
│
└─ Danger Zone
   ├─ [Disconnect Gmail]
   ├─ [Clear all campaign data]
   └─ [Delete account]
```

**Keep it minimal.** 90% of power users won't visit this tab.

---

## User Journey Map: "From Target to First Reply"

### Timeline: Day 0 to Day 10

```
DAY 0 (Hour 0)
├─ Sarah lands on homepage
├─ "AI Agent That Reaches Anyone For You"
├─ Clicks "Start Your First Connection"
└─ → Intake Form

DAY 0 (Hour 0:15)
├─ Fills form: Target = "Roelof Botha, Sequoia"
├─ "Why him?" = "Want to discuss series A fundraising for energy tech"
├─ Clicks "Let AI Research & Plan"
└─ → Gmail Sign-In OAuth

DAY 0 (Hour 0:30)
├─ Completes OAuth consent (read contacts, send email)
└─ → Dashboard / "Your Campaign" tab

DAY 0 (Hour 0:45) ← CRITICAL MOMENT
├─ Sarah sees:
│  ├─ "AI found 4 paths to Roelof"
│  ├─ 6-degree chain visualization
│  ├─ Email #1 preview: "To: College Friend Jake"
│  ├─ "[Start Campaign]" button prominent
│  └─ "Ready to reach Roelof? Here's the plan..."
│
└─ Sarah clicks [Start Campaign]

DAY 0 (Hour 1:00)
├─ Email #1 sent to Jake: "Quick intro to Sarah Chen..."
├─ Status: ✓ Delivered
├─ Dashboard shows: "Waiting for Jake's reply (48 hours)"
└─ Sarah closes browser

DAY 1 (Hour 14:00)
├─ Email arrives: Jake replies "Happy to help! Let me forward you to my colleague at Tesla..."
├─ AI detects reply, initiates Email #2
├─ Email #2 (To: Tesla colleague): "Thanks for the intro from Jake..."
├─ Status: ✓ Delivered
└─ Dashboard notifies Sarah: "First reply! Moving to next step..."

DAY 2 (Hour 15:00)
├─ Tesla colleague replies with intro to Roelof
├─ AI drafts Email #3 (to Roelof): "Tesla colleague introduced us..."
├─ Email #3 sent
├─ Status: ✓ Delivered
└─ Dashboard: "You're 1 degree away now!"

DAY 3 (Hour 09:00)
├─ Roelof replies: "Let's hop on a call Tuesday"
├─ Dashboard celebration: "🎉 SUCCESS! Roelof replied!"
├─ [Schedule call]
└─ Sarah got what she wanted without writing a single email

TOTAL TIME: 3 days
SARAH'S EFFORT: 5 minutes (form + start)
EMAILS WRITTEN: 0 (AI wrote them all)
SUCCESS: Roelof engaged
```

---

## Interaction Patterns: How Users Discover & Use Features

### Pattern 1: Progressive Disclosure
**Problem:** Landing page is overwhelming if we show 100% of features.
**Solution:** Show only what's relevant at each stage.

| Stage | Show | Hide |
|-------|------|------|
| Landing | Value prop, CTA | Pricing, integrations |
| Intake | Target name, context | Campaign history, credits |
| Dashboard (new campaign) | Strategy, plan | API, bulk campaigns |
| Dashboard (active campaign) | Live status, replies | Advanced filters, webhooks |

### Pattern 2: Confirmation Without Friction
**Problem:** Sarah is nervous. "Will this email look weird from an AI?"
**Solution:** Always show draft BEFORE sending.

```
User Action: Clicks [Start Campaign]
↓
System Response: "Preview your email to Jake"
(shows full email text)
↓
Two options:
├─ [Send As-Is] (blue, primary)
└─ [Edit This Email] (gray, secondary)
```

**NOT:** Confirmation dialog ("Are you sure?"). **YES:** Draft preview.

---

### Pattern 3: Status Without Polling
**Problem:** Sarah checks dashboard 20 times/hour. "Did Jake reply yet?"
**Solution:** Push notifications (email reminder), not pull.

```
Dashboard shows:
├─ Last checked: 2 hours ago
├─ [Refresh] button (manual override)
└─ Notification: "Jake replied! → New email sent to Tesla colleague"

Email to Sarah:
├─ Subject: "🎉 Jake replied to your outreach"
├─ CTA: "See what's next" → Dashboard
```

---

### Pattern 4: Error Recovery (Graceful Degradation)
**Scenario:** Gmail OAuth fails. Stripe API down. Email bounces.

**Rule:** Never show technical errors to user.

| Technical Error | User Message | Action |
|-----------------|--------------|--------|
| Gmail OAuth timeout | "Hmm, couldn't verify Gmail. Try again?" | [Retry button] |
| Email bounced (recipient not found) | "Looks like Jake's email changed. Want to update it?" | [Add new email] |
| Stripe API error | "Can't process payment right now. We'll retry in 1 hour." | [Check back later] |
| AI plan generation failed | "Still analyzing connections... usually takes 2 min." | [Keep waiting] [Contact us] |

**Key principle:** User is NEVER told "Database error" or "Network timeout." They hear human language.

---

## Input Requirements by Screen

### Intake Form (Minimum Data)
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

### Campaign Creation (Derived by AI)
```json
{
  "campaign_id": "uuid",
  "user_id": "uuid",
  "target_info": { name, company, research_notes },
  "connection_paths": [
    {
      "path_id": "path-1",
      "degree": 3,
      "confidence": 0.85,
      "chain": [
        { user_id, user_name },
        { contact_id, contact_name, contact_email },
        { intermediate_id, intermediate_name, intermediate_email },
        { target_id, target_name, target_email }
      ]
    }
  ],
  "selected_path": "path-1",
  "emails": [
    {
      "degree": 1,
      "recipient_email": "...",
      "subject": "...",
      "body": "...",
      "status": "draft|sent|replied"
    }
  ]
}
```

---

## Feedback Mechanisms: How Users Know What's Happening

### Real-time Feedback (During User Action)
```
User clicks:         System shows:
─────────────────────────────────────────
[Fill form]          Progress: 1/4 → 2/4 → 3/4 → 4/4
[Submit]             Spinner + "Analyzing your request..." (2 sec)
[Start Campaign]     Status: "Sending email..." (1 sec)
[View email]         Email body fades in (100ms animation)
```

### Temporal Feedback (Over Minutes/Hours)
```
Email status progression:
✉️  Sent (just now)
↓
📬 Delivered (10 seconds later)
↓
👁️  Read (if email opened)
↓
↩️  Replied (when response arrives)
```

**Shown on dashboard:** Live update, no refresh needed.

### Instructional Feedback (Guiding User)
```
When user opens dashboard for first time:
┌─ Tour overlay (optional, can dismiss)
├─ "Here's your 6-degree chain to Roelof" → highlights chain diagram
├─ "Here's the email we'll send to Jake" → highlights email preview
├─ "Ready? Click Start" → button pulses
└─ [Got it] [Show me more]
```

**Key:** Not a popup. An overlay tour that explains the interface.

---

## Error States: What Can Go Wrong?

### Category 1: User Errors (Bad Input)
```
Error: Invalid email on intake form
├─ Detection: User types "elon@" and blurs field
├─ Message: "Is that email complete?" (friendly, not "INVALID EMAIL")
├─ Solution: User corrects, continues
└─ No form submission blocked

Error: Target person doesn't exist
├─ Detection: AI can't find public info on target
├─ Message: "Can't find public info on Roelof (that's OK—we work with less)"
├─ Solution: Let user continue anyway, AI tries different strategies
└─ Campaign still launches
```

### Category 2: System Errors (Fixable)
```
Error: Gmail OAuth fails
├─ Detection: OAuth window doesn't close, timeout after 30 sec
├─ Message: "Couldn't sign in. Network hiccup? Try again."
├─ Solution: [Retry button]
└─ No data lost

Error: Email send fails (MailChannels API down)
├─ Detection: API returns 5xx error
├─ Message: "Email not sent yet. We're retrying... (usually works within 5 min)"
├─ Solution: Auto-retry every 30 sec, user can see retry count
└─ Email queued in database, not lost
```

### Category 3: Business Logic Errors (Design Prevention)
```
Error: User has 0 campaigns remaining
├─ Detection: User clicks [Start Campaign], limit reached
├─ Message: "You've used your 1 free campaign. Want to upgrade?"
├─ Solution: Show pricing, [Upgrade now] button
└─ Form doesn't submit, no frustration

Error: No connection path found to target
├─ Detection: AI analyzed contacts, couldn't find chain
├─ Message: "We couldn't find a connection path. Here's why... Want to try a different target?"
├─ Solution: [Start new campaign] or [Edit target]
└─ Campaign doesn't launch; user tries different approach
```

---

## Wireframe-Level Prototypes

### Landing Page Layout
```
┌─────────────────────────────────────────────────────────────────┐
│  [Lang Toggle: 中文]                                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│               AI Agent That Reaches Anyone For You                │
│                                                                   │
│           [See How It Works]  [Start Your First Connection]      │
│                                                                   │
│          6 degrees of separation. Your AI agent finds the path.   │
│                                                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│                      ─── How It Works ───                        │
│                                                                   │
│  [Icon] Research        [Icon] Find Path      [Icon] Send        │
│  Your target's          through your          personalized       │
│  background             network               emails             │
│                                                                   │
│  [Icon] Track           [Icon] Get Result      [Icon] Celebrate  │
│  every reply            in 3-7 days            the intro         │
│                                                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│                    ─── Why SixDegrees? ───                       │
│                                                                   │
│  ✓ No more cold emails (personalized through warm intros)       │
│  ✓ AI does the research (you just set the target)               │
│  ✓ Replies in 48 hours (or your credits back)                   │
│  ✓ Privacy first (we don't sell data)                           │
│                                                                   │
├─────────────────────────────────────────────────────────────────┤
│                           Privacy | Pricing | Contact us         │
└─────────────────────────────────────────────────────────────────┘
```

### Dashboard Layout (Campaign In Progress)
```
┌─────────────────────────────────────────────────────────────────┐
│  SixDegrees  [Logo]    Elon Musk Campaign    [Settings]  [Logout]│
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─ [Your Campaign] [Connections] [Credits] [Settings] ────────┐│
│  │                                                              ││
│  │         AI Strategy to Reach Elon Musk                      ││
│  │         Status: In Progress [████████░░]                   ││
│  │                                                              ││
│  │   6-Degree Chain Visualization:                            ││
│  │   [You] → [Friend] → [Tesla Emp] → [Researcher] → [Elon] ││
│  │     ✓       ✓          ✓              ⏳        ⏳         ││
│  │   (Sent)  (Replied)  (Replied)    (Waiting)  (Draft)      ││
│  │                                                              ││
│  │   What's Happening Now (auto-refresh):                     ││
│  │   ├─ ✓ Email sent to Friend (2 hours ago)                 ││
│  │   ├─ ✓ Friend replied (1 hour ago)                        ││
│  │   ├─ ✓ Email sent to Tesla Emp (45 min ago)              ││
│  │   ├─ ⏳ Waiting for Tesla Emp reply (48h timeout)         ││
│  │   └─ [Refresh]                                            ││
│  │                                                              ││
│  │   Email Preview Carousel:                                  ││
│  │   ┌─ Email #1 (to Friend): Subject: "Quick intro..."     ││
│  │   │  Status: ✓ Delivered                                 ││
│  │   │  Reply: "Happy to help! Let me intro you to..."      ││
│  │   │  [View full]                                         ││
│  │   │                                                       ││
│  │   ├─ Email #2 (to Tesla Emp): Subject: "Intro from..."  ││
│  │   │  Status: ✓ Delivered                                ││
│  │   │  Reply: Waiting...                                  ││
│  │   │  [View full]                                        ││
│  │   │                                                      ││
│  │   └─ Email #3 (to Elon): [Draft, waiting for #2 reply] ││
│  │      [View draft]                                       ││
│  │                                                          ││
│  │   [More details below] ↓                                ││
│  │                                                          ││
│  └──────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## Bilingual (EN / 中文) Strategy

**NOT:** Separate sites. **YES:** Toggle language on every page.

```
Language Toggle (top-right):
┌──────────────────────┐
│ [English ▼] [中文]   │
└──────────────────────┘

On click:
- Entire page re-renders in selected language
- Local storage saves preference
- All future visits use saved language
- Every element has data-en="..." data-zh="..."
```

**Translation approach:**
- All UI strings in JSON file (`/lang/strings.json`)
- Translates by user's browser preference (not server-side)
- Fastest, no server latency

---

## Key Success Metrics (For Design)

| Metric | Target | Why |
|--------|--------|-----|
| Time from landing to campaign start | < 5 min | User should feel friction-free |
| Dashboard comprehension on first visit | > 80% | Users understand what's happening |
| Email draft preview completion rate | > 90% | Users confirm before we send |
| Campaign completion rate | > 70% | Users get replies (AI quality metric) |
| Upgrade rate (free → paid) | > 15% | Business viability |
| Return visit rate (7-day) | > 40% | Users trust the product |

---

## Design Red Flags (What NOT to Do)

### 🚫 Red Flag 1: Showing Technical Implementation
**Bad:** "Your request is in the processing queue. Job ID: 12345-xyz"
**Good:** "Analyzing your target... almost done (2 min remaining)"

### 🚫 Red Flag 2: Requiring User Decisions AI Can Make
**Bad:** "Select which path to use: Path A (85% confidence) vs Path B (72%)"
**Good:** "We recommend Path A. Here's why: [brief explanation]"

### 🚫 Red Flag 3: Multi-Step Confirmation Flows
**Bad:** "Confirm? → Are you sure? → Final confirmation?"
**Good:** "Here's your email. [Send] [Edit] [Cancel]"

### 🚫 Red Flag 4: Hiding Critical Info Behind Secondary Tabs
**Bad:** Put "Campaign Status" behind [Advanced] tab
**Good:** Status is primary; advanced options are secondary

### 🚫 Red Flag 5: Demanding Email Writing Skill
**Bad:** "Customize the email template before sending"
**Good:** AI writes; user only edits if they want

---

## Next Actions: For Implementation

1. **Frontend engineers** (fullstack-dhh):
   - Build intake form (Screen 2)
   - Build dashboard tabs (Screen 4A-D)
   - Implement language toggle (EN/中文)
   - Add email preview modal

2. **Backend engineers** (devops-hightower):
   - Gmail OAuth integration (Google Sign-In)
   - Campaign creation API endpoint
   - Email send queuing with MailChannels/Resend
   - Connection path ranking algorithm

3. **AI/Logic layer** (to be determined):
   - Target research module (search public info)
   - Connection graph traversal (find 6-degree paths)
   - Email draft generation (personalized templates)
   - Reply detection (email parsing)

4. **Product** (product-norman):
   - Validate Persona assumptions with 3-5 users
   - Test intake form clarity (can users explain why they need target?)
   - Measure dashboard comprehension time
   - A/B test "Start Campaign" vs "Launch Outreach" button copy

5. **QA** (qa-bach):
   - Test OAuth happy + failure paths
   - Verify email preview shows correct recipient
   - Test bilingual rendering (fonts, layout)
   - Edge case: target not found, no connection path, Gmail auth timeout

---

## Summary: Why This Design Works

**For Sarah Chen (founder, our primary persona):**
- Lands → 30 sec to understand value
- Form → 2 min to describe goal
- Dashboard → Immediately sees the plan, not a search interface
- Trusts it → Can preview exactly what will be sent
- Gets results → 3-7 days to first real reply
- Repeats → Because she saw the AI actually worked

**For Marcus Washington (researcher, secondary persona):**
- No network anxiety → AI does the research
- Professional tone → Emails sound like him, not a bot
- Credibility → Intro chain is warm, not cold

**For business:**
- Clear funnel: Landing → Intake → OAuth → Dashboard → Campaign → Payment
- Monetization path: Free trial (1 campaign) → Paid (10+/month)
- Retention driver: Users who get one reply will buy more campaigns
- Viral potential: "How did you get Elon to reply?" → "SixDegrees"

This is not a search tool. This is an AI agent that **takes action on behalf of the user**, and the UI reflects that from the first interaction.

---

**Document Version:** 1.0
**Status:** Ready for engineering handoff
**Next Review:** After intake form + dashboard MVP built
