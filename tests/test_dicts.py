from hypothesis import given
from hypothesis import strategies as st

from pysnippets.dicts import (
    collect_dictionary,
    find_keys,
    get_nested,
    invert_dictionary,
    key_of_max,
    key_of_min,
    map_values,
    pluck,
    sort_dict_by_value,
)

dicts = st.dictionaries(st.text(max_size=3), st.integers(-5, 5))


@given(dicts)
def test_invert_twice_is_identity_when_values_are_unique(d: dict[str, int]) -> None:
    if len(set(d.values())) == len(d):
        assert invert_dictionary(invert_dictionary(d)) == d


@given(dicts)
def test_collect_dictionary_keeps_every_key(d: dict[str, int]) -> None:
    collected = collect_dictionary(d)
    assert sorted(k for keys in collected.values() for k in keys) == sorted(d)
    for value, keys in collected.items():
        assert find_keys(d, value) == keys


@given(dicts.filter(bool))
def test_key_of_max_and_min(d: dict[str, int]) -> None:
    assert d[key_of_max(d)] == max(d.values())
    assert d[key_of_min(d)] == min(d.values())


@given(dicts)
def test_map_values_keeps_keys(d: dict[str, int]) -> None:
    mapped = map_values(d, lambda v: v * 2)
    assert list(mapped) == list(d)
    assert all(mapped[k] == d[k] * 2 for k in d)


@given(dicts, st.booleans())
def test_sort_dict_by_value_is_sorted(d: dict[str, int], reverse: bool) -> None:
    values = list(sort_dict_by_value(d, reverse=reverse).values())
    assert values == sorted(d.values(), reverse=reverse)


def test_get_nested_returns_default_on_any_missing_step() -> None:
    data = {"a": [{"b": 1}], "n": None}
    assert get_nested(data, ["a", 0, "b"]) == 1
    assert get_nested(data, ["a", 5, "b"], default="x") == "x"
    assert get_nested(data, ["n", "b"], default="x") == "x"
    assert get_nested(data, []) is data


def test_pluck_has_one_result_per_record() -> None:
    records: list[dict[str, int | None]] = [{"a": 1}, {}, {"a": None}]
    assert pluck(records, "a") == [1, None, None]
