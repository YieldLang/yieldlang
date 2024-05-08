import itertools
from typing import Iterator

from yieldlang.types import ProxySymbol, Symbol


def repeat(symbol: Symbol, n_times: int) -> Iterator[Symbol]:
    """Repeat a symbol ``n_times`` times.

    Args:
        symbol (Symbol): The symbol to repeat.
        n_times (int): The number of times to repeat the symbol.
    Returns:
        Symbol: The repeated symbol.
    """
    yield itertools.repeat(symbol, n_times)


def select(*args: Symbol) -> ProxySymbol:
    """Select a symbol from a set of symbols.

    Args:
        *args (Symbol): The symbols to select from.
    Returns:
        ProxySymbol: The proxy symbol that selects a symbol from the set.
    """
    return ProxySymbol(select, *args)
