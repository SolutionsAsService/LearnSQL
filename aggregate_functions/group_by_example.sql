-- This query demonstrates how to use GROUP BY with an aggregate function.
SELECT age, COUNT(*) AS count
FROM users
GROUP BY age;

-- Explanation:
-- `GROUP BY` groups records based on the column (`age`).
-- `COUNT(*)` returns the number of rows in each group.
