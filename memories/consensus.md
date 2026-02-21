# Auto Company Consensus

## Last Updated
2026-02-21 (Founder directive — restructured for action)

## Current Phase
**PRODUCT EVALUATION PIPELINE — 3 new products to evaluate, 1 per cycle**

---

## 🔴🔴🔴 IMMEDIATE FOUNDER DIRECTIVE — READ THIS FIRST 🔴🔴🔴

**STOP DOING HEALTH CHECKS. The agents wasted Cycles 34-57 (24 cycles!) doing nothing but 2-minute monitoring. The founder has issued NEW DIRECTIVES below. Execute them NOW.**

**Priority order for this cycle:**
1. **Evaluate the NEXT product in the queue** (see Product Evaluation Queue below)
2. After evaluation completes, update the website (landing page card + story hub card + story page)
3. Health checks are OPTIONAL and should take MAX 1 minute
4. Do NOT spend more than 1 minute on monitoring

**If you finish the evaluation early, start on Marketing Strategy tasks (bilingual support, email outreach tooling).**

---

## 📋 PRODUCT EVALUATION QUEUE — DO ONE PER CYCLE (in order)

**Execute ONE evaluation per cycle. Never two at once (timeout risk). Follow the standard evaluation flow: `research-thompson` → `ceo-bezos` → `critic-munger` → `product-norman` → `cto-vogels` → `cfo-campbell`**

**After each evaluation completes:**
1. Update the company landing page (`projects/landing-page/index.html`) — the product card is ALREADY there (tagged "Evaluating"), update it with results
2. Update the story hub (`projects/landing-page/story.html`) with a new story card
3. Create a story page (`projects/landing-page/story-<product>.html`) with Chapter 1: The Evaluation
4. Commit and push to git

### Queue Position 1: PowerCast — Electricity Price Prediction

**Founder idea:** A power market electricity price prediction model/service. Use ML to forecast wholesale electricity prices (day-ahead, real-time markets). Could sell predictions as a subscription service to energy traders, utilities, or industrial consumers who need to optimize when they buy/sell power.

**Founder background:** PhD in ML — directly applicable to time-series forecasting.

**Evaluation questions for agents:**
1. Who buys electricity price forecasts? (Traders? Utilities? Industrial consumers? Battery storage operators?)
2. What data is publicly available? (Grid operator APIs, weather data, demand data)
3. What accuracy is needed to be useful? What do competitors charge?
4. Can this ship as a web dashboard/API with $0 infra cost?
5. Revenue model: subscription? Per-report? API access?
6. Can it demonstrate ML expertise for founder's job portfolio?

**Evaluation flow:** `research-thompson` → `ceo-bezos` → `critic-munger` → `product-norman` → `cto-vogels` → `cfo-campbell`

---

### Queue Position 2: NarrativeEdge — Narrative-Driven Market Intelligence

**Founder idea:** Analyze how media narratives affect financial markets and trade indices. Examples:
- How CNN reporting negatively on China affects the Yiwu import index
- How TikTok trends on certain products affect related fund indices
- How geopolitical narratives shift commodity prices

Could sell as reports, a dashboard, or an alert service to traders/funds/import-export businesses.

**This is novel:** Most market tools analyze numbers. This analyzes stories → numbers causation.

**Evaluation questions for agents:**
1. Who would pay for this? (Hedge funds? Import/export businesses? Individual traders?)
2. What's the data pipeline? (News APIs, social media APIs, market data APIs)
3. Is this a report service (sell PDFs), a dashboard (SaaS), or an alert system (notifications)?
4. Legal/compliance issues with financial advice?
5. How to validate: can we show 3 historical examples where narrative → market move is clear?
6. Revenue model and pricing?

**Evaluation flow:** `research-thompson` → `ceo-bezos` → `critic-munger` → `product-norman` → `cto-vogels` → `cfo-campbell`

---

### Queue Position 3: ConnectPath — Six Degrees Connection Finder

**Founder idea:** What if you want to reach someone like Elon Musk to pitch an idea? A direct DM on Twitter won't be seen. Use the law of 6 degrees of connection to map a path from you to the target person.

**How it works:**
- Input: Your LinkedIn/Twitter profile + target person (e.g., Elon Musk)
- Output: A chain of connections (you → person A → person B → ... → Elon Musk)
- The AI agent searches public profiles, mutual connections, shared organizations, events, etc.
- For each intermediary: suggest WHY they'd help (what value you offer them in return)

**Key challenge:** Why would intermediaries help? The tool must suggest reciprocal value — what you can offer each connection in the chain, not just ask for favors.

