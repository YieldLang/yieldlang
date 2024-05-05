from typing import Iterable

from yieldlang.constants import EmptyString, Token
from yieldlang.sampler import BaseSampler
from yieldlang.types import (
    NonTerminal,
    Symbol,
    SymbolFn,
    SymbolProxy,
    is_callable,
    is_non_terminal,
    is_strable,
    is_symbol_proxy,
    is_token,
)


class TextGenerator:
    """
    A generator that generates text using a sampler.
    """

    def top(self) -> Symbol:
        """
        Get the top symbol of the generator.

        :warning: This method should be implemented by the subclass.
        """
        raise NotImplementedError

    def __init__(self, sampler: BaseSampler | None = None) -> None:
        """
        Initialize the generator with a sampler.
        """
        if sampler is None:
            sampler = BaseSampler.default()
        self.__sampler = sampler

    def __iter__(self) -> Iterable[str]:
        """
        Iterate over the generator.
        """
        return self.__iter_symbol(self.top)

    def __iter_symbol(self, symbol: Symbol) -> Iterable[str]:
        """
        Iterate over a symbol.
        """
        for token in self.__flatten(symbol):
            yield token

    def __flatten_non_terminal(self, nt: NonTerminal) -> Iterable[str]:
        """
        Flatten a non-terminal.
        """
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

    def __flatten_token(self, token: Token) -> Iterable[str]:
        """
        Flatten a token.
        """
        match token:
            case Token.EOF:
                raise EOFError
            case Token.EOS:
                raise StopIteration
            case Token.Empty:
                yield EmptyString
            case _:
                raise ValueError(f"Invalid token: {token}")

    def __flatten_symbol_proxy(self, proxy: SymbolProxy) -> Iterable[str]:
        """
        Flatten a symbol proxy.
        """
        try:
            fn: SymbolFn = getattr(self.__sampler, proxy.fn.__name__)
            symbol: Symbol = fn(*proxy.args, **proxy.kwargs)
        except (NotImplementedError, AttributeError):
            ff = fn.__name__
            cc = self.__sampler.__class__.__name__
            raise NotImplementedError(f"{ff} is not implemented in {cc}")
        yield from self.__flatten(symbol)

    def __flatten(self, symbol: Symbol) -> Iterable[str]:
        """
        Flatten a symbol.
        """
        if is_strable(symbol):
            yield str(symbol)
        elif symbol is None:
            yield EmptyString
        elif is_callable(symbol):
            yield from self.__flatten(symbol())
        elif is_symbol_proxy(symbol):
            yield from self.__flatten_symbol_proxy(symbol)
        elif is_non_terminal(symbol):
            yield from self.__flatten_non_terminal(symbol)
        elif is_token(symbol):
            yield from self.__flatten_token(symbol)
        else:
            raise TypeError(f"Invalid symbol: {symbol}")
