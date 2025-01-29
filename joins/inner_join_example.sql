-- This query demonstrates an INNER JOIN, which combines records from two tables where there is a match.
SELECT users.first_name, users.last_name, orders.order_id
FROM users
INNER JOIN orders
ON users.user_id = orders.user_id;

-- Explanation:
-- `INNER JOIN` only returns rows where there is a matching value in both tables.
-- `ON` specifies the condition for matching records.
