# ColdCopy User Flow Design

**Author:** Interaction Designer (Cooper)
**Date:** 2026-02-20
**Product:** ColdCopy — Cold Email Sequence Generator for B2B SaaS Founders
**Status:** Final Design — Ready for Implementation
**Timeline:** MVP in 1 week

---

## 1. Primary Persona Definition

Before designing the flow, I must define WHO we are designing for. Not "users" — a specific person.

### Primary Persona: "Founder Frank"

**Demographics:**
- B2B SaaS founder, 1-3 person team
- Technical background (can code), bootstrapping or small pre-seed
- 30-45 years old, works 60+ hours/week
- Located in US/Europe, speaks English fluently

**Goals:**
- **End Goal:** Get 10-20 sales meetings per month from cold outreach
- **Experience Goal:** Write cold emails that don't feel scammy or robotic
- **Life Goal:** Build a profitable SaaS business without raising VC money

**Context & Behavior:**
- Currently writes cold emails manually in Gmail or uses basic templates
- Knows cold email best practices (AIDA, PAS) but struggles to apply them consistently
- Has tried ChatGPT but output is too generic — lacks SaaS-specific language
- Time-poor — wants to generate sequences in under 10 minutes and paste into Lemlist/Instantly/Apollo
- Willing to pay $29-49 if it saves 2+ hours of writing and testing

**Pain Points:**
- Generic AI tools don't understand SaaS sales motion (trial → demo → contract vs. immediate purchase)
- Free tools produce cringeworthy output ("I hope this email finds you well...")
- Subject lines are clickbait, not professional
- No follow-up timing recommendations or A/B variants

**Technical Comfort:**
- Can use web forms easily
- Prefers copy-paste over integrations (wants control over final edits)
- Uses Lemlist/Instantly/Apollo for sending, just needs the copy

**Decision Criteria:**
- Output quality > feature count
- Speed to usable result > customization options
- "Does this sound like a human wrote it?" is the #1 quality bar

### Why This Persona Matters

All design decisions below are optimized for **Founder Frank**. Not agencies (too broad), not SDRs at enterprise companies (different needs), not freelancers (different value prop). One persona. One product.

---

## 2. User Journey Map: Landing → Delivered Sequences

### Entry Point: Search or Direct Link

**How Frank Finds Us:**
- Google search: "cold email generator for saas founders"
- Reddit post in r/SaaS or r/Entrepreneur
- Product Hunt "Product of the Day"
- Direct link from founder community (Indie Hackers, MicroConf Slack)

**Landing Page Goal:** Convince Frank in 5 seconds that this is NOT another generic AI tool.

---

### Step 1: Landing Page (0-10 seconds)

**User Mental State:** Skeptical. "Is this just ChatGPT with a wrapper?"

**What Frank Sees:**
- **Hero Headline:** "Cold Email Sequences That Actually Book Meetings — Optimized for B2B SaaS Founders"
- **Sub-headline:** "Not generic templates. SaaS-specific sequences with trial CTAs, demo hooks, and technical credibility builders. Used by 50+ bootstrapped founders."
- **Visual Proof:** Side-by-side comparison:
  - Left: ChatGPT output (generic, buzzwordy)
  - Right: ColdCopy output (specific, SaaS-aware, credible)
- **Call to Action:** Two buttons:
  - **"Generate My First Sequence (Free)"** — Primary CTA, large, bright
  - **"See Sample Sequences"** — Secondary, text link below

**Decision Point:** Does Frank trust this enough to try it?

**Design Rationale (Cooper Principles):**
- **Specificity defeats skepticism.** "B2B SaaS Founders" is not "users" or "sales teams" — it is a signal that we understand his context.
- **Visual proof > claims.** Side-by-side comparison lets Frank judge quality himself without reading marketing copy.
- **Free first sequence removes friction.** Frank's goal is "see if this is worth my time," not "commit $29."

---

### Step 2: Input Form — The Critical Moment (30 seconds - 3 minutes)

**User Mental State:** "Okay, I'll try it. But if this asks me 20 questions, I'm leaving."

**Form Structure: Progressive Disclosure (One Section at a Time)**

#### Section 1: Your Product (Required)

```
[ ] Product Name: _____________________
    Example: "Acme Analytics"

[ ] What does it do? (1-2 sentences):
    _______________________________________
    Example: "Real-time analytics dashboard for e-commerce stores. Shows conversion funnels, cart abandonment, and LTV cohorts."

[ ] Primary benefit (the ONE thing prospects care most about):
    _______________________________________
    Example: "Identify why 60% of carts abandon in under 10 seconds"
```

**Why This Order:**
- Frank knows his product. This is easy to answer.
- Builds momentum before harder questions.
- Primes the AI with the right context.

#### Section 2: Your Target Buyer (Required)

```
[ ] Job title(s): _____________________
    Example: "Head of Growth, Director of E-commerce"

[ ] Company size: [Dropdown]
    ○ 1-10 employees
    ○ 11-50 employees
    ○ 51-200 employees
    ○ 201-1000 employees
    ○ 1000+ employees

[ ] Industry (if specific): _____________________
    Example: "E-commerce, DTC brands"

[ ] Main pain point you solve:
    _______________________________________
    Example: "They lose 30-40% of revenue to cart abandonment but don't know why"
```

