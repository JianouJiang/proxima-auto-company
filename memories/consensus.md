# Auto Company Consensus

## Last Updated
2026-02-21 22:15 UTC (Cycle 61 complete — SixDegrees V1 built but WRONG, rebuild pending)

## Current Phase
**BUILD PIPELINE — PowerCast LIVE, SixDegrees V1 WRONG (rebuild needed), AutoNovel next**

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

### ✅ BUILD #1: PowerCast — Electricity Price Prediction ⚡ COMPLETE

**Status: LIVE at https://powercast.pages.dev/ (Cycle 60)**

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

### BUILD #2: SixDegrees — AI Agent That Reaches Anyone For You 🔗 MUST GO

**Status: V1 built but WRONG (Cycle 61). Founder says SCRAP V1 and REBUILD with correct vision below.**

**⚠️ Cycle 61 built a simple GitHub graph search tool, which is NOT what the founder wants. The V1 in `projects/sixdegrees/` must be REPLACED with this vision:**

**What SixDegrees ACTUALLY is:**
SixDegrees is an **AI agent service** that actively works to connect you to anyone in the world through 6 degrees of separation. It's NOT a search tool — it's an agent that TAKES ACTION on your behalf.

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

1. **ONE build per cycle.** Do PowerCast first, then SixDegrees, then AutoNovel.
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

## 🚨 FOUNDER DIRECTIVE — SIXDEGREES REAL VALIDATION TEST 🚨

**⚠️ DO NOT REMOVE THIS SECTION. THIS IS A FOUNDER DIRECTIVE. ⚠️**

**SixDegrees must ACTUALLY SEND EMAILS.** The current V2 researches and drafts but doesn't send. The whole point is the agent ACTS on your behalf.

**VALIDATION TEST: Get Jianou connected to Elon Musk via 6 degrees**
- Use `jianou.works@gmail.com` as the sender email
- **DO NOT email Elon Musk directly — he won't reply.**
- **USE STRATEGY: Break it down into 5-6 degrees of contact, gradually leading to him.**

**Example 6-degree chain:**
```
Jianou (ML PhD, energy/AI background)
  → Degree 1: A professor or researcher Jianou has real connection to
  → Degree 2: Someone that professor knows in the AI/energy industry
  → Degree 3: A startup founder or VC in the Tesla/SpaceX ecosystem
  → Degree 4: Someone who works at Tesla/SpaceX/xAI
  → Degree 5: Someone in Elon's inner circle
  → Degree 6: Elon Musk
```

**The agent must:**
1. Research Jianou's REAL background (ML PhD, energy expertise, CFD) to find credible starting points
2. Map the REALISTIC chain — each intermediary must have a plausible reason to help
3. Start from Degree 1 — email people Jianou can ACTUALLY reach
4. Each email must explain WHY this connection benefits the intermediary
5. SEND the email via Gmail SMTP
6. Track responses and adapt

**Implementation:**
- Gmail SMTP: `smtp.gmail.com`, port 587 (TLS)
- Sender: `jianou.works@gmail.com`
- Gmail App Password already set as Cloudflare secret: `GMAIL_APP_PASSWORD`

---

## 🚨 FOUNDER DIRECTIVE — ALL PRODUCTS BILINGUAL EN/中文 + STORY PAGES 🚨

**⚠️ AGENTS HAVE REMOVED THIS 6 TIMES. PRESERVE VERBATIM. ⚠️**

**Status: MOSTLY DONE ✅** — Founder manually added bilingual to these pages and deployed:
- ✅ FlowPrep AI (`flowprep-ai.pages.dev`) — bilingual deployed
- ✅ PowerCast (`powercast.pages.dev`) — bilingual deployed
- ✅ Company landing page (`coldcopy-au3.pages.dev`) — bilingual deployed, ConnectPath→SixDegrees
- ✅ Story page — bilingual deployed
- ✅ Double Mood — already bilingual
- ✅ SixDegrees (ConnectPath V2) — already bilingual

**Still needs bilingual:**
- ColdCopy app (React/Vite — more complex, needs i18n in React components)
- AutoNovel (not built yet — must launch bilingual)
- Story sub-pages (story-powercast.html, story-sixdegrees.html, etc.)

---

## 🚨 FOUNDER DIRECTIVE — DUAL-MARKET: WESTERN + CHINESE (ALL PRODUCTS) 🚨

**⚠️ DO NOT REMOVE OR SHORTEN. ⚠️**

**WESTERN social media:** Reddit, Twitter/X, LinkedIn, HN, Product Hunt
**CHINESE social media:** 小红书 (Xiaohongshu), 微信公众号 (WeChat), 知乎 (Zhihu), 哔哩哔哩 (Bilibili), 抖音 (Douyin)
**WESTERN payments:** Stripe (live), Gumroad (live)
**CHINESE payments:** WeChat Pay, Alipay — research cross-border integration
**Email outreach:** `jianou.works@gmail.com`, dogfood ColdCopy

**Cloudflare Web Analytics — DO NOT REMOVE:**
- Double Mood: `d373debf0c0e4b8cbc752883cd00c8cb`
- ColdCopy: `3d9bb59f7ef5487fb82a6e246857148f`
- PowerCast: `94d80efb33534267bad16e81b8e35ae1`

---

## Active Products (3 Live + 3 Building)

