#!/usr/bin/env python3
"""
Generate weekly ERCOT electricity price forecast report.

This is the $99/month product sold on Gumroad.

Usage:
    python generate_report.py

Output:
    weekly_forecast.html — Shareable HTML report
    weekly_forecast.pdf — PDF version (optional, requires wkhtmltopdf)
"""

import pandas as pd
import json
from datetime import datetime
import pickle

print("PowerCast Report Generator — Weekly Forecast")
print("=" * 60)

# Load model and forecast
print("\n[1/4] Loading model and forecast data...")

try:
    with open('../models/model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✓ Model loaded")
except FileNotFoundError:
    print("✗ model.pkl not found. Run train_simple_model.py first.")
    exit(1)

try:
    forecast_df = pd.read_csv('../models/forecast_7day.csv')
    forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])
    print(f"✓ Loaded 7-day forecast ({len(forecast_df)} hours)")
except FileNotFoundError:
    print("✗ forecast_7day.csv not found. Run train_simple_model.py first.")
    exit(1)

try:
    with open('../models/backtest_results.json', 'r') as f:
        backtest = json.load(f)
    print("✓ Loaded backtest results")
except FileNotFoundError:
    print("✗ backtest_results.json not found. Run train_simple_model.py first.")
    backtest = None

# Prepare forecast data for visualization
print("\n[2/4] Processing forecast data...")

# Daily summary
forecast_df['date'] = forecast_df['ds'].dt.date
daily_summary = forecast_df.groupby('date').agg({
    'yhat': ['mean', 'min', 'max']
}).reset_index()
daily_summary.columns = ['date', 'avg_price', 'min_price', 'max_price']

print(f"✓ Prepared daily summary for {len(daily_summary)} days")

# Generate HTML report
print("\n[3/4] Generating HTML report...")

