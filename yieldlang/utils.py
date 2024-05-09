"""Utility functions for the YieldLang."""

import dataclasses
import json
from typing import Iterable, Iterator, TypeVar

from yieldlang.types import EmptyType, Symbol, is_empty, is_iterable

T = TypeVar("T")
"""Type variable for generic types."""


def iter_not_empty(iterable: Iterable[T | EmptyType]) -> Iterator[T]:
    """Iterate over non-empty items in an iterable.

    Args:
        iterable (Iterable[T | EmptyType]): The iterable to iterate over.
    Returns:
        Iterator[T]: The iterator over non-empty items.
    """
    for item in iterable:
        if not is_empty(item):
            yield item


def symbol_to_iterator(symbol: Symbol) -> Iterator[Symbol]:
    """Convert a symbol to an iterator.

    Args:
        symbol (Symbol): The symbol to convert.
    Returns:
        Iterator[Symbol]: The iterator over the symbol.
    """
    if is_iterable(symbol):
        yield from symbol
    else:
        yield symbol


class DataclassJSONEncoder(json.JSONEncoder):
    """JSON encoder for dataclasses."""

    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def dataclass_to_json(dc: object):
    """Convert a dataclass to a JSON string."""
    return json.dumps(dc, cls=DataclassJSONEncoder)


def dataclass_to_dict(dc):
    """Convert a dataclass to a dictionary."""
    return dataclasses.asdict(dc)


def minify_ctx_tree(ctx_tree_dict: dict):
    """Minify a context tree dictionary by removing empty values."""
    new_dict = {}
    for k, v in ctx_tree_dict.items():
        if v is None or v == []:
            continue
        elif isinstance(v, dict):
            new_dict[k] = minify_ctx_tree(v)
        elif isinstance(v, list):
            new_dict[k] = [minify_ctx_tree(item) for item in v]
        else:
            new_dict[k] = v
    return new_dict
