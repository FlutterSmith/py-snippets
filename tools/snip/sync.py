"""Keeps the code fences in snippet pages identical to the modules."""

from __future__ import annotations

import re

from snip.model import Repo, Snippet

MARKER = re.compile(r'^<\?snippet\s+"([^"]+)"(?:\s+part="(\w+)")?\s*\?>$')
FENCE = re.compile(r"^(`{3,})")


def render_fences(snippet: Snippet, body: str) -> str:
    """Return ``body`` with the fence after every ``<?snippet?>`` marker rebuilt."""
    lines = body.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        i += 1
        match = MARKER.match(line)
        if not match:
            continue
        part = match.group(2) or "code"
        module = snippet.module
        if part == "code":
            lang, content = "python", module.code.rstrip("\n")
        elif part == "examples":
            lang, content = "pycon", module.pycon
        else:
            raise ValueError(f"{snippet.page}: unknown part {part!r}")
        # Drop the existing fence, if there is one, and write a fresh one.
        if i < len(lines) and (fence := FENCE.match(lines[i])):
            close = fence.group(1)
            j = i + 1
            while j < len(lines) and lines[j].strip() != close:
                j += 1
            i = j + 1
        out += [f"```{lang}", content, "```"]
    return "\n".join(out)


def sync(repo: Repo, *, check: bool) -> list[str]:
    """Rewrite out-of-date pages, or with ``check`` only report them."""
    stale = []
    for snippet in repo.snippets:
        text = snippet.page.read_text(encoding="utf-8")
        head = text[: len(text) - len(snippet.body)]
        fresh = head + render_fences(snippet, snippet.body)
        if fresh != text:
            stale.append(str(snippet.page.relative_to(repo.root)))
            if not check:
                snippet.page.write_text(fresh, encoding="utf-8")
    return stale