report_date = datetime.now().strftime("%Y-%m-%d")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PowerCast Weekly Forecast — {report_date}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            background: #f8f9fa;
            padding: 20px;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .header {{
            border-bottom: 3px solid #0066cc;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}

        .header h1 {{
            color: #0066cc;
            font-size: 2.2em;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            color: #666;
            font-size: 1.1em;
        }}

        .meta {{
            background: #f0f7ff;
            padding: 15px 20px;
            border-left: 4px solid #0066cc;
            margin-bottom: 30px;
            border-radius: 4px;
        }}

        .meta strong {{
            color: #0066cc;
        }}

        .section {{
            margin-bottom: 40px;
        }}

        .section h2 {{
            color: #333;
            font-size: 1.6em;
            margin-bottom: 15px;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 10px;
        }}

        .forecast-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}

        .forecast-table th,
        .forecast-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }}

        .forecast-table th {{
            background: #f5f5f5;
            font-weight: 600;
            color: #333;
        }}

        .forecast-table tbody tr:hover {{
            background: #fafafa;
        }}

        .price {{
            font-weight: 600;
            color: #0066cc;
        }}

        .price-high {{
            color: #d9534f;
        }}

        .price-low {{
            color: #5cb85c;
        }}

        .accuracy-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}

        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #0066cc;
        }}

        .stat-card .label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}

        .stat-card .value {{
            color: #1a1a1a;
            font-size: 1.8em;
            font-weight: 700;
        }}

        .disclaimer {{
            background: #fff9e6;
            border: 1px solid #ffd700;
            border-radius: 8px;
            padding: 20px;
            margin-top: 40px;
            font-size: 0.9em;
            color: #666;
        }}

        .disclaimer h3 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 1.1em;
        }}

        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
            text-align: center;
            color: #999;
            font-size: 0.9em;
        }}

        .chart-placeholder {{
            background: #f5f5f5;
            border: 2px dashed #ccc;
            border-radius: 8px;
            padding: 60px 20px;
            text-align: center;
            color: #999;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ PowerCast Weekly Forecast</h1>
            <div class="subtitle">ERCOT Day-Ahead Electricity Price Predictions</div>
        </div>

        <div class="meta">
            <strong>Report Date:</strong> {report_date}<br>
            <strong>Forecast Period:</strong> {daily_summary['date'].iloc[0]} to {daily_summary['date'].iloc[-1]}<br>
            <strong>Market:</strong> ERCOT (Texas)<br>
            <strong>Model:</strong> Prophet Time Series Forecasting
        </div>

        <div class="section">
            <h2>📊 7-Day Price Forecast</h2>
            <table class="forecast-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Day</th>
                        <th>Avg Price ($/MWh)</th>
                        <th>Low ($/MWh)</th>
                        <th>High ($/MWh)</th>
                    </tr>
                </thead>
                <tbody>
"""

for _, row in daily_summary.iterrows():
    date_obj = pd.to_datetime(row['date'])
    day_name = date_obj.strftime('%A')

    # Classify price level
    price_class = ''
    if row['avg_price'] > 100:
        price_class = 'price-high'
    elif row['avg_price'] < 30:
        price_class = 'price-low'
    else:
        price_class = 'price'

    html_content += f"""
                    <tr>
                        <td>{row['date']}</td>
                        <td>{day_name}</td>
                        <td class="{price_class}">${row['avg_price']:.2f}</td>
                        <td class="price-low">${row['min_price']:.2f}</td>
                        <td class="price-high">${row['max_price']:.2f}</td>
                    </tr>
"""

html_content += """
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>📈 Hourly Price Chart</h2>
            <div class="chart-placeholder">
                📊 Interactive chart will be added in dashboard version<br>
                <small>For now, see hourly data in forecast_7day.csv</small>
            </div>
        </div>
"""

if backtest:
    mape = backtest['prophet_model']['mape']
    mae = backtest['prophet_model']['mae']
    improvement = backtest['improvement']['mape_improvement_pct']

    html_content += f"""
        <div class="section">
            <h2>✓ Model Accuracy</h2>
            <p>Based on 30-day backtest against actual ERCOT prices:</p>

            <div class="accuracy-stats">
                <div class="stat-card">
                    <div class="label">MAPE (Error Rate)</div>
                    <div class="value">{mape:.1f}%</div>
                </div>
                <div class="stat-card">
                    <div class="label">MAE (Avg Error)</div>
                    <div class="value">${mae:.2f}</div>
                </div>
                <div class="stat-card">
                    <div class="label">vs. Baseline</div>
                    <div class="value">{improvement:.0f}% better</div>
                </div>
            </div>

            <p style="margin-top: 20px; color: #666; font-size: 0.95em;">
                <strong>Interpretation:</strong> Our model's average error is {mape:.1f}% (MAPE), meaning predictions
                are typically within ${mae:.2f}/MWh of actual prices. This is {improvement:.0f}% more accurate
                than a naive "yesterday = today" baseline.
            </p>
        </div>
"""

html_content += """
        <div class="disclaimer">
            <h3>⚠️ Important Disclaimer</h3>
            <p>
                This forecast is provided for informational purposes only and should not be considered
                financial or trading advice. Electricity prices are highly volatile and influenced by
                numerous factors including weather, demand, generation capacity, and transmission
                constraints. Actual prices may differ significantly from forecasts.
            </p>
            <p style="margin-top: 10px;">
                Users should conduct their own due diligence and consult with qualified professionals
                before making any trading or operational decisions based on this forecast.
            </p>
        </div>

        <div class="footer">
            <p><strong>PowerCast</strong> — AI-Powered Electricity Price Forecasting</p>
            <p>Built with Prophet time series forecasting | Data: ERCOT Public API</p>
            <p style="margin-top: 10px;">
                Questions? Contact: <a href="mailto:support@powercast.ai">support@powercast.ai</a>
            </p>
        </div>
    </div>
</body>
</html>
"""

# Save report
output_file = 'weekly_forecast.html'
with open(output_file, 'w') as f:
    f.write(html_content)

print(f"✓ HTML report saved: {output_file}")

# Generate CSV for subscribers
forecast_csv = forecast_df[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
forecast_csv.columns = ['timestamp', 'predicted_price', 'lower_bound', 'upper_bound']
forecast_csv.to_csv('weekly_forecast.csv', index=False)
print("✓ CSV export saved: weekly_forecast.csv")

print("\n[4/4] Report generation complete!")
print("\n" + "=" * 60)
print("SUCCESS: Weekly forecast report ready for distribution")
print("=" * 60)
print(f"\nOutputs:")
print(f"  HTML report: {output_file} (share with subscribers)")
print(f"  CSV data: weekly_forecast.csv (downloadable data)")
print(f"\nNext steps:")
print("1. Review the HTML report in your browser")
print("2. Upload to Gumroad as weekly subscription content")
print("3. Email to subscribers (if using email distribution)")
print("4. Post free sample on landing page")
