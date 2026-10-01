# Changelog

## 0.1.0 (2026-10-01)

First release.

- 40 snippets in five categories: lists (16), dicts (8), strings (8), numbers (5) and dates (3). Every one is typed, passes `mypy --strict`, and has doctests that run on Python 3.11 to 3.14.
- Property-based tests with Hypothesis for the claims that matter.
- Fixes for bugs in the originals, noted on each page: `union_by` ordering, `unique_elements` losing order, `chunk_into_n` uneven chunks, `deep_flatten` recursing into strings, `months_diff` counting 30-day blocks, `is_weekday` defaulting to the import date, and more.
- "The stdlib already does this": 22 verified rows.
- "Python idioms for JavaScript developers": 31 verified rows covering 52 retired snippets.
- The `snip` CLI: `new`, `sync`, `validate`, `generate`.
- Website with search, an in-browser Run panel (Pyodide), light and dark themes.
