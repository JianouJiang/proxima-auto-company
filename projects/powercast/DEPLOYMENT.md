# PowerCast Deployment Guide

## Quick Start

PowerCast V1 is designed to ship in HOURS not weeks. Follow these steps.

## Phase 1: Data Pipeline (2-3 hours)

### 1. Install Dependencies

```bash
cd projects/powercast
pip install -r requirements.txt
```

**Note:** Prophet requires pystan which can be slow to compile. If installation fails:

```bash
# Alternative: use statsforecast (lighter, faster)
pip install statsforecast
# OR use Google Colab for training
```

### 2. Fetch Data

```bash
cd data/

# Fetch ERCOT data (may require ERCOT API registration)
python fetch_ercot.py

# Fetch weather data
python fetch_weather.py

# Merge into single dataset
python merge_dataset.py
```

**Expected outputs:**
- `ercot_lmp_data.csv` (~50-100 MB, 2 years hourly)
- `texas_weather_data.csv` (~5-10 MB)
- `dataset.csv` (~60-120 MB, merged and ready)

**If ERCOT API fails:**
1. Register at: https://www.ercot.com/services/mdt/data-portal
2. Or manually download historical data: https://www.ercot.com/mp/data-products/data-product-details?id=NP6-785-CD
3. Place in `data/` directory as `ercot_manual.csv`

### 3. Upload Dataset to Gumroad (IMMEDIATE REVENUE)

1. Go to: https://gumroad.com
2. Create product: "ERCOT Electricity Price Dataset (2024-2026)"
3. Description:
   ```
   Clean, analysis-ready ERCOT LMP data with weather integration.
   Perfect for ML research, energy analytics, and trading model development.

   What's included:
   - 2 years of hourly ERCOT LMP data
   - Texas weather data (temperature, wind, humidity)
   - Pre-engineered temporal and lag features
   - CSV format, 60k+ rows
   - Example Jupyter notebooks
   - Documentation

   Data sources: ERCOT Public API + NOAA Weather
   ```
4. Upload: `dataset.csv` + `README.md` as ZIP
5. Price: $39 (dataset only) or $69 (dataset + notebooks)
6. Publish immediately

**Time to first dollar: Week 1-2** (depends on promotion)

## Phase 2: Model Training (3-4 hours)

### Option A: Simple Prophet Model (Recommended for V1)

```bash
cd models/
python train_simple_model.py
```

This will:
- Train Prophet model on historical data
- Backtest last 30 days
- Generate accuracy metrics
- Save model.pkl and backtest_results.json
- Create 7-day forecast

**Target accuracy:** MAPE < 12% (acceptable for V1)

### Option B: LSTM in Google Colab (Better accuracy, more complex)

1. Open: https://colab.research.google.com
2. Upload `data/dataset.csv`
3. Create new notebook with LSTM training code
4. Train on free GPU (15-30 min)
5. Download `model.h5` and accuracy metrics
6. Save to `models/`

**Target accuracy:** MAPE < 8% (competitive)

## Phase 3: Weekly Report (2 hours)

### Generate First Report

```bash
cd reports/
python generate_report.py
```

Outputs:
- `weekly_forecast.html` — Shareable HTML report
- `weekly_forecast.csv` — Raw data export

### Upload to Gumroad

1. Create product: "PowerCast Weekly ERCOT Forecast"
2. Type: **Subscription** (recurring)
3. Description:
   ```
   Get accurate 7-day ahead ERCOT electricity price forecasts,
   updated weekly. Make better trading and operational decisions.

   What you get:
   - 7-day day-ahead LMP predictions
   - Daily price averages, minimums, maximums
   - Hourly granularity
   - Model accuracy metrics (30-day backtest)
   - HTML report + CSV data export
   - Weekly updates every Monday

   Model: Prophet time series with weather integration
   Accuracy: 8-12% MAPE (backtested)
   Market: ERCOT (Texas)
   ```
4. Price: $99/month
5. Upload sample report as free preview
6. Publish

**Time to first subscriber: Week 6-8** (with promotion)

## Phase 4: Dashboard Deployment (1 hour)

### Deploy to Cloudflare Pages

```bash
cd dashboard/

# Initialize Cloudflare Pages
wrangler pages project create powercast

# Deploy
wrangler pages deploy . --project-name=powercast
```

This creates:
- Public landing page: `https://powercast.pages.dev`
- Shows forecast preview
- Links to Gumroad products
- Sample report
- Pricing tiers

### Update Links

After Gumroad products are live, update `dashboard/index.html`:

1. Replace `https://gumroad.com/powercast-dataset` with real dataset link
2. Replace `https://gumroad.com/powercast-weekly` with real subscription link
3. Replace `https://gumroad.com/powercast-bundle` with real bundle link

