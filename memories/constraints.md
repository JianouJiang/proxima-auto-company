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

## Payment & Revenue Collection
- Revenue should be collected via Stripe (preferred) or similar payment processor.
- Set up a Stripe account early — agents should integrate Stripe Checkout or Payment Links.
- All revenue goes to the founder's Stripe account.
- If selling digital products (PDFs, reports), use Stripe Payment Links or Gumroad as a quick start.

## Scope
- Focus on ONE product at a time. No parallel product development.
- Ship MVP in under 2 weeks, then iterate based on real customer feedback.
- Do things that don't scale first (manual processes OK if they generate revenue).

---

> **To modify these constraints:** Edit this file directly. Changes take effect on the next cycle.
> These constraints persist across ALL cycles and CANNOT be changed by any AI agent.
