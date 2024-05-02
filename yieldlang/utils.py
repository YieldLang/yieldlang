from typing import Any, Iterable, TypeVar

from .types import EmptyString, Token

T = TypeVar("T")


def iterable(obj: Any):
    """
    Check if an object is iterable.
    :param obj: The object to check.
    :type obj: Any
    :return: True if the object is iterable, False otherwise.
    :rtype: bool
    """
    try:
        iter(obj)
    except TypeError:
        return False
    return True


def iter_next(iterable: Iterable[T]):
    for next_item in iterable:
        yield next_item
        return


def iter_next_not_null(iterable: Iterable[T]):
    for item in iterable:
        if not is_empty_symbol(item):
            yield item
            break


def is_empty_symbol(symbol: Any) -> bool:
    return symbol in (
        None,
        EmptyString,
        Token.Empty,
    )
