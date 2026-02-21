#!/usr/bin/env python3
"""
Simple electricity price forecasting model for PowerCast V1.

Uses Prophet (Facebook's time series forecasting library) for simplicity.
Prophet is easier to deploy and maintain than LSTM for V1.

If you want LSTM, open train_lstm.ipynb in Google Colab instead.

Usage:
    python train_simple_model.py

Output:
    model.pkl — Trained Prophet model
    backtest_results.json — Accuracy metrics
"""

import pandas as pd
import numpy as np
from prophet import Prophet
import json
from datetime import datetime, timedelta
import pickle

print("PowerCast Model Training — Prophet Baseline")
print("=" * 60)

# Load dataset
print("\n[1/6] Loading dataset...")
try:
    df = pd.read_csv('../data/dataset.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    print(f"✓ Loaded {len(df):,} records")
except FileNotFoundError:
    print("✗ dataset.csv not found. Run merge_dataset.py first.")
    exit(1)

# Prepare data for Prophet
print("\n[2/6] Preparing data for Prophet...")

# Prophet requires 'ds' (date) and 'y' (target) columns
prophet_df = df[['timestamp', 'LMP']].copy()
prophet_df.columns = ['ds', 'y']

# Add weather as regressor if available
use_weather = 'temperature_c' in df.columns

if use_weather:
    prophet_df['temperature'] = df['temperature_c']
    print("✓ Including temperature as external regressor")

print(f"✓ Prepared {len(prophet_df)} records for training")

# Train/test split
split_date = prophet_df['ds'].max() - timedelta(days=30)  # Last 30 days for testing
train_df = prophet_df[prophet_df['ds'] <= split_date]
test_df = prophet_df[prophet_df['ds'] > split_date]

print(f"\nTrain set: {len(train_df)} records ({train_df['ds'].min()} to {train_df['ds'].max()})")
print(f"Test set: {len(test_df)} records ({test_df['ds'].min()} to {test_df['ds'].max()})")

# Train Prophet model
print("\n[3/6] Training Prophet model...")
print("This may take 2-5 minutes...")

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=True,
    changepoint_prior_scale=0.05,  # Flexibility for trend changes
)

if use_weather:
    model.add_regressor('temperature')

model.fit(train_df)

print("✓ Model training complete")

# Backtest on test set
print("\n[4/6] Backtesting on last 30 days...")

# Create future dataframe for test period
if use_weather:
    future = test_df[['ds', 'temperature']]
else:
    future = test_df[['ds']]

forecast = model.predict(future)

# Calculate accuracy metrics
actual = test_df['y'].values
predicted = forecast['yhat'].values

mae = np.mean(np.abs(actual - predicted))
rmse = np.sqrt(np.mean((actual - predicted) ** 2))
mape = np.mean(np.abs((actual - predicted) / actual)) * 100

# Naive baseline (yesterday's price = today's price)
naive_predictions = test_df['y'].shift(24).dropna().values  # 24-hour lag
naive_actual = test_df['y'].iloc[24:].values
naive_mae = np.mean(np.abs(naive_actual - naive_predictions))
naive_mape = np.mean(np.abs((naive_actual - naive_predictions) / naive_actual)) * 100

print("\n" + "=" * 60)
print("BACKTEST RESULTS (Last 30 Days)")
print("=" * 60)
print(f"\nProphet Model:")
print(f"  MAE: ${mae:.2f}/MWh")
print(f"  RMSE: ${rmse:.2f}/MWh")
print(f"  MAPE: {mape:.2f}%")

print(f"\nNaive Baseline (yesterday = today):")
print(f"  MAE: ${naive_mae:.2f}/MWh")
print(f"  MAPE: {naive_mape:.2f}%")

print(f"\nImprovement over baseline:")
print(f"  MAE improvement: {((naive_mae - mae) / naive_mae * 100):.1f}%")
print(f"  MAPE improvement: {((naive_mape - mape) / naive_mape * 100):.1f}%")

