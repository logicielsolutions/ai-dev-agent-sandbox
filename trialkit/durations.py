"""Human-readable durations."""


def format_duration(seconds: int) -> str:
    """Format whole seconds as e.g. "1h30m", "45s" or "25h1m1s", leaving out zero parts.

    Hours are not rolled up into days. Raises TypeError for anything that is not an
    int (bool and float included) and ValueError for a negative number.
    """
    if type(seconds) is not int:
        raise TypeError(f"seconds must be an int, not {type(seconds).__name__}")
    if seconds < 0:
        raise ValueError("seconds must not be negative")
    if seconds == 0:
        return "0s"
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    parts = [(hours, "h"), (minutes, "m"), (secs, "s")]
    return "".join(f"{value}{unit}" for value, unit in parts if value)
