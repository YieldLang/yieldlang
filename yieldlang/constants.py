from enum import Enum

EmptyString: str = ""
"""Empty string constant.
"""


class Token(Enum):
    """Token enumeration for the generator."""

    Empty = 0
    """Empty token."""
    EOF = 1
    """End of file token."""
    EOS = 2
    """End of statement token."""
