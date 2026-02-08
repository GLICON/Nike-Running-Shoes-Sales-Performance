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
