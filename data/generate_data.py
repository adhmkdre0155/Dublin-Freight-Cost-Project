"""
Generates a simulated freight shipments dataset for Irish import logistics,
structured around the real post-Brexit route landscape (UK landbridge vs.
direct EU-Ireland ferry routes via Dublin Port and Rosslare Europort).

Intentionally messy (inconsistent carrier name casing/spacing, ~2% missing
Transit Days, a handful of zero/negative weight data-entry errors, and
~1% duplicate Shipment IDs) so the Excel/SQL cleaning step is genuine.
"""
import random
import csv
from datetime import date, timedelta

random.seed(11)

# Real post-Brexit Irish freight route structure (CSO Ireland trade statistics context):
# UK Landbridge = Dublin<->Holyhead/Liverpool (shortest transit, most volume, pre-Brexit default)
# EU Direct routes emerged/grew post-Brexit to avoid UK customs friction
ROUTES = {
    "UK Landbridge (Dublin-Holyhead)": {
        "carriers": ["Celtic Sealink", "Nordic Freight Lines"],
        "base_transit": 1, "transit_var": 1, "base_cost_per_kg": 0.42, "volume_share": 0.48,
    },
    "EU Direct (Dublin-Cherbourg)": {
        "carriers": ["Celtic Sealink", "Atlantic Cargo Ferries"],
        "base_transit": 2, "transit_var": 1, "base_cost_per_kg": 0.58, "volume_share": 0.29,
    },
    "EU Direct (Rosslare-Dunkirk)": {
        "carriers": ["Atlantic Cargo Ferries", "Nordic Freight Lines"],
        "base_transit": 2, "transit_var": 1, "base_cost_per_kg": 0.55, "volume_share": 0.23,
    },
}

# Carrier reliability/cost personality (deliberately includes a "costly but not more
# reliable" carrier on one route, to create a genuine, discoverable BA finding)
CARRIER_PROFILE = {
    "Celtic Sealink":          {"cost_mult": 1.00, "ontime_rate": 0.93},
    "Nordic Freight Lines":    {"cost_mult": 0.91, "ontime_rate": 0.90},
    "Atlantic Cargo Ferries":  {"cost_mult": 1.14, "ontime_rate": 0.89},  # pricier, NOT more reliable
}

CASING_VARIANTS = lambda name: random.choice([name, name.upper(), name.lower(), " " + name + " "])

PERIOD_START = date(2024, 1, 1)
PERIOD_END = date(2025, 12, 31)

rows = []
shipment_id = 700000

for route, rcfg in ROUTES.items():
    n_shipments = int(6000 * rcfg["volume_share"])
    for _ in range(n_shipments):
        shipment_id += 1
        carrier = random.choice(rcfg["carriers"])
        cprof = CARRIER_PROFILE[carrier]

        d = PERIOD_START + timedelta(days=random.randint(0, (PERIOD_END - PERIOD_START).days))

        weight = round(max(50, random.gauss(1800, 900)), 0)  # kg
        cost_per_kg = rcfg["base_cost_per_kg"] * cprof["cost_mult"] * random.uniform(0.92, 1.08)
        cost = round(weight * cost_per_kg, 2)

        transit = max(1, round(random.gauss(rcfg["base_transit"], rcfg["transit_var"] * 0.4)))
        on_time = "Y" if random.random() < cprof["ontime_rate"] else "N"

        carrier_raw = CASING_VARIANTS(carrier) if random.random() < 0.15 else carrier

        # Data quality issues
        transit_val = "" if random.random() < 0.02 else transit
        weight_val = weight
        if random.random() < 0.005:
            weight_val = -abs(weight)  # data-entry error

        rows.append([shipment_id, d.strftime("%Y-%m-%d"), route, carrier_raw,
                     weight_val, cost, transit_val, on_time])

# Inject ~1% duplicate Shipment IDs (system export error)
dupes = random.sample(rows, int(len(rows) * 0.01))
rows.extend(dupes)
random.shuffle(rows)

header = ["ShipmentID", "ShipDate", "Route", "Carrier", "WeightKg", "Cost", "TransitDays", "OnTime"]
with open("freight_shipments_raw.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(header)
    w.writerows(rows)

print(f"Generated {len(rows)} raw shipment rows across {len(ROUTES)} routes.")
