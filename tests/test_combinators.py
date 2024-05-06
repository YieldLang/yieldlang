from yieldlang.combinators import select
from yieldlang.generator import TextGenerator
from yieldlang.types import EmptyString


def test_y_select():
    class G(TextGenerator):
        def top(self):
            a = yield select("A", "B", "C")
            assert a in ("A", "B", "C")

            b = yield select("D", self.e, self.f)
            assert b in ("D", "E", "F")

        def e(self):
            yield "E"

        def f(self):
            yield "F"

    for _ in range(10):
        EmptyString.join(G().__iter__())


if __name__ == "__main__":
    test_y_select()
