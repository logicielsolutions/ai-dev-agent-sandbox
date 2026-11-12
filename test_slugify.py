import unittest

from slugify import slugify


class SlugifyTests(unittest.TestCase):
    def test_plain_words(self):
        self.assertEqual(slugify("hello world"), "hello-world")

    def test_mixed_case(self):
        self.assertEqual(slugify("Hello WORLD Again"), "hello-world-again")

    def test_punctuation_removed(self):
        self.assertEqual(slugify("Hi, there! It's me."), "hi-there-its-me")

    def test_repeated_spaces_and_underscores(self):
        self.assertEqual(slugify("  foo__bar   baz_ "), "foo-bar-baz")

    def test_no_leading_trailing_or_repeated_hyphens(self):
        self.assertEqual(slugify("--a--b--"), "a-b")


if __name__ == "__main__":
    unittest.main()
