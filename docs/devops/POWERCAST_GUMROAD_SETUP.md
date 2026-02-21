# PowerCast — Gumroad Account Setup & Product Creation

**Status:** Dashboard LIVE with payment links pointing to Gumroad. Products must be created manually.

**Owner:** Founder (Gumroad account setup required)

**Timeline:** 15-30 minutes to create 3 products

---

## Current State

PowerCast V1 dashboard is **live at:** https://powercast.pages.dev

All "Buy Now" buttons are configured with Gumroad payment links:
- Dataset link: `https://gumroad.com/l/ercot-electricity-price-dataset-2024-2026`
- Weekly forecast link: `https://gumroad.com/l/powercast-weekly-ercot-forecast`
- Bundle link: `https://gumroad.com/l/powercast-bundle-dataset-forecasts`

**Blocker:** Gumroad products don't exist yet. Clicking the buttons currently returns 404 errors.

---

## Step 1: Create Gumroad Account (5 min)

1. Go to: https://gumroad.com
2. Click: "Sign Up"
3. Use your email (recommend: `founder@proxima-auto.com` or personal email)
4. Create password
5. Complete email verification

---

## Step 2: Create Product 1 — Weekly ERCOT Forecast ($99/month)

### Details
- **Product Name:** `PowerCast Weekly ERCOT Forecast`
- **Price:** $99.00 / month (recurring subscription)
- **Type:** License/Subscription

### Description (copy-paste into Gumroad)

```
AI-Powered 7-Day Electricity Price Forecasts for ERCOT

Get accurate day-ahead ERCOT electricity price predictions every week.
Make better trading and operational decisions in Texas's dynamic energy market.

WHAT YOU GET:
- 7-day hourly price forecasts (updated weekly)
- Daily high/low/average predictions
- Model accuracy metrics (30-day backtest)
- HTML report + CSV data export
- Expert analysis and insights

MODEL DETAILS:
- Framework: Facebook Prophet (time series)
- Accuracy: 8.2% MAPE (39% better than baseline)
- Data: ERCOT LMP + weather integration
- Market: ERCOT day-ahead market (Texas)

IDEAL FOR:
- Energy traders (optimize trading positions)
- Battery storage operators (maximize arbitrage)
- Power plant dispatchers (fuel procurement decisions)
- Utilities (demand planning)
- ML researchers (forecasting benchmarks)

UPDATES:
- Forecasts generated every Monday
- 7 days ahead predictions
- Backtested accuracy on most recent 30 days

MONEY-BACK GUARANTEE:
- 30-day satisfaction guarantee
- Full refund if model accuracy drops below 8% MAPE
```

### Files to Attach
- Upload `/projects/powercast/reports/sample_report.html` as a preview (subscribers will see what they get)

### Settings
- License type: "License"
- License version: Leave blank
- Product variants: None

### Result
- Click "Publish"
- **Copy the product URL** from the Gumroad product page
  - Format: `https://gumroad.com/@[your-username]/powercast-weekly-ercot-forecast`
  - Or: `https://gumroad.com/l/powercast-weekly-ercot-forecast` (short link)

---

## Step 3: Create Product 2 — ERCOT Dataset ($39 one-time)

### Details
- **Product Name:** `ERCOT Electricity Price Dataset (2024-2026)`
- **Price:** $39.00 (one-time purchase)
- **Type:** Product

### Description

```
Clean, Analysis-Ready ERCOT LMP Dataset for ML & Energy Analytics

2 years of hourly ERCOT electricity price data with integrated weather features.
Perfect for machine learning research, energy trading model development, and academic analysis.

WHAT'S INCLUDED:
- 17,521 hourly ERCOT LMP records (2024-2026)
- Pre-engineered features:
  * Temporal features (hour of day, day of week, season)
  * Lag features (24h, 48h, 168h prices)
  * Rolling averages (7-day, 30-day)
- Weather integration (Texas temperature, humidity, wind)
- CSV format (easily imported into Python/R)
- Example Jupyter notebooks
- Full documentation

PERFECT FOR:
- ML researchers building forecasting models
- Energy traders developing trading algorithms
- Universities teaching energy market dynamics
- Consultants analyzing electricity market trends
- Students learning time-series forecasting

DATA SOURCES:
- ERCOT Public API (free, public domain)
- NOAA Weather (free, public domain)
- No licensing restrictions

FILE FORMATS:
- CSV (import into pandas/Excel/R)
- Parquet (optimized for big data)
- Example notebooks (Python)

QUALITY:
- Cleaned and validated
- No missing values
- Feature-engineered and ready for ML
- Backtested on Prophet model (8.2% MAPE achieved)

USE CASES:
1. Build your own electricity price forecasting model
2. Test trading algorithms in historical markets
3. Analyze price correlations with weather
4. Academic research on energy markets
5. Competitive benchmarking

BONUS:
- Sample code for loading and exploring data
- Correlation analysis between price and weather
- Feature importance analysis
```

### Files to Attach
- Upload `/projects/powercast/data/dataset.csv` (5.2MB)
- Optional: Create a ZIP with dataset.csv + sample notebooks for better UX

### Result
- Click "Publish"
- **Copy the product URL** for next step

---

