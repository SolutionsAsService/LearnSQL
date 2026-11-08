# LearnSQL

Eleven SQL queries, every one run. A static site where each result table and figure is the real output of the query, executed in SQLite on a small invented dataset.

- Pages: Home (a poster of all eleven results), Change the table (INSERT / UPDATE / DELETE), Squash many rows into one (COUNT / SUM / AVG / GROUP BY), Put two tables side by side (INNER / LEFT / RIGHT / FULL OUTER JOIN), About.
- Source of truth: the `.sql` files in `basic_operations/`, `aggregate_functions/` and `joins/`. Data: `_src/data/seed.sql`.
- Build: `python3 _src/build.py` (Python 3 with SQLite 3.39+, no other dependencies). It runs every query, writes `site/`, and fails if a printed figure (`EXPECT` in the script) or an internal link drifts.
- Deploy: `vercel.json` serves `site/`. Intended address: https://learnsql.shadw.app/ (not yet deployed).
- Design record: `_src/design/DESIGN-LOG.md`.

Contributing: see [CONTRIBUTING.md](CONTRIBUTING.md). MIT licensed.
