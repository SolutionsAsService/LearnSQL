-- This query demonstrates how to calculate the sum of a column.
SELECT SUM(order_amount) AS total_sales
FROM orders;

-- Explanation:
-- `SUM()` adds up all values in the specified column (`order_amount`).
