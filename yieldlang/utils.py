from typing import Any, Iterable, TypeVar

from .types import EmptyString, Token

T = TypeVar("T")
"""
Type variable for generic types.
"""


def iterable(obj: Any) -> bool:
    """
    Check if an object is iterable.

    :param obj: The object to check.
    :type obj: Any
    :return: `True` if the object is iterable, `False` otherwise.
    :rtype: bool
    """
    try:
        iter(obj)
    except TypeError:
        return False
    return True


def iter_next(iterable: Iterable[T]):
    """
    Iterate over the next item in an iterable.
    """
    for next_item in iterable:
        yield next_item
        return


def iter_next_not_null(iterable: Iterable[T]):
    """
    Iterate over the next item in an iterable that is not empty.
    """
    for item in iterable:
        if not is_empty_symbol(item):
            yield item
            break


def is_empty_symbol(symbol: Any) -> bool:
    """
    Check if a symbol is empty.

    :param symbol: The symbol to check.
    :type symbol: Any
    :return: `True` if the symbol is empty, `False` otherwise.
    :rtype: bool
    """
    return symbol in (
        None,
        EmptyString,
        Token.Empty,
    )
