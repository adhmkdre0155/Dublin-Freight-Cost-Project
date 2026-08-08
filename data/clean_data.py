"""
Cleaning step for the Dublin Port Freight & Logistics Cost Optimization project.
  1. Standardize carrier names (trim whitespace, fix casing)
  2. Remove exact duplicate ShipmentIDs (keep first occurrence)
  3. Remove/flag invalid weights (negative or zero)
  4. Fill missing TransitDays using the route+carrier median (documented assumption)
  5. Add CostPerKg derived column used throughout the analysis
"""
import pandas as pd

df = pd.read_csv("freight_shipments_raw.csv")
raw_rows = len(df)

# 1) Standardize carrier names
df["Carrier"] = df["Carrier"].str.strip().str.title()
df.loc[df["Carrier"] == "Nordic Freight Lines", "Carrier"] = "Nordic Freight Lines"  # normalize casing edge cases
df["Carrier"] = df["Carrier"].replace({
    "Celtic Sealink": "Celtic Sealink",
    "Atlantic Cargo Ferries": "Atlantic Cargo Ferries",
})

# 2) Remove duplicate ShipmentIDs
df = df.drop_duplicates(subset="ShipmentID", keep="first")
after_dedupe = len(df)

# 3) Remove invalid weights
df = df[df["WeightKg"] > 0]
after_weight = len(df)

# 4) Fill missing TransitDays using route+carrier median
df["TransitDays"] = pd.to_numeric(df["TransitDays"], errors="coerce")
medians = df.groupby(["Route", "Carrier"])["TransitDays"].transform("median")
df["TransitDays"] = df["TransitDays"].fillna(medians).round(0).astype(int)

# 5) Derived columns
df["CostPerKg"] = (df["Cost"] / df["WeightKg"]).round(3)
df["ShipDate"] = pd.to_datetime(df["ShipDate"])
df["Month"] = df["ShipDate"].dt.to_period("M").astype(str)
df["OnTimeFlag"] = (df["OnTime"] == "Y").astype(int)

df = df.sort_values("ShipDate").reset_index(drop=True)
df.to_csv("freight_shipments_clean.csv", index=False)

print(f"Raw rows:              {raw_rows}")
print(f"After dedupe:          {after_dedupe}  ({raw_rows - after_dedupe} duplicates removed)")
print(f"After invalid weights: {after_weight}  ({after_dedupe - after_weight} removed)")
print(f"Final rows:            {len(df)}")
print(f"Carriers: {sorted(df['Carrier'].unique())}")
print(f"Routes: {sorted(df['Route'].unique())}")
