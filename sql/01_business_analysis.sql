
USE retailpulse;

-- =========================================
-- 1. TOTAL REVENUE
-- =========================================

SELECT
    ROUND(SUM(revenue), 2) AS total_revenue
FROM fact_sales;


-- =========================================
-- 2. TOTAL ORDERS
-- =========================================

SELECT
    COUNT(DISTINCT invoice_no) AS total_orders
FROM fact_sales;


-- =========================================
-- 3. TOTAL CUSTOMERS
-- =========================================

SELECT
    COUNT(DISTINCT customer_id) AS total_customers
FROM fact_sales;


-- =========================================
-- 4. TOTAL PRODUCTS
-- =========================================

SELECT
    COUNT(DISTINCT stock_code) AS total_products
FROM fact_sales;


-- =========================================
-- 5. COUNTRY-WISE REVENUE
-- =========================================

SELECT
    country,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM fact_sales
GROUP BY country
ORDER BY total_revenue DESC
LIMIT 10;


-- =========================================
-- 6. TOP 10 PRODUCTS
-- =========================================

SELECT
    stock_code,
    MAX(description) AS product_name,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM fact_sales
GROUP BY stock_code
ORDER BY total_revenue DESC
LIMIT 10;


-- =========================================
-- 7. MONTHLY REVENUE
-- =========================================

SELECT
    DATE_FORMAT(invoice_date, '%Y-%m') AS sales_month,
    ROUND(SUM(revenue), 2) AS monthly_revenue
FROM fact_sales
GROUP BY DATE_FORMAT(invoice_date, '%Y-%m')
ORDER BY sales_month;

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