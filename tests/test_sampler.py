from yieldlang.combinators import select
from yieldlang.generator import TextGenerator
from yieldlang.sampler import ParserSampler


def test_parser_sampler():
    class G(TextGenerator):
        def top(self):
            yield select("A", "B", "C")
            yield select(1, 2, 3)
            yield select("XYZ", "456")

    sampler = ParserSampler()
    g = G(sampler)
    stream = ["!!!!", "A", "3", "X", "YZ", None]
    for s in stream:
        try:
            print(g.send(s), end="")
            for _ in range(len(s) - 1):
                print(g.send(None), end="")
        except StopIteration as e:
            print()
            print(e.value)
            break


if __name__ == "__main__":
    test_parser_sampler()
