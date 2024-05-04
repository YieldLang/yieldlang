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

    EmptyString.join(TestGen(...).__iter__())


if __name__ == "__main__":
    test_y_a_eq_a()
    test_y_seq_eq_join_seq()
