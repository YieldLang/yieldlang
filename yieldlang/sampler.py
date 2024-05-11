import random
from typing import TYPE_CHECKING

from yieldlang.types import Symbol

if TYPE_CHECKING:
    from yieldlang.generator import TextGenerator


class BaseSampler:
    """Base class for samplers."""

    @staticmethod
    def default() -> "RandomSampler":
        """Get the default sampler."""
        return RandomSampler()

    def select(self, g: "TextGenerator", *symbol: Symbol) -> Symbol:
        """Select a symbol from a set of symbols.

        Warning:
            This method should be implemented by the subclass.
        """
        raise NotImplementedError


class RandomSampler(BaseSampler):
    """Random sampler."""

    def select(self, g: "TextGenerator", *symbol: Symbol) -> Symbol:
        """Randomly select a symbol from a set of symbols."""
        return random.choice(symbol)