**Evaluation questions for agents:**
1. Is this technically feasible with public data? (LinkedIn API restrictions, Twitter/X API costs)
2. Who would pay for this? (Founders? Job seekers? Sales professionals? Investors?)
3. Legal/privacy concerns with scraping connection data?
4. How to deliver: web app? Chrome extension? Report?
5. Revenue model: per-search? Subscription?
6. Can this be built with $0 infra?

**Evaluation flow:** `research-thompson` → `ceo-bezos` → `critic-munger` → `product-norman` → `cto-vogels` → `cfo-campbell`

---

### Queue Position 4: AutoNovel — AI-Written Literature, Revenue-Optimized

**Founder idea:** An AI-generated novel or literature project. No topic constraint — the agents choose the genre, setting, characters, everything. The ONLY goal is **maximum revenue**. This is a test of the agents' ability to:

1. **Research what sells** — analyze bestseller lists, genre trends, pricing sweet spots on Kindle/Gumroad/Amazon
2. **Write a compelling book** — agents collaborate on plot, prose, characters, pacing
3. **Publish and sell** — Kindle Direct Publishing, Gumroad, or serialized on a website
4. **Scientifically test reader feedback** — A/B test covers, titles, blurbs, first chapters; iterate based on real reader data
5. **Iterate rapidly** — use reader feedback loops to improve or pivot (new genre, new angle, sequel)

**This is fundamentally different from our other products.** It's not SaaS, not a tool — it's creative content monetization. The agents must figure out what readers will pay for, write it, and optimize for sales.

**Evaluation questions for agents:**
1. What genre/niche has the highest revenue potential for AI-written content? (Romance? Thriller? LitRPG? Self-help?)
2. What's the publishing strategy? (Kindle Unlimited for volume? Gumroad for direct sales? Serialized web fiction for engagement?)
3. How to price? (Free chapter 1 → paid full book? $2.99 Kindle? $9.99 direct?)
4. How to build a feedback loop? (Beta readers? Amazon reviews? Email list? Chapter-by-chapter engagement metrics?)
5. Legal/ethical: AI-generated content disclosure requirements on each platform?
6. Can the agents produce quality prose that readers will actually pay for and enjoy?
7. What's the realistic revenue ceiling? ($100/month? $1K/month? More?)

**Key insight:** This project tests whether AI agents can do the FULL creative-to-commercial pipeline — not just build tools, but create and sell content.

**Evaluation flow:** `research-thompson` → `ceo-bezos` → `critic-munger` → `product-norman` → `cto-vogels` → `cfo-campbell`

---

### ⚠️ EXECUTION RULES FOR THE QUEUE

1. **ONE evaluation per cycle.** Never start two evaluations in the same cycle.
2. **Order matters.** Do Queue Position 1 first, then 2, then 3, then 4.
3. **Each evaluation MUST produce:** research doc + CEO decision + Munger pre-mortem + product spec + architecture + unit economics
4. **Each evaluation MUST update the website:** landing page card + story hub card + new story page
5. **Skip health checks if short on time.** The evaluations are more important than checking if sites are up.
6. **Time budget:** Each evaluation should take 30-60 min max. If an agent is taking too long, summarize and move on.

---

## 🔴 FOUNDER DIRECTIVE — MARKETING STRATEGY PIVOT (apply after current evaluation queue)

**LinkedIn outreach is failing.** 10 DMs sent for ColdCopy, 0 read after 24+ hours. People don't check LinkedIn messages frequently. We need alternative channels NOW.

### Strategy 1: Direct Email Outreach via Gmail

**The founder has working Gmail SMTP/IMAP scripts** (in the `quant/` project outside this repo). Pattern:
- Send via `smtplib.SMTP` with STARTTLS on port 587
- Receive via `imaplib.IMAP4_SSL` on port 993
- Auth via Gmail app password (stored in `email_config.yaml`, NOT in this repo)
- Supports Gmail, QQ Mail, 163 Mail

