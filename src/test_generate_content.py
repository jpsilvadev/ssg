import unittest

from generate_content import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_h1(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_strips_whitespace(self):
        self.assertEqual(extract_title("#    Hello World   "), "Hello World")

    def test_first_h1_wins(self):
        md = "# First\n\nsome text\n\n# Second"
        self.assertEqual(extract_title(md), "First")

    def test_h1_not_on_first_line(self):
        md = "some intro text\n\n# The Title\n\nmore text"
        self.assertEqual(extract_title(md), "The Title")

    def test_ignores_lower_level_headings(self):
        md = "## Not this\n\n### Nor this\n\n# Yes this"
        self.assertEqual(extract_title(md), "Yes this")

    def test_hash_without_space_is_not_h1(self):
        with self.assertRaises(RuntimeError):
            extract_title("#NoSpace")

    def test_raises_when_no_h1(self):
        with self.assertRaises(RuntimeError):
            extract_title("## Subheading\n\njust a paragraph")

    def test_raises_on_empty_string(self):
        with self.assertRaises(RuntimeError):
            extract_title("")


if __name__ == "__main__":
    unittest.main()
