-- This query demonstrates a LEFT JOIN, which returns all records from the left table and matched records from the right table.
SELECT users.first_name, users.last_name, orders.order_id
FROM users
LEFT JOIN orders
ON users.user_id = orders.user_id;

-- Explanation:
-- `LEFT JOIN` returns all records from the left table (`users`), even if there is no match in the right table (`orders`).
