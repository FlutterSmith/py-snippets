"""Tests for the snip CLI, run against a copy of the real repository."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from snip.cli import main
from snip.model import Repo
from snip.source import Example, markdown_summary, parse_module, to_pycon
from snip.validate import validate, word_count

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def repo_copy(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    for name in ("content", "src"):
        shutil.copytree(ROOT / name, tmp_path / name)
    for name in ("pyproject.toml", "CATALOG.md", "ATTRIBUTION.md"):
        shutil.copy(ROOT / name, tmp_path / name)
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_parse_module_reads_functions_and_examples() -> None:
    module = parse_module(ROOT / "src/pysnippets/lists/index_of_all.py")
    assert [f.name for f in module.functions] == ["index_of_all", "find_index_of_all"]
    assert module.functions[0].signature == (
        "index_of_all(items: Iterable[T], value: T) -> list[int]"
    )
    assert len(module.examples) == 4
    # Docstrings are cut to their summary in the displayed code.
    assert (
        '"""Return every index at which ``value`` occurs in ``items``."""'
        in module.code
    )
    assert ">>>" not in module.code


def test_to_pycon_renders_continuation_lines() -> None:
    example = Example("for x in [1]:\n    print(x)\n", "1\n")
    assert to_pycon(example) == ">>> for x in [1]:\n...     print(x)\n1"


def test_markdown_summary_converts_rest_literals() -> None:
    assert markdown_summary("Split ``items`` in ``n``.") == "Split `items` in `n`."


def test_word_count_ignores_punctuation_runs() -> None:
    assert word_count("`divmod` gives the base -- size.") == 5


def test_the_real_repository_is_valid() -> None:
    assert validate(Repo.load(ROOT)) == []


def test_sync_and_generate_are_current(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.MonkeyPatch.context() as mp:
        mp.chdir(ROOT)
        assert main(["sync", "--check"]) == 0
        assert main(["generate", "--check"]) == 0
    assert "Pages match the code." in capsys.readouterr().out


def test_sync_rewrites_a_stale_fence(repo_copy: Path) -> None:
    page = repo_copy / "content/snippets/digitize/index.md"
    fresh = page.read_text()
    page.write_text(fresh.replace("[1, 2, 3]", "[3, 2, 1]"))
    assert main(["sync", "--check"]) == 1
    assert main(["sync"]) == 0
    assert page.read_text() == fresh


def test_validate_flags_a_missing_doctest(repo_copy: Path) -> None:
    module = repo_copy / "src/pysnippets/numbers/digitize.py"
    text = module.read_text()
    start = text.index("    >>>")
    end = text.index('    """\n', start)
    module.write_text(text[:start] + text[end:])
    problems = validate(Repo.load(repo_copy))
    assert "numbers/digitize.py: digitize() has no doctest example" in problems


def test_validate_flags_unaccounted_upstream_snippets(repo_copy: Path) -> None:
    upstream = repo_copy / "content/upstream.yaml"
    upstream.write_text(upstream.read_text().replace("  - fibonacci\n", "", 1))
    problems = validate(Repo.load(repo_copy))
    assert "content/upstream.yaml: 'fibonacci' is accounted for 0 times" in problems


def test_validate_flags_banned_phrases_and_bad_tags(repo_copy: Path) -> None:
    page = repo_copy / "content/snippets/pluck/index.md"
    text = page.read_text().replace("tags: [mapping, nested]", "tags: [mapping, nope]")
    page.write_text(
        text.replace("## How it works", "Simply put, it works.\n\n## How it works")
    )
    problems = validate(Repo.load(repo_copy))
    where = "content/snippets/pluck/index.md"
    assert f"{where}: unknown tag 'nope' (add it to content/tags.yaml)" in problems
    assert f"{where}: avoid 'simply'" in problems


def test_new_scaffolds_a_module_and_page(repo_copy: Path) -> None:
    assert main(["new", "lists", "take_while_sum"]) == 0
    assert (repo_copy / "src/pysnippets/lists/take_while_sum.py").is_file()
    page = (repo_copy / "content/snippets/take-while-sum/index.md").read_text()
    assert "module: lists/take_while_sum.py" in page
    with pytest.raises(SystemExit, match="already exists"):
        main(["new", "lists", "take_while_sum"])


def test_generate_site_writes_meta(repo_copy: Path) -> None:
    assert main(["generate", "--site"]) == 0
    meta = (repo_copy / "site/src/generated/meta.json").read_text()
    assert '"slug": "chunk-into-n"' in meta
