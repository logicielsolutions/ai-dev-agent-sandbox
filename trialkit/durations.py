"""Human-readable durations, as shown on the board (for example "1h30m")."""


def format_duration(seconds: int) -> str:
    """Format a whole number of seconds as hours, minutes and seconds, leaving out zero parts.

    5400 -> "1h30m", 3605 -> "1h5s", 0 -> "0s". Hours are not rolled into days.
    Raises TypeError for anything that is not an int (bool and float included)
    and ValueError for a negative number.
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
