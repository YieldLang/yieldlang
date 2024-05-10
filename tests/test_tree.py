from yieldlang.combinators import select
from yieldlang.generator import TextGenerator
from yieldlang.tree import minify_ctx_tree


def test_base_tree():
    class G(TextGenerator):
        def top(self):
            yield "{", self.abc, "}"

        def abc(self):
            yield select("a", "b", "c")

    def gg():
        ret = yield from G()
        dic = minify_ctx_tree(ret)

        assert "value" in dic
        v = dic["value"]
        assert isinstance(v, str)
        assert len(v) == 3
        assert v.startswith("{")
        assert v.endswith("}")
        assert v[1] in "abc"

        assert "children" in dic
        c = dic["children"]

        assert isinstance(c, list)
        assert len(c) == 3

        c0, c1, c2 = c[0], c[1], c[2]
        assert "value" in c0
        assert "value" not in c1
        assert "value" in c2

        assert c0["value"] == "{"
        assert c2["value"] == "}"

        assert "name" in c1
        assert "children" in c1
        c1c = c1["children"]
        assert isinstance(c1c, list)
        assert len(c1c) == 1
        assert "value" in c1c[0]
        c1v = c1c[0]["value"]
        assert isinstance(c1v, str)
        assert c1v in "abc"

    list(gg())


if __name__ == "__main__":
    test_base_tree()
