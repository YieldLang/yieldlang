"""Utility functions for the YieldLang."""

from typing import Iterable, TypeVar

from yieldlang.types import EmptyType, is_empty

T = TypeVar("T")


def iter_not_empty(iterable: Iterable[T | EmptyType]) -> Iterable[T]:
    for item in iterable:
        if not is_empty(item):
            yield item
