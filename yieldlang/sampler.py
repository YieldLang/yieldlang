from random import choice as rand_choice

from yieldlang.types import Symbol


class BaseSampler:
    """A sampler that sample a symbol from a set of symbols."""

    def __init__(self) -> None:
        pass

    @staticmethod
    def default() -> "RandomSampler":
        """Get the default sampler."""
        return RandomSampler()

    def select(self, *args: Symbol) -> Symbol:
        """Select a symbol from a set of symbols."""
        raise NotImplementedError


class RandomSampler(BaseSampler):
    def select(self, *args: Symbol) -> Symbol:
        """Randomly select a symbol from a set of symbols."""
        return rand_choice(args)
