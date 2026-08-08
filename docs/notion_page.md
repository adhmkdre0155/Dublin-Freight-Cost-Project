# 📋 Dublin Port Freight & Logistics Cost Optimization

**Type:** Business Analyst project · **Tools:** Excel, SQL, interactive dashboard, BRD · **Status:** Complete

[🔗 Live interactive dashboard](#) · [🔗 GitHub repository](#) · [📄 BRD (PDF)](#) · [📄 Findings & Recommendation (PDF)](#)

---

### The problem
A logistics/import business wants to reduce per-shipment freight cost across routes and carriers — **without hurting delivery SLAs**. The real challenge: translating a vague ask ("reduce costs") into a measurable, data-backed recommendation.

### Business context
Ireland's post-Brexit supply chains rely heavily on Dublin Port and Rosslare Europort, split between the traditional UK landbridge route and newer direct-to-EU routes. Freight cost efficiency is a live topic for Irish importers right now.

### What I did — requirements first, then data
1. **Wrote a one-page BRD** before touching any data — the key requirements-gathering question was defining what "cost efficiency" actually means: cost/kg minimized, but *not* at the expense of on-time delivery %. That single framing decision shaped the entire analysis.
2. **Cleaned and modeled** 5,970 shipments in a formula-driven Excel workbook (SUMIFS/AVERAGEIFS, not hardcoded values).
3. **Queried in SQL** to build the cost vs. reliability efficiency frontier by carrier and route.
4. **Mapped the current process** with the bottleneck (habit-based carrier selection) explicitly called out.
5. **Wrote the findings as a client-ready memo**, not just a chart — including what I deliberately did *not* recommend, and why.

### 🔑 Key insight
> On the **Dublin-Cherbourg** route, Atlantic Cargo Ferries is both **more expensive** (€0.662/kg) **and less reliable** (87.9% on-time) than Celtic Sealink (€0.580/kg, 93.1% on-time). This isn't a cost-vs-reliability trade-off — it's a clear reallocation opportunity.

### Recommendation
Reallocate Atlantic Cargo Ferries' Dublin-Cherbourg volume to Celtic Sealink: **€130,645 projected saving** over 2 years (12.4% on that route) **while improving on-time delivery from 87.9% to 93.1%**.

### What I didn't recommend (and why that matters)
The other two routes were deliberately left alone — Nordic Freight Lines is already the efficient carrier on UK Landbridge, and Rosslare-Dunkirk showed no clear-cut case. Knowing when *not* to act on a marginal difference is as much a BA skill as finding a strong recommendation.

### Business impact
Turns "reduce freight costs" into a scoped requirement, a specific carrier-level recommendation, and a documented rationale a Logistics Manager or Finance stakeholder could approve directly.

---

**CV / LinkedIn bullet:**
*Led a logistics cost-optimization analysis across 3 freight routes and 3 carriers; recommended a carrier reallocation projected to cut route-level freight cost by 12.4% (€130K+ over 2 years) while improving on-time delivery from 87.9% to 93.1%.*

**Skills demonstrated:** Requirements gathering (BRD) · Stakeholder framing · SQL · Excel (formula-driven dashboards) · Process mapping · Data-backed recommendation writing
