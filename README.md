# Nike-Running-Shoes-Sales-Performance
This analysis explores Nike Running Shoes transactions in Arizona, California, and Washington during 2023–2024, drawn from filtered product sales records, highlighting regional revenue patterns, annual growth trends, seasonal rhythms, and the ideal pricing-profit equilibrium.

## Table of Contents

- [Project Overview](#project-overview)
- [Project Focus](#project-focus)
- [Questions](#questions)
- [Data Cleaning and Preparation](#data-cleaning-and-preparation)
- [Data Extraction and Querying](#data-extraction-and-querying)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Results and Findings](#results-and-findings)
- [Recomendations](#recommendations)
- [Limitations](#limitations)
- [References](#references)
- [Data Sources](#data-sources)
- [Tools](#tools)

## Project Overview
This project examines Nike Running Shoes sales performance across Arizona, California, and Washington from 2023 to 2024 using cleaned, order-level transaction data. The analysis directly addresses three key stakeholder questions: geographic concentration of revenue and profit, year-over-year growth trends, and the optimal price–volume–profit balance. It provides clear, actionable insights to support better decisions in inventory allocation, regional marketing focus, pricing strategy, and seasonal planning in the athletic footwear retail sector.

## Project Focus
- Geographic concentration of revenue and profit across states and key cities
- Year-over-year performance trends and seasonal patterns
- Price elasticity, volume behavior, and profit optimization by unit-price segment

### Questions
- Which of the three Western states (Arizona, California, Washington) and their top-performing cities contribute the most to Nike Running Shoes profit, and how should we prioritize regional inventory allocation and localized marketing spend for 2025–2026?
  
- What was the actual year-over-year growth (or decline) in units sold and profit for Nike Running Shoes across Arizona, California, and Washington from 2023 to 2024, and which months or price segments explain most of the change?
  
- Within the observed price range of Nike Running Shoes sales in these three states, where is the optimal price–volume–profit balance located, and are we capturing maximum margin dollars by appropriately emphasizing (or de-emphasizing) certain unit-price tiers?
  
## Data Cleaning and Preparation
- No missing values detected
- No duplicates found
- Converted order_date to datetime format
- Confirmed all records are for 'Nike Running Shoes' only

## Data Extraction and Querying
### Geographic Performance

```sql
SELECT 
    state,
    COUNT(*) AS orders,
    SUM(quantity) AS total_units,
    SUM(revenue)::numeric AS total_revenue,
    SUM(profit)::numeric AS total_profit
FROM footwear_filtered
GROUP BY state
ORDER BY total_revenue DESC;

-- Top 10 cities
WITH city_agg AS (
    SELECT 
        state,
        TRIM(city) AS city_clean,
        COUNT(*) AS orders,
        SUM(quantity) AS units,
        ROUND(SUM(revenue)::numeric, 2) AS revenue,
        ROUND(SUM(profit)::numeric, 2) AS profit
    FROM footwear_filtered
    GROUP BY state, TRIM(city)
)
SELECT 
    city_clean AS city,
    state,
    orders,
    units,
    revenue,
    profit,
    ROUND(100.0 * revenue / SUM(revenue) OVER (), 1) AS revenue_share_pct
FROM city_agg
ORDER BY revenue DESC
LIMIT 10;
```

### Year-over-Year Change
```sql
WITH yearly AS (
    SELECT 
        state,
        EXTRACT(YEAR FROM order_date) AS sales_year,
        SUM(quantity) AS units,
        ROUND(SUM(profit)::numeric, 2) AS profit
    FROM footwear_filtered
    GROUP BY state, EXTRACT(YEAR FROM order_date)
)
SELECT 
    state,
    sales_year,
    units,
    profit,
    ROUND(100.0 * (units - LAG(units) OVER (PARTITION BY state ORDER BY sales_year)) 
          / NULLIF(LAG(units) OVER (PARTITION BY state ORDER BY sales_year), 0), 1) AS yoy_units_pct,
    ROUND(100.0 * (profit - LAG(profit) OVER (PARTITION BY state ORDER BY sales_year)) 
          / NULLIF(LAG(profit) OVER (PARTITION BY state ORDER BY sales_year), 0), 1) AS yoy_profit_pct
FROM yearly
ORDER BY state, sales_year;
```

## Results and Findings
### Year-over-Year Growth Trends and Seasonal Patterns


| State       | Year | Units | Profit      | YoY Units Δ | YoY Profit Δ |
|-------------|------|-------|-------------|-------------|--------------|
| Arizona     | 2023 | 328   | $24,851.70  | —           | —            |
| Arizona     | 2024 | 289   | $22,696.83  | ↓ 11.9%     | ↓ 8.7%       |
| California  | 2023 | 309   | $24,874.98  | —           | —            |
| California  | 2024 | 272   | $21,572.17  | ↓ 12.0%     | ↓ 13.3%      |
| Washington  | 2023 | 107   | $7,734.46   | —           | —            |
| Washington  | 2024 | 141   | $11,693.09  | ↑ 31.8%     | ↑ 51.2%      |

- Arizona and California experienced similar mid-teens percentage declines in units and profit, potentially driven by softer demand, increased competition (e.g., from brands like Hoka or On in running), or macroeconomic factors affecting consumer spending in those states.

- Washington bucked the trend with robust double-digit gains, particularly in profit (51.2% increase), suggesting stronger local demand, successful marketing, demographic factors (e.g., active outdoor culture in the Pacific Northwest), or less saturation.


<img width="494" height="400" alt="Screenshot 2026-02-04 at 22 42 05" src="https://github.com/user-attachments/assets/0ba89dc0-ebf9-4754-bd50-61434b589978" />

<img width="493" height="398" alt="Screenshot 2026-02-04 at 22 37 56" src="https://github.com/user-attachments/assets/0038ed58-1eb1-47e7-ba16-71c1df4bef9d" />

### Price-Tier Analysis

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ───────────────────────────────────────────────
# Styling (makes charts look more professional)
# ───────────────────────────────────────────────
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("viridis")

# ───────────────────────────────────────────────
# 1. Load and prepare data
# ───────────────────────────────────────────────
df = pd.read_csv('footwear_filtered.csv')

# Price bins
bins = [0, 100, 150, 200, 250, 300, 350, 400, np.inf]
labels = ['< $100', '$100–150', '$150–200', '$200–250', 
          '$250–300', '$300–350', '$350–400', '$400+']

df['price_bin'] = pd.cut(
    df['unit_price'], 
    bins=bins, 
    labels=labels, 
    right=False, 
    include_lowest=True
)

# ───────────────────────────────────────────────
# 2. Aggregate metrics
# ───────────────────────────────────────────────
bin_stats = df.groupby('price_bin', observed=True).agg(
    orders           = ('order_id',    'count'),
    total_units      = ('quantity',    'sum'),
    avg_unit_price   = ('unit_price',  'mean'),
    total_revenue    = ('revenue',     'sum'),
    total_profit     = ('profit',      'sum')
).round(2)

bin_stats['profit_per_unit']   = (bin_stats['total_profit'] / bin_stats['total_units']).round(2)
bin_stats['margin_pct']        = (bin_stats['total_profit'] / bin_stats['total_revenue'] * 100).round(2)
bin_stats['profit_share_pct']  = (bin_stats['total_profit'] / bin_stats['total_profit'].sum() * 100).round(1)
bin_stats['revenue_share_pct'] = (bin_stats['total_revenue'] / bin_stats['total_revenue'].sum() * 100).round(1)

# Sort by total profit (most important business view)
bin_stats = bin_stats.sort_values('total_profit', ascending=False)

print("\nPrice Segment Performance Summary")
print(bin_stats)

# ───────────────────────────────────────────────
# 3. Visualizations
# ───────────────────────────────────────────────

# Figure setup - two subplots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), gridspec_kw={'width_ratios': [5, 4]})

# ─── Left: Bar + Line - Total Profit & Profit per Unit ───
color_profit = '#2ecc71'
color_ppu    = '#e74c3c'

bars = ax1.bar(
    bin_stats.index, 
    bin_stats['total_profit'], 
    color=color_profit, 
    alpha=0.85, 
    label='Total Profit ($)'
)

ax1.set_title('Total Profit by Price Segment', fontsize=14, fontweight='bold', pad=15)
ax1.set_ylabel('Total Profit ($)', color=color_profit, fontsize=12)
ax1.tick_params(axis='y', labelcolor=color_profit)

ax1_ppu = ax1.twinx()
ax1_ppu.plot(
    bin_stats.index, 
    bin_stats['profit_per_unit'], 
    color=color_ppu, 
    marker='o', 
    linewidth=2.5, 
    markersize=8, 
    label='Profit per Unit ($)'
)
ax1_ppu.set_ylabel('Profit per Unit ($)', color=color_ppu, fontsize=12)
ax1_ppu.tick_params(axis='y', labelcolor=color_ppu)

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_ppu.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

ax1.tick_params(axis='x', rotation=45, labelsize=10)
ax1.grid(True, axis='y', linestyle='--', alpha=0.7)

# ─── Right: Stacked bar - Revenue & Profit Share ───
bin_stats_sorted_rev = bin_stats.sort_values('total_revenue', ascending=True)  # for nicer stacking order

x = np.arange(len(bin_stats_sorted_rev))
width = 0.35

ax2.bar(x - width/2, bin_stats_sorted_rev['revenue_share_pct'], width, 
        label='Revenue Share %', color='#3498db', alpha=0.9)
ax2.bar(x + width/2, bin_stats_sorted_rev['profit_share_pct'], width, 
        label='Profit Share %', color='#9b59b6', alpha=0.9)

ax2.set_title('Revenue vs Profit Share by Price Segment', fontsize=14, fontweight='bold', pad=15)
ax2.set_xticks(x)
ax2.set_xticklabels(bin_stats_sorted_rev.index, rotation=45, ha='right', fontsize=10)
ax2.set_ylabel('Percentage of Total (%)', fontsize=12)
ax2.legend(loc='upper left', fontsize=10)
ax2.grid(True, axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# ─── Optional: Extra chart - Margin stability ───
plt.figure(figsize=(10, 5))

sns.lineplot(
    x=bin_stats.index,
    y=bin_stats['margin_pct'],
    marker='o',
    linewidth=2.5,
    markersize=10,
    color='#27ae60'
)

plt.title('Gross Margin % Across Price Segments', fontsize=14, fontweight='bold', pad=15)
plt.ylabel('Gross Margin (%)', fontsize=12)
plt.xlabel('Price Segment', fontsize=12)
plt.ylim(bin_stats['margin_pct'].min() - 1, bin_stats['margin_pct'].max() + 1)
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
```
### Price-Tier Analysis

**Top profit contributors** — The $350–400 and $400+ segments together generate ~40.6% of all profit dollars — despite only ~24% of orders. These premium tiers drive the majority of margin dollars.

**Profit per unit rises steadily with price** — peaking at $141.04 in the $400+ band. No sharp drop-off is visible, indicating customers in these states accept (and purchase) higher-priced running shoes without strong negative elasticity in this sample.

**Gross margins are remarkably stable** — ranging 31.4%–33.6% across all bins, with only a minor dip in the $300–350 range. This suggests consistent cost structures and limited promotional pressure distorting margins.

Lowest tier (< $100) has the most orders (120) and units (236) but contributes just 4% of profit — the lowest profit/unit ($19). Deep discounting here erodes value without proportional volume upside.

**Sweet spot** — $250–400 range offers the best balance:
~50.7% of total profit
Solid volume (good number of units)
High profit/unit ($89–$125)
Healthy, stable margins (~32–33%)


<img width="1600" height="700" alt="price-tier" src="https://github.com/user-attachments/assets/60e9a818-5cee-4d79-93ab-b63cd51f9cf0" />

<img width="1000" height="500" alt="Gross-margin_percentage" src="https://github.com/user-attachments/assets/4a34c23e-eb0a-482d-9836-4c9c89c36867" />

## Recommendations for Maximum Profit in 2025 - 2026

- **Accelerate investment in Washington State**: Washington delivered the strongest performance momentum in 2024 (+31% units, +51% profit YoY). We recommend meaningfully increasing inventory allocation and localized marketing support — targeting 20–25% of total Western-region resources (up from ~17% current profit contribution), with particular focus on Seattle and Spokane.

- **Maintain Arizona as the anchor market**: Arizona remains our largest absolute profit contributor. We should protect core city performance (Phoenix, Glendale, Chandler, Tucson, Mesa) and hold ~40–42% of regional inventory & marketing allocation.

- **Stabilize California**: prevent further share erosion. California showed similar softness to Arizona in 2024. We recommend defending key markets (San Diego, Sacramento, Los Angeles, San Jose) at ~38–40% allocation while closely monitoring competitive dynamics.


- **Position Washington as the primary growth engine**: Double-down on regional activation tactics (community running events, university/outdoor partnerships, targeted local influencers) to protect and extend 2024 momentum.

- **Maintain Arizona as the anchor market**:Arizona remains our largest absolute profit contributor. We should protect core city performance (Phoenix, Glendale, Chandler, Tucson, Mesa) and hold ~40–42% of regional inventory & marketing allocation.

- **Stabilize California**: prevent further share erosion
California showed similar softness to Arizona in 2024. We recommend defending key markets (San Diego, Sacramento, Los Angeles, San Jose) at ~38–40% allocation while closely monitoring competitive dynamics.

- **Emphasize mid-premium positioning** — Prioritize marketing spend, in-store visibility, online featured placements, and inventory allocation toward $250–400 items (especially $350–400 zone) to capture maximum profit dollars.

- **Regional nuance** — In declining markets (Arizona/California), test whether shifting emphasis toward $250–350 helps stabilize volume without sacrificing too much margin. In high-growth Washington, lean harder into $350+ tiers where demand appears strongest.

- **Minimize reliance on deep discounts** — Avoid aggressive promotions below $150 except for targeted use cases (customer acquisition, seasonal clearance, entry-level bundles). Margin compression here is not offset by enough incremental volume.

## Tools
- Excel (Data Cleaning)
- SQL (Data Extraction and Querying)
- Python (
