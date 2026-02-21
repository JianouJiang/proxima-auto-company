# PowerCast Operations Runbook

Quick reference for weekly operations, maintenance, and troubleshooting.

---

## Weekly Tasks (Every Monday)

### 1. Generate New Forecast (30 min)
```bash
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/powercast

# Train model with latest data
cd models
python train_simple_model.py

# Generate weekly report
cd ../reports
python generate_report.py

# Output files:
# - reports/weekly_forecast.html (upload to Gumroad)
# - reports/weekly_forecast.csv (attached to email)
```

### 2. Upload Forecast to Gumroad
```
1. Go to: https://gumroad.com/dashboard
2. Select "PowerCast Weekly Forecasts" product
3. Upload new weekly_forecast.html as preview
4. Update "Latest forecast" text if needed
5. Publish/Save
```

### 3. Verify Dashboard Metrics
```bash
# Check Cloudflare analytics
curl -s https://powercast.pages.dev | grep -i "9.2%"
# Should show current MAPE metric

# If metrics are stale, update dashboard/index.html with latest values
```

### 4. Monitor Sales
```
1. Go to: https://gumroad.com/dashboard
2. Check this week's sales:
   - Dataset purchases (target: 1-2/week)
   - New subscribers (target: 1-5/month)
   - Churn rate (watch for cancellations)
3. Note any customer feedback or questions
```

---

## Emergency Procedures

### Dashboard is Down (HTTP 503/504/522)

**Step 1: Check Cloudflare Status**
- Visit: https://www.cloudflarestatus.com/
- If Cloudflare is down, wait for their recovery
- If status is green, proceed to Step 2

**Step 2: Verify Project Exists**
```bash
wrangler pages project list | grep powercast
# Expected output: powercast | powercast.pages.dev | No | <timestamp>
```

**Step 3: Check Recent Deployments**
```bash
wrangler pages deployment list --project-name=powercast
# Should show recent successful deployment
```

**Step 4: Test Authentication**
```bash
wrangler whoami
# Should show: Jianou.works@gmail.com
# If not authenticated, run: wrangler login
```

**Step 5: Redeploy Dashboard**
```bash
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/powercast/dashboard
wrangler pages deploy . --project-name=powercast
# Wait for: "Deployment complete!"
# Test: curl -I https://powercast.pages.dev
```

### Model Accuracy Degraded (MAPE > 12%)

**Step 1: Rebuild Training Dataset**
```bash
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/powercast/data
python fetch_ercot.py      # Get latest ERCOT data
python fetch_weather.py    # Get latest weather
python merge_dataset.py    # Create merged dataset
```

**Step 2: Retrain Model**
```bash
cd ../models
python train_simple_model.py
# Review: models/backtest_results.json
# If MAPE still > 12%, try alternative models
```

**Step 3: Compare Model Performance**
```bash
# If Prophet MAPE poor, try statsforecast:
cd ../models
python train_statsforecast_model.py  # Alternative (if available)
# Compare accuracy metrics and select best
```

**Step 4: Deploy Best Model**
```bash
# Copy best_model.pkl to production
cp best_model.pkl final_model.pkl

# Generate new forecast with updated model
cd ../reports
python generate_report.py

# Upload to Gumroad and notify subscribers
```

### Gumroad Links Broken or Not Updating

**Step 1: Verify Product URLs**
```bash
# Go to: https://gumroad.com/dashboard
# Copy exact product URLs:
# - Dataset product URL
# - Forecast subscription URL
# - Bundle URL (if exists)
```

**Step 2: Update Dashboard**
```bash
# Edit: projects/powercast/dashboard/index.html
# Find and replace 3 placeholder Gumroad URLs:
# 1. https://gumroad.com/powercast-dataset -> [real URL]
# 2. https://gumroad.com/powercast-weekly -> [real URL]
# 3. https://gumroad.com/powercast-bundle -> [real URL]
```

**Step 3: Redeploy Dashboard**
```bash
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/powercast/dashboard
wrangler pages deploy . --project-name=powercast
# Verify: Visit https://powercast.pages.dev and test links
```

### No Sales This Week

**Diagnostic Steps:**
1. Check Gumroad product visibility: https://gumroad.com/dashboard
2. Verify product links work: Test each link manually
3. Review product descriptions: Are they compelling?
4. Check dashboard traffic: Any visitors? (Cloudflare analytics)
5. Monitor Gumroad messaging: Any customer questions?

**Recovery Actions:**
1. Increase price visibility in dashboard (highlight discount)
2. Post dataset to Reddit (r/datasets, r/MachineLearning, r/energy)
3. Share on Twitter/X with sample metrics
4. Create blog post about ERCOT market volatility
5. Email dataset buyers about subscription discount

---

## Routine Monitoring

### Daily
```bash
# Check dashboard is responsive
curl -I https://powercast.pages.dev
# Expected: HTTP/2 200

# Quick metric check (dashboard should be accessible)
curl -s https://powercast.pages.dev | head -20
```

### Weekly (After forecast generation)
```bash
# Verify latest report uploaded
# Check Gumroad dashboard for new preview

# Review Gumroad sales metrics
# Note: Any new subscribers, refunds, or chargebacks?

# Check email for customer inquiries
# Respond within 24 hours
```

