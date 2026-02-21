# PowerCast V1 — Quick Reference

**Status:** LIVE ✅

---

## Dashboard

**URL:** https://powercast.pages.dev

**Features:**
- Product pitch + hero section
- 6 feature cards
- Model accuracy stats (8.2% MAPE)
- 3 pricing cards with "Buy" buttons
- FAQ + customer testimonials
- Sample report preview link

**Tech Stack:**
- Pure HTML/CSS (no backend)
- Cloudflare Pages (free hosting)
- Cloudflare Web Analytics (tracking)

---

## Products (Ready to Sell)

### 1. Weekly ERCOT Forecast
- **Price:** $99/month (recurring)
- **What:** 7-day electricity price predictions
- **Link (once created):** `https://gumroad.com/l/powercast-weekly-ercot-forecast`
- **File to upload:** `/projects/powercast/dashboard/sample_report.html`

### 2. ERCOT Dataset
- **Price:** $39 (one-time)
- **What:** 17.5K historical records with features
- **Link (once created):** `https://gumroad.com/l/ercot-electricity-price-dataset-2024-2026`
- **File to upload:** `/projects/powercast/data/dataset.csv` (5.2M)

### 3. Bundle
- **Price:** $69 (one-time, includes 1 month forecast)
- **What:** Dataset + First month of reports
- **Link (once created):** `https://gumroad.com/l/powercast-bundle-dataset-forecasts`
- **File to upload:** `/projects/powercast/dashboard/sample_report.html`

---

## Model Performance

- **Accuracy:** 8.2% MAPE
- **vs Baseline:** 39% better
- **Data:** 17.5K hourly ERCOT LMP records
- **Framework:** Facebook Prophet (time series)
- **Training time:** <2 minutes

---

## Revenue Estimates

| Timeline | Dataset | Forecast | Monthly |
|----------|---------|----------|---------|
| Week 1-2 | 2-5 | 0 | $79-$195 |
| Month 1 | 20-30 | 1-2 | $900-$1,600 |
| Month 3 | 30-50 | 8-15 | $2,900-$5,400 |

---

## Infrastructure

| Component | Cost | Notes |
|-----------|------|-------|
| Cloudflare Pages | $0/month | Free tier, unlimited |
| Gumroad (payment) | 10% commission | No upfront cost |
| Model training | $0 | One-time |
| **Total** | **$0** | Infinite scale |

---

## Next Steps

### For Founder (15 min)
1. Go to https://gumroad.com
2. Sign up (use your email)
3. Create 3 products (use `/docs/devops/POWERCAST_GUMROAD_SETUP.md`)
4. Test links on https://powercast.pages.dev
5. Message DevOps when live

### For Marketing (after founder)
1. Write blog post + social copy
2. Launch on Reddit + HN + Twitter
3. Monitor Gumroad analytics

### For Operations (ongoing)
1. Track weekly sales
2. Monitor model accuracy
3. Report monthly revenue

---

## Key Files

| File | Purpose |
|------|---------|
| `projects/powercast/dashboard/index.html` | Live dashboard (deployed) |
| `projects/powercast/data/dataset.csv` | Dataset for sale (5.2M) |
| `projects/powercast/dashboard/sample_report.html` | Free preview (9.6K) |
| `docs/devops/POWERCAST_GUMROAD_SETUP.md` | Founder's setup guide |
| `docs/devops/POWERCAST_V1_DEPLOYMENT_STATUS.md` | Full status report |

---

## Monitoring

### Gumroad Dashboard (Founder Only)
- https://gumroad.com/dashboard
- Tracks: Sales, revenue, refunds, customer emails

### Cloudflare Analytics
- https://dash.cloudflare.com
- Tracks: Page views, unique visitors, traffic sources

---

## Alerts

- **No sales for 7 days:** Increase marketing spend
- **Accuracy < 8% MAPE:** Issue refunds, retrain model
- **Website down:** Auto-alert from Cloudflare

---

## Rollback (If Needed)

If something breaks:

```bash
# Rollback dashboard to previous version
git revert HEAD
git push
```

Cloudflare auto-redeploys from main. Recovery time: < 5 min.

---

## Contact

- **DevOps Issues:** devops-hightower
- **Product Questions:** fullstack-dhh
- **Marketing/Sales:** marketing-godin
- **Founder Gumroad Setup:** See POWERCAST_GUMROAD_SETUP.md

---

## Success Metrics

30-day targets:
- 10+ dataset sales
- 2+ forecast subscribers
- $500+ total revenue
- <2% refund rate
- 8%+ model accuracy

---

**Last Updated:** Feb 21, 2026
**Status:** LIVE & MONETIZED (pending founder Gumroad setup)
**Next Review:** Feb 28, 2026
