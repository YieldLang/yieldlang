from typing import Any, Callable, Generator, TypeAlias, TypeGuard, Union

from yieldlang.constants import Token
from yieldlang.utils import is_iterable

Strable: TypeAlias = str | int | float
"""Type alias for a stringable type."""

Terminal: TypeAlias = Strable | Token | None
"""Type alias for a terminal type."""

NonTerminal: TypeAlias = Generator[Union["Symbol"], str, None]
"""Type alias for a non-terminal type."""

SymbolFn: TypeAlias = Callable[[], "Symbol"]
"""Type alias for a symbol function type."""

Symbol: TypeAlias = Terminal | NonTerminal | SymbolFn | "SymbolProxy"
"""Type alias for a symbol type."""

SymbolProxyFn: TypeAlias = Callable[..., "SymbolProxy"]
"""Type alias for a symbol proxy function type."""


class SymbolProxy:
    """A proxy for a symbol."""

    def __init__(self, fn: SymbolProxyFn, *args: Symbol, **kwargs) -> None:
        self.fn = fn
        self.args = args
        self.kwargs = kwargs


def is_symbol_proxy(obj: Any) -> TypeGuard[SymbolProxy]:
    """Check if an object is a symbol proxy.

    Args:
        obj (Any): The object to check.
    Returns:
        bool: ``True`` if the object is a symbol proxy, ``False`` otherwise.
    """
    return isinstance(obj, SymbolProxy)


def is_non_terminal(symbol: Symbol) -> TypeGuard[NonTerminal]:
    """Check if a symbol is a non-terminal.

    Args:
        symbol (Symbol): The symbol to check.
    Returns:
        bool: ``True`` if the symbol is a non-terminal, ``False`` otherwise.
    """

    return is_iterable(symbol)


def is_callable(symbol: Symbol) -> TypeGuard[Callable[[], Symbol]]:
    """Check if a symbol is callable.

    Args:
        symbol (Symbol): The symbol to check.
    Returns:
        bool: ``True`` if the symbol is callable, ``False`` otherwise.
    """
    return callable(symbol)


def is_strable(obj: Any) -> TypeGuard[Strable]:
    """Check if an object is stringable.

    Args:
        obj (Any): The object to check.
    Returns:
        bool: ``True`` if the object is stringable, ``False`` otherwise.
    """
    return isinstance(obj, (str, int, float))


def is_token(obj: Any) -> TypeGuard[Token]:
    """Check if an object is a token.

    Args:
        obj (Any): The object to check.
    Returns:
        bool: ``True`` if the object is a token, ``False`` otherwise.
    """
    return isinstance(obj, Token)
