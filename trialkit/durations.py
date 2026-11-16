"""Parse short duration strings such as "1h30m" into seconds."""
import re

_PATTERN = re.compile(r"(?:([0-9]+)h)?(?:([0-9]+)m)?(?:([0-9]+)s)?")


def parse_duration(text: str) -> int:
    """Return the number of seconds in `text`, e.g. "1h30m" -> 5400.

    Units are h, m and s, in that order, each at most once, with whole numbers.
    Spaces are ignored and case does not matter. Raises TypeError for a
    non-string and ValueError for anything else that does not match.
    """
    if not isinstance(text, str):
        raise TypeError(f"expected a string, got {type(text).__name__}")
    compact = "".join(text.split()).lower()
    match = _PATTERN.fullmatch(compact)
    if not compact or match is None:
        raise ValueError(f"invalid duration: {text!r}")
    hours, minutes, seconds = (int(g) if g else 0 for g in match.groups())
    return hours * 3600 + minutes * 60 + seconds
