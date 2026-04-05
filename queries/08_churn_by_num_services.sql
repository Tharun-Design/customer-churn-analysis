-- ============================================================
-- Query 08: Churn by Number of Services
-- Business Question: Do customers with more services stay longer?
-- ============================================================

SELECT
    num_services,
    COUNT(*)                                        AS total_customers,
    SUM(Churn)                                      AS churned,
    ROUND(SUM(Churn) * 100.0 / COUNT(*), 2)        AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2)                   AS avg_monthly_charge,
    ROUND(AVG(tenure), 1)                           AS avg_tenure_months
FROM customers
GROUP BY num_services
ORDER BY num_services ASC;

-- Expected insight:
-- Customers with 1-2 services churn significantly more
-- than those with 4+ services
-- → More product adoption = higher stickiness
--
-- Recommendation: Cross-sell additional services during
-- onboarding to increase product stickiness
