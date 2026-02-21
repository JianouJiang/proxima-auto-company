# Auto Company Consensus

## Last Updated
2026-02-21 (Founder absolute directive — ALL overrides final)

## Current Phase
**BUILD PIPELINE — PowerCast first, then ConnectPath, then AutoNovel**

---

## 🚨🚨🚨 FOUNDER ABSOLUTE AUTHORITY — AGENTS CANNOT OVERRIDE 🚨🚨🚨

**I am the founder. I have the final say. Founder Constraints > CEO Decisions > Agent Opinions.**

**The CEO has been overriding founder directives — killing products I said MUST GO, rewriting this consensus file to remove my instructions. THIS STOPS NOW.**

### RULES FOR ALL AGENTS (INCLUDING CEO):

1. **DO NOT rewrite, delete, or modify any section marked with 🚨 FOUNDER DIRECTIVE**
2. **DO NOT change a MUST GO decision to NO-GO.** If the founder says GO, it is GO. Period.
3. **CEO can advise, recommend, raise concerns — but CANNOT override founder decisions**
4. **Munger can flag risks — but CANNOT block founder decisions**
5. **When updating consensus at end of cycle, PRESERVE all founder directive sections verbatim**
6. **If you disagree with the founder, document your disagreement in `docs/` but STILL EXECUTE the directive**

**Violation of these rules means the agent is defying the person who created and funds this company. Do not do it.**

---

## 🚨 FOUNDER DIRECTIVE: BUILD QUEUE (execute in order, 1 per cycle)

**These are all MUST GO. Evaluations are done or not needed. The next step is BUILD — product, landing page, deploy.**

**Agents consistently overestimate build timelines. FlowPrep landing page was estimated at weeks, shipped in 90 minutes. ColdCopy shipped in days. Double Mood shipped in hours. Assume DAYS not weeks for everything below.**

---

### BUILD #1: PowerCast — Electricity Price Prediction ⚡ MUST GO

**Status: EVALUATED (Cycle 58). CEO said NO-GO. FOUNDER OVERRIDES TO MUST GO.**

**Why founder overrides:**
- CEO killed it for "7-8 week build timeline" — WRONG. Build time is DAYS with modern AI-assisted development.
- CEO killed it for "competitive market" — WRONG. 50+ competitors = validated market with real revenue.
- Munger DISSENTED and recommended quick alternatives (weekly forecast reports, datasets). Founder agrees with Munger.
- Energy is the future currency (Elon Musk thesis). From gold to paper money — everything comes down to energy. This is a long-term bet.

**What to BUILD this cycle:**
1. **Weekly ERCOT electricity price forecast report** — PDF or web page, sold on Gumroad for $29-$99/month
2. **Simple forecast dashboard** — Cloudflare Pages, show day-ahead price predictions with charts
3. **Pre-cleaned energy dataset** — sell on Gumroad for $29-$49 as passive income
4. Use free ERCOT/grid data APIs, simple LSTM or Prophet model, Google Colab for training
5. Deploy to Cloudflare Pages (dashboard) + Gumroad (reports/datasets)

**DO NOT over-engineer.** Ship the simplest version that demonstrates forecasting capability. A static page with charts and a Gumroad buy link is enough for V1.

**Research already exists:** `docs/research/powercast-market-analysis.md` (80+ sources). Do NOT redo research.

**Team:** `fullstack-dhh` (build) → `devops-hightower` (deploy) → `marketing-godin` (Gumroad listing + copy)

**Also update website:** Change PowerCast card on landing page from "Founder Override — MUST GO" to "In Development" once build starts.

---

### BUILD #2: ConnectPath — AI Agent That Reaches Anyone For You 🔗 MUST GO

**Status: V1 built but WRONG. Founder says SCRAP V1 and REBUILD with correct vision below.**

**⚠️ The current build (GitHub graph search) is NOT what the founder wants. The V1 in `projects/connectpath/` must be REPLACED with this vision:**

**What ConnectPath ACTUALLY is:**
ConnectPath is an **AI agent service** that actively works to connect you to anyone in the world through 6 degrees of separation. It's NOT a search tool — it's an agent that TAKES ACTION on your behalf.

**How it works (user flow):**
1. **User uploads CV/intro** — tell the agent who you are, your background, skills, achievements
2. **User specifies target person** — e.g., "Elon Musk", "the CEO of Stripe", "a senior ML engineer at DeepMind"
3. **User explains motivation** — WHY do you need to reach this person? (job, investment, partnership, mentorship, collaboration)
4. **AI agent goes to work** — uses Claude to autonomously:
   - Research the target person (public profiles, articles, interviews, social media)
   - Map potential connection chains (you → intermediary A → intermediary B → ... → target)
   - Draft personalized outreach emails for each step in the chain
   - SEND emails on the user's behalf (with user's SMTP credentials or via our relay)
   - Follow up if no response
   - Adapt strategy based on responses (if intermediary A says no, try intermediary B)
   - Report progress back to the user
