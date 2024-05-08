import itertools
from typing import Iterator

from yieldlang.generator import TextGenerator
from yieldlang.types import EmptyString, ProxySymbol, Symbol
from yieldlang.utils import iter_not_empty


def repeat(symbol: Symbol, n_times: int) -> Iterator[Symbol]:
    """Repeat a symbol ``n_times`` times.

    Args:
        symbol (Symbol): The symbol to repeat.
        n_times (int): The number of times to repeat the symbol.
    Returns:
        Symbol: The repeated symbol.
    """
    yield itertools.repeat(symbol, n_times)


def select(*symbol: Symbol) -> ProxySymbol:
    """Select a symbol from a set of symbols.

    Args:
        *symbol (Symbol): The symbols to select from.
    Returns:
        ProxySymbol: The proxy symbol that selects a symbol from the set.
    """

    def generator(self: TextGenerator):
        yield self._sampler.select(*symbol)

    return ProxySymbol(generator)


def optional(*symbol: Symbol) -> ProxySymbol:
    """Make a symbol optional.

    Args:
        *symbol (Symbol): The symbol to make optional.
    Returns:
        Symbol: The optional symbol.
    """
    return select(EmptyString, *symbol)


def join(sep: Symbol, to_seq: Symbol) -> ProxySymbol:
    """Join a sequence of symbols with a separator.

    Args:
        sep (Symbol): The separator symbol.
        to_seq (Symbol): The symbol to join.
    Returns:
        Symbol: The joined symbol.
    """

    def generator(self: TextGenerator):
        iterator = iter_not_empty(self._flatten(to_seq))
        for symbol in iterator:
            yield symbol
            break
        for symbol in iterator:
            yield sep
            yield symbol

    return ProxySymbol(generator)
