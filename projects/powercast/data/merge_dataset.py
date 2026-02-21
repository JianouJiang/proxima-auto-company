#!/usr/bin/env python3
"""
Merge ERCOT LMP data with weather data to create analysis-ready dataset.

This is the dataset we'll sell on Gumroad for $39-$69.

Usage:
    python merge_dataset.py

Output:
    dataset.csv — Analysis-ready dataset for ML training
"""

import pandas as pd

print("PowerCast Data Pipeline — Dataset Merger")
print("=" * 60)

print("\n[1/4] Loading ERCOT LMP data...")
try:
    lmp_df = pd.read_csv('ercot_lmp_data.csv')
    lmp_df['timestamp'] = pd.to_datetime(lmp_df['timestamp'])
    print(f"✓ Loaded {len(lmp_df):,} LMP records")
except FileNotFoundError:
    print("✗ ercot_lmp_data.csv not found. Run fetch_ercot.py first.")
    exit(1)

print("\n[2/4] Loading weather data...")
try:
    weather_df = pd.read_csv('texas_weather_data.csv')
    weather_df['timestamp'] = pd.to_datetime(weather_df['timestamp'])
    print(f"✓ Loaded {len(weather_df):,} weather records")
except FileNotFoundError:
    print("✗ texas_weather_data.csv not found. Run fetch_weather.py first.")
    exit(1)

print("\n[3/4] Merging datasets...")

# Merge on timestamp
merged_df = pd.merge(lmp_df, weather_df, on='timestamp', how='left')

print(f"✓ Merged dataset: {len(merged_df):,} records")
print(f"  Columns: {len(merged_df.columns)}")

# Fill missing weather values with forward fill (weather changes slowly)
merged_df.fillna(method='ffill', inplace=True)

# Drop any remaining NaN rows (first few rows with lag features)
initial_rows = len(merged_df)
merged_df.dropna(inplace=True)
print(f"  Dropped {initial_rows - len(merged_df)} rows with NaN (lag features)")

# Final dataset
print(f"\n✓ Final dataset: {len(merged_df):,} rows × {len(merged_df.columns)} columns")

# Data quality summary
print("\n" + "=" * 60)
print("DATA QUALITY SUMMARY")
print("=" * 60)
print(f"\nTarget variable (LMP):")
print(f"  Mean: ${merged_df['LMP'].mean():.2f}/MWh")
print(f"  Std: ${merged_df['LMP'].std():.2f}/MWh")
print(f"  Min: ${merged_df['LMP'].min():.2f}/MWh")
print(f"  Max: ${merged_df['LMP'].max():.2f}/MWh")
print(f"  Price spikes (>$100/MWh): {(merged_df['LMP'] > 100).sum()} hours")

if 'temperature_c' in merged_df.columns:
    print(f"\nWeather features:")
    print(f"  Temperature range: {merged_df['temperature_c'].min():.1f}°C to {merged_df['temperature_c'].max():.1f}°C")
    print(f"  LMP-Temperature correlation: {merged_df['LMP'].corr(merged_df['temperature_c']):.3f}")

print(f"\nTemporal coverage:")
print(f"  Start: {merged_df['timestamp'].min()}")
print(f"  End: {merged_df['timestamp'].max()}")
print(f"  Duration: {(merged_df['timestamp'].max() - merged_df['timestamp'].min()).days} days")

# Save dataset
output_file = 'dataset.csv'
print(f"\n[4/4] Saving to {output_file}...")
merged_df.to_csv(output_file, index=False)

file_size_mb = pd.io.common.get_filepath_or_buffer(output_file)[0].stat().st_size / 1024 / 1024
print(f"✓ Dataset saved: {output_file} ({file_size_mb:.2f} MB)")

print("\n" + "=" * 60)
print("SUCCESS: Dataset ready for Gumroad sale + ML training")
print("=" * 60)
print("\nThis dataset is now ready to:")
print("1. Sell on Gumroad for $39-$69")
print("2. Use for LSTM model training")
print("3. Share as portfolio work sample")