# Price spike detection
spike_threshold = 100  # $100/MWh
spikes_actual = (actual > spike_threshold)
spikes_predicted = (predicted > spike_threshold)

# True positives, false positives, false negatives
tp = np.sum(spikes_actual & spikes_predicted)
fp = np.sum(~spikes_actual & spikes_predicted)
fn = np.sum(spikes_actual & ~spikes_predicted)

precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

print(f"\nPrice Spike Detection (>${spike_threshold}/MWh):")
print(f"  Precision: {precision:.2f}")
print(f"  Recall: {recall:.2f}")
print(f"  F1 Score: {f1:.2f}")

# Save backtest results
backtest_results = {
    'test_period': {
        'start': test_df['ds'].min().isoformat(),
        'end': test_df['ds'].max().isoformat(),
        'days': 30,
        'records': len(test_df)
    },
    'prophet_model': {
        'mae': float(mae),
        'rmse': float(rmse),
        'mape': float(mape)
    },
    'naive_baseline': {
        'mae': float(naive_mae),
        'mape': float(naive_mape)
    },
    'improvement': {
        'mae_improvement_pct': float((naive_mae - mae) / naive_mae * 100),
        'mape_improvement_pct': float((naive_mape - mape) / naive_mape * 100)
    },
    'spike_detection': {
        'threshold': spike_threshold,
        'precision': float(precision),
        'recall': float(recall),
        'f1': float(f1)
    }
}

print("\n[5/6] Saving model and results...")

# Save model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("✓ Model saved: model.pkl")

# Save backtest results
with open('backtest_results.json', 'w') as f:
    json.dump(backtest_results, f, indent=2)
print("✓ Backtest results saved: backtest_results.json")

# Generate 7-day forecast
print("\n[6/6] Generating 7-day ahead forecast...")

future_dates = pd.date_range(
    start=prophet_df['ds'].max() + timedelta(days=1),
    end=prophet_df['ds'].max() + timedelta(days=7),
    freq='H'
)

if use_weather:
    # For simplicity, use historical average temperature by hour
    future_weather = []
    for date in future_dates:
        historical_temp = df[
            (df['timestamp'].dt.month == date.month) &
            (df['timestamp'].dt.hour == date.hour)
        ]['temperature_c'].mean()
        future_weather.append(historical_temp)

    future_df = pd.DataFrame({
        'ds': future_dates,
        'temperature': future_weather
    })
else:
    future_df = pd.DataFrame({'ds': future_dates})

forecast_7d = model.predict(future_df)

print(f"✓ Generated 7-day forecast ({len(forecast_7d)} hours)")
print(f"\nForecast summary (next 7 days):")
print(f"  Mean LMP: ${forecast_7d['yhat'].mean():.2f}/MWh")
print(f"  Min LMP: ${forecast_7d['yhat'].min():.2f}/MWh")
print(f"  Max LMP: ${forecast_7d['yhat'].max():.2f}/MWh")
print(f"  Expected price spikes: {(forecast_7d['yhat'] > spike_threshold).sum()} hours")

# Save forecast
forecast_7d.to_csv('forecast_7day.csv', index=False)
print("✓ Forecast saved: forecast_7day.csv")

print("\n" + "=" * 60)
print("SUCCESS: Model trained and ready for production")
print("=" * 60)
print("\nModel performance assessment:")

if mape < 10:
    print("✓ EXCELLENT: MAPE < 10% — competitive with commercial offerings")
elif mape < 15:
    print("✓ GOOD: MAPE < 15% — acceptable for V1 MVP")
elif mape < 20:
    print("⚠ FAIR: MAPE < 20% — usable but needs improvement")
else:
    print("✗ POOR: MAPE > 20% — consider feature engineering or LSTM upgrade")

print("\nNext steps:")
print("1. Review backtest_results.json")
print("2. Generate weekly forecast report: cd ../reports && python generate_report.py")
print("3. Deploy dashboard to Cloudflare Pages")
