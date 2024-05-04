from typing import Any, Callable, Generator, TypeAlias, TypeGuard, Union

from yieldlang.utils import is_iterable

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


def is_non_terminal(symbol: Symbol) -> TypeGuard[NonTerminal]:
    """
    Check if a symbol is a non-terminal.

    :param symbol: The symbol to check.
    :type symbol: Any
    :return: `True` if the symbol is a non-terminal, `False` otherwise.
    :rtype: bool
    """
    return is_iterable(symbol)


def is_callable(symbol: Symbol) -> TypeGuard[Callable[[], Symbol]]:
    """
    Check if a symbol is a callable.

    :param symbol: The symbol to check.
    :type symbol: Any
    :return: `True` if the symbol is a callable, `False` otherwise.
    :rtype: bool
    """
    return callable(symbol)


def is_strable(obj: Any) -> TypeGuard[Strable]:
    """
    Check if an object is stringable.

    :param obj: The object to check.
    :type obj: Any
    :return: `True` if the object is stringable, `False` otherwise.
    :rtype: bool
    """
    return isinstance(obj, (str, int, float))


def is_token(obj: Any) -> TypeGuard[Token]:
    """
    Check if an object is a token.

    :param obj: The object to check.
    :type obj: Any
    :return: `True` if the object is a token, `False` otherwise.
    :rtype: bool
    """
    return isinstance(obj, Token)
