# py-snippets: Look & Feel

> Status: **approved**. A sibling of [fluttersmith/tips](https://github.com/FlutterSmith/tips): same family, its own personality.

## 1. Fresh eyes on the original

| What | Problem |
|---|---|
| Generic snippet "cards" with stock cover photos (red berries, jars on a shelf) | Decoration unrelated to the code. Interchangeable with any blog |
| Result comments (`# [[1, 2], [3, 4], [5]]`) | Look identical whether or not they're true. Some aren't |
| Brand, logo and tag pills shared with the JS site | Python is a second-class citizen in a JS-shaped product |
| No sense of "does this run, and on which version?" | Trust has to be taken on faith |

## 2. The idea: **"the lab notebook"**

Python's home is the **interactive interpreter**: the `>>>` prompt, an answer printed back, and the notebook where you scribble and try things. Doctest is literally that transcript, kept honest.

- **Light theme = graph paper.** A faint 24px grid on cool off-white, like a squared lab notebook. Ink-blue prompts.
- **Dark theme = chalkboard.** Deep green-black, chalk-white text, the grid as faint chalk lines.
- **The REPL panel is the hero component.** Examples are shown as a real session: `>>>` in ink blue, results below. In the left gutter, a **✓ tick per example** shows that this exact line passed on 3.11–3.14; hovering a tick explains it.
- **Handwritten margin notes and arrows** carry over from fluttersmith/tips. That's the family signature.
- **Run it** turns any snippet into a live, editable session in the page. Ticks go green or red as you edit.

The contrast: **printed, verified machine output** (mono, ticks) next to **a human hand** (notes).

## 3. Tokens

| Token | Light (graph paper) | Dark (chalkboard) | Role |
|---|---|---|---|
| `--ground` | `#F4F7F3` | `#0F1713` | Page |
| `--grid` | `#E1E8E0` | `#18241E` | 24px graph lines (1px, very faint) |
| `--paper` | `#FBFCFA` | `#131D18` | Raised areas |
| `--ink` | `#132019` | `#E6EEE8` | Text (green-black / chalk) |
| `--ink-2` | `#4A5A50` | `#9CB0A3` | Secondary |
| `--rule` | `#CFD9D0` | `#22332A` | Hairlines |
| `--prompt` | `#2448B8` | `#93B4FF` | `>>>`, links, focus |
| `--pass` | `#1C7A4A` | `#5FD49A` | Ticks, "verified" |
| `--fail` | `#B3362A` | `#FF8A7A` | Failing example in Run mode (glyph + colour) |
| `--panel` | `#16211C` | `#09100C` | Code / REPL panel (dark in both) |
| `--marker` | `#FFD54A` | `#FFD54A` | Handwritten notes on the panel |

Syntax colours on the panel: keywords `#7FD0E6`, builtins `#C9B6FF`, strings `#A8DCA0`, numbers `#FFB98F`, comments `#7F9288` italic. Checked for AA contrast.

**Type:**

| Role | Face | Why |
|---|---|---|
| Display | **Gloock** | A high-contrast serif with a lab-journal feel. Titles only |
| Body | Atkinson Hyperlegible Next | Shared with the family |
| Code / REPL / metadata | Fragment Mono | Shared with the family |
| Notes | Kalam | Shared with the family |

The scale is 1.25 from 17px. Prose is at most 64ch.

**Shape:** 2px radius on UI, 10px on panels. No card grids. Rows and hairlines everywhere else.

## 4. Key screens

**Home**
```
fluttersmith/py-snippets            Search ( / )   ◐   GitHub ↗
──────────────────────────────────────────────────────────────
Python snippets                  ┌ REPL ─────────────────────┐
that still pass.                 │ ✓ >>> chunk_into_n(r, 3)  │  ← lines type in,
                                 │   [[0, 1, 2], [3, 4, 5]…  │    ticks land one by one
77 typed functions. Every        │ ✓ >>> slugify("Hello, W…  │
example runs on 3.11–3.14.       │   'hello-world'           │
[Random snippet r] [Stdlib ▸]    └───────────────────────────┘
──────────────────────────────────────────────────────────────
pysnippets/                      LATEST
├─ lists/        28  chunk_into_n.py …     rows: name() · summary · O(n) · 3.11+
├─ dicts/        14
├─ strings/      12              THE STDLIB ALREADY DOES THIS → 23 one-liners
└─ dates/  …
```
The index is the package tree, with real module names.

**Snippet page:** breadcrumb `pysnippets.lists` → the title in Gloock as the function signature (`chunk_into_n(items, n)`) → one-sentence summary → **function panel** (annotated) → **REPL panel** (ticks) → `[▶ Run in your browser]` → "How it works" (≤ 4 bullets) → `Complexity: O(n) time · O(n) space` → **"The stdlib may already do this"** strip when it applies → version chips `3.11 ✓ 3.12 ✓ 3.13 ✓ 3.14 ✓` → related → credit line.

**Stdlib cheat sheet** (`/stdlib/`): a two-column ledger, "Instead of writing… / Use…". Each row has a mini REPL proof and a version tag, with search filtering.

**404:** a traceback.
```
Traceback (most recent call last):
  File "fluttersmith.github.io", line 404, in <module>
NameError: name 'this_page' is not defined. Did you mean: 'chunk_into_n'?
```
The "Did you mean" suggestion is a real fuzzy match on the URL.

## 5. Motion

- **One orchestrated moment:** on the home page, the hero REPL types its two examples (≈ 900ms total) and the ticks land in turn. It is complete at rest; reduced motion shows it finished.
- Run mode: each tick flips with a 120ms scale-in when a result changes.
- Everything else is 80–150ms state feedback. No parallax, no scroll effects.

## 6. Voice

Same rules as fluttersmith/tips: plain, specific, no emoji, no hype. Python-specific additions:
- Say which version a feature needs ("3.12+").
- Say what happens on empty input.
- Prefer "use `Counter`" over clever one-liners.

## 7. Accessibility and performance

- Ticks have text equivalents ("passed on Python 3.11 to 3.14").
- The Run panel is fully keyboard operable, and results are announced (`aria-live`).
- Pyodide loads only on Run (lazy, with a progress line). A page without Run ships ≤ 25KB JS.
- Fonts are self-hosted and subset. Lighthouse ≥ 95.
