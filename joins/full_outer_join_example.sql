-- This query demonstrates a FULL OUTER JOIN, which returns all records when there is a match in either the left or the right table.
SELECT users.first_name, users.last_name, orders.order_id
FROM users
FULL OUTER JOIN orders
ON users.user_id = orders.user_id;

-- Explanation:
-- `FULL OUTER JOIN` returns all records from both tables, matching where possible.
