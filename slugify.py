import re


def slugify(text: str) -> str:
    """Return a lowercase, hyphen-separated slug of ``text``.

    Spaces and underscores become single hyphens, characters other than
    a-z, 0-9 and hyphens are removed, and there are no leading, trailing
    or repeated hyphens.
    """
    text = text.lower()
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"[^a-z0-9-]", "", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")
