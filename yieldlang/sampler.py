import random
from typing import TYPE_CHECKING

from yieldlang.tree import YContextTree
from yieldlang.types import EmptyString, Symbol

if TYPE_CHECKING:
    from yieldlang.generator import TextGenerator


class BaseSampler:
    """Base class for samplers."""

    def __init__(self) -> None:
        self.inputs: list[int] = []

    @staticmethod
    def default() -> "RandomSampler":
        """Get the default sampler."""
        return RandomSampler()

    def select(
        self, g: "TextGenerator", ctx: YContextTree, *symbol: Symbol
    ) -> Symbol:
        """Select a symbol from a set of symbols.

        Warning:
            This method should be implemented by the subclass.
        """
        raise NotImplementedError


class RandomSampler(BaseSampler):
    """Random sampler."""

    def select(
        self, g: "TextGenerator", ctx: YContextTree, *symbol: Symbol
    ) -> Symbol:
        """Randomly select a symbol from a set of symbols."""
        return random.choice(symbol)


class ParserSampler(BaseSampler):
    def __init__(self) -> None:
        super().__init__()
        self.pt: int = -1

    def select(
        self, g: "TextGenerator", ctx: YContextTree, *symbol: Symbol
    ) -> Symbol:
        while True:
            strs = map(str, symbol)  # TODO: Implement first set
            for s in strs:
                p = self.pt
                flag = True
                for c in s:
                    p = yield from self._next_pt(p)
                    char = self._char(p)
                    if char != c:
                        flag = False
                        break
                    else:
                        yield char
                if flag:
                    self.pt = p
                    return s
            self.pt = yield from self._next_pt(self.pt)
            print("Bad Input!!!")

    def _char(self, i: int) -> str:
        s = self.inputs[i]
        return chr(s)

    def _cur_char(self) -> str:
        return self._char(self.pt)

    def _next_pt(self, i: int):
        while True:
            if i + 1 >= len(self.inputs):
                yield EmptyString
            else:
                return i + 1
