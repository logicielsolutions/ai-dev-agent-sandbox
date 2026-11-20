"""Parse short duration strings such as "1h30m" into seconds."""

import re

_DURATION = re.compile(
    r"(?:(?P<h>[0-9]+)h)?(?:(?P<m>[0-9]+)m)?(?:(?P<s>[0-9]+)s)?",
    re.IGNORECASE,
)


def parse_duration(text):
    """Return the number of seconds in a duration like "1h30m".

    Units are h, m and s, in that order, each at most once, and at least
    one is required. Each amount is a whole non-negative number. Units are
    case-insensitive and surrounding spaces are ignored.

    >>> parse_duration("1h30m")
    5400

    Raises TypeError if text is not a string, ValueError if it is not a
    valid duration.
    """
    if not isinstance(text, str):
        raise TypeError(f"duration must be a string, not {type(text).__name__}")
    stripped = text.strip()
    match = _DURATION.fullmatch(stripped)
    if not stripped or match is None:
        raise ValueError(f"invalid duration: {text!r}")
    hours, minutes, seconds = (int(match.group(u) or 0) for u in "hms")
    return hours * 3600 + minutes * 60 + seconds
