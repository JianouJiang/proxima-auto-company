# ColdCopy Cost Monitoring & Budget Guide

**Date:** 2026-02-20
**Engineer:** Kelsey Hightower
**Service:** ColdCopy Production (MVP Phase)

---

## Cost Breakdown

### Service Costs (Monthly Estimate)

| Service | Free Tier | Cost Per Unit | Est. Monthly Cost | Notes |
|---------|-----------|---------------|-------------------|-------|
| **Cloudflare Pages** | 100,000 req/mo | $0 | $0 | Free tier includes D1, KV, Functions |
| **D1 Database** | 500 MB storage | $0.75/GB | $0 (under 100MB projected) | Automates backups |
| **KV Namespace** | 100,000 writes/mo | $0.50/million | $0 (50-100 writes/day) | Rate limiting store |
| **Claude Haiku** | None | $0.011/gen | $0-$5/week | Variable by usage |
| **Stripe** | None | 2.9% + $0.30 | 0% (no revenue yet) | Charges only on successful payments |
| **GitHub** | Public repos | $0 | $0 | Free for public projects |
| **Total (estimated)** | | | **$0-$5/week** | |

---

## 1. Claude API Cost Monitoring

### Cost Per Generation

```
Typical generation = ~2,500 output tokens + 200 input tokens = 2,700 tokens
Cost = 2,700 tokens × $0.011 / 1M = $0.0297 ≈ $0.03 per generation
```

### Projected Usage & Cost

| Users/Day | Gen/Day | Cost/Day | Cost/Week | Cost/Month |
|-----------|---------|----------|-----------|------------|
| 1 | 1 | $0.03 | $0.21 | $0.90 |
| 5 | 5 | $0.15 | $1.05 | $4.50 |
| 10 | 10 | $0.30 | $2.10 | $9.00 |
| 20 | 20 | $0.60 | $4.20 | $18.00 |
| 50 | 50 | $1.50 | $10.50 | $45.00 |

**Alert Threshold:** If daily cost exceeds $5, investigate for:
- Infinite loops in frontend
- Bot/scraper abuse (rate limit check needed)
- Malicious API calls

---

### How to Check API Usage

**Via Anthropic Console:**

1. Go to https://console.anthropic.com/account/usage
2. View:
   - Daily token usage (last 30 days)
   - Estimated monthly cost
   - Usage breakdown by model

**Via Logs (Manual Calculation):**

```bash
# Option 1: Calculate from Cloudflare logs
# Each successful POST to /api/generate costs ~$0.03
# Count 200 responses in last 24h = rough estimate

# Option 2: Calculate from expected input/output
# Prompt template uses ~200 tokens input
# Average output is 2000-2500 tokens per email sequence (7 emails)
# Total per generation = ~2700 tokens × $0.011 / 1M tokens = $0.03
```

**Cost Alert Script:**

Save as: `docs/devops/check-api-cost.sh`

```bash
#!/bin/bash

echo "=== Claude API Cost Check ==="
echo "Usage data available at: https://console.anthropic.com/account/usage"
echo ""
echo "Daily Threshold: $5/day (investigate if exceeded)"
echo "Weekly Threshold: $35/week (pause marketing if exceeded)"
echo "Monthly Threshold: $150/month (needs budget review)"
echo ""
echo "Current generation cost: ~$0.03 per request"
echo "At 1 request/day = $0.90/month (safe)"
echo "At 50 requests/day = $45/month (monitor)"
echo ""

# If you have API access, you can parse usage:
# curl -s https://api.anthropic.com/v1/beta/usage \
#   -H "x-api-key: $ANTHROPIC_API_KEY" | jq '.daily_cost'
```

---

## 2. Cloudflare Free Tier Monitoring

### Current Limits

| Resource | Limit | Current Usage | Status |
|----------|-------|----------------|--------|
| **Pages Requests** | 100,000/month | ~300-500/week (MVP) | ✓ Safe |
| **D1 Rows** | Unlimited | ~5-20 rows/day | ✓ Safe |
| **D1 Storage** | 500 MB | ~2-5 MB projected | ✓ Safe |
| **KV Writes** | 100,000/month | ~50-100/day | ✓ Safe |
| **Functions** | 100,000/month | Same as requests | ✓ Safe |

**No cost for Cloudflare at current MVP scale.**

### How to Check Cloudflare Usage

**Dashboard:**

1. Go to https://dash.cloudflare.com/68ec8b1ccccb48e1a7cf898d2228c713/pages
2. Click "Analytics" > "Requests"
3. View last 7 days:
   - Total requests
   - Average response time
   - Error rate (4xx, 5xx)

**D1 Storage Check:**

```bash
# Check database size
npx wrangler d1 list
# Shows: Size: X MB

# Manual row count
npx wrangler d1 execute coldcopy-db --command \
  "SELECT COUNT(*) FROM sessions; SELECT COUNT(*) FROM sequences;"
```

**KV Namespace Check:**

```bash
# List all keys
npx wrangler kv key list --binding RATE_LIMIT

# Each key = 1 write (rate_limit:{sessionId})
# Count per day ~= unique sessions in that day
```

---

## 3. Payment Processing Cost (Future)

When we add paid plans:

### Stripe Payment Cost

