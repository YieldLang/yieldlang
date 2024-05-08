"""Utility functions for the YieldLang."""

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