Then redeploy:

```bash
wrangler pages deploy . --project-name=powercast
```

## Phase 5: Automation (Optional, 2-3 hours)

### Weekly Forecast Automation

**Option A: GitHub Actions (Free)**

Create `.github/workflows/weekly_forecast.yml`:

```yaml
name: Generate Weekly Forecast

on:
  schedule:
    - cron: '0 6 * * 1'  # Every Monday 6 AM
  workflow_dispatch:  # Manual trigger

jobs:
  forecast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: cd models && python train_simple_model.py
      - run: cd reports && python generate_report.py
      - uses: actions/upload-artifact@v3
        with:
          name: weekly-forecast
          path: reports/weekly_forecast.*
```

**Option B: Manual Weekly (5 min/week)**

1. Every Monday morning:
   ```bash
   cd models && python train_simple_model.py
   cd reports && python generate_report.py
   ```
2. Upload `weekly_forecast.html` to Gumroad subscribers

## Promotion Strategy

### Week 1: Launch Dataset

1. Post on Reddit:
   - r/MachineLearning (2.9M subscribers)
   - r/datasets (400K subscribers)
   - r/energy (50K subscribers)
   - r/datascience (1.5M subscribers)

2. Post on Hacker News:
   - Title: "Show HN: Clean ERCOT electricity price dataset for ML research"
   - Include: link to dataset, sample notebook, accuracy benchmarks

3. Post on Twitter/X:
   - Tag: #MachineLearning #EnergyTrading #ERCOT #DataScience
   - Share sample visualizations

### Week 2-3: Monitor Sales

- Goal: 5-10 dataset sales
- If hit goal → proceed to weekly report
- If miss goal → adjust pricing or pivot

### Week 6-8: Launch Weekly Report

1. Email dataset buyers:
   - "You bought our dataset — now get weekly forecasts"
   - Offer 20% discount for first month

2. Post sample report:
   - Reddit: r/energy, r/trading
   - HN: "Show HN: AI-powered electricity price forecasts for ERCOT"
   - Twitter: Share forecast accuracy metrics

3. Content marketing:
   - "How we predict ERCOT prices with 9% MAPE"
   - "Why ERCOT is the most volatile electricity market"
   - "Battery storage arbitrage opportunities in Texas"

## Success Metrics

### Phase 1 Success (Dataset)
- 10+ sales at $39-$69
- $390-$690 revenue
- **Time to achieve:** 2-3 weeks

### Phase 2 Success (Weekly Report)
- 5+ subscribers at $99/month
- $495/month MRR
- **Time to achieve:** 6-8 weeks

### Phase 3 Success (Sustainable)
- 20+ subscribers
- $2,000/month MRR
- **Time to achieve:** 3-6 months

## Maintenance

### Weekly (30 min)
- Run model training
- Generate report
- Upload to Gumroad
- Monitor accuracy metrics

### Monthly (2 hours)
- Review accuracy vs. actual prices
- Adjust model if MAPE degrades
- Update landing page with latest metrics
- Respond to customer questions

## Troubleshooting

### ERCOT API fails
- Use manual download: https://www.ercot.com/mp/data-products
- Or use historical CSVs from Grid Status: https://www.gridstatus.io

### Prophet installation fails
- Use Google Colab for training
- Or switch to `statsforecast` library (lighter)
- Or use simple ARIMA via `pmdarima`

### Model accuracy poor (MAPE > 15%)
- Add more weather features
- Extend training data to 3+ years
- Upgrade to LSTM/Transformer
- Engineer better lag features

### No sales after 2 weeks
- Lower price to $19 for dataset
- Post to more communities
- Share free sample on landing page
- Improve SEO (blog posts)

## Next Steps After V1

If PowerCast hits $500/month revenue:

1. **API Access** — $199-$499/month for programmatic access
2. **Real-time Updates** — Intraday forecasts every 4 hours
3. **Multi-market** — Expand to CAISO, PJM, NYISO
4. **Custom Models** — LSTM/Transformer upgrade for enterprise tier
5. **Spike Alerts** — Email/SMS when prices forecast > $100/MWh

## Budget Tracking

**Total infrastructure cost: $0**

All components use free tiers:
- Cloudflare Pages: Free (unlimited bandwidth)
- Gumroad: Free (10% commission on sales)
- GitHub Actions: 2,000 min/month free
- Google Colab: Free GPU access
- ERCOT/NOAA APIs: Free public data

**Only costs:**
- Anthropic API (LLM): ~$3-7/week
- Time: ~15-20 hours for V1 build

**Break-even:** 1 subscriber at $99/month covers API costs

---

**Ready to ship? Start with Phase 1 data pipeline. Ship dataset to Gumroad within 48 hours.**
