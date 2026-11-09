
USE retailpulse;

-- ==========================================
-- 1. MONTHLY REVENUE GROWTH
-- ==========================================

WITH monthly_sales AS (
    SELECT
        DATE_FORMAT(invoice_date, '%Y-%m') AS sales_month,
        SUM(revenue) AS monthly_revenue
    FROM fact_sales
    GROUP BY DATE_FORMAT(invoice_date, '%Y-%m')
),
sales_with_previous AS (
    SELECT
        sales_month,
        monthly_revenue,
        LAG(monthly_revenue) OVER (
            ORDER BY sales_month
        ) AS previous_month_revenue
    FROM monthly_sales
)
SELECT
    sales_month,
    ROUND(monthly_revenue, 2) AS monthly_revenue,
    ROUND(previous_month_revenue, 2) AS previous_month_revenue,
    ROUND(
        (monthly_revenue - previous_month_revenue)
        / NULLIF(previous_month_revenue, 0) * 100,
        2
    ) AS growth_percentage
FROM sales_with_previous
ORDER BY sales_month;


-- ==========================================
-- 2. TOP 10 CUSTOMERS BY REVENUE
-- ==========================================

SELECT
    customer_id,
    COUNT(DISTINCT invoice_no) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM fact_sales
WHERE customer_id IS NOT NULL
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 10;


-- ==========================================
-- 3. REVENUE CONTRIBUTION BY COUNTRY
-- ==========================================

SELECT
    country,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(
        SUM(revenue) * 100
        / (SELECT SUM(revenue) FROM fact_sales),
        2
    ) AS revenue_percentage
FROM fact_sales
GROUP BY country
ORDER BY total_revenue DESC;


-- ==========================================
-- 4. RETURN ANALYSIS
-- ==========================================

SELECT
    COUNT(*) AS total_return_records,
    COUNT(DISTINCT invoice_no) AS return_invoices,
    SUM(ABS(quantity)) AS returned_units,
    ROUND(SUM(ABS(revenue)), 2) AS return_value
FROM fact_returns;


-- ==========================================
-- 5. CANCELLATION ANALYSIS
-- ==========================================

SELECT
    COUNT(*) AS cancelled_records,
    COUNT(DISTINCT invoice_no) AS cancelled_invoices,
    SUM(ABS(quantity)) AS cancelled_units,
    ROUND(SUM(ABS(revenue)), 2) AS cancelled_value
FROM fact_cancelled;


-- ==========================================
-- 6. REVENUE BY DAY OF WEEK
-- ==========================================

SELECT
    DAYNAME(invoice_date) AS day_name,
    DAYOFWEEK(invoice_date) AS day_number,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM fact_sales
GROUP BY
    DAYNAME(invoice_date),
    DAYOFWEEK(invoice_date)
ORDER BY day_number;


-- ==========================================
-- 7. AVERAGE ORDER VALUE
-- ==========================================

SELECT
    ROUND(
        SUM(revenue) / COUNT(DISTINCT invoice_no),
        2
    ) AS average_order_value
FROM fact_sales;


-- ==========================================
-- 8. PRODUCT PERFORMANCE
-- ==========================================

SELECT
    stock_code,
    MAX(description) AS product_name,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(AVG(unit_price), 2) AS average_unit_price
FROM fact_sales
GROUP BY stock_code
ORDER BY revenue DESC
LIMIT 20;