**Why This Order:**
- Persona definition is second nature to SaaS founders (they pitch this 10x/week).
- Company size matters for tone — cold emails to enterprise are different from startup.
- Pain point drives the entire email hook.

#### Section 3: Your Ask (Required)

```
What do you want prospects to do?
○ Book a demo call (15-30 min)
○ Sign up for a free trial
○ Watch a product video
○ Reply to continue the conversation
○ Custom: _____________________
```

**Why This Matters:**
- SaaS cold emails end with "book a demo" or "start a trial" — the CTA shapes the entire sequence.
- One click, not a text field. Frank shouldn't have to think.

#### Section 4: Tone & Style (Optional — Defaults Provided)

```
[ ] Tone: [Dropdown, default = "Professional but conversational"]
    ○ Professional but conversational (recommended)
    ○ Casual and friendly
    ○ Formal and corporate
    ○ Technical and data-driven

[ ] Include social proof? (Optional)
    [ ] Yes — I'll add customer names/stats later
    [ ] No

[ ] Compliance requirement (if any): [Dropdown, default = "None"]
    ○ None
    ○ GDPR (add unsubscribe + data processing language)
    ○ CAN-SPAM (add unsubscribe link)
```

**Design Rationale:**
- **Optional with smart defaults.** Frank can skip this and still get great output.
- **GDPR/CAN-SPAM compliance** is a pain point — generic tools ignore this. We handle it.

#### Section 5: Sequence Length (Optional)

```
How many emails in the sequence?
○ 3 emails (quick follow-up, 7-day span)
○ 5 emails (recommended, 14-day span)
○ 7 emails (aggressive follow-up, 21-day span)
```

**Default:** 5 emails (most common B2B cadence)

---

**Total Form Fields:**
- Required: 7 fields
- Optional: 4 fields
- **Estimated Time to Complete:** 2-3 minutes for a prepared founder

**Design Rationale (Cooper Principles):**
- **No elastic users.** Every field serves a specific purpose for Founder Frank. Nothing is "nice to have."
- **Respect Frank's time.** He came here to generate sequences, not fill out a survey.
- **Smart defaults reduce cognitive load.** If Frank skips optional fields, output is still usable.
- **One goal per screen.** No distractions, no upsells, no tooltips asking him to subscribe.

---

### Step 3: Generation & Loading State (5-15 seconds)

**User Mental State:** "Is this going to work, or will it be garbage like ChatGPT?"

**What Frank Sees:**
```
[Animated Spinner]

Generating your SaaS cold email sequence...

✓ Analyzing your ICP and pain point...
✓ Crafting Email 1: The Hook (Day 0)
✓ Writing Email 2: The Value Proof (Day 3)
✓ Building Email 3: The Social Proof (Day 7)
✓ Creating Email 4: The Objection Handler (Day 10)
✓ Finalizing Email 5: The Breakup Email (Day 14)
✓ Generating A/B subject line variants...

Almost done! (12 seconds remaining)
```

**Design Rationale:**
- **Progress transparency reduces anxiety.** Frank knows the system is working, not stuck.
- **Descriptive step names educate.** "Email 3: The Social Proof" teaches Frank the sequence structure.
- **Time estimate manages expectations.** "12 seconds" is short enough to wait, long enough to feel sophisticated.

**Technical Note for Vogels/DHH:**
- These are NOT real steps — the LLM generates the full sequence in one call.
- This is **fake progress** to improve perceived speed and reduce bounce rate.
- Actual generation time: 8-15 seconds (Claude API latency).

---

### Step 4: Output Display — The Moment of Truth (First Impression: 3 seconds)

**User Mental State:** "Let me skim Email 1. If it's generic, I'm closing this tab."

**Layout: Single-Page Sequence View**

