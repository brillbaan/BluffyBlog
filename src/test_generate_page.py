import unittest

from generate_page import extract_title


class TestGeneratePage(unittest.TestCase):

    def test_extract_title(self):
        md = "# Hello"

        self.assertEqual(
            extract_title(md),
            "Hello",
        )

    def test_extract_title_whitespace(self):
        md = "   #     My Blog     "

        self.assertEqual(
            extract_title(md),
            "My Blog",
        )

    def test_extract_title_multiline(self):
        md = """
Some paragraph

# My Title

Another paragraph
"""

        self.assertEqual(
            extract_title(md),
            "My Title",
        )

    def test_extract_title_exception(self):
        md = """
## Heading

Paragraph
"""

        with self.assertRaises(Exception):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()
