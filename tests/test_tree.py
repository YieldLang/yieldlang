import json

from yieldlang.combinators import select
from yieldlang.generator import TextGenerator
from yieldlang.tree import YContextTree, minify_ctx_tree


def test_base_tree():
    class G(TextGenerator):
        def top(self):
            yield "{", self.abc, "}"

        def abc(self):
            yield select("a", "b", "c")

    def gg():
        ctx: YContextTree = yield from G()
        dic = minify_ctx_tree(ctx)

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


def test_ctx_tree():
    class G(TextGenerator):
        def top(self):
            yield "{", self.abc, "}"

        def abc(self):
            yield select("a", "b", "c")

    def gg():
        ctx: YContextTree = yield from G()
        assert ctx.ret_value is not None
        assert isinstance(ctx.ret_value, list)
        assert ctx.ret_value[0] == "{"
        assert ctx.ret_value[2] == "}"
        assert isinstance(ctx.ret_value[1], str)
        assert ctx.ret_value[1] in "abc"
        assert len(ctx.children) > 0

        def c0(ctx: YContextTree):
            return ctx.children[0]

        assert c0(ctx).name == "Callable: top"
        assert c0(ctx).ret_value is None
        assert c0(c0(ctx)).name == "Iterable: generator"
        assert c0(c0(ctx)).ret_value is None
        assert c0(c0(c0(ctx))).ret_value is None
        assert c0(c0(c0(ctx))).cur_depth == 3
        assert c0(c0(c0(c0(ctx)))).cur_depth == 4
        assert c0(c0(c0(c0(ctx)))).ret_value == "{"

        assert c0(ctx).parent is ctx
        assert c0(c0(ctx)).parent is c0(ctx)
        assert c0(c0(c0(ctx))).parent is c0(c0(ctx))
        assert c0(c0(c0(c0(ctx)))).parent is c0(c0(c0(ctx)))

        dic = ctx.to_dict()
        json_str = json.dumps(dic, indent=2)
        print(json_str)

    list(gg())


if __name__ == "__main__":
    test_base_tree()
    test_ctx_tree()
