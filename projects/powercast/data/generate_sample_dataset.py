#!/usr/bin/env python3
"""
Generate synthetic but realistic ERCOT electricity price data for V1 MVP.

This script creates 2 years of hourly LMP data with realistic patterns:
- Daily seasonality (peaks at midday and evening)
- Weekly seasonality (weekday > weekend)
- Seasonal trends (summer/winter spikes)
- Random noise and occasional price spikes

This allows us to train and test the model immediately without waiting
for actual ERCOT API data.

Usage:
    python generate_sample_dataset.py

Output:
    dataset.csv - Ready for model training
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("PowerCast Sample Data Generator")
print("=" * 60)

# Generate 2 years of hourly data
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
dates = pd.date_range(start=start_date, end=end_date, freq='h')

print(f"\n[1/3] Generating {len(dates):,} hourly timestamps...")
print(f"Date range: {start_date.date()} to {end_date.date()}")

# Base price model
np.random.seed(42)

# 1. Trend component (seasonal)
days_since_start = np.arange(len(dates)) / 24  # Convert hours to days
year_progress = (days_since_start % 365) / 365

# Summer/winter cycle (higher prices in summer and winter, lower in spring/fall)
seasonal_cycle = 20 * (np.sin(2 * np.pi * year_progress) + 0.5)

# 2. Daily cycle (peak at noon and evening)
hour_of_day = dates.hour.values
daily_cycle = 15 * (1 + np.sin(np.pi * (hour_of_day - 6) / 12))
daily_cycle[hour_of_day < 6] = 5  # Low at night
daily_cycle[hour_of_day > 22] = 5  # Low at late night

# 3. Weekly cycle (weekends lower)
day_of_week = dates.dayofweek.values
weekly_cycle = np.where(day_of_week >= 5, -5, 3)  # Weekends -5, weekdays +3

# 4. Random noise and spikes
noise = np.random.normal(0, 3, len(dates))
spikes = np.random.poisson(0.05, len(dates)) * np.random.exponential(50, len(dates))

# Combine all components
base_price = 40  # Average ERCOT LMP
lmp_prices = base_price + seasonal_cycle + daily_cycle + weekly_cycle + noise + spikes
lmp_prices = np.maximum(lmp_prices, 0)  # No negative prices

# Add realistic components
energy = lmp_prices * 0.85  # Energy component ~85% of LMP
congestion = lmp_prices * 0.10  # Congestion ~10%
loss = lmp_prices * 0.05  # Loss ~5%

# Create dataframe
df = pd.DataFrame({
    'timestamp': dates,
    'LMP': lmp_prices,
    'Energy': energy,
    'Congestion': congestion,
    'Loss': loss,
})

print(f"✓ Generated {len(df):,} price records")
print(f"\nPrice statistics:")
print(f"  Mean: ${df['LMP'].mean():.2f}/MWh")
print(f"  Median: ${df['LMP'].median():.2f}/MWh")
print(f"  Min: ${df['LMP'].min():.2f}/MWh")
print(f"  Max: ${df['LMP'].max():.2f}/MWh")
print(f"  Std Dev: ${df['LMP'].std():.2f}/MWh")
print(f"  Price spikes (>$100/MWh): {(df['LMP'] > 100).sum()} hours")

# Add temporal features
print("\n[2/3] Engineering temporal features...")

df['year'] = df['timestamp'].dt.year
df['month'] = df['timestamp'].dt.month
df['day'] = df['timestamp'].dt.day
df['hour'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
df['quarter'] = df['timestamp'].dt.quarter

# Lag features
for lag in [1, 2, 3, 6, 12, 24, 168]:
    df[f'LMP_lag_{lag}h'] = df['LMP'].shift(lag)

# Rolling averages
for window in [3, 6, 12, 24]:
    df[f'LMP_rolling_{window}h'] = df['LMP'].rolling(window).mean()

print(f"✓ Added {len(df.columns) - 5} temporal and lag features")

# Save
print("\n[3/3] Saving dataset...")
output_file = 'dataset.csv'
df.to_csv(output_file, index=False)

print(f"✓ Dataset saved: {output_file}")
print(f"  Size: {len(df):,} rows × {len(df.columns)} columns")

print("\n" + "=" * 60)
print("SUCCESS: Sample dataset ready for model training")
print("=" * 60)
print("\nNext step: python ../models/train_simple_model.py")
