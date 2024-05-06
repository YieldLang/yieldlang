from typing import Iterator

from yieldlang.sampler import BaseSampler
from yieldlang.types import (
    EmptyString,
    NonTerminal,
    ProxySymbol,
    Symbol,
    Token,
    is_callable,
    is_empty,
    is_non_terminal,
    is_strable,
    is_symbol_proxy,
    is_token,
)


class TextGenerator:
    """A generator that generates text using a sampler."""

    def top(self) -> Symbol:
        """Get the top symbol of the generator.

        Warning:
            This method should be implemented by the subclass.
        """
        raise NotImplementedError

    def __init__(self, sampler: BaseSampler | None = None) -> None:
        """Initialize the generator with a sampler."""
        if sampler is None:
            sampler = BaseSampler.default()
        self.__sampler = sampler
        self.__iterator = iter(self)

    def __next__(self) -> str:
        """Get the next token."""
        return next(self.__iterator)

    def __iter__(self) -> Iterator[str]:
        """Iterate over the generator."""
        return self.__iter_symbol(self.top)

    def __iter_symbol(self, symbol: Symbol) -> Iterator[str]:
        """Iterate over a symbol."""
        try:
            for token in self.__flatten(symbol):
                yield token
        except EOFError:
            pass

    def __flatten_non_terminal(self, nt: NonTerminal) -> Iterator[str]:
        """Flatten a non-terminal."""
        if not hasattr(nt, "send"):
            for symbol in nt:
                if symbol is Token.EOS:
                    break
                yield from self.__flatten(symbol)
        else:
            try:
                symbol = next(nt)
                while True:
                    if symbol is Token.EOS:
                        break
                    str_list: list[str] = []
                    for s in self.__flatten(symbol):
                        yield s
                        str_list.append(s)
                    symbol = nt.send(EmptyString.join(str_list))
            except StopIteration:
                pass

    def __flatten_token(self, token: Token) -> Iterator[str]:
        """Flatten a token."""
        match token:
            case Token.EOF:
                raise EOFError
            case Token.EOS:
                raise StopIteration
            case Token.Empty:
                yield EmptyString
            case _:
                raise ValueError(f"Invalid token: {token}")

    def __flatten_symbol_proxy(self, proxy: ProxySymbol) -> Iterator[str]:
        """Flatten a symbol proxy."""
        symbol = self.__sampler.process_symbol_proxy(proxy)
        yield from self.__flatten(symbol)

    def __flatten(self, symbol: Symbol) -> Iterator[str]:
        """Flatten a symbol."""
        if is_strable(symbol):
            yield str(symbol)
        elif is_empty(symbol):
            yield EmptyString
        elif is_callable(symbol):
            yield from self.__flatten(symbol())
        elif is_token(symbol):
            yield from self.__flatten_token(symbol)
        elif is_symbol_proxy(symbol):
            yield from self.__flatten_symbol_proxy(symbol)
        elif is_non_terminal(symbol):
            yield from self.__flatten_non_terminal(symbol)
        else:
            raise TypeError(f"Invalid symbol: {symbol}")
