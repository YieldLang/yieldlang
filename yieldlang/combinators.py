from itertools import repeat as _repeat

from yieldlang.types import Symbol, SymbolProxy


def repeat(symbol: Symbol, n_times: int) -> Symbol:
    """
    Repeat a symbol `n_times` times.
    """
    yield from _repeat(symbol, n_times)
    return None


def select(*args: Symbol) -> SymbolProxy:
    """
    Select a symbol from a set of symbols.
    """
    return SymbolProxy(select, *args)
