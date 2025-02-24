import unittest
from site_generator import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Title\n\nText"
        self.assertEqual(extract_title(markdown), "Title")

    def test_extract_title_no_title(self):
        markdown = "Text"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_h2(self):
        markdown = "## Title\n\nText"
        with self.assertRaises(ValueError):
            extract_title(markdown)
