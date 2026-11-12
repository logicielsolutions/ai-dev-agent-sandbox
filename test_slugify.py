import unittest

from slugify import slugify


class SlugifyTests(unittest.TestCase):
    def test_plain_words(self):
        self.assertEqual(slugify("hello world"), "hello-world")

    def test_mixed_case(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_punctuation(self):
        self.assertEqual(slugify("Hello, World!"), "hello-world")

    def test_repeated_spaces_and_underscores(self):
        self.assertEqual(slugify("hello   world__foo"), "hello-world-foo")

    def test_leading_trailing_separators(self):
        self.assertEqual(slugify("  --hello world--  "), "hello-world")


if __name__ == "__main__":
    unittest.main()
