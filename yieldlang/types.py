from enum import Enum
from typing import (
    Callable,
    Generator,
    Iterable,
    Iterator,
    Literal,
    TypeAlias,
    TypeGuard,
)

from typing_extensions import TypeIs

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

IterableSymbol: TypeAlias = Iterable["Symbol"]
"""Type alias for an iterable symbol type."""

IteratorSymbol: TypeAlias = Iterator["Symbol"]
"""Type alias for an iterator symbol type."""

GeneratorSymbol: TypeAlias = Generator["Symbol", str, None]
"""Type alias for a generator symbol type."""

NonTerminal: TypeAlias = IterableSymbol | IteratorSymbol | GeneratorSymbol
"""Type alias for a non-terminal type."""

CallableSymbol: TypeAlias = Callable[[], "Symbol"]
"""Type alias for a callable symbol type."""

Symbol: TypeAlias = Terminal | NonTerminal | CallableSymbol | "ProxySymbol"
"""Type alias for a symbol type."""

ProxySymbolFn: TypeAlias = Callable[..., "ProxySymbol"]
"""Type alias for a proxy symbol function type."""


class ProxySymbol:
    """A proxy symbol that represents a symbol that is not yet evaluated."""

    def __init__(self, fn: ProxySymbolFn, *args: Symbol, **kwargs) -> None:
        self.fn = fn
        self.args = args
        self.kwargs = kwargs


def is_proxy_symbol(obj: object) -> TypeGuard[ProxySymbol]:
    """Check if an object is a proxy symbol.

    Args:
        obj (object): The object to check.
    Returns:
        bool: ``True`` if the object is a proxy symbol, ``False`` otherwise.
    """
    return isinstance(obj, ProxySymbol)


def is_non_terminal(symbol: Symbol) -> TypeGuard[NonTerminal]:
    """Check if a symbol is a non-terminal.

    Args:
        symbol (Symbol): The symbol to check.
    Returns:
        bool: ``True`` if the symbol is a non-terminal, ``False`` otherwise.
    """

    return is_iterable(symbol) and not isinstance(symbol, str)


def is_callable(symbol: Symbol) -> TypeGuard[Callable[[], Symbol]]:
    """Check if a symbol is callable.

    Args:
        symbol (Symbol): The symbol to check.
    Returns:
        bool: ``True`` if the symbol is callable, ``False`` otherwise.
    """
    return callable(symbol)


def is_strable(obj: object) -> TypeGuard[Strable]:
    """Check if an object is stringable.

    Args:
        obj (object): The object to check.
    Returns:
        bool: ``True`` if the object is stringable, ``False`` otherwise.
    """
    return isinstance(obj, (str, int, float))


def is_token(obj: object) -> TypeGuard[Token]:
    """Check if an object is a token.

    Args:
        obj (object): The object to check.
    Returns:
        bool: ``True`` if the object is a token, ``False`` otherwise.
    """
    return isinstance(obj, Token)


def is_iterable(obj: object) -> TypeGuard[Iterable]:
    """Check if an object is iterable.

    Args:
        obj (object): The object to check.
    Returns:
        bool: ``True`` if the object is iterable, ``False`` otherwise.
    """
    return isinstance(obj, Iterable)


def is_iterator(obj: object) -> TypeGuard[Iterator]:
    """Check if an object is an iterator.

    Args:
        obj (object): The object to check.
    Returns:
        bool: ``True`` if the object is an iterator, ``False`` otherwise.
    """
    return isinstance(obj, Iterator)


def is_generator(obj: object) -> TypeGuard[Generator]:
    """Check if an object is a generator.

    Args:
        obj (object): The object to check.
    Returns:
        bool: ``True`` if the object is a generator, ``False`` otherwise.
    """
    return isinstance(obj, Generator)


def is_nt_generator(obj: NonTerminal) -> TypeIs[GeneratorSymbol]:
    """Check if a non-terminal is a generator.

    Args:
        obj (NonTerminal): The non-terminal to check.
    Returns:
        bool: ``True`` if the non-terminal is a generator, ``False`` otherwise.
    """
    return hasattr(obj, "send")


def is_empty(symbol: object) -> TypeGuard[EmptyType]:
    """Check if a symbol is empty.

    Args:
        symbol (object): The symbol to check.
    Returns:
        bool: ``True`` if the symbol is empty, ``False`` otherwise.
    """
    return symbol in Emptys