### Monthly
```bash
# Review Cloudflare analytics:
curl 'https://api.cloudflare.com/client/v4/accounts/<account_id>/analytics/reports' \
  -H 'Authorization: Bearer <token>'
# Or visit: https://dash.cloudflare.com/ > powercast > Analytics

# Analyze Gumroad revenue metrics
# Calculate: MRR, CAC, LTV

# Review model accuracy trends
# Compare this month's MAPE vs. last month

# Plan next month optimizations
```

---

## Common Commands Reference

### Cloudflare Pages Deployment
```bash
# List projects
wrangler pages project list

# Deploy to specific project
wrangler pages deploy . --project-name=powercast

# View recent deployments
wrangler pages deployment list --project-name=powercast

# Rollback to previous version
wrangler pages deployment rollback --project-name=powercast --id=<deployment_id>

# Tail live logs (real-time)
wrangler pages deployment tail --project-name=powercast

# Check project info
wrangler pages project info powercast
```

### Data Pipeline
```bash
# Fetch data
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/powercast/data
python fetch_ercot.py
python fetch_weather.py
python merge_dataset.py

# Train model
cd ../models
python train_simple_model.py

# Generate report
cd ../reports
python generate_report.py

# View model metrics
cat ../models/backtest_results.json
```

### Git Operations
```bash
# Check status
git status

# Commit changes
git add -A
git commit -m "Message"

# Push to GitHub
git push origin main

# View recent commits
git log --oneline -10
```

---

## Useful Links

### Dashboards & Analytics
- **PowerCast Dashboard:** https://powercast.pages.dev
- **Cloudflare Pages:** https://dash.cloudflare.com/
- **Gumroad Dashboard:** https://gumroad.com/dashboard
- **GitHub Repo:** https://github.com/proximaauto/...

### APIs & Documentation
- **Cloudflare Pages Docs:** https://developers.cloudflare.com/pages/
- **Wrangler CLI:** https://developers.cloudflare.com/workers/cli-wrangler/
- **ERCOT API:** https://www.ercot.com/services/mdt/
- **Gumroad API:** https://app.gumroad.com/api

### Support & Status
- **Cloudflare Status:** https://www.cloudflarestatus.com/
- **Gumroad Status:** https://gumroad.com/api-status
- **Gumroad Support:** support@gumroad.com
- **GitHub Issues:** Create issue if bug found

---

## Troubleshooting Decision Tree

```
Problem: Dashboard not loading?
├─ Check Cloudflare status page
│  ├─ Cloudflare down? → Wait for recovery
│  └─ Cloudflare OK? → Continue
├─ Verify wrangler auth: wrangler whoami
│  ├─ Auth failed? → wrangler login
│  └─ Auth OK? → Continue
├─ Check deployment: wrangler pages deployment list --project-name=powercast
│  ├─ No deployments? → wrangler pages deploy . --project-name=powercast
│  └─ Recent deployment? → Continue
└─ Clear CDN cache
   └─ Redeploy: wrangler pages deploy . --project-name=powercast

Problem: Low/no sales?
├─ Check product links work
│  ├─ Links broken? → Update dashboard with correct URLs
│  └─ Links OK? → Continue
├─ Review product descriptions
│  ├─ Unclear? → Improve copy on Gumroad
│  └─ Clear? → Continue
├─ Check traffic to dashboard
│  ├─ No visitors? → Increase marketing (Reddit, Twitter, HN)
│  └─ Visitors present? → Review conversion rate
└─ Analyze competitor pricing
   └─ Price too high? → Reduce by 25-50% and test

Problem: Model accuracy degraded?
├─ Rebuild dataset with fresh data
├─ Retrain with same model (Prophet)
├─ If MAPE still poor, try alternative model
├─ Test alternative models:
│  ├─ statsforecast (faster, lighter)
│  ├─ ARIMA via pmdarima
│  └─ LSTM in Google Colab (GPU)
└─ Deploy best performing model

Problem: Payment not processing?
├─ Check Gumroad account status
├─ Verify payment method on file
├─ Test payment flow manually
├─ Contact Gumroad support: support@gumroad.com
└─ Post update to dashboard about issue
```

---

## Critical Metrics to Monitor

| Metric | Target | Check Frequency | Alert Threshold |
|--------|--------|-----------------|-----------------|
| Dashboard Uptime | 99.99% | Daily | < 99% |
| Page Load Time | < 200ms | Daily | > 1s |
| Model MAPE | < 12% | Weekly | > 15% |
| Weekly Sales | > 0 | Weekly | 2 weeks no sales |
| Subscriber Churn | < 10%/mo | Monthly | > 20% |
| Dashboard Errors | 0 | Real-time | Any 5xx errors |

---

## Contact Information

- **Founder (Gumroad):** jianou.works@gmail.com
- **DevOps Issues:** devops-hightower
- **Cloudflare Support:** https://support.cloudflare.com/
- **Gumroad Support:** support@gumroad.com
- **Emergency:** Check status page first, then escalate

---

*Last updated: 2026-02-21*
*Version: 1.0*
*Next review: 2026-03-21*
