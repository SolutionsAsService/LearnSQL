-- This query demonstrates how to update existing records in a table.
UPDATE users
SET age = 31
WHERE first_name = 'John' AND last_name = 'Doe';

-- Explanation:
-- `UPDATE` modifies existing data in a table.
-- `SET` is used to assign new values.
-- `WHERE` ensures only specific records are updated.
