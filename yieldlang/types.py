from enum import Enum
from typing import Iterable, TypeAlias

EmptyString = ""
"""
Empty string constant.
"""


class Token(Enum):
    """Token enumeration for the generator."""

    EOF = 0
    Empty = 1


Strable: TypeAlias = str | int | float | bool
"""
Type alias for a stringable type.
"""
Symbol: TypeAlias = Strable | Token | None | Iterable
"""
Type alias for a symbol type.
"""
