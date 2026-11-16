"""Durations as people type them, e.g. "1h30m" or "45 m"."""
import re

_DURATION = re.compile(r"(?:([0-9]+)h)?(?:([0-9]+)m)?(?:([0-9]+)s)?")


def parse_duration(text: str) -> int:
    """Total seconds in a duration like "1h30m" (units h, m, s, in that order, each at most once).

    Spaces are ignored and case does not matter. Raises TypeError for non-strings and
    ValueError for anything else that is not a valid duration.
    """
    if not isinstance(text, str):
        raise TypeError(f"expected a str, got {type(text).__name__}")
    compact = text.replace(" ", "").lower()
    match = _DURATION.fullmatch(compact)
    if not compact or match is None:
        raise ValueError(f"invalid duration: {text!r}")
    hours, minutes, seconds = (int(g or 0) for g in match.groups())
    return hours * 3600 + minutes * 60 + seconds
