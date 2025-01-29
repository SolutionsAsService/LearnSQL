-- This query demonstrates a RIGHT JOIN, which returns all records from the right table and matched records from the left table.
SELECT users.first_name, users.last_name, orders.order_id
FROM users
RIGHT JOIN orders
ON users.user_id = orders.user_id;

-- Explanation:
-- `RIGHT JOIN` returns all records from the right table (`orders`), even if there is no match in the left table (`users`).
