from yieldlang.constants import EmptyString
from yieldlang.generator import TextGenerator


def test_y_a_eq_a():
    class TestGen(TextGenerator):
        def top(self):
            a = yield "A"
            assert a == "A"

    EmptyString.join(TestGen(...).__iter__())


def test_y_seq_eq_join_seq():
    class TestGen(TextGenerator):
        def top(self):
            a = yield ("A", "B", "C")
            assert a == "ABC"

            b = yield self.abd
            assert b == "abd"

            c = yield list("ABCD")
            assert c == "ABCD"

            d = yield ("1", self.abd, "2")
            assert d == "1abd2"

        def abd(self):
            yield "a"
            yield "b"
            yield "d"

    EmptyString.join(TestGen(...).__iter__())


if __name__ == "__main__":
    test_y_a_eq_a()
    test_y_seq_eq_join_seq()
