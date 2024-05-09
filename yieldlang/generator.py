from yieldlang.sampler import BaseSampler
from yieldlang.types import (
    EmptyString,
    EOSError,
    IteratorStr,
    IteratorSymbol,
    NonTerminal,
    ProxySymbol,
    Symbol,
    Token,
    YContextTree,
    YGenerator,
    is_callable,
    is_empty,
    is_non_terminal,
    is_nt_generator,
    is_proxy_symbol,
    is_strable,
    is_token,
)


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
        self._root_ctx = YContextTree(max_depth=None, cur_depth=0)
        """The root context for flattening symbols."""
        self._generator: YGenerator = self.__iter_symbol(self.top)
        """The iterator to generate text."""

    def __iter__(self) -> IteratorStr:
        """Get the iterator."""
        return self._generator

    def __next__(self) -> str:
        """Get the next token."""
        return next(self._generator)

    def __iter_symbol(self, symbol: Symbol) -> YGenerator:
        """Iterate over a symbol."""
        try:
            self._root_ctx.ret_value = ""
            for s in self._flatten(symbol, self._root_ctx):
                self._root_ctx.ret_value += str(s)
                yield str(s)
        except EOFError:
            pass
        return self._root_ctx

    def _flatten_non_terminal(
        self, nt: NonTerminal, ctx: YContextTree
    ) -> IteratorSymbol:
        """Flatten a non-terminal."""

        ctx.ret_value = ""  # Initialize

        def flatten_symbol(symbol: Symbol) -> IteratorSymbol:
            for s in self._flatten(symbol, ctx):
                ctx.ret_value += str(s)  # type: ignore
                yield s

        try:
            if is_nt_generator(nt):  # Must be a generator
                symbol = next(nt)
                while True:  # Break when StopIteration or EOSError is raised
                    index = len(ctx.ret_value)
                    yield from flatten_symbol(symbol)
                    symbol = nt.send(ctx.ret_value[index:])
            else:  # Must be an iterable
                for symbol in iter(nt):
                    yield from flatten_symbol(symbol)
        except (StopIteration, EOSError):
            pass

    def _process_token(self, token: Token) -> IteratorStr:
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
        self, proxy: ProxySymbol, ctx: YContextTree
    ) -> IteratorSymbol:
        """Flatten a proxy symbol."""
        symbol = proxy.fn(self, ctx, *proxy.args, **proxy.kwargs)
        yield from self._flatten(symbol, ctx)

    def _flatten(self, symbol: Symbol, ctx: YContextTree) -> IteratorSymbol:
        """Flatten a symbol.

        Args:
            symbol (Symbol): The symbol to flatten.
            ctx (FlattenContext): The context for flattening.
        """
        child = YContextTree(ctx.max_depth, cur_depth=ctx.cur_depth + 1)
        ctx.children.append(child)
        ctx = child

        if ctx.max_depth is not None and ctx.cur_depth > ctx.max_depth:
            ctx.ret_value = symbol
            yield symbol
            return None

        match symbol:
            case _ if is_empty(symbol):
                ctx.name = "Empty"
                yield EmptyString
            case _ if is_strable(symbol):
                ctx.name = "Strable"
                ctx.ret_value = symbol
                yield str(symbol)
            case _ if is_callable(symbol):
                ctx.name = f"Callable: {symbol.__name__}"
                yield from self._flatten(symbol(), ctx)
            case _ if is_token(symbol):
                ctx.name = f"Token: {symbol}"
                ctx.ret_value = symbol
                yield from self._process_token(symbol)
            case _ if is_proxy_symbol(symbol):
                ctx.name = f"Proxy: {symbol.fn.__name__}"
                yield from self._flatten_proxy_symbol(symbol, ctx)
            case _ if is_non_terminal(symbol):
                ctx.name = f"Iterable: {symbol.__class__.__name__}"
                yield from self._flatten_non_terminal(symbol, ctx)
            case _:
                ctx.name = "Invalid"
                raise TypeError(f"Invalid symbol: {symbol}")