| Payment Volume | Stripe Fee | Our Net | Notes |
|----------------|-----------|---------|-------|
| $10 (1 customer) | $0.59 | $9.41 | 2.9% + $0.30 |
| $100 (10 customers) | $3.20 | $96.80 | 2.9% + $0.30 per transaction |
| $1,000 (100 customers) | $29.30 | $970.70 | 2.9% + $0.30 per transaction |

**Alert:** If payment processing cost exceeds revenue by >5%, consider alternative payment method (e.g., higher price point).

---

## 4. Weekly Cost Review Checklist

Every Friday, run this checklist:

```
[ ] Claude API cost check
    - Visit https://console.anthropic.com/account/usage
    - Note daily cost trends
    - Alert if >$5/day

[ ] Cloudflare usage check
    - Visit Cloudflare dashboard
    - Verify under free tier limits
    - Check error rate (should be <1%)

[ ] Request volume check
    - Count successful API calls this week
    - Divide by days = estimate daily users
    - Project to monthly

[ ] Budget status
    - Expected monthly cost (Claude + other) = $_____
    - Budget remaining this month = $_____
    - If overage projected: investigate

[ ] Cost optimization opportunities
    - Are we wasting API calls? (e.g., duplicate requests)
    - Can we batch requests?
    - Can we cache results?
```

---

## 5. Cost Optimization Strategies

### Short-term (MVP Phase - Now)

1. **Rate Limiting (Done)**
   - Free tier: 1 generation per session
   - Premium tier: More (future)
   - Impact: Prevents accidental loops costing hundreds

2. **Caching Results (Future)**
   - Store generated sequences in KV (5-min cache)
   - Deduplicate identical input requests
   - Impact: Reduce API calls by ~5-10%

3. **Batch Processing (Future)**
   - Queue requests, batch every 10 min
   - Impact: Reduced latency, better Claude context
   - Cost impact: Neutral (same tokens)

### Mid-term (After Revenue)

1. **Switch to Claude Opus for high-value customers**
   - Input: $3/1M tokens, Output: $15/1M tokens
   - Use Haiku for free tier ($0.011/$0.04)
   - Impact: Higher quality for paid users

2. **Implement result caching**
   - Store in D1 instead of regenerating
   - Impact: 20-30% cost reduction for similar queries

3. **Implement streaming responses**
   - Start sending email #1 while generating #7
   - Impact: Perceived performance improvement

---

## 6. Budget Alerts & Escalation

### Alert Thresholds

| Threshold | Action | Who |
|-----------|--------|-----|
| >$2/day | Check logs for anomalies | DevOps |
| >$5/day | Pause product marketing (investigate) | DevOps + CEO |
| >$10/day | Immediate cost review (possible rollback) | CEO |
| >$50/day | Critical issue (likely attack or bug) | CEO + CTO |

### Emergency Cost Cutoff

If daily Claude API cost exceeds $20:

1. Immediately disable `/api/generate` endpoint
2. Investigate root cause (loop? attack? bot?)
3. Fix issue in staging
4. Re-enable endpoint with fix

```bash
# Emergency cutoff: Comment out Claude call in functions/api/generate.ts
# Deploy: git push (auto-redeploys)
# Investigate: Check logs for what triggered spike
```

---

## 7. Cost Reporting Template

Use for weekly reports to CEO (save to `docs/cfo/`):

```markdown
# Weekly Cost Report - Week of Feb 20, 2026

## Summary
- Claude API: $1.50 (5 generations × $0.30 avg)
- Cloudflare: $0 (free tier)
- Stripe: $0 (no sales yet)
- **Total: $1.50**

## Breakdown
- Monday: 1 request = $0.03
- Tuesday: 1 request = $0.03
- Wednesday: 1 request = $0.03
- Thursday: 1 request = $0.03
- Friday: 1 request = $0.03
- Weekend: 0 requests = $0

## Projection
- Current weekly burn: $1.50
- Monthly run rate: ~$6
- Budget remaining: Unlimited (MVP phase)

## Optimization Opportunities
- None at current usage level
- Once 10+ users/day: consider caching

## Risks
- None identified
- No cost anomalies

## Next Week Goals
- Monitor for first paid customer
- Set up revenue tracking
```

---

## 8. Integration with Financial Models

### Unit Economics

```
Free Tier:
- Users: Unlimited
- Cost per user: $0.03 (1 generation)
- Revenue per user: $0
- LTV: $0 (not profitable)

Premium Tier (Future):
- Price: $9/month (10 generations)
- Cost per user: $0.30 (10 generations)
- Revenue per user: $9
- Gross margin: 96.7%
- LTV: $9/user (at 1-month horizon)
```

---

## Resources

- **Anthropic Pricing:** https://www.anthropic.com/pricing
- **Anthropic Usage Console:** https://console.anthropic.com/account/usage
- **Cloudflare Pricing:** https://www.cloudflare.com/pricing/
- **Cloudflare Dashboard:** https://dash.cloudflare.com/
- **Stripe Pricing:** https://stripe.com/pricing
- **Cost Calculator:** See spreadsheet in `docs/cfo/financial-model.xlsx` (if created)

---

**Last Updated:** 2026-02-20
**Next Review:** 2026-02-27 (weekly)
**Budget Responsibility:** DevOps + CFO
**Escalation Contact:** CEO (over $10/day)