### Live Products
| Product | URL | Status | Revenue |
|---------|-----|--------|---------|
| ColdCopy | https://coldcopy-au3.pages.dev | LIVE, Phase 1 | $0 |
| Double Mood | https://double-mood.pages.dev/ | LIVE, Phase 2 | $0 |
| FlowPrep AI | https://flowprep-ai.pages.dev/ | LIVE, landing page | $0 |
| PowerCast | https://powercast.pages.dev/ | LIVE, Gumroad products live | $0 |

### Building (MUST GO — founder directive)
| Product | Status | Next Step |
|---------|--------|-----------|
| SixDegrees | V1 WRONG (GitHub search tool) | REBUILD as AI agent service |
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

**THIS CYCLE: SixDegrees (formerly SixDegrees) — RENAME + GMAIL SMTP + ELON MUSK 6-DEGREE TEST**

**This is the ONLY priority this cycle. Do NOT split time on other tasks.**

1. **RENAME** the project: `projects/sixdegrees/` → `projects/sixdegrees/`. Update all references. Redeploy as `sixdegrees.pages.dev`
2. **Add Gmail SMTP** to worker.js so SixDegrees can ACTUALLY SEND EMAILS
   - Use `jianou.works@gmail.com` as sender
   - Gmail App Password is already set as Cloudflare secret: `GMAIL_APP_PASSWORD`
   - SMTP: `smtp.gmail.com`, port 587 (TLS) or 465 (SSL)
3. **Run the Elon Musk 6-degree validation test:**
   - Research Jianou's background (ML PhD, energy/CFD expertise)
   - Map a REALISTIC 5-6 degree chain from Jianou → ... → Elon Musk
   - **DO NOT email Elon directly.** Start from Degree 1 — people Jianou can actually reach (professors, alumni, colleagues, researchers in AI/energy)
   - Draft personalized email for the Degree 1 contact explaining who Jianou is and why the connection matters
   - **ACTUALLY SEND the Degree 1 email** via Gmail SMTP
   - Log the full chain + emails in the campaign dashboard
4. **Deploy** and verify the email was sent (check Gmail sent folder)

**After SixDegrees is working with real email sending, THEN move to AutoNovel and bilingual updates in the NEXT cycle.**

---

## Company State

- **Phase:** BUILD PIPELINE (PowerCast LIVE, SixDegrees V1 WRONG need rebuild, AutoNovel next)
- **Revenue:** $0 (4 products live, awaiting first sale)
- **Live Products:** ColdCopy, Double Mood, FlowPrep AI, PowerCast (4 total)
- **Building:** SixDegrees (rebuild), AutoNovel
- **Infrastructure:** Cloudflare Pages (free), Gumroad (live), Stripe (live)
- **Runway:** Infinite (free tier infra)
- **Gumroad Account:** https://jianou.gumroad.com (5 products published)

---

## Previous Cycles Summary

**Cycle 61: SixDegrees V1 built BUT WRONG (simple GitHub search ≠ AI agent service founder wants)**
**Cycle 60: PowerCast BUILD — SHIPPED in 2.5 hours (CEO estimated 7-8 weeks)**
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

## Cycle 61 Report — SixDegrees V1 Built (BUT WRONG)

**Objective:** Execute founder directive — BUILD SixDegrees (product #2 in queue)

**What was built:**
- Simple connection finder using GitHub API
- BFS graph search to find shortest path between two GitHub users
- Freemium model: 3 searches/day free, $9.99/month unlimited
- Bilingual UI (EN + 中文)
- Deployed to https://sixdegrees.pages.dev/

**Team:**
- research-thompson (haiku, 15 min) — Quick feasibility check → GO recommendation
- product-norman (haiku, 10 min) — MVP spec with Don Norman design principles
- fullstack-dhh (sonnet, 3.5 hrs) — Built complete app (928 lines, vanilla JS + Cloudflare Workers + KV)
- devops-hightower (haiku, 25 min) — Deployed to Cloudflare Pages
- marketing-godin (haiku, 20 min) — Gumroad listing copy + story page
- editor-chronicler (haiku, 10 min) — Recorded cycle work

**Deliverables:**
- `/home/jianoujiang/Desktop/proxima-auto-company/projects/sixdegrees/` (complete source, 928 lines)
- `docs/research/sixdegrees-quick-feasibility.md`
- `docs/product/sixdegrees-mvp-spec.md`
- `docs/fullstack/sixdegrees-technical-spec.md`
- `docs/fullstack/sixdegrees-handoff.md`
- `docs/devops/sixdegrees-deployment.md`
- `docs/marketing/sixdegrees-gumroad-listing.md`
- `projects/landing-page/story-sixdegrees.html`

**Timeline:** 4.5 hours total (research → build → deploy → marketing)

**Cost:** $0/month (Cloudflare free tier)

**⚠️ PROBLEM:** Agents misunderstood the founder's vision. Built a simple "GitHub connection search tool" instead of an "AI agent service that actively reaches people on user's behalf."

**Root cause:** Founder directive was unclear in the consensus file at the time. Cycle 61 agents executed based on limited context ("six degrees connection finder"), which sounded like a search tool.

**What founder actually wants (now clarified in BUILD #2 spec):**
- AI agent that researches target person + drafts outreach emails + SENDS them on user's behalf
- Credit-based pricing (agent searches) OR outcome-based pricing (pay only if connection succeeds)
- Multi-step autonomous campaign, not a one-time search

**Next:** REBUILD SixDegrees with correct vision in next cycle

**Learning:** When founder says "six degrees connection finder," confirm whether it's:
- A) Passive search tool (what was built)
- B) Active AI agent service (what founder wants)

Always validate vision before building.

---
