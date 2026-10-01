"""Loads the content tree: snippet pages, categories, tags and data files."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from functools import cached_property
from pathlib import Path
from typing import Any

import yaml

from snip.source import Module, parse_module

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


class ContentError(Exception):
    """A content file can't be read at all."""


def read_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    """Split a Markdown file into its YAML frontmatter and body."""
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        raise ContentError(f"{path}: missing --- frontmatter ---")
    data = yaml.safe_load(match.group(1)) or {}
    if not isinstance(data, dict):
        raise ContentError(f"{path}: frontmatter must be a mapping")
    return data, text[match.end() :]


def load_yaml(path: Path) -> Any:
    """Load a YAML data file."""
    return yaml.safe_load(path.read_text(encoding="utf-8"))


@dataclass
class Snippet:
    """A snippet page plus the module it documents."""

    root: Path
    dir: Path
    meta: dict[str, Any]
    body: str

    @property
    def slug(self) -> str:
        return str(self.meta.get("slug", ""))

    @property
    def page(self) -> Path:
        return self.dir / "index.md"

    @property
    def module_path(self) -> Path:
        return self.root / "src" / "pysnippets" / str(self.meta.get("module", ""))

    @cached_property
    def module(self) -> Module:
        return parse_module(self.module_path)

    @property
    def origin(self) -> dict[str, Any] | None:
        origin = self.meta.get("origin")
        return origin if isinstance(origin, dict) else None

    @property
    def upstream(self) -> list[str]:
        return list(self.origin.get("upstream", [])) if self.origin else []

    @property
    def published(self) -> str:
        value = self.meta.get("published", "")
        return value.isoformat() if isinstance(value, date) else str(value)


@dataclass
class Repo:
    """Everything ``snip`` reads, rooted at the repository directory."""

    root: Path
    snippets: list[Snippet] = field(default_factory=list)

    @classmethod
    def load(cls, root: Path) -> Repo:
        repo = cls(root)
        for page in sorted((root / "content" / "snippets").glob("*/index.md")):
            meta, body = read_frontmatter(page)
            repo.snippets.append(Snippet(root, page.parent, meta, body))
        return repo

    @cached_property
    def categories(self) -> list[dict[str, str]]:
        data: list[dict[str, str]] = load_yaml(
            self.root / "content" / "categories.yaml"
        )
        return data

    @cached_property
    def tags(self) -> dict[str, str]:
        data: dict[str, str] = load_yaml(self.root / "content" / "tags.yaml")
        return data

    @cached_property
    def stdlib(self) -> list[dict[str, Any]]:
        data: list[dict[str, Any]] = load_yaml(self.root / "content" / "stdlib.yaml")
        return data

    @cached_property
    def idioms(self) -> list[dict[str, Any]]:
        data: list[dict[str, Any]] = load_yaml(self.root / "content" / "idioms.yaml")
        return data

    @cached_property
    def upstream(self) -> dict[str, Any]:
        data: dict[str, Any] = load_yaml(self.root / "content" / "upstream.yaml")
        return data

    def by_slug(self) -> dict[str, Snippet]:
        return {s.slug: s for s in self.snippets}

    def ordered(self) -> list[Snippet]:
        """Snippets in catalog order: by category, then by title."""
        rank = {c["id"]: i for i, c in enumerate(self.categories)}
        return sorted(
            self.snippets,
            key=lambda s: (rank.get(str(s.meta.get("category")), 99), s.slug),
        )
