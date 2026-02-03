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
  
- What was the actual year-over-year growth (or decline) in units sold, revenue, and profit for Nike Running Shoes across Arizona, California, and Washington from 2023 to 2024, and which months or price segments explain most of the change?
  
- Within the observed price range of Nike Running Shoes sales in these three states, where is the optimal price–volume–profit balance located, and are we capturing maximum margin dollars by appropriately emphasizing (or de-emphasizing) certain unit-price tiers?
  
## Data Cleaning and Preparation
- No missing values detected
- No duplicates found
- Converted order_date to datetime format
- Confirmed all records are for 'Nike Running Shoes' only

## Data Extraction and Querying
### State Level Summary

```sql
SELECT 
    state,
    COUNT(*) AS orders,
    SUM(quantity) AS total_units,
    SUM(revenue) AS total_revenue,
    SUM(profit) AS total_profit,
    SUM(revenue) / COUNT(*) AS aov
FROM footwear_filtered
GROUP BY state
ORDER BY total_revenue DESC;
```
### Year-over-year

```sql
SELECT 
    EXTRACT(YEAR FROM order_date) AS year,
    COUNT(*) AS orders,
    SUM(quantity) AS total_units,
    ROUND(SUM(revenue)) AS total_revenue,
    ROUND(SUM(profit)) AS total_profit,
    ROUND(SUM(revenue) / COUNT(*)) AS aov
FROM footwear_filtered
GROUP BY year
ORDER BY year;
```
