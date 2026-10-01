"""Content rules. Each returns human-readable problems; an empty list is a pass."""

from __future__ import annotations

import ast
import doctest
import re
from collections import Counter
from collections.abc import Iterator
from datetime import date
from pathlib import Path

from snip.model import Repo, Snippet
from snip.sync import MARKER

REQUIRED = ("slug", "title", "summary", "category", "tags", "module", "complexity",
            "since", "published")  # fmt: skip
VERSIONS = ("3.11", "3.12", "3.13", "3.14")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_PROSE_WORDS = 200
MAX_SUMMARY = 160
BANNED = ("simply", "just ", "easy", "easily", "obviously", "of course", "let's",
          "dive into", "in this snippet", "powerful", "seamless")  # fmt: skip


def prose(body: str) -> str:
    """``body`` without code fences, markers or HTML comments."""
    body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    return re.sub(r"<\?snippet[^>]*\?>|<!--.*?-->", "", body, flags=re.DOTALL)


def word_count(text: str) -> int:
    """Words of prose; a run of punctuation like ``--`` isn't a word."""
    return len(re.findall(r"[\w'`.()-]*\w[\w'`.()-]*", text))


def _snippet(repo: Repo, s: Snippet) -> Iterator[str]:
    where = s.page.relative_to(repo.root)
    for key in REQUIRED:
        if key not in s.meta:
            yield f"{where}: missing `{key}`"
    if s.slug != s.dir.name or not SLUG.match(s.slug):
        yield f"{where}: slug must be kebab-case and match the folder name"
    if len(str(s.meta.get("summary", ""))) > MAX_SUMMARY:
        yield f"{where}: summary is over {MAX_SUMMARY} characters"
    categories = {c["id"] for c in repo.categories}
    if s.meta.get("category") not in categories:
        yield f"{where}: unknown category {s.meta.get('category')!r}"
    module = str(s.meta.get("module", ""))
    if not module.startswith(f"{s.meta.get('category')}/"):
        yield f"{where}: module must live in its category's package"
    for tag in s.meta.get("tags") or []:
        if tag not in repo.tags:
            yield f"{where}: unknown tag {tag!r} (add it to content/tags.yaml)"
    if str(s.meta.get("since")) not in VERSIONS:
        yield f"{where}: since must be one of {', '.join(VERSIONS)}"
    if not isinstance(s.meta.get("published"), date):
        yield f"{where}: published must be a YYYY-MM-DD date"
    known = repo.by_slug()
    for slug in s.meta.get("related") or []:
        if slug not in known or slug == s.slug:
            yield f"{where}: related {slug!r} is not another snippet"

    if s.origin is not None:
        names = set(repo.upstream["snippets"])
        if not s.upstream:
            yield f"{where}: origin.upstream must list the original snippet(s)"
        for name in s.upstream:
            if name not in names:
                yield f"{where}: origin.upstream {name!r} is not an upstream snippet"
        if not s.origin.get("change"):
            yield f"{where}: origin.change must say what changed (CC BY 4.0)"

    text = prose(s.body)
    if (n := word_count(text)) > MAX_PROSE_WORDS:
        yield f"{where}: {n} words of prose; the limit is {MAX_PROSE_WORDS}"
    lowered = f"{s.meta.get('summary', '')} {text}".lower()
    for phrase in BANNED:
        if phrase in lowered:
            yield f"{where}: avoid {phrase.strip()!r}"
    if "## How it works" not in s.body:
        yield f"{where}: needs a '## How it works' section"

    parts = Counter(
        (m.group(2) or "code")
        for line in s.body.splitlines()
        if (m := MARKER.match(line))
    )
    if parts != Counter({"code": 1, "examples": 1}):
        yield f"{where}: needs exactly one code marker and one examples marker"
    for line in s.body.splitlines():
        if (m := MARKER.match(line)) and m.group(1) != module:
            yield f"{where}: marker points at {m.group(1)!r}, not {module!r}"

    if not s.module_path.is_file():
        yield f"{where}: module {module!r} does not exist"
        return
    functions = s.module.functions
    if not functions:
        yield f"{where}: {module} has no public function"
    for fn in functions:
        if not fn.examples:
            yield f"{module}: {fn.name}() has no doctest example"
    if len(s.module.examples) < 2:
        yield f"{module}: needs at least two examples (one an edge case)"
    exported = _exports(s.module_path.parent / "__init__.py")
    for fn in functions:
        if fn.name not in exported:
            yield f"{module}: {fn.name} is missing from the package's __all__"


def _exports(init: Path) -> set[str]:
    tree = ast.parse(init.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets
        ):
            value = ast.literal_eval(node.value)
            return set(value)
    return set()


def _examples_parse(where: str, text: str) -> Iterator[str]:
    if not doctest.DocTestParser().get_examples(text):
        yield f"{where}: example has no >>> lines"


def _data(repo: Repo) -> Iterator[str]:
    ids: Counter[str] = Counter()
    for row in repo.stdlib:
        where = f"content/stdlib.yaml#{row.get('id')}"
        ids[str(row.get("id"))] += 1
        for key in ("id", "instead", "use", "since", "example"):
            if not row.get(key):
                yield f"{where}: missing `{key}`"
        yield from _examples_parse(where, str(row.get("example", "")))
    for row in repo.idioms:
        where = f"content/idioms.yaml#{row.get('id')}"
        ids[str(row.get("id"))] += 1
        for key in ("id", "group", "js", "python", "example"):
            if not row.get(key):
                yield f"{where}: missing `{key}`"
        yield from _examples_parse(where, str(row.get("example", "")))
    for name, count in ids.items():
        if count > 1:
            yield f"content: id {name!r} is used {count} times"


def _upstream(repo: Repo) -> Iterator[str]:
    """Every upstream snippet is accounted for exactly once."""
    names = repo.upstream["snippets"]
    homes: Counter[str] = Counter()
    for s in repo.snippets:
        homes.update(s.upstream)
    for row in [*repo.stdlib, *repo.idioms]:
        homes.update(row.get("upstream") or [])
    homes.update(repo.upstream.get("planned") or [])
    for name in names:
        if homes[name] != 1:
            count = homes[name]
            yield f"content/upstream.yaml: {name!r} is accounted for {count} times"
    for name in homes:
        if name not in names:
            yield f"content: {name!r} is not an upstream snippet"


def validate(repo: Repo) -> list[str]:
    """Run every content rule."""
    problems = []
    for snippet in repo.snippets:
        problems += list(_snippet(repo, snippet))
    problems += list(_data(repo))
    problems += list(_upstream(repo))
    return problems
