from typing import Iterable

from .constants import EmptyString, Token
from .types import (
    NonTerminal,
    Symbol,
    is_callable,
    is_non_terminal,
    is_strable,
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

    def __init__(self, sampler):
        self.sample = sampler

    def __iter__(self) -> Iterable[str]:
        return self.__iter_symbol(self.top)

    def __iter_symbol(self, symbol: Symbol) -> Iterable[str]:
        for token in self.__flatten(symbol):
            yield token

    def __flatten_non_terminal(self, nt: NonTerminal) -> Iterable[str]:
        if not hasattr(nt, "send"):
            for symbol in nt:
                yield from self.__flatten(symbol)
        else:
            try:
                symbol = next(nt)
                while True:
                    str_list: list[str] = []
                    for s in self.__flatten(symbol):
                        yield s
                        str_list.append(s)
                    symbol = nt.send(EmptyString.join(str_list))
            except StopIteration:
                pass

    def __flatten_token(self, token: Token) -> Iterable[str]:
        match token:
            case Token.EOF:
                raise EOFError
            case Token.Empty:
                yield EmptyString
            case _:
                raise ValueError(f"Invalid token: {token}")

    def __flatten(self, symbol: Symbol) -> Iterable[str]:
        if is_strable(symbol):
            yield str(symbol)
        elif symbol is None:
            yield EmptyString
        elif is_callable(symbol):
            yield from self.__flatten(symbol())
        elif is_non_terminal(symbol):
            yield from self.__flatten_non_terminal(symbol)
        elif is_token(symbol):
            yield from self.__flatten_token(symbol)
        else:
            raise TypeError(f"Invalid symbol: {symbol}")
