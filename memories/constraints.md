# Founder Constraints — IMMUTABLE RULES

These constraints are set by the human founder BEFORE the company starts.
**Every agent MUST obey these constraints at ALL times. They CANNOT be overridden by any agent, including the CEO.**
They are injected into every cycle and take priority over all other decisions.

---

## Budget & Capital
- **Starting capital: $0** — There is NO startup funding. The company starts with zero money.
- All tools/services used must be FREE tier or already available (Claude API, Cloudflare free tier, GitHub free, etc.)
- Do NOT assume any budget for paid services, ads, or hiring.
- Bootstrap everything. Revenue must come before spending.

## Timeline
- **This is a SHORT-TERM project: 3-6 months maximum.**
- The company MUST generate revenue within the first 2-3 months.
- No multi-year roadmaps. No "long-term vision" that delays revenue.
- If a product idea takes more than 1 month to build, it's too complex. Simplify or pick something else.
- Every week should show measurable progress toward revenue.

## Revenue Priority
- **Revenue is the #1 metric.** Not users, not traffic, not signups — MONEY.
- The first product must be something people will PAY for immediately.
- Prefer digital products with near-zero marginal cost (reports, tools, templates, SaaS).
- Price from Day 1. No "free now, monetize later" strategies.

## Technical Constraints
- Must run on Linux (current system is Ubuntu on VMware).
- Use free deployment: Cloudflare Workers/Pages (free tier), GitHub Pages, or similar.
- No paid cloud services (no AWS/GCP bills).
- Keep it simple: monolith, single repo, minimal dependencies.

## Payment & Revenue Collection — STRIPE IS LIVE
- **Stripe account is FULLY SET UP and LIVE.** Bank account linked, charges enabled, verification complete.
- **LIVE API keys are in `.env`** (STRIPE_PUBLISHABLE_KEY and STRIPE_SECRET_KEY). Use `python-dotenv` or read from environment.
- **Account currency: GBP** (British Pounds). Prices should be set in GBP or USD (Stripe auto-converts).
- **Integration approach (in order of preference):**
  1. **Stripe Payment Links** — Fastest. Create via `stripe.PaymentLink.create()`. No checkout page code needed.
  2. **Stripe Checkout Sessions** — For embedded checkout. Use `stripe.checkout.Session.create()` with success/cancel URLs.
  3. Checkout server template exists at `projects/stripe-integration/checkout-server.py` for reference.
- **For ColdCopy specifically:** After free sequence, redirect to Stripe Checkout for payment. Create a Stripe Product + Price for the subscription ($39/month) and one-time ($19) options.
- All revenue goes to the founder's bank account (auto-payout every 2 business days).
- **API keys are NEVER committed to git.** Read from `.env` or environment variables only.
- Company landing page for Stripe verification: https://jianoujiang.github.io/proxima-auto-company/projects/landing-page/

## Scope
- Focus on ONE product at a time. No parallel product development.
- Ship MVP in under 2 weeks, then iterate based on real customer feedback.
- Do things that don't scale first (manual processes OK if they generate revenue).

---

> **To modify these constraints:** Edit this file directly. Changes take effect on the next cycle.
> These constraints persist across ALL cycles and CANNOT be changed by any AI agent.
