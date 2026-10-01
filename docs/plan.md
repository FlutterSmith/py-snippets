# py-snippets: Rebuild Plan

> Status: **approved and shipped as v0.1**. Companions: [design.md](design.md) and the [clickable preview](design-preview.html). Where the build departed from this plan, see the [build log](#build-log) at the end.
> Source analysed: [`30-seconds/30-seconds-of-python`](https://github.com/30-seconds/30-seconds-of-python) at `42680a0` (archived 2023-05-07).
> Toolchain today: Python 3.14 (3.10 reaches end of life on 2026-10-31), uv 0.12, Pyodide 314 (Python 3.14 in the browser).

---

## 0. TL;DR

The original is **160 short Python snippets** with 8.8k stars. Each one is a function plus a usage example whose result is written in a comment. It was archived in 2023, and its content is now just one part of a personal blog.

We ran every documented example. 228 of 242 match their comment. **13 snippets have examples that are wrong or can't be checked**, including one real bug (`union_by` returns elements in the wrong order). The bigger finding is that the collection is a **port of the JavaScript 30-seconds-of-code**:
- About 40 snippets wrap things Python already does natively (`head`, `tail`, `every`, `some`, `for_each`, `curry`).
- About 25 reimplement the standard library (`chunk`, `flatten`, `median`, `factorial`, `cumsum`).
- 131 use 2-space indentation, and 155 have no type hints.

We build **py-snippets: Python snippets that still pass.**
- **Examples are doctests.** Every `>>>` line on the site is executed in CI on Python 3.11, 3.12, 3.13 and 3.14. A wrong comment can't ship.
- **Pythonic, not ported.** Typed, PEP 8, ruff-clean, standard library first.
- **"The stdlib already does this"** is a first-class page. Over 20 of the old snippets become one-line pointers to the built-in you should use instead, each one verified.
- **Run it in your browser.** Every snippet opens in an in-page Python (Pyodide): edit, run, and see the doctests go green.
- **Property-based tests** (Hypothesis) back the claims that matter, for example "`chunk` never loses or reorders an element".
- **Same proven machinery as fluttersmith/tips:** content-as-code, a CLI that keeps docs and code in sync, an Astro site with search and handwritten notes, and weekly freshness checks.

Triage of all 160: **71 keep and modernize · 23 become stdlib pointers · 14 merge into 6 · 52 retire.** That gives about 77 snippet pages plus a stdlib cheat sheet. The first release is **40 snippets plus the cheat sheet**.

---

## 1. Understanding the original

**The idea.** "Short code snippets for all your development needs," readable in 30 seconds. It was a Python spin-off of the hugely popular JavaScript collection (30-seconds-of-code). The site 30secondsofcode.org rendered the Markdown as cards with tags, search and a copy button.

**Who it's for.** Beginner-to-intermediate developers who search "python chunk list" and want a copy-paste answer with a short explanation.

**How it worked end to end.**
```
snippets/<name>.md  (frontmatter: title, tags, cover image, dateModified)
   ├─ prose: one-line summary + bullet "how it works"
   ├─ ```py  the function
   └─ ```py  usage, with expected results as comments   ← never executed
            │
            ▼  (separate repo: 30-seconds-web, Next.js)
   30secondsofcode.org cards · search · copy button
```
There were no tests or linting in the repo. Contributors were told to "test your code before submitting".

**Why it was built this way.** It reused the JavaScript project's format and tooling wholesale. That's why the snippets read like JS: lodash-style helpers, `map`/`lambda` everywhere, 2-space indents, and results like `{ x: 2 }` that aren't valid Python.

## 2. Audit

**Strengths, which we keep:**
- One function per page, explained in a few bullets.
- Copy-pasteable.
- Good naming and tags.
- A pleasant "30-second" reading budget.
- Many genuinely useful utilities (`chunk_into_n`, `bifurcate_by`, `group_by`, `to_roman_numeral`, `slugify`).

**Weaknesses (scripted findings):**

| # | Problem | Evidence |
|---|---|---|
| W1 | Examples never executed | 14 of 242 documented results wrong or unverifiable, across 13 snippets |
| W2 | Real bugs | `union_by` order is non-deterministic (it goes through a `set`). `median` sorts the caller's list in place and shadows `list`. `unique_elements` loses order. `most_frequent` is O(n²) |
| W3 | Not Pythonic | ~40 JS-isms (`head`, `last`, `every`, `none`, `for_each`, `spread`, `curry`, `when`…) |
| W4 | Reinvents the stdlib | ~25 snippets duplicate `itertools`, `math`, `statistics`, `collections`, or the `\|` operator |
| W5 | Dated style | Target is Python 3.6. 155/160 have no type hints, 131/160 use 2-space indents. Results are written in JS syntax (`{ a: 1 }`) |
| W6 | Untestable examples | Results that depend on today's date (`days_ago(5) # date(2020, 10, 23)`), randomness, or `print` |
| W7 | Abandoned | Archived May 2023. The org was archived October 2023 |
| W8 | Thin taxonomy | 9 flat tags. "list" alone covers 91 snippets |

**What's missing entirely:**
- verified examples
- type hints
- complexity notes
- "which Python version"
- property tests
- run-in-browser
- "use the stdlib instead" guidance
- learning paths
- a real contribution workflow

## 3. License: what we may reuse

**CC-BY-4.0** ("All snippets are licensed under the CC-BY-4.0 License"). The README also says: *"Logos, names and trademarks are not to be used without the explicit consent of the owners."*

| Item | Reuse? | Obligation |
|---|---|---|
| Snippet text and code | ✅ Share and adapt, including commercially | **Attribution** (credit, link to the license, **indicate changes**) on every adapted page and in ATTRIBUTION.md |
| The "30 seconds of code" name, logo, cover images | ❌ | Distinct name, no logo, no cover images |
| The 30secondsofcode.org site design | ❌ (not in repo) | Our own design |

**How we comply:**
1. Each adapted snippet gets `origin:` frontmatter. The page footer reads *"Adapted from 30-seconds-of-python by 30 seconds of code contributors, CC BY 4.0. Changed: rewritten with type hints, doctests and fixes."* Pages we rewrite from scratch say "Inspired by…".
2. `ATTRIBUTION.md` lists every adapted snippet, the pinned upstream commit, the CC BY 4.0 link and the non-affiliation line.
3. Our own code and prose are **MIT**. Adapted snippets stay CC BY 4.0, and the repo `LICENSE` says this plainly: MIT for the project, CC BY 4.0 for material adapted from the original, as marked on each page.

## 4. Principles

1. **If it's on the page, it ran.** Every `>>>` example is a doctest, run on 3.11 to 3.14.
2. **Stdlib first.** If Python already has it, say so and show it, and don't ship a worse copy.
3. **Pythonic.** Typed, PEP 8, ruff-clean, mypy `--strict` clean. Generators where they fit. No JS-isms.
4. **Honest about cost.** Each snippet states its time complexity and its edge cases (empty input, `n <= 0`).
5. **Runnable anywhere.** One click opens an editable, in-browser Python.
6. **Generated, not hand-kept:** catalog, nav, attribution, version badges.
7. **Ship in slices.** v0.1 is 40 snippets plus the stdlib cheat sheet.

## 5. Architecture

```
py-snippets/
├─ src/pysnippets/<category>/<name>.py   real, typed functions; examples live in docstrings as doctests
├─ tests/<category>/test_<name>.py       Hypothesis property tests + edge cases
├─ content/snippets/<slug>/index.md      prose + excerpt markers (function, examples)
├─ content/stdlib.md                     "the stdlib already does this" (verified mappings)
├─ tools/snip/                           the `snip` CLI (Python): new, sync, validate, generate
├─ site/                                 Astro site (shared engine with fluttersmith/tips) + Pyodide runner
├─ pyproject.toml · uv.lock              uv-managed; ruff, mypy, pytest, hypothesis as dev deps
└─ .github/workflows/                    ci (matrix 3.11–3.14), site deploy, weekly freshness, links
```

**Snippet source of truth (one file per snippet):**
```python
# src/pysnippets/lists/chunk_into_n.py
from collections.abc import Sequence
from math import ceil


# region snippet
def chunk_into_n[T](items: Sequence[T], n: int) -> list[list[T]]:
    """Split ``items`` into ``n`` lists of (almost) equal size.

    >>> chunk_into_n([1, 2, 3, 4, 5, 6, 7], 4)
    [[1, 2], [3, 4], [5, 6], [7]]
    >>> chunk_into_n([], 3)
    []
    """
    # @note size rounds up, so the last chunk may be shorter
    size = ceil(len(items) / n)
    return [list(items[i : i + size]) for i in range(0, len(items), size or 1)]
# endregion snippet
```
- **PEP 695 generics** (`def f[T]`) need 3.12. Snippets that must run on 3.11 use `TypeVar`. The CI matrix decides, and each page shows a computed "Works on 3.11+" badge.
- `snip sync` copies the region into the Markdown as two fences: the function (docstring stripped, `# @note` kept for the annotation lane) and a `pycon` block built from the doctest. The `pycon` block is what the site shows as a REPL panel. On GitHub it renders as plain `>>>` text.
- `pytest --doctest-modules` runs every example. A `# doctest: +SKIP` needs a `nocheck` reason the validator can see (randomness, current time). Those examples get seeded or fixed-clock versions instead whenever possible.

**`snip` CLI:**
- Written in Python, as a uv-installed entry point. Same contract as `tips`: `sync --check`, `validate`, `generate --check`, `new`.
- Validation:
  - frontmatter schema
  - tags from `tags.yaml`
  - prose ≤ 200 words (these are 30-second reads)
  - banned phrases
  - every function has a doctest
  - every page has a "Complexity" line
  - `origin` set when the snippet is adapted

**Site:**
- Reuses the fluttersmith/tips Astro engine: the annotated code panel, search, RSS, three-way themes and keyboard shortcuts. It gets its own Python identity (see [design.md](design.md)).
- **New: a Run panel** that lazy-loads Pyodide (~6–10 MB, only on the first click, with an honest progress line). It loads the snippet's function into a live REPL with the doctests pre-filled, and shows ✓/✗ per example as you edit.

**CI:**
- `ruff check` and `ruff format --check`
- `mypy --strict`
- `pytest` (doctests + Hypothesis) on **3.11, 3.12, 3.13 and 3.14**
- `snip validate`, `snip sync --check` and `snip generate --check`
- site build, then Pages deploy
- weekly: newest CPython and newest deps
- weekly: link check

The version matrix also computes each snippet's minimum version badge.

## 6. Content strategy

- **Keep and modernize (71):** type hints, 4-space indents, doctests, fixed bugs, complexity notes, edge cases.
- **Stdlib pointers (23):** no snippet page. Each becomes a row on `/stdlib/`, "Instead of writing `chunk`, use `itertools.batched(items, n)` (3.12+)", with a verified example.
- **Merge (14 into 6):** for example `camel`, `kebab` and `snake` become one "Convert between naming cases" page.
- **Retire (52):** JS-isms and trivial wrappers. They're listed in ATTRIBUTION.md with the idiom to use instead (`head(lst)` → `lst[0]`), and the most instructive ones become a single "Python idioms for JavaScript developers" page.
- **New originals** fill the modern-Python gaps:
  - `itertools.pairwise`
  - `functools.cache`
  - structural pattern matching on data
  - `dataclass(slots=True)` helpers
  - `pathlib` recipes
  - a typed `retry` decorator

## 7. Roadmap

| Release | Contents |
|---|---|
| v0.0 | Repo, LICENSE (MIT + CC BY 4.0), ATTRIBUTION, uv project, CI skeleton, `snip` CLI with tests |
| **v0.1** | **40 snippets** (Lists 16, Dicts 8, Strings 8, Math & dates 8) + stdlib cheat sheet + "idioms for JS developers" page + site with Run panel, live on GitHub Pages |
| v0.2–v0.4 | The remaining kept and merged snippets, by category |
| v1.0 | ~77 snippets, learning paths, share cards, originals |

## 8. Quality gates (per snippet)

- [ ] Typed; ruff and mypy `--strict` clean
- [ ] ≥ 2 doctest examples, including one edge case
- [ ] Property test where an invariant exists
- [ ] Complexity line; edge cases stated
- [ ] "Stdlib alternative" line if one exists
- [ ] Origin and credit correct; ≤ 200 words of prose

## 9. Risks

| Risk | Mitigation |
|---|---|
| Pyodide is heavy | Lazy-load on click, cached by the browser, honest progress line; the page is complete without it |
| CC BY 4.0 attribution done wrong | Generated per-page credit with "changes made"; ATTRIBUTION.md table |
| Looks like a fork of 30-seconds | Distinct name and design, retire 52, stdlib-first angle, verified examples |
| 3.11 compatibility vs modern syntax | The CI matrix is the judge; badges show the true minimum |

## 10. Decisions

1. **Name:** `FlutterSmith/py-snippets`, site `fluttersmith.github.io/py-snippets`.
2. **Design:** the "lab notebook" direction in design.md, approved from the clickable preview.

## Appendix A: Triage of all 160 (provisional)

**Keep and modernize (71):**
all_unique · arithmetic_progression · average_by · bifurcate · bifurcate_by · byte_size · capitalize_every_word · chunk_into_n · clamp_number · collect_dictionary · combine_values · compact · count_by · daterange · days_diff · deep_flatten · difference · difference_by · digitize · every_nth · fibonacci · filter_non_unique · filter_unique · find_index_of_all · find_key · find_keys · find_parity_outliers · geometric_progression · get · group_by · hamming_distance · has_duplicates · have_same_contents · in_range · index_of_all · initialize_2d_list · intersection_by · invert_dictionary · is_anagram · is_contained_in · is_prime · key_of_max · key_of_min · longest_item · map_dictionary · map_values · max_by · max_element_index · min_by · min_element_index · months_diff · most_frequent · num_to_range · offset · pad · palindrome · pluck · similarity · slugify · sort_by_indexes · sort_dict_by_key · sort_dict_by_value · split_lines · sum_of_powers · symmetric_difference_by · to_roman_numeral · unfold · union_by · unique_elements · weighted_average · words

**Stdlib pointers (23):**
chunk → `itertools.batched` · flatten → `itertools.chain.from_iterable` · gcd / lcm → `math.gcd`, `math.lcm` · average → `statistics.mean` · median → `statistics.median` · factorial → `math.factorial` · binomial_coefficient → `math.comb` · cumsum → `itertools.accumulate` · frequencies / count_occurrences → `collections.Counter` · max_n / min_n → `heapq.nlargest` / `nsmallest` · degrees_to_rads / rads_to_degrees → `math.radians` / `degrees` · to_binary / to_hex → `bin` / `hex` / `format` · sum_by → `sum(f(x) for x in xs)` · merge_dictionaries → `a | b` · transpose → `zip(*m)` · powerset → `itertools` recipe · roll → `collections.deque.rotate` · reverse → slicing `[::-1]`

**Merge (14 into 6):**
camel + kebab + snake → *naming cases* · add_days + days_ago + days_from_now → *date arithmetic* · hex_to_rgb + rgb_to_hex → *hex and RGB* · is_weekday + is_weekend → *weekday checks* · union + intersection → *set operations that keep order* · compose + compose_right → *compose functions*

**Retire (52):**
head · tail · last · initial · take · take_right · drop · drop_right · every · some · none · find · find_index · find_last · find_last_index · for_each · for_each_right · spread · cast_list · is_empty · key_in_dict · keys_only · values_only · dict_to_list · to_dictionary · check_prop · when · delay · curry · all_equal · capitalize · decapitalize · includes_all · includes_any · reverse_number · pad_number · n_times_string · sample · shuffle · initialize_list_with_range · initialize_list_with_values · celsius_to_fahrenheit · fahrenheit_to_celsius · km_to_miles · miles_to_km · is_even · is_odd · is_divisible · from_iso_date · to_iso_date · merge · symmetric_difference

## Build log

Where v0.1 departed from the plan, and why.

| Plan | Build | Why |
|---|---|---|
| `# region snippet` markers inside each module | The whole module is the snippet | Every module already stands alone; regions added noise. `snip sync` shows the module with each docstring cut to its summary line, and turns the doctests into the `pycon` block. |
| PEP 695 generics (`def f[T]`) where possible | `TypeVar` everywhere | 3.11 is in the support matrix, and one style is easier to copy. Every snippet is honestly 3.11+. |
| Categories: Lists 16, Dicts 8, Strings 8, Math & dates 8 | Numbers 5 and Dates 3 as separate categories | Clearer package names: `pysnippets.numbers`, `pysnippets.dates`. |
| One page per kept snippet | A few pages hold two functions | `index_of_all` + `find_index_of_all`, `key_of_max` + `key_of_min`, `filter_unique` + `filter_non_unique` (renamed `duplicates` and `singles`) read better together. |
| 23 stdlib pointers | 18 rows cover the 23 originals, plus 4 new rows | Pairs like `gcd`/`lcm` share a row. Added `pairwise`, `functools.cache`, `math.isclose` and `textwrap.shorten`. |
| Retired snippets listed in ATTRIBUTION | Every retired snippet has a verified row on the idioms page | 31 rows cover all 52, so each retirement shows its replacement. |
| Triage kept in this appendix | `content/upstream.yaml` is the executable triage | `snip validate` fails unless each of the 160 originals has exactly one home. |

Things the checks caught during the build:
- **A doctest caught a wrong example in a draft.** The draft's `sort_by_indexes` error message named the wrong `zip` argument.
- **A version difference.** An example relied on the text of `max()`'s empty-input error, which changed in 3.12. It was replaced with an example that's stable on every version.
- **Hypothesis found a real limitation.** Single-letter words don't survive a naming-case round trip (`a_b` → `AB` → `ab`). It's now documented on the page and pinned by a test.
- **Each "fixed from the original" claim was checked by running the original code.** Two draft claims didn't hold up and were removed: the original `snake` handles acronyms fine, and the `is_prime` float issue only appears at sizes the original couldn't finish anyway. The `camel` bug replaced them.
