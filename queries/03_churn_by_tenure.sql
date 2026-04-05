-- ============================================================
-- Query 03: Churn Rate by Tenure Group
-- Business Question: At what stage of the customer lifecycle
--                   is churn highest?
-- ============================================================

SELECT
    tenure_group,
    COUNT(*)                                        AS total_customers,
    SUM(Churn)                                      AS churned,
    ROUND(SUM(Churn) * 100.0 / COUNT(*), 2)        AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2)                   AS avg_monthly_charge,
    ROUND(AVG(TotalCharges), 2)                     AS avg_total_revenue
FROM customers
GROUP BY tenure_group
ORDER BY churn_rate_pct DESC;

-- Expected insight:
-- 0-12 months:   ~47% churn  ← critical onboarding window
-- 12-24 months:  ~35% churn
-- 24-48 months:  ~20% churn
-- 48-72 months:  ~8%  churn  ← loyal long-term customers
--
-- Recommendation: Focus retention efforts on first 12 months
