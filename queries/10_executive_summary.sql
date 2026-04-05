-- ============================================================
-- Query 10: Executive Summary - KPI Dashboard
-- Business Question: Give me the full picture in one query
--                   for a business stakeholder report
-- ============================================================

SELECT 'OVERALL' AS metric, '' AS value
UNION ALL
SELECT 'Total Customers',
    CAST(COUNT(*) AS TEXT) FROM customers
UNION ALL
SELECT 'Total Churned',
    CAST(SUM(Churn) AS TEXT) FROM customers
UNION ALL
SELECT 'Overall Churn Rate',
    ROUND(SUM(Churn)*100.0/COUNT(*),2) || '%' FROM customers
UNION ALL
SELECT 'Monthly Revenue at Risk ($)',
    CAST(ROUND(SUM(CASE WHEN Churn=1 THEN MonthlyCharges ELSE 0 END),0) AS TEXT) FROM customers

UNION ALL SELECT 'HIGHEST RISK SEGMENTS', ''
UNION ALL
SELECT 'Worst Contract Type',
    Contract || ' - ' || ROUND(SUM(Churn)*100.0/COUNT(*),1) || '% churn'
    FROM customers GROUP BY Contract
    HAVING SUM(Churn)*1.0/COUNT(*) = (
        SELECT MAX(r) FROM (
            SELECT SUM(Churn)*1.0/COUNT(*) AS r FROM customers GROUP BY Contract
        )
    )
UNION ALL
SELECT 'Worst Tenure Group',
    tenure_group || ' - ' || ROUND(SUM(Churn)*100.0/COUNT(*),1) || '% churn'
    FROM customers GROUP BY tenure_group
    HAVING SUM(Churn)*1.0/COUNT(*) = (
        SELECT MAX(r) FROM (
            SELECT SUM(Churn)*1.0/COUNT(*) AS r FROM customers GROUP BY tenure_group
        )
    )
UNION ALL
SELECT 'Worst Payment Method',
    PaymentMethod || ' - ' || ROUND(SUM(Churn)*100.0/COUNT(*),1) || '% churn'
    FROM customers GROUP BY PaymentMethod
    HAVING SUM(Churn)*1.0/COUNT(*) = (
        SELECT MAX(r) FROM (
            SELECT SUM(Churn)*1.0/COUNT(*) AS r FROM customers GROUP BY PaymentMethod
        )
    )

UNION ALL SELECT 'REVENUE', ''
UNION ALL
SELECT 'Avg Charge - Churned ($)',
    CAST(ROUND(AVG(CASE WHEN Churn=1 THEN MonthlyCharges END),2) AS TEXT) FROM customers
UNION ALL
SELECT 'Avg Charge - Retained ($)',
    CAST(ROUND(AVG(CASE WHEN Churn=0 THEN MonthlyCharges END),2) AS TEXT) FROM customers
UNION ALL
SELECT 'Total Monthly Revenue ($)',
    CAST(ROUND(SUM(MonthlyCharges),0) AS TEXT) FROM customers;