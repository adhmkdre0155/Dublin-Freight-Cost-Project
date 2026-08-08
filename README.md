# Dublin Port Freight & Logistics Cost Optimization

**Business Analyst portfolio project — Adham AlHers**
[Live interactive dashboard](./dashboard/index.html) · [LinkedIn](https://www.linkedin.com/in/adhamalhers/) · [Portfolio home](#)

## Problem statement
A logistics/import business wants to reduce per-shipment freight cost across routes and carriers **without hurting delivery SLAs** — the classic BA challenge of translating a vague business ask ("reduce costs") into a measurable, data-backed recommendation.

## Business context
Ireland's post-Brexit supply chains rely heavily on Dublin Port and Rosslare Europort, with a mix of the traditional UK landbridge route and newer direct EU routes that grew to avoid UK customs friction. Freight cost efficiency is a live, current topic for Irish importers.

## Dataset
A simulated shipments dataset (5,970 cleaned shipments, 2024–2025) structured around the real Irish freight route landscape: **UK Landbridge (Dublin-Holyhead)**, **EU Direct (Dublin-Cherbourg)**, and **EU Direct (Rosslare-Dunkirk)**, across 3 carriers. Generated with realistic data-quality issues (inconsistent carrier name casing, missing transit days, duplicate shipment IDs, a handful of data-entry weight errors) so the cleaning step is genuine. See `data/generate_data.py` for full generation logic.

## Tools
Excel (openpyxl, formula-driven) · SQL (SQLite) · Chart.js for the interactive dashboard · Graphviz for the process flow diagram.

## Repository structure
```
├── data/
│   ├── generate_data.py              # Generates the raw simulated dataset
│   ├── clean_data.py                 # Cleaning: carrier names, duplicates, invalid weights, missing transit days
│   ├── freight_shipments_raw.csv
│   └── freight_shipments_clean.csv
├── sql/
│   └── queries.sql                   # Cost/kg by route+carrier, efficiency frontier, savings scenario
├── excel/
│   └── Dublin_Freight_Cost_Dashboard.xlsx   # Formula-driven pivot dashboard with KPI cards and scatter chart
├── dashboard/
│   └── index.html                    # Self-contained interactive web dashboard
└── docs/
    ├── BRD_Dublin_Freight.docx/.pdf         # Business Requirements Document
    ├── findings_recommendation.docx/.pdf    # Consulting-style findings & recommendation memo
    └── process_flow.png                     # Current-state process map with bottleneck highlighted
```

## Step-by-step approach (this is a BA project — process matters as much as the numbers)
1. **Gather requirements first** — before touching data, `docs/BRD_Dublin_Freight.docx` defines what "cost efficiency" means to stakeholders: cost/kg minimized *subject to no reduction in on-time delivery %*, not cost/kg alone. This single framing decision shaped everything downstream.
2. **Clean and model in Excel** — `excel/Dublin_Freight_Cost_Dashboard.xlsx` uses SUMIFS/AVERAGEIFS/COUNTIFS formulas (not hardcoded) across a Data → Route_Carrier_Summary → Savings_Scenario → Dashboard structure.
3. **Analyze in SQL** — `sql/queries.sql` calculates cost/kg and on-time % by carrier, builds the route x carrier efficiency frontier, and models the projected saving from a specific reallocation scenario.
4. **Map the current process** — `docs/process_flow.png` (Graphviz) shows the current manual booking workflow with the root-cause bottleneck (carrier chosen by habit, not data) called out explicitly.
5. **Present findings as a recommendation, not just a chart** — `docs/findings_recommendation.docx` is written as a client-ready memo: headline finding, comparison table, recommendation, and what was deliberately *not* recommended on the other two routes (and why).

## Key insight
On the **Dublin-Cherbourg** route, **Atlantic Cargo Ferries** (€0.662/kg, 87.9% on-time) is both **more expensive and less reliable** than **Celtic Sealink** (€0.580/kg, 93.1% on-time) — this isn't a cost-vs-reliability trade-off, it's a clear-cut reallocation opportunity.

## Recommendation
Reallocate Atlantic Cargo Ferries' Dublin-Cherbourg volume to Celtic Sealink: projected saving of **€130,645** over the 2-year analysis period (≈€65,300/year, a 12.4% reduction on that route/carrier spend) **with on-time performance improving from 87.9% to 93.1%** — satisfying the stakeholder-agreed requirement that cost reduction cannot come at the expense of SLA performance.

The other two routes were deliberately **not** flagged for action — Nordic Freight Lines is already the efficient choice on UK Landbridge, and Rosslare-Dunkirk shows no clear-cut case yet. Knowing when *not* to recommend a change is as much a BA skill as finding one.

## Business impact
Demonstrates the core BA skill: turning a vague ask ("reduce freight costs") into a scoped requirement, a data-backed recommendation, and a documented rationale a Logistics Manager or Finance stakeholder could act on directly.

## CV / LinkedIn bullet
> Led a logistics cost-optimization analysis across 3 freight routes and 3 carriers; recommended a carrier reallocation projected to cut route-level freight cost by 12.4% (€130K+ over 2 years) while improving on-time delivery from 87.9% to 93.1%.

---
*Dataset is simulated for portfolio purposes, structured on real Irish post-Brexit freight route patterns. All cleaning, SQL, and Excel formula logic is fully reproducible.*
