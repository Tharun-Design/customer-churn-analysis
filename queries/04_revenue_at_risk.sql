-- ============================================================
-- Query 04: Revenue at Risk
-- Business Question: How much monthly revenue is the business
--                   losing to churn?
-- ============================================================

SELECT
    -- Revenue from churned customers (lost revenue)
    ROUND(SUM(CASE WHEN Churn = 1 THEN MonthlyCharges ELSE 0 END), 2)
        AS monthly_revenue_lost,

    -- Revenue from retained customers (safe revenue)
    ROUND(SUM(CASE WHEN Churn = 0 THEN MonthlyCharges ELSE 0 END), 2)
        AS monthly_revenue_retained,

    -- Total revenue
    ROUND(SUM(MonthlyCharges), 2)
        AS total_monthly_revenue,

    -- % of revenue at risk
    ROUND(
        SUM(CASE WHEN Churn = 1 THEN MonthlyCharges ELSE 0 END) * 100.0
        / SUM(MonthlyCharges), 2
    )   AS pct_revenue_at_risk,

    -- Average charge comparison
    ROUND(AVG(CASE WHEN Churn = 1 THEN MonthlyCharges END), 2)
        AS avg_charge_churned,
    ROUND(AVG(CASE WHEN Churn = 0 THEN MonthlyCharges END), 2)
        AS avg_charge_retained

FROM customers;

-- Expected insight:
-- ~$139k/month is at risk from churning customers
-- Churned customers pay MORE on average ($74 vs $61)
-- → High-value customers are leaving!
