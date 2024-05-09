from yieldlang.generator import TextGenerator
from yieldlang.types import EmptyString, Token


def test_y_a_eq_a():
    class G(TextGenerator):
        def top(self):
            a = yield "A"
            assert a == "A"

    ret = EmptyString.join(G())
    assert ret == "A"


def test_y_seq_eq_join_seq():
    class G(TextGenerator):
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

    ret = EmptyString.join(G())
    assert ret == "ABCabdABCDxabdy"


def test_y_eos():
    class G(TextGenerator):
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

    ret = EmptyString.join(G())
    assert ret == "ABCABCF" + "ABCF" + "ABC"


def test_y_eof():
    class G(TextGenerator):
        def top(self):
            yield "A"
            yield self.b

            ce = yield (self.c, self.d, "E")
            assert ce == "CE"

            yield self.f
            yield self.g

        def b(self):
            yield "B"

        def c(self):
            yield "C"

        def d(self):
            pass

        def f(self):
            yield "F"
            yield Token.EOF
            raise RuntimeError("This should not be reached")

        def g(self):
            yield "G"
            raise RuntimeError("This should not be reached")

    ret = EmptyString.join(G())
    assert ret == "ABCEF"


def test_y_from():
    class G(TextGenerator):
        def top(self):
            a = yield "A"
            assert a == "A"

            b = yield self.b
            assert b == "2"

            c = yield from self.b()
            assert c == "b"

        def b(self):
            yield "2"
            return "b"

    EmptyString.join(G())


def test_y_strale():
    class G(TextGenerator):
        def top(self):
            a = yield 3.14
            assert a == "3.14"

            b = yield 15926
            assert b == "15926"

            c = yield "5"
            assert c == "5"

    ret = EmptyString.join(G())
    assert ret == "3.14159265"


def test_y_fstring():
    class G(TextGenerator):
        def top(self):
            yield 1

            a3b5 = yield f"a{yield 3}{yield self.b}5"
            assert a3b5 == "a3b5"

        def b(self):
            yield "b"

    ret = EmptyString.join(G())
    assert ret == "13ba3b5"


def test_y_generator():
    class A(TextGenerator):
        def top(self):
            yield "A"

            bcd = yield (B, C, "D")
            assert bcd == "BCD"

    class B(TextGenerator):
        def top(self):
            yield "B"

    class C(TextGenerator):
        def top(self):
            yield "C"
            yield self.eof
            raise RuntimeError("This should not be reached")

        def eof(self):
            raise EOFError

    ret = EmptyString.join(A())
    assert ret == "ABCD"


def test_next_generator():
    class G(TextGenerator):
        def top(self):
            yield "A"

            bcd = yield ("B", "C", "D")
            assert bcd == "BCD"

            yield self.e
            yield (1, 2, 3)

        def e(self):
            yield "EF666"

    g = G()
    assert next(g) == "A"
    assert next(g) == "B"
    assert next(g) == "C"
    assert next(g) == "D"
    assert next(g) == EmptyString.join(g.e())
    assert EmptyString.join(g) == "123"


if __name__ == "__main__":
    test_y_a_eq_a()
    test_y_seq_eq_join_seq()
    test_y_eos()
    test_y_eof()
    test_y_from()
    test_y_strale()
    test_y_fstring()
    test_y_generator()
    test_next_generator()
