-- ============================================================
-- Query 06: Churn by Internet Service + Tech Support
-- Business Question: Which service combination is highest risk?
-- ============================================================

SELECT
    InternetService                                     AS internet_service,
    TechSupport                                         AS tech_support,
    COUNT(*)                                            AS total_customers,
    SUM(Churn)                                          AS churned,
    ROUND(SUM(Churn) * 100.0 / COUNT(*), 2)            AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2)                       AS avg_monthly_charge
FROM customers
GROUP BY InternetService, TechSupport
ORDER BY churn_rate_pct DESC;

-- Expected insight:
-- Fiber optic + No tech support = ~41% churn (highest!)
-- Fiber optic + Tech support    = ~18% churn
-- DSL + No tech support         = ~25% churn
-- No internet                   = ~7%  churn (lowest)
--
-- Recommendation: Proactively upsell TechSupport to
-- Fiber Optic customers — it cuts churn by more than half
