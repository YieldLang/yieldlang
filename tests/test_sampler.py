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
    stream = ["A", "3", "X", "YZ"]
    for s in stream:
        try:
            print(g.send(s), end="")
            for _ in range(len(s) - 1):
                print(g.send(None), end="")
        except StopIteration as e:
            print(e.value)
            break


def test_next_pointer():
    s = ParserSampler()
    s.inputs = [None, "", "123", "", "4", None, "5"]

    def g():
        s.pointer = yield from s._next_pointer(*s.pointer)
        assert s._cur_char() == "1"
        s.pointer = yield from s._next_pointer(*s.pointer)
        assert s._cur_char() == "2"
        s.pointer = yield from s._next_pointer(*s.pointer)
        assert s._cur_char() == "3"
        s.pointer = yield from s._next_pointer(*s.pointer)
        assert s._cur_char() == "4"
        s.pointer = yield from s._next_pointer(*s.pointer)
        assert s._cur_char() == "5"

    list(g())


if __name__ == "__main__":
    test_parser_sampler()
    test_next_pointer()
