"""Durations as short text, e.g. "1h30m"."""


def format_duration(seconds: int) -> str:
    """Format whole seconds as hours, minutes and seconds, e.g. 5400 -> "1h30m".

    Zero parts are left out; 0 is "0s". Hours are not rolled into days, so
    90061 -> "25h1m1s".

    Raises TypeError if `seconds` is not an int (bool and float included) and
    ValueError if it is negative.
    """
    if not isinstance(seconds, int) or isinstance(seconds, bool):
        raise TypeError(f"seconds must be an int, not {type(seconds).__name__}")
    if seconds < 0:
        raise ValueError("seconds must not be negative")
    if seconds == 0:
        return "0s"

    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    parts = [(hours, "h"), (minutes, "m"), (secs, "s")]
    return "".join(f"{value}{unit}" for value, unit in parts if value)
