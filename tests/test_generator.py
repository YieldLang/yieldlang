from yieldlang.combinators import select
from yieldlang.constants import EmptyString, Token
from yieldlang.generator import TextGenerator


def test_y_a_eq_a():
    class TestGen(TextGenerator):
        def top(self):
            a = yield "A"
            assert a == "A"

    ret = EmptyString.join(TestGen().__iter__())
    assert ret == "A"


def test_y_seq_eq_join_seq():
    class TestGen(TextGenerator):
        def top(self):
            abc = yield ("A", "B", "C")
            assert abc == "ABC"

            abd = yield self.abd
            assert abd == "abd"

            abcd = yield list("ABCD")
            assert abcd == "ABCD"

            xabdy = yield ("x", self.abd, "y")
            assert xabdy == "xabdy"

        def abd(self):
            yield "a"
            yield "b"
            yield "d"

    ret = EmptyString.join(TestGen().__iter__())
    assert ret == "ABCabdABCDxabdy"


def test_y_eos():
    class TestGen(TextGenerator):
        def top(self):
            abc = yield ("A", "B", "C", Token.EOS, "D", "E", "F")
            assert abc == "ABC"

            abcf = yield self.abcf
            assert abcf == "ABCF"

            yield (abcf, abc, Token.EOS, "666")

        def abcf(self):
            yield "AB"
            yield ("C", Token.EOS, "D", "E")
            yield "F"
            yield Token.EOS
            yield "G"

    ret = EmptyString.join(TestGen().__iter__())
    assert ret == "ABCABCF" + "ABCF" + "ABC"


def test_y_strbale():
    class TestGen(TextGenerator):
        def top(self):
            a = yield 3.14
            assert a == "3.14"

            b = yield 15926
            assert b == "15926"

            c = yield "5"
            assert c == "5"

    ret = EmptyString.join(TestGen().__iter__())
    assert ret == "3.14159265"


def test_y_select():
    class TestGen(TextGenerator):
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
        EmptyString.join(TestGen().__iter__())


if __name__ == "__main__":
    test_y_a_eq_a()
    test_y_seq_eq_join_seq()
    test_y_eos()
    test_y_strbale()
    test_y_select()