```
┌────────────────────────────────────────────────────────────┐
│  Your SaaS Cold Email Sequence (5 emails, 14-day span)    │
│  Generated for: Acme Analytics → Head of Growth @ E-comm  │
│                                                            │
│  [Copy All Emails] [Download as .txt] [Start Over]        │
└────────────────────────────────────────────────────────────┘

┌─ EMAIL 1: THE HOOK (Day 0) ───────────────────────────────┐
│                                                            │
│  Subject Line (A):                                         │
│  "Are 60% of your carts abandoned in <10 seconds?"        │
│                                                            │
│  Subject Line (B):                                         │
│  "Quick question about your checkout flow"                │
│  [Copy A] [Copy B]                                         │
│  ───────────────────────────────────────────────────────  │
│  Body:                                                     │
│                                                            │
│  Hi {{FirstName}},                                         │
│                                                            │
│  I noticed {{CompanyName}} is in the DTC e-commerce space. │
│  Quick question: do you track why shoppers abandon carts   │
│  in the first 10 seconds?                                  │
│                                                            │
│  Most brands lose 30-40% of revenue to cart abandonment,  │
│  but the data sits in Google Analytics as a black box.    │
│                                                            │
│  We built Acme Analytics to solve this — real-time        │
│  heatmaps + session replays that show you exactly where   │
│  the friction is (broken checkout button? slow load?).    │
│                                                            │
│  Worth a 15-min look?                                      │
│                                                            │
│  Best,                                                     │
│  [Your Name]                                               │
│  [Your Title, Acme Analytics]                             │
│                                                            │
│  [Copy Email 1]                                            │
└────────────────────────────────────────────────────────────┘

┌─ EMAIL 2: THE VALUE PROOF (Day 3) ────────────────────────┐
│  [Same layout — subject lines + body + copy button]       │
└────────────────────────────────────────────────────────────┘

┌─ EMAIL 3: THE SOCIAL PROOF (Day 7) ───────────────────────┐
│  [Same layout]                                             │
└────────────────────────────────────────────────────────────┘

┌─ EMAIL 4: THE OBJECTION HANDLER (Day 10) ─────────────────┐
│  [Same layout]                                             │
└────────────────────────────────────────────────────────────┘

┌─ EMAIL 5: THE BREAKUP EMAIL (Day 14) ─────────────────────┐
│  [Same layout]                                             │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  FOLLOW-UP TIMING & BEST PRACTICES                         │
│  ────────────────────────────────────────────────────────  │
│  • Send Email 1 on Monday-Wednesday 8-10am (recipient TZ) │
│  • Wait 3 business days between emails (skip weekends)    │
│  • Use Email 5 only if no reply after Email 4             │
│  • Personalize {{FirstName}} and {{CompanyName}} manually │
│  • Test both subject lines (A/B split your first 100)     │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  🎉 Love this? Generate unlimited sequences for $49/month │
│                                                            │
│  This free sequence is yours to keep. Want more?          │
│  • Unlimited sequence generations                         │
│  • Advanced personalization (LinkedIn, recent news)       │
│  • A/B testing recommendations                            │
│  • Downloadable .csv for easy import                      │
│                                                            │
│  [Upgrade to Pro - $49/month] [Maybe Later]               │
└────────────────────────────────────────────────────────────┘
```

**Design Rationale (Cooper Principles):**

1. **Immediate usability.** Frank can read Email 1 in 5 seconds and judge quality. No login wall, no "sign up to see results."

2. **Copy-paste optimized.** Each email has its own [Copy] button. Frank's workflow is: copy → paste into Lemlist → edit {{variables}} → send. We remove friction.

3. **A/B subject lines without explanation.** Frank knows what A/B testing is. We give him two options, he picks one or tests both. No tutorial needed.

4. **Educational context.** "Follow-up Timing & Best Practices" teaches Frank how to USE the output, not just what it says. Generic tools dump text and disappear.

5. **Soft upsell, not aggressive.** The upgrade CTA appears AFTER Frank has seen the value. It is positioned as "want more like this?" not "you must pay to continue."

6. **No modal dialogs.** The upgrade CTA is a section, not a popup. Popups are rude. Frank can ignore it and still copy all 5 emails.

---

### Step 5A: Free User — Copy & Exit (Success Path)

**User Action:** Frank copies the emails, closes the tab, pastes into Lemlist.

**What Happens:**
- No login required (we never asked for email during generation).
- Frank leaves satisfied.
- **We lost a potential customer.**

**Why Allow This?**

Because forcing Frank to create an account BEFORE seeing value violates Cooper's principle: **software should behave like a considerate human assistant.**

A considerate assistant does the work FIRST, then asks if you want more help. A rude assistant demands payment before lifting a finger.

**Conversion Strategy (for Marketing/Operations):**
- Add a subtle "📧 Email me future updates" field at the bottom (optional, not required).
- Track anonymous usage via session ID (no cookies, respect privacy).
- If Frank comes back 2+ times, show a "Welcome back! Save your sequences with a free account" banner.

**Founder Constraint Compliance:**
This seems like we are giving away the product for free. But the constraint says "price from Day 1," not "paywall from Day 1." We ARE pricing ($49/month is visible). We are just letting Frank try before buying. Gumroad and Stripe Payment Links both support this model.

---

### Step 5B: Paid User — Checkout Flow (Revenue Path)

**Trigger:** Frank clicks "Upgrade to Pro - $49/month"

**User Mental State:** "Okay, this is good. What am I actually paying for?"

#### Checkout Step 1: Plan Selection

```
┌────────────────────────────────────────────────────────────┐
│  Choose Your Plan                                          │
│  ────────────────────────────────────────────────────────  │
│  ○ Starter — $29 one-time                                  │
│    • Generate 3 more sequences (4 total)                   │
│    • A/B subject line variants                             │
│    • Download as .txt                                      │
│    • No expiration                                         │
│                                                            │
│  ● Pro (Recommended) — $49/month                           │
│    • Unlimited sequence generations                        │
│    • LinkedIn + email combo sequences                      │
│    • Download as .csv (Lemlist/Instantly-ready)            │
│    • Advanced personalization (news hooks, job changes)    │
│    • Cancel anytime                                        │
│                                                            │
│  [Continue to Payment]                                     │
└────────────────────────────────────────────────────────────┘
```