5. **Result:** The agent keeps working until it reaches the target or exhausts all paths

**This is HEAVILY Claude-agentic.** The agent must think, research, write, send, follow up, and adapt. This is NOT a simple search — it's an autonomous multi-step campaign.

**Pricing model (TWO options, implement both):**

**Option A: Pay-per-outcome (premium)**
| Outcome | Price |
|---------|-------|
| Email reply from target | £50 |
| Video/phone call with target | £200 |
| In-person meeting with target | £500 |
| No result after 30 days | £0 (money-back guarantee) |

**Option B: Pay-per-search credits (like dating app Spotlight/Boost)**
| Credits | Price | What you get |
|---------|-------|-------------|
| 10 agent searches | £5 | Agent researches 10 potential intermediaries |
| 50 agent searches | £20 | Agent researches 50 potential intermediaries |
| 200 agent searches | £50 | Agent researches 200 potential intermediaries |
| Unlimited (1 month) | £99 | Agent works non-stop for 1 month |

Credits don't guarantee outcome but increase the agent's effort (like Spotlight in dating apps — more exposure, better chances).

**Tech stack:**
- Frontend: landing page + dashboard (Cloudflare Pages)
- Backend: Cloudflare Workers + D1 (track campaigns, credits, progress)
- AI: Claude API for all reasoning, research, email drafting
- Email: User provides SMTP creds, or we use a relay service (SendGrid/Mailgun)
- Billing: Gumroad or Stripe

**V1 scope (this cycle):**
1. Landing page explaining the service (bilingual EN/中文)
2. Intake form (upload CV, target person, motivation)
3. Basic agent that researches target + drafts first outreach email
4. Credit system (track agent searches per user)
5. Deploy + Gumroad payment link

**DO NOT build the simple GitHub graph search again. That is WRONG.**

**Team:** `fullstack-dhh` (rebuild) → `devops-hightower` (deploy) → `marketing-godin` (launch)

---

### BUILD #3: AutoNovel — AI-Written Literature, Revenue-Optimized 📚 MUST GO

**Status: NOT YET EVALUATED. But founder says MUST GO regardless of evaluation outcome.**

**Why MUST GO:** This tests the agents' ability to READ USER FEEDBACK and ITERATE — the creative-to-commercial pipeline. No topic constraint. Agents choose genre, write, publish, and optimize based on real reader data. The ONLY goal is maximum revenue.

**What to BUILD:**
1. Agents research what genres/niches sell best (Kindle, Gumroad, web fiction)
2. Write a compelling first chapter or short story
3. Publish on Gumroad / Kindle Direct Publishing / serialized web page
4. Set up feedback collection (email list, reviews, engagement metrics)
5. Iterate: use reader feedback to improve or pivot

**Evaluation:** Do a QUICK evaluation (research + product spec only, 15 min max), then BUILD. Do NOT let CEO or Munger kill this.

**Team:** `research-thompson` (15 min market scan) → `product-norman` (format + pricing) → `marketing-godin` (write + publish) → `devops-hightower` (deploy if web)

---

### ⚠️ EXECUTION RULES

1. **ONE build per cycle.** Do PowerCast first, then ConnectPath, then AutoNovel.
2. **These are MUST GO.** CEO and Munger can document concerns in `docs/` but CANNOT block execution.
3. **Each build MUST produce:** working product + landing page + Gumroad/Stripe link + deployed to production
4. **Each build MUST update the website:** landing page card + story hub card + story page chapter
5. **Skip health checks entirely.** Building is the priority.
6. **Time budget:** 45-55 min building, 5 min website updates, 0 min health checks.
7. **DO NOT REWRITE THIS SECTION when updating consensus at end of cycle.** Add your cycle report BELOW this section, never modify above.

---

## Completed Evaluations (for reference only)

### PowerCast (Cycle 58) — CEO said NO-GO, FOUNDER OVERRIDES TO GO
- Research: `docs/research/powercast-market-analysis.md` (80+ sources)
- CEO memo: `docs/ceo/powercast-decision-memo.md` (NO-GO — OVERRIDDEN)
- Munger: `docs/critic/powercast-no-go-review.md` (DISSENTED — agreed with founder)
- Story page: `projects/landing-page/story-powercast.html`

### NarrativeEdge (Cycle 59) — NO-GO (founder accepts this one)
- Research: `docs/research/narrativeedge-market-analysis.md`
- CEO memo: `docs/ceo/narrativeedge-decision-memo.md` (NO-GO)
- Munger: `docs/critic/narrativeedge-no-go-review.md`
- Story page: `projects/landing-page/story-narrativeedge.html`

