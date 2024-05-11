from dataclasses import dataclass, field
from typing import Generator, Optional, TypeAlias, TypedDict

from typing_extensions import NotRequired

from yieldlang.types import Symbol, is_empty


class YContextDict(TypedDict):
    """Dictionary for the context tree."""

    name: str
    """The name of the context."""
    max_depth: int
    """The maximum depth to flatten."""
    cur_depth: int
    """The current depth of flattening."""
    ret_value: list[Symbol] | Symbol | None
    """The return value of the context."""
    children: list["YContextDict"]
    """The children of the context."""


@dataclass
class YContextTree:
    """Context for YieldLang TextGenerator."""

    name: str = "Top"
    """The name of the context."""
    max_depth: int = -1
    """The maximum depth to flatten. If ``-1``, flatten all symbols."""
    cur_depth: int = 0
    """The current depth of flattening."""
    ret_value: list[Symbol] | Symbol | None = None
    """The return value of the context."""
    parent: Optional["YContextTree"] = None
    """The parent of the context."""
    children: list["YContextTree"] = field(default_factory=list)
    """The children of the context."""

    def to_dict(self) -> YContextDict:
        """Convert the context to a dictionary."""
        return {
            "name": self.name,
            "max_depth": self.max_depth,
            "cur_depth": self.cur_depth,
            "ret_value": self.ret_value,
            "children": [c.to_dict() for c in self.children],
        }


YGenerator: TypeAlias = Generator[str, str | None, YContextTree]
"""Type alias for a generator that generates text."""


class YMiniTree(TypedDict):
    """YieldLang mini tree type."""

    name: NotRequired[str]
    """Name of the y-mini tree. Not required if root or leaf."""
    value: NotRequired[str]
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
        if isinstance(value, list):
            ret_dict["value"] = "".join(map(str, value))
        elif isinstance(value, str):
            ret_dict["value"] = value
        else:
            ret_dict["value"] = str(value)

    children_len = len(ctx.children)

    if children_len == 1:
        children = list(map(minify_ctx_tree, find(ctx.children[0])))
        ret_dict["children"] = children
    elif children_len > 1:
        children = list(map(minify_ctx_tree, ctx.children))
        ret_dict["children"] = children

    return ret_dict
