# DESIGN-LOG: LearnSQL (DADA-Lite run)

**Run type: DADA-Lite** (by the owner's ruling, 8 Nov 2026). **Mode: Adaptive** (a public of learners). One build round, measure-first, no critic panel was convened; the owner graded the result A, which is recorded below.

## Plan
Rebuild an existing repository (eleven `.sql` files, a one-word README) as a multi-page static site in the shape of `esoteric-languages`. Seed: stance `Make It Bigger (Paula Scher)`, rule `Grid Systems in Graphic Design (Josef Müller-Brockmann)`. The signature graphic is the landing poster: one tile per query carrying the figure the query returned.

## Moves
- **M1 SOURCE. The repo's own `.sql` files are the content.** The build parses and executes each in SQLite on invented seed data; every table and figure printed is what came back. Measure: 11 of 11 queries run, figures pinned in `EXPECT`, build fails on drift.
- **M2 POSTER.** Home is one poster of all eleven results plus an About tile (12 tiles, no empty cell). Measure: whole poster inside the first 800px at 1280.
- **M3 MARK IN WORDS.** Join rows say `both`, `LEFT only`, `RIGHT only`; DML rows say `new`, `changed`, `removed`. Venn diagrams are drawn from the join kind.
- **M4 DELETE CLAIMS.** Data declared invented; About states that MySQL has no FULL OUTER JOIN; "not yet deployed" stated in README.

## Measure
| Step | Tool | Result |
|---|---|---|
| Own probes, 5 pages x 3 widths | Playwright | overflow 0; 2 figures overflowing tiles and 1 empty cell found and fixed |
| `audit.py` round 1, widths 1280/390/320 | dada-lite | **TOTAL 161**: SQL text contrast 1.11:1 (inline `code` background leaked into the dark block), source links 17px tall |
| After fix | dada-lite | **TOTAL 0** |
| Look at the diagram | screenshot | "orders" clipped at the edge, then labels colliding; fixed (labels under circles, spaced) |

The audit found what my own probes did not: contrast. Own probes covered overflow, targets and text size, not contrast.

## Stop check
Audit clean (0). Boldest move (the poster) pushed once and measured. No panel round was run, so the Provocateur, Inclusion, Usability and Craft seats never sat; this is open if the run is ever re-opened as a full or panelled lite run.

## Open
Not deployed (README address is intended). No in-browser SQL editor. Dark mode and reduced motion not screenshotted.

## Human grade
**A.** 8 Nov 2026. The owner: "That's very good thing count it as dada lite that's what dada lite is for that's a an A". The run did what lite is for: one measure-first pass and cheap fixes on a site whose content was already true and runnable.
