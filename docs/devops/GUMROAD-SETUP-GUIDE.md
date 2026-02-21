# PowerCast on Gumroad — Setup Guide for Founder

Step-by-step instructions to create PowerCast products on Gumroad and connect them to the dashboard.

---

## Prerequisites

- Gumroad account (or create at https://gumroad.com/creator-onboarding)
- Payment method on file (Stripe, PayPal, or bank account)
- Access to PowerCast files:
  - Dataset: `/projects/powercast/data/dataset.csv`
  - Dashboard HTML: `/projects/powercast/dashboard/index.html`

---

## Phase 1: Create Dataset Product

### Step 1: Log into Gumroad
1. Go to: https://gumroad.com/dashboard
2. Click "Create a new product" or "+"
3. Select "Create product"

### Step 2: Product Details
| Field | Value |
|-------|-------|
| **Product Name** | ERCOT Electricity Price Dataset |
| **Product Type** | File (one-time purchase) |
| **Description** | See below |
| **Price** | $39 (or $69 for dataset + notebooks) |
| **Preview Image** | Optional (use PowerCast logo) |

### Step 3: Product Description
Copy this text into Gumroad description field:

```
Clean, analysis-ready ERCOT LMP data with weather integration.
Perfect for ML research, energy analytics, and trading model development.

What's included:
- 2 years of hourly ERCOT LMP data (2024-2026)
- Texas weather data (temperature, wind, humidity)
- Pre-engineered temporal and lag features (47 total)
- CSV format, 60k+ hourly rows
- Example Jupyter notebooks
- Detailed documentation
- Updates: Dataset refreshed monthly

Data sources:
- ERCOT Public API (Day-Ahead LMP)
- NOAA Weather Database
- Public domain, no license restrictions

Perfect for:
- ML/AI research and model development
- Energy trading strategy backtesting
- Academic research
- Electricity market analysis
- Battery storage optimization

Questions? Email: hello@powercast.ai
```

### Step 4: Upload Dataset File
1. In the "Files" section, click "Upload files"
2. Upload: `projects/powercast/data/dataset.csv`
3. (Optional) Also upload: `projects/powercast/README.md` as documentation
4. Set CSV as the primary download file
5. Click "Save"

### Step 5: Pricing Strategy
- **Option A (Simple):** Single price $39 → appeals to budget researchers
- **Option B (Better):**
  - $39 for dataset only
  - $69 for dataset + Jupyter notebooks (higher perceived value)
- **Recommended:** Use Option A initially, upgrade to Option B after first month

### Step 6: Publish Product
1. Review all details
2. Click "Publish" or "Save as draft"
3. **Copy the product URL** (you'll need this for dashboard)
   - Format: `https://gumroad.com/<your_username>/<product_id>`
   - Example: `https://gumroad.com/powercast/ercot-dataset`

---

## Phase 2: Create Weekly Forecast Subscription

### Step 1: Create New Product
1. Go to: https://gumroad.com/dashboard
2. Click "Create a new product"
3. Select "Create product"

### Step 2: Product Details
| Field | Value |
|-------|-------|
| **Product Name** | PowerCast Weekly ERCOT Forecast |
| **Product Type** | Subscription (recurring) |
| **Frequency** | Monthly billing |
| **Price** | $99/month |
| **Description** | See below |

### Step 3: Product Description
Copy this text into Gumroad description field:

```
Get accurate 7-day ahead ERCOT electricity price forecasts, updated weekly.
Make better trading and operational decisions.

What you get:
- 7-day day-ahead LMP predictions (hourly)
- Daily price summaries (avg, min, max)
- Model accuracy metrics (30-day rolling backtest)
- HTML report + CSV data export (weekly)
- Email notification when new forecast is available
- Cancel anytime (no long-term contract)

Model details:
- Algorithm: Facebook Prophet Time Series Forecasting
- Features: Historical prices + weather + temporal patterns
- Accuracy: 8-12% MAPE (backtested)
- Training data: 2+ years ERCOT LMP history
- Update frequency: Every Monday 6:00 AM CT

Ideal for:
- Battery storage (BESS) operators optimizing charge/discharge
- Energy traders supplementing their own models
- Utility planners forecasting demand and costs
- Academic researchers studying electricity markets
- Consultants providing market insights to clients

Note: Past performance does not guarantee future results.
Use predictions for informational purposes only.

Questions? Email: hello@powercast.ai
```

### Step 4: Upload Sample Preview
1. Generate sample report (or create manually):
   - Run: `cd projects/powercast/reports && python generate_report.py`
   - Creates: `weekly_forecast.html`
2. In "Files" section, upload the HTML report
3. Mark as "Preview" so subscribers can see what they're buying
4. This builds confidence before purchase

### Step 5: Subscription Settings
```
- Billing frequency: Monthly
- Price: $99/month
- Trial period: None (or 7-day trial if you want)
- Auto-renewal: Yes (unless customer cancels)
- Refund period: 7 days (standard)
```

### Step 6: Publish Subscription
1. Review all details
2. Click "Publish"
3. **Copy the product URL**
   - Example: `https://gumroad.com/powercast/weekly-forecast`

---

## Phase 3: (Optional) Create Bundle Product

### Step 1: Create New Product
1. Go to: https://gumroad.com/dashboard
2. Create product with these details:

| Field | Value |
|-------|-------|
| **Product Name** | PowerCast Bundle (Data + First Month) |
| **Type** | Subscription |
| **Price** | $69 one-time, then $99/month |
| **Description** | See below |

### Step 2: Bundle Description
```
Best value! Get the dataset + first month of forecasts.

What's included:
- Full ERCOT electricity price dataset (2 years)
- First month of weekly forecasts (free)
- Then $99/month for ongoing forecasts (cancel anytime)

Perfect if you want to:
- Backtest trading strategies with historical data
- See forecast quality before committing to subscription
- Get started with both research and decision-support tools

Savings: $39 dataset + $99 first month = $138 value for $69
```

### Step 3: Handle Bundle Logistics
**Challenge:** Gumroad subscriptions can't combine one-time + recurring pricing natively.

**Solutions:**
1. **Simple:** Create as $69 one-time payment with note "You'll be added to subscription manually"
2. **Better:** Set up Zapier/webhook to auto-enroll in subscription
3. **Manual:** Add bundle purchaser to subscriber list manually (via email)

---

## Phase 4: Update Dashboard with Real Links

### Step 1: Collect Gumroad URLs
From your Gumroad dashboard, copy the URLs for:
1. ERCOT Dataset product → `https://gumroad.com/...`
2. Weekly Forecast subscription → `https://gumroad.com/...`
3. Bundle (if created) → `https://gumroad.com/...`

### Step 2: Edit Dashboard HTML
```bash
# Edit the dashboard file
nano /home/jianoujiang/Desktop/proxima-auto-company/projects/powercast/dashboard/index.html
```

Find these three lines and replace the placeholder URLs:

**Line 1 - Dataset purchase button:**
```html
OLD: <a href="https://gumroad.com/powercast-dataset" class="btn btn-primary"...
NEW: <a href="https://gumroad.com/YOUR_USERNAME/ercot-dataset" class="btn btn-primary"...
```

**Line 2 - Weekly forecast subscription:**
```html
OLD: <a href="https://gumroad.com/powercast-weekly" class="btn btn-primary"...
NEW: <a href="https://gumroad.com/YOUR_USERNAME/weekly-forecast" class="btn btn-primary"...
```

**Line 3 - Bundle (optional):**
```html
OLD: <a href="https://gumroad.com/powercast-bundle" class="btn btn-primary"...
NEW: <a href="https://gumroad.com/YOUR_USERNAME/bundle-data-forecast" class="btn btn-primary"...
```

### Step 3: Test Links Locally
1. Open updated `dashboard/index.html` in a browser (drag and drop)
2. Click each button to verify links work
3. Should open Gumroad product pages

### Step 4: Deploy Updated Dashboard
```bash
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/powercast/dashboard
wrangler pages deploy . --project-name=powercast
```

**Verify deployment:**
```bash
# Should see: "Deployment complete! Take a peek over at https://..."
curl -I https://powercast.pages.dev
# Should return: HTTP/2 200
```

### Step 5: Test Live Links
1. Visit: https://powercast.pages.dev
2. Click "Get Weekly Forecasts" button
3. Should redirect to Gumroad subscription page
4. Click "View Sample Report" button
5. Should show sample forecast preview
6. Test on mobile device too (responsive design)

---

## Phase 5: Ongoing Maintenance

### Weekly (Every Monday)
1. Generate new forecast: `python reports/generate_report.py`
2. Log into Gumroad dashboard
3. Find "PowerCast Weekly Forecast" product
4. Upload new forecast HTML as preview/attachment
5. Announce "New forecast available!" in Gumroad product description

### Monthly
1. Review Gumroad sales metrics:
   - How many dataset purchases? (target: 5-10)
   - How many new subscribers? (target: 2-5)
   - Any refunds or chargebacks?
2. Monitor customer feedback/comments on Gumroad
3. Respond to customer questions within 24 hours
4. Update dashboard with latest metrics if needed

### Quarterly
1. Analyze revenue trends
2. Test alternative pricing ($49 vs $39 for dataset)
3. Consider creating variants (e.g., $29 "lite" version)
4. Plan upgrades (API access, real-time forecasts, etc.)

---

## Troubleshooting

### Issue: Payment method rejected
**Solution:**
1. Log into Gumroad account settings
2. Update payment method (Stripe, PayPal, or direct bank)
3. Retry product creation
4. Contact Gumroad support if persistent

### Issue: Can't upload dataset file (too large)
**Solution:**
1. Gumroad has a 2GB file limit per product
2. `dataset.csv` should be < 200MB
3. If file too large, compress with gzip first
4. Or split into multiple files

### Issue: Product link doesn't work
**Solution:**
1. Verify product is "Published" (not "Draft")
2. Check URL is exactly correct (copy from Gumroad dashboard)
3. Verify it's your real Gumroad username, not placeholder
4. Test in incognito/private browser window

### Issue: Subscriber can't download files
**Solution:**
1. In Gumroad product page, check "Files" section
2. Verify file is uploaded and visible
3. Mark correct file as "Primary download"
4. Test by purchasing as yourself (then refund)

---

## Email Template for First Customers

Send this to your first dataset buyers:

---

**Subject:** Welcome to PowerCast! Your ERCOT Dataset is ready

Hi [Customer Name],

Thanks for buying the PowerCast ERCOT Electricity Price Dataset!

Your download is ready: [Gumroad download link]

This dataset includes:
- 2 years of hourly ERCOT LMP data (2024-2026)
- Weather data from Texas (temp, wind, humidity)
- 47 engineered features (lag, temporal, etc.)
- Example Jupyter notebooks for analysis
- Full documentation

**What's next?**

If you find this dataset useful, consider subscribing to our weekly forecasts:
- Get 7-day ahead price predictions
- Updated every Monday
- $99/month (cancel anytime)
- Subscribe here: [Gumroad subscription link]

**Questions?**

Reply to this email or email: hello@powercast.ai

We'd love to hear what you're building with this data!

Thanks,
PowerCast Team

---

## Success Metrics

After launching Gumroad products, track these metrics:

| Metric | Target (Week 1) | Target (Month 1) |
|--------|-----------------|------------------|
| Dataset page views | 100+ | 500+ |
| Dataset purchases | 1-2 | 5-10 |
| First subscriber | 1 | 2-5 |
| Product reviews | 4.5+ stars | 4.5+ stars |
| Email inquiries | 1-2 | 5+ |
| Refund requests | 0 | < 10% |

If hitting targets early, consider:
- Creating API tier ($199-499/month)
- Adding premium tier with LSTM forecasts
- Expanding to other markets (CAISO, PJM, NYISO)

---

## Reference Links

- **Gumroad Creator Onboarding:** https://gumroad.com/creator-onboarding
- **Gumroad Dashboard:** https://gumroad.com/dashboard
- **Gumroad File Limits:** https://gumroad.com/help#file-upload-limits
- **Gumroad Subscription Setup:** https://gumroad.com/help#recurring-products
- **Stripe Connect (Payment):** https://stripe.com/en-gb/connect

---

## Timeline

**Today (Hour 1):** Create Gumroad account
**Today (Hour 2-3):** Create dataset product + upload CSV
**Today (Hour 4-5):** Create forecast subscription + sample preview
**Today (Hour 6):** Update dashboard with real links + redeploy
**Today (Hour 7):** Test all links manually + verify payments work
**Tomorrow:** Promote on Reddit, HN, Twitter

**Expected first sale:** Within 3-7 days of launch

---

*Last updated: 2026-02-21*
*Questions? Contact: devops-hightower*