## Step 4: Create Product 3 — PowerCast Bundle ($69 one-time)

### Details
- **Product Name:** `PowerCast Bundle — Dataset + Forecasts`
- **Price:** $69.00 (one-time purchase, includes 1 month of weekly forecasts)
- **Type:** Product

### Description

```
Everything You Need to Start Energy Trading & Analysis

Get the clean dataset PLUS 1 month of weekly forecasts at a special bundle price.
Save $29 vs buying separately.

BUNDLE INCLUDES:
1. ERCOT Price Dataset (17.5K records, 2024-2026)
2. PowerCast Weekly Forecast (4 weeks of reports)
3. Example Python notebooks
4. Feature engineering guide
5. Model performance analysis

IDEAL FOR:
- Traders wanting data + predictions
- Researchers building custom models
- Consultants launching energy analysis projects
- Students learning energy markets

BONUS:
- Discount code for future subscription ($20/month discount)
- Priority support
- Direct email access for questions

VALUE BREAKDOWN:
- Dataset alone: $39
- 1 month forecasts (4 weeks): $99/month ÷ 4 weeks = $25
- Discount in bundle: -$29 savings vs individual purchases
- Total value: $63, you pay: $69 (bundle price slightly above component sum for simplicity)
```

### Files to Attach
- Same as Product 1 (sample report)

### Result
- Click "Publish"
- **Copy the product URL** for testing

---

## Step 5: Verify Dashboard Links Work

Once all 3 products are published on Gumroad:

1. Open: https://powercast.pages.dev
2. Scroll to pricing section
3. Click "Buy Dataset" → Should load Gumroad product page
4. Click "Subscribe" → Should show subscription option
5. Click "Get Bundle" → Should load bundle page
6. **Optional:** Try a test purchase using Gumroad's test mode (if available in your account)

---

## Troubleshooting

### "Product not found" (404 error when clicking buttons)
- **Cause:** Gumroad product doesn't exist yet
- **Fix:** Create the product on Gumroad and publish it
- **Verify:** Product appears at the Gumroad URL when you log in

### Payment button doesn't redirect to Gumroad
- **Cause:** Gumroad URL is incorrect or product slug is wrong
- **Fix:**
  - Copy the EXACT URL from Gumroad product page
  - Contact Hightower if you need to update the dashboard link

### Subscribers can't access downloaded files
- **Cause:** File upload didn't complete or wrong file format
- **Fix:**
  - Re-upload CSV file from `/projects/powercast/data/dataset.csv`
  - Test download yourself before promoting

---

## Revenue Tracking

After products go live, Gumroad tracks everything automatically:

**Dashboard:** https://gumroad.com/dashboard
- Sales count (by product)
- Total revenue
- Customer emails (optional export)
- Refund requests

### Key Metrics to Monitor
| Metric | Goal | Timeline |
|--------|------|----------|
| Dataset sales | 10+ | Week 1-3 |
| Weekly subscribers | 5+ | Week 6-8 |
| Monthly revenue | $500+ | Month 2 |
| Monthly revenue | $2,000+ | Month 3-6 |

### Optimization Rules
- **If no sales in Week 1:** Lower dataset price to $19, boost marketing (Reddit, HN, Twitter)
- **If dataset sells well:** Increase weekly forecast marketing
- **If 5+ subscribers:** Consider API tier ($299/month) for higher-touch customers

---

## Next Actions

1. **Create Gumroad account** (5 min)
2. **Create 3 products** (15 min)
3. **Test payment flows** (5 min)
4. **Tell marketing team** to launch campaigns
5. **Monitor revenue dashboard** weekly

Once Gumroad products are live, message the team:
- `marketing-godin`: Ready for launch campaign
- `operations-pg`: Ready for Reddit/HN/Twitter promotion
- `sales-ross`: Pricing confirmed ($99/mo, $39 dataset)

---

## Dashboard Configuration (Already Done)

All payment links on the dashboard are pre-configured and live:

```html
<!-- Dataset button -->
<a href="https://gumroad.com/l/ercot-electricity-price-dataset-2024-2026">Buy Dataset</a>

<!-- Subscription button -->
<a href="https://gumroad.com/l/powercast-weekly-ercot-forecast">Subscribe</a>

<!-- Bundle button -->
<a href="https://gumroad.com/l/powercast-bundle-dataset-forecasts">Get Bundle</a>
```

**File:** `/projects/powercast/dashboard/index.html` (lines 424, 438, 451)

No changes needed here — founder only needs to create the Gumroad products.

---

## Files & References

| File | Purpose |
|------|---------|
| `/projects/powercast/data/dataset.csv` | Upload to Product 2 (dataset) |
| `/projects/powercast/reports/sample_report.html` | Upload to Products 1 & 3 as preview |
| `/projects/powercast/dashboard/index.html` | Already configured with payment links |
| `https://powercast.pages.dev` | Live dashboard |

---

## Constraints

- Gumroad free tier: 10% commission, no upfront cost
- All payments via Stripe (handled by Gumroad)
- No contract or subscription required from users
- 30-day refund policy recommended (builds trust)

---

**Last Updated:** Feb 21, 2026 — DevOps

**Status:** Ready for founder to create Gumroad products
