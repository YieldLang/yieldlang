from enum import Enum
from typing import Iterable, TypeAlias

EmptyString = ""


class Token(Enum):
    EOF = -1
    Empty = 0


Strable: TypeAlias = str | int | float | bool
Symbol: TypeAlias = Strable | Token | None | Iterable
