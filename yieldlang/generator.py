from dataclasses import dataclass
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
    is_nt_generator,
    is_proxy_symbol,
    is_strable,
    is_token,
)


class EOSError(Exception):
    """Raised when the end of the sequence is reached."""


@dataclass
class FlattenContext:
    """Context for flattening symbols."""

    max_depth: int | None = None
    """The maximum depth to flatten. If None, flatten all symbols."""
    cur_depth: int = 0
    """The current depth of flattening."""


class TextGenerator:
    """Generator that generates text using a sampler."""

    def top(self) -> Symbol:
        """Get the top symbol of the generator.

        Warning:
            This method should be implemented by the subclass.
        """
        raise NotImplementedError

    def __init__(self, sampler: BaseSampler | None = None) -> None:
        """Initialize the generator with a sampler."""
        self._sampler: BaseSampler = sampler or BaseSampler.default()
        """The sampler to use for sampling symbols."""
        self._iterator: Iterator[str] = self.__iter_symbol(self.top)
        """The iterator to generate text."""

    def __iter__(self) -> Iterator[str]:
        """Get the iterator."""
        return self._iterator

    def __next__(self) -> str:
        """Get the next token."""
        return next(self._iterator)

    def __iter_symbol(self, symbol: Symbol) -> Iterator[str]:
        """Iterate over a symbol."""
        try:
            ctx = FlattenContext(max_depth=None, cur_depth=0)
            for token in self._flatten(symbol, ctx):
                yield str(token)
        except EOFError:
            pass

    def _flatten_non_terminal(
        self, nt: NonTerminal, /, ctx: FlattenContext
    ) -> Iterator[Symbol]:
        """Flatten a non-terminal."""
        try:
            if is_nt_generator(nt):  # Must be a generator
                symbol = next(nt)
                while True:  # break when StopIteration or EOSError is raised
                    strs: list[str] = []
                    for s in self._flatten(symbol, ctx):
                        yield s
                        strs.append(str(s))
                    symbol = nt.send(EmptyString.join(strs))
            else:  # Must be an iterable
                for symbol in iter(nt):
                    yield from self._flatten(symbol, ctx)
        except (StopIteration, EOSError):
            pass

    def _process_token(self, token: Token) -> Iterator[str]:
        """Flatten a token."""
        match token:
            case Token.EOF:
                raise EOFError
            case Token.EOS:
                raise EOSError
            case Token.Empty:
                yield EmptyString
            case _:
                raise ValueError(f"Invalid token: {token}")

    def _flatten_proxy_symbol(
        self, proxy: ProxySymbol, ctx: FlattenContext
    ) -> Iterator[Symbol]:
        """Flatten a proxy symbol."""
        symbol = proxy.fn(self, *proxy.args, **proxy.kwargs)
        yield from self._flatten(symbol, ctx)

    def _flatten(
        self, symbol: Symbol, ctx: FlattenContext
    ) -> Iterator[Symbol]:
        """Flatten a symbol.

        Args:
            symbol (Symbol): The symbol to flatten.
            ctx (FlattenContext): The context for flattening.
        """
        ctx = FlattenContext(ctx.max_depth, cur_depth=ctx.cur_depth + 1)
        if ctx.max_depth is not None and ctx.cur_depth > ctx.max_depth:
            yield symbol
            return None

        match symbol:
            case _ if is_strable(symbol):
                yield str(symbol)
            case _ if is_empty(symbol):
                yield EmptyString
            case _ if is_callable(symbol):
                yield from self._flatten(symbol(), ctx)
            case _ if is_token(symbol):
                yield from self._process_token(symbol)
            case _ if is_proxy_symbol(symbol):
                yield from self._flatten_proxy_symbol(symbol, ctx)
            case _ if is_non_terminal(symbol):
                yield from self._flatten_non_terminal(symbol, ctx)
            case _:
                raise TypeError(f"Invalid symbol: {symbol}")
