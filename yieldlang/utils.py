"""Utility functions for the YieldLang."""

from typing import Iterable, Iterator, TypeVar

from yieldlang.types import EmptyType, Symbol, is_empty, is_iterable

T = TypeVar("T")


def iter_not_empty(iterable: Iterable[T | EmptyType]) -> Iterator[T]:
    for item in iterable:
        if not is_empty(item):
            yield item


def symbol_to_iterator(symbol: Symbol) -> Iterator[Symbol]:
    if is_iterable(symbol):
        yield from symbol
    else:
        yield symbol
