from yieldlang.combinators import join, optional, repeat, select
from yieldlang.generator import TextGenerator
from yieldlang.types import EmptyString, Symbol
from yieldlang.utils import iter_not_empty


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

    for _ in range(100):
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


def test_y_optional():
    class G(TextGenerator):
        def top(self):
            a = yield optional("A")
            assert a in ("", "A")

            b = yield optional("B", "C", self.d)
            assert b in ("", "B", "C", "D")

        def d(self):
            yield "D"

    for _ in range(100):
        EmptyString.join(G())


def test_y_join():
    class G(TextGenerator):
        def top(self):
            a = yield join(", ", self.seq)
            assert a == "A, B, C, E"

            b = yield join(", ", 1234)
            assert b == "1234"

            c = yield join(", ", list("789"))
            assert c == "7, 8, 9"

            d = yield join(", ", (1, 2, 3))
            assert d == "1, 2, 3"

            e = yield join(0, join(1, range(3)))
            assert e == "001010102"

        def seq(self):
            yield "A"
            yield None
            yield "B"
            yield ("C", "E")

        def join(self, sep: Symbol, to_seq: Symbol):
            iterator = iter_not_empty(self._flatten(to_seq))
            for symbol in iterator:
                yield symbol
                break
            for symbol in iterator:
                yield sep
                yield symbol

    EmptyString.join(G())


if __name__ == "__main__":
    test_y_select()
    test_y_repeat()
    test_y_optional()
    test_y_join()
