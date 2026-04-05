-- ============================================================
-- Query 07: High-Risk Customer Segment
-- Business Question: Who are the top customers most likely
--                   to churn right now? (Retention hit list)
-- ============================================================

SELECT
    Contract                    AS contract_type,
    tenure_group,
    PaymentMethod               AS payment_method,
    InternetService             AS internet_service,
    TechSupport                 AS tech_support,
    COUNT(*)                    AS segment_size,
    SUM(Churn)                  AS already_churned,
    ROUND(SUM(Churn) * 100.0 / COUNT(*), 2)  AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2)             AS avg_monthly_charge,
    -- Estimated monthly revenue at risk from this segment
    ROUND(
        SUM(CASE WHEN Churn = 0 THEN MonthlyCharges ELSE 0 END)
        * SUM(Churn) * 1.0 / NULLIF(COUNT(*) - SUM(Churn), 0),
    2) AS est_revenue_at_risk
FROM customers
GROUP BY Contract, tenure_group, PaymentMethod, InternetService, TechSupport
HAVING churn_rate_pct > 40
   AND segment_size   > 20
ORDER BY churn_rate_pct DESC, est_revenue_at_risk DESC
LIMIT 10;

-- Expected insight:
-- Top 10 highest-risk customer segments
-- Each row = a specific combo the retention team should target
