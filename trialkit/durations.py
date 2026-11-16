"""Parsing of short duration strings such as '1h30m'."""
import re

_PATTERN = re.compile(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?", re.IGNORECASE)


def parse_duration(text: str) -> int:
    """Convert e.g. '1h30m' to seconds.

    Units are h, m, s in that order, each at most once; spaces are ignored and
    case does not matter. Raises ValueError for malformed input, TypeError for
    a non-string.
    """
    if not isinstance(text, str):
        raise TypeError(f"expected str, got {type(text).__name__}")
    compact = "".join(text.split())
    m = _PATTERN.fullmatch(compact)
    if not compact or m is None:
        raise ValueError(f"invalid duration: {text!r}")
    h, mi, s = (int(g) if g else 0 for g in m.groups())
    return h * 3600 + mi * 60 + s
