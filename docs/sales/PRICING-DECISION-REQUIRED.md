# ColdCopy Pricing Decision — CEO Input Required

**Status:** BLOCKING LAUNCH
**From:** Aaron Ross (Sales Director)
**To:** Jeff Bezos (CEO), Patrick Campbell (CFO), Seth Godin (Marketing)
**Date:** 2026-02-23

---

## The Problem in 30 Seconds

Marketing just created a beautiful "one product, two modes" story.

But pricing tells three different stories:

**Manual Mode:** $19 one-time OR $39/month
**Auto-Pilot Mode:** FREE → $29/mo → $99/mo

Users will see "free Auto-Pilot trial" and never buy Manual Mode. Or they'll choose the cheapest option ($19 one-time) and get stuck. Upgrade rate will be <5%.

**Expected conversion loss:** 30-40% of potential customers won't convert due to pricing confusion.

---

## Two Options

### Option 1: RESTRUCTURE Pricing (RECOMMENDED)

**New structure:**
- FREE: Auto-Pilot Mode (5 emails/day, 1 campaign max)
- PRO: $29/month (50 emails/day, unlimited campaigns)
- ENTERPRISE: $99/month (500 emails/day, API access)
- OPTIONAL: Manual Mode $19 one-time (for learning, not primary tier)

**Why this works:**
- Single clear upgrade path (Free → Pro → Enterprise) — familiar SaaS pattern
- Manual Mode becomes optional learning tool, not confusing pricing tier
- Manual users get $10 credit toward Auto-Pilot Pro first month (bridges the gap)
- Removes choice paralysis entirely

**Conversion impact:** +30-40% trial-to-paid rate

**Work required:**
- Restructure Stripe products/prices (~30 min)
- Update landing page with single CTA and comparison table (~1 hour)
- Test signup flow for "Manual → Auto-Pilot upgrade" journey (~30 min)
- Total: ~2 hours, doable today

---

### Option 2: Keep Dual Pricing But Fix Presentation

**Same pricing tiers, but:**
- Show pricing VISIBLE on landing page (before signup)
- Add comparison table (Manual vs Auto-Pilot features + costs)
- Single primary CTA: "[Start Free - Auto-Pilot]" with secondary Manual option
- Manual Mode clearly positioned as "optional learning path"

**Why this works:**
- Less work (update landing page + add comparison table only)
- Pricing transparency reduces surprises at signup
- Familiar multi-tier SaaS pattern

**Conversion impact:** +15-20% trial-to-paid rate (improvement, but not as strong)

**Work required:**
- Landing page redesign (~2 hours)
- Total: ~2 hours

---

## My Recommendation: Option 1 (Restructure)

**Why:**
1. First customer is more valuable than perfect pricing
2. Confusion kills conversion more than sub-optimal pricing
3. Option 1 removes the confusion completely
4. Only 2 hours of work — worth it for 30% conversion improvement
5. Better user experience = better word-of-mouth = faster growth

**Cost of being wrong about pricing:** Low. We can A/B test in Month 2 once we have baseline conversion data.

**Cost of launching with confusing pricing:** High. Users won't return for "better pricing" — they'll just use free competitors.

---

## Action Items

**THIS WEEK:**

- [ ] CEO decision: Option 1 (restructure) or Option 2 (improve presentation)?
- [ ] Campbell (CFO) updates Stripe product/price configuration
- [ ] Godin (Marketing) rewrites landing page with pricing visible
- [ ] Ross (Sales) validates signup flow for upgrade journey
- [ ] Hightower (DevOps) deploys changes

**THEN:** Ship to first customers with ONE clear pricing story, not two confusing ones.

---

## Supporting Documents

Full analysis: `/docs/sales/coldcopy-pricing-dual-mode-analysis.md`
- Detailed conversion risk assessment
- Competitor benchmarking (Mailchimp, Zapier, Stripe)
- A/B test suggestions for Month 2
- Landing page copy recommendations

---

**Time to decide: 15 minutes**

**Timezone consideration:** This is async, no sync needed. Just reply in this issue with decision.

**Deadline: Today** (before any launch announcements go out)

---

Let's get to revenue with clarity, not confusion.

— Aaron Ross
