from typing import TypedDict

from typing_extensions import NotRequired

from yieldlang.types import YContextTree, is_empty


class YMiniTree(TypedDict):
    """YieldLang mini tree type."""

    name: NotRequired[str]
    """Name of the y-mini tree. Not required if root or leaf."""
    value: NotRequired[object]
    """Value of the y-mini tree. Required only if root or leaf."""
    children: NotRequired[list["YMiniTree"]]
    """Children of the y-mini tree. Not required if leaf."""


def minify_ctx_tree(ctx: YContextTree) -> YMiniTree:
    """Minify a y-context tree to a y-mini tree.

    Args:
        ctx (YContextTree): The y-context tree to minify.
    Returns:
        YMiniTree: The y-mini tree.
    """

    def find(ctx: YContextTree) -> list[YContextTree]:
        n = len(ctx.children)
        if n == 0:
            return [ctx]
        elif n == 1:
            return find(ctx.children[0])
        else:
            return ctx.children

    ret_dict: YMiniTree = {}
    name = ctx.name
    value = ctx.ret_value

    value_empty = is_empty(value)

    if name.startswith("Callable: "):
        ret_dict["name"] = name[10:]
    elif name.startswith("Empty"):
        ret_dict["value"] = ""

    if not value_empty:
        ret_dict["value"] = value

    children_len = len(ctx.children)

    if children_len == 1:
        children = list(map(minify_ctx_tree, find(ctx.children[0])))
        ret_dict["children"] = children
    elif children_len > 1:
        children = list(map(minify_ctx_tree, ctx.children))
        ret_dict["children"] = children

    return ret_dict
