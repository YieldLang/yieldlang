from enum import Enum
from typing import (
    Any,
    Callable,
    Generator,
    Iterator,
    Literal,
    TypeAlias,
    TypeGuard,
    Union,
)

EmptyString: Literal[""] = ""
"""Empty string constant."""

EmptyStringType: TypeAlias = Literal[""]
"""Type alias for an empty string type."""


class Token(Enum):
    """Token enumeration for the generator."""

    Empty = 0
    """Empty token."""
    EOF = 1
    """End of file token."""
    EOS = 2
    """End of statement token."""


EmptyType: TypeAlias = None | EmptyStringType | Literal[Token.Empty]
"""Type alias for an empty type."""

Emptys = (None, EmptyString, Token.Empty)
"""Tuple of empty types."""

Strable: TypeAlias = str | int | float
"""Type alias for a stringable type."""

Terminal: TypeAlias = Strable | Token | None
"""Type alias for a terminal type."""

NonTerminal: TypeAlias = Generator[Union["Symbol"], str, None]
"""Type alias for a non-terminal type."""

CallableSymbol: TypeAlias = Callable[[], "Symbol"]
"""Type alias for a callable symbol type."""

Symbol: TypeAlias = Terminal | NonTerminal | CallableSymbol | "ProxySymbol"
"""Type alias for a symbol type."""

ProxySymbolFn: TypeAlias = Callable[..., "ProxySymbol"]
"""Type alias for a symbol proxy function type."""


class ProxySymbol:
    """A proxy symbol that represents a symbol that is not yet evaluated."""

    def __init__(self, fn: ProxySymbolFn, *args: Symbol, **kwargs) -> None:
        self.fn = fn
        self.args = args
        self.kwargs = kwargs


def is_symbol_proxy(obj: Any) -> TypeGuard[ProxySymbol]:
    """Check if an object is a symbol proxy.

    Args:
        obj (Any): The object to check.
    Returns:
        bool: ``True`` if the object is a symbol proxy, ``False`` otherwise.
    """
    return isinstance(obj, ProxySymbol)


def is_non_terminal(symbol: Symbol) -> TypeGuard[NonTerminal]:
    """Check if a symbol is a non-terminal.

    Args:
        symbol (Symbol): The symbol to check.
    Returns:
        bool: ``True`` if the symbol is a non-terminal, ``False`` otherwise.
    """

    return is_iterator(symbol) and not isinstance(symbol, str)


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


def is_iterator(obj: Any) -> TypeGuard[Iterator]:
    """Check if an object is iterator.

    Args:
        obj (Any): The object to check.
    Returns:
        bool: ``True`` if the object is iterator, ``False`` otherwise.
    """
    try:
        iter(obj)
    except TypeError:
        return False
    return True


def is_empty(symbol: Any) -> TypeGuard[EmptyType]:
    """Check if a symbol is empty.

    Args:
        symbol (Any): The symbol to check.
    Returns:
        bool: ``True`` if the symbol is empty, ``False`` otherwise.
    """
    return symbol in Emptys
