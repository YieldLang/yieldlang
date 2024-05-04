from typing import Any, Callable, Generator, TypeAlias, TypeGuard, Union

from .constants import Token

Strable: TypeAlias = str | int | float
"""
Type alias for a stringable type.
"""

Terminal: TypeAlias = Strable | Token | None
"""
Type alias for a terminal type.
"""

NonTerminal: TypeAlias = Generator[Union["Symbol"], str, None]
"""
Type alias for a non-terminal type.
"""

Symbol: TypeAlias = Terminal | NonTerminal | Callable[[], "Symbol"]
"""
Type alias for a symbol type.
"""


def is_strable(symbol: Any) -> TypeGuard[Strable]:
    """
    Check if a symbol is stringable.

    :param symbol: The symbol to check.
    :type symbol: Any
    :return: `True` if the symbol is stringable, `False` otherwise.
    :rtype: bool
    """
    return isinstance(symbol, (str, int, float))


def is_token(symbol: Any) -> TypeGuard[Token]:
    """
    Check if a symbol is a token.

    :param symbol: The symbol to check.
    :type symbol: Any
    :return: `True` if the symbol is a token, `False` otherwise.
    :rtype: bool
    """
    return isinstance(symbol, Token)


def is_non_terminal(symbol: Any) -> TypeGuard[NonTerminal]:
    """
    Check if a symbol is a non-terminal.

    :param symbol: The symbol to check.
    :type symbol: Any
    :return: `True` if the symbol is a non-terminal, `False` otherwise.
    :rtype: bool
    """
    return iterable(symbol)


def is_callable(symbol: Any) -> TypeGuard[Callable[[], Symbol]]:
    """
    Check if a symbol is a callable.

    :param symbol: The symbol to check.
    :type symbol: Any
    :return: `True` if the symbol is a callable, `False` otherwise.
    :rtype: bool
    """
    return callable(symbol)


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
