from itertools import repeat as _repeat

from yieldlang.types import Symbol, SymbolProxy


def repeat(symbol: Symbol, n_times: int) -> Symbol:
    """Repeat a symbol ``n_times`` times.

    Args:
        symbol (Symbol): The symbol to repeat.
        n_times (int): The number of times to repeat the symbol.
    Returns:
        Symbol: The repeated symbol.
    """
    yield from _repeat(symbol, n_times)
    return None


def select(*args: Symbol) -> SymbolProxy:
    """Select a symbol from a set of symbols.

    Args:
        *args (Symbol): The symbols to select from.
    Returns:
        SymbolProxy: The selected symbol.
    """
    return SymbolProxy(select, *args)
