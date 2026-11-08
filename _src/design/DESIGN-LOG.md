# DESIGN-LOG: LearnSQL

**Run type: bounded, not full.** This was a rebuild of an existing repository (eleven `.sql` files and a one-word README) in the shape of `esoteric-languages`. It did **not** convene the DADA critic panel, so it does not meet the dada stop conditions and should not be rated or entered in `ledger/runs.jsonl` as a full run. A full adaptive run is the open item below.

**Mode: Adaptive** (a public of learners; advanced and acceptable both have to hold).

## What was decided
- **Landing = one poster of the whole site, a computed figure per tile** (dada-lessons grade A shape): INSERT +1 row, UPDATE 1 row changed, DELETE −3 rows, COUNT 7, SUM 550.75, AVG 25.8571, GROUP BY 5 groups, INNER 6, LEFT 9, RIGHT 7, FULL OUTER 10.
- **Every claim has a source in the repo.** The `.sql` files are read by the build, executed, and their output is what the pages print. The dataset is declared invented. Nothing else is claimed.
- **Join rows are marked in words, not colour alone:** `both`, `LEFT only`, `RIGHT only`. Insert/update/delete rows are marked `new`, `changed`, `removed`.
- **Venn diagrams drawn from the join kind**, not from an image.
- Build guarantees: every query run; figures pinned in `EXPECT`; internal links and fragments verified.

## Measured (headless Chromium, 360 / 390 / 1280 px, all five pages)
| Probe | Result |
|---|---|
| Horizontal overflow | 0 px on every page and width |
| Interactive targets under 44 px (excluding the off-screen skip link and in-prose links) | 0 |
| Text under 11 px | 0 (after fixing the Venn labels, which were 9 px) |
| Figures overflowing their tile | 2 found (550.75, 25.8571), fixed by a smaller size for figures over 4 characters |
| Empty grid cell on the poster | 1 found, filled with the About tile |

## Not done (open frontier)
- No critic panel, no contrast measurement, no reduced-motion or dark-mode screenshots, no `measure.py` presets.
- No answers to "try it yourself": the site is read-only. An in-browser editor (sql.js) would be the natural next move.
- The `.sql` files target the dialect SQLite accepts; MySQL has no `FULL OUTER JOIN` (stated on About).
- Not deployed; the address in the README is intended, not live.
