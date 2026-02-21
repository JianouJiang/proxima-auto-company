#!/usr/bin/env python3
"""
Fetch ERCOT electricity price data using gridstatus library.

This script pulls 2 years of historical LMP (Locational Marginal Price) data
from ERCOT's public API via the gridstatus library.

Usage:
    python fetch_ercot.py

Output:
    ercot_lmp_data.csv — 2 years of ERCOT LMP data with hourly aggregation
"""

import pandas as pd
from datetime import datetime, timedelta
import gridstatus

print("PowerCast Data Pipeline — ERCOT LMP Fetcher")
print("=" * 60)

# Initialize ERCOT client
print("\n[1/5] Initializing ERCOT API client...")
try:
    ercot = gridstatus.ERCOT()
    print("✓ ERCOT client initialized")
except Exception as e:
    print(f"✗ Failed to initialize ERCOT client: {e}")
    exit(1)

# Define date range: 2 years of data
end_date = datetime.now()
start_date = end_date - timedelta(days=730)  # 2 years

print(f"\n[2/5] Fetching LMP data from {start_date.date()} to {end_date.date()}...")
print("This may take several minutes for 2 years of 5-minute interval data...")

try:
    # Fetch real-time LMP data
    # ERCOT provides LMP at 5-minute intervals across hundreds of settlement points
    # For V1, we'll use the hub average (HOUSTON, NORTH, SOUTH, WEST hubs)

    lmp_data = ercot.get_lmp(
        date=start_date.strftime("%Y%m%d"),
        end=end_date.strftime("%Y%m%d"),
        market="DAM"  # Day-Ahead Market
    )

    print(f"✓ Fetched {len(lmp_data)} records")
    print(f"  Date range: {lmp_data['Time'].min()} to {lmp_data['Time'].max()}")
    print(f"  Settlement points: {lmp_data['Location'].nunique()} unique locations")

except Exception as e:
    print(f"✗ Failed to fetch LMP data: {e}")
    print("\nNote: ERCOT API may require registration. Fallback to manual download.")
    print("Visit: https://www.ercot.com/mp/data-products/data-product-details?id=NP6-785-CD")
    exit(1)

# Process data: aggregate to hourly hub averages
print("\n[3/5] Processing data...")

# Filter to major hubs only (reduces noise)
major_hubs = ['HB_HOUSTON', 'HB_NORTH', 'HB_SOUTH', 'HB_WEST', 'HB_BUSAVG']
lmp_hub = lmp_data[lmp_data['Location'].isin(major_hubs)].copy()

# Convert to datetime and aggregate hourly
lmp_hub['Time'] = pd.to_datetime(lmp_hub['Time'])
lmp_hub['Hour'] = lmp_hub['Time'].dt.floor('H')

# Calculate hourly average LMP across all hubs
lmp_hourly = lmp_hub.groupby('Hour').agg({
    'LMP': 'mean',
    'Energy': 'mean',
    'Congestion': 'mean',
    'Loss': 'mean'
}).reset_index()

lmp_hourly.rename(columns={'Hour': 'timestamp'}, inplace=True)

print(f"✓ Aggregated to {len(lmp_hourly)} hourly records")
print(f"  Average LMP: ${lmp_hourly['LMP'].mean():.2f}/MWh")
print(f"  LMP range: ${lmp_hourly['LMP'].min():.2f} - ${lmp_hourly['LMP'].max():.2f}/MWh")
print(f"  Price spikes (>$100/MWh): {(lmp_hourly['LMP'] > 100).sum()} hours ({(lmp_hourly['LMP'] > 100).sum() / len(lmp_hourly) * 100:.2f}%)")

# Add temporal features for ML
print("\n[4/5] Engineering temporal features...")

lmp_hourly['year'] = lmp_hourly['timestamp'].dt.year
lmp_hourly['month'] = lmp_hourly['timestamp'].dt.month
lmp_hourly['day'] = lmp_hourly['timestamp'].dt.day
lmp_hourly['hour'] = lmp_hourly['timestamp'].dt.hour
lmp_hourly['day_of_week'] = lmp_hourly['timestamp'].dt.dayofweek
lmp_hourly['is_weekend'] = lmp_hourly['day_of_week'].isin([5, 6]).astype(int)
lmp_hourly['quarter'] = lmp_hourly['timestamp'].dt.quarter

# Lag features (previous hours' prices)
for lag in [1, 2, 3, 6, 12, 24, 168]:  # 1h, 2h, 3h, 6h, 12h, 24h, 7d
    lmp_hourly[f'LMP_lag_{lag}h'] = lmp_hourly['LMP'].shift(lag)

# Rolling averages
for window in [3, 6, 12, 24]:
    lmp_hourly[f'LMP_rolling_{window}h'] = lmp_hourly['LMP'].rolling(window).mean()

print(f"✓ Added {len(lmp_hourly.columns) - 5} temporal and lag features")

# Save to CSV
output_file = 'ercot_lmp_data.csv'
print(f"\n[5/5] Saving to {output_file}...")

lmp_hourly.to_csv(output_file, index=False)
file_size_mb = pd.io.common.get_filepath_or_buffer(output_file)[0].stat().st_size / 1024 / 1024

print(f"✓ Dataset saved: {output_file} ({file_size_mb:.2f} MB)")
print("\n" + "=" * 60)
print("SUCCESS: ERCOT LMP data ready for model training")
print("=" * 60)
print(f"\nDataset stats:")
print(f"  Rows: {len(lmp_hourly):,}")
print(f"  Columns: {len(lmp_hourly.columns)}")
print(f"  Missing values: {lmp_hourly.isnull().sum().sum()}")
print(f"  Date range: {lmp_hourly['timestamp'].min()} to {lmp_hourly['timestamp'].max()}")
print(f"\nNext step: python fetch_weather.py")