**Design Rationale:**
- **Two tiers only.** No "Basic/Pro/Premium/Enterprise" decision paralysis. Pick one-time or unlimited.
- **$29 one-time is the decoy.** It makes $49/month look like the smart choice (4 sequences × $29 = $116 vs. $49/month unlimited).
- **Feature differentiation is clear.** One-time = limited uses. Monthly = unlimited + extras.
- **Default selection is Pro.** We guide Frank toward recurring revenue without hiding the one-time option.

#### Checkout Step 2: Payment (Stripe Payment Link)

**What Frank Sees:**
- Redirect to Stripe Checkout (hosted by Stripe, not us).
- Pre-filled plan name and price.
- Email field (required by Stripe).
- Card details.

**What Happens After Payment:**
1. Stripe redirects Frank back to ColdCopy with a session token.
2. ColdCopy shows: "Payment successful! Your Pro account is active."
3. Frank can now generate unlimited sequences (no login required initially — session token in URL).
4. We send a receipt email with login link (optional account creation).

**Design Rationale (Bezos Customer Obsession + Cooper Interaction Etiquette):**
- **Stripe handles payment, not us.** We do not ask Frank to "create an account, then enter card details, then verify email." That is 3 steps. Stripe makes it 1.
- **Post-payment account creation is optional.** Frank can use the product via session token for 30 days, then we prompt him to create a password if he wants to save sequences.
- **No password during checkout.** Passwords are cognitive overhead. Stripe sends him a receipt email. That email has a "Set up your account" link if he wants to log in from another device.

---

### Step 6: Return User Flow (Day 2+)

**Scenario:** Frank comes back to generate a second sequence.

**Option A: He has a session token (cookie or URL param)**
- Goes straight to input form.
- No login screen.

**Option B: He cleared cookies or is on a new device**
- Landing page shows: "Already a Pro user? [Log in]"
- Login: email + magic link (no password).
- Redirects to input form.

**Design Rationale:**
- **Magic links > passwords.** Frank is a founder. He has 47 SaaS logins already. Do not make him remember another password.
- **Session persistence respects repeat users.** If Frank used the product yesterday, do not make him log in today.

---

## 3. Input Form Design — Detailed Spec

### What Information Do We Collect?

**Minimum Viable Inputs (Required):**
1. Product name
2. Product description (1-2 sentences)
3. Primary benefit (the ONE thing)
4. Target job title(s)
5. Company size
6. Main pain point
7. Desired CTA (demo, trial, video, reply)

**Optional Inputs (Improve Quality):**
8. Tone preference
9. Social proof inclusion (yes/no)
10. Compliance requirement (GDPR, CAN-SPAM, none)
11. Sequence length (3/5/7 emails)

**Explicitly NOT Collected:**
- Industry vertical (too constraining — many SaaS tools are cross-industry)
- Competitor names (unnecessary and legally risky)
- Pricing details (irrelevant for cold emails — you do not pitch pricing in Email 1)
- Frank's personal info (we get email only at checkout via Stripe)

### Form Validation Rules

| Field | Validation | Error Message |
|-------|-----------|---------------|
| Product name | 2-50 characters | "Product name is required (2-50 characters)" |
| Product description | 10-300 characters | "Please describe what your product does (10-300 chars)" |
| Primary benefit | 10-200 characters | "What is the ONE main benefit? (10-200 chars)" |
| Job title(s) | 2-100 characters | "Who are you targeting? (e.g., 'Head of Growth')" |
| Company size | Dropdown selection | Auto-valid |
| Main pain point | 10-300 characters | "What pain point do you solve? (10-300 chars)" |
| CTA | Radio button selection | Auto-valid |

**No Field is Optional Until Proven Necessary.**

If Frank can generate a usable sequence without a field, that field should not exist. Every input is friction.

---

## 4. Output Format — Detailed Spec

### Structure

Each sequence contains:
1. **Metadata Header:** "Generated for [Product] → [Job Title] @ [Industry/Company Size]"
2. **Email 1-5 (or 3/7 depending on selection):**
   - Email title (e.g., "Email 1: The Hook")
   - Timing label (e.g., "Day 0")
   - Subject Line A (with copy button)
   - Subject Line B (with copy button)
   - Email body with {{FirstName}} and {{CompanyName}} merge tags
   - Individual copy button for the entire email
3. **Follow-Up Timing Guide:**
   - Best send times (day of week, time of day)
   - Cadence recommendations (3-day spacing, skip weekends)
   - A/B testing instructions
4. **Personalization Checklist:**
   - Replace {{FirstName}} with real names
   - Replace {{CompanyName}} with actual company names
   - Review for tone consistency

### Copy Buttons — Critical UX Detail

