from yieldlang.types import ProxySymbol, Symbol


def repeat(symbol: Symbol, n_times: int) -> Symbol:
    """Repeat a symbol ``n_times`` times.

    Args:
        symbol (Symbol): The symbol to repeat.
        n_times (int): The number of times to repeat the symbol.
    Returns:
        Symbol: The repeated symbol.
    """
    # Get an error: `yield from itertools.repeat`
    # See: https://github.com/YieldLang/yieldlang/commit/3cd965b26636e4b5a90ed7c4701c32391d0a9cad#r141767404
    for _ in range(n_times):
        yield symbol
    return None


def select(*args: Symbol) -> ProxySymbol:
    """Select a symbol from a set of symbols.

    Args:
        *args (Symbol): The symbols to select from.
    Returns:
        ProxySymbol: The selected symbol.
    """
    return ProxySymbol(select, *args)
