# ConnectPath V2 - Complete Rebuild

**Date**: 2026-02-21
**Agent**: fullstack-dhh
**Status**: Built, Ready for Deployment

## Problem

The V1 in `projects/connectpath/` was WRONG. It was just a GitHub search tool. Founder directive: rebuild as an **AI agent service** that actively works to connect users to anyone in the world.

## What ConnectPath Actually Is

An AI-powered connection service that:

1. Takes user's CV/intro + target person + motivation
2. AI researches the target (LinkedIn, articles, social media, interviews)
3. Maps potential connection chains (user → intermediary A → intermediary B → target)
4. Drafts personalized outreach emails for each step
5. Returns actionable results to user

**V1 Scope**: Research + mapping + drafting (NO actual sending)

## Architecture Decisions

### Why Monolith?

- Single Cloudflare Worker handles everything
- D1 for persistent data (users, campaigns, steps, transactions)
- KV for credits tracking (optional, using D1 for now)
- Queue for async AI processing
- No microservices complexity—one deployment unit

### Why Vanilla JS?

- No React/Next.js bloat
- Faster page loads
- Bilingual UI with simple toggle
- DHH principle: Convention over Configuration

### Why Credit-Based Pricing?

Two models considered:
1. **Pay-per-outcome** (reply £50, call £200, meeting £500)
2. **Pay-per-search credits** ← **IMPLEMENTED**

Chose credits because:
- Easier to implement for V1
- Predictable cost for users
- No refund complexity
- Scalable to unlimited plans

## Tech Stack

| Layer | Technology | Why |
|-------|------------|-----|
| Frontend | HTML + Tailwind + vanilla JS | Fast, simple, no build step |
| Backend | Cloudflare Workers | Edge compute, 0ms cold start |
| Database | D1 (SQLite) | Serverless SQL, cheap |
| AI | Claude Sonnet 4.5 | Best reasoning for research + drafting |
| Payment | Gumroad | Fastest integration, no code |
| Queue | Cloudflare Queues | Async campaign processing |

## File Structure

```
projects/connectpath/
├── index.html          # Landing page (bilingual)
├── intake.html         # CV + target form
├── dashboard.html      # User campaigns + credits
├── campaign.html       # Single campaign details
├── worker.js           # Cloudflare Worker (API + AI agent)
├── schema.sql          # D1 database schema
├── wrangler.toml       # Cloudflare config
└── README.md           # Setup instructions
```

## Database Schema

### users
- id, email, credits_balance, created_at, updated_at

### campaigns
- id, user_id, email, cv, target_name, target_role, motivation, status, credits_used, results, created_at, updated_at

### campaign_steps
- id, campaign_id, step_type (research_target/find_intermediary/draft_email), step_description, credits_cost, result, status, created_at, completed_at

### credit_transactions
- id, user_id, amount, transaction_type (purchase/usage/refund), plan, campaign_id, created_at

## AI Agent Logic

Each campaign runs 3 steps:

### Step 1: Research Target (1 credit)
Prompt Claude to find:
- Professional background
- Current role and company
- Public interests and passions
- Recent content (articles, talks, interviews)
- Potential connection points

Returns structured JSON.

### Step 2: Find Intermediaries (1 credit)
Given user CV + target research:
- Find 2-3 potential bridge people
- Assess connection strength (weak/medium/strong)
- Explain why they're good intermediaries
- How to find them (LinkedIn, mutual friends, events)

Returns JSON array of intermediaries.

### Step 3: Draft Outreach Emails (1 credit)
Given all context:
- Draft personalized email to each intermediary
- Draft direct email to target (backup)
- 150-200 words, specific, actionable

Returns JSON with email drafts.

**Total: 3 credits per campaign**

## Pricing

| Plan | Credits | Price |
|------|---------|-------|
| Starter | 10 | £5 |
| Growth | 50 | £20 |
| Pro | 200 | £50 |
| Unlimited | ∞ (1 month) | £99 |

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /api/campaigns | Create new campaign |
| GET | /api/dashboard?email=X | Get user credits + campaigns |
| POST | /api/webhook/gumroad | Handle payment webhook |
| GET | /api/campaign/:id | Get campaign details + steps |

## User Flow

1. User lands on `index.html` → sees pricing
2. Clicks "Start Your First Connection" → `intake.html`
3. Fills CV + target + motivation + selects plan
4. Submits → creates campaign in DB (status: pending)
5. Redirects to Gumroad payment link
6. After payment → Gumroad webhook → adds credits to user
7. Worker triggers campaign processing (async via Queue)
8. AI agent runs 3 steps → deducts 3 credits
9. Campaign status: processing → completed
10. User goes to `dashboard.html` → sees results
11. Clicks campaign → `campaign.html` → sees email drafts

## Deployment Checklist

- [ ] Create D1 database: `wrangler d1 create connectpath-db`
- [ ] Update `wrangler.toml` with database_id
- [ ] Run schema: `wrangler d1 execute connectpath-db --file=schema.sql`
- [ ] Set secrets: `wrangler secret put ANTHROPIC_API_KEY`
- [ ] Deploy: `wrangler deploy`
- [ ] Setup Gumroad products (4 plans)
- [ ] Configure Gumroad webhook to Worker URL
- [ ] Test full flow: intake → payment → campaign processing

## V2 Features (Future)

- [ ] Actually send emails (Gmail API integration)
- [ ] Track email open rates and replies
- [ ] LinkedIn API for real mutual connections
- [ ] Success-based pricing (pay when target replies)
- [ ] Multi-language beyond EN/中文
- [ ] Campaign templates
- [ ] Team accounts with shared credits

## Why This Works

1. **Real value**: Saves hours of manual research and cold email drafting
2. **Clear pricing**: Credits are easy to understand
3. **Low risk**: Users see results before sending emails
4. **Scalable**: AI agent works 24/7, no human bottleneck
5. **Boring tech**: Proven stack, minimal complexity

## DHH Principles Applied

- **Majestic Monolith**: One Worker, one database, one deployment
- **Convention over Configuration**: Sensible defaults, no complex config
- **Programmer Happiness**: Vanilla JS, no webpack hell
- **No SPA Madness**: Server-rendered HTML + progressive enhancement
- **Boring Technology**: Cloudflare + D1 + Claude, all proven at scale

## Next Steps

1. Deploy to Cloudflare Workers
2. Create Gumroad products
3. Test end-to-end flow
4. Ship to founder for review
5. If approved, market and launch

---

**Outcome**: Rebuilt ConnectPath as intended. Ready for deployment.