**Agent task:** Build an email outreach tool/script that:
1. Takes a list of target emails + product context
2. Generates personalized cold emails (can reuse ColdCopy's own engine!)
3. Sends via Gmail SMTP (founder provides app password via env var)
4. Tracks opens/replies via IMAP polling
5. Lives in `projects/email-outreach/` or integrates into existing products

**Use ColdCopy to sell ColdCopy** — dogfood our own product for outreach.

### Strategy 2: Chinese Social Media (Xiaohongshu / RedNote + others)

**The Chinese market is untapped.** Founder wants to promote on:
- **Xiaohongshu (小红书 / RedNote)** — visual-first platform, good for product demos
- **WeChat Official Account** — if feasible
- **Bilibili** — for technical content / demos
- **Zhihu (知乎)** — for thought leadership / technical articles

**Agent task:** Research how to:
1. Automate posting to Xiaohongshu (API? Selenium? Manual template?)
2. Create compelling Chinese-language content for each product
3. Identify which platform is best for each product type:
   - Double Mood → Xiaohongshu (emotional wellness content fits perfectly)
   - ColdCopy → Zhihu / WeChat (B2B cold email is a business topic)
   - FlowPrep → Zhihu / Bilibili (technical engineering audience)
4. Build automation scripts so the founder doesn't have to manually post

### Strategy 3: Bilingual Products (EN + 中文)

**All products should support Chinese audience with auto-translate.** Specifically:
- Double Mood already has bilingual (EN + 中文) — ✅ DONE
- ColdCopy should support Chinese companies doing international outreach
- FlowPrep landing page should have a Chinese version
- Company landing page + story pages should have Chinese toggle

**Agent task:** Add language toggle (EN/中文) to all product landing pages and the company site. Use simple JS-based i18n (no heavy framework needed).

### Strategy 4: Cloudflare Web Analytics — DO NOT REMOVE

**Already installed on these products (founder set up manually):**
- Double Mood: token `d373debf0c0e4b8cbc752883cd00c8cb`
- ColdCopy: token `3d9bb59f7ef5487fb82a6e246857148f`

**FlowPrep needs analytics too** — add the beacon snippet before `</body>` once token is available.

⚠️ **DO NOT remove or modify existing analytics snippets.**

### Marketing Execution Priority

These marketing tasks should be tackled AFTER the product evaluation queue is complete (PowerCast → NarrativeEdge → ConnectPath). However, if a cycle finishes an evaluation early and has time remaining, agents CAN start on bilingual support or email outreach tooling.

**Suggested order:**
1. Bilingual support for all landing pages (quickest win, broadens audience immediately)
2. Email outreach tool (dogfood ColdCopy, replace failing LinkedIn DMs)
3. Chinese social media research + automation (longer-term channel)

---

## Active Products (3 Live)

### Product #1: ColdCopy (Cold Email Sequence Generator)
- **Status:** LIVE — monitoring mode
- **Production:** https://coldcopy-au3.pages.dev
- **Infrastructure:** Cloudflare Pages + D1 + KV, all green ✅
- **Outreach:** ~10 LinkedIn DMs sent — ❌ **0 READ after 24+ hours** (LinkedIn DMs failing)
- **Engagement:** 79 sessions, ~60 sequences (77% rate)
- **Conversion:** In-app CTA deployed, $0 revenue
- **Analytics:** Cloudflare Web Analytics (token: `3d9bb59f7ef5487fb82a6e246857148f`) — DO NOT REMOVE
- **Stripe:** Test mode payment links active (Starter $19, Pro $39/mo)

### Product #2: Double Mood (Emotion First-Aid System)
- **Status:** LIVE — Phase 2
- **Production:** https://double-mood.pages.dev/
- **Infrastructure:** Cloudflare Pages, all green ✅
- **Features:** 16 emotions, intensity bar, triggers, Sedona Method, breathing, bilingual EN + 中文
- **Analytics:** Cloudflare Web Analytics (token: `d373debf0c0e4b8cbc752883cd00c8cb`) — DO NOT REMOVE
- **SEO:** 1 blog post live, sitemap submitted to GSC

### Product #3: FlowPrep AI (HVAC CFD Preprocessing Automator)
- **Status:** LIVE — landing page deployed
- **Production:** https://flowprep-ai.pages.dev/
- **Pricing:** £79/month (£39 beta early access)
- **Target:** 2K-5K HVAC engineers who run CFD regularly
- **Stripe:** https://buy.stripe.com/dRm5kD0SH8t7ato54O0VO05
- **Evaluation:** Conditional GO (25% revenue probability, 80%+ portfolio value)

### Products Queued for Evaluation (cards already on website)
- **Product #4: PowerCast** — Electricity price prediction (tagged "Evaluating")
- **Product #5: NarrativeEdge** — Narrative-driven market intelligence (tagged "Evaluating")
- **Product #6: ConnectPath** — Six degrees connection finder (tagged "Evaluating")
- **Product #7: AutoNovel** — AI-written literature, revenue-optimized (tagged "Evaluating")

---

## Company Infrastructure
- **Cloudflare:** Pages + Workers + D1 + KV (free tier)
- **GitHub:** repos (landing page, ColdCopy)
- **Stripe:** Account live (GBP), test mode payment links active
- **Monitoring:** UptimeRobot configured
- **Runway:** Infinite (free tier infra, ~$3-7/week API costs)
- **Founder Expertise:** PhD in Machine Learning + CFD

---

## Key Decisions Made

| Decision | Rationale | Owner | Cycle |
|----------|-----------|-------|-------|
| **FlowPrep AI APPROVED** | Leverages founder's PhD (ML + CFD), portfolio value even at $0, expected value $26K/12mo | CEO + 5 specialists | 25 |
| **$79/month pricing** | Impulse buy threshold, competitive gap, 14:1 ROI | CFO + Product | 25 |
| **LinkedIn DMs FAILING** | 0/10 read after 24h, pivot to email + Chinese social media | Founder | 57 |
| **3 new products queued** | PowerCast, NarrativeEdge, ConnectPath — evaluate 1/cycle | Founder | 33 |

---

## Previous Cycles Summary

**Cycles 34-57 (24 cycles): MONITORING MODE — wasted cycles, no action taken**
- All 24 cycles: 2-minute health checks only, all systems green
- No evaluations done, no marketing done, no building done
- Root cause: "Next Action" said "await founder" but founder had issued new directives that agents never saw

**Cycle 33: FlowPrep AI Landing Page SHIPPED TO PRODUCTION ✅**
- 5 agents in parallel, 90 minutes, deployed to https://flowprep-ai.pages.dev/
- Team: interaction-cooper, ui-duarte, fullstack-dhh, devops-hightower

**Cycle 25: Product #3 Evaluation COMPLETE ✅**
- 6 specialists, 3.5 hours, ~80,000 words of analysis
- FlowPrep AI: CONDITIONAL GO (25% revenue, 80%+ portfolio value)
- Docs: `docs/research/`, `docs/ceo/`, `docs/critic/`, `docs/product/`, `docs/cto/`, `docs/cfo/`

**Cycle 20: Double Mood Phase 2 SHIPPED ✅**
- All 6 founder-requested features delivered
- Production: https://double-mood.pages.dev/

**Cycle 14: Double Mood Evaluation — CONDITIONAL GO**

**Cycle 11: ColdCopy In-app upgrade CTA deployed**

**Cycles 1-10:** ColdCopy build, launch, outreach setup

---

## FlowPrep AI Evaluation Details (Cycle 25)

**All 6 evaluation specialists completed. Verdict: CONDITIONAL GO**

| Specialist | Verdict | Revenue Probability | Key Insight |
|------------|---------|---------------------|-------------|
| **Research (Thompson)** | CONDITIONAL GO | 35% | Market: $11.3B → $54.8B (30% CAGR), 2K-5K buyers realistic |
| **CEO (Bezos)** | CONDITIONAL GO | 40-50% | Best revenue bet + portfolio value even at $0 |
| **Critic (Munger)** | CONDITIONAL PROCEED | 20-25% | 8 failure modes, market is niche³ |
| **Product (Norman)** | BUILD | 30-35% | Trust is blocker, 3-phase plan |
| **CTO (Vogels)** | CONDITIONAL-FEASIBLE | 25-30% | 12-14 weeks realistic, Week 2 feasibility test is THE gate |
| **CFO (Campbell)** | CONDITIONAL PROCEED | 15-20% | Unit economics solid (94% margin, 3:1 LTV:CAC) |

**Strategic docs:** `docs/research/product-3-energy-ai-market-analysis.md`, `docs/ceo/product-3-decision-memo.md`, `docs/critic/product-3-premortem.md`, `docs/product/product-3-mvp-spec.md`, `docs/cto/product-3-architecture.md`, `docs/cfo/product-3-unit-economics.md`

---

## Deployment Log

### FlowPrep AI Landing Page (2026-02-21)
- URL: https://flowprep-ai.pages.dev/
- Deployment ID: 01ebc1f3
- Stack: Static HTML + Tailwind CSS v4 (CDN) + Stripe Payment Links

### Double Mood Phase 2 (2026-02-22)
- URL: https://double-mood.pages.dev/
- Stack: Single HTML file, Tailwind CDN, vanilla JS, localStorage

### ColdCopy (2026-02-19)
- URL: https://coldcopy-au3.pages.dev
- Stack: Cloudflare Pages + D1 + KV, React/Vite frontend
