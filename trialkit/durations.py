"""Human-readable durations, e.g. 5400 seconds -> "1h30m"."""


def format_duration(seconds: int) -> str:
    """Format a whole number of seconds as hours, minutes and seconds.

    Zero parts are left out ("1h5s", "1h"); 0 is "0s". Hours are not rolled
    into days, so 90061 is "25h1m1s".

    Raises TypeError for anything that is not an int (bool and float included)
    and ValueError for a negative number.
    """
    if isinstance(seconds, bool) or not isinstance(seconds, int):
        raise TypeError(f"seconds must be an int, not {type(seconds).__name__}")
    if seconds < 0:
        raise ValueError("seconds must not be negative")
    if seconds == 0:
        return "0s"
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    parts = [(hours, "h"), (minutes, "m"), (secs, "s")]
    return "".join(f"{value}{unit}" for value, unit in parts if value)
