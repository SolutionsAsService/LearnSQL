-- Invented sample data for the LearnSQL site. Nobody here is a real person.
CREATE TABLE users (
  user_id    INTEGER PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name  TEXT NOT NULL,
  age        INTEGER NOT NULL
);
CREATE TABLE orders (
  order_id     INTEGER PRIMARY KEY,
  user_id      INTEGER,          -- no foreign key on purpose: order 107 has no matching user
  order_amount REAL NOT NULL
);
INSERT INTO users VALUES
  (1,'Ana','Silva',25),(2,'Li','Wei',25),(3,'Omar','Haddad',42),(4,'Mira','Novak',19),
  (5,'Tom','Ellis',17),(6,'Priya','Nair',34),(7,'Sven','Berg',19);
INSERT INTO orders VALUES
  (101,1,120.00),(102,1,45.50),(103,2,80.00),(104,4,30.00),(105,4,15.25),(106,6,200.00),(107,99,60.00);
