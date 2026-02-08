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
