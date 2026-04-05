-- ============================================================
-- Query 02: Churn Rate by Contract Type
-- Business Question: Which contract type has the highest churn?
-- ============================================================

SELECT
    Contract                                                AS contract_type,
    COUNT(*)                                                AS total_customers,
    SUM(Churn)                                              AS churned,
    ROUND(SUM(Churn) * 100.0 / COUNT(*), 2)                AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2)                           AS avg_monthly_charge
FROM customers
GROUP BY Contract
ORDER BY churn_rate_pct DESC;

-- Expected insight:
-- Month-to-month: ~42% churn  (highest risk)
-- One year:       ~11% churn
-- Two year:        ~3% churn  (most loyal)
--
-- Recommendation: Incentivise month-to-month customers
-- to upgrade to annual plans
