-- ============================================================
-- Query 05: Churn Rate by Payment Method
-- Business Question: Does payment method correlate with churn?
-- ============================================================

SELECT
    PaymentMethod                                       AS payment_method,
    COUNT(*)                                            AS total_customers,
    SUM(Churn)                                          AS churned,
    ROUND(SUM(Churn) * 100.0 / COUNT(*), 2)            AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2)                       AS avg_monthly_charge
FROM customers
GROUP BY PaymentMethod
ORDER BY churn_rate_pct DESC;

-- Expected insight:
-- Electronic check:     ~45% churn  ← highest risk
-- Mailed check:         ~19% churn
-- Bank transfer (auto): ~17% churn
-- Credit card (auto):   ~15% churn  ← lowest risk
--
-- Recommendation: Offer a 5% discount to switch from
-- electronic check to auto-pay methods