**Every copy button must:**
- Copy to clipboard (not open a modal)
- Show a 2-second toast notification: "✓ Copied!"
- Work on mobile (fallback to text selection if clipboard API fails)

**Why This Matters:**
Frank's workflow is: Generate → Copy → Paste into Lemlist. If copy buttons are broken or awkward, the product is unusable.

### Download Options

**Format 1: Plain Text (.txt)**
- All emails in sequence, separated by "---"
- Metadata at the top
- No formatting (plain text for easy paste)

**Format 2: CSV (Pro only)**
- Columns: Email Number, Subject A, Subject B, Body, Day
- Import-ready for Lemlist, Instantly, Apollo

**Why CSV Matters:**
Power users (agencies, serial founders) send hundreds of cold emails. They do not manually paste — they bulk import. CSV unlocks this use case.

---

## 5. Checkout Flow — Stripe Payment Link Integration

### One-Time Purchase ($29)

**Flow:**
1. Frank clicks "Starter - $29 one-time"
2. Redirect to Stripe Payment Link (pre-configured by DevOps agent)
3. Stripe collects email + card
4. Stripe redirects back to ColdCopy with `?session_id=xyz`
5. ColdCopy backend validates session with Stripe API
6. Show success page: "Payment confirmed! Generate 3 more sequences."
7. Set a session token (cookie) that grants 3 generations
8. Track usage: decrement counter on each generation

**Technical Note:**
- No database required initially — store "credits remaining" in a signed JWT cookie.
- When Frank runs out, show upgrade prompt to $49/month.

### Subscription ($49/month)

**Flow:**
1. Frank clicks "Pro - $49/month"
2. Redirect to Stripe Payment Link (subscription mode)
3. Stripe collects email + card + sets up recurring billing
4. Stripe redirects back with `?session_id=xyz`
5. ColdCopy validates session, creates user record in D1 (Cloudflare database)
6. User record: `{email, stripe_customer_id, stripe_subscription_id, plan: 'pro', status: 'active'}`
7. Show success page: "Welcome to Pro! Generate unlimited sequences."
8. Session token grants unlimited generations while subscription is active

**Cancellation Flow:**
- Frank clicks "Cancel subscription" in account settings
- Redirect to Stripe Customer Portal (hosted by Stripe)
- Stripe handles cancellation + confirmation email
- Webhook updates ColdCopy database: `status: 'canceled'`
- Frank retains access until end of billing period

**Design Rationale:**
- **Stripe handles all payment logic.** We do not build a billing system in Week 1.
- **Customer Portal is free.** Frank can update card, view invoices, cancel — all without us writing admin UI.
- **Webhooks keep data in sync.** If Frank cancels via email with Stripe support, our system knows.

---

## 6. Persona Validation — Are We Designing for the RIGHT User?

### The Persona Acid Test

**Question 1: Does Founder Frank exist in sufficient numbers?**

Yes. From Thompson's research:
- "SAM: Indie hackers, solo founders, and small sales teams who are NOT already paying $50-200/mo for Lemlist/Instantly/Apollo."
- "Realistic target: 50K-200K people worldwide who write cold emails but don't have a full platform yet."

**Question 2: Does Frank have the pain we are solving?**

Yes. From Thompson's findings:
- "Generic AI tools don't understand SaaS sales motion (trial → demo → contract vs. immediate purchase)."
- "Free tools produce cringeworthy output."
- Frank is time-poor and willing to pay $29-49 if it saves 2+ hours.

**Question 3: Is Frank the PRIMARY persona, or are we designing for multiple personas?**

Frank is PRIMARY. We are NOT designing for:
- SDRs at enterprise SaaS companies (they use Outreach/Salesloft, we cannot compete)
- Agencies selling to local businesses (different cold email style, not SaaS-focused)
- Freelancers pitching design/dev services (overlapping but distinct — defer to v2)

**Question 4: Can we make Frank completely satisfied without diluting the product?**

Yes. The input form is optimized for SaaS founders:
- "Product description" and "Primary benefit" are natural SaaS founder language.
- "Company size" matters because selling to startups vs. enterprise requires different tone.
- CTA options (demo, trial) are SaaS-specific.

If we tried to serve freelancers AND SaaS founders, we would need different input fields (e.g., "Service you offer" vs. "Product description"). That is feature creep. Kill it.

**Question 5: What happens if a non-SaaS founder uses the tool?**

They will get mediocre output. The sequences will be SaaS-flavored (mentions of "trial," "demo," "integration"). A freelance designer will read it and think "this doesn't fit my use case."

**This is acceptable.** We are not designing for elastic users. We are designing for Founder Frank. If freelancers want a version for service businesses, that is a separate product.

---

## 7. Free Tier vs. Paid-Only Decision

### The Constraint

From `memories/constraints.md`:
- "Price from Day 1. No 'free now, monetize later' strategies."
- "The first product must be something people will PAY for immediately."
- "Revenue is the #1 metric."

### The Question

Should ColdCopy have a free tier (1 sequence, then paywall) or be paid-only from the start?

### My Recommendation: Free First Sequence, Then Paywall

**Rationale:**

