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