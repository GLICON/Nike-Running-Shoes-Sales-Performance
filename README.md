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
- Which of the three Western states (Arizona, California, Washington) and their top-performing cities contribute the most to Nike Running Shoes revenue and profit, and how should we prioritize regional inventory allocation and localized marketing spend for 2025–2026?
  
- What was the actual year-over-year growth (or decline) in units sold and profit for Nike Running Shoes across Arizona, California, and Washington from 2023 to 2024, and which months or price segments explain most of the change?
  
- Within the observed price range of Nike Running Shoes sales in these three states, where is the optimal price–volume–profit balance located, and are we capturing maximum margin dollars by appropriately emphasizing (or de-emphasizing) certain unit-price tiers?
  
## Data Cleaning and Preparation
- No missing values detected
- No duplicates found
- Converted order_date to datetime format
- Confirmed all records are for 'Nike Running Shoes' only

## Data Extraction and Querying


Exploratory Data Analysis

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


| State       | Year | Units | Profit      | YoY Units Δ | YoY Profit Δ |
|-------------|------|-------|-------------|-------------|--------------|
| Arizona     | 2023 | 328   | $24,851.70  | —           | —            |
| Arizona     | 2024 | 289   | $22,696.83  | ↓ 11.9%     | ↓ 8.7%       |
| California  | 2023 | 309   | $24,874.98  | —           | —            |
| California  | 2024 | 272   | $21,572.17  | ↓ 12.0%     | ↓ 13.3%      |
| Washington  | 2023 | 107   | $7,734.46   | —           | —            |
| Washington  | 2024 | 141   | $11,693.09  | ↑ 31.8%     | ↑ 51.2%      |


<img width="494" height="400" alt="Screenshot 2026-02-04 at 22 42 05" src="https://github.com/user-attachments/assets/0ba89dc0-ebf9-4754-bd50-61434b589978" />

<img width="493" height="398" alt="Screenshot 2026-02-04 at 22 37 56" src="https://github.com/user-attachments/assets/0038ed58-1eb1-47e7-ba16-71c1df4bef9d" />


It can be seen that Washington has the largest increase in units sold and profit made with 31.8% and 51.28% increase respectively.

Results and Findings
