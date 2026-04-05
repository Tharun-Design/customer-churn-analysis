-- ============================================================
-- Query 09: Churn by Senior Citizen Status + Dependents
-- Business Question: Do demographics affect churn behaviour?
-- ============================================================

SELECT
    CASE WHEN SeniorCitizen = 1 THEN 'Senior' ELSE 'Non-Senior' END
        AS customer_segment,
    CASE WHEN Dependents = 'Yes' THEN 'Has Dependents' ELSE 'No Dependents' END
        AS dependents,
    CASE WHEN Partner = 'Yes' THEN 'Has Partner' ELSE 'No Partner' END
        AS partner_status,
    COUNT(*)                                        AS total_customers,
    SUM(Churn)                                      AS churned,
    ROUND(SUM(Churn) * 100.0 / COUNT(*), 2)        AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2)                   AS avg_monthly_charge
FROM customers
GROUP BY customer_segment, dependents, partner_status
ORDER BY churn_rate_pct DESC;

-- Expected insight:
-- Senior citizens without dependents churn the most
-- Customers with partners and dependents are most stable
-- → Loyalty programmes could target solo senior customers