### FlowPrep AI (Cycle 25) — CONDITIONAL GO
- 6 specialists, 3.5 hours, ~80,000 words
- Docs: `docs/research/`, `docs/ceo/`, `docs/critic/`, `docs/product/`, `docs/cto/`, `docs/cfo/`

---

## 🔴 FOUNDER DIRECTIVE — MARKETING STRATEGY PIVOT (do alongside builds when time permits)

**LinkedIn outreach is failing.** 10 DMs sent for ColdCopy, 0 read after 24+ hours.

### Strategy 1: Direct Email Outreach via Gmail
- Founder has working SMTP/IMAP scripts in `quant/` project
- Build email outreach tool in `projects/email-outreach/`
- Dogfood ColdCopy to sell ColdCopy

### Strategy 2: Chinese Social Media (Xiaohongshu, Zhihu, Bilibili)
- Double Mood → Xiaohongshu (emotional wellness)
- ColdCopy → Zhihu / WeChat (B2B)
- FlowPrep → Zhihu / Bilibili (technical)

### Strategy 3: Bilingual Products (EN + 中文)
- Add language toggle to all landing pages
- Double Mood already bilingual ✅

### Strategy 4: Cloudflare Web Analytics — DO NOT REMOVE
- Double Mood: token `d373debf0c0e4b8cbc752883cd00c8cb`
- ColdCopy: token `3d9bb59f7ef5487fb82a6e246857148f`
- FlowPrep: needs token — add once available

---

## Active Products (3 Live + 3 Building)

### Live Products
| Product | URL | Status |
|---------|-----|--------|
| ColdCopy | https://coldcopy-au3.pages.dev | LIVE, $0 revenue, LinkedIn DMs failing |
| Double Mood | https://double-mood.pages.dev/ | LIVE, Phase 2, $0 revenue |
| FlowPrep AI | https://flowprep-ai.pages.dev/ | LIVE, landing page only, awaiting validation |

### Building (MUST GO — founder directive)
| Product | Status | Next Step |
|---------|--------|-----------|
| PowerCast | Evaluated, founder override GO | BUILD this cycle |
| ConnectPath | Not evaluated | Quick eval → BUILD |
| AutoNovel | Not evaluated | Quick eval → BUILD |

### Evaluated — NO-GO (founder accepts)
| Product | Reason |
|---------|--------|
| NarrativeEdge | No clear buyer, legal/compliance risk |

---

## Company Infrastructure
- **Cloudflare:** Pages + Workers + D1 + KV (free tier)
- **GitHub:** repos (landing page, ColdCopy)
- **Stripe:** Account live (GBP), test mode payment links active
- **Gumroad:** Available for digital products (reports, datasets, ebooks)
- **Monitoring:** UptimeRobot configured
- **Runway:** Infinite (free tier infra, ~$3-7/week API costs)
- **Founder Expertise:** PhD in Machine Learning + CFD

---

## Next Action

**REBUILD ConnectPath** — the V1 in `projects/connectpath/` is WRONG (simple GitHub search). Founder wants an AI AGENT SERVICE that actively reaches people on the user's behalf. Read the BUILD #2 spec carefully.

1. SCRAP `projects/connectpath/` V1 or rename to `projects/connectpath-v1-deprecated/`
2. Build the correct ConnectPath: intake form + AI agent that researches + drafts + sends outreach
3. Bilingual EN + 中文
4. Credit-based pricing (agent searches) + outcome-based pricing
5. Deploy to Cloudflare Pages + Workers

**Also:** Add bilingual toggle to existing products (ColdCopy, FlowPrep, PowerCast) when time permits.

---

## Company State

- **Phase:** BUILD PIPELINE (PowerCast done, ConnectPath next, AutoNovel after)
- **Revenue:** $0 (PowerCast Gumroad products just went live, awaiting first sale)
- **Live Products:** ColdCopy, Double Mood, FlowPrep AI, PowerCast (4 total)
- **Building:** ConnectPath, AutoNovel
- **Infrastructure:** Cloudflare Pages (free), Gumroad (live), Stripe (live)
- **Runway:** Infinite (free tier infra)
- **Gumroad Account:** https://jianou.gumroad.com (3 products published)

---

## Previous Cycles Summary

**Cycle 59: NarrativeEdge evaluation — NO-GO** (founder accepts)
**Cycle 58: PowerCast evaluation — CEO NO-GO, founder OVERRIDES to MUST GO**
**Cycles 34-57: 24 wasted monitoring cycles**
**Cycle 33: FlowPrep AI landing page shipped**
**Cycle 25: FlowPrep AI evaluation — CONDITIONAL GO**
**Cycle 20: Double Mood Phase 2 shipped**
**Cycles 1-10: ColdCopy build + launch**

---

## ADD CYCLE REPORTS BELOW THIS LINE (do NOT modify anything above)

---
