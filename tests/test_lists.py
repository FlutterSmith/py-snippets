from collections import Counter
from itertools import chain

import pytest
from hypothesis import given
from hypothesis import strategies as st

from pysnippets.lists import (
    bifurcate_by,
    chunk_into_n,
    count_by,
    deep_flatten,
    difference_by,
    duplicates,
    every_nth,
    find_index_of_all,
    group_by,
    has_duplicates,
    have_same_contents,
    index_of_all,
    intersection_by,
    most_frequent,
    singles,
    sort_by_indexes,
    union_by,
    unique_elements,
)

ints = st.lists(st.integers(-20, 20))


@given(ints, st.integers(1, 30))
def test_chunk_into_n_keeps_every_item_in_order(items: list[int], n: int) -> None:
    chunks = chunk_into_n(items, n)
    assert len(chunks) == n
    assert list(chain.from_iterable(chunks)) == items
    sizes = [len(c) for c in chunks]
    assert max(sizes) - min(sizes) <= 1
    assert sizes == sorted(sizes, reverse=True)


@pytest.mark.parametrize("n", [0, -1])
def test_chunk_into_n_rejects_non_positive_n(n: int) -> None:
    with pytest.raises(ValueError, match="at least 1"):
        chunk_into_n([1], n)


@given(ints)
def test_bifurcate_by_is_a_partition(items: list[int]) -> None:
    passed, failed = bifurcate_by(iter(items), lambda n: n > 0)
    assert all(n > 0 for n in passed)
    assert not any(n > 0 for n in failed)
    assert Counter(passed) + Counter(failed) == Counter(items)


def test_bifurcate_by_calls_predicate_once_per_item() -> None:
    calls: list[int] = []

    def check(n: int) -> bool:
        calls.append(n)
        return n % 2 == 0

    bifurcate_by(iter([1, 2, 3]), check)
    assert calls == [1, 2, 3]


@given(ints)
def test_group_by_and_count_by_agree(items: list[int]) -> None:
    groups = group_by(items, abs)
    counts = count_by(items, abs)
    assert {k: len(v) for k, v in groups.items()} == counts
    assert sorted(chain.from_iterable(groups.values())) == sorted(items)


nested = st.recursive(
    st.integers() | st.text(max_size=3),
    lambda inner: st.lists(inner, max_size=4),
    max_leaves=20,
)


@given(st.lists(nested, max_size=5))
def test_deep_flatten_yields_only_leaves(items: list[object]) -> None:
    flat = list(deep_flatten(items))
    assert all(isinstance(x, int | str) for x in flat)


@given(ints, st.integers(1, 10))
def test_every_nth_matches_a_filter(items: list[int], n: int) -> None:
    expected = [x for i, x in enumerate(items, start=1) if i % n == 0]
    assert every_nth(items, n) == expected


@given(ints, st.integers(-20, 20))
def test_index_of_all_points_at_every_match(items: list[int], value: int) -> None:
    found = index_of_all(items, value)
    assert found == find_index_of_all(items, lambda x: x == value)
    assert len(found) == items.count(value)
    assert all(items[i] == value for i in found)


@given(ints)
def test_unique_elements_keeps_first_occurrences(items: list[int]) -> None:
    unique = unique_elements(items)
    assert set(unique) == set(items)
    assert len(unique) == len(set(items))
    assert unique == sorted(unique, key=items.index)


@given(ints)
def test_duplicates_and_singles_split_the_distinct_values(items: list[int]) -> None:
    dupes, once = duplicates(items), singles(items)
    assert set(dupes).isdisjoint(once)
    assert set(dupes) | set(once) == set(items)
    assert all(items.count(x) == 1 for x in once)


@given(ints, ints)
def test_set_operations_by_key(a: list[int], b: list[int]) -> None:
    diff = difference_by(a, b, abs)
    both = intersection_by(a, b, abs)
    assert Counter(diff) + Counter(both) == Counter(a)
    union = union_by(a, b, abs)
    assert len({abs(x) for x in union}) == len(union)
    assert {abs(x) for x in union} == {abs(x) for x in a + b}


def test_union_by_order_is_first_seen() -> None:
    assert union_by([3, 1], [2, -3, 4], abs) == [3, 1, 2, 4]


@given(ints)
def test_has_duplicates_matches_set_size(items: list[int]) -> None:
    assert has_duplicates(items) == (len(items) != len(set(items)))


@given(ints, st.randoms())
def test_have_same_contents_ignores_order(items: list[int], rnd: object) -> None:
    shuffled = sorted(items, key=lambda _: rnd.random())  # type: ignore[attr-defined]
    assert have_same_contents(items, shuffled)
    assert have_same_contents(items, [*items, 0]) is False


@given(st.lists(st.integers(0, 5), min_size=1))
def test_most_frequent_has_the_top_count(items: list[int]) -> None:
    top = most_frequent(items)
    assert items.count(top) == max(Counter(items).values())
    tied = [x for x in items if items.count(x) == items.count(top)]
    assert top == tied[0]


def test_most_frequent_rejects_empty_input() -> None:
    with pytest.raises(ValueError, match="empty"):
        most_frequent([])


@given(st.lists(st.tuples(st.integers(), st.integers())))
def test_sort_by_indexes_orders_by_index(pairs: list[tuple[int, int]]) -> None:
    items = [item for item, _ in pairs]
    indexes = [index for _, index in pairs]
    result = sort_by_indexes(items, indexes)
    assert result == [item for item, _ in sorted(pairs, key=lambda p: p[1])]


def test_sort_by_indexes_never_compares_items() -> None:
    assert sort_by_indexes([{"a": 1}, {"b": 2}], [1, 1]) == [{"a": 1}, {"b": 2}]