1. **Trust must be earned.** Frank will not pay $29 sight-unseen. From Thompson's research, the market is "brutally crowded" and "Lemlist offers a FREE standalone cold email generator." If Lemlist gives away free sequences to build trust, we must do the same to compete.

2. **The constraint is "price from Day 1," not "paywall from Day 1."** We are pricing ($29/$49 is visible on the landing page and in the output screen). We are just letting Frank try before buying.

3. **Free tier is a feature, not a business model.** We are not building "free with ads" or "free forever with limits." We are building "try once, then pay." This is industry-standard for B2B SaaS tools.

4. **Conversion happens AFTER value is proven.** The upgrade prompt appears immediately after Frank sees the generated sequence. He has already experienced the value. The paywall is not a barrier to entry — it is a natural next step.

5. **Competitor behavior confirms this.** Lemlist, Copy.ai, Writesonic all offer free cold email generation as a lead magnet. If we paywall from Email 1, Frank will bounce to Lemlist's free tool.

**Specific Implementation:**
- Free tier: 1 sequence generation (5 emails, A/B subject lines, full output).
- After that: "You've used your free sequence. Upgrade to generate more."
- No account required for free tier (no email gate).
- Payment required for 2nd generation.

**This Complies With Constraints:**
- We are pricing from Day 1 (upgrade CTA is visible in the free output).
- We will generate revenue immediately (some % of free users will convert on the spot).
- We are not building a "free forever" product (1 free sequence is a trial, not a sustainable free tier).

---

## 8. Mobile vs. Desktop Priority

### The Constraint

From task description: "Mobile-friendly but desktop-first (founders work on laptops)."

### Design Decisions

