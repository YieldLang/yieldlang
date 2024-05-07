from random import choice as rand_choice

from yieldlang.types import CallableSymbol, ProxySymbol, Symbol


class BaseSampler:
    """A sampler that sample a symbol from a set of symbols."""

    def __init__(self) -> None:
        pass

    @staticmethod
    def default() -> "RandomSampler":
        """Get the default sampler."""
        return RandomSampler()

    def process_proxy_symbol(self, proxy: ProxySymbol) -> Symbol:
        """Process a proxy symbol.

        Args:
            proxy (ProxySymbol): A proxy symbol.
        Returns:
            Symbol: The result of the proxy symbol.
        Raises:
            NotImplementedError: If the function is not implemented in the sampler.
        """
        try:
            fn: CallableSymbol = getattr(self, proxy.fn.__name__)
            return fn(*proxy.args, **proxy.kwargs)
        except (AttributeError, NotImplementedError):
            ff = proxy.fn.__name__
            cc = self.__class__.__name__
            raise NotImplementedError(f"{ff} is not implemented in {cc}")

    def select(self, *args: Symbol) -> Symbol:
        """Select a symbol from a set of symbols."""
        raise NotImplementedError


class RandomSampler(BaseSampler):
    def select(self, *args: Symbol) -> Symbol:
        """Randomly select a symbol from a set of symbols."""
        return rand_choice(args)
