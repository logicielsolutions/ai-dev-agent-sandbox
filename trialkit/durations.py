"""Parse short duration strings such as "1h30m" into seconds."""
import re

_DURATION = re.compile(r"(?:([0-9]+)h)?(?:([0-9]+)m)?(?:([0-9]+)s)?", re.IGNORECASE)


def parse_duration(text: str) -> int:
    """Turn a duration like "1h30m" into whole seconds (5400).

    Units are h, m and s, in that order, each at most once, at least one
    present. Numbers are whole and not negative. Surrounding whitespace is
    ignored and units may be upper or lower case. Anything else raises
    ValueError; a non-string raises TypeError.
    """
    if not isinstance(text, str):
        raise TypeError(f"expected a string, got {type(text).__name__}")
    match = _DURATION.fullmatch(text.strip())
    if match is None or not any(match.groups()):
        raise ValueError(f"invalid duration: {text!r}")
    hours, minutes, seconds = (int(part) if part else 0 for part in match.groups())
    return hours * 3600 + minutes * 60 + seconds
