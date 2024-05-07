from yieldlang.combinators import repeat, select
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
        EmptyString.join(G())


def test_y_repeat():
    class G(TextGenerator):
        def top(self):
            a666 = yield ("a", repeat("6", 3))
            assert a666 == "a666"
            aaa = yield repeat(self.a, 3)
            assert aaa == "aaa"
            a12a12 = yield repeat((self.a, 1, 2), 2)
            assert a12a12 == "a12a12"

        def a(self):
            yield "a"

    EmptyString.join(G())


if __name__ == "__main__":
    test_y_select()
    test_y_repeat()
