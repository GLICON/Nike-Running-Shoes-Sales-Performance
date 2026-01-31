# Nike-Running-Shoes-Sales-Performance
This project leverages a real-world dataset of coffee sales from a vending machine (covering transactions in 2024) to investigate purchasing patterns, temporal trends, and customer behaviors. The goal is to derive actionable insights for optimizing operations, such as restocking, pricing, and promotions.

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

### Project Overview
This project analyzes sales performance of Nike Running Shoes in select Western U.S. cities. The goal is to identify high-performing locations, evaluate year-over-year trends, detect seasonal patterns, and provide actionable recommendations for marketing, inventory allocation, and strategic planning.

## Project Focus
- Prioritize cities for marketing and inventory investment.
- Assess growth/decline between 2023 and 2024 in revenue, profit, and average order value (AOV).
- Identify seasonal sales patterns to optimize stock levels and promotional timing.

## Questions
- Which cities generate the highest revenue and profit for Nike Running Shoes, and should we prioritize them?
- How did performance change from 2023 to 2024 (revenue, profit, AOV)?
- Is there a clear seasonal pattern in sales (by month), and which months require higher preparation?

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
