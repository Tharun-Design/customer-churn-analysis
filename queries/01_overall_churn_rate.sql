-- ============================================================
-- Query 01: Overall Churn Rate
-- Business Question: What percentage of customers are churning?
-- ============================================================

SELECT
    COUNT(*)                                          AS total_customers,
    SUM(Churn)                                        AS churned_customers,
    COUNT(*) - SUM(Churn)                             AS retained_customers,
    ROUND(SUM(Churn) * 100.0 / COUNT(*), 2)          AS churn_rate_pct,
    ROUND((COUNT(*) - SUM(Churn)) * 100.0 / COUNT(*), 2) AS retention_rate_pct
FROM customers;

-- Expected insight:
-- Overall churn rate is ~26%, meaning 1 in 4 customers leaves
