import random
from typing import TYPE_CHECKING

from yieldlang.tree import YContextTree
from yieldlang.types import EmptyString, Symbol

if TYPE_CHECKING:
    from yieldlang.generator import TextGenerator


class BaseSampler:
    """Base class for samplers."""

    def __init__(self) -> None:
        self.inputs: list[str | None] = []

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
        self.pointer = (0, -1)

    def select(
        self, g: "TextGenerator", ctx: YContextTree, *symbol: Symbol
    ) -> Symbol:
        strs = map(str, symbol)  # TODO: Implement first set
        # print(symbol, self.pointer, self.inputs)
        for s in strs:
            p = self.pointer
            flag = True
            for c in s:
                p = yield from self._next_pointer(*p)
                char = self._char(*p)
                if char != c:
                    flag = False
                    break
                else:
                    yield char
            if flag:
                self.pointer = p
                return s
        raise EOFError

    def _char(self, i: int, j: int) -> str:
        s = self.inputs[i]
        assert s
        return s[j]

    def _cur_char(self) -> str:
        return self._char(*self.pointer)

    def _next_pointer(self, i: int, j: int):
        while True:
            try:
                while not self.inputs[i]:
                    i += 1
                    j = -1
                s = self.inputs[i]
                assert s
                j += 1
                if j >= len(s):
                    i += 1
                    j = 0
                while not self.inputs[i]:
                    i += 1
                return i, j
            except IndexError:
                yield EmptyString
