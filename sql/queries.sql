-- ============================================================
-- Dublin Port Freight & Logistics Cost Optimization — Analysis Queries
-- Table: shipments (loaded from freight_shipments_clean.csv)
-- ============================================================

-- 1. Cost per kg by route and carrier (core cost-efficiency view)
SELECT
    Route,
    Carrier,
    COUNT(*) AS Shipments,
    ROUND(AVG(CostPerKg), 3) AS AvgCostPerKg,
    ROUND(SUM(Cost), 0) AS TotalCost,
    ROUND(SUM(WeightKg), 0) AS TotalWeightKg
FROM shipments
GROUP BY Route, Carrier
ORDER BY Route, AvgCostPerKg;

-- 2. Carrier reliability (on-time %) vs. average cost — the efficiency frontier
SELECT
    Carrier,
    COUNT(*) AS Shipments,
    ROUND(AVG(OnTimeFlag) * 100, 1) AS OnTimePct,
    ROUND(AVG(CostPerKg), 3) AS AvgCostPerKg,
    ROUND(AVG(TransitDays), 1) AS AvgTransitDays
FROM shipments
GROUP BY Carrier
ORDER BY AvgCostPerKg DESC;

-- 3. Route x Carrier efficiency frontier (cost vs. reliability at the route level —
--    this is the query that surfaces the headline recommendation)
SELECT
    Route,
    Carrier,
    COUNT(*) AS Shipments,
    ROUND(AVG(CostPerKg), 3) AS AvgCostPerKg,
    ROUND(AVG(OnTimeFlag) * 100, 1) AS OnTimePct
FROM shipments
GROUP BY Route, Carrier
ORDER BY Route, OnTimePct DESC;

-- 4. Monthly cost trend by route (for the Executive Overview)
SELECT
    Route,
    Month,
    ROUND(SUM(Cost), 0) AS MonthlyCost,
    COUNT(*) AS Shipments
FROM shipments
GROUP BY Route, Month
ORDER BY Route, Month;

-- 5. Headline comparison: EU Direct (Dublin-Cherbourg) — Celtic Sealink vs Atlantic Cargo Ferries
SELECT
    Carrier,
    COUNT(*) AS Shipments,
    ROUND(AVG(CostPerKg), 3) AS AvgCostPerKg,
    ROUND(AVG(OnTimeFlag) * 100, 1) AS OnTimePct,
    ROUND(SUM(Cost), 0) AS TotalCost
FROM shipments
WHERE Route = 'EU Direct (Dublin-Cherbourg)'
GROUP BY Carrier;

-- 6. Projected annual saving if reallocating Atlantic Cargo Ferries volume on
--    Dublin-Cherbourg to Celtic Sealink's average cost/kg
WITH route_data AS (
    SELECT Route, Carrier, SUM(WeightKg) AS TotalWeightKg, SUM(Cost) AS TotalCost
    FROM shipments
    WHERE Route = 'EU Direct (Dublin-Cherbourg)'
    GROUP BY Route, Carrier
),
target_rate AS (
    SELECT TotalCost * 1.0 / TotalWeightKg AS RatePerKg
    FROM route_data WHERE Carrier = 'Celtic Sealink'
)
SELECT
    rd.Carrier,
    rd.TotalWeightKg,
    rd.TotalCost AS ActualCost,
    ROUND(rd.TotalWeightKg * (SELECT RatePerKg FROM target_rate), 0) AS ProjectedCostAtCelticRate,
    ROUND(rd.TotalCost - (rd.TotalWeightKg * (SELECT RatePerKg FROM target_rate)), 0) AS ProjectedSaving
FROM route_data rd
WHERE rd.Carrier = 'Atlantic Cargo Ferries';
