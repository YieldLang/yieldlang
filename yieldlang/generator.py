from yieldlang.sampler import BaseSampler
from yieldlang.tree import YContextTree, YGenerator
from yieldlang.types import (
    EmptyString,
    EOSError,
    IteratorStr,
    IteratorSymbol,
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


class TextGenerator:
    """Generator that generates text using a sampler."""

    def top(self) -> Symbol:
        """Get the top symbol of the generator.

        Warning:
            This method should be implemented by the subclass.
        """
        raise NotImplementedError

    def send(self, value: str | None) -> str:
        self._sampler.inputs.append(value)
        if self._generator.gi_running:
            return self._generator.send(value)
        return next(self._generator)

    def __init__(self, sampler: BaseSampler | None = None) -> None:
        """Initialize the generator with a sampler."""
        self._sampler: BaseSampler = sampler or BaseSampler.default()
        """The sampler to use for sampling symbols."""
        self._top_ctx: YContextTree = YContextTree(max_depth=-1, cur_depth=0)
        """The root context for flattening symbols."""
        self._cur_ctx: YContextTree = self._top_ctx
        """The current context for flattening symbols."""
        self._generator: YGenerator = self._iter_symbol(self.top)
        """The generator for the text."""

    def __iter__(self) -> YGenerator:
        """Get the generator."""
        return self._generator

    def __next__(self) -> str:
        """Get the next token."""
        return next(self._generator)

    def _iter_symbol(self, symbol: Symbol) -> YGenerator:
        """Iterate over a symbol."""
        try:
            self._top_ctx.ret_value = []
            for s in self._flatten(symbol, self._top_ctx):
                self._top_ctx.ret_value.append(s)
                yield str(s)
        except EOFError:
            pass
        return self._top_ctx

    def _flatten_non_terminal(
        self, nt: NonTerminal, ctx: YContextTree
    ) -> IteratorSymbol:
        """Flatten a non-terminal."""
        try:
            if is_nt_generator(nt):  # Must be a generator
                symbol = next(nt)
                while True:  # Break when StopIteration or EOSError is raised
                    strs: list[str] = []
                    for s in self._flatten(symbol, ctx):
                        strs.append(str(s))
                        yield s
                    symbol = nt.send("".join(strs))
            else:  # Must be an iterable
                for symbol in iter(nt):
                    yield from self._flatten(symbol, ctx)
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
            ctx (YContextTree): The context for flattening.
        """
        self._cur_ctx = ctx = self._new_child_ctx(ctx)
        if ctx.max_depth > -1 and ctx.cur_depth > ctx.max_depth:
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
                yield symbol
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
                ctx.name = f"Invalid: {symbol}"
                raise TypeError(f"Invalid symbol: {symbol}")

    def _new_child_ctx(self, parent: YContextTree) -> YContextTree:
        """Create a new child context.

        Args:
            parent (YContextTree): The parent context.
        Returns:
            YContextTree: The child context.
        """
        child = YContextTree()
        child.cur_depth = parent.cur_depth + 1
        child.max_depth = parent.max_depth
        parent.children.append(child)
        child.parent = parent
        return child