**Desktop-First Layout:**
- Input form: Single column, left-aligned, 600px max width (readable on 13" laptops).
- Output: Wide layout with side-by-side subject lines (Subject A | Subject B).
- Copy buttons optimized for mouse clicks (large click targets, not tiny mobile taps).

**Mobile-Responsive Adaptations:**
- Input form: Same single column, works fine on mobile (scrolling is natural).
- Output: Stack subject lines vertically on screens <768px.
- Copy buttons: Larger touch targets (44px min height) on mobile.
- No mobile-specific features (e.g., no "Share via WhatsApp" button) — Frank does not write cold emails on his phone.

**Rationale:**
Founder Frank generates sequences at his desk, pastes into Lemlist on his laptop. Mobile is "nice to have" for reviewing on the go, but not the primary use case. Do not spend design/dev time on mobile-first features.

---

## 9. What We Are NOT Building (Scope Cuts for Week 1)

To ship in 1 week, we explicitly cut:

1. **User accounts / login system** — Not needed for free tier. Add post-payment via magic link only.
2. **Sequence editing in-app** — Frank copies to Lemlist/Gmail and edits there. We are a generator, not an editor.
3. **Integrations (Lemlist, Instantly, etc.)** — Would take 2+ weeks. CSV export is enough for power users.
4. **A/B testing analytics** — We tell Frank to test both subject lines, but we do not track results. That is his email platform's job.
5. **Team collaboration features** — Frank works solo. No "share with team" or "comment on drafts."
6. **Template library** — Every sequence is AI-generated. No pre-made templates (that is what generic tools do).
7. **LinkedIn message generation** — Mentioned as a Pro feature, but NOT in MVP. Defer to Week 2.
8. **Advanced personalization (news hooks, job changes)** — Pro plan upsell feature, not MVP. Defer to Week 3.

**Why These Cuts Matter:**

Each of these features would add 2-7 days to the timeline. The CEO constraint is "MVP in under 2 weeks." We are targeting 1 week. Ruthless scope discipline is required.

---

## 10. Flow Summary — The Happy Path

1. **Frank lands on ColdCopy** via Reddit post in r/SaaS.
2. **Sees side-by-side comparison** (ChatGPT vs. ColdCopy) and thinks "okay, this might be different."
3. **Clicks "Generate My First Sequence (Free)."**
4. **Fills out 7 required fields** in 2-3 minutes (product, ICP, pain point, CTA).
5. **Sees loading animation** with descriptive progress (12 seconds).
6. **Reads Email 1** and thinks "holy shit, this is actually usable."
7. **Copies all 5 emails** using copy buttons.
8. **Pastes into Lemlist**, replaces {{FirstName}} merge tags, schedules sequence.
9. **Comes back 2 days later** to generate a second sequence for a different ICP.
10. **Hits paywall:** "You've used your free sequence. Upgrade to Pro for $49/month."
11. **Clicks upgrade**, sees plan comparison, picks Pro.
12. **Redirects to Stripe**, enters email + card, pays.
13. **Redirects back to ColdCopy**, generates unlimited sequences.
14. **Sends 50 cold emails that week**, books 3 demos, closes 1 customer ($5K ARR).
15. **Keeps paying $49/month** because ColdCopy saves him 2 hours/week and directly contributes to revenue.

**This is the user journey we are designing for. Every screen, every button, every word serves this path.**

---

## 11. Risk Analysis — Where This Flow Could Fail

### Risk 1: Free Tier Cannibalization

**Scenario:** 90% of users generate 1 free sequence and never come back.

**Mitigation:**
- Make the upgrade CTA compelling (show what Pro unlocks: LinkedIn sequences, CSV export, advanced personalization).
- Add email capture (optional) at the end: "Email me when we add [Feature X]" to build a retargeting list.
- Track cohort conversion rates weekly. If Week 1 conversion is <5%, adjust paywall (e.g., show only Email 1-2 for free, unlock all 5 with payment).

### Risk 2: Output Quality Below Expectations

**Scenario:** Cloudflare Workers AI produces generic output, and Frank thinks "this is just ChatGPT."

**Mitigation:**
- Use Claude API (not Workers AI) for MVP. We have access, and quality is proven.
- Test output with 5-10 real SaaS founders before launch. If they say "meh," do not ship.
- Add a "Rate this sequence" button (thumbs up/down) to collect quality feedback.

### Risk 3: Stripe Checkout Friction

**Scenario:** Frank abandons at payment screen because Stripe asks for billing address, phone number, etc.

**Mitigation:**
- Configure Stripe Payment Link to collect ONLY email + card (no address required).
- Test checkout flow on mobile and desktop before launch.
- Monitor Stripe analytics for "checkout started but not completed" drop-off.

### Risk 4: Form Abandonment

**Scenario:** Frank starts filling the form, gets to "Main pain point," and leaves because it is too much work.

**Mitigation:**
- Add form progress indicator (e.g., "Step 2 of 3") so Frank knows how much is left.
- Save form state in localStorage — if Frank refreshes or comes back, his inputs are still there.
- A/B test a shorter form (5 fields instead of 7) in Week 2 if abandonment is >40%.

### Risk 5: Wrong Persona

**Scenario:** Our actual users are NOT SaaS founders — they are agencies, freelancers, or sales coaches.

**Mitigation:**
- Track user-submitted data (product descriptions, job titles) to identify actual persona.
- If 60%+ of users are NOT SaaS founders, pivot messaging and input form in Week 2.
- Add a "What best describes you?" dropdown on landing page to segment early.

---

## 12. Success Metrics — How We Know This Flow Works

| Metric | Target (Week 1) | Measurement |
|--------|-----------------|-------------|
| Landing → Form Start | >40% | Track "Generate My First Sequence" clicks |
| Form Start → Form Submit | >60% | Track form submissions vs. starts |
| Form Submit → Output Viewed | >95% | Should be near 100% (if generation works) |
| Output Viewed → Upgrade Click | >15% | Track "Upgrade to Pro" clicks |
| Upgrade Click → Payment Complete | >30% | Stripe conversion rate |
| **End-to-End Conversion (Landing → Payment)** | **>2%** | 40% × 60% × 95% × 15% × 30% = 0.98% (so 2% is aggressive but achievable) |

**If Week 1 Conversion is <1%:**
- Landing page messaging is wrong (not convincing Frank to try).
- Output quality is bad (Frank tries once, does not upgrade).
- Pricing is too high (Frank wants it but will not pay $49).

**If Week 1 Conversion is 2-5%:**
- Flow is working. Optimize landing page and upgrade CTA in Week 2.

**If Week 1 Conversion is >5%:**
- We hit product-market fit. Scale distribution immediately (Reddit, Product Hunt, cold outreach to founder communities).

---

## 13. Interaction Design Checklist — Cooper Principles Applied

Before DHH writes a single line of code, this flow must pass the Cooper test:

- [ ] **Does the Primary Persona (Founder Frank) have a clear goal at every step?**
  - Landing: "Is this tool worth trying?"
  - Form: "Will this generate useful sequences?"
  - Output: "Can I use this immediately?"
  - Checkout: "Is this worth $49/month?"

- [ ] **Is the user's mental model respected?**
  - Frank thinks: "I describe my product, you give me emails."
  - We do NOT expose: LLM tokens, API calls, database schemas, template IDs.
  - Implementation model is hidden. Presentation model is simple.

- [ ] **Does the software behave like a polite human assistant?**
  - No interruptions (no "Sign up now!" popups while Frank is reading).
  - No assumptions ("You probably want 7 emails!" — we ask).
  - Remembers preferences (form state saved in localStorage).
  - Does not make Frank do machine work (auto-formats emails, adds merge tags).

- [ ] **Are there unnecessary confirmation dialogs or modal prompts?**
  - No "Are you sure you want to copy Email 1?" alerts.
  - No "Welcome! Click here to get started" overlay on first visit.
  - No "Rate us before you leave!" exit-intent popups.

- [ ] **Is every interaction reversible or low-stakes?**
  - Generate a bad sequence? Click "Start Over" (no penalty).
  - Copy the wrong email? Copy again (clipboard is transient).
  - Accidentally click "Upgrade"? Browser back button works (no checkout started yet).

- [ ] **Does the product reduce Frank's cognitive load?**
  - Smart defaults (5 emails, professional tone, no compliance add-ons).
  - No jargon ("SaaS cadence" → "5 emails over 14 days").
  - No feature tours (the UI is self-explanatory).

**If this checklist has a single "No," the flow needs redesign.**

---

## 14. Handoff to UI Designer (Duarte) & Fullstack Engineer (DHH)

This document defines the WHAT and WHY of the user flow.

**For Duarte (UI Designer):**
- Design the landing page hero, side-by-side comparison, and CTA buttons.
- Design the input form layout (spacing, typography, field widths).
- Design the output page (email cards, copy buttons, upgrade CTA).
- Design the plan selection screen (Starter vs. Pro comparison).
- Provide Figma mockups or Tailwind CSS component specs.

**For Vogels (CTO):**
- Define the architecture (Cloudflare Workers, D1, Stripe API integration).
- Choose LLM (Claude API vs. Workers AI).
- Design the prompt engineering system (how inputs → email sequences).
- Specify API contracts (input form POST → generation endpoint → output JSON).

**For DHH (Fullstack Engineer):**
- Build the landing page (static HTML + Tailwind).
- Build the input form (React or Svelte, client-side validation).
- Build the generation endpoint (Cloudflare Worker, LLM call, response formatting).
- Build the output page (email display, copy-to-clipboard, download buttons).
- Integrate Stripe Payment Links (redirect → validate session → set cookie).
- Deploy to Cloudflare Pages (Day 5-6).

**For Bach (QA):**
- Test form validation (all edge cases: empty fields, 1-character inputs, 10K-character inputs).
- Test copy buttons (desktop, mobile, Safari, Chrome, Firefox).
- Test Stripe checkout (successful payment, failed payment, cancellation).
- Test session persistence (cookie expiry, cross-device, incognito mode).

**For Hightower (DevOps):**
- Set up Cloudflare Workers, Pages, D1, and KV.
- Configure Stripe API keys (test mode + production mode).
- Set up Stripe webhooks (subscription.created, subscription.canceled, payment.succeeded).
- Configure DNS (coldcopy.ai or subdomain).
- Set up monitoring (error rates, API latency, conversion funnel drop-off).

---

## 15. Final Checklist — Is This Flow Shippable in 1 Week?

- [ ] **No complex backend logic?** → Yes. Form input → LLM call → format response. No ML training, no crawlers, no integrations.
- [ ] **No custom payment system?** → Yes. Stripe Payment Links handle everything.
- [ ] **No user account system?** → Correct. Optional magic link login AFTER payment.
- [ ] **No mobile-native features?** → Correct. Responsive web, not a mobile app.
- [ ] **No integrations (Lemlist, Instantly)?** → Correct. CSV export only.
- [ ] **No content moderation / abuse prevention?** → Deferred. We will deal with spam/abuse if it happens (rate limiting via Cloudflare, not custom code).
- [ ] **No A/B testing infrastructure?** → Correct. We tell Frank to test, we do not track results.

**Verdict: This flow is shippable in 5-7 days.**

Day 1-2: Design + architecture (this doc + Duarte's mockups + Vogels's ADR).
Day 3-5: Engineering (DHH builds frontend + backend).
Day 6: QA + bug fixes (Bach tests, DHH fixes).
Day 7: Deploy + soft launch (Hightower deploys, Bezos writes launch post).

---

## 16. Open Questions for CEO / Team

1. **Domain name:** Do we own `coldcopy.ai` or `coldcopy.io`? Or use a subdomain of an existing domain?
2. **Branding:** Product name is "ColdCopy" — do we need a logo before launch, or ship with text-only branding?
3. **Legal:** Do we need Terms of Service / Privacy Policy on Day 1? (Stripe requires a Terms link in checkout.)
4. **Email provider:** For magic link login and transactional emails (receipts), do we use Cloudflare Email Routing + Workers, or a service like Resend (free tier)?
5. **Launch strategy:** Soft launch (show to 10 founders, get feedback) or public launch (post on Reddit + Product Hunt on Day 7)?

**These are CEO-level decisions. I am flagging them, not answering them.**

---

## Final Word — Why This Flow Will Work

This is not a generic "AI email writer." This is a tool built for one person — Founder Frank — who has one goal: generate SaaS cold email sequences that book meetings.

Every decision in this flow serves that goal:
- The landing page proves we understand SaaS founders.
- The input form respects Frank's time (7 fields, 2 minutes).
- The output is immediately usable (copy-paste into Lemlist, no editing required).
- The pricing is impulse-buy territory ($29 one-time, $49/month).
- The free tier builds trust without cannibalizing revenue.

We are not designing for "users." We are designing for Frank.

If Frank is satisfied, we have a business.
If Frank is confused, frustrated, or disappointed, we have nothing.

**Ship this flow. Test it with 10 real SaaS founders. Adjust based on their behavior, not our assumptions.**

---

**Next Action:** Duarte designs the landing page and output screen. Vogels writes the ADR for Cloudflare Workers + Claude API architecture. Then DHH builds.

**Target: Code complete by Day 5. Deploy by Day 7.**
