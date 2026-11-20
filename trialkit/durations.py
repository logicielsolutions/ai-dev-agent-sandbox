"""Parse short duration strings such as "1h30m" into seconds."""

import re

# Hours, minutes and seconds, in that order, each at most once.
# ASCII digits only, so "-1h", "1.5h" and non-ASCII digits are rejected.
_DURATION = re.compile(
    r"(?:(?P<h>[0-9]+)h)?(?:(?P<m>[0-9]+)m)?(?:(?P<s>[0-9]+)s)?",
    re.IGNORECASE,
)


def parse_duration(text: str) -> int:
    """Return the number of seconds in a duration like "1h30m".

    Units are h, m and s, in that order, each used at most once, and at
    least one is required. Surrounding spaces are ignored and units may be
    upper or lower case. Numbers must be whole and not negative.

    Raises TypeError if text is not a string and ValueError if it is not a
    valid duration.
    """
    if not isinstance(text, str):
        raise TypeError(f"duration must be a string, not {type(text).__name__}")

    match = _DURATION.fullmatch(text.strip())
    if match is None or not any(match.groupdict().values()):
        raise ValueError(f"invalid duration: {text!r}")

    hours, minutes, seconds = (int(match[unit] or 0) for unit in ("h", "m", "s"))
    return hours * 3600 + minutes * 60 + seconds
